from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn
import os
import json
import urllib.request
import urllib.error
from urllib.parse import urlsplit
import ssl
import socket
import time
from contextlib import asynccontextmanager

DEFAULT_QDRANT_URL = "https://e1b44e0a-3fd9-48b2-b529-a9dcd260c23a.ca-central-1-0.aws.cloud.qdrant.io"
QDRANT_URL = os.environ.get("QDRANT_URL", DEFAULT_QDRANT_URL)
QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY", "")

COLLECTION_NAME = "anas_perfume_catalog_v1_1_multilingual_e5_small_384"
HEADERS = {
    "api-key": QDRANT_API_KEY,
    "Content-Type": "application/json"
}

CATALOG_CACHE = []

def catalog_error(exc):
    if isinstance(exc, urllib.error.HTTPError):
        return f"http_{exc.code}"
    cause = exc.reason if isinstance(exc, urllib.error.URLError) else exc
    if isinstance(cause, ssl.SSLError):
        return "tls_error"
    if isinstance(cause, socket.gaierror):
        return "dns_error"
    if isinstance(cause, TimeoutError):
        return "timeout"
    if isinstance(cause, OSError):
        return "connection_error"
    if isinstance(exc, (ValueError, TypeError, AttributeError, KeyError)):
        return "invalid_request_or_response"
    return "unclassified_error"


def fetch_all_perfumes():
    try:
        origin = urlsplit(QDRANT_URL)
        configured_origin = (origin.scheme.lower(), origin.hostname, origin.port or 443)
        default_origin = ("https", urlsplit(DEFAULT_QDRANT_URL).hostname, 443)
        matches_default_origin = configured_origin == default_origin
        has_base_path = origin.path not in ("", "/")
    except ValueError:
        matches_default_origin = False
        has_base_path = None
    settings = {
        "url_source": "environment" if "QDRANT_URL" in os.environ else "default",
        "matches_default_origin": matches_default_origin,
        "has_base_path": has_base_path,
        "key_present": bool(QDRANT_API_KEY.strip()),
        "collection": COLLECTION_NAME,
    }
    print("ANAS_QDRANT_CONFIG", json.dumps(settings), flush=True)
    all_points = []
    offset = None
    while True:
        body = {
            "limit": 15,
            "with_payload": True,
            "with_vectors": False
        }
        if offset:
            body["offset"] = offset
        
        success = False
        retries = 3
        points = []
        result = {}
        
        while retries > 0 and not success:
            try:
                req = urllib.request.Request(
                    f"{QDRANT_URL}/collections/{COLLECTION_NAME}/points/scroll",
                    data=json.dumps(body).encode("utf-8"),
                    headers=HEADERS,
                    method="POST"
                )
                with urllib.request.urlopen(req, timeout=30) as res:
                    result = json.loads(res.read().decode("utf-8"))["result"]
                    points = result["points"]
                    if not isinstance(points, list):
                        raise ValueError("invalid points format")
                    if not all_points:
                        print(f"ANAS_QDRANT_READ http={res.status} first_page_points={len(points)}", flush=True)
                    success = True
            except Exception as exc:
                retries -= 1
                if retries == 0:
                    print(f"ANAS_QDRANT_READ failure={catalog_error(exc)} loaded_points={len(all_points)}", flush=True)
                time.sleep(1)
                
        if not success or not points:
            break
            
        all_points.extend(points)
        offset = result.get("next_page_offset")
        if not offset:
            break
            
    return all_points

@asynccontextmanager
async def lifespan(app: FastAPI):
    global CATALOG_CACHE
    print("🔄 جاري تحميل الكتالوج إلى ذاكرة الخادم السحابي...")
    CATALOG_CACHE = fetch_all_perfumes()
    print(f"ANAS_CATALOG loaded_points={len(CATALOG_CACHE)}", flush=True)
    yield

app = FastAPI(
    title="ANAS Perfume Recommendation Engine API",
    version="1.2.0",
    lifespan=lifespan
)

class CloudSessionManager:
    def __init__(self):
        self._store = {}
    
    def get_session(self, session_id: str):
        return self._store.get(session_id)
        
    def save_session(self, session_id: str, session_data: dict):
        self._store[session_id] = session_data
        
    def delete_session(self, session_id: str):
        if session_id in self._store:
            del self._store[session_id]

session_manager = CloudSessionManager()

class SessionAdvisor:
    def __init__(self, perfumes, stored_state=None):
        self.perfumes = perfumes
        self.session = stored_state or {
            "concentration": None,
            "family": None,
            "preference": None,
            "active_codes": []
        }

    def parse_natural_language(self, text):
        t = text.lower()
        extracted = {}
        if any(w in t for w in ["بارفيوم", "برفيوم", "edp", "parfum", "ثقيل"]):
            extracted["concentration"] = "Eau de Parfum"
        elif any(w in t for w in ["تواليت", "edt", "toilette", "خفيف", "يومي"]):
            extracted["concentration"] = "Eau de Toilette"
            
        if any(w in t for w in ["خشب", "خشبي", "woody", "أخشاب"]):
            extracted["family"] = "woody"
        elif any(w in t for w in ["زهور", "زهري", "floral", "ورد"]):
            extracted["family"] = "floral"
        elif any(w in t for w in ["حمضيات", "منعش", "citrus", "فواكه"]):
            extracted["family"] = "citrus"
        elif any(w in t for w in ["توابل", "حار", "spicy", "بهارات"]):
            extracted["family"] = "spicy"
        elif any(w in t for w in ["عود", "oud"]):
            extracted["family"] = "oud"

        if any(w in t for w in ["انتعاش", "صيف", "نهار", "fresh"]):
            extracted["preference"] = "freshness"
        elif any(w in t for w in ["دافئ", "شتاء", "مساء", "فخم", "warm"]):
            extracted["preference"] = "warmth"
        elif any(w in t for w in ["حلو", "سويت", "فانيليا", "sweet"]):
            extracted["preference"] = "sweetness"
            
        return extracted

    def check_invalidation(self, extracted):
        changes = []
        for key in ["concentration", "family", "preference"]:
            new_val = extracted.get(key)
            old_val = self.session.get(key)
            if new_val and old_val and new_val != old_val:
                changes.append(f"تعديل {key}: من [{old_val}] إلى [{new_val}]")
                self.session[key] = new_val
            elif new_val and not old_val:
                self.session[key] = new_val
                
        if changes and self.session["active_codes"]:
            self.session["active_codes"] = []
            return True, changes
        return False, []

    def check_missing_info(self):
        if not self.session["family"] and not self.session["preference"]:
            return "لأرشح لك الكود الأدق من كتالوجنا الموثق: هل تفضل الطابع الخشبي الدافئ، أم الحمضي المنعش، أم الزهري؟"
        if not self.session["concentration"]:
            return "هل تفضل تركيز (Eau de Parfum) لثبات أعلى وفوحان أغنى، أم (Eau de Toilette) لاستخدام أخف؟"
        return None

    def build_grounded_justification(self, payload):
        olfactory = payload.get("olfactory_profile", {})
        notes = olfactory.get("notes", [])[:4]
        attrs = olfactory.get("attributes", {})
        evd_ids = olfactory.get("evidence_ids", [])
        commercial = payload.get("private_commercial_identity", {})
        code = payload.get("public_display_code")

        dominant_traits = []
        if attrs.get("warmth", 0) >= 4:
            dominant_traits.append(f"دفء عالٍ ({attrs['warmth']}/5)")
        if attrs.get("freshness", 0) >= 4:
            dominant_traits.append(f"انتعاش واضح ({attrs['freshness']}/5)")
        if attrs.get("woody", 0) >= 3:
            dominant_traits.append(f"طابع خشبي ({attrs['woody']}/5)")
        if attrs.get("spicy", 0) >= 3:
            dominant_traits.append(f"لمسة توابل ({attrs['spicy']}/5)")
            
        traits_str = "، ".join(dominant_traits) if dominant_traits else "توازن معتدل"
        notes_str = ", ".join(notes) if notes else "غير محددة"
        
        return {
            "title": f"الكود المعتمد: [{code}]",
            "public_display_code": code,
            "concentration": commercial.get("concentration"),
            "technical_justification": f"السمات الموثقة: {traits_str}",
            "primary_notes": notes_str,
            "evidence_references": evd_ids
        }

    def process(self, user_text):
        extracted = self.parse_natural_language(user_text)
        invalidated, changes = self.check_invalidation(extracted)
        
        response_data = {
            "invalidation_triggered": invalidated,
            "changes": changes
        }
        
        clarification = self.check_missing_info()
        if clarification:
            response_data["clarification_question"] = clarification
            response_data["recommendations"] = []
            return response_data, self.session
            
        candidates = []
        for pt in self.perfumes:
            p = pt.get("payload", {})
            if p.get("eligibility_state") != "ELIGIBLE":
                continue
            comm = p.get("private_commercial_identity", {})
            olf = p.get("olfactory_profile", {})
            
            if self.session["concentration"] and self.session["concentration"].lower() not in comm.get("concentration", "").lower():
                continue
            if self.session["family"] and not any(self.session["family"] in f.lower() for f in olf.get("families", [])):
                continue
                
            attrs = olf.get("attributes", {})
            pref_key = self.session["preference"] or "warmth"
            score = attrs.get(pref_key, 0) + attrs.get("woody", 0)
            candidates.append((score, p))
            
        candidates.sort(key=lambda x: x[0], reverse=True)
        
        if not candidates:
            response_data["message"] = "لا يوجد عطر مؤهل في الكتالوج يجمع بين هذه القيود بدقة."
            response_data["recommendations"] = []
            return response_data, self.session
            
        top_3 = [c[1] for c in candidates[:3]]
        self.session["active_codes"] = [item.get("public_display_code") for item in top_3]
        
        response_data["recommendations"] = [
            self.build_grounded_justification(item) for item in top_3
        ]
        return response_data, self.session

CHAT_PAGE = r"""<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#f7f5ef">
  <title>ANAS | مستشارك العطري</title>
  <style>
    :root { color-scheme: light; --ink: #233b32; --muted: #56685e; --line: #d5dacf; --paper: #f7f5ef; }
    * { box-sizing: border-box; }
    body { margin: 0; background: var(--paper); color: var(--ink); font-family: Tahoma, Arial, sans-serif; line-height: 1.8; }
    main { width: min(100%, 47rem); margin: auto; padding: clamp(14px, 4vw, 40px); }
    header { display: flex; align-items: baseline; justify-content: space-between; gap: 1rem; border-bottom: 1px solid var(--line); padding-bottom: .75rem; }
    h1 { font-size: clamp(1.2rem, 4vw, 1.65rem); margin: 0; font-weight: 600; }
    .wordmark { font: 600 1.6rem Georgia, serif; letter-spacing: .14em; }
    #messages { display: flex; flex-direction: column; align-items: flex-start; gap: .9rem; margin: 1.3rem 0; }
    article { max-width: 92%; border: 1px solid var(--line); background: #fffefa; padding: .75rem 1rem; border-radius: 1rem .25rem 1rem 1rem; overflow-wrap: anywhere; }
    article.user { align-self: flex-end; background: #e4ede3; border-color: #d0dbd0; border-radius: .25rem 1rem 1rem 1rem; }
    article b { color: var(--muted); font-size: .8rem; }
    article p { margin: .15rem 0 0; white-space: pre-wrap; }
    ul { margin-block: .35rem 0; padding-inline-start: 1.4rem; }
    form { border-top: 1px solid var(--line); padding-top: .8rem; }
    label { display: block; font-weight: 600; margin-bottom: .3rem; }
    textarea { display: block; width: 100%; padding: .8rem; background: #fffefa; border: 1px solid #aab8ae; border-radius: .65rem; resize: vertical; font: inherit; color: var(--ink); }
    :focus-visible { outline: 3px solid #587358; outline-offset: 3px; }
    .actions { display: flex; align-items: center; gap: 1rem; margin-top: .6rem; }
    button { background: var(--ink); color: white; border: 0; border-radius: .55rem; padding: .5rem 1.4rem; min-height: 44px; font: inherit; cursor: pointer; }
    button:disabled { opacity: .6; cursor: wait; }
    #status { color: var(--muted); font-size: .9rem; }
    #status.error { color: #913b2c; }
  </style>
</head>
<body>
  <main>
    <header><h1>مستشارك العطري</h1><span class="wordmark" lang="en" dir="ltr">ANAS</span></header>
    <section id="messages" role="log" aria-label="المحادثة" aria-live="polite">
      <article><b>مستشار ANAS</b><p>ما الطابع العطري الذي تفضّله؟</p></article>
    </section>
    <form id="chat">
      <label for="message">رسالتك</label>
      <textarea id="message" rows="2" required placeholder="مثلاً، أحب العطور الزهرية"></textarea>
      <div class="actions"><button type="submit">إرسال</button><span id="status" role="status"></span></div>
    </form>
    <noscript>فعّل JavaScript في المتصفح لإرسال الرسائل.</noscript>
  </main>
  <script>
    const form = document.querySelector('#chat');
    const input = document.querySelector('#message');
    const button = form.querySelector('button');
    const status = document.querySelector('#status');
    const messages = document.querySelector('#messages');
    const sessionId = Array.from(crypto.getRandomValues(new Uint8Array(16)),
      byte => byte.toString(16).padStart(2, '0')).join('');

    function addMessage(speaker, message, codes = []) {
      const bubble = document.createElement('article');
      bubble.className = speaker;
      const label = document.createElement('b');
      label.textContent = speaker === 'user' ? 'أنت' : 'مستشار ANAS';
      const body = document.createElement('p');
      body.textContent = message;
      bubble.append(label, body);
      if (codes.length) {
        const list = document.createElement('ul');
        for (const code of codes) {
          const item = document.createElement('li');
          const value = document.createElement('bdi');
          value.textContent = code;
          item.append('رمز العطر ', value);
          list.append(item);
        }
        bubble.append(list);
      }
      messages.append(bubble);
      return bubble;
    }

    function showReply(result) {
      if (!result || !Array.isArray(result.recommendations)) throw new Error('invalid');
      let message = result.clarification_question || result.message || '';
      const codes = [...new Set(result.recommendations.map(item => item.public_display_code)
        .filter(code => typeof code === 'string' && /^[0-9]{4}$/.test(code)))];
      if (!message && codes.length) message = 'هذه الرموز التي اقترحها المحرك بناءً على رسائلك:';
      if (!message) message = 'لا يتوفر اقتراح برمز صالح للعرض.';
      if (result.invalidation_triggered) {
        for (const list of messages.querySelectorAll('article ul')) {
          const withdrawn = document.createElement('small');
          withdrawn.textContent = 'سُحبت هذه الرموز بعد تعديل التفضيلات.';
          list.replaceWith(withdrawn);
        }
        message = 'بعد تحديث تفضيلاتك، سُحبت الاقتراحات السابقة.\n' + message;
      }
      addMessage('advisor', message, codes);
    }

    form.addEventListener('submit', async event => {
      event.preventDefault();
      const message = input.value.trim();
      if (!message || button.disabled) return;
      button.disabled = true;
      input.readOnly = true;
      status.className = '';
      status.textContent = 'بانتظار رد المحرك…';
      const pending = addMessage('user', message);
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), 120000);
      try {
        const response = await fetch('/api/v1/recommend', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({session_id: sessionId, message}),
          signal: controller.signal
        });
        if (!response.ok) throw new Error(String(response.status));
        const data = await response.json();
        if (data.session_id !== sessionId) throw new Error('invalid');
        showReply(data.result);
        input.value = '';
        status.textContent = '';
      } catch (error) {
        pending.remove();
        status.className = 'error';
        status.textContent = error.message === '503'
          ? 'الكتالوج غير متاح حاليًا. يمكنك إعادة إرسال رسالتك لاحقًا.'
          : 'تعذّر استلام الرد. رسالتك محفوظة في الحقل للمحاولة مرة أخرى.';
      } finally {
        clearTimeout(timer);
        input.readOnly = false;
        button.disabled = false;
        form.scrollIntoView({block: 'nearest'});
      }
    });
  </script>
</body>
</html>"""


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def chat_page():
    return CHAT_PAGE


class QueryRequest(BaseModel):
    session_id: str
    message: str

@app.post("/api/v1/recommend")
def recommend_endpoint(req: QueryRequest):
    if not CATALOG_CACHE:
        raise HTTPException(status_code=503, detail="Catalog is not loaded yet. Please try later.")
        
    stored_state = session_manager.get_session(req.session_id)
    advisor = SessionAdvisor(CATALOG_CACHE, stored_state=stored_state)
    result, updated_state = advisor.process(req.message)
    session_manager.save_session(req.session_id, updated_state)
    
    return {"session_id": req.session_id, "result": result}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import os
import json
import urllib.request
import time
from contextlib import asynccontextmanager

QDRANT_URL = os.environ.get("QDRANT_URL", "https://e1b44e0a-3fd9-48b2-b529-a9dcd260c23a.ca-central-1-0.aws.cloud.qdrant.io")
QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY", "")

COLLECTION_NAME = "anas_perfume_catalog_v1_1_multilingual_e5_small_384"
HEADERS = {
    "api-key": QDRANT_API_KEY,
    "Content-Type": "application/json"
}

CATALOG_CACHE = []

def fetch_all_perfumes():
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
                    result = json.loads(res.read().decode("utf-8")).get("result", {})
                    points = result.get("points", [])
                    success = True
            except Exception:
                retries -= 1
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
    print(f"✅ تم تحميل إجمالي {len(CATALOG_CACHE)} عطر بنجاح.")
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
        visibility = payload.get("public_visibility", {})
        commercial = payload.get("private_commercial_identity", {})
        
        if visibility.get("show_commercial_identity") is True:
            title = f"الكود [{payload.get('public_display_code')}] - {commercial.get('perfume_name_canonical_candidate')}"
        else:
            title = f"الكود المعتمد: [{payload.get('public_display_code')}]"
            
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
            "title": title,
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

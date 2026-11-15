"""ANAS-G. The mobile form and the JSON API use the same session and evidence matcher."""
import hashlib
import html
import json
import logging
import os
import re
import secrets
import threading
import time
import unicodedata
import urllib.error
import urllib.request
from collections import Counter, OrderedDict, defaultdict
from contextlib import asynccontextmanager
from urllib.parse import parse_qs, urlsplit

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

RELEASE = "ANAS-G-catalog-guide-2"
COLLECTION_NAME = "anas_perfume_catalog_v1_1_multilingual_e5_small_384"
DEFAULT_QDRANT_URL = "https://e1b44e0a-3fd9-48b2-b529-a9dcd260c23a.ca-central-1-0.aws.cloud.qdrant.io"
CATALOG_SHA256 = "ea1bd9165d42afee3d5fefe4df4c49592033eab5dd0fffcb85d8858b25a26afc"
log = logging.getLogger("uvicorn.error")

def fingerprint(value):
    data = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(data.encode("ascii")).hexdigest()

# Generated from ANAS's adopted registry and point snapshot. Only IDs and digests ship.


POINT_REFERENCE = json.loads(r'''{
"0001":[[1,"3d7eb3db2a5f0b38338a27d96ee515fc9d7ab5c467cfbf2262959d3e96e8ce1b"],["a1632f97-5bb6-5f26-9442-d1b6ffa67d55","c6564ce41d070ca5c3308c5a9574dd59a563587afe795f9c9a6bc0d6937cb202"]],
"0002":[[2,"8301390b1194c18d9b81f1bff8fde05d5bdea758c2f4bc3ec5fe79d0e3e609b2"],["17f006bd-5ad2-553f-a98e-d4e3b5e83f12","1f96381e629efa75f9858151a9f809a93552ca442127e0c3bb1b3657ae08f7b8"]],
"0003":[[3,"2e7d41a5eef5dc7b3186fd91883cb101222d74ea13cccd722d7ea35b468419b9"],["d36b843a-7c21-5298-abe8-4d925c8b7283","4cf1954b79fec0672fbcd5117b466e4a6ba4d927d76aea28b3e076481e615e51"]],
"0004":[[4,"f8bebd8352a0da17493515655d1b4121a9dbde9289a2398c414b2e4c928dbd54"],["e24ece82-7990-5fff-ab3c-8881e832bdd7","17ecca5c1f70553c801463a165c5f9d56858d025368250057ef7db5f83caea4e"]],
"0005":[[5,"7b030b1225651114471887ad2ecfbdb652e91b0d8d7e48ada04d959eb44ce35f"],["7588b273-367c-5aae-86c0-162ecd6443bb","1e07117d578191ce0ff4b1771b8a02349ab7ada89642dc2df3823e8e9fc3972b"]],
"0006":[[6,"10c2fdb491fb02f34d89ae4eae1aff36de0356ae7a09fe4b60da34b00a46b497"],["8a5a7731-6dfa-5cf8-8ce4-e66080d0ce13","b85e871d43f3a8b5277debe1055071ac1a4e9ae8b3af575f889dd5c9d6e37a2c"]],
"0009":[[7,"124f7fcbe0f5b770d9b8142cf63eb05d0887417cc2f8210e28ded4355cea1d2e"],["a943a6f4-06a4-5fef-b88b-5bc293f5fc59","8c42b39b74d1ea98ec3b50188b611d4eda369d8ce749ca42d9439ed85dfcf14d"]],
"0010":[[8,"b62fadb3970692fac6896b2e587d050e51c9e90ff1cf4b2ffe42015a16fec894"],["ca504b7b-f690-5e96-a8b1-00cc807a5810","d542461746a89ead7c5e38de617e16f0537a9ccd3d4447588d60d7b167dcd3d0"]],
"0012":[[9,"7672962f3950dcd8196824294eb3be1470265b49496fed1f2ba0cc4de3915006"],["dd8365fa-3424-5dc7-9d21-95ebde5d55e6","65500c96b6e3d802c6747deabddbadfed5efc16e7abdc6722d3793836de3fe85"]],
"0013":[[10,"12c40689c61d0ad5dede655d984083a745338bf9fcbfd1f6e3d63a3ac572890a"],["e0e944aa-18b6-52c9-9a3d-8441a38d2c00","f36a6c9a9e88e808440172c4185c1cfb7eb74b93509b797f956f80e4838fa665"]],
"0018":[[11,"ec0d0c8dfe7f34c809928175ca9cac37d5dd1200435eba36b9f4698e38545c3e"],["6e7fd217-ef4a-5170-b1fd-07dd03828e78","edd7f6ae15a106fcf1b2bd8b8a3d96d284aedaa9837985789f140aeaa7ee93bd"]],
"0022":[[12,"6629f12552df86d891e79cd56b6d2a5dcd1fff8cb4d4653bf4d3b99fe0f7b1f7"],["5e950cdb-c777-5eab-9a23-5f704ff2f891","23b7d6a918fb89f8bab506f8a338851668d52cd579d7bd16e7de7f794a9c4fe1"]],
"0023":[[13,"4db132ec5e953b0db7d5c6bf014bada0fa9188913bf1830458b0335889d0b07d"],["3cefa0ca-6542-5150-9e3d-8a893d491e6d","d0ecfe57d43b65d22175e515c20a47c8c28e1a6a1bc549f4a6fc5e910a7c6df0"]],
"0027":[[14,"f8b01d18639aabc7746ad7731bd900aa046748d38cdc0c57756e2477bed93834"],["616a3ad2-c1fa-5967-bc3a-2ddc080febc5","ee87e0e0e5f79649ba6ec67b04883d853e2b6a082abbd36251b4fde91609db67"]],
"0029":[[15,"ab939fecda1e346b51fc6a839c516cca9e20ea7b0294561936d3474673e55c9b"],["99fd8b66-89ec-527d-a556-23a77b4479c7","7d215a4adf9f4dc2dbfb6391b23fbb397e6a4f3771ae4e41af47e146ab60a6e5"]],
"0030":[[16,"d3b12ea551b89e493ee416861b95993f2ac5f04a8e8ecff57c7b5f3be525c2c2"],["1a74d96b-540f-5d59-8ce4-0e250c043e2c","520d7e12e09cd509e8ae32ebbafebafdcbf6eb3a3bf91e7b4d3b843deabf3726"]],
"0031":[[17,"df4ab77fe0ef18fda19954a3bad89973b2aa5358234a81af5eeb58d582f598f9"],["6c18c5e4-b8be-5afc-9e2d-e0986ed18739","5df73647aefb5b2691bbdd3de784f100dfcaa49f765fb5ea2f59c666dafc9248"]],
"0032":[[18,"b1530aa5cc8e9e7dff7945cfe8fc5adc4b30acb312f34956273ff2b4304eaa1d"],["32b45031-a9ce-5667-a0ce-71ffdc99abd2","77bab2fe0b7fe0de17ca1b6a6cc4a7bb40efe2945f40e68ab2554b8d82b72778"]],
"0033":[[19,"11e5ba8538f650ec196ce0fb32774f56b5ff80e8cb35ec4701aaf6de84769cfa"],["f2daf011-98ac-5cd6-9c69-f9dc68be35b7","9ee0e643c0f942d874e46a84be9cd26e13332b079903d77aa10a2bca89b63ab8"]],
"0034":[[20,"1b6c313f368a7cada10a3cb343ba9308d60b3e060d08c2668915fbf972a262a2"],["29844608-049a-56f6-9cdf-d62b682a6b9d","852cefb521bb3233790b975047dcd91757174415dcea556766acea362d951329"]],
"0035":[[21,"f7c0211171edc2261d4c932da8ca2004cea7d695606e7fcc45bea61d4d253997"],["447c71a2-5ce4-5d53-bf74-9c7e2616a77c","d36514a0d1c91816d8b5bd9324cd5e8ee30e4fa30ba229429e3c44001c02d0c4"]],
"0036":[[22,"b9150986f98d085504fe27ed13c70368e2f4f5698f3429ddcc236cfd84ab7534"],["49b7cb23-d034-5bb1-a03d-835ba73cdd04","cab0e804568997b410d7198978f42be576bcdd43bcb5d497afe34d07d7224d67"]],
"0037":[[23,"0da917c78902078db21a84a71e518fc5d4c1259cb7eddf47109c42af9f0cbb0c"],["b2bf6e47-197b-5ab3-957b-0f439b38ec50","8fd5cdc60fc7747ba6f92c9b3508b2ff21271ab83df59a621dc398be9b150fde"]],
"0038":[[24,"4dc13a3e3d34a26f6844a08595f7fdd4a1f1013bf8b3ae10060a1ff3b65cddec"],["176af633-fdce-52c1-98ff-348c77a6dfe2","003853c1b7c9c78a89f448df84d41cb14433c01c655c9400c1f911b1bb4318dc"]],
"0039":[[25,"386077808fb9310ee1978a2e9be0c3c2cdf359b8f577b941fc008a435740e135"],["963e74d6-17a5-5e31-9b48-35609ba0c3f1","2e3a2a30514450b75ac54af9bbb514807b7e8d44f1664449d5edc922c4815872"]],
"0040":[[26,"6dd16cdc14bc712158d5ffa46515ba61498dc831233a6160a0523b8e3ab2d709"],["7d0e0307-e8b6-5803-8a89-317fa01ccc2a","5313932000d424faaed15055ec12903dad6eab83ed217b9b9a9b60dbca9920e8"]],
"0042":[[27,"b818720f587c4e075b45d1b02511fa8e9369d051cf859b62e137aefeb81c7cc4"],["50c681ee-fa60-51f4-a02e-60fc3b2d877b","98005d5f4799d4176d3c67818e403fbe46cb352f525bdcd661b02a461dcadbf9"]],
"0043":[[28,"02c394f8cf38a657cf924f2f0175e1fd2fb4156b258b0975d6a19a7446644867"],["afcd3b97-5548-502f-bc16-b6d4f5c03738","ee3b47ab1a74ae9b9b8fd32e15e9171d95f1f55f50577efcaecb6fdd8fe9b61f"]],
"0046":[[29,"40372f1199f002199dda624caa9d2c03a1ea649d1341ba460891b106c4fa08fc"],["0fb8c42f-082f-5812-8048-4cfe5924703d","376b48e76e0c9e3ba0692673b57eb84710de42b4d3d933107573591b11276c71"]],
"0047":[[30,"9efb0a0e778530fd22a8221b507c4cbd46fb63b6cbf501b1d8484c06c2b3b614"],["fd3d608f-7ba7-5056-8079-168538c73252","ecf77535f2e9743a0a76763c848458b17aa6b7bd01f5d986888d3697eaeaed7f"]],
"0048":[[31,"3f7378adc81484772f266762de1b4f6cfae5f33315887a9f7e430b32e2b8296a"],["8955e89b-cd1b-5723-931e-ca72d94f0aa5","683eaee4fc0a74199e7a686678cb58baceb5e1bdfb936737b21005f18f791065"]],
"0050":[[32,"384c1517cb308dbd727e12e3a9c2fd21deeee61008f5f9672b210cf6f2e8e640"],["0bff9308-1880-5dce-b7d7-fe8deb5cceb9","e93ca50b87a1328a07739142384eb3d767da033ebfb80fd20a25e72c5663d616"]],
"0052":[[33,"1c1b0bc923dbff66ddbec0053ede3cafe5c5075eea9da7afa1a3d0d79bf461be"],["ebfd1833-7ceb-5cf6-a23c-bc541ea76045","2c46801a40950d1c9105303ae783a7df2f5fa49d3972ce6669fd6afca07b64ca"]],
"0053":[[34,"690223ec87eb5d4671c441578f23e13eb03a507dd00825efa16682b4f9e78887"],["811ab581-d560-5c96-bba1-cf7e0f5d0a03","d80bbe25390b1eced852f06aac0ac43a132c728b599bc5f2ab1f5e273dc19575"]],
"0054":[[35,"6cb4ab726d9dda5ceebd4a0230b6ec08db5fda870c2157097581348c5ed47e8c"],["c0097d84-1175-5b70-b247-46876dbeccbd","ffa4924327c0be8cd9e2cc9aad5a05b4856856ddf8f53787a347276982192008"]],
"0055":[[36,"090cbd4fec37946945a1176cb76f0d2b25a166ec2ec168da940f74140823e86b"],["ba7a8625-2a6f-5583-960b-1d4688337a4e","41170e0001314906b495bbc679b5de647fa9a8c398a91e5692d973809c94c602"]],
"0056":[[37,"457df8874122d15e3f3217a25fc88462a8410554d4337143eb57efb3d7ebf3cd"],["fb97a240-7354-55df-8403-1eff64d2e866","d037a3bc1ec992ce7a3b669e86d95eae02381acf8b40f4afc5b806510ee846c0"]],
"0057":[[38,"43edd067e5b19b71c37a5d3eb29b60669c3a82316d788d7d873789a7b9643f73"],["2b793b39-1c82-5447-a607-4f2451db0d0c","4726a71b278ad1383566481710b87e7bb4d06096f9e4722931a00d1441c5c19f"]],
"0059":[[39,"55066cca3b8369d4b7649e217fadd57f57a49cba6ea61fc5a17fd75f6f73af38"],["8b280778-bb0d-5947-a5df-96ea4c865671","86397efe1d4ae62ea20a6d338528d4fbe8a37452f4049df01512cb20a4a83b2d"]],
"0061":[[40,"09f74bddd99a6b4644e5482466f39d770ff900cebaeb0f18704b9467cb3ce775"],["13865a09-c403-57ed-b414-d279711fb0c5","fe959993e535efd9a2fa2e9891f9cba8c1e8211e19a6dfd77d1136c26e42292d"]],
"0062":[[41,"5801ade3af33b530a0270e02d9cfab4bf61253204cc29546fd8e11cab8aeb372"],["c2db623c-c03c-5f83-96e6-c71889d8db0e","1b55cd747d41c3a20371fe49f62fd46db7cb461e24afa548caa53d24313904c7"]],
"0065":[[42,"5443793139d5ddf0c5a8bd4e9c3777d3ae4b6e46ffaa04b1ad4f756f536c2ff0"],["ec7f141b-bede-5bc3-8976-e8498c24870b","dbda4530965bb1ad7b037306e5dbddc4923ac2e1e25d58886d6aafa6e137209a"]],
"0068":[[43,"7835d51dc5597a093fca9b01dc5bf64887cdbadcb46cf6103deacb9a6deb18e7"],["98849724-5544-5b63-b374-9fbcbdcbeb91","d4f02c0c00192c84d8a66625fa65db0fdfa5a7eaac5c69200ac9f3b04b44e0da"]],
"0071":[[44,"c23b6584a5f0325e1dc05fe170b152d815861891b0b01335ba81304d5763b244"],["943275b8-b915-561f-9340-eb723b2e311f","d448c88c21f52f81e51e25166b452cabadff747c5663374c7e04d0d507d2664f"]],
"0075":[[45,"6d81353f348d40b55c2954246ef3f90471cfc399905bb0fb89832a3ca6aa5395"],["9171ca71-3154-5f22-bd23-1bdc2d33fbec","372bb85cf905309f63f326072a7b40525a20406875a8368936a9c8daf2aaeb5a"]],
"0079":[[46,"806f67c3053e2d548b3633bd37260f3339f4771f3f8ec1bb97c192dfc64ba849"],["cf94cd1a-d901-511a-ac85-3aad6ab014fc","737d3c4a635a46167db981da563575b44e5ff5df2a0dd01f4bbe3e0a10f6a240"]],
"0080":[[47,"9787568afc18670bb2931256f72226bbe78a6c6ef6757c04cb5a3b2c29c0578f"],["19703cac-e7b6-5e3c-ac9e-fb0078cdfb11","7f7debe2d8cffb8ac1a54174a239353578fdcbe520191119b6fc77a866d6fe5d"]],
"0081":[[48,"477a6a17239fbcee7809300d4a3b3f11c2fc8640133f5a3b95c3d70812e23c90"],["c489a5c7-cbdb-5c75-bb27-d2d2a6d6339a","f3b1289a9385e75df56869de10098886573891eaa5c499007f0abab142b1bd1a"]],
"0083":[[49,"bc5e81914d5348920bdeeee3bdb695230f98860733309da21369db12c7cad301"],["6be29d3c-4c3a-5c56-8460-3246385d6118","9f7693ac44026bbf05e048307f3a2534d5a757d1505b6c666187eb8de872f985"]],
"0084":[[50,"88647223eb8cd14af32835a957d758d55a61ee02c9e8665801d64309d495571b"],["fb3117aa-2353-5830-9516-539cd4148ae4","d9a766e2e90c2d21d63f1ea0ce053c3c92ef6e41ff81c39a349f0821a7a6b321"]],
"0085":[[51,"c4bb1372456435311d3a5649f9909edaec07f9bb4d01d0b20182c0b355ae5725"],["4cdfd243-a42e-5553-bfe8-cc3a515f6238","712d1e87e916a8f3aa4cb984533c380c199817f7b44a19ea4f12a42d1d829ed9"]],
"0086":[[52,"335a57563dd023f2bbfff974d8fb0b808ab5ce03fe26f6582c31521d6d4b3959"],["2c3e900f-a432-5f1f-8580-5855356b6385","8d107f215bcdfa2f93a012a9402b7e414f4c79a2b45b0e12a8110a6063294084"]],
"0087":[[53,"8d4f36f75b211eb1cd7772fa8e87e979667435c9eeb73a5da3796851bbd30473"],["928929b3-8501-5d9f-ae28-7e4e36a5cdcf","bc6e0a403e6667ff587b8d527a412592e86de533528091e525db474368b2014e"]],
"0091":[[54,"d256d5df1f90585b7072fb306e150dd83d2cea50799f24de2a2ba652b1c2798d"],["e921af74-ac47-5483-b4b7-d8c5eba05a6e","6f53f5a7d234e6d89db0c40e61102dd5eb735fdc474bbc6cc0eab556f39affff"]],
"0093":[[55,"fd3415fec782b7b457a8dbd6a5a4df93a7c6dbcf4e56816c9250bd5cced91b3b"],["78f32d34-c560-52c1-825d-258bcc903f94","cb43955118abb4946b9f03d21af457d2e8164025e56e94db47d477b1e8d67f90"]],
"0094":[[56,"0f7fd9e315397921cdf6390a367e16f87de2cc8ea0b15316eb10d47d5e72e822"],["1b3402db-7d1d-5b9f-a200-951da976c5e2","493acbfbb8b3d44f9af7290d581417e1e5d25619036361e6d07355612eb2791f"]],
"0096":[[57,"cce0feb895fe153868d6627f11ebbb11b8adb226739e0c034ad208f232e61174"],["41e5ece0-08fe-5cc1-9948-0c51c6e392dd","6c0b0a67638164f797ba48618c0796a8a3d4bee87581364aeb57d24904826d4d"]],
"0097":[[58,"3571dc8ad7f021ae9be239063ddd7e5a1553688b08e8f37350906cad1b774ddd"],["c97c432f-9f60-5e94-be93-ddc1e02fe646","42d0fd324a573fc8d42ba23fe68289fb36c7b3b62fc368ed9c2bab8c714b329a"]],
"0098":[[59,"fb3725ab638310cb51f3889a3f64336c5b38e2dc32747d5f47252ce1aadcc251"],["d4816365-26f9-5508-8038-3b061a5fbebb","74201f55acd1327b27d325491f0809335c298672869abeec7a71991ace0fa55d"]],
"0099":[[60,"c3ae8081a25a3cea8a532e9ad749cf3621e6e35e1681bcd048e9e399a945b973"],["aa4eb411-e8c2-58f3-b75a-e818c8d5de1f","5173773d5fdf11a3ab968f4c7cc7d174bc646a59d3d33ea904a54298ba9f3b1d"]],
"0100":[[61,"77e80fb1c3d50152fd96e412a5a759f2f416b2f9d02c9cd2b7c625276b8f28d4"],["c964e7ee-bdbe-5ab6-a2f3-0279cabbd2e4","7b998e4165e10d76f40c0144bf1925aace6a5cb3be38067c2d811c205e79f342"]],
"0101":[[62,"f24c5b88555a690c59bbc559353f7c1c59058c6f56223a3b402341fea4d7075d"],["b70bcae7-a88c-5215-b4ba-e53f4c56ef2c","36dd4bf618100eeb927e205e1a7e3b89282322fae7834a6bf91e4cc4512fb662"]],
"0102":[[63,"8492d1c475788b8173b761c2f80becdf439ed4e464dc0eb3ff9e4d3cde2e579a"],["0dcf411b-75fc-5b44-bea2-4d1e9b47d694","916e3e0e4c155eab32b6daa2f2e995c3da587b46b3aa542c8476e7feaae90604"]],
"0103":[[64,"cd587522329f4304849d2d15412e1fac1f78b6e20c4fac446c454583167d2684"],["8077bf66-34ce-5ad8-8ad1-3027c2863113","a3dab1519895ff3ec1d7a11e18da2cc9d4d9e0e6cc0cf149f6bab10b952a05d4"]],
"0104":[[65,"f143ed751ff7632dbc3797dc376726b8f1bfc6f8bf3d70be515be459a721022b"],["9c512ccc-da44-5185-860d-785939867f82","4d05fabefb7f3d1be39bf2fd49f0c7c1d5f03e19f76f773bca10d75b2049f8e3"]],
"0105":[[66,"cf913d059461e67570523c4bac6a59c59bdd878454642d846c06a21951308599"],["fe224c7a-ae95-5b64-b1a3-5feda7c30d20","a0419fd9ce5b20118cf4f44ee0956451164bcf7acb1a263349b7224c782fd425"]],
"0106":[[67,"4f35040e9a7ed85a7ad664c1054293f9d340135309cbae9a35024298246d8f0f"],["0dd24696-66f3-5586-8c45-c42e8684a3be","572e274d766952a388cd2b6e1fe8c68f8c25c42c4d87bbf3fb3e19b02a68ff17"]],
"0107":[[68,"a74bdd78799e7807e52a10210f51504200dde761f7bf124ae101deffec817e3b"],["faee1ffd-1cd1-5d55-8df0-f393753bab48","92494c874228b122ac49021d3690c58e9e18c18d387216b2def3cb4daf712a3b"]],
"0108":[[69,"b599fecd542aa9054a82cd00444f84c1ebcd76b2a997dd82a840e3827705570d"],["2155f798-3c79-51bd-8438-1061fd2b2d1a","3c62e9eff82d31190e998c7783b6cf1264cf3ab878b29f56a4808bedb8eafb29"]],
"0109":[[70,"2343931fa581a630d70074d25f4b037ca6fd12f44887dc0b974b2a770e85f55e"],["a4ec9fc2-ae2e-5c36-9d8c-ff0107551176","83249e768a88d7e5db828da6cee3b799e2eb7b4cd894aa746ed59145da8b4103"]],
"0110":[[71,"a29f2f92fab9df1f8e93a7df534366f9141a67c3dcc7c5bfa6e2cb7f4a3e5c53"],["b2bf82c7-27c7-5f18-bf9f-d61a3069471d","b424c8f00d339ce0059c8aeefc0825f751c9230f6d1711a279883a816dda7f75"]],
"0111":[[72,"f2adaf2e7f1d430e098ade48ae2bfe72594c51df1cc9a2830811ed7bac7cf9ae"],["cfe2c3c6-133a-5418-9c85-5f3a924a2005","7ed1a452a2d164b9bd7df9c54f7f8c69534d9d7daf53c24e70d1c9e009254d33"]],
"0112":[[73,"3d938ceea9404f98f729856cc7163e9255c423814335cb67051491a8a8a3a733"],["a67186ed-a266-5a39-8af7-7ddd2860e0c1","044b1619c0e419f511b8fc6c76de30ec4fc981a93963ceecc1da7b0b72bad691"]],
"0113":[[74,"001bd11ef972ec258d200bea7fabd0c58881a23696f9102beb8dc8016eaed963"],["8eef2824-fec9-57d7-9ac9-be49d4f0c9c2","15837fc60dab990d3bef11efd8104bbdf065a7aed52ec4a37dbbf3365a37d897"]],
"0114":[[75,"f3543e95ad61ce4e17e1d324367e16e670c3f5217334fbdf2923b7bc0a3982f7"],["ed1a67b0-1014-59fa-9648-1ab7e0888e5f","cbc1a14c1fd6756cb9354968fa2877ea113939dbcece09a695da4d94cd11f79c"]],
"0115":[[76,"bfb057db4d8b3864f71e94c997f4700f189aea8696b7980afbad2a83da841cd9"],["8ff713b8-a796-5a69-8493-459f51212535","a514593ecd6ac2dea2b8922685c88fe9cbf1be3341dc54cfc927a18ea0781646"]],
"0116":[[77,"d9732a0e12d383b748aa61e6f4bedc8a2e75a7036f0817c86a431a91a1efe8b8"],["78fdd2ab-6df3-5e9a-9d3c-754719916ef4","c49265a4c1c90ae0552482d27046257aba7ba9c033e8655a2eb4ca6106d8ddb5"]],
"0117":[[78,"c96df902c457c7b04fdcc1fc4386865e299fd292b3d0ddc509c1062151eef0e8"],["3981041c-4d07-521f-99a2-afb81e157259","dc067ec061812e9192a450ec244183150efa579cd6daf5bcf30696e544e413bd"]],
"0118":[[79,"11d07290da6639fec3a2ed2ab51424f7aac1f2151544b52cf6b8edc91a966c81"],["cd34e5ad-b7d5-5a77-afab-a9be0fd26ff2","e00f4c7dd8cc644f8c98c3ae8a75bb985c01ce6b9c9f6d1504f4ea02cac071ef"]],
"0119":[[80,"a480b78e1b6f3281fe627e3f1fc2b898e59ef99a03be167c929961fd84170fd0"],["6e1e3202-1542-5cd7-8fab-48379b05bd4a","acf3c2af110b6fe9d22062747f990c56895b41374a0c33c99c177fc3bf178ad2"]],
"0120":[[81,"acee47fc99e713dbb48fd3152f60e4e45917e0067d0fe4b42d15f23d8ddfd5de"],["fdb18cf6-438b-558f-9d9a-a6496945de56","d604ba31247f4a52627a6deb5846a4e47f954abef3181086c3c7f4c3e06a7792"]],
"0121":[[82,"46f7192a344d01a2ca3638c28fe8177868aac2c62b5933c09a3c90255e07ab09"],["9d8918fb-21a6-5d5b-bd93-fd9b6b3e7778","bbb7e380f2b8b77bcfb27ab14758da4c43d0222ab953edaab8085354e1c3ac9a"]],
"0122":[[83,"362d6cef31f39c050886fbbb597c6309d59309a4402f6dac8ebe95d01e4d948f"],["7c7c2fc2-afac-5488-a8e9-b19e97c45773","53cde559ee6980a5a71c39bdeb1a00b5bf2d9d4de27063a03eb665d712a52bdb"]],
"0123":[[84,"d10b0baeb772371ef6cae0461c54f24de82fbb6389998581c940a73146e1966f"],["f54d5d7b-03eb-5bb6-957f-22b3f3c4a50c","ce39655d66d97f177fac424aa7a659df264193ab5a64b48058bc8a954bf17b2f"]],
"0124":[[85,"bf71de51face4d7523878aef4702737832928e0b3384e2f48abb7a60bbc065a6"],["03df39d7-8d04-58db-9198-cf948e2bd0c4","3a0bbcbbf0dabe09850dd62b27bfc3976490a135878298636d53aebbc5805862"]],
"0125":[[86,"c5b23a35e932f4f59a1c59802c45e0b6f54b2dcca3cab06b184e42ea839e0640"],["914f858e-3c71-5862-bcb2-a00737f0d875","c06b833e7680496855e01efa453cec70bbbb6dfe13611464e1a05c1f3225d3c8"]],
"0126":[[87,"b7ce54c8c99a106a45cf74c24572376f06e85375063431fdac58436132b394c2"],["2546d8a9-65f6-5a9a-bb98-7a19bfacc458","906fc931821bc39e9ea18231a5f9363dd1e85422c30ad54a7c47c589576df1fe"]],
"0127":[[88,"f9fce096a7f24160575925a6a3c964c63fd678daf442c51a1e9b0517ddbf9dc0"],["9a4467b2-c5d6-55c0-ae13-7f217829e3fd","d429a0349def2717eed59fb74d2aeb049562d507562f4f3f8082771682715210"]],
"0128":[[89,"9080f23a64e168de5f0f23b00235ac3df59fd56b342c3f342f6fad0efc81b06c"],["769efb39-7f07-57ea-9ec9-bcde36c92dae","43721fe027d48b1e62a0dbb8623231edc5e6f07bec46a0ee6afef6c7aa0fb2b6"]],
"0129":[[90,"b4ce1b16567bcdb7997f0fe063c0c74241f357193beabc0dcdd5f2c603949b05"],["ca84da9b-df63-5393-b07c-32e48858bc21","a3ba883c6ed56048749548cb471826b9030716a6a93c945d8831e22e9c5405a9"]],
"0130":[[91,"273eeec53137776b6ab0e760799df87561ebfb02c83ef75de8d5db9244c465dd"],["e330c772-294b-509c-9cad-dc17334f1a97","25a840d7f64d762ae80a3150567645818604a1f754fcffa49afabc5b434e99e2"]],
"0131":[[92,"cbae20a3ea34988e90a96028943bea6622f8648e22f56b77c24f205b3c2149b7"],["46f0a310-7f9c-5aef-8f7f-a8999734f151","629b969b2aec84acd3504926fe6f548555d367a4d1c177b19cb9364b89be4d8c"]],
"0132":[[93,"13570c5d7e0ffac2ce9758803e43ac059e2c2fc7a258c020f683ff6e42cf8c74"],["19797c50-eb95-5bf3-9706-36d6d4db606b","640699091c5dda71dfd15933bfabb1dae2405f435c7840e3c05ca9646f39fb3e"]],
"0133":[[94,"cee38183312ba04d0c73d7465bfc347373dab480e4b13c4c0c7f270a578fe039"],["5d39807a-3b94-5dc8-83dd-3c2b90b7f6a7","a042c8942b9d29fd81a2bfcf250b7c562796258c55f127592f740ad7fee8b660"]],
"0134":[[95,"1fc7be33f0b9d22ca68b4bfdb085a91de3f889486cb04c5f3a3b87b22d2b2e0d"],["fa47430a-b5ca-5aed-a4b9-2b443bfaedac","d29a5318c55819b434ea2a602c053011591c5a94f43f76ac15089bab6ca78f88"]],
"0135":[[96,"74634b5341ff57a26225bd941dba21abc3ba86fdb0864af83b738c91f1f482ec"],["7ab5ac8d-25bd-5130-931f-d41edf9d190e","3f2b69bf70b00bd5f3ede2f163174b6daf15ad3b09db0f92aad43096e3c1bc7d"]],
"0136":[[97,"626af9981b312d3f1f7944c7753e6e358c351f87362dca02980c25702e7d1058"],["e95e49ec-c938-575e-a7d4-267c82656ff3","6344b9c5244eeb9ea321a4792108548ec53efe873e4ee669340d16c1d2ac2b30"]],
"0137":[[98,"b2d216adaade30ee393f6ed2124f2e3295e647fef1bd71d193a9f7c5ca4378bd"],["87097f5e-5d6c-5ddb-b8a6-214a0a6be553","0a433151b29f1cfd2bbe7b704cddb4820aaa4f9ecb6d88d3c949d07310715dd9"]],
"0138":[[99,"8a9b91d3b13db50902ac8718cf8d6efbdef8744b05acde88e594d6358a0da79e"],["251e60fa-389e-502c-b9ac-6ba809ee2de5","bd028788f31c513db37ae260c344d68cacf805a8b3e12a712dafef310c880d63"]],
"0139":[[100,"c2e6ee0576ec99b8378362043efd0337a4f3988c3c7f42fd8058b2b18c3be267"],["7a4963d8-1dbe-5810-b910-7dbb4aecb040","901f699e2e345836fbd469c660b2988dfbdc9173bf8a93ce871f99e66768e6ab"]],
"0140":[[101,"0202e66afdb61c70f70ebb2537b0cff80ee31f8a4a17bcee20a1ff2171108f4f"],["106a4f77-39fb-5f03-a5de-ff056d41442d","9f1306a8182f4ae5c5f98b8536d0461d0665df8e8f1fd5ce911807650d7f4dac"]],
"0141":[[102,"661586c6c60574262aed17a080cf45b0d297337b6d89b85b18ab251bb32ced87"],["b1e4beb3-2032-542b-84ca-9f0ff6d85a71","53e9c2546774d50ebd8013cca64f55c027ddbd1f6f2ee6f4c96512f25222486c"]],
"0142":[[103,"dd6a02c3c04149b0fb2534bbde1ee3d1cf34823faac4de38467fc635190663eb"],["cdd8adfa-b45f-5006-a819-a5a971c82b32","0a2db82563866a08f171320facb74c737de52f2d67ec51eebd574558ff0219a8"]],
"0143":[[104,"400d1c98ad083a41fff16fd6d4f3ccd2b440114ebe9f71c1417391b3471af24d"],["611d006a-c382-56b5-8767-8bbe56772709","98a9af33c3ec1a0297f96bf3f86c62a2ee71bae18d04ad124633b1f4464f3962"]],
"0144":[[105,"1875a79bb49b816ce7e5f33ee1a0c3f71eb898adf834d40df54c59877ad42e43"],["6b54982f-4916-513d-ad31-64fabbdb3299","f6acbe768f9530bfde653470e8eccc81a2f86fefe92c43f5876f99f0175b4849"]],
"0145":[[106,"a8f9c6491e3cd174f45c946e99db623f9974135b6423d049ca0fa57b53cab441"],["9ff93c3b-b746-5fed-a36c-a5b480cb1083","d2f32a21189984f38c21a43384bbd415dcb3d1346fca02ea00d939d091ab32b3"]],
"0146":[[107,"d5dce26345340b0eb7156b4d873c3a1ea10ba828560741cc7b05e2345dcffe48"],["71d69b89-e882-5193-b9fc-34ec36e07e3d","f4753db48e0e368e89ca1e58f0ecdf0c0545e3e2cc525e6cd87c179eeecb3fe4"]],
"0147":[[108,"2d05415f169c5ffd8ecb51b32819c03c67e8eecc90edf5716a495979dea50691"],["54adccd7-e5c2-5107-a2ef-37367bf58a5d","366ad9a2864f31e11fce9e7db11c8b177be3f436803db2f99192913e00491c69"]],
"0148":[[109,"10901f239ea53a17966f561e1e011e25ba4757654d1d2683d648fa11e5126c50"],["d5260a82-488e-5a6b-9c37-de8682684216","22a6744c3f2f0112ee69f22d1e17f8575326a56ce429ae7935d42cca48663351"]],
"0149":[[110,"2511e6b5696fbbaf79d03f3d77dd5cd385db84926bb386aa18ee84ad3a1d903c"],["f1d05591-95e5-5caf-821f-1fd75931e6c6","cdf5586e6c2f5a1b82f7c51f05d8246507f1491b26f7ffedb29f608b3aaff5c8"]],
"0150":[[111,"26b333d334af1fd2b5edcfd40d97fbc5676d356efef2c9086245d22110772a3b"],["7f8a3db4-170e-579e-abcc-5499307a3d40","47a0157ac85d02a5229658d1abb39c0bfee2bd3bfe85adad9fd27c83f6ab641c"]],
"0151":[[112,"e1386511d3a3e8ac2fb4f39736aa34938cbf5db7767d94eb64675d4e4077d9af"],["5539f213-b14e-50e1-8caa-92937414b224","6c67706fe5cd071863bd8de953210bdc4d9cee132ac1a5d08eeb71f40b7c0067"]],
"0152":[[113,"066dfbe2a75fc8434a34fd2bebcf9c4d281f182d6587f5ca2a02b9248f01780f"],["d4a076a1-7264-5af8-9b77-d873b2c7c951","0c65e6675863b30b5543d7ba931e33d2a8b284152fb42d995c575815dd0c5d6d"]],
"0153":[[114,"f34175e7a54c48dc68b5fd8a1c91209d0cf6aec283337d0b39fcbb7f047cfb40"],["0bdb1071-57bc-5fb2-b150-1793cd8b1454","47993fb6cd9b6f0fb4cfd9c12e99d6e0dec18c2722d9eb9259a251f1edab9c9a"]],
"0154":[[115,"5fe2f30bb2ae1bcc8cbf2d46b759390243693c1218464abed3bd5477b22185f6"],["372e45f3-f83f-5bdc-a5f2-be70c860105d","565c106da02d9706e0219ea26b0f7354784c8854f369292f1ace55af4ae5e2ad"]],
"0155":[[116,"a96216fbe19446c49b8dfa63d91371001d20950346e98c7afd8bf2bb4b4c0502"],["250bf8e0-b522-573c-9deb-801a88fc0697","32f9d8664d89ab02907168573117fd9b10e6f0f27f603eae422c85699ae503c1"]],
"0156":[[117,"4f701b8a6953fb9a98b85454946d95c0aec63d0a9f805deb0d0bf0a7fc65512d"],["bf6e478c-a87b-5e87-9406-11e0eb419b5a","84d8a24ca5e5f3351edd1baab56e41e62c84434c0814a75fad698215b79de3cf"]],
"0157":[[118,"29aa4c19e015ece850f493d5504b1df4d04b00a752f0468cc94e9c737cfed9c2"],["ed3ca2ef-36db-52df-9c2f-e225a168db4a","378fda121d1b181200d66ceb271200e5ed9b9f760e75cd06f9a0e2c1a2b64820"]],
"0158":[[119,"e27fb6e39e4b628a1bc7fec7fae239cfe9a0f55f6b112dca7f63eecbaf6245d5"],["5b318d37-4448-535a-80dc-e6b56278c236","e51185f95a0c672489ef6fdb185101f23025c541cb06c08071ed75c279b4489e"]],
"0159":[[120,"abaaf60668234013d3f66c0e8a4808ca68c5db36e56e47516863690e9881b22f"],["61b1f48e-b634-51f4-aed8-494a80a307a5","8501ae37aa79b329fa8c1630de3981273d43d037469c067946aeb00bfb3d02d2"]],
"0160":[[121,"b3d7ae6714e734aa1a3d788ab2d0d09df58771cf49f488e7ae5a615e3019cc42"],["9b94f46d-8e40-5000-a866-bf30b046fcf3","c481867294cebf14d4de5e2df2b5a246da604f95210090cb3a6c74511118b964"]],
"0161":[[122,"b8db7247746dc8c1464400580a5e7df948c1a4b8dcb549efd66abbe20c287e3a"],["43fd5243-5165-5b4d-bf1e-90d02326911e","a404dc64c2ed448fc80340f5b7a0b9a38624e2a40ff4dccd5171f6dc45c5a24b"]],
"0162":[[123,"5b45e1046700822d23eb7f171abd011646d91dfc59145c295a79d7f14d427bca"],["4bb177d9-b21c-5383-9f48-c296511f59df","db3f0eb72da346eb9b98cae8f37129bf95ab01085d9c8368a5a8d86ea54f0943"]],
"0163":[[124,"8aa6150e153c41b41d2e4dcefcc8b0b8f5304a510bb1cdcc7b2ee6c7f0ecf218"],["728bf6e6-e126-550c-bfd1-dea96cc5f4e1","06c165f9e9cd5a300577800d587c2489dd3953853e2a7031be76715e3c792242"]],
"0164":[[125,"46f465df8d779e5e788d31c6ce12c120836ea39971f146235c4755912140bb13"],["4644f18a-3051-52bb-9b29-d4fe29669fbe","e400c0b258c4b4cc721f655b2d7d52d833e7b758163cf6916e00ab8e2c05c911"]]
}''')


REVIEWED_ROWS = json.loads(r'''[
{"claims":[{"attribute":"note","channel":"manufacturer_authored_content","layer":"top","polarity":"positive","ref":"e_5556fcd88a2ceb79302aeb79fc66e51b","restricted_bridge":false,"source_ref":"s_3c14dfd03f7a89c042af5041c21524aa","value":"note:mint","version_ref":"v_864ed19ca46f712f7941b2d3b8903ddd"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"heart","polarity":"positive","ref":"e_6a05a512246ee6122ed756b4b3d36728","restricted_bridge":false,"source_ref":"s_3c14dfd03f7a89c042af5041c21524aa","value":"note:rose","version_ref":"v_864ed19ca46f712f7941b2d3b8903ddd"},{"attribute":"context","channel":"manufacturer_authored_content","layer":null,"polarity":"positive","ref":"e_fb449db7f1a42a2b8652a4ccae76172f","restricted_bridge":false,"source_ref":"s_3c14dfd03f7a89c042af5041c21524aa","value":"use:evenings_date_nights_autumn_winter","version_ref":"v_864ed19ca46f712f7941b2d3b8903ddd"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"base","polarity":"positive","ref":"e_e068c3ceff1e60c748b96245f3b68723","restricted_bridge":false,"source_ref":"s_3c14dfd03f7a89c042af5041c21524aa","value":"note:patchouli","version_ref":"v_864ed19ca46f712f7941b2d3b8903ddd"}],"classification":"both_documentary_axes","code":"0001","concentration":"EDT","same_source_manufacturer_dual":true},
{"claims":[{"attribute":"note","channel":"manufacturer_authored_content","layer":"heart","polarity":"positive","ref":"e_2702b51c4912060e509f9ac1bb2e1444","restricted_bridge":false,"source_ref":"s_0eff91a48b6ad944bf93ef8b832e4d50","value":"note:nutmeg","version_ref":"v_c605e7dee9f48fa8f439cdfc9c9a4f63"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"base","polarity":"positive","ref":"e_c2034ac398fa51d71b60c67167b920dd","restricted_bridge":false,"source_ref":"s_0eff91a48b6ad944bf93ef8b832e4d50","value":"note:vanilla","version_ref":"v_c605e7dee9f48fa8f439cdfc9c9a4f63"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"base","polarity":"positive","ref":"e_4f6ee3920ce9e5e216cf746a3034be7e","restricted_bridge":false,"source_ref":"s_0eff91a48b6ad944bf93ef8b832e4d50","value":"note:sandalwood","version_ref":"v_c605e7dee9f48fa8f439cdfc9c9a4f63"}],"classification":"taste_only","code":"0002","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_72df1b43485d48224ab142a58ca4fbe1","restricted_bridge":false,"source_ref":"s_0caf5173d289d98c6b45a1ba1e6569af","value":"note:mint","version_ref":"v_5553fb05ca9c6010d5f98407e0eb73a2"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_2662cf95d5b7b4929515e2b82f9516fa","restricted_bridge":false,"source_ref":"s_0caf5173d289d98c6b45a1ba1e6569af","value":"note:ginger","version_ref":"v_5553fb05ca9c6010d5f98407e0eb73a2"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_b32868d049377a0edb154708f6bfe131","restricted_bridge":false,"source_ref":"s_0caf5173d289d98c6b45a1ba1e6569af","value":"note:kingwood","version_ref":"v_5553fb05ca9c6010d5f98407e0eb73a2"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_b0fea6e89729c7545105f118a7edcfec","restricted_bridge":false,"source_ref":"s_0caf5173d289d98c6b45a1ba1e6569af","value":"note:amber","version_ref":"v_5553fb05ca9c6010d5f98407e0eb73a2"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_6814e74a562414de2303765c493a5af8","restricted_bridge":false,"source_ref":"s_0caf5173d289d98c6b45a1ba1e6569af","value":"note:musk","version_ref":"v_5553fb05ca9c6010d5f98407e0eb73a2"},{"attribute":"context","channel":"manufacturer_authored_content","layer":null,"polarity":"positive","ref":"e_73e521e06c9e9b758f9029ee6bd0112f","restricted_bridge":false,"source_ref":"s_5f779f8cb45b33f2de3410dd39dbe99f","value":"use:evenings_after_work_rooftop_dates_nights_out","version_ref":"v_3347b97f2cc01fbb1854e28069bef36f"}],"classification":"both_documentary_axes","code":"0003","concentration":"EDT","same_source_manufacturer_dual":false},
{"claims":[],"classification":"attributed_use_only","code":"0004","concentration":"EDT","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"note","channel":"manufacturer_authored_content","layer":"top","polarity":"positive","ref":"e_e73cf9918474a43664b58df355e9ed99","restricted_bridge":false,"source_ref":"s_23a766cb089a4341ffa43310112c8724","value":"note:gardenia","version_ref":"v_d97b8ddedc4f1ba386a44226f1ca8a08"}],"classification":"taste_only","code":"0005","concentration":"EDT","same_source_manufacturer_dual":false},
{"claims":[],"classification":"attributed_use_only","code":"0006","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"note","channel":"manufacturer_authored_content","layer":"base","polarity":"positive","ref":"e_d0f172f14a4cacf4de54480508199139","restricted_bridge":false,"source_ref":"s_431c2554dc22b93ec3c003ae433b74ea","value":"note:cedarwood","version_ref":"v_c1dc23e1bb02328ec0ab930ded949f7a"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"heart","polarity":"positive","ref":"e_9c53939e94b6458ce50639f34a5c83f6","restricted_bridge":false,"source_ref":"s_431c2554dc22b93ec3c003ae433b74ea","value":"note:lavandin","version_ref":"v_c1dc23e1bb02328ec0ab930ded949f7a"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"base","polarity":"positive","ref":"e_01153516a739479def93c10354dd1d49","restricted_bridge":false,"source_ref":"s_431c2554dc22b93ec3c003ae433b74ea","value":"note:tonka bean","version_ref":"v_c1dc23e1bb02328ec0ab930ded949f7a"},{"attribute":"context","channel":"professional_editorial","layer":null,"polarity":"positive","ref":"e_48a1d5f19d4904a95a478b113f74010e","restricted_bridge":false,"source_ref":"s_9c80d0c2fdaee098486275063b81dd7d","value":"use:date_night_editorial","version_ref":"v_2ef759a6aed8687db7d6fdc16670a680"}],"classification":"both_documentary_axes","code":"0009","concentration":"EDT","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_6ed5400583d6b0d3a5550a9b5067e650","restricted_bridge":false,"source_ref":"s_6174df737b0935037430b39ed2261bda","value":"note:pink pepper","version_ref":"v_b30cea2be99582ffe405e1f2c4c69341"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_4c3436a505624212bd1c73c1d45f4ded","restricted_bridge":false,"source_ref":"s_6174df737b0935037430b39ed2261bda","value":"note:birch","version_ref":"v_b30cea2be99582ffe405e1f2c4c69341"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_32205e103bb9b3c5b8dfb705a1a09bc7","restricted_bridge":false,"source_ref":"s_6174df737b0935037430b39ed2261bda","value":"note:patchouli","version_ref":"v_b30cea2be99582ffe405e1f2c4c69341"},{"attribute":"context","channel":"manufacturer_authored_content","layer":null,"polarity":"positive","ref":"e_8d04fe34c12fb5fba30c92bd83485776","restricted_bridge":false,"source_ref":"s_94f3395cb9023aa86c1c01ee6c2d594b","value":"use:evening_or_more_formal_occasions","version_ref":"v_951300da3e88e5b5580d7d2c3b0e8835"}],"classification":"both_documentary_axes","code":"0010","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_39839418e977f5751cfe5aa5a3d89101","restricted_bridge":false,"source_ref":"s_a59415cb0cad8c9551677f7b0b48ff4c","value":"note:saffron","version_ref":"v_f1524bda6bbb1ea3f583765b874b29bf"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_665f42de98279e8dbaacb1856d5d793e","restricted_bridge":false,"source_ref":"s_a59415cb0cad8c9551677f7b0b48ff4c","value":"note:patchouli","version_ref":"v_f1524bda6bbb1ea3f583765b874b29bf"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_66933427d47fb02777a71b08318d77c1","restricted_bridge":false,"source_ref":"s_a59415cb0cad8c9551677f7b0b48ff4c","value":"note:sandalwood","version_ref":"v_f1524bda6bbb1ea3f583765b874b29bf"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_a8d2a2d8f60e748b10386528e6538c31","restricted_bridge":false,"source_ref":"s_a59415cb0cad8c9551677f7b0b48ff4c","value":"note:leather","version_ref":"v_f1524bda6bbb1ea3f583765b874b29bf"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_a314c33074102252830645aca0da1df5","restricted_bridge":false,"source_ref":"s_a59415cb0cad8c9551677f7b0b48ff4c","value":"note:mandarin","version_ref":"v_f1524bda6bbb1ea3f583765b874b29bf"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_0048f0c1e0b731683ad05268a0884027","restricted_bridge":false,"source_ref":"s_a59415cb0cad8c9551677f7b0b48ff4c","value":"note:rose","version_ref":"v_f1524bda6bbb1ea3f583765b874b29bf"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_3d535e6ea37310280dcda588660aa529","restricted_bridge":false,"source_ref":"s_a59415cb0cad8c9551677f7b0b48ff4c","value":"note:lemon","version_ref":"v_f1524bda6bbb1ea3f583765b874b29bf"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_dc168ac3cfa6d0a44a173c6136c3006a","restricted_bridge":false,"source_ref":"s_a59415cb0cad8c9551677f7b0b48ff4c","value":"note:oud","version_ref":"v_f1524bda6bbb1ea3f583765b874b29bf"}],"classification":"taste_only","code":"0012","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_79bc6e22d93eb9082e3afbd89f73b447","restricted_bridge":false,"source_ref":"s_5f12718a0afc915789187b44ad34f566","value":"note:patchouli","version_ref":"v_ca1740ca3563936a85bf7a7952fea809"}],"classification":"both_documentary_axes","code":"0013","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"note","channel":"manufacturer_authored_content","layer":"unknown","polarity":"positive","ref":"e_e1f9c7eb9b865d85b3f2cdff3204a2f7","restricted_bridge":false,"source_ref":"s_ea79d822fe48a4663506c76744659759","value":"note:frankincense","version_ref":"v_434e97e8ddf0b9920869bc06213ed150"},{"attribute":"named_note_or_accord","channel":"manufacturer_authored_content","layer":null,"polarity":"positive","ref":"e_4d925909c80e3e2190855df070d8ad49","restricted_bridge":false,"source_ref":"s_ea79d822fe48a4663506c76744659759","value":"note:iris accord","version_ref":"v_434e97e8ddf0b9920869bc06213ed150"}],"classification":"taste_only","code":"0018","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"note","channel":"manufacturer_authored_content","layer":"heart","polarity":"positive","ref":"e_b9ac4a8cfaaccf19648c538e825e50b2","restricted_bridge":false,"source_ref":"s_58e040ae530486749c515618ae3d09f7","value":"note:magnolia","version_ref":"v_c7169a7df4c2341a3422e7dfb30069f0"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"heart","polarity":"positive","ref":"e_2d29eb57c7bac62787050e5ef190a27d","restricted_bridge":false,"source_ref":"s_58e040ae530486749c515618ae3d09f7","value":"note:peony","version_ref":"v_c7169a7df4c2341a3422e7dfb30069f0"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"top","polarity":"positive","ref":"e_babb02a49f1aee1a11678069fd60b26d","restricted_bridge":false,"source_ref":"s_58e040ae530486749c515618ae3d09f7","value":"note:yuzu","version_ref":"v_c7169a7df4c2341a3422e7dfb30069f0"}],"classification":"taste_only","code":"0022","concentration":"EDT","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"context","channel":"retailer_editorial","layer":null,"polarity":"positive","ref":"e_4863226789135fc8d2659aa8bccdd7a6","restricted_bridge":false,"source_ref":"s_df8f6d92014405bfeb3b119916063841","value":"use:cool_evenings_weekends_casual_seller_editorial","version_ref":"v_f23f206749f41452a6ea1e9eb1c764b1"}],"classification":"attributed_use_only","code":"0023","concentration":"EDT","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"manufacturer_authored_content","layer":null,"polarity":"positive","ref":"e_1c2c9f4da4cf2fa912c1053a7eb8cd5e","restricted_bridge":false,"source_ref":"s_97ed5cff4428ca96694256401759d604","value":"note:leather","version_ref":"v_c2e7d1c73258a576b6348a5fa8bd1700"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"top","polarity":"positive","ref":"e_88083a0c0de89371750df3be62f47a70","restricted_bridge":false,"source_ref":"s_97ed5cff4428ca96694256401759d604","value":"note:violet leaves","version_ref":"v_c2e7d1c73258a576b6348a5fa8bd1700"},{"attribute":"named_note_or_accord","channel":"manufacturer_authored_content","layer":null,"polarity":"positive","ref":"e_1b2595559343c8c084ecf80a6e85f72f","restricted_bridge":false,"source_ref":"s_97ed5cff4428ca96694256401759d604","value":"note:material_fe810b84462c54bae483e67d022a1059","version_ref":"v_c2e7d1c73258a576b6348a5fa8bd1700"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"top","polarity":"positive","ref":"e_7628ae52fc911ff5c135bb68657a1d30","restricted_bridge":false,"source_ref":"s_97ed5cff4428ca96694256401759d604","value":"note:grapefruit","version_ref":"v_c2e7d1c73258a576b6348a5fa8bd1700"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"heart","polarity":"positive","ref":"e_432dd6407be448940c60dd5a4bda36b7","restricted_bridge":false,"source_ref":"s_97ed5cff4428ca96694256401759d604","value":"note:cyclamen","version_ref":"v_c2e7d1c73258a576b6348a5fa8bd1700"},{"attribute":"context","channel":"manufacturer_authored_content","layer":null,"polarity":"positive","ref":"e_3779a3e70fb9dd108c8cb998ee94ee98","restricted_bridge":false,"source_ref":"s_97ed5cff4428ca96694256401759d604","value":"use:day","version_ref":"v_c2e7d1c73258a576b6348a5fa8bd1700"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"heart","polarity":"positive","ref":"e_3653aa1d146a59009051677e21983e2d","restricted_bridge":false,"source_ref":"s_97ed5cff4428ca96694256401759d604","value":"note:saffron","version_ref":"v_c2e7d1c73258a576b6348a5fa8bd1700"}],"classification":"both_documentary_axes","code":"0027","concentration":"EDT","same_source_manufacturer_dual":true},
{"claims":[{"attribute":"named_note_or_accord","channel":"manufacturer_authored_content","layer":null,"polarity":"positive","ref":"e_e6cbdbce0c502575fc4d7c9b8a012f74","restricted_bridge":false,"source_ref":"s_cb31f0ea0336c6f365ead9fc321d9329","value":"note:amber patchouli","version_ref":"v_a8787b38123c2e80dafb3eda9a5591e3"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"unknown","polarity":"positive","ref":"e_2d3b97763379f720ff810dd236d0ab31","restricted_bridge":false,"source_ref":"s_cb31f0ea0336c6f365ead9fc321d9329","value":"note:jasmine","version_ref":"v_a8787b38123c2e80dafb3eda9a5591e3"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"unknown","polarity":"positive","ref":"e_36b5cda512197818a69c1fe4cdc6c47c","restricted_bridge":false,"source_ref":"s_cb31f0ea0336c6f365ead9fc321d9329","value":"note:pink pepper","version_ref":"v_a8787b38123c2e80dafb3eda9a5591e3"}],"classification":"taste_only","code":"0029","concentration":"EDT","same_source_manufacturer_dual":false},
{"claims":[],"classification":"attributed_use_only","code":"0030","concentration":"EDT","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"note","channel":"manufacturer_authored_content","layer":"unknown","polarity":"positive","ref":"e_35087cffa171de3e71211135588f9e50","restricted_bridge":false,"source_ref":"s_a10773ad3cdb8dcbe9899f238bec647b","value":"note:jasmine","version_ref":"v_22ebb8a589c7dd7858d75e15ee6c557b"},{"attribute":"named_note_or_accord","channel":"manufacturer_authored_content","layer":null,"polarity":"positive","ref":"e_e6544fd72afd481aa966110e2a6187be","restricted_bridge":false,"source_ref":"s_a10773ad3cdb8dcbe9899f238bec647b","value":"note:white musks","version_ref":"v_22ebb8a589c7dd7858d75e15ee6c557b"},{"attribute":"named_note_or_accord","channel":"manufacturer_authored_content","layer":null,"polarity":"positive","ref":"e_0faf7ebeedabb8e0425a936e09931801","restricted_bridge":false,"source_ref":"s_a10773ad3cdb8dcbe9899f238bec647b","value":"note:grapefruit-quince accord","version_ref":"v_22ebb8a589c7dd7858d75e15ee6c557b"}],"classification":"taste_only","code":"0031","concentration":"EDT","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_5efe1a9343b45cf939f992872bb6454e","restricted_bridge":false,"source_ref":"s_62b6dfc7fb7f4f61ce3d45dbd93f0f52","value":"note:musk","version_ref":"v_b0ab0061e4c7cb5ee60eaf7bb9ca22f0"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_02c37af2a39797bfb114401071534486","restricted_bridge":false,"source_ref":"s_62b6dfc7fb7f4f61ce3d45dbd93f0f52","value":"note:bergamot","version_ref":"v_b0ab0061e4c7cb5ee60eaf7bb9ca22f0"}],"classification":"both_documentary_axes","code":"0032","concentration":"EDT","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_84f73268a1406232387a7cca462a3759","restricted_bridge":false,"source_ref":"s_7652129f005c2a1390b83de67dd012b0","value":"note:bergamot","version_ref":"v_146738f29b36b3cbd3e291ed0356a568"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_e4ca8126255e35941cae915edf4cb251","restricted_bridge":false,"source_ref":"s_7652129f005c2a1390b83de67dd012b0","value":"note:amber","version_ref":"v_146738f29b36b3cbd3e291ed0356a568"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_9befbd17d2b8d739bb04740482ba1ea7","restricted_bridge":false,"source_ref":"s_7652129f005c2a1390b83de67dd012b0","value":"note:rose","version_ref":"v_146738f29b36b3cbd3e291ed0356a568"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_982f1ae5b4101226d0d649d46640300f","restricted_bridge":false,"source_ref":"s_7652129f005c2a1390b83de67dd012b0","value":"note:musk","version_ref":"v_146738f29b36b3cbd3e291ed0356a568"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_504582285fa92aa190f4d8499bce8d68","restricted_bridge":false,"source_ref":"s_7652129f005c2a1390b83de67dd012b0","value":"note:violet","version_ref":"v_146738f29b36b3cbd3e291ed0356a568"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_b20f7fa1c4194c98428889fc2472efba","restricted_bridge":false,"source_ref":"s_7652129f005c2a1390b83de67dd012b0","value":"note:papaya","version_ref":"v_146738f29b36b3cbd3e291ed0356a568"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_8241e9a7b68fd9444cbb15f7c199700d","restricted_bridge":false,"source_ref":"s_7652129f005c2a1390b83de67dd012b0","value":"note:jasmine","version_ref":"v_146738f29b36b3cbd3e291ed0356a568"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_e6d9ff90cac1b8c2233e56766eb89e34","restricted_bridge":false,"source_ref":"s_7652129f005c2a1390b83de67dd012b0","value":"note:pineapple","version_ref":"v_146738f29b36b3cbd3e291ed0356a568"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_73a06d88052c008eca5fb0dea70ce395","restricted_bridge":false,"source_ref":"s_7652129f005c2a1390b83de67dd012b0","value":"note:cardamom","version_ref":"v_146738f29b36b3cbd3e291ed0356a568"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_46e8eae05dbf3fc92d7d582b230a3680","restricted_bridge":false,"source_ref":"s_7652129f005c2a1390b83de67dd012b0","value":"note:nutmeg","version_ref":"v_146738f29b36b3cbd3e291ed0356a568"}],"classification":"both_documentary_axes","code":"0033","concentration":"EDT","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_e174651e72137d200d3dc016c26281d7","restricted_bridge":false,"source_ref":"s_2a9d46239d50c8420a979498647dd5ac","value":"note:orange blossom","version_ref":"v_98a1e531fa58eb86049ef737dcb076d6"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_0d7537126a6b37c7e34ba21b65da7933","restricted_bridge":false,"source_ref":"s_2a9d46239d50c8420a979498647dd5ac","value":"note:ginger","version_ref":"v_98a1e531fa58eb86049ef737dcb076d6"}],"classification":"taste_only","code":"0034","concentration":"EDT","same_source_manufacturer_dual":false},
{"claims":[],"classification":"attributed_use_only","code":"0035","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_65657c50613c792c206ef2fb1723ee14","restricted_bridge":false,"source_ref":"s_0ceb942040064019599c8e185aefd794","value":"note:sandalwood","version_ref":"v_bdd9228ec4e90c451f943e4ecd99de68"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_10e3201870bc35f434b81d56b99aa65e","restricted_bridge":false,"source_ref":"s_0ceb942040064019599c8e185aefd794","value":"note:musk","version_ref":"v_bdd9228ec4e90c451f943e4ecd99de68"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_b220bdd6719a8fa82ab830614b00ea44","restricted_bridge":false,"source_ref":"s_0ceb942040064019599c8e185aefd794","value":"note:amber","version_ref":"v_bdd9228ec4e90c451f943e4ecd99de68"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_b6c1ec7f52895c027768fcac2856ecdf","restricted_bridge":false,"source_ref":"s_0ceb942040064019599c8e185aefd794","value":"note:geranium","version_ref":"v_bdd9228ec4e90c451f943e4ecd99de68"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_1ad005f9476b0604a994f55ccab1f1c1","restricted_bridge":false,"source_ref":"s_0ceb942040064019599c8e185aefd794","value":"note:oakmoss","version_ref":"v_bdd9228ec4e90c451f943e4ecd99de68"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_20cf884a4951e21a1b781bdfacf9eb00","restricted_bridge":false,"source_ref":"s_0ceb942040064019599c8e185aefd794","value":"note:lavender","version_ref":"v_bdd9228ec4e90c451f943e4ecd99de68"},{"attribute":"context","channel":"manufacturer_authored_content","layer":null,"polarity":"positive","ref":"e_301a3ea0fddc47cedb701f8c3ddc3fb5","restricted_bridge":false,"source_ref":"s_72b89656bfbfa9cf9fefaaef4d821b4c","value":"use:daily_office_casual_warm_weather","version_ref":"v_13aa0204e73445510110ff9166a82c24"}],"classification":"both_documentary_axes","code":"0036","concentration":"EDT","same_source_manufacturer_dual":false},
{"claims":[],"classification":"attributed_use_only","code":"0037","concentration":"EDT","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_d556b91ec8405b369fda1c8c852072c3","restricted_bridge":false,"source_ref":"s_96b60147e180d3296de7f733d74c5320","value":"note:iris","version_ref":"v_a1de9ad654da8d7bb8a3e275b1d52ad7"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_b8f529b04626504b0207cbfbaf862f68","restricted_bridge":false,"source_ref":"s_96b60147e180d3296de7f733d74c5320","value":"note:iris","version_ref":"v_a1de9ad654da8d7bb8a3e275b1d52ad7"},{"attribute":"context","channel":"professional_editorial","layer":null,"polarity":"positive","ref":"e_c95a34bfb1c098cd5bd2d780b863834c","restricted_bridge":false,"source_ref":"s_c392d7688aa935e1888b66dbf8a01386","value":"use:evening_editorial_selection","version_ref":"v_5a5873553c2ac7e137ab9a5162189afe"}],"classification":"both_documentary_axes","code":"0038","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[],"classification":"taste_only","code":"0039","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[],"classification":"neither_axis_sufficient","code":"0040","concentration":"EDT","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"note","channel":"manufacturer_authored_content","layer":"top","polarity":"positive","ref":"e_f78cbf52adc5eb234a7c13abf92b11cb","restricted_bridge":false,"source_ref":"s_5a0a197f6a2a39134fb3ba33a8d8d1f4","value":"note:cypress","version_ref":"v_130561394b201ac7c6a4d4efce14ea7b"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"heart","polarity":"positive","ref":"e_ebd4ecb35c00fb1ea1d15d8f63fae309","restricted_bridge":false,"source_ref":"s_5a0a197f6a2a39134fb3ba33a8d8d1f4","value":"note:haiti vetyver","version_ref":"v_130561394b201ac7c6a4d4efce14ea7b"}],"classification":"taste_only","code":"0042","concentration":"EDT","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_de941b791269d3ae835781c25b2dfc8c","restricted_bridge":false,"source_ref":"s_3f5faf278e4ceed382e0026d39ab0a3a","value":"note:pomegranate","version_ref":"v_3aa7992fb9e4cc0f34c1050d190ce8e3"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_11329f19c3690b56217d6f8a94b7018b","restricted_bridge":false,"source_ref":"s_3f5faf278e4ceed382e0026d39ab0a3a","value":"note:mahogany","version_ref":"v_3aa7992fb9e4cc0f34c1050d190ce8e3"}],"classification":"both_documentary_axes","code":"0043","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_ddc46a417cbabbe5c01c193ac8772469","restricted_bridge":false,"source_ref":"s_670962edf9f48e9a93fd0fdb632c5826","value":"note:osmanthus","version_ref":"v_8cd07ca8f6554de893cd043d3792bf5a"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_2d287e776e4c43a29bd7ba0d6d168ea7","restricted_bridge":false,"source_ref":"s_670962edf9f48e9a93fd0fdb632c5826","value":"note:orange blossom","version_ref":"v_8cd07ca8f6554de893cd043d3792bf5a"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_eb23c4efee357857c7de5619f059e703","restricted_bridge":false,"source_ref":"s_670962edf9f48e9a93fd0fdb632c5826","value":"note:amber","version_ref":"v_8cd07ca8f6554de893cd043d3792bf5a"}],"classification":"both_documentary_axes","code":"0046","concentration":"EDT","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"note","channel":"manufacturer_authored_content","layer":"unknown","polarity":"positive","ref":"e_c77a3033f68bff397cc57b9583a42cd1","restricted_bridge":false,"source_ref":"s_3425637b978d9885b163d7e014b70845","value":"note:jasmine","version_ref":"v_9e62da76cc1bec1d2601f993858b2619"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"unknown","polarity":"positive","ref":"e_3db1cecebdd10bbec3530efe8fb015a8","restricted_bridge":false,"source_ref":"s_3425637b978d9885b163d7e014b70845","value":"note:orange blossom","version_ref":"v_9e62da76cc1bec1d2601f993858b2619"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"unknown","polarity":"positive","ref":"e_848b1888a88bba6851b694d5982ac972","restricted_bridge":false,"source_ref":"s_3425637b978d9885b163d7e014b70845","value":"note:ylang-ylang","version_ref":"v_9e62da76cc1bec1d2601f993858b2619"}],"classification":"taste_only","code":"0047","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"note","channel":"manufacturer_authored_content","layer":"top","polarity":"positive","ref":"e_bfaa9b45e181aa435a4024015a53fdc8","restricted_bridge":false,"source_ref":"s_a8e4647bbbe0d98a0e048d82b869546a","value":"note:pink pepper","version_ref":"v_2950bab45a03d15b97f8b1b47f00711a"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"top","polarity":"positive","ref":"e_9cb2c0bba78ec81ee2bc3aa67a2fd61d","restricted_bridge":false,"source_ref":"s_a8e4647bbbe0d98a0e048d82b869546a","value":"note:nutmeg","version_ref":"v_2950bab45a03d15b97f8b1b47f00711a"}],"classification":"taste_only","code":"0048","concentration":"EDT","same_source_manufacturer_dual":false},
{"claims":[],"classification":"attributed_use_only","code":"0050","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[],"classification":"neither_axis_sufficient","code":"0052","concentration":"EDT","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"manufacturer_authored_content","layer":null,"polarity":"positive","ref":"e_792596bdad223c05f9f2a30f4ce71185","restricted_bridge":false,"source_ref":"s_759e538ab16185958852d0c3ae288c0b","value":"note:marine accord","version_ref":"v_cf667a766ecb62417f49f01a4a9ea37a"},{"attribute":"context","channel":"manufacturer_authored_content","layer":null,"polarity":"positive","ref":"e_5c21f6a4c5f55012aae9da5efb5ac978","restricted_bridge":false,"source_ref":"s_759e538ab16185958852d0c3ae288c0b","value":"use:daytime_warm_weather_sport_office_everyday_spring_summer","version_ref":"v_cf667a766ecb62417f49f01a4a9ea37a"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"top","polarity":"positive","ref":"e_1de083bb7a4d4b482752876aa3d79fb4","restricted_bridge":false,"source_ref":"s_759e538ab16185958852d0c3ae288c0b","value":"note:grapefruit","version_ref":"v_cf667a766ecb62417f49f01a4a9ea37a"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"base","polarity":"positive","ref":"e_55360b44fa5d58c5a172cfad20af69ce","restricted_bridge":false,"source_ref":"s_759e538ab16185958852d0c3ae288c0b","value":"note:gaiac wood","version_ref":"v_cf667a766ecb62417f49f01a4a9ea37a"}],"classification":"both_documentary_axes","code":"0053","concentration":"EDT","same_source_manufacturer_dual":true},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_f7689e3155de4b4cd5ce15cb47a2c696","restricted_bridge":false,"source_ref":"s_6ade7d29384280919ba25f6bc0117b1f","value":"note:jasmine","version_ref":"v_35762b923b432ccdde5373b233c08e58"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_6347e0271f0f6c5b0495e038fb3d9df7","restricted_bridge":false,"source_ref":"s_6ade7d29384280919ba25f6bc0117b1f","value":"note:ylang-ylang","version_ref":"v_35762b923b432ccdde5373b233c08e58"},{"attribute":"context","channel":"manufacturer_authored_content","layer":null,"polarity":"positive","ref":"e_d52f043b48447bf028e272ec4ebabdb3","restricted_bridge":false,"source_ref":"s_95b73f38f238cd6241307ddde906bd49","value":"use:spring_summer_also_year_round","version_ref":"v_1f08f0d985d4e4bc4a4754e847686f7c"}],"classification":"both_documentary_axes","code":"0054","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_fac85bc8444531b16b333b4dba2ca519","restricted_bridge":false,"source_ref":"s_9d644309657771589a6424bd63ecc85c","value":"note:jasmine","version_ref":"v_53f43fba33b37dbe8f288f9a0004a089"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_5f9137c213e83ef320c7a06bb1c12a2b","restricted_bridge":false,"source_ref":"s_9d644309657771589a6424bd63ecc85c","value":"note:sandalwood","version_ref":"v_53f43fba33b37dbe8f288f9a0004a089"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_2a28aed0d6863d09151ac32d1dc91e28","restricted_bridge":false,"source_ref":"s_9d644309657771589a6424bd63ecc85c","value":"note:bergamot","version_ref":"v_53f43fba33b37dbe8f288f9a0004a089"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_a87b2fc12b299befd207ce794527d048","restricted_bridge":false,"source_ref":"s_9d644309657771589a6424bd63ecc85c","value":"note:mandarin","version_ref":"v_53f43fba33b37dbe8f288f9a0004a089"}],"classification":"both_documentary_axes","code":"0055","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_4bb62a550070f1602751cd0bd0d5f4e5","restricted_bridge":false,"source_ref":"s_45a6fecaaa1fea3d03d7f131d7919e2d","value":"note:vetiver","version_ref":"v_9f180ef89d3d3bd596bd1d75e5b8aca8"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_2b3af8f2980f69ca807074a14cfeed5b","restricted_bridge":false,"source_ref":"s_45a6fecaaa1fea3d03d7f131d7919e2d","value":"note:patchouli","version_ref":"v_9f180ef89d3d3bd596bd1d75e5b8aca8"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_bbc15a1bf125df841f6f6235eaba2b5a","restricted_bridge":false,"source_ref":"s_45a6fecaaa1fea3d03d7f131d7919e2d","value":"note:leather","version_ref":"v_9f180ef89d3d3bd596bd1d75e5b8aca8"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_2225b138f010edca91d871b13c25405b","restricted_bridge":false,"source_ref":"s_45a6fecaaa1fea3d03d7f131d7919e2d","value":"note:coriander","version_ref":"v_9f180ef89d3d3bd596bd1d75e5b8aca8"}],"classification":"taste_only","code":"0056","concentration":"EDT","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"manufacturer_authored_content","layer":null,"polarity":"positive","ref":"e_63532477586d28b64713c8595b4b26e3","restricted_bridge":false,"source_ref":"s_54c1ed01f393d1c934708882613da0ce","value":"note:dark chocolate","version_ref":"v_0125d6fabc5c5f3c66cde13442f036b0"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"heart","polarity":"positive","ref":"e_b881ad9c8f10c8e8ac09dfb7a91637e5","restricted_bridge":false,"source_ref":"s_54c1ed01f393d1c934708882613da0ce","value":"note:lavender","version_ref":"v_0125d6fabc5c5f3c66cde13442f036b0"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"top","polarity":"positive","ref":"e_12826b3f66fce81d502b43bf993a324d","restricted_bridge":false,"source_ref":"s_54c1ed01f393d1c934708882613da0ce","value":"note:watermelon","version_ref":"v_0125d6fabc5c5f3c66cde13442f036b0"}],"classification":"taste_only","code":"0057","concentration":"EDT","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"note","channel":"manufacturer_authored_content","layer":"base","polarity":"positive","ref":"e_de47a314e1ae9445a78d6e339d46b435","restricted_bridge":false,"source_ref":"s_7e23ce607dcf3d8cbba5d6e55c529aa2","value":"note:sandalwood","version_ref":"v_4b6b981de7858f2a3deefb5df5e47562"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"top","polarity":"positive","ref":"e_3f568e9bf9d6c07669bb4a812af7438d","restricted_bridge":false,"source_ref":"s_7e23ce607dcf3d8cbba5d6e55c529aa2","value":"note:ginger","version_ref":"v_4b6b981de7858f2a3deefb5df5e47562"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"base","polarity":"positive","ref":"e_2e3a2cba31467c7b864bca1bf74a84c9","restricted_bridge":false,"source_ref":"s_7e23ce607dcf3d8cbba5d6e55c529aa2","value":"note:vetiver","version_ref":"v_4b6b981de7858f2a3deefb5df5e47562"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"heart","polarity":"positive","ref":"e_32666d006f155972537501a7eff49e83","restricted_bridge":false,"source_ref":"s_7e23ce607dcf3d8cbba5d6e55c529aa2","value":"note:violet leaves","version_ref":"v_4b6b981de7858f2a3deefb5df5e47562"}],"classification":"taste_only","code":"0059","concentration":"EDT","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_335ebc1c8dd746480f065a93f7bb2d10","restricted_bridge":false,"source_ref":"s_eb1452b0176151e17c74b3a45eb86276","value":"note:vanilla","version_ref":"v_6d6024cd3eaf9eaf8f7d81d72fb4e001"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_7a855d9d5b9ec23bbea4e371e27d4dc2","restricted_bridge":false,"source_ref":"s_eb1452b0176151e17c74b3a45eb86276","value":"note:patchouli","version_ref":"v_6d6024cd3eaf9eaf8f7d81d72fb4e001"},{"attribute":"context","channel":"manufacturer_authored_content","layer":null,"polarity":"positive","ref":"e_d063edea076a449c864a74e6c0c702c7","restricted_bridge":false,"source_ref":"s_6bd16d92062f5882aff3707b82011979","value":"use:everyday_summer_wear","version_ref":"v_eb2a8505ac086e4dc129315ae393d7bf"}],"classification":"both_documentary_axes","code":"0061","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[],"classification":"attributed_use_only","code":"0062","concentration":"EDT","same_source_manufacturer_dual":false},
{"claims":[],"classification":"attributed_use_only","code":"0065","concentration":"Parfum","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"note","channel":"manufacturer_authored_content","layer":"unknown","polarity":"positive","ref":"e_5e01836717a26b88d1e570cfe3664c0a","restricted_bridge":false,"source_ref":"s_6b7d400542e193ae4eba1edf617a3a06","value":"note:neroli","version_ref":"v_f9e029928a65fac7002719a56ac7a6ca"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"unknown","polarity":"positive","ref":"e_88e989110c8dbc35322ddb55c3ac3f46","restricted_bridge":false,"source_ref":"s_6b7d400542e193ae4eba1edf617a3a06","value":"note:rose de mai","version_ref":"v_f9e029928a65fac7002719a56ac7a6ca"}],"classification":"taste_only","code":"0068","concentration":"Extrait","same_source_manufacturer_dual":false},
{"claims":[],"classification":"attributed_use_only","code":"0071","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"note","channel":"manufacturer_authored_content","layer":"heart","polarity":"positive","ref":"e_e274290764f8aaa0fa941ee3cf62b894","restricted_bridge":false,"source_ref":"s_8c1b2e48d1361597a5b64c8b8f1c624c","value":"note:jasmine","version_ref":"v_5e3d2a754892bda04c7d7a452db9841d"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"heart","polarity":"positive","ref":"e_9023a0a4d4c09817a3767ff33fd2af9d","restricted_bridge":false,"source_ref":"s_8c1b2e48d1361597a5b64c8b8f1c624c","value":"note:rose","version_ref":"v_5e3d2a754892bda04c7d7a452db9841d"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"base","polarity":"positive","ref":"e_336ae5aa04b4e8f6bb70db211c30d235","restricted_bridge":false,"source_ref":"s_8c1b2e48d1361597a5b64c8b8f1c624c","value":"note:sandalwood","version_ref":"v_5e3d2a754892bda04c7d7a452db9841d"}],"classification":"taste_only","code":"0075","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"manufacturer_authored_content","layer":null,"polarity":"positive","ref":"e_d208b10b1fd7a3212064ac9b19e44b7d","restricted_bridge":false,"source_ref":"s_52d3dd131d9997e68a6f9d307a681596","value":"note:dark woods","version_ref":"v_7ff38fcd5caeb62289dd0bd4ec922202"},{"attribute":"named_note_or_accord","channel":"manufacturer_authored_content","layer":null,"polarity":"positive","ref":"e_d09e8698ab0fccc88744ccb30dbf96de","restricted_bridge":false,"source_ref":"s_52d3dd131d9997e68a6f9d307a681596","value":"note:golden amber accord","version_ref":"v_7ff38fcd5caeb62289dd0bd4ec922202"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"heart","polarity":"positive","ref":"e_0636932afcab0281856677eee9d3ca97","restricted_bridge":false,"source_ref":"s_52d3dd131d9997e68a6f9d307a681596","value":"note:patchouli","version_ref":"v_7ff38fcd5caeb62289dd0bd4ec922202"}],"classification":"taste_only","code":"0079","concentration":"Eau de Parfum Intense","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_8c3c27dde01a004f1c8bde771ca83d63","restricted_bridge":false,"source_ref":"s_4ad8278eb15b6f336f4beb575b4726d8","value":"note:amber","version_ref":"v_5db915904308f77b93295628bc6770fb"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_be101a13868b3ea563fdb7d8c3fc3f02","restricted_bridge":false,"source_ref":"s_4ad8278eb15b6f336f4beb575b4726d8","value":"note:blackcurrant","version_ref":"v_5db915904308f77b93295628bc6770fb"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_4efced606e4b0563609c778d0be02de6","restricted_bridge":false,"source_ref":"s_4ad8278eb15b6f336f4beb575b4726d8","value":"note:benzoin","version_ref":"v_5db915904308f77b93295628bc6770fb"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_a3ec37f6ba932018d60cfd05792b3830","restricted_bridge":false,"source_ref":"s_4ad8278eb15b6f336f4beb575b4726d8","value":"note:mandarin","version_ref":"v_5db915904308f77b93295628bc6770fb"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_5522358500684aae6e6b4df7d4e6b8d6","restricted_bridge":false,"source_ref":"s_4ad8278eb15b6f336f4beb575b4726d8","value":"note:jasmine","version_ref":"v_5db915904308f77b93295628bc6770fb"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_b1afc48ebbb1844acf8b8a8f111a5bb5","restricted_bridge":false,"source_ref":"s_4ad8278eb15b6f336f4beb575b4726d8","value":"note:vanilla","version_ref":"v_5db915904308f77b93295628bc6770fb"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_6cd042fca06528302006da78dfe452de","restricted_bridge":false,"source_ref":"s_4ad8278eb15b6f336f4beb575b4726d8","value":"note:coconut","version_ref":"v_5db915904308f77b93295628bc6770fb"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_93df68726a0e08a34684f896a42b38dd","restricted_bridge":false,"source_ref":"s_4ad8278eb15b6f336f4beb575b4726d8","value":"note:peach","version_ref":"v_5db915904308f77b93295628bc6770fb"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_89b20a70ff278e4f6ae9c4807042a5e4","restricted_bridge":false,"source_ref":"s_4ad8278eb15b6f336f4beb575b4726d8","value":"note:aquatic flowers","version_ref":"v_5db915904308f77b93295628bc6770fb"}],"classification":"taste_only","code":"0080","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_1de1dd4e1fff04ac24b64c06053e9031","restricted_bridge":false,"source_ref":"s_3a9b17a2e5184459b2e75dd4faf2dfa9","value":"note:cedarwood","version_ref":"v_66a16a09590b49071acb945c4f473e7c"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_839fb1e83ce0974bcd6f4381249a1c7d","restricted_bridge":false,"source_ref":"s_3a9b17a2e5184459b2e75dd4faf2dfa9","value":"note:rose","version_ref":"v_66a16a09590b49071acb945c4f473e7c"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_fb5ad69f2cac6eedcae6003b8d1b976e","restricted_bridge":false,"source_ref":"s_3a9b17a2e5184459b2e75dd4faf2dfa9","value":"note:vanilla","version_ref":"v_66a16a09590b49071acb945c4f473e7c"},{"attribute":"context","channel":"brand_regional_store_editorial","layer":null,"polarity":"positive","ref":"e_3146aca818663ed9c3e9b690fa2726bb","restricted_bridge":false,"source_ref":"s_5a5a4394259408367e417a7728ae0b6d","value":"use:romantic_evening","version_ref":"v_c3681fdd71d882ece427e9ec1f677262"}],"classification":"both_documentary_axes","code":"0081","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_1b15cac4dcfc827ed1d84f0201fac276","restricted_bridge":false,"source_ref":"s_923deac53e57c0aa28df753f750bc09e","value":"note:lavender","version_ref":"v_8e1be8cb301a2f64cfb745a4c41466df"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_20896f6db2e839a25ef09ab3bcbb1558","restricted_bridge":false,"source_ref":"s_923deac53e57c0aa28df753f750bc09e","value":"note:wood","version_ref":"v_8e1be8cb301a2f64cfb745a4c41466df"},{"attribute":"context","channel":"manufacturer_authored_content","layer":null,"polarity":"positive","ref":"e_874cb915a1ec3923829b84ba7ccee98f","restricted_bridge":false,"source_ref":"s_4e433bb881a287ace0bbcea13d2c4601","value":"use:fall_winter_evening_cooler_with_office_summer_caution","version_ref":"v_d0be3c62e588ac3a0a9480c60d5fd936"}],"classification":"both_documentary_axes","code":"0083","concentration":"Elixir","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_e68160b6cea88ca3fa0e4f6ab5a29c7f","restricted_bridge":false,"source_ref":"s_96819670bae050fe154b40aa8e439e37","value":"note:blackcurrant","version_ref":"v_9e24e04ea2fe4be089f4eda09c3887b1"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_53a056b3aa52b6f8876b20b7b2799916","restricted_bridge":false,"source_ref":"s_96819670bae050fe154b40aa8e439e37","value":"note:sandalwood","version_ref":"v_9e24e04ea2fe4be089f4eda09c3887b1"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_e9c7cebd783927ea988ae983aca404d7","restricted_bridge":false,"source_ref":"s_96819670bae050fe154b40aa8e439e37","value":"note:musk","version_ref":"v_9e24e04ea2fe4be089f4eda09c3887b1"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_481d322af2052fbc722e3e081ea933e6","restricted_bridge":false,"source_ref":"s_96819670bae050fe154b40aa8e439e37","value":"note:tea","version_ref":"v_9e24e04ea2fe4be089f4eda09c3887b1"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_985213a6aed5ed41e1373e4454f7d5d4","restricted_bridge":false,"source_ref":"s_96819670bae050fe154b40aa8e439e37","value":"note:bergamot","version_ref":"v_9e24e04ea2fe4be089f4eda09c3887b1"}],"classification":"taste_only","code":"0084","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[],"classification":"neither_axis_sufficient","code":"0085","concentration":"EDT","same_source_manufacturer_dual":false},
{"claims":[],"classification":"neither_axis_sufficient","code":"0086","concentration":"EDT","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"note","channel":"manufacturer_authored_content","layer":"unknown","polarity":"positive","ref":"e_463583295175915f1291d91e22d66484","restricted_bridge":false,"source_ref":"s_bfa1f37906d46d490da268abf7061f60","value":"note:cinnamon","version_ref":"v_725739d41c7f9ae7e939d004c9d1e05f"},{"attribute":"context","channel":"manufacturer_authored_content","layer":null,"polarity":"positive","ref":"e_e96fd1a1af0cc3b8fe6e3cb870706ccf","restricted_bridge":false,"source_ref":"s_bfa1f37906d46d490da268abf7061f60","value":"use:winter_chilly_nights_close_encounters","version_ref":"v_37b32243c7aa910bc293224c664c0fcc"},{"attribute":"named_note_or_accord","channel":"manufacturer_authored_content","layer":null,"polarity":"positive","ref":"e_16f669c77097cfc5f6be2b6f1161f71a","restricted_bridge":false,"source_ref":"s_bfa1f37906d46d490da268abf7061f60","value":"note:white leather accord","version_ref":"v_725739d41c7f9ae7e939d004c9d1e05f"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"unknown","polarity":"positive","ref":"e_7eb70186c9fe3885a32df085a5fc924e","restricted_bridge":false,"source_ref":"s_bfa1f37906d46d490da268abf7061f60","value":"note:tobacco","version_ref":"v_725739d41c7f9ae7e939d004c9d1e05f"}],"classification":"both_documentary_axes","code":"0087","concentration":"EDT","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_e9d69b29f69e912e70925817705e295f","restricted_bridge":false,"source_ref":"s_c80ce6fb1c7775e78b473f94b7c2c683","value":"note:saffron","version_ref":"v_4472cc68b67fc2769eed8d4870844c1e"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_b15f749acaa342660a361579b479d92f","restricted_bridge":false,"source_ref":"s_c80ce6fb1c7775e78b473f94b7c2c683","value":"note:thyme","version_ref":"v_4472cc68b67fc2769eed8d4870844c1e"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_83c78937ae69cef8a45e4cdc049db8dc","restricted_bridge":false,"source_ref":"s_c80ce6fb1c7775e78b473f94b7c2c683","value":"note:raspberry","version_ref":"v_4472cc68b67fc2769eed8d4870844c1e"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_f34454833e600c375417ce135020de5a","restricted_bridge":false,"source_ref":"s_c80ce6fb1c7775e78b473f94b7c2c683","value":"note:leather","version_ref":"v_4472cc68b67fc2769eed8d4870844c1e"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_25bead12a3894b88616687fd77fbf438","restricted_bridge":false,"source_ref":"s_c80ce6fb1c7775e78b473f94b7c2c683","value":"note:amberwood","version_ref":"v_4472cc68b67fc2769eed8d4870844c1e"}],"classification":"taste_only","code":"0091","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"manufacturer_authored_content","layer":null,"polarity":"positive","ref":"e_89c2557917dd5d51a79c9c1cc8dc6c93","restricted_bridge":false,"source_ref":"s_1aa85d97f89617ec5a93adf7cd95938b","value":"note:rose bouquet accord","version_ref":"v_d7738c50ebe96a56659249991cfd6816"},{"attribute":"named_note_or_accord","channel":"manufacturer_authored_content","layer":null,"polarity":"positive","ref":"e_359245c02df5ac231aac8159d0145ef6","restricted_bridge":false,"source_ref":"s_1aa85d97f89617ec5a93adf7cd95938b","value":"note:star anise accord","version_ref":"v_d7738c50ebe96a56659249991cfd6816"}],"classification":"taste_only","code":"0093","concentration":"EDT","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_d7a0cc78d25e07dbba9a489fba5eaf13","restricted_bridge":false,"source_ref":"s_5f4449dc641a17ac0294029ba2a69aba","value":"note:vanilla","version_ref":"v_b4e8ef7adae9b8cfd4bdc26e12e3d335"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_87a24093b6abcc74b81cde6c190c51be","restricted_bridge":false,"source_ref":"s_5f4449dc641a17ac0294029ba2a69aba","value":"note:mandarin","version_ref":"v_b4e8ef7adae9b8cfd4bdc26e12e3d335"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_06e950679946259a6d839f905af3a67e","restricted_bridge":false,"source_ref":"s_5f4449dc641a17ac0294029ba2a69aba","value":"note:amber","version_ref":"v_b4e8ef7adae9b8cfd4bdc26e12e3d335"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_04d6188c3b288b5873395680162470e9","restricted_bridge":false,"source_ref":"s_5f4449dc641a17ac0294029ba2a69aba","value":"note:caramel","version_ref":"v_b4e8ef7adae9b8cfd4bdc26e12e3d335"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_197796ebfb37dffe1c5e4b4e80af7a67","restricted_bridge":false,"source_ref":"s_5f4449dc641a17ac0294029ba2a69aba","value":"note:honeysuckle","version_ref":"v_b4e8ef7adae9b8cfd4bdc26e12e3d335"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_7d9f43fdf275d856ce1bd24b7a1782d2","restricted_bridge":false,"source_ref":"s_5f4449dc641a17ac0294029ba2a69aba","value":"note:jasmine","version_ref":"v_b4e8ef7adae9b8cfd4bdc26e12e3d335"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_1a9b11274272a0486a21b47e137e52af","restricted_bridge":false,"source_ref":"s_5f4449dc641a17ac0294029ba2a69aba","value":"note:sandalwood","version_ref":"v_b4e8ef7adae9b8cfd4bdc26e12e3d335"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_05365c56fe36c5877d023c77cc4494f3","restricted_bridge":false,"source_ref":"s_5f4449dc641a17ac0294029ba2a69aba","value":"note:gardenia","version_ref":"v_b4e8ef7adae9b8cfd4bdc26e12e3d335"}],"classification":"taste_only","code":"0094","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_4b90125ced1006b97c20eb2b7ddacb6b","restricted_bridge":false,"source_ref":"s_469e28d6cba60cb35cf1d2ed4859085e","value":"note:ginger","version_ref":"v_6b1f5a6813885335fa254596ca63c137"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_1de1059dd5e346dafa65f3fbbdc25cfc","restricted_bridge":false,"source_ref":"s_469e28d6cba60cb35cf1d2ed4859085e","value":"note:tonka bean","version_ref":"v_6b1f5a6813885335fa254596ca63c137"}],"classification":"both_documentary_axes","code":"0096","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_1cbc0b95dac057729260f502207bf009","restricted_bridge":false,"source_ref":"s_c76bb63f691044ef906f22be9d3742ac","value":"note:tonka bean","version_ref":"v_a74ec1495fd4912e52c9f40da3a7b39f"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_54bf424ecda4e9bd348e2fe69c329361","restricted_bridge":false,"source_ref":"s_c76bb63f691044ef906f22be9d3742ac","value":"note:oud","version_ref":"v_a74ec1495fd4912e52c9f40da3a7b39f"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_4033f556bd83bdfb4f66028b7e357d19","restricted_bridge":false,"source_ref":"s_c76bb63f691044ef906f22be9d3742ac","value":"note:amber","version_ref":"v_a74ec1495fd4912e52c9f40da3a7b39f"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_e6718307bf32d7316c6c32a99b29418f","restricted_bridge":false,"source_ref":"s_c76bb63f691044ef906f22be9d3742ac","value":"note:pink pepper","version_ref":"v_a74ec1495fd4912e52c9f40da3a7b39f"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_86e52bd83f95c5267dad0039de839d3a","restricted_bridge":false,"source_ref":"s_c76bb63f691044ef906f22be9d3742ac","value":"note:patchouli","version_ref":"v_a74ec1495fd4912e52c9f40da3a7b39f"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_ad8544eb748a2ee25283061c6dede6e9","restricted_bridge":false,"source_ref":"s_c76bb63f691044ef906f22be9d3742ac","value":"note:cardamom","version_ref":"v_a74ec1495fd4912e52c9f40da3a7b39f"}],"classification":"both_documentary_axes","code":"0097","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_5b818c8b421c12bc2940d26a426d3c26","restricted_bridge":false,"source_ref":"s_a20ad650fbf6a9f2a385af2abcd8f50f","value":"note:saffron","version_ref":"v_603ee23b85e221b31a4bb246dea2acbf"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_fc8718e241fd664ee2bb99f31d157152","restricted_bridge":false,"source_ref":"s_a20ad650fbf6a9f2a385af2abcd8f50f","value":"note:amber","version_ref":"v_603ee23b85e221b31a4bb246dea2acbf"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_2e4a0c413545e427cbac1a509e34b415","restricted_bridge":false,"source_ref":"s_a20ad650fbf6a9f2a385af2abcd8f50f","value":"note:sandalwood","version_ref":"v_603ee23b85e221b31a4bb246dea2acbf"}],"classification":"taste_only","code":"0098","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_3eda37130f8cf8ad7da54cee8625dec9","restricted_bridge":false,"source_ref":"s_e971c758d977b82054a27a506e9766db","value":"note:grapefruit","version_ref":"v_ac835f3ba800e49ffc6ed2fc0dba845c"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_04a285c4b12db81e6379d065e581e008","restricted_bridge":false,"source_ref":"s_e971c758d977b82054a27a506e9766db","value":"note:nutmeg","version_ref":"v_ac835f3ba800e49ffc6ed2fc0dba845c"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_28a41809f4b091985fd0a8caa925a367","restricted_bridge":false,"source_ref":"s_e971c758d977b82054a27a506e9766db","value":"note:oakmoss","version_ref":"v_ac835f3ba800e49ffc6ed2fc0dba845c"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_11dc2c7e3f1e7591290af578a60ed0fe","restricted_bridge":false,"source_ref":"s_e971c758d977b82054a27a506e9766db","value":"note:pimento","version_ref":"v_ac835f3ba800e49ffc6ed2fc0dba845c"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_a2e989116d13231c310b6ec262b4edfb","restricted_bridge":false,"source_ref":"s_e971c758d977b82054a27a506e9766db","value":"note:vetiver","version_ref":"v_ac835f3ba800e49ffc6ed2fc0dba845c"}],"classification":"both_documentary_axes","code":"0099","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_3c095c055652da2d5cf778ad2ad49276","restricted_bridge":false,"source_ref":"s_fc30ed18c85c0eda273ef1240a4b076d","value":"note:labdanum","version_ref":"v_12ef55d2ee9c0efa6e9118e7f0dd022f"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_b6233946dd49e6e22605cef08b786929","restricted_bridge":false,"source_ref":"s_fc30ed18c85c0eda273ef1240a4b076d","value":"note:davana","version_ref":"v_12ef55d2ee9c0efa6e9118e7f0dd022f"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_76bc4bfdbea2a1e5948a647d5542c10c","restricted_bridge":false,"source_ref":"s_fc30ed18c85c0eda273ef1240a4b076d","value":"note:blood orange","version_ref":"v_12ef55d2ee9c0efa6e9118e7f0dd022f"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_047093f4eb98443a040e414ac084bd43","restricted_bridge":false,"source_ref":"s_fc30ed18c85c0eda273ef1240a4b076d","value":"note:sandalwood","version_ref":"v_12ef55d2ee9c0efa6e9118e7f0dd022f"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_ab4dd84a83fa4af336f97ff00cff82cf","restricted_bridge":false,"source_ref":"s_fc30ed18c85c0eda273ef1240a4b076d","value":"note:patchouli","version_ref":"v_12ef55d2ee9c0efa6e9118e7f0dd022f"}],"classification":"taste_only","code":"0100","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_3d69e55c71f182b68830d49ac0acc3bc","restricted_bridge":false,"source_ref":"s_2936f723da83347fca6f68c32549012d","value":"note:patchouli","version_ref":"v_3d97b577716d3d955f754a16b8916b67"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_8dcd482a9cb97557d7471890b07566e5","restricted_bridge":false,"source_ref":"s_2936f723da83347fca6f68c32549012d","value":"note:sichuan pepper","version_ref":"v_3d97b577716d3d955f754a16b8916b67"}],"classification":"both_documentary_axes","code":"0101","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"note","channel":"manufacturer_authored_content","layer":"unknown","polarity":"positive","ref":"e_1f6a225095cc9e4b180c54fa4aac2e58","restricted_bridge":false,"source_ref":"s_1e4f409d83417ac8907f7adf39bb4c38","value":"note:cardamom","version_ref":"v_04e8fa58f458d8bd0d794e6cbdfe0e3c"},{"attribute":"context","channel":"professional_editorial","layer":null,"polarity":"positive","ref":"e_989194f68b3182654e2659db14f3f5c2","restricted_bridge":false,"source_ref":"s_b4ca1fa4a4fbaeb4b1b92bbfb9ed75a0","value":"use:special_occasion_editorial","version_ref":"v_0d9822de97d47a37967bd54090f89568"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"unknown","polarity":"positive","ref":"e_d912652b440900cfe056ee1d162428e5","restricted_bridge":false,"source_ref":"s_1e4f409d83417ac8907f7adf39bb4c38","value":"note:jasmine sambac","version_ref":"v_04e8fa58f458d8bd0d794e6cbdfe0e3c"},{"attribute":"named_note_or_accord","channel":"manufacturer_authored_content","layer":null,"polarity":"positive","ref":"e_f91530699afd41ba1ee9234378c8d575","restricted_bridge":false,"source_ref":"s_1e4f409d83417ac8907f7adf39bb4c38","value":"note:black leather accord","version_ref":"v_04e8fa58f458d8bd0d794e6cbdfe0e3c"}],"classification":"both_documentary_axes","code":"0102","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_53e638b33a84f34cad7d4bb520a0a033","restricted_bridge":false,"source_ref":"s_79ec5e445453eb1425a4d5a64abfdf37","value":"note:cardamom","version_ref":"v_f5fe15d1f2c4a1a8ce920c27da04f43f"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_96f8dd80d89dd4e84e44f61211775f4f","restricted_bridge":false,"source_ref":"s_79ec5e445453eb1425a4d5a64abfdf37","value":"note:bergamot","version_ref":"v_f5fe15d1f2c4a1a8ce920c27da04f43f"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_303b42c5ce64a4d588b1233b851fad2b","restricted_bridge":false,"source_ref":"s_79ec5e445453eb1425a4d5a64abfdf37","value":"note:ylang-ylang","version_ref":"v_f5fe15d1f2c4a1a8ce920c27da04f43f"}],"classification":"taste_only","code":"0103","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_96739562dfc22b4b54115a54d4e720ed","restricted_bridge":false,"source_ref":"s_1fee92868020d28377c06069c18b61c3","value":"note:lavender","version_ref":"v_092e9850e1a3a5abdac6639831d7862f"}],"classification":"taste_only","code":"0104","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_028aaecb7948a41475778f2a49f365cd","restricted_bridge":false,"source_ref":"s_d7bba42900bff7907b927eb89f44109a","value":"note:griotte syrup","version_ref":"v_20a348baac6e8ec55c447eaf026ea772"},{"attribute":"context","channel":"professional_editorial","layer":null,"polarity":"positive","ref":"e_337c62366b63d5914b0ba6b7662ef2b8","restricted_bridge":false,"source_ref":"s_2e6f08dfbd3c2a1494cff46654734f7a","value":"use:date_night_editorial","version_ref":"v_12063bb57fb65ead34c33f875d96f1a6"}],"classification":"both_documentary_axes","code":"0105","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_eb19c63d3d92f9ec941d75e25b2feb90","restricted_bridge":false,"source_ref":"s_3e7fa6ae85b0976c1336501cd9d82754","value":"note:thyme","version_ref":"v_95b75bb28b8e0140190b74ff2436ca19"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_517a2e1738dab11145a1a2e0e7060382","restricted_bridge":false,"source_ref":"s_3e7fa6ae85b0976c1336501cd9d82754","value":"note:musk","version_ref":"v_95b75bb28b8e0140190b74ff2436ca19"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_29680463e5c7ff0ae023f60f2befc04d","restricted_bridge":false,"source_ref":"s_3e7fa6ae85b0976c1336501cd9d82754","value":"note:rose","version_ref":"v_95b75bb28b8e0140190b74ff2436ca19"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_d3eba8ce285b23b75859f3d2c19838b8","restricted_bridge":false,"source_ref":"s_3e7fa6ae85b0976c1336501cd9d82754","value":"note:amber","version_ref":"v_95b75bb28b8e0140190b74ff2436ca19"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_9851a7f1914d971858bea6b0303b861e","restricted_bridge":false,"source_ref":"s_3e7fa6ae85b0976c1336501cd9d82754","value":"note:suede","version_ref":"v_95b75bb28b8e0140190b74ff2436ca19"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_f8b6ed0e81372324ccb04358beedc244","restricted_bridge":false,"source_ref":"s_3e7fa6ae85b0976c1336501cd9d82754","value":"note:saffron","version_ref":"v_95b75bb28b8e0140190b74ff2436ca19"}],"classification":"taste_only","code":"0106","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_1d4d41e3c7bf3b11a0ce3512f50ee4c5","restricted_bridge":false,"source_ref":"s_e53127051df9e6d096a422ea5831e0e3","value":"note:amber","version_ref":"v_e42133277b772664dabf41c0f956622d"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_4de288dc650020662f34cafbc41e7e21","restricted_bridge":false,"source_ref":"s_e53127051df9e6d096a422ea5831e0e3","value":"note:lemon","version_ref":"v_e42133277b772664dabf41c0f956622d"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_550fb80609db9b71fbbc34f59e04666d","restricted_bridge":false,"source_ref":"s_e53127051df9e6d096a422ea5831e0e3","value":"note:rose","version_ref":"v_e42133277b772664dabf41c0f956622d"}],"classification":"taste_only","code":"0107","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"note","channel":"manufacturer_authored_content","layer":"unknown","polarity":"positive","ref":"e_923364b9eb427a38ac61fcc9ab01fd40","restricted_bridge":false,"source_ref":"s_d2791f648975c8ac7267a0e3f97b5c86","value":"note:labdanum","version_ref":"v_1bb1d5353f62ad4df583f86fd707facf"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"unknown","polarity":"positive","ref":"e_d706b71aa95ed0687d00530e011d9303","restricted_bridge":false,"source_ref":"s_d2791f648975c8ac7267a0e3f97b5c86","value":"note:rose","version_ref":"v_1bb1d5353f62ad4df583f86fd707facf"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"unknown","polarity":"positive","ref":"e_21c7c453a0e64a8beff44dea76f86b42","restricted_bridge":false,"source_ref":"s_d2791f648975c8ac7267a0e3f97b5c86","value":"note:patchouli","version_ref":"v_1bb1d5353f62ad4df583f86fd707facf"}],"classification":"taste_only","code":"0108","concentration":"Eau de Parfum Intense","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"note","channel":"manufacturer_authored_content","layer":"unknown","polarity":"positive","ref":"e_f2063690279a6a3b17117ad398602f2e","restricted_bridge":false,"source_ref":"s_6d2919e381b744e226f2fa2ee7b5ac08","value":"note:patchouli","version_ref":"v_f55575cc52655c1061beb7f79f1d9c32"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"unknown","polarity":"positive","ref":"e_ad3fe278bd8a8785c347f725633d90dc","restricted_bridge":false,"source_ref":"s_6d2919e381b744e226f2fa2ee7b5ac08","value":"note:benzoin","version_ref":"v_f55575cc52655c1061beb7f79f1d9c32"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"unknown","polarity":"positive","ref":"e_e2e299efb1bb867285277ec433ddb55c","restricted_bridge":false,"source_ref":"s_6d2919e381b744e226f2fa2ee7b5ac08","value":"note:vanilla","version_ref":"v_f55575cc52655c1061beb7f79f1d9c32"}],"classification":"taste_only","code":"0109","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"note","channel":"manufacturer_authored_content","layer":"top","polarity":"positive","ref":"e_8f5ef7e5b6b6c9640c91952c82fbd384","restricted_bridge":false,"source_ref":"s_59506da630f057eaef7062452393a999","value":"note:freesia","version_ref":"v_5ed0fd705777edadea93e56844335158"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"base","polarity":"positive","ref":"e_4ececad0d5eb614ef66119eb62d721da","restricted_bridge":false,"source_ref":"s_59506da630f057eaef7062452393a999","value":"note:sandalwood","version_ref":"v_5ed0fd705777edadea93e56844335158"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"top","polarity":"positive","ref":"e_e1f094bb59772c30ff2a7ceedd9060f5","restricted_bridge":false,"source_ref":"s_59506da630f057eaef7062452393a999","value":"note:sage","version_ref":"v_5ed0fd705777edadea93e56844335158"}],"classification":"taste_only","code":"0110","concentration":"Eau de Parfum for Women","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_cd082c9171b95d19dc17b807b9c9d527","restricted_bridge":false,"source_ref":"s_480158c6e4b3666eb6d113ddb7bfded6","value":"note:jasmine sambac","version_ref":"v_64b72450dbbece5d6b41a2a2d4b2606a"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_6eb400286a40062cda96ac4bfadc5f64","restricted_bridge":false,"source_ref":"s_480158c6e4b3666eb6d113ddb7bfded6","value":"note:tuberose","version_ref":"v_64b72450dbbece5d6b41a2a2d4b2606a"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_8e177c1b78fea958223434244e21514e","restricted_bridge":false,"source_ref":"s_480158c6e4b3666eb6d113ddb7bfded6","value":"note:almond","version_ref":"v_64b72450dbbece5d6b41a2a2d4b2606a"},{"attribute":"context","channel":"manufacturer_authored_content","layer":null,"polarity":"positive","ref":"e_450bc1ce2c936077a688f316a9559081","restricted_bridge":false,"source_ref":"s_9b9ab09c62326f2c027e12c894e3fe4f","value":"use:day_night_everyday_evenings_special_occasions","version_ref":"v_0dcf4f2d48e6f74f965e3b75e6d16177"}],"classification":"both_documentary_axes","code":"0111","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"context","channel":"manufacturer_authored_content","layer":null,"polarity":"positive","ref":"e_4a929b8bd4cd2f6d39cde5acf5447197","restricted_bridge":true,"source_ref":"s_38b7448937fa2a9914dd8e496a86d8f3","value":"use:workdays_weekends_nights_out_bold_impression","version_ref":"v_400abcfdf8a46f8f3c71c7d1c370f4db"},{"attribute":"named_note_or_accord","channel":"manufacturer_authored_content","layer":null,"polarity":"positive","ref":"e_823cdadf174ca71ac6f87ead16916547","restricted_bridge":false,"source_ref":"s_79d971dcce1a7d27fac47456c877bb7f","value":"note:ambar wood","version_ref":"v_5ea3c6b457382e306ebcd2e1512f609f"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"heart","polarity":"positive","ref":"e_71b50b850ee06006a05c6a114aeeed07","restricted_bridge":false,"source_ref":"s_79d971dcce1a7d27fac47456c877bb7f","value":"note:cedarwood","version_ref":"v_5ea3c6b457382e306ebcd2e1512f609f"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"heart","polarity":"positive","ref":"e_34949815cb278272ac584d9ffca54975","restricted_bridge":false,"source_ref":"s_79d971dcce1a7d27fac47456c877bb7f","value":"note:sage","version_ref":"v_5ea3c6b457382e306ebcd2e1512f609f"}],"classification":"both_documentary_axes","code":"0112","concentration":"EDT","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"note","channel":"manufacturer_authored_content","layer":"heart","polarity":"positive","ref":"e_9d3d7880487e55f497a7923f70f5f3c7","restricted_bridge":false,"source_ref":"s_ab7f921ade2667b50e415d15c28ee430","value":"note:jasmine","version_ref":"v_6e689db860d0c575ffc5b12633faf7e0"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"top","polarity":"positive","ref":"e_1fce3e448b87727a54bbe867202d725b","restricted_bridge":false,"source_ref":"s_ab7f921ade2667b50e415d15c28ee430","value":"note:lily of the valley","version_ref":"v_6e689db860d0c575ffc5b12633faf7e0"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"heart","polarity":"positive","ref":"e_979698f4ae38ff9b2a1a3b25577e75bc","restricted_bridge":false,"source_ref":"s_ab7f921ade2667b50e415d15c28ee430","value":"note:myrrh","version_ref":"v_6e689db860d0c575ffc5b12633faf7e0"}],"classification":"taste_only","code":"0113","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_c7fe56014d70bb084bf8c5826389dd3c","restricted_bridge":false,"source_ref":"s_e2e2559e415bd34a2501f8a9fe9ca407","value":"note:osmanthus","version_ref":"v_d90bdba84a60b15b016216559348bbcd"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_0acc750851d546234ee47d18263c6075","restricted_bridge":false,"source_ref":"s_e2e2559e415bd34a2501f8a9fe9ca407","value":"note:sandalwood","version_ref":"v_d90bdba84a60b15b016216559348bbcd"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_574246206d1c2543fba4ba506d2945d6","restricted_bridge":false,"source_ref":"s_e2e2559e415bd34a2501f8a9fe9ca407","value":"note:ambergris","version_ref":"v_d90bdba84a60b15b016216559348bbcd"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_b2e7a6794a75abb0ae0d3a19e56d5d88","restricted_bridge":false,"source_ref":"s_e2e2559e415bd34a2501f8a9fe9ca407","value":"note:jasmine sambac","version_ref":"v_d90bdba84a60b15b016216559348bbcd"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_5bf63d5cbb90057f946668d30d0f50fb","restricted_bridge":false,"source_ref":"s_e2e2559e415bd34a2501f8a9fe9ca407","value":"note:vanilla","version_ref":"v_d90bdba84a60b15b016216559348bbcd"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_63cca4c21f859ad54bb5072d28330a5c","restricted_bridge":false,"source_ref":"s_e2e2559e415bd34a2501f8a9fe9ca407","value":"note:material_32a22e130f7a7a738ca146effbd221a8","version_ref":"v_d90bdba84a60b15b016216559348bbcd"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_714b8272cf2b408039223d878c0e8c77","restricted_bridge":false,"source_ref":"s_e2e2559e415bd34a2501f8a9fe9ca407","value":"note:hazelnut","version_ref":"v_d90bdba84a60b15b016216559348bbcd"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_727f1dbe286a3be78bf76c60aede232f","restricted_bridge":false,"source_ref":"s_e2e2559e415bd34a2501f8a9fe9ca407","value":"note:frankincense","version_ref":"v_d90bdba84a60b15b016216559348bbcd"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_18cb1b56ece88dc1265a490a1c67c8e1","restricted_bridge":false,"source_ref":"s_e2e2559e415bd34a2501f8a9fe9ca407","value":"note:saffron","version_ref":"v_d90bdba84a60b15b016216559348bbcd"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_c573d2f4a67987191c45681274fe87c6","restricted_bridge":false,"source_ref":"s_e2e2559e415bd34a2501f8a9fe9ca407","value":"note:rose","version_ref":"v_d90bdba84a60b15b016216559348bbcd"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_86682ef61625541c481bf538bc19844a","restricted_bridge":false,"source_ref":"s_e2e2559e415bd34a2501f8a9fe9ca407","value":"note:pear","version_ref":"v_d90bdba84a60b15b016216559348bbcd"}],"classification":"taste_only","code":"0114","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"note","channel":"manufacturer_authored_content","layer":"top","polarity":"positive","ref":"e_a02ffa857b1563114027c5224f2232d9","restricted_bridge":false,"source_ref":"s_3776f852ea4ebb15de6e8b6fc927323b","value":"note:oregano","version_ref":"v_589099010ffa449096f9bf9e03cfe7c6"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"base","polarity":"positive","ref":"e_713bd0ed08ee4939b5d5a069355533f9","restricted_bridge":false,"source_ref":"s_3776f852ea4ebb15de6e8b6fc927323b","value":"note:sandalwood","version_ref":"v_589099010ffa449096f9bf9e03cfe7c6"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"heart","polarity":"positive","ref":"e_0e2c63e0f612f334aaa3a0d3723e8065","restricted_bridge":false,"source_ref":"s_3776f852ea4ebb15de6e8b6fc927323b","value":"note:frankincense","version_ref":"v_589099010ffa449096f9bf9e03cfe7c6"}],"classification":"taste_only","code":"0115","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"note","channel":"manufacturer_authored_content","layer":"heart","polarity":"positive","ref":"e_1472ddf807582ee598be8bf31140c7ee","restricted_bridge":false,"source_ref":"s_8425302c4ce6d6301146bf3bceb106b6","value":"note:jasmine","version_ref":"v_29e2e4de74802c03c3006db2e4a55de3"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"base","polarity":"positive","ref":"e_9064032f8533e51c9c3ad2390d151711","restricted_bridge":false,"source_ref":"s_8425302c4ce6d6301146bf3bceb106b6","value":"note:sandalwood","version_ref":"v_29e2e4de74802c03c3006db2e4a55de3"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"top","polarity":"positive","ref":"e_0ce4ebb0030e8d161bb7200ea04a7318","restricted_bridge":false,"source_ref":"s_8425302c4ce6d6301146bf3bceb106b6","value":"note:rosemary","version_ref":"v_29e2e4de74802c03c3006db2e4a55de3"}],"classification":"taste_only","code":"0116","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"manufacturer_authored_content","layer":null,"polarity":"positive","ref":"e_b002de3c1077ffa95395602f30fb0a54","restricted_bridge":false,"source_ref":"s_ed9c6652a85cc9bf6530ea31b67d2fdf","value":"note:plum accord","version_ref":"v_9ab8ecf4f5fbb75720a32f8020fff9b8"},{"attribute":"named_note_or_accord","channel":"manufacturer_authored_content","layer":null,"polarity":"positive","ref":"e_9bbcc0b4648a9d12e256fd1eb1d8b468","restricted_bridge":false,"source_ref":"s_ed9c6652a85cc9bf6530ea31b67d2fdf","value":"note:saffron accord","version_ref":"v_9ab8ecf4f5fbb75720a32f8020fff9b8"},{"attribute":"named_note_or_accord","channel":"manufacturer_authored_content","layer":null,"polarity":"positive","ref":"e_7bd6397b6a4f7c6038936da6fcaf807c","restricted_bridge":false,"source_ref":"s_ed9c6652a85cc9bf6530ea31b67d2fdf","value":"note:black leather accord","version_ref":"v_9ab8ecf4f5fbb75720a32f8020fff9b8"}],"classification":"taste_only","code":"0117","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"note","channel":"manufacturer_authored_content","layer":"top","polarity":"positive","ref":"e_9ab72adbe98cc844e670d68494a9a5dd","restricted_bridge":false,"source_ref":"s_352a478d382756ddf3972e705db7c745","value":"note:pineapple","version_ref":"v_7f53e15a32166b1ca87293d7a7082f42"},{"attribute":"named_note_or_accord","channel":"manufacturer_authored_content","layer":null,"polarity":"positive","ref":"e_be2045e6b7025a1b8deab5cd059281ef","restricted_bridge":false,"source_ref":"s_352a478d382756ddf3972e705db7c745","value":"note:material_048fc2d98e00e7db1706dcc568cefeea","version_ref":"v_7f53e15a32166b1ca87293d7a7082f42"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"base","polarity":"positive","ref":"e_cc0b69fbcd74b40506f991ef4741f4c5","restricted_bridge":false,"source_ref":"s_352a478d382756ddf3972e705db7c745","value":"note:birch","version_ref":"v_7f53e15a32166b1ca87293d7a7082f42"}],"classification":"taste_only","code":"0118","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"note","channel":"manufacturer_authored_content","layer":"top","polarity":"positive","ref":"e_af6e7e3c6c426fce5e16c17bab0e0141","restricted_bridge":false,"source_ref":"s_e2edf118b1c975b788a08c161043e7b7","value":"note:black tea","version_ref":"v_54537e2cedc002906dd0ecc4223d6dd5"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"top","polarity":"positive","ref":"e_5b9de96a9882027e2c0fe1e38d78a364","restricted_bridge":false,"source_ref":"s_e2edf118b1c975b788a08c161043e7b7","value":"note:fig","version_ref":"v_54537e2cedc002906dd0ecc4223d6dd5"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"base","polarity":"positive","ref":"e_396b5ddb988d7f367c99ce6a1a26b556","restricted_bridge":false,"source_ref":"s_e2edf118b1c975b788a08c161043e7b7","value":"note:sandalwood","version_ref":"v_54537e2cedc002906dd0ecc4223d6dd5"}],"classification":"taste_only","code":"0119","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"note","channel":"manufacturer_authored_content","layer":"heart","polarity":"positive","ref":"e_9617de8705d22eed7fc8a97fefba410d","restricted_bridge":false,"source_ref":"s_309224b82d3cbdcb210dae5251fdac7e","value":"note:turkish rose","version_ref":"v_9a15861421340543e02e13bb61fc5a03"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"heart","polarity":"positive","ref":"e_b5b3382680c6389717ff5d350b65f61a","restricted_bridge":false,"source_ref":"s_309224b82d3cbdcb210dae5251fdac7e","value":"note:cumin","version_ref":"v_9a15861421340543e02e13bb61fc5a03"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"unknown","polarity":"positive","ref":"e_1391e1514dd6ecd415472ef137835cb2","restricted_bridge":false,"source_ref":"s_309224b82d3cbdcb210dae5251fdac7e","value":"note:agarwood","version_ref":"v_9a15861421340543e02e13bb61fc5a03"}],"classification":"taste_only","code":"0120","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[],"classification":"attributed_use_only","code":"0121","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"note","channel":"manufacturer_authored_content","layer":"heart","polarity":"positive","ref":"e_e734457b736980bd50eedf763a3ee4d2","restricted_bridge":false,"source_ref":"s_19b234b97a2a28ec20cbd9fa56242a91","value":"note:heliotrope","version_ref":"v_232a651fcbc0533c1173fdb453245969"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"heart","polarity":"positive","ref":"e_35a9fec8a7ce05cbd8bcfe3b8eeaae41","restricted_bridge":false,"source_ref":"s_19b234b97a2a28ec20cbd9fa56242a91","value":"note:black vanilla","version_ref":"v_232a651fcbc0533c1173fdb453245969"},{"attribute":"named_note_or_accord","channel":"manufacturer_authored_content","layer":null,"polarity":"positive","ref":"e_195472fb23d368dbf57a7287746e3796","restricted_bridge":false,"source_ref":"s_19b234b97a2a28ec20cbd9fa56242a91","value":"note:cherry accord","version_ref":"v_232a651fcbc0533c1173fdb453245969"}],"classification":"taste_only","code":"0122","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"manufacturer_authored_content","layer":null,"polarity":"positive","ref":"e_8306f0d88f0ddaeed263b4f558a66b96","restricted_bridge":false,"source_ref":"s_84207de2c1e8e0b7ad224c911255e6eb","value":"note:salted accord","version_ref":"v_5000eb46cf382a6008e5d8cc2f99a294"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"base","polarity":"positive","ref":"e_6154afdc05c4a36e4a6cc5391caa4714","restricted_bridge":false,"source_ref":"s_84207de2c1e8e0b7ad224c911255e6eb","value":"note:white musk","version_ref":"v_5000eb46cf382a6008e5d8cc2f99a294"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"top","polarity":"positive","ref":"e_39f4c75aa8ab137303cd3c9ebe058f70","restricted_bridge":false,"source_ref":"s_84207de2c1e8e0b7ad224c911255e6eb","value":"note:grapefruit","version_ref":"v_5000eb46cf382a6008e5d8cc2f99a294"}],"classification":"taste_only","code":"0123","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"note","channel":"manufacturer_authored_content","layer":"heart","polarity":"positive","ref":"e_20dfc389c8df5d6f9de4ab1f55d8e10c","restricted_bridge":false,"source_ref":"s_fa7f00414d673fdd00db71cef1c6a50f","value":"note:indian tuberose","version_ref":"v_d40b9ce3b5b7fcd5e6b889743541894d"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"heart","polarity":"positive","ref":"e_bdac0fdb163fafe56a6dc27a64e8260b","restricted_bridge":false,"source_ref":"s_fa7f00414d673fdd00db71cef1c6a50f","value":"note:sambac jasmine","version_ref":"v_d40b9ce3b5b7fcd5e6b889743541894d"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"heart","polarity":"positive","ref":"e_8ccf9cc2bf3250dfe6aa2ee724f09f70","restricted_bridge":false,"source_ref":"s_fa7f00414d673fdd00db71cef1c6a50f","value":"note:iris","version_ref":"v_d40b9ce3b5b7fcd5e6b889743541894d"}],"classification":"taste_only","code":"0124","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"note","channel":"manufacturer_authored_content","layer":"base","polarity":"positive","ref":"e_3ba6cee60ff9158a10849adb7969026c","restricted_bridge":false,"source_ref":"s_6432eb5511aa1c7b80121a7d6639edf5","value":"note:vanilla","version_ref":"v_cd9442bb52497a8abfbe2903af66b5de"},{"attribute":"named_note_or_accord","channel":"manufacturer_authored_content","layer":null,"polarity":"positive","ref":"e_8144b4d098afdcdce63c6febcb494a6e","restricted_bridge":false,"source_ref":"s_6432eb5511aa1c7b80121a7d6639edf5","value":"note:leather accord","version_ref":"v_cd9442bb52497a8abfbe2903af66b5de"},{"attribute":"named_note_or_accord","channel":"manufacturer_authored_content","layer":null,"polarity":"positive","ref":"e_2a9e15f8022fc6fa437bac763f10e27e","restricted_bridge":false,"source_ref":"s_6432eb5511aa1c7b80121a7d6639edf5","value":"note:violet accord","version_ref":"v_cd9442bb52497a8abfbe2903af66b5de"}],"classification":"taste_only","code":"0125","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[],"classification":"attributed_use_only","code":"0126","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"note","channel":"manufacturer_authored_content","layer":"top","polarity":"positive","ref":"e_c709f356e3d7e3cd9fa5df5a8c3412b9","restricted_bridge":false,"source_ref":"s_a71929813d311592f5a2e67ed4955f92","value":"note:neroli","version_ref":"v_26e62c36e146ddeee19051ae172e4586"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"heart","polarity":"positive","ref":"e_0b276746544b58c87811c60f227e71f1","restricted_bridge":false,"source_ref":"s_a71929813d311592f5a2e67ed4955f92","value":"note:rose","version_ref":"v_26e62c36e146ddeee19051ae172e4586"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"base","polarity":"positive","ref":"e_8d1682592aece749df35c626a37e103f","restricted_bridge":false,"source_ref":"s_a71929813d311592f5a2e67ed4955f92","value":"note:vanilla","version_ref":"v_26e62c36e146ddeee19051ae172e4586"}],"classification":"taste_only","code":"0127","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_0855d7da77e42afc472679598238f7a9","restricted_bridge":false,"source_ref":"s_36357bb2f2a10d51fac41b25a0ef7d4f","value":"note:cedarwood","version_ref":"v_dcd32bb5a2ef28de10e1efbb126d932e"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_ffc64f1cc8b1249a4ea879b30f7714d8","restricted_bridge":false,"source_ref":"s_36357bb2f2a10d51fac41b25a0ef7d4f","value":"note:vetiver","version_ref":"v_dcd32bb5a2ef28de10e1efbb126d932e"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_5d13d50264dab4664f51aaf92c2f95d5","restricted_bridge":false,"source_ref":"s_36357bb2f2a10d51fac41b25a0ef7d4f","value":"note:violet","version_ref":"v_dcd32bb5a2ef28de10e1efbb126d932e"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_17e463f7ea94eb0227684d4303ef825e","restricted_bridge":false,"source_ref":"s_36357bb2f2a10d51fac41b25a0ef7d4f","value":"note:bergamot","version_ref":"v_dcd32bb5a2ef28de10e1efbb126d932e"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_686f4cec1d9abf2fb7995021e1744a7f","restricted_bridge":false,"source_ref":"s_36357bb2f2a10d51fac41b25a0ef7d4f","value":"note:blackcurrant","version_ref":"v_dcd32bb5a2ef28de10e1efbb126d932e"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_6bc0c8f80a1703110c9d5f871656e463","restricted_bridge":false,"source_ref":"s_36357bb2f2a10d51fac41b25a0ef7d4f","value":"note:african marigold","version_ref":"v_dcd32bb5a2ef28de10e1efbb126d932e"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_e3e646da129df04a92561a99aa6b53b7","restricted_bridge":false,"source_ref":"s_36357bb2f2a10d51fac41b25a0ef7d4f","value":"note:cyclamen","version_ref":"v_dcd32bb5a2ef28de10e1efbb126d932e"}],"classification":"both_documentary_axes","code":"0128","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_9029ada2ef8d135f84f779e77bdb997c","restricted_bridge":false,"source_ref":"s_0f788ae3594351a4bc22d5317349eaab","value":"note:lemon","version_ref":"v_bd470274d76e33e54646b4f01fd994d8"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_6b7810295bed21e63b0452f90dc0a53b","restricted_bridge":false,"source_ref":"s_0f788ae3594351a4bc22d5317349eaab","value":"note:amber","version_ref":"v_bd470274d76e33e54646b4f01fd994d8"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_4154a9d26698f862bbb60b22c88b4b9d","restricted_bridge":false,"source_ref":"s_0f788ae3594351a4bc22d5317349eaab","value":"note:sandalwood","version_ref":"v_bd470274d76e33e54646b4f01fd994d8"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_652c3a6419e91ea7b90650197be2ae24","restricted_bridge":false,"source_ref":"s_0f788ae3594351a4bc22d5317349eaab","value":"note:pine needle","version_ref":"v_bd470274d76e33e54646b4f01fd994d8"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_56299146966fb1dd29d7b7fe93a6f741","restricted_bridge":false,"source_ref":"s_0f788ae3594351a4bc22d5317349eaab","value":"note:vanilla","version_ref":"v_bd470274d76e33e54646b4f01fd994d8"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_71a69d21a80edd39ed8111b7aab056dc","restricted_bridge":false,"source_ref":"s_0f788ae3594351a4bc22d5317349eaab","value":"note:bergamot","version_ref":"v_bd470274d76e33e54646b4f01fd994d8"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_00572f2bc0aff818ae42a4feca15adb1","restricted_bridge":false,"source_ref":"s_0f788ae3594351a4bc22d5317349eaab","value":"note:incense","version_ref":"v_bd470274d76e33e54646b4f01fd994d8"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_42ae2ee31596ffefd0a689c36ea127f8","restricted_bridge":false,"source_ref":"s_0f788ae3594351a4bc22d5317349eaab","value":"note:pepper","version_ref":"v_bd470274d76e33e54646b4f01fd994d8"}],"classification":"taste_only","code":"0129","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_a385f6e235be2deaf9f7f56d06ce655f","restricted_bridge":false,"source_ref":"s_6ee0134e75e140cd88c258651c70d51a","value":"note:cedarwood","version_ref":"v_8034b4b2273c6b701862d17da63c058f"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_ab7f04c6d52fed708fd290c7cb18db6f","restricted_bridge":false,"source_ref":"s_6ee0134e75e140cd88c258651c70d51a","value":"note:vetiver","version_ref":"v_8034b4b2273c6b701862d17da63c058f"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_df09363dfa50fc09c3b3843f6739f705","restricted_bridge":false,"source_ref":"s_6ee0134e75e140cd88c258651c70d51a","value":"note:ambrette","version_ref":"v_8034b4b2273c6b701862d17da63c058f"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_ee641d93bea931d893cc56279dbe106c","restricted_bridge":false,"source_ref":"s_6ee0134e75e140cd88c258651c70d51a","value":"note:magnolia","version_ref":"v_8034b4b2273c6b701862d17da63c058f"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_754086055bdb7302a8eedb7de371d193","restricted_bridge":false,"source_ref":"s_6ee0134e75e140cd88c258651c70d51a","value":"note:naseberry","version_ref":"v_8034b4b2273c6b701862d17da63c058f"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_640e4650851dec3ab7fadd95c6af24a7","restricted_bridge":false,"source_ref":"s_6ee0134e75e140cd88c258651c70d51a","value":"note:sandalwood","version_ref":"v_8034b4b2273c6b701862d17da63c058f"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_371320c26c6878b6f6006e0f8a26290b","restricted_bridge":false,"source_ref":"s_6ee0134e75e140cd88c258651c70d51a","value":"note:violet","version_ref":"v_8034b4b2273c6b701862d17da63c058f"}],"classification":"both_documentary_axes","code":"0130","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_5efa13a1e0f56b16265acec4c04f0462","restricted_bridge":false,"source_ref":"s_e4193ec92602748773fa51b167e91680","value":"note:rose","version_ref":"v_de5368620bdeb0b9c48f1571d72d92db"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_401a4e1ebcd9653f09f7066eb9a0d1c3","restricted_bridge":false,"source_ref":"s_e4193ec92602748773fa51b167e91680","value":"note:vetiver","version_ref":"v_de5368620bdeb0b9c48f1571d72d92db"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_ef702844fe763fb1cc7199c10567dc60","restricted_bridge":false,"source_ref":"s_e4193ec92602748773fa51b167e91680","value":"note:cedarwood","version_ref":"v_de5368620bdeb0b9c48f1571d72d92db"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_b3556ad929b299653840c7438690be2b","restricted_bridge":false,"source_ref":"s_e4193ec92602748773fa51b167e91680","value":"note:musk","version_ref":"v_de5368620bdeb0b9c48f1571d72d92db"}],"classification":"taste_only","code":"0131","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_375a27cf3f2bdbb0be93dc3bb5acb5a3","restricted_bridge":false,"source_ref":"s_515671dd5a278fc3f6b9c1893e939dc7","value":"note:galbanum","version_ref":"v_32b02d06c31430c277749d30cefb9417"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_1026ed5ab3ebe13e4a0944afef6fcc92","restricted_bridge":false,"source_ref":"s_515671dd5a278fc3f6b9c1893e939dc7","value":"note:cedarwood","version_ref":"v_32b02d06c31430c277749d30cefb9417"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_b515f4a5ef794972c4c3357fe88ecee6","restricted_bridge":false,"source_ref":"s_515671dd5a278fc3f6b9c1893e939dc7","value":"note:bergamot","version_ref":"v_32b02d06c31430c277749d30cefb9417"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_6b879fc98e1f8ea0205b3fe475cbbe5a","restricted_bridge":false,"source_ref":"s_515671dd5a278fc3f6b9c1893e939dc7","value":"note:geranium","version_ref":"v_32b02d06c31430c277749d30cefb9417"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_5bb0d73fcb05f0a4508ae3b2b6d47bdf","restricted_bridge":false,"source_ref":"s_515671dd5a278fc3f6b9c1893e939dc7","value":"note:oakmoss","version_ref":"v_32b02d06c31430c277749d30cefb9417"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_4ca1a9bd2fb2a2dad8e6f2a46a771d0c","restricted_bridge":false,"source_ref":"s_515671dd5a278fc3f6b9c1893e939dc7","value":"note:violet","version_ref":"v_32b02d06c31430c277749d30cefb9417"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_6ec0209d133fa93742a06ebc06a45098","restricted_bridge":false,"source_ref":"s_515671dd5a278fc3f6b9c1893e939dc7","value":"note:material_7bf1bf8416fcb4cac26ca297a96e448a","version_ref":"v_32b02d06c31430c277749d30cefb9417"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_f061add3b021b870e82b15b657aa1e0e","restricted_bridge":false,"source_ref":"s_515671dd5a278fc3f6b9c1893e939dc7","value":"note:verbena","version_ref":"v_32b02d06c31430c277749d30cefb9417"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_ed3d0eca5c32fb1f79ee0297b9a9a813","restricted_bridge":false,"source_ref":"s_515671dd5a278fc3f6b9c1893e939dc7","value":"note:sandalwood","version_ref":"v_32b02d06c31430c277749d30cefb9417"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_2d86bfc8d0184e98045d3696f8c42d16","restricted_bridge":false,"source_ref":"s_515671dd5a278fc3f6b9c1893e939dc7","value":"note:lavender","version_ref":"v_32b02d06c31430c277749d30cefb9417"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_294eab03e93370b9c394c90f8b8c0d44","restricted_bridge":false,"source_ref":"s_515671dd5a278fc3f6b9c1893e939dc7","value":"note:lemon","version_ref":"v_32b02d06c31430c277749d30cefb9417"},{"attribute":"context","channel":"manufacturer_authored_content","layer":null,"polarity":"positive","ref":"e_1df26e34fc2d3def565e3e516f31868f","restricted_bridge":false,"source_ref":"s_1cd8fbc8d4084dc669f82eb72ca13b5c","value":"use:wedding_groom_confidence","version_ref":"v_4f46ba14d309a2f5d9f685f516d2e8ed"}],"classification":"both_documentary_axes","code":"0132","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"context","channel":"manufacturer_authored_content","layer":null,"polarity":"positive","ref":"e_916fbb3538071372d20ae118f71e10d7","restricted_bridge":false,"source_ref":"s_a5712fd9fc7f50adf6381fb7e0701ffc","value":"use:wedding_groom","version_ref":"v_d6d8df181be1157918c72984ad5d2c18"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"base","polarity":"positive","ref":"e_421ada9f6c4a58b8940194720a759bbb","restricted_bridge":false,"source_ref":"s_fbb4557123bb199f23485443cc850717","value":"note:benzoin","version_ref":"v_218b73890d36168ca41f0d506320cdc1"},{"attribute":"named_note_or_accord","channel":"manufacturer_authored_content","layer":null,"polarity":"positive","ref":"e_3ba39fd4eb937603a1897c8ec7a7a1f9","restricted_bridge":false,"source_ref":"s_fbb4557123bb199f23485443cc850717","value":"note:incense accord","version_ref":"v_218b73890d36168ca41f0d506320cdc1"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"heart","polarity":"positive","ref":"e_d359eb56065acdad38788cee18894bbc","restricted_bridge":false,"source_ref":"s_fbb4557123bb199f23485443cc850717","value":"note:angelica","version_ref":"v_218b73890d36168ca41f0d506320cdc1"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"heart","polarity":"positive","ref":"e_d0e99d1b6ef3594b516c3541194aaf55","restricted_bridge":false,"source_ref":"s_fbb4557123bb199f23485443cc850717","value":"note:geranium","version_ref":"v_218b73890d36168ca41f0d506320cdc1"}],"classification":"both_documentary_axes","code":"0133","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_e2c613edf86de11ce9b9be9c15ed1910","restricted_bridge":false,"source_ref":"s_f611e062873dc68083c1782e7c3cc9a2","value":"note:elemi","version_ref":"v_2cc76f1d92eabcf5813f5080300ffbbe"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_c0b4c8bee9668697ae5f9e0a8071ec9a","restricted_bridge":false,"source_ref":"s_f611e062873dc68083c1782e7c3cc9a2","value":"note:pink pepper","version_ref":"v_2cc76f1d92eabcf5813f5080300ffbbe"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_840488bebdff73d60eb007ad6eecb8fd","restricted_bridge":false,"source_ref":"s_f611e062873dc68083c1782e7c3cc9a2","value":"note:frankincense","version_ref":"v_2cc76f1d92eabcf5813f5080300ffbbe"}],"classification":"taste_only","code":"0134","concentration":"EDT","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_00b4a0693174ef81dfa85ebfbe46e509","restricted_bridge":false,"source_ref":"s_7c823fd481c41dc1d5a5ebc4df1e4bc8","value":"note:basil","version_ref":"v_bfc19a9733e105a43d454618208e4cde"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_83773aee50bb7920ad93b2741545bbf2","restricted_bridge":false,"source_ref":"s_7c823fd481c41dc1d5a5ebc4df1e4bc8","value":"note:rosemary","version_ref":"v_bfc19a9733e105a43d454618208e4cde"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_63cdeedc1f595587346538d4b328f318","restricted_bridge":false,"source_ref":"s_7c823fd481c41dc1d5a5ebc4df1e4bc8","value":"note:petitgrain","version_ref":"v_bfc19a9733e105a43d454618208e4cde"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_1bbc34147833a6f250002589a5fbe32a","restricted_bridge":false,"source_ref":"s_7c823fd481c41dc1d5a5ebc4df1e4bc8","value":"note:lemon","version_ref":"v_bfc19a9733e105a43d454618208e4cde"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_b68f7055b66e5cdbe6ac4f74400b07fb","restricted_bridge":false,"source_ref":"s_7c823fd481c41dc1d5a5ebc4df1e4bc8","value":"note:vetiver","version_ref":"v_bfc19a9733e105a43d454618208e4cde"}],"classification":"taste_only","code":"0135","concentration":"EDT","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_e52263c52a64389673974c077a32dc6d","restricted_bridge":false,"source_ref":"s_d104ffa5dcdcb748f538423d47e16453","value":"note:leather","version_ref":"v_91413182719321b847d7cbe76a15e889"}],"classification":"taste_only","code":"0136","concentration":"EDT","same_source_manufacturer_dual":false},
{"claims":[],"classification":"attributed_use_only","code":"0137","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"note","channel":"manufacturer_authored_content","layer":"unknown","polarity":"positive","ref":"e_b7bc005a627247355243aa0685ee98cc","restricted_bridge":false,"source_ref":"s_49d8f20522de43573dd6fbe11900c2fa","value":"note:mandarin","version_ref":"v_3383292b54837eba317f8c6751f3e19a"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"unknown","polarity":"positive","ref":"e_67588c1b0eb28c39d331ce374fd5b535","restricted_bridge":false,"source_ref":"s_49d8f20522de43573dd6fbe11900c2fa","value":"note:rosemary","version_ref":"v_3383292b54837eba317f8c6751f3e19a"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"unknown","polarity":"positive","ref":"e_0c7a6e74e1e511d1e038eddca7c62e10","restricted_bridge":false,"source_ref":"s_49d8f20522de43573dd6fbe11900c2fa","value":"note:tonka bean","version_ref":"v_3383292b54837eba317f8c6751f3e19a"}],"classification":"taste_only","code":"0138","concentration":"EDT","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_ba0be2cda13a57fc5b8a1a09b504f891","restricted_bridge":false,"source_ref":"s_448a3f5fad482c817fdce9c7e0bc4586","value":"note:saffron","version_ref":"v_b3cfc974d5453a332ed3143b02683d11"}],"classification":"taste_only","code":"0139","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_d8e52fbbdb862f07ec1484cb99e263c2","restricted_bridge":false,"source_ref":"s_ca84109d2bd983e060c9c16a0df1d212","value":"note:coriander","version_ref":"v_1a6829d6f67c8366e2a095d3e5d7646b"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_72d6a11a386fb13bf1b31b3b00de61e2","restricted_bridge":false,"source_ref":"s_ca84109d2bd983e060c9c16a0df1d212","value":"note:musk","version_ref":"v_1a6829d6f67c8366e2a095d3e5d7646b"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_7b1f7604d7b041b1187b384201130300","restricted_bridge":false,"source_ref":"s_ca84109d2bd983e060c9c16a0df1d212","value":"note:nutmeg","version_ref":"v_1a6829d6f67c8366e2a095d3e5d7646b"}],"classification":"taste_only","code":"0140","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_99e8ccb287483aeabfe9f7840b1ce770","restricted_bridge":false,"source_ref":"s_5e684bd10b62961daedbea20fb1acbef","value":"note:musk","version_ref":"v_efbb32101ee98eaa9abd04d2d54457fd"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_de4cadd4ce62505b61a0c9a81d682bdf","restricted_bridge":false,"source_ref":"s_5e684bd10b62961daedbea20fb1acbef","value":"note:coriander","version_ref":"v_efbb32101ee98eaa9abd04d2d54457fd"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_d9d7e58e2c3110aa4f02c352f3a4c20c","restricted_bridge":false,"source_ref":"s_5e684bd10b62961daedbea20fb1acbef","value":"note:vanilla","version_ref":"v_efbb32101ee98eaa9abd04d2d54457fd"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_84e1a682a13d985ff75cc5dcffe47b66","restricted_bridge":false,"source_ref":"s_5e684bd10b62961daedbea20fb1acbef","value":"note:nutmeg","version_ref":"v_efbb32101ee98eaa9abd04d2d54457fd"}],"classification":"both_documentary_axes","code":"0141","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_62320e75f8bdd96c716d4bfe4ad87b10","restricted_bridge":false,"source_ref":"s_81f10a8896c60b9f4133dc0f2fd28389","value":"note:labdanum","version_ref":"v_86b8920fd2e15aca9a0087df0e6657c5"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_794a0ae263e9091661595b8b1263b1a0","restricted_bridge":false,"source_ref":"s_81f10a8896c60b9f4133dc0f2fd28389","value":"note:amber","version_ref":"v_86b8920fd2e15aca9a0087df0e6657c5"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_270a96701be7bbd8f59000d5ba1a7d1e","restricted_bridge":false,"source_ref":"s_81f10a8896c60b9f4133dc0f2fd28389","value":"note:benzoin","version_ref":"v_86b8920fd2e15aca9a0087df0e6657c5"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_23f12ce4bed45ca2d0ef50a6527223b7","restricted_bridge":false,"source_ref":"s_81f10a8896c60b9f4133dc0f2fd28389","value":"note:vanilla","version_ref":"v_86b8920fd2e15aca9a0087df0e6657c5"}],"classification":"both_documentary_axes","code":"0142","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_e0e183a26689a973138265ca7d5261e2","restricted_bridge":false,"source_ref":"s_d09da8761cf1c8483ed7b42fc0bd0a69","value":"note:oud","version_ref":"v_45fe7c79ab78d685c029a1256bd83637"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_8149bfd55a580ecb1eafcd2e156ff071","restricted_bridge":false,"source_ref":"s_d09da8761cf1c8483ed7b42fc0bd0a69","value":"note:amber","version_ref":"v_45fe7c79ab78d685c029a1256bd83637"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_b9798e78b2af428fcda952f6f106b9c3","restricted_bridge":false,"source_ref":"s_d09da8761cf1c8483ed7b42fc0bd0a69","value":"note:benzoin","version_ref":"v_45fe7c79ab78d685c029a1256bd83637"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_f76b2249c192a9f9d73422e2364ffb32","restricted_bridge":false,"source_ref":"s_d09da8761cf1c8483ed7b42fc0bd0a69","value":"note:violet","version_ref":"v_45fe7c79ab78d685c029a1256bd83637"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_4b3ba2be82258eca52161da1cfbf8d8b","restricted_bridge":false,"source_ref":"s_d09da8761cf1c8483ed7b42fc0bd0a69","value":"note:rose","version_ref":"v_45fe7c79ab78d685c029a1256bd83637"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_49a92835b6853334648ffa083f178c85","restricted_bridge":false,"source_ref":"s_d09da8761cf1c8483ed7b42fc0bd0a69","value":"note:vanilla","version_ref":"v_45fe7c79ab78d685c029a1256bd83637"}],"classification":"taste_only","code":"0143","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[],"classification":"attributed_use_only","code":"0144","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_5cbac4dc7fa7377507ac8674d2c4a368","restricted_bridge":false,"source_ref":"s_c3f8513cfbfa9b96befd9f617431232d","value":"note:nutmeg","version_ref":"v_2cc0ece7320265005aa8e23d10f5aefd"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_30342ff97b1f0861835ea5b687424125","restricted_bridge":false,"source_ref":"s_c3f8513cfbfa9b96befd9f617431232d","value":"note:saffron","version_ref":"v_2cc0ece7320265005aa8e23d10f5aefd"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_831ab1bb37824d83b7878f4e95b6b151","restricted_bridge":false,"source_ref":"s_c3f8513cfbfa9b96befd9f617431232d","value":"note:rose","version_ref":"v_2cc0ece7320265005aa8e23d10f5aefd"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_ec91ece45d557133c8acc549335ef243","restricted_bridge":false,"source_ref":"s_c3f8513cfbfa9b96befd9f617431232d","value":"note:osmanthus","version_ref":"v_2cc0ece7320265005aa8e23d10f5aefd"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_62e97551d30a93e5ad17f5d7028a7a6d","restricted_bridge":false,"source_ref":"s_c3f8513cfbfa9b96befd9f617431232d","value":"note:tonka bean","version_ref":"v_2cc0ece7320265005aa8e23d10f5aefd"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_b8d07bb6727eec5095eb9e659184dad6","restricted_bridge":false,"source_ref":"s_c3f8513cfbfa9b96befd9f617431232d","value":"note:patchouli","version_ref":"v_2cc0ece7320265005aa8e23d10f5aefd"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_17d1f29ec3dc5f8098722af7b9a13ce2","restricted_bridge":false,"source_ref":"s_c3f8513cfbfa9b96befd9f617431232d","value":"note:vanilla","version_ref":"v_2cc0ece7320265005aa8e23d10f5aefd"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_cba52be63f1ac302b887174554c5f0b6","restricted_bridge":false,"source_ref":"s_c3f8513cfbfa9b96befd9f617431232d","value":"note:davana","version_ref":"v_2cc0ece7320265005aa8e23d10f5aefd"}],"classification":"taste_only","code":"0145","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"note","channel":"manufacturer_authored_content","layer":"top","polarity":"positive","ref":"e_5cac4f91a53e6e7bad81fdd1c99a0332","restricted_bridge":false,"source_ref":"s_4aa8ca95ce7415db27ee2e6097d84386","value":"note:pear","version_ref":"v_c2dc55a0ab5f11b2afb1d81a3c641f99"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"heart","polarity":"positive","ref":"e_bfd02d28743d62bb7990a2fb19144d34","restricted_bridge":false,"source_ref":"s_4aa8ca95ce7415db27ee2e6097d84386","value":"note:damascena rose","version_ref":"v_c2dc55a0ab5f11b2afb1d81a3c641f99"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"base","polarity":"positive","ref":"e_1ea195871c39db456d8f303071712052","restricted_bridge":false,"source_ref":"s_4aa8ca95ce7415db27ee2e6097d84386","value":"note:vanilla","version_ref":"v_c2dc55a0ab5f11b2afb1d81a3c641f99"}],"classification":"taste_only","code":"0146","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_6c28e2fba0133719dc60299b1d958abc","restricted_bridge":false,"source_ref":"s_0c4e5ff677efc87062555e0305861245","value":"note:cardamom","version_ref":"v_925f5007fdf37579f2f7820b5d036a0a"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_7b8e4d71d6d737a29d71cb2b2224859c","restricted_bridge":false,"source_ref":"s_0c4e5ff677efc87062555e0305861245","value":"note:pepper","version_ref":"v_925f5007fdf37579f2f7820b5d036a0a"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_8c2a9d95706e79a6ba13dcb0bbe3a7f1","restricted_bridge":false,"source_ref":"s_0c4e5ff677efc87062555e0305861245","value":"note:cypriol","version_ref":"v_925f5007fdf37579f2f7820b5d036a0a"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_49bd25eb70437844cda5437a59add952","restricted_bridge":false,"source_ref":"s_0c4e5ff677efc87062555e0305861245","value":"note:musk","version_ref":"v_925f5007fdf37579f2f7820b5d036a0a"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_2f9b16c50e0d21ccc2965ac5fefe6e45","restricted_bridge":false,"source_ref":"s_0c4e5ff677efc87062555e0305861245","value":"note:lemon","version_ref":"v_925f5007fdf37579f2f7820b5d036a0a"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_49ca169b37a98cb79587069f8b1516f2","restricted_bridge":false,"source_ref":"s_0c4e5ff677efc87062555e0305861245","value":"note:iris","version_ref":"v_925f5007fdf37579f2f7820b5d036a0a"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_96604c5d0107b2e9ac51de8cfbc167a5","restricted_bridge":false,"source_ref":"s_0c4e5ff677efc87062555e0305861245","value":"note:elemi","version_ref":"v_925f5007fdf37579f2f7820b5d036a0a"}],"classification":"taste_only","code":"0147","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_891cc691d57e65814297222cfa0ec9cd","restricted_bridge":false,"source_ref":"s_ec1b872b2913de5c1e3d506756576195","value":"note:rose","version_ref":"v_307cd84235902f5ada8d3415fd9382a1"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_5da86067d9c8801d5fa96680e844ea4a","restricted_bridge":false,"source_ref":"s_ec1b872b2913de5c1e3d506756576195","value":"note:raspberry","version_ref":"v_307cd84235902f5ada8d3415fd9382a1"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_1cef34425ce102c21c419d675ce92d93","restricted_bridge":false,"source_ref":"s_ec1b872b2913de5c1e3d506756576195","value":"note:thyme","version_ref":"v_307cd84235902f5ada8d3415fd9382a1"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_afde681057f4bd43c553244c26fbaf5b","restricted_bridge":false,"source_ref":"s_ec1b872b2913de5c1e3d506756576195","value":"note:leather","version_ref":"v_307cd84235902f5ada8d3415fd9382a1"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_2d5a3f1f87aefb6095d8ee75d5c8e232","restricted_bridge":false,"source_ref":"s_ec1b872b2913de5c1e3d506756576195","value":"note:iris","version_ref":"v_307cd84235902f5ada8d3415fd9382a1"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_ca37c76d33c7f94f529faf49f1629b58","restricted_bridge":false,"source_ref":"s_ec1b872b2913de5c1e3d506756576195","value":"note:jasmine","version_ref":"v_307cd84235902f5ada8d3415fd9382a1"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_a7f8242ed8a96643fc82d0ec716bf26a","restricted_bridge":false,"source_ref":"s_ec1b872b2913de5c1e3d506756576195","value":"note:saffron","version_ref":"v_307cd84235902f5ada8d3415fd9382a1"}],"classification":"taste_only","code":"0148","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_c2cb9709b07b80d6f2e6921430c777d1","restricted_bridge":false,"source_ref":"s_9b70bd117806d84e4b4a636c3668c1b7","value":"note:mandarin","version_ref":"v_2ede1089884e18e4b87f4c95c68323ff"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_18a26608cc6e708127b12b783e36225b","restricted_bridge":false,"source_ref":"s_9b70bd117806d84e4b4a636c3668c1b7","value":"note:cedarwood","version_ref":"v_2ede1089884e18e4b87f4c95c68323ff"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_20c7e2f43a075b0564d5d19c2eaed3fa","restricted_bridge":false,"source_ref":"s_9b70bd117806d84e4b4a636c3668c1b7","value":"note:amberwood","version_ref":"v_2ede1089884e18e4b87f4c95c68323ff"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_c0c8294495c71fe6c50425c1e0f404b2","restricted_bridge":false,"source_ref":"s_9b70bd117806d84e4b4a636c3668c1b7","value":"note:petitgrain","version_ref":"v_2ede1089884e18e4b87f4c95c68323ff"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_2b4f2fc3e9c19851916705d17a932031","restricted_bridge":false,"source_ref":"s_9b70bd117806d84e4b4a636c3668c1b7","value":"note:bergamot","version_ref":"v_2ede1089884e18e4b87f4c95c68323ff"}],"classification":"taste_only","code":"0149","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_2aa79bc908dc21738333a8d3aeee42b5","restricted_bridge":false,"source_ref":"s_851808e523b51f41ce8a1e3dd4efcfdb","value":"note:bergamot","version_ref":"v_24a94694e96c2a8804e6c7fbb365b7f3"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_447e6f8c72c577352c014178de32ce78","restricted_bridge":false,"source_ref":"s_851808e523b51f41ce8a1e3dd4efcfdb","value":"note:saffron","version_ref":"v_24a94694e96c2a8804e6c7fbb365b7f3"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_6cc8c16b83114ec7833dde61cc707491","restricted_bridge":false,"source_ref":"s_851808e523b51f41ce8a1e3dd4efcfdb","value":"note:oud","version_ref":"v_24a94694e96c2a8804e6c7fbb365b7f3"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_332b33ed40956ed6dc8640f14ee8e7a0","restricted_bridge":false,"source_ref":"s_851808e523b51f41ce8a1e3dd4efcfdb","value":"note:clary sage","version_ref":"v_24a94694e96c2a8804e6c7fbb365b7f3"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_b73852a1968d01152fff5cdf34e59452","restricted_bridge":false,"source_ref":"s_851808e523b51f41ce8a1e3dd4efcfdb","value":"note:vetiver","version_ref":"v_24a94694e96c2a8804e6c7fbb365b7f3"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_59bfaece9206210949a8f6d454bd3076","restricted_bridge":false,"source_ref":"s_851808e523b51f41ce8a1e3dd4efcfdb","value":"note:leather","version_ref":"v_24a94694e96c2a8804e6c7fbb365b7f3"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_3dea6052528f5320a0d9217116fa1b7d","restricted_bridge":false,"source_ref":"s_851808e523b51f41ce8a1e3dd4efcfdb","value":"note:patchouli","version_ref":"v_24a94694e96c2a8804e6c7fbb365b7f3"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_1348108c175c7658ca308ef5dffd7643","restricted_bridge":false,"source_ref":"s_851808e523b51f41ce8a1e3dd4efcfdb","value":"note:praline","version_ref":"v_24a94694e96c2a8804e6c7fbb365b7f3"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_8106dc071052c15f55d10b26733c0341","restricted_bridge":false,"source_ref":"s_851808e523b51f41ce8a1e3dd4efcfdb","value":"note:lavender","version_ref":"v_24a94694e96c2a8804e6c7fbb365b7f3"}],"classification":"both_documentary_axes","code":"0150","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_32a2d27ae9b349392a7c64a3f849da03","restricted_bridge":false,"source_ref":"s_65b51d9129d75ab6ceff8c63919ca4b4","value":"note:vanilla","version_ref":"v_4bfd9c71538103db26b093175994d8de"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_ea568a7026c5f1e6d81083fbf120e300","restricted_bridge":false,"source_ref":"s_65b51d9129d75ab6ceff8c63919ca4b4","value":"note:osmanthus","version_ref":"v_4bfd9c71538103db26b093175994d8de"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_e6f79947f6cf98640938e649ae1830a9","restricted_bridge":false,"source_ref":"s_65b51d9129d75ab6ceff8c63919ca4b4","value":"note:incense","version_ref":"v_4bfd9c71538103db26b093175994d8de"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_c311ecc8a8fe08f067d1a66c6a8908ff","restricted_bridge":false,"source_ref":"s_65b51d9129d75ab6ceff8c63919ca4b4","value":"note:musk","version_ref":"v_4bfd9c71538103db26b093175994d8de"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_d5b4bc71f4a1c5fb99808dc7bd98c725","restricted_bridge":false,"source_ref":"s_65b51d9129d75ab6ceff8c63919ca4b4","value":"note:pepper","version_ref":"v_4bfd9c71538103db26b093175994d8de"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_ab45dd36bf4beed259e8f45bd84b5c8d","restricted_bridge":false,"source_ref":"s_65b51d9129d75ab6ceff8c63919ca4b4","value":"note:cinnamon","version_ref":"v_4bfd9c71538103db26b093175994d8de"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_7a0ed8c934cdf2c1c3effc847f8329c4","restricted_bridge":false,"source_ref":"s_65b51d9129d75ab6ceff8c63919ca4b4","value":"note:cedarwood","version_ref":"v_4bfd9c71538103db26b093175994d8de"}],"classification":"both_documentary_axes","code":"0151","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_70feab56f86df7571032080e4023237c","restricted_bridge":false,"source_ref":"s_87f78b746cc45f9e68f8e67cfb15d4b1","value":"note:lavender","version_ref":"v_32b3278ff787070865dccc2c157db72d"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_6554481d1db4dd39965988372ede019c","restricted_bridge":false,"source_ref":"s_87f78b746cc45f9e68f8e67cfb15d4b1","value":"note:cedarwood","version_ref":"v_32b3278ff787070865dccc2c157db72d"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_93eac1af2e7abb68e4b96f3431a92093","restricted_bridge":false,"source_ref":"s_87f78b746cc45f9e68f8e67cfb15d4b1","value":"note:tonka bean","version_ref":"v_32b3278ff787070865dccc2c157db72d"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_7ef0750552eb1d177e9b37655ab2992c","restricted_bridge":false,"source_ref":"s_87f78b746cc45f9e68f8e67cfb15d4b1","value":"note:blood orange","version_ref":"v_32b3278ff787070865dccc2c157db72d"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_40117f5ac3558baeba86e93dea45d1ad","restricted_bridge":false,"source_ref":"s_87f78b746cc45f9e68f8e67cfb15d4b1","value":"note:orange blossom","version_ref":"v_32b3278ff787070865dccc2c157db72d"}],"classification":"taste_only","code":"0152","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_1ab6e3e04d6cef142432e6e0473b7e29","restricted_bridge":false,"source_ref":"s_200663ef14d7268a75eb11d83c5bb3cd","value":"note:lavender","version_ref":"v_7e5928faab2f0c5c5f3b8de37f80b54d"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_3da0cce934ed446f5aad7a03752d8a27","restricted_bridge":false,"source_ref":"s_200663ef14d7268a75eb11d83c5bb3cd","value":"note:praline","version_ref":"v_7e5928faab2f0c5c5f3b8de37f80b54d"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_c01582f88580a118d7f883aabb6f3054","restricted_bridge":false,"source_ref":"s_200663ef14d7268a75eb11d83c5bb3cd","value":"note:vanilla","version_ref":"v_7e5928faab2f0c5c5f3b8de37f80b54d"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_26a9e75faed0b3f410b7f000eb288f78","restricted_bridge":false,"source_ref":"s_200663ef14d7268a75eb11d83c5bb3cd","value":"note:violet","version_ref":"v_7e5928faab2f0c5c5f3b8de37f80b54d"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_173f3fe253c18a6ca94da965bc128a7b","restricted_bridge":false,"source_ref":"s_200663ef14d7268a75eb11d83c5bb3cd","value":"note:geranium","version_ref":"v_7e5928faab2f0c5c5f3b8de37f80b54d"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_64023393b4e2aa1891a8377509aa5adb","restricted_bridge":false,"source_ref":"s_200663ef14d7268a75eb11d83c5bb3cd","value":"note:patchouli","version_ref":"v_7e5928faab2f0c5c5f3b8de37f80b54d"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_a5eb389325b83e19c0f6d0239d45700f","restricted_bridge":false,"source_ref":"s_200663ef14d7268a75eb11d83c5bb3cd","value":"note:apple","version_ref":"v_7e5928faab2f0c5c5f3b8de37f80b54d"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_8dbdc090bc0dafc7a5bbe1115233b98a","restricted_bridge":false,"source_ref":"s_200663ef14d7268a75eb11d83c5bb3cd","value":"note:cardamom","version_ref":"v_7e5928faab2f0c5c5f3b8de37f80b54d"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_0e7d844ab516c0e43b3394708e7bb79c","restricted_bridge":false,"source_ref":"s_200663ef14d7268a75eb11d83c5bb3cd","value":"note:bergamot","version_ref":"v_7e5928faab2f0c5c5f3b8de37f80b54d"}],"classification":"taste_only","code":"0153","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"note","channel":"manufacturer_authored_content","layer":"base","polarity":"positive","ref":"e_7e69bcc1016bedb79cab18fd233f692c","restricted_bridge":false,"source_ref":"s_64b0e38e16841ea120ea90f7bf76ca6f","value":"note:sandalwood","version_ref":"v_05e459e4e83a265f36e2e8ac700973b8"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"top","polarity":"positive","ref":"e_9f045a34d04810c554a297978446f2a1","restricted_bridge":false,"source_ref":"s_64b0e38e16841ea120ea90f7bf76ca6f","value":"note:cardamom","version_ref":"v_05e459e4e83a265f36e2e8ac700973b8"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"base","polarity":"positive","ref":"e_e0163e47e9d20b6858aec07a07e314f4","restricted_bridge":false,"source_ref":"s_64b0e38e16841ea120ea90f7bf76ca6f","value":"note:oud","version_ref":"v_05e459e4e83a265f36e2e8ac700973b8"}],"classification":"taste_only","code":"0154","concentration":"Parfum","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_5c703153473785f6af7e04857d4cc288","restricted_bridge":false,"source_ref":"s_6e890980a9fc2578357bd424a4a0981f","value":"note:osmanthus","version_ref":"v_c4b786cdaeba745b7e913a01900d5b84"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_061d9ffda17e2777aa8ea7540051e3e5","restricted_bridge":false,"source_ref":"s_6e890980a9fc2578357bd424a4a0981f","value":"note:labdanum","version_ref":"v_c4b786cdaeba745b7e913a01900d5b84"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_59d5ef336f773a4ffdd7faf2cf0afe5e","restricted_bridge":false,"source_ref":"s_6e890980a9fc2578357bd424a4a0981f","value":"note:amber","version_ref":"v_c4b786cdaeba745b7e913a01900d5b84"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_927a99fc12bb5acfe5d2c603b68c091e","restricted_bridge":false,"source_ref":"s_6e890980a9fc2578357bd424a4a0981f","value":"note:patchouli","version_ref":"v_c4b786cdaeba745b7e913a01900d5b84"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_998bfafa7b20c3058e6fa9ad3236655a","restricted_bridge":false,"source_ref":"s_6e890980a9fc2578357bd424a4a0981f","value":"note:honey","version_ref":"v_c4b786cdaeba745b7e913a01900d5b84"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_62997489067692cf924b32a740c8e5dc","restricted_bridge":false,"source_ref":"s_6e890980a9fc2578357bd424a4a0981f","value":"note:benzoin","version_ref":"v_c4b786cdaeba745b7e913a01900d5b84"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_78bb41a3d7109cea0f9bc44354de81bf","restricted_bridge":false,"source_ref":"s_6e890980a9fc2578357bd424a4a0981f","value":"note:tonka bean","version_ref":"v_c4b786cdaeba745b7e913a01900d5b84"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_7856ad6fcb100d58429576d8e3662aee","restricted_bridge":false,"source_ref":"s_6e890980a9fc2578357bd424a4a0981f","value":"note:vanilla","version_ref":"v_c4b786cdaeba745b7e913a01900d5b84"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_1f610b5aa7904d07e918660b1adc54d9","restricted_bridge":false,"source_ref":"s_6e890980a9fc2578357bd424a4a0981f","value":"note:cinnamon","version_ref":"v_c4b786cdaeba745b7e913a01900d5b84"}],"classification":"taste_only","code":"0155","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_23cecfc55fa92cd82049adac898333e7","restricted_bridge":false,"source_ref":"s_9361ca02ba689c1a63408c4c778bd4a5","value":"note:mandarin","version_ref":"v_336eb182bdfc48c949277a17b84bf311"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_78b48c90d18694bdb1389bc81d3dbf8e","restricted_bridge":false,"source_ref":"s_9361ca02ba689c1a63408c4c778bd4a5","value":"note:lemon","version_ref":"v_336eb182bdfc48c949277a17b84bf311"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_b5ee41c3b791ab09572ee7daf14b25cb","restricted_bridge":false,"source_ref":"s_9361ca02ba689c1a63408c4c778bd4a5","value":"note:orange blossom","version_ref":"v_336eb182bdfc48c949277a17b84bf311"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_b39fe271d08e1b7f55a3ce21ee8f9d67","restricted_bridge":false,"source_ref":"s_9361ca02ba689c1a63408c4c778bd4a5","value":"note:jasmine","version_ref":"v_336eb182bdfc48c949277a17b84bf311"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_a67ed63b006261e2271a0e820f3f68b6","restricted_bridge":false,"source_ref":"s_9361ca02ba689c1a63408c4c778bd4a5","value":"note:marshmallow","version_ref":"v_336eb182bdfc48c949277a17b84bf311"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_449b7e2a1ba50147177cf75fcf39fb8d","restricted_bridge":false,"source_ref":"s_9361ca02ba689c1a63408c4c778bd4a5","value":"note:chantilly","version_ref":"v_336eb182bdfc48c949277a17b84bf311"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_1fa197d9634b0c6148a54e9722e39134","restricted_bridge":false,"source_ref":"s_9361ca02ba689c1a63408c4c778bd4a5","value":"note:praline","version_ref":"v_336eb182bdfc48c949277a17b84bf311"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_3303ed82b1bb4e661af4b39a6214c424","restricted_bridge":false,"source_ref":"s_9361ca02ba689c1a63408c4c778bd4a5","value":"note:grapefruit","version_ref":"v_336eb182bdfc48c949277a17b84bf311"}],"classification":"taste_only","code":"0156","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_4a475bd4093a1d24b7f3694e74e948cf","restricted_bridge":false,"source_ref":"s_1c3d6d532aaee1e0ef85d3b97d78cc7e","value":"note:orange blossom","version_ref":"v_5e2190b5cbf04dc1b2a21f85c196e65e"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_3381a98807de2bd33b8d8843f291d29f","restricted_bridge":false,"source_ref":"s_1c3d6d532aaee1e0ef85d3b97d78cc7e","value":"note:bergamot","version_ref":"v_5e2190b5cbf04dc1b2a21f85c196e65e"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_028f4483d7cff5e5998e03111d4ccdac","restricted_bridge":false,"source_ref":"s_1c3d6d532aaee1e0ef85d3b97d78cc7e","value":"note:sandalwood","version_ref":"v_5e2190b5cbf04dc1b2a21f85c196e65e"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_4336d43d258530a1e9090190578e20af","restricted_bridge":false,"source_ref":"s_1c3d6d532aaee1e0ef85d3b97d78cc7e","value":"note:cypress","version_ref":"v_5e2190b5cbf04dc1b2a21f85c196e65e"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_f63a92d8867715e1e904ff9ac3c6b58b","restricted_bridge":false,"source_ref":"s_1c3d6d532aaee1e0ef85d3b97d78cc7e","value":"note:almond","version_ref":"v_5e2190b5cbf04dc1b2a21f85c196e65e"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_887830eb27a0ce0e888cf7e76a652491","restricted_bridge":false,"source_ref":"s_1c3d6d532aaee1e0ef85d3b97d78cc7e","value":"note:anise","version_ref":"v_5e2190b5cbf04dc1b2a21f85c196e65e"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_394a3a1d23c6e669b303070f7d535690","restricted_bridge":false,"source_ref":"s_1c3d6d532aaee1e0ef85d3b97d78cc7e","value":"note:vanilla","version_ref":"v_5e2190b5cbf04dc1b2a21f85c196e65e"}],"classification":"taste_only","code":"0157","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"note","channel":"manufacturer_authored_content","layer":"heart","polarity":"positive","ref":"e_a5eef4197101c55366970a5f8cd6157e","restricted_bridge":false,"source_ref":"s_38da344e7125c9e841a966091e8b1d0b","value":"note:orange blossom","version_ref":"v_92c399e49cfd87a910f4375eebe3be8c"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"base","polarity":"positive","ref":"e_edbb48e044499cf3b9b3769cb18c52b1","restricted_bridge":false,"source_ref":"s_38da344e7125c9e841a966091e8b1d0b","value":"note:vanilla","version_ref":"v_92c399e49cfd87a910f4375eebe3be8c"},{"attribute":"note","channel":"manufacturer_authored_content","layer":"top","polarity":"positive","ref":"e_8d5512c8c6419d5b25b4ea834e17ecec","restricted_bridge":false,"source_ref":"s_38da344e7125c9e841a966091e8b1d0b","value":"note:almond","version_ref":"v_92c399e49cfd87a910f4375eebe3be8c"}],"classification":"taste_only","code":"0158","concentration":"Parfum","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_5ea7aaccb3fb2bf8b080d2ebced93730","restricted_bridge":false,"source_ref":"s_c1643e14b2f449ad3aa7ec7a790fe48f","value":"note:iris","version_ref":"v_160f99b28e9f0b2213eb183a691f6c08"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_efaf220b8a6afdf16a496a70fb4cbc2b","restricted_bridge":false,"source_ref":"s_c1643e14b2f449ad3aa7ec7a790fe48f","value":"note:mandarin","version_ref":"v_160f99b28e9f0b2213eb183a691f6c08"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_828c1b8bf6c0ac6161b6b314cb85d5fa","restricted_bridge":false,"source_ref":"s_c1643e14b2f449ad3aa7ec7a790fe48f","value":"note:tonka bean","version_ref":"v_160f99b28e9f0b2213eb183a691f6c08"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_ba1143234fb546c000187d0e8c8afe7d","restricted_bridge":false,"source_ref":"s_c1643e14b2f449ad3aa7ec7a790fe48f","value":"note:cardamom","version_ref":"v_160f99b28e9f0b2213eb183a691f6c08"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_0914b6bc84a072be75679ba46dd0ceb5","restricted_bridge":false,"source_ref":"s_c1643e14b2f449ad3aa7ec7a790fe48f","value":"note:fir balsam","version_ref":"v_160f99b28e9f0b2213eb183a691f6c08"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_3d0028ff58e97d4f2109503a54904e92","restricted_bridge":false,"source_ref":"s_c1643e14b2f449ad3aa7ec7a790fe48f","value":"note:bergamot","version_ref":"v_160f99b28e9f0b2213eb183a691f6c08"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_953594d90a4bcb8641750c57f54c2143","restricted_bridge":false,"source_ref":"s_c1643e14b2f449ad3aa7ec7a790fe48f","value":"note:lavender","version_ref":"v_160f99b28e9f0b2213eb183a691f6c08"}],"classification":"taste_only","code":"0159","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_bdf76c6bec20088be63076902ad00b39","restricted_bridge":false,"source_ref":"s_66e5c9f0238a134420385353e5cc121a","value":"note:bergamot","version_ref":"v_d103ab9cc3f3152ea4f8af951b26d706"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_f6990901421ba26c1b582508a1b96ebf","restricted_bridge":false,"source_ref":"s_66e5c9f0238a134420385353e5cc121a","value":"note:pine","version_ref":"v_d103ab9cc3f3152ea4f8af951b26d706"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_c373da9217846f49f2595580a7123327","restricted_bridge":false,"source_ref":"s_66e5c9f0238a134420385353e5cc121a","value":"note:sandalwood","version_ref":"v_d103ab9cc3f3152ea4f8af951b26d706"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_de268eee21df726f5d90b37ec3821eff","restricted_bridge":false,"source_ref":"s_66e5c9f0238a134420385353e5cc121a","value":"note:orange","version_ref":"v_d103ab9cc3f3152ea4f8af951b26d706"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_234174f0b1dd7ddfb6881696073c9aa8","restricted_bridge":false,"source_ref":"s_66e5c9f0238a134420385353e5cc121a","value":"note:lavandin","version_ref":"v_d103ab9cc3f3152ea4f8af951b26d706"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_4321b810ae4f786e404670d22d9ffe99","restricted_bridge":false,"source_ref":"s_66e5c9f0238a134420385353e5cc121a","value":"note:geranium","version_ref":"v_d103ab9cc3f3152ea4f8af951b26d706"}],"classification":"taste_only","code":"0160","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_cdc04769a72cc1959d4c33eb3f399aef","restricted_bridge":false,"source_ref":"s_5bc57c122f25ef3436acb2478a71221b","value":"note:lavender","version_ref":"v_872c09efb101fb0b30364ba3c012c911"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_c00cac8b326e791bc327ef7d9ade5611","restricted_bridge":false,"source_ref":"s_5bc57c122f25ef3436acb2478a71221b","value":"note:vetiver","version_ref":"v_872c09efb101fb0b30364ba3c012c911"}],"classification":"taste_only","code":"0161","concentration":"EDT","same_source_manufacturer_dual":false},
{"claims":[],"classification":"attributed_use_only","code":"0162","concentration":"EDT","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_99d894d7b2ecb3578a6b4459fa615c11","restricted_bridge":false,"source_ref":"s_3f5d7cd0b4359db478fab6dd9953ddd2","value":"note:tobacco","version_ref":"v_f65490c471517154e2d4aeb9eb30fe3f"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_681c39a3dc79e8ad7f50798110d99a1f","restricted_bridge":false,"source_ref":"s_3f5d7cd0b4359db478fab6dd9953ddd2","value":"note:cypress","version_ref":"v_f65490c471517154e2d4aeb9eb30fe3f"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_07009f1f123266fd27011db6388302d6","restricted_bridge":false,"source_ref":"s_3f5d7cd0b4359db478fab6dd9953ddd2","value":"note:incense","version_ref":"v_f65490c471517154e2d4aeb9eb30fe3f"},{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_9a2395cf21d1e7d659dc80d415398520","restricted_bridge":false,"source_ref":"s_3f5d7cd0b4359db478fab6dd9953ddd2","value":"note:cinnamon","version_ref":"v_f65490c471517154e2d4aeb9eb30fe3f"}],"classification":"taste_only","code":"0163","concentration":"EDP","same_source_manufacturer_dual":false},
{"claims":[{"attribute":"named_note_or_accord","channel":"secondary_aggregator","layer":null,"polarity":"positive","ref":"e_9d828231b51a5188a2348bd1934bc169","restricted_bridge":false,"source_ref":"s_1fee1bdda63170d8c5b7244a6d8c0fa4","value":"note:orange blossom","version_ref":"v_51efd603e8175990cffae70ecd72e24f"}],"classification":"taste_only","code":"0164","concentration":"EDP","same_source_manufacturer_dual":false}
]''')


REGISTRY = json.loads(r'''{
"0001":{"audience":null,"families":["woody","spicy"],"family_contexts":[{"ref":"e_fb449db7f1a42a2b8652a4ccae76172f","source_ref":"s_3c14dfd03f7a89c042af5041c21524aa","uses":["use:evenings_date_nights_autumn_winter"],"value":"use:evenings_date_nights_autumn_winter","version_ref":"v_864ed19ca46f712f7941b2d3b8903ddd"}]},
"0002":{"audience":null,"families":["fresh floral"]},
"0003":{"audience":"men","families":["woody","ambery","aromatic"],"family_contexts":[{"ref":"e_73e521e06c9e9b758f9029ee6bd0112f","source_ref":"s_5f779f8cb45b33f2de3410dd39dbe99f","uses":["use:evening","use:evenings_after_work_rooftop_dates_nights_out"],"value":"use:evenings_after_work_rooftop_dates_nights_out","version_ref":"v_3347b97f2cc01fbb1854e28069bef36f"}]},
"0004":{"audience":"men","families":["fresh","woody"]},
"0005":{"audience":null,"families":["floral"]},
"0006":{"audience":null,"families":["ambery","floral"]},
"0009":{"audience":null,"families":["earthy","woody","citrus"]},
"0010":{"audience":null,"families":["dry woods","fresh","citrus","fruity"]},
"0012":{"audience":null,"families":["oriental","oud","rose"]},
"0013":{"audience":null,"families":["floral amber"]},
"0018":{"audience":null,"families":["ambery","floral","woody"]},
"0022":{"audience":null,"families":["floral","fruity","musky"]},
"0023":{"audience":"men","families":["woody","spicy"]},
"0027":{"audience":"men","families":[]},
"0029":{"audience":null,"families":["floral","spicy","gourmand"]},
"0030":{"audience":null,"families":["floral","sparkling"]},
"0031":{"audience":null,"families":["floral","fruity"]},
"0032":{"audience":null,"families":["citrus","aquatic","woody"]},
"0033":{"audience":null,"families":[]},
"0034":{"audience":null,"families":["amber","floral"]},
"0035":{"audience":null,"families":["ambery","fresh","woody"]},
"0036":{"audience":null,"families":[]},
"0037":{"audience":"men","families":["woody","spicy"]},
"0038":{"audience":"men","families":["ambery","woody"]},
"0039":{"audience":null,"families":["floral"]},
"0040":{"audience":null,"families":["floral","fresh","fruity"]},
"0042":{"audience":null,"families":["woody"]},
"0043":{"audience":null,"families":["oriental"]},
"0046":{"audience":"women","families":["chypre","musk"]},
"0047":{"audience":null,"families":["floral"]},
"0048":{"audience":null,"families":["woody","aromatic"]},
"0050":{"audience":null,"families":["chypre","floral","woody"]},
"0052":{"audience":"men","families":[]},
"0053":{"audience":null,"families":["aquatic","woody"]},
"0054":{"audience":null,"families":["floral","solar"]},
"0055":{"audience":null,"families":["floral","woody","musky"]},
"0056":{"audience":null,"families":["aromatic","leathery","fougere"]},
"0057":{"audience":null,"families":["fougere","aromatic"]},
"0059":{"audience":"men","families":["fresh","woody"]},
"0061":{"audience":null,"families":["floral","gourmand"]},
"0062":{"audience":null,"families":["fresh","fougere"]},
"0065":{"audience":null,"families":["floral","fruity","woody"]},
"0068":{"audience":null,"families":["floral","aldehydic"]},
"0071":{"audience":null,"families":["woody","floral"]},
"0075":{"audience":null,"families":["floral"]},
"0079":{"audience":null,"families":["ambery","floral"]},
"0080":{"audience":null,"families":["floral","gourmand"]},
"0081":{"audience":null,"families":["floral","gourmand"]},
"0083":{"audience":null,"families":["spicy","fresh","woody"]},
"0084":{"audience":null,"families":["fresh","citrus","fruity","woody"]},
"0085":{"audience":"men","families":["oriental","woody"]},
"0086":{"audience":null,"families":["oriental","woody"]},
"0087":{"audience":null,"families":["woody","spicy"]},
"0091":{"audience":null,"families":["leathery"]},
"0093":{"audience":null,"families":["floral","aromatic"]},
"0094":{"audience":null,"families":["floral","amber","sweet"]},
"0096":{"audience":null,"families":["amber","spicy","gourmand"]},
"0097":{"audience":null,"families":["woody","amber"]},
"0098":{"audience":null,"families":["amber","woody"]},
"0099":{"audience":null,"families":[]},
"0100":{"audience":null,"families":[]},
"0101":{"audience":null,"families":["floral","chypre"]},
"0102":{"audience":null,"families":["floral","leathery"]},
"0103":{"audience":null,"families":[]},
"0104":{"audience":null,"families":[]},
"0105":{"audience":null,"families":[]},
"0106":{"audience":null,"families":["musky","leathery"]},
"0107":{"audience":null,"families":["floral","musky"]},
"0108":{"audience":null,"families":["floral","musky"]},
"0109":{"audience":null,"families":["amber","woody","vanilla"]},
"0110":{"audience":"women","families":["floral"]},
"0111":{"audience":null,"families":["amber","floral"]},
"0112":{"audience":null,"families":["amber","aromatic"]},
"0113":{"audience":null,"families":[]},
"0114":{"audience":null,"families":["floral","amber"]},
"0115":{"audience":null,"families":[]},
"0116":{"audience":null,"families":[]},
"0117":{"audience":null,"families":[]},
"0118":{"audience":null,"families":[]},
"0119":{"audience":null,"families":[]},
"0120":{"audience":null,"families":[]},
"0121":{"audience":null,"families":[]},
"0122":{"audience":null,"families":[]},
"0123":{"audience":null,"families":["fresh","marine","floral","musky"]},
"0124":{"audience":null,"families":["amber","floral","white floral","solar","woody"]},
"0125":{"audience":null,"families":["floral","white floral","vanilla","leather","woody"]},
"0126":{"audience":null,"families":["amber","woody","gourmand","powdery"]},
"0127":{"audience":null,"families":["fresh","citrus","floral","warm"]},
"0128":{"audience":null,"families":["floral"]},
"0129":{"audience":null,"families":["woody"]},
"0130":{"audience":null,"families":["woody"]},
"0131":{"audience":null,"families":["woody"]},
"0132":{"audience":null,"families":["aromatic foug\u00e8re","green","mossy woods"]},
"0133":{"audience":null,"families":["woody","oud","spicy"]},
"0134":{"audience":"men","families":["fresh","woody","spicy","ambery"]},
"0135":{"audience":null,"families":["citrus","floral","woody"]},
"0136":{"audience":null,"families":["fresh","woody","leathery","floral"]},
"0137":{"audience":null,"families":["woody","oud","aromatic","spicy","musky"]},
"0138":{"audience":"men","families":["fresh","woody","aromatic","floral","ambery"]},
"0139":{"audience":null,"families":["woody","ambery","floral"]},
"0140":{"audience":null,"families":["musky","ambery","woody"]},
"0141":{"audience":null,"families":["aromatic","woody","spicy","musky"]},
"0142":{"audience":null,"families":["ambery","woody","spicy","gourmand"]},
"0143":{"audience":null,"families":["floral","ambery","woody","oud"]},
"0144":{"audience":null,"families":["ambery","aromatic","vanilla","gourmand"]},
"0145":{"audience":null,"families":["ambery","spicy","floral","woody"]},
"0146":{"audience":null,"families":["floral","fruity","ambery"]},
"0147":{"audience":null,"families":["fougere","citrus","ambery"]},
"0148":{"audience":null,"families":["woody","spicy","leathery"]},
"0149":{"audience":null,"families":["woody","green","citrus"]},
"0150":{"audience":null,"families":["woody","spicy","leathery","oud","gourmand"]},
"0151":{"audience":null,"families":["woody","spicy","gourmand"]},
"0152":{"audience":null,"families":["woody","spicy","gourmand"]},
"0153":{"audience":null,"families":["fougere","ambery","fruity"]},
"0154":{"audience":null,"families":["fougere","ambery","leathery"]},
"0155":{"audience":null,"families":["ambery","spicy","gourmand"]},
"0156":{"audience":null,"families":["floral","fruity","gourmand"]},
"0157":{"audience":null,"families":["fougere","ambery","powdery"]},
"0158":{"audience":null,"families":["fougere","ambery","leathery"]},
"0159":{"audience":null,"families":["fougere","aromatic","powdery"]},
"0160":{"audience":null,"families":["woody","citrus","aromatic"]},
"0161":{"audience":"men","families":["fougere","aromatic","woody"]},
"0162":{"audience":null,"families":["woody","citrus","spicy"]},
"0163":{"audience":null,"families":["woody","ambery","spicy"]},
"0164":{"audience":null,"families":["floral","ambery","woody","musky"]}
}''')


POINT_OWNER = {pid: (code, role, checksum)
               for code, pair in POINT_REFERENCE.items()
               for role, (pid, checksum) in zip(("record", "index"), pair)}
APPROVED_PUBLIC_CODES = frozenset(POINT_REFERENCE)
EVIDENCE = {row["code"]: row for row in REVIEWED_ROWS}
if len(EVIDENCE) != 125 or EVIDENCE.keys() != APPROVED_PUBLIC_CODES:
    raise RuntimeError("catalog and evidence registry disagree")
del REVIEWED_ROWS

def match_catalog_points(points, emit=None):
    """A metadata companion has its own attested payload. It never supplies perfume facts."""
    matched = defaultdict(set)
    blocked = defaultdict(set)
    observed = defaultdict(list)
    seen = set()
    unknown = 0
    for point in points:
        if not isinstance(point, dict):
            unknown += 1
            continue
        payload = point.get("payload")
        raw_code = payload.get("public_display_code") if isinstance(payload, dict) else None
        code = raw_code if isinstance(raw_code, str) and raw_code in APPROVED_PUBLIC_CODES else None
        pid = point.get("id")
        binding = POINT_OWNER.get(pid) if type(pid) in (str, int) else None
        if binding is None:
            unknown += 1
            if code:
                blocked[code].add("unregistered_point_id")
            continue
        owner, role, expected = binding
        reasons = set()
        if pid in seen:
            reasons.add("repeated_point_id")
        seen.add(pid)
        actual = fingerprint(payload)
        if code != owner:
            reasons.add("code_identity_mismatch")
            if code:
                blocked[code].add("foreign_point_id")
        if not isinstance(payload, dict) or payload.get("eligibility_state") != "ELIGIBLE":
            reasons.add("ineligible_or_invalid_payload")
        if actual != expected:
            reasons.add(role + "_digest_mismatch")
        if not reasons:
            matched[owner].add(role)
        blocked[owner].update(reasons)
        observed[owner].append({"id": pid, "role": role, "reference_match": actual == expected,
                                "reasons": sorted(reasons)})
    accepted = set()
    reasons_total = Counter()
    for code in sorted(APPROVED_PUBLIC_CODES, key=lambda c: (c != "0145", c)):
        reasons = blocked[code]
        for role in ("record", "index"):
            if role not in matched[code]:
                reasons.add("missing_verified_" + role)
        if not reasons:
            accepted.add(code)
        reasons_total.update(reasons)
        if emit:
            emit({"code": code, "admitted": not reasons, "points": observed[code], "reasons": sorted(reasons)})
    return frozenset(accepted), {"retrieved_points": len(points), "unregistered_points": unknown,
                                 "admitted_unique_codes": len(accepted), "exclusions": dict(reasons_total)}

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args):
        raise ValueError("unexpected Qdrant redirect")

def read_catalog():
    url = os.getenv("QDRANT_URL", DEFAULT_QDRANT_URL).rstrip("/")
    key = os.getenv("QDRANT_API_KEY", "").strip()
    address = urlsplit(url)
    if (not key or address.scheme != "https" or not address.hostname or address.username
            or address.password or address.query or address.fragment or address.path):
        raise ValueError("invalid Qdrant configuration")
    endpoint = url + "/collections/" + COLLECTION_NAME + "/points/scroll"
    open_request = urllib.request.build_opener(NoRedirect()).open
    points, offsets = [], set()
    cursor = None
    while True:
        body = {"limit": 15, "with_payload": True, "with_vectors": False}
        if cursor is not None:
            body["offset"] = cursor
        request = urllib.request.Request(endpoint, data=json.dumps(body).encode("utf-8"),
            headers={"api-key": key, "content-type": "application/json"}, method="POST")
        with open_request(request, timeout=30) as response:
            result = json.load(response)["result"]
        page = result["points"]
        if not isinstance(page, list) or "next_page_offset" not in result:
            raise ValueError("invalid scroll result")
        points.extend(page)
        cursor = result["next_page_offset"]
        if cursor is None:
            break
        if not page or type(cursor) not in (int, str) or cursor in offsets or len(points) > 10000:
            raise ValueError("invalid pagination")
        offsets.add(cursor)
    return points

@asynccontextmanager
async def lifespan(app):
    app.state.admitted = frozenset()
    try:
        points = read_catalog()
        emit = lambda row: log.info("ANAS_CATALOG_PAIR %s", json.dumps(row, separators=(",", ":")))
        app.state.admitted, counts = match_catalog_points(points, emit)
        log.info("ANAS_CATALOG_MATCH %s", json.dumps(counts))
    except (OSError, ValueError, KeyError, TypeError, EOFError) as exc:
        # The exception text or response body can include upstream configuration.
        log.error("ANAS_CATALOG_UNAVAILABLE %s", type(exc).__name__)
    yield

app = FastAPI(title="ANAS", version=RELEASE, lifespan=lifespan)


# Customer-facing labels. Material identifiers and private product identities stay off the page.
NOTE_AR = dict(line.split("|",1) for line in """african marigold|القطيفة الأفريقية
agarwood|خشب العود
almond|اللوز
ambar wood|خشب عنبري
amber|العنبر
amber patchouli|عنبر وباتشولي
ambergris|العنبر الرمادي
amberwood|الخشب العنبري
ambrette|بذور الأمبريت
angelica|حشيشة الملاك
anise|اليانسون
apple|التفاح
aquatic flowers|الزهور المائية
basil|الريحان
benzoin|الجاوي
bergamot|البرغموت
birch|البتولا
black leather accord|أكورد الجلد الأسود
black tea|الشاي الأسود
black vanilla|الفانيليا السوداء
blackcurrant|الكشمش الأسود
blood orange|البرتقال الأحمر
caramel|الكراميل
cardamom|الهيل
cedarwood|خشب الأرز
chantilly|كريمة شانتيه
cherry accord|أكورد الكرز
cinnamon|القرفة
clary sage|المريمية المتصلبة
coconut|جوز الهند
coriander|الكزبرة
cumin|الكمون
cyclamen|بخور مريم
cypress|السرو
cypriol|السعد
damascena rose|الورد الدمشقي
dark chocolate|الشوكولاتة الداكنة
dark woods|الأخشاب الداكنة
davana|الدافانا
elemi|راتنج الإليمي
fig|التين
fir balsam|بلسم التنوب
frankincense|اللبان
freesia|الفريزيا
gaiac wood|خشب الغاياك
galbanum|الجلبانوم
gardenia|الغاردينيا
geranium|إبرة الراعي
ginger|الزنجبيل
golden amber accord|أكورد العنبر الذهبي
grapefruit|الجريب فروت
grapefruit-quince accord|أكورد الجريب فروت والسفرجل
griotte syrup|شراب الكرز الحامض
haiti vetyver|نجيل الهند الهايتي
hazelnut|البندق
heliotrope|الهليوتروب
honey|العسل
honeysuckle|زهرة العسل
incense|البخور
incense accord|أكورد البخور
indian tuberose|مسك الروم الهندي
iris|السوسن
iris accord|أكورد السوسن
jasmine|الياسمين
jasmine sambac|ياسمين السامباك
kingwood|خشب الكينغوود
labdanum|اللابدانوم
lavandin|اللافاندين
lavender|اللافندر
leather|الجلد
leather accord|أكورد الجلد
lemon|الليمون
lily of the valley|زنبق الوادي
magnolia|الماغنوليا
mahogany|الماهوجني
mandarin|اليوسفي
marine accord|أكورد بحري
marshmallow|المارشميلو
mint|النعناع
musk|المسك
myrrh|المر
naseberry|السابوديلا
neroli|النيرولي
nutmeg|جوزة الطيب
oakmoss|طحلب البلوط
orange|البرتقال
orange blossom|زهر البرتقال
oregano|الأوريغانو
osmanthus|الأوسمانثوس
oud|العود
papaya|البابايا
patchouli|الباتشولي
peach|الخوخ
pear|الكمثرى
peony|الفاوانيا
pepper|الفلفل
petitgrain|أوراق وأغصان النارنج
pimento|البهار الإفرنجي
pine|الصنوبر
pine needle|إبر الصنوبر
pineapple|الأناناس
pink pepper|الفلفل الوردي
plum accord|أكورد البرقوق
pomegranate|الرمان
praline|البرالين
raspberry|توت العليق
rose|الورد
rose bouquet accord|أكورد باقة الورد
rose de mai|ورد مايو
rosemary|إكليل الجبل
saffron|الزعفران
saffron accord|أكورد الزعفران
sage|المريمية
salted accord|أكورد ملحي
sambac jasmine|ياسمين سامباك
sandalwood|خشب الصندل
sichuan pepper|فلفل سيتشوان
star anise accord|أكورد اليانسون النجمي
suede|الشمواه
tea|الشاي
thyme|الزعتر
tobacco|التبغ
tonka bean|حبوب التونكا
tuberose|مسك الروم
turkish rose|الورد التركي
vanilla|الفانيليا
verbena|اللويزة
vetiver|نجيل الهند
violet|البنفسج
violet accord|أكورد البنفسج
violet leaves|أوراق البنفسج
watermelon|البطيخ
white leather accord|أكورد الجلد الأبيض
white musk|المسك الأبيض
white musks|المسك الأبيض المتعدد
wood|الأخشاب
ylang-ylang|الإيلنغ
yuzu|اليوزو""".splitlines())

FAMILY_AR = dict(line.split("|") for line in """woody|خشبي
floral|زهري
ambery|عنبري
amber|عنبر
spicy|متبّل
aromatic|عشبي عطري
fresh|منعش
gourmand|غورمان
citrus|حمضي
musky|مسكي
fougere|فوجير
fruity|فاكهي
leathery|جلدي
oud|عودي
oriental|شرقي
chypre|شيبر
vanilla|فانيلي
powdery|بودري
aquatic|مائي
solar|شمسي
white floral|زهور بيضاء
green|أخضر
fresh floral|زهري منعش
earthy|ترابي
dry woods|أخشاب جافة
rose|وردي
floral amber|زهري عنبري
sparkling|فوّار
musk|طابع المسك
aldehydic|ألدهيدي
sweet|حلو
marine|بحري
leather|طابع الجلد
warm|دافئ
aromatic fougère|فوجير عطري
mossy woods|أخشاب طحلبية""".splitlines())
AUDIENCES = {'men':'رجالي','women':'نسائي','unisex':'للجنسين'}
CHANNELS = {'manufacturer_authored_content':'المصنّع','professional_editorial':'مرجع تحريري متخصص',
            'retailer_editorial':'تحرير بائع','brand_regional_store_editorial':'تحرير متجر العلامة الإقليمي',
            'secondary_aggregator':'مرجع تجميعي ثانوي'}
CONTEXT_AR = dict(line.split('|') for line in """use:evenings_after_work_rooftop_dates_nights_out|الأمسيات والخروج بعد العمل والمواعيد والسهر
use:date_night_editorial|موعد مسائي
use:evening_or_more_formal_occasions|المساء أو المناسبات الرسمية
use:cool_evenings_weekends_casual_seller_editorial|الأمسيات الباردة وعطلات نهاية الأسبوع والاستعمال غير الرسمي
use:daily_office_casual_warm_weather|الاستعمال اليومي والمكتب والأيام غير الرسمية والطقس الدافئ
use:evening_editorial_selection|اختيار تحريري للمساء
use:spring_summer_also_year_round|الربيع والصيف مع ذكر الاستعمال على مدار السنة
use:romantic_evening|أمسية رومانسية
use:fall_winter_evening_cooler_with_office_summer_caution|المساء والخريف والشتاء والجو البارد، مع تحفّظ المصدر على المكتب والصيف
use:winter_chilly_nights_close_encounters|الشتاء والليالي الباردة واللقاءات القريبة
use:special_occasion_editorial|مناسبة خاصة
use:day_night_everyday_evenings_special_occasions|النهار والليل والاستعمال اليومي والأمسيات والمناسبات الخاصة
use:workdays_weekends_nights_out_bold_impression|أيام العمل وعطلات نهاية الأسبوع والخروج ليلًا وإبراز الحضور
use:wedding_groom_confidence|العريس يوم زفافه مع ذكر الثقة""".splitlines())
CONCENTRATIONS={'EDT':'أو دو تواليت','EDP':'أو دو بارفان','Extrait':'خلاصة عطرية','Parfum':'بارفان',
  'Elixir':'إكسير','Eau de Parfum for Women':'أو دو بارفان','Eau de Parfum Intense':'أو دو بارفان إنتنس'}


# A small, closed Arabic grammar. Every word must be consumed before an interpretation
# can be confirmed. A later unrecognised clause puts the entire selection on hold.
def normalize(text):
    text = unicodedata.normalize("NFKC", text).casefold().translate(
        str.maketrans("أإآٱى٠١٢٣٤٥٦٧٨٩", "ااااي0123456789"))
    return " ".join("".join(ch for ch in text if not unicodedata.combining(ch) and ch != "ـ").split())

# Arabic display labels and accepted literal phrasings; these are language mappings,
# never evidence about a particular perfume. Context vocabulary retains source scope.
NOTES = {
    "grapefruit": ("الجريب فروت", "جريب فروت", "غريب فروت", "الجريب فروت", "الغريب فروت", "جريبفروت"),
    "mint": ("النعناع", "نعناع", "النعناع"), "rose": ("الورد", "الورد", "ورد"),
    "patchouli": ("الباتشولي", "الباتشولي", "باتشولي"), "oud": ("العود", "عود", "العود"),
    "vanilla": ("الفانيليا", "فانيليا", "فانيلا", "الفانيلا", "الفانيليا"),
    "jasmine": ("الياسمين", "ياسمين", "الياسمين"), "lemon": ("الليمون", "ليمون", "الليمون"),
    "saffron": ("الزعفران", "زعفران", "الزعفران"), "cyclamen": ("بخور مريم", "بخور مريم"),
    "violet leaves": ("أوراق البنفسج", "أوراق البنفسج"), "leather": ("الجلد", "الجلد", "جلد"),
    "lavender": ("اللافندر", "اللافندر", "لافندر", "الخزامى"), "vetiver": ("نجيل الهند", "نجيل الهند"),
    "sandalwood": ("خشب الصندل", "خشب الصندل"), "bergamot": ("البرغموت", "البرغموت", "برغموت"),
    "amber": ("العنبر", "عنبر", "العنبر"), "musk": ("المسك", "المسك", "مسك"),
    "ginger": ("الزنجبيل", "زنجبيل", "الزنجبيل"), "iris": ("السوسن", "السوسن", "سوسن"),
    "orange blossom": ("زهر البرتقال", "زهر البرتقال"), "pear": ("الكمثرى", "الكمثرى", "كمثرى"),
    "cedarwood": ("خشب الأرز", "خشب الأرز"), "tobacco": ("التبغ", "التبغ", "تبغ"),
}
CONTEXTS = {
    "use:day": ("الاستخدام نهارًا", "نهار", "نهارا", "نهاري", "نهارية", "للنهار", "بالنهار", "في النهار", "صباحا"),
    "use:evening": ("الاستخدام مساءً", "مساء", "مسائي", "للمساء", "في المساء"),
    "use:hot_weather": ("الاستخدام في الجو الحار", "في الجو الحار", "للجو الحار", "للحر", "في الحر"),
    "use:office": ("الاستخدام في المكتب", "للعمل", "للمكتب", "في المكتب", "في العمل"),
    "use:everyday_summer_wear": ("الاستخدام اليومي في الصيف", "يوميا في الصيف", "للاستخدام اليومي في الصيف"),
    "use:evenings_date_nights_autumn_winter": ("الأمسيات والمواعيد الغرامية في الخريف والشتاء",
            "للأمسيات والمواعيد الغرامية في الخريف والشتاء"),
    "use:daytime_warm_weather_sport_office_everyday_spring_summer": (
        "النهار والطقس الدافئ والرياضة والمكتب والاستخدام اليومي في الربيع والصيف",
        "للنهار والطقس الدافئ والرياضة والمكتب والاستخدام اليومي في الربيع والصيف"),
    "use:wedding_groom": ("استخدام العريس في الزفاف", "للعريس في الزفاف"),
}
for slug, arabic in NOTE_AR.items():
    if slug not in NOTES:
        NOTES[slug] = (arabic, arabic.removeprefix('ال'))
for key, arabic in CONTEXT_AR.items():
    CONTEXTS.setdefault(key, (arabic,))
LABELS = {"note:" + slug: spec[0] for slug, spec in NOTES.items()}
LABELS.update({slug: spec[0] for slug, spec in CONTEXTS.items()})
TERMS = {normalize(alias): ("note:" + slug) for slug, spec in NOTES.items() for alias in spec}
TERMS.update({normalize(alias): slug for slug, spec in CONTEXTS.items() for alias in spec})
for key, options in {
    'audience:men': ('رجالي','رجاليا','رجاليه','رجالية','للرجال','رجل','للرجل','for men','men'),
    'audience:women': ('نسائي','نسائيا','نسائيه','نسائية','للنساء','للمرأة','للنساء فقط','حريمي','women'),
    'audience:unisex': ('للجنسين','مشترك','للرجال والنساء','يونيسكس','unisex'),
    'use:day': ('بالصباح','الصباح','للصباح','في الصباح','للنهار','نهاراً'),
    'use:evening': ('المساء','بالليل','في الليل','لليل','ليلي','ليلا'),
    'use:office': ('الدوام','للدوام','في الدوام','للمكتب','المكتب','للشغل'),
    'use:daily': ('كل يوم','للاستخدام اليومي','يومي','يوميا','يومية'),
    'use:occasion': ('للمناسبات','مناسبة','مناسبات','لمناسبة خاصة'),
    'use:summer': ('للصيف','صيفي','في الصيف'), 'use:winter': ('للشتاء','شتوي','في الشتاء'),
}.items():
    for word in options: TERMS[normalize(word)] = key
LABELS.update({'audience:'+key:val for key,val in AUDIENCES.items()})
LABELS.update({'use:daily':'الاستخدام اليومي','use:occasion':'المناسبات','use:summer':'الصيف','use:winter':'الشتاء'})
for slug, arabic in FAMILY_AR.items():
    k='family:'+slug
    LABELS[k]='طابع '+arabic
    for wording in ('طابع '+arabic,'بطابع '+arabic,arabic):
        TERMS.setdefault(normalize(wording),k)
for word,slug in {'خشبية':'woody','حمضيات':'citrus','حمضية':'citrus','منعشة':'fresh','زهور':'floral','زهرية':'floral','سكّري':'sweet','حلوة':'sweet'}.items():
    TERMS[normalize(word)]='family:'+slug
TERMS = dict(sorted(TERMS.items(), key=lambda item: -len(item[0])))
# Filler is deliberately restricted to phrases with no additional material meaning.
PREFIX = re.compile(r"(?:(?:السلام عليكم|مرحبا|يا ريت|لو تكرمت|ممكن تقترح لي|ممكن ترشح لي|عايز لي|رشحلي|عايزه|عاوزة|عايزة|ابحث عن|ادور علي|ابحث|ممكن|احتاج الي|محتاج|ترشح لي|رشح لي|رشحلي|عاوز|بدي|بغيت|انا|لي|عطور|عطره|يكون|يكون فيه|اريد|اريده|احب|افضل|ابي|ابغي|ابغى|عايز|احتاج|اطلب|اشترط|لنفسى|لنفسي|عطرا|عطر|رائحه|رائحة|برائحة|برائحه|بنوتة|نوتة|نوتات|فيه|للاستخدام|لاستخدامه|استعمله|استخدمه|واستخدمه|واستعمله|واشترط|واريد|واحب|وافضل|من فضلك|لو سمحت|وايضا|ايضا|مع|و)(?=\s|$)\s*)+")
GENERAL = {normalize(x) for x in ("أريد عطراً","أريد عطر","عطر","عطور","ابحث عن عطر","أريد توصية","رشح لي عطر","ممكن تساعدني","مرحبا","السلام عليكم","هلا","ما بعرف","لا أعرف","ساعدني أختار","ما عندي تفضيل")}
AVOID = re.compile(r"(?:بدون|بلا|من دون|لا احب|ما احب|ما بحب|اتجنب|من غير|لا اريد|ما اريد)\s+")
HOURS = re.compile(r"(?:ثبات(?:ه)?|يثبت|يدوم)\s+(?:(?:لمدة|ل)\s*)?(ست|ستة|\d{1,2})\s*ساعات?(?=$|\s)")
CONFIRM = {"تاكيد", "تاكيد التفضيلات", "اكد تفضيلاتي"}
RESET = {"بداية جديدة", "من جديد", "ابدا من جديد", "اعادة البدء", "ابدأ من جديد"}

def parse_conditions(message):
    normalized = normalize(message)
    # Commas separate clauses; a question, quotation, URL, or unconsumed word
    # is ambiguous. In particular, other people's statements cannot become self claims.
    rest = re.sub(r"[،,؛;.!]+", " ", normalized).strip()
    found = []
    while rest:
        rest = PREFIX.sub("", rest, count=1).strip()
        if rest.startswith("و") and len(rest) > 1 and rest[1] != " " and not rest.startswith("ورد"):
            rest = rest[1:].lstrip()
            rest = PREFIX.sub("", rest, count=1).strip()
        negative = AVOID.match(rest)
        if negative:
            rest = rest[negative.end():]
        duration = HOURS.match(rest)
        if duration:
            n = duration.group(1)
            key = "duration_hours:" + ("6" if n in ("ست", "ستة") else str(int(n)))
            end = duration.end()
        else:
            phrase = next((s for s in TERMS if rest == s or rest.startswith(s + " ")), None)
            if phrase is None:
                return None
            key, end = TERMS[phrase], len(phrase)
        polarity = "negative" if negative else "positive"
        if (key, polarity) not in found:
            found.append((key, polarity))
        rest = rest[end:].strip()
    return found or None

def label(condition):
    key, polarity = condition
    value = "ثبات لمدة " + key.split(":")[1] + " ساعات" if key.startswith("duration_hours:") else LABELS[key]
    return ("تجنّب " if polarity == "negative" else "") + value

def catalog_filters_match(code, conditions):
    record=REGISTRY[code]
    for key, polarity in conditions:
        kind, value = key.split(':',1)
        if kind == 'audience':
            if polarity != 'positive' or record['audience'] != value:
                return False
        if kind == 'family' and (polarity != 'positive' or value not in record['families']):
            return False
    return True

def catalog_family_support(row, conditions):
    # Join verified family metadata to advice on the exact official product page.
    # The SKU, accepted publisher text version, and excerpt reference must still match.
    if not any(k.startswith('family:') for k,p in conditions) or not catalog_filters_match(row['code'],conditions):
        return None
    uses=[k for k,p in conditions if k.startswith('use:') and p=='positive']
    if not uses or any(p!='positive' or not k.startswith(('family:','audience:','use:')) for k,p in conditions):
        return None
    for link in REGISTRY[row['code']].get('family_contexts',[]):
        if not set(uses)<=set(link['uses']):continue
        for claim in row['claims']:
            if (claim['ref']==link['ref'] and claim['source_ref']==link['source_ref']
                and claim['version_ref']==link['version_ref'] and claim['value']==link['value']
                and claim['attribute']=='context' and claim['polarity']=='positive'
                and claim['channel']=='manufacturer_authored_content' and not claim['restricted_bridge']):
                return claim
    return None

def support_for(row, conditions):
    """Intersect exact claim groups by source, source version, and authority on this product."""
    if not catalog_filters_match(row['code'], conditions):
        return None
    conditions = [c for c in conditions if not c[0].startswith(('audience:','family:'))]
    if not conditions:
        return None
    groups = defaultdict(dict)
    for claim in row["claims"]:
        attribute = claim["attribute"]
        key = (claim["value"], claim["polarity"])
        if key not in conditions:
            continue
        ordered_type = key[0].split(":", 1)[0]
        if not ((ordered_type == "note" and attribute in ("note", "named_note_or_accord"))
                or (ordered_type == "use" and attribute == "context")):
            continue
        # This product match promises a single first-party account of taste and use.
        if claim["channel"] != "manufacturer_authored_content":
            continue
        group = (claim["source_ref"], claim["version_ref"], claim["channel"])
        groups[group][key] = claim["ref"]
    for group, proof in groups.items():
        if all(condition in proof for condition in conditions):
            # Contradictory in-scope testimony must not result in an unconditional match.
            opposite = {(k, "negative" if p == "positive" else "positive") for k,p in conditions}
            if any((c["value"], c["polarity"]) in opposite for c in row["claims"]
                   if c["channel"] == "manufacturer_authored_content"):
                return None
            return [proof[condition] for condition in conditions]
    return None

def evaluate(conditions, admitted):
    matches = [(row["code"], support_for(row, conditions) if any(k.startswith("note:") for k,p in conditions)
                else catalog_family_support(row,conditions)) for row in EVIDENCE.values()]
    matches = [(code, proof) for code, proof in matches if proof]
    if not matches:
        if any(k.startswith("duration_hours:") for k, _ in conditions):
            return [], "لم أجد دليلًا يثبت مدة الثبات المطلوبة مع بقية شروطك، لذلك سحبتُ أي ترشيح سابق."
        return [], "لم أجد في الأدلة المراجعة إصدارًا يوثّق كل ما طلبته. يمكنك حذف شرط أو تغييره، أو فتح السجل للاطلاع على الأوصاف المتاحة."
    recs=[]
    notes = [label(c) for c in conditions if c[0].startswith("note:")]
    contexts = [label(c) for c in conditions if c[0].startswith("use:")]
    filters = [label(c) for c in conditions if c[0].startswith(("audience:","family:"))]
    for code, proof in sorted(matches):
        if code not in admitted:
            continue
        explanation = ("ورد في وصف المصنّع لهذا الإصدار " + " و".join(notes)
                       + " ضمن الوصف العطري. ويذكر المصدر نفسه " + " و".join(contexts) + ".")
        if not notes:
            explanation = ("يصنّف السجل المعتمد هذا الإصدار ضمن " + " و".join(label(c) for c in conditions if c[0].startswith('family:'))
                           + ". ويذكر المصنّع في الصفحة الرسمية للإصدار " + LABELS[proof['value']] + ".")
            filters=[label(c) for c in conditions if c[0].startswith('audience:')]
        if filters:
            explanation += " ويطابق تصنيف السجل طلبك (" + "، ".join(filters) + ")."
        recs.append({"public_display_code": code,"title": "رمز العطر "+code,"reason": explanation})
    if not recs:
        return [], "تعذّر التحقق من سجل العطر في الكتالوج المتصل. أوقفت عرض الرمز."
    return recs, recs[0]["reason"] if len(recs)==1 else "هذه الإصدارات تطابق الشروط الموثقة."

def initial_state():
    return {"conditions": [], "active": [], "phase": "new", "revision": 0}

def suggestions(conditions, phase, admitted):
    if phase == 'new':
        return ['رجالي','نسائي','أريد عطر']
    if phase != 'collect':
        return []
    has_note = any(k.startswith(('note:','family:')) and p=='positive' for k,p in conditions)
    wanted='use:' if has_note else 'note:'
    keys=set()
    for code,row in EVIDENCE.items():
        if code not in admitted or not catalog_filters_match(code,conditions):
            continue
        for link in REGISTRY[code].get('family_contexts',[]):
            for f in REGISTRY[code]['families']:
                fk='family:'+f
                for uk in link['uses']:
                    if not catalog_family_support(row,[(fk,'positive'),(uk,'positive')]):continue
                    if not all(p=='positive' and (k.startswith('audience:') or k in (fk,uk)) for k,p in conditions):continue
                    if has_note and not any(k.startswith('use:') for k,p in conditions):keys.add(uk)
                    elif not has_note:keys.add(fk)
        groups=defaultdict(set)
        for c in row['claims']:
            if c['channel']=='manufacturer_authored_content' and c['polarity']=='positive':
                groups[c['source_ref'],c['version_ref']].add(c['value'])
        for facts in groups.values():
            if not any(k.startswith('use:') for k in facts) or not any(k.startswith('note:') for k in facts):
                continue
            if not all(p=='positive' and k in facts for k,p in conditions if not k.startswith(('audience:','family:'))):
                continue
            keys.update(k for k in facts if k.startswith(wanted) and k in LABELS and (k,'positive') not in conditions)
    if not keys:
        return []
    return [LABELS[k] for k in sorted(keys,key=lambda k:(k not in ('family:woody','note:grapefruit','note:mint','note:rose','use:day','use:evening'),LABELS[k]))][:7]

def process(message, state, admitted):
    old_codes = state['active']
    conditions = list(state['conditions'])
    command = normalize(message)
    recs, question, msg = [], None, ''
    phase = state['phase']
    blocked = False
    if command in RESET:
        conditions, phase = [], 'new'
    elif command in CONFIRM:
        if phase in ('confirm','result'):
            recs,msg = evaluate(conditions,admitted)
            phase='result'
        else:
            question='أكمل الوصف أولًا. يمكنك الكتابة أو اختيار أحد الاقتراحات.'
    else:
        if phase=='unresolved' and not command.startswith('استبدل رسالتي:'):
            blocked=True
        elif command.startswith('احذف '):
            target=command[5:].strip()
            kept=[c for c in conditions if normalize(label(c))!=target]
            if len(kept)==len(conditions) or phase=='unresolved':
                blocked=True
            else:
                conditions=kept
        elif command in GENERAL and phase != 'unresolved':
            pass
        else:
            revised=message.split(':',1)[1] if phase=='unresolved' and command.startswith('استبدل رسالتي:') else message
            parsed=parse_conditions(revised)
            if parsed:
                conditions=list(dict.fromkeys(conditions+parsed))
            else:
                blocked=True
        conflicts=any((k,'negative' if pol=='positive' else 'positive') in conditions for k,pol in conditions)
        audiences={k for k,pol in conditions if k.startswith('audience:') and pol=='positive'}
        if blocked:
            phase='unresolved'
            question='بقي جزء من رسالتك غير واضح. أعد صياغة آخر رسالة كاملة في الحقل أدناه؛ ستبقى الشروط السابقة المعروضة محفوظة.'
        elif conflicts or len(audiences)>1:
            phase='edit'
            question='لديك شرطان متعارضان. احذف الشرط الذي تريد تغييره ثم أكمل طلبك.'
        elif not conditions:
            phase='collect'
            question='أي رائحة أو طابع تفضّل؟ اختر من الاقتراحات أو اكتب ما تحب.'
        elif not any(k.startswith(('note:','family:')) and pol=='positive' for k,pol in conditions):
            phase='collect'
            question='أي رائحة تحبّها في العطر؟ اختر نوتة أو طابعًا عطريًا، أو اكتب تفضيلك.'
        elif not any(k.startswith('use:') and pol=='positive' for k,pol in conditions):
            phase='collect'
            question='ومتى أو أين تريد استعمال العطر؟'
        elif any(k.startswith('duration_hours:') for k,_ in conditions) and not any(
                c['attribute']=='performance' for r in EVIDENCE.values() for c in r['claims']):
            phase='unsupported'
            msg='لا يتوفر في الأدلة المراجعة قياس يثبت مدة الثبات المطلوبة. لا أستطيع ترشيح رمز بهذه الشروط.'
        else:
            phase,question='confirm','هل أعتمد هذا الوصف للبحث في الكتالوج؟'
    codes=[r['public_display_code'] for r in recs]
    state.update(conditions=conditions,active=codes,phase=phase,revision=state['revision']+1)
    choices=suggestions(conditions,phase,admitted)
    if phase=='collect' and not choices and any(k.startswith(('audience:','family:')) for k,p in conditions):
        question='لم أجد ضمن اختيارات التوصية الموثقة مسارًا يجمع هذا التصنيف مع شروطك الحالية. يمكنك تصفّح السجلات المطابقة أو تعديل شرط من طلبك.'
    return {'recommendations':recs,'clarification_question':question,'message':msg,'phase':phase,
            'criteria':[label(c) for c in conditions],'revision':state['revision'],
            'invalidation_triggered':bool(old_codes and old_codes!=codes),
            'choices':choices,
            'audience':next((k.split(':')[1] for k,p in conditions if k.startswith('audience:') and p=='positive'),''),
            'family':next((k.split(':')[1] for k,p in conditions if k.startswith('family:') and p=='positive'),'')}


class QueryRequest(BaseModel):
    session_id: str = Field(min_length=1, max_length=128)
    message: str = Field(min_length=1, max_length=1200)

sessions = OrderedDict()
session_lock = threading.Lock()
SESSION_TTL = 1800
SESSION_LIMIT = 4096

def prune_sessions(now):
    while sessions:
        _, (last, _) = next(iter(sessions.items()))
        if now - last < SESSION_TTL:
            return
        sessions.popitem(last=False)

def create_state(key, now):
    if len(sessions) >= SESSION_LIMIT:
        sessions.popitem(last=False)
    state = initial_state()
    sessions[key] = (now, state)
    return state

def turn(key, message, version=None):
    if not isinstance(message, str) or not 1 <= len(message.strip()) <= 1200:
        raise HTTPException(422, "invalid message length")
    now = time.monotonic()
    with session_lock:
        prune_sessions(now)
        if key not in sessions:
            if version is not None:
                raise HTTPException(409, "expired")
            state = create_state(key, now)
        else:
            _, state = sessions[key]
        if version is not None and version != state["revision"]:
            raise HTTPException(409, "stale")
        if not app.state.admitted:
            raise HTTPException(503, "catalog unavailable")
        result = process(message.strip(), state, app.state.admitted)
        sessions[key] = (now, state)
        sessions.move_to_end(key)
        return result

@app.post("/api/v1/recommend")
def recommend_endpoint(req: QueryRequest):
    result = turn(("api", req.session_id), req.message)
    return {"session_id": req.session_id, "result": result}

CSS = """
*{box-sizing:border-box}html{background:#f5f2e9;color:#233c32;color-scheme:light}
body{margin:0;font:1rem/1.75 Tahoma,Arial,sans-serif}
main{width:min(100%,42rem);margin:0 auto;padding:clamp(1rem,5vw,2.5rem)}
header{display:flex;align-items:center;justify-content:space-between;gap:.75rem;padding:.4rem 0 1rem;border-bottom:1px solid #adbcae}
h1{font-size:clamp(1.2rem,4.5vw,1.8rem);line-height:1.4;margin:0}
.wordmark{font:1.55rem Georgia,serif;letter-spacing:.14em}
.panel{background:#fffef8;border:1px solid #c7d2c4;border-radius:.9rem;padding:1.2rem;margin:1.15rem 0}
p{margin:.35rem 0 .6rem}h2{font-size:1.06rem;margin:.1rem 0 .45rem}.small{font-size:.92rem;color:#47614f}
code,bdi{font:600 1.8rem/1.5 Georgia,serif;letter-spacing:.07em}
ul{padding-inline-start:1.3rem;margin:.2rem 0 .8rem}.result{border-inline-start:4px solid #356146}
label{display:block;font-weight:600;margin:.8rem 0 .3rem}textarea{width:100%;padding:.65rem .85rem;border-radius:.55rem;border:1px solid #829488;font:inherit;background:white;color:inherit}
button,a.button{min-height:44px;padding:.4rem .9rem;border:1px solid #294936;border-radius:.55rem;font:inherit;cursor:pointer;color:white;background:#294936;text-decoration:none}
button.secondary{background:transparent;color:#294936}
.actions{display:flex;gap:.55rem;flex-wrap:wrap;align-items:center;margin:.5rem 0}
:focus-visible{outline:3px solid #706632;outline-offset:3px}
"""
CSS += """
main.wide{width:min(100%,62rem)}header{margin-bottom:1.4rem}header nav{display:flex;gap:.7rem 1.2rem;flex-wrap:wrap}
a{color:#26533e;text-underline-offset:.22em}h1{font-size:clamp(1.6rem,5vw,2.3rem);margin:.5rem 0 1rem}
.records{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,10rem),1fr));gap:.65rem}
.record{display:flex;flex-direction:column;padding:.75rem 1rem;background:#fffdf6;border:1px solid #bdc9b9;border-radius:.55rem;text-decoration:none;color:#223c30}
.record bdi{font-size:1.35rem;font-variant-numeric:tabular-nums;align-self:start}.record span{font-size:.85rem;color:#43564a}
.record:hover,.record:focus-visible{background:#e7eee1}.filters{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,10rem),1fr));gap:.6rem;align-items:end;margin:1rem 0}
.filters label{margin:0}.filters input,select{box-sizing:border-box;display:block;width:100%;max-width:100%;min-height:44px;border:1px solid #829488;border-radius:.5rem;background:#fffef8;color:inherit;font:inherit;padding:.32rem .5rem}
.actions.choices{align-items:stretch}.choices button{background:#eff3e9;color:#294936;border-color:#b3c4af;text-align:start}
.facts{display:flex;flex-wrap:wrap;gap:.85rem 2rem;padding:1rem 0;border-block:1px solid #c5cebd}
dt{color:#4c6152;font-size:.86rem}dd{margin:0;font-weight:bold}.lede{color:#445a4b}.scope{margin:.6rem 0 1.15rem}
details{margin:.7rem 0}summary{cursor:pointer;text-decoration:underline}.confirm{margin:.85rem 0}
"""
def render_page(session_id, result=None, error=None):
    esc = html.escape
    result = result or {"revision":0,"phase":"new","criteria":[],"recommendations":[],"choices":suggestions([], "new", ())}
    bits = []
    if error:
        bits.append('<p role="alert">' + esc(error) + '</p><a class="button" href="/">ابدأ محادثة جديدة</a>')
        return page_shell('مستشارك العطري',''.join(bits))
    if result.get('invalidation_triggered'):
        bits.append('<p role="status">سُحب الترشيح السابق بعد تعديل طلبك.</p>')
    if result['criteria']:
        bits.append('<section aria-label="الشروط"><h2>ما فهمته من طلبك</h2><ul>')
        bits.extend('<li>'+esc(c)+'</li>' for c in result['criteria'])
        bits.append('</ul></section>')
    if result['recommendations']:
        bits.append('<section class="panel result" data-recommendations><h2>العطر المقترح</h2>')
        for item in result['recommendations']:
            code=item['public_display_code']
            bits.append('<p>رمز العطر <a href="/catalog/'+code+'"><bdi dir="ltr">'+code+'</bdi></a></p><p>'+esc(item['reason'])+'</p>')
        bits.append('</section>')
    else:
        body=result.get('clarification_question') or result.get('message') or 'لمن تبحث عن عطر؟ صف ما تحبه وأين تريد استعماله، أو اختر نقطة بداية.'
        bits.append('<p class="panel" role="status">'+esc(body)+'</p>')
    aud,fam=result.get('audience',''),result.get('family','')
    if aud or fam:
        available=sum((not aud or row['audience']==aud) and (not fam or fam in row['families']) for row in REGISTRY.values())
        scope=' · '.join(filter(None,[AUDIENCES.get(aud),FAMILY_AR.get(fam)]))
        bits.append('<p class="scope"><a href="'+esc(catalog_url(aud,fam),quote=True)+'">عرض سجلات '+esc(scope)+' ('+str(available)+')</a></p>')
        if (result['phase']=='collect' and len(result['criteria'])==1 and available>0):
            subset=[code for code,m in sorted(REGISTRY.items()) if (not aud or m['audience']==aud) and (not fam or fam in m['families'])]
            bits.append('<details><summary>معاينة سجلات من هذا التصنيف</summary><div class="records">'+''.join(record_card(c) for c in subset[:4])+'</div></details>')
    bits.append('<form action="/chat" method="post" autocomplete="off">')
    bits.append('<input type="hidden" name="session_id" value="'+esc(session_id,quote=True)+'">')
    bits.append('<input type="hidden" name="revision" value="'+str(result['revision'])+'">')
    phase=result['phase']
    if phase=='confirm':
        bits.append('<button class="confirm" name="command" value="تأكيد" formnovalidate>تأكيد التفضيلات</button>')
    choices=result.get('choices',[])
    if choices:
        bits.append('<div class="choices actions" aria-label="اختيارات للمتابعة">')
        bits.extend('<button name="choice" value="'+esc(v,quote=True)+'" formnovalidate>'+esc('ساعدني أختار' if v=='أريد عطر' else v)+'</button>' for v in choices)
        bits.append('</div>')
    bits.append('<label for="message">رسالتك</label><textarea name="message" id="message" rows="2" maxlength="1200" placeholder="مثلاً، أريد عطر رجالي"></textarea><div class="actions">')
    bits.append('<button type="submit"'+(' name="command" value="صياغة"' if phase=='unresolved' else '')+'>'+('استبدال الرسالة غير المفهومة' if phase=='unresolved' else 'إرسال')+'</button>')
    if phase!='new':
        bits.append('<button class="secondary" name="command" value="بداية جديدة" formnovalidate>بداية جديدة</button>')
    bits.append('</div>')
    if result['criteria'] and phase!='unresolved':
        bits.append('<details><summary>تعديل الشروط</summary><div class="actions choices">')
        bits.extend('<button name="remove" value="'+esc(c,quote=True)+'">حذف '+esc(c)+'</button>' for c in result['criteria'])
        bits.append('</div></details>')
    bits.append('</form>')
    return page_shell('مستشارك العطري',''.join(bits))

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def chat_page():
    # A fresh form has an isolated, random session. No tracking/persistent cookies.
    token = secrets.token_urlsafe(24)
    with session_lock:
        now = time.monotonic()
        prune_sessions(now)
        create_state(("form", token), now)
    return render_page(token)

@app.post("/chat", response_class=HTMLResponse, include_in_schema=False)
async def submit_form(request: Request):
    content = bytearray()
    async for chunk in request.stream():
        content.extend(chunk)
        if len(content) > 24576:
            raise HTTPException(413)
    try:
        fields = parse_qs(content.decode("ascii"), encoding="utf-8", errors="strict", keep_blank_values=True, max_num_fields=4)
        if not all(len(items)==1 for items in fields.values()):
            raise ValueError
        sid, rev = fields["session_id"][0], int(fields["revision"][0])
        draft = fields.get("message", [""])[0].strip()
        cmd = fields.get("command", [""])[0]
        choice = fields.get("choice", [""])[0]
        remove = fields.get("remove", [""])[0]
        if cmd not in ("", "تأكيد", "بداية جديدة", "صياغة") or sum(bool(x) for x in (choice,remove,cmd))>1:
            raise ValueError
        # Edits typed under a pending proposal take precedence over its old confirmation.
        if cmd == "صياغة":
            if not draft: raise HTTPException(422)
            message="استبدل رسالتي:"+draft
        elif remove:
            message="احذف "+remove
        else:
            message=draft if draft and cmd!="بداية جديدة" else cmd or choice or draft
        result = turn(("form", sid), message, rev)
        return render_page(sid, result)
    except (UnicodeError, ValueError, KeyError) as err:
        raise HTTPException(422, "invalid form") from err
    except HTTPException as err:
        messages = {409:"انتهت صلاحية هذه الصفحة أو أُرسلت الرسالة من قبل. ابدأ محادثة جديدة.",
                    422:"اكتب رسالتك ثم أرسلها.", 503:"تعذّرت قراءة الكتالوج. حاول مجددًا بعد قليل."}
        response = render_page("", error=messages.get(err.status_code, "تعذّر إكمال الطلب."))
        response.status_code = err.status_code
        return response



def page_shell(title, content, *, wide=False, status=200):
    heading=html.escape(title)
    page = ('<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1"><title>'+heading+' | ANAS</title>'
            '<style>'+CSS+'</style></head><body><main'+(' class="wide"' if wide else '')+'>'
            '<header><span class="wordmark" lang="en" dir="ltr">ANAS</span><nav aria-label="التنقل الرئيسي">'
            '<a href="/">المستشار العطري</a><a href="/catalog">سجل الكتالوج</a></nav></header>'
            '<h1>'+heading+'</h1>'+content+'</main></body></html>')
    return HTMLResponse(page,status_code=status,headers={'Cache-Control':'no-store','Referrer-Policy':'no-referrer',
       'Content-Security-Policy':"default-src 'none'; style-src 'unsafe-inline'; form-action 'self'; frame-ancestors 'none'; base-uri 'none'"})

def catalog_url(audience='', family=''):
    query=urllib.parse.urlencode({k:v for k,v in [('audience',audience),('family',family)] if v})
    return '/catalog'+('?' + query if query else '')

def note_label(value):
    if value.startswith('note:material_'):
        return 'مكوّن عطري ذو تسمية خاصة'
    return LABELS.get(value) or NOTE_AR.get(value.removeprefix('note:'))

def evidence_label(c):
    return LABELS.get(c['value']) if c['attribute']=='context' else note_label(c['value'])

def record_card(code):
    row=EVIDENCE[code];meta=REGISTRY[code]
    tags=[CONCENTRATIONS[row['concentration']]]
    if meta['audience']:tags.append(AUDIENCES[meta['audience']])
    tags += [FAMILY_AR.get(f,f) for f in meta['families'][:2]]
    return ('<a class="record" href="/catalog/'+code+'"><bdi dir="ltr">'+code+'</bdi><span>'
            +html.escape(' · '.join(tags))+'</span></a>')

def filter_select(field, label_text, options, selected):
    opts=['<option value="">الكل</option>']
    for value,display in options:
        opts.append('<option value="'+html.escape(value,quote=True)+'"'+(' selected' if value==selected else '')+'>'
                    +html.escape(display)+'</option>')
    return '<label>'+label_text+'<select name="'+field+'">'+''.join(opts)+'</select></label>'

@app.get('/catalog',response_class=HTMLResponse,include_in_schema=False)
def catalog_page(q: str='', audience: str='', family: str=''):
    raw=q.strip()[:120]
    term=normalize(raw)
    if term.isascii() and term.isdigit() and len(term)<=4:term=term.zfill(4)
    rows=[]
    for code,row in sorted(EVIDENCE.items()):
        meta=REGISTRY[code]
        if audience and (meta['audience'] or 'unknown')!=audience:continue
        if family and family not in meta['families']:continue
        if term:
            if term.isdigit():
                if term!=code:continue
            else:
                words=[CONCENTRATIONS[row['concentration']],AUDIENCES.get(meta['audience'],''),*[FAMILY_AR.get(f,f) for f in meta['families']]]
                words+= [evidence_label(c) for c in row['claims']]
                if not any(term in normalize(w) for w in words if w):continue
        rows.append(code)
    bits=['<p class="lede">125 رمزًا معتمدًا بين <span dir="ltr">0001</span> و<span dir="ltr">0164</span>. اختر رمزًا لعرض سجله.</p>',
          '<form class="filters" action="/catalog" method="get"><label>بحث بالرمز أو الوصف<input name="q" maxlength="120" value="'+html.escape(raw,quote=True)+'" placeholder="مثلاً 0145 أو زعفران"></label>',
          filter_select('audience','التصنيف الموثق',list(AUDIENCES.items())+[('unknown','غير محدد')],audience),
          filter_select('family','العائلة العطرية',sorted(FAMILY_AR.items(),key=lambda kv:kv[1]),family),
          '<button type="submit">بحث</button></form>']
    if term or audience or family:
        bits.append('<div class="actions"><strong>'+str(len(rows))+' من 125</strong><a href="/catalog">عرض جميع الرموز</a></div>')
    if rows:bits.append('<section class="records" aria-label="سجلات العطور">'+''.join(record_card(c) for c in rows)+'</section>')
    else:bits.append('<p class="panel" role="status">لم أجد سجلًا بهذه المواصفات. غيّر البحث أو اعرض جميع الرموز.</p>')
    return page_shell('سجل الكتالوج',''.join(bits),wide=True)

@app.get('/catalog/{code}',response_class=HTMLResponse,include_in_schema=False)
def catalog_detail(code: str):
    if code not in EVIDENCE:
        return page_shell('السجل غير موجود','<p>هذا الرمز خارج القائمة المعتمدة.</p><a href="/catalog">العودة إلى سجل الكتالوج</a>',status=404)
    r=EVIDENCE[code];m=REGISTRY[code]
    families='، '.join(FAMILY_AR.get(f,f) for f in m['families']) or 'غير موثّقة في السجل'
    audience=(AUDIENCES[m['audience']]+' بحسب التسمية الرسمية للإصدار') if m['audience'] else 'غير محدد في التسمية المعتمدة'
    bits=['<p><a href="/catalog">جميع الرموز</a></p><dl class="facts">']
    for key,val in [('التركيز',CONCENTRATIONS[r['concentration']]),('التصنيف',audience),('العائلة العطرية',families)]:
        bits.append('<div><dt>'+key+'</dt><dd>'+html.escape(val)+'</dd></div>')
    bits.append('</dl>')
    for kind,title in [(False,'النوتات والأكوردات'),(True,'الاستخدام الموثّق')]:
        groups=defaultdict(list)
        for claim in r['claims']:
            if (claim['attribute']=='context')!=kind:continue
            val=evidence_label(claim)
            if val and val not in groups[claim['channel']]:groups[claim['channel']].append(val)
        bits.append('<section class="panel"><h2>'+title+'</h2>')
        for channel,values in groups.items():
            bits.append('<p><strong>'+CHANNELS[channel]+'</strong><br>'+html.escape('، '.join(values))+'</p>')
        if not groups:
            archival=r['classification'] in (('attributed_use_only','both_documentary_axes') if kind else ('taste_only','both_documentary_axes'))
            bits.append('<p>'+('توجد مادة وصفية محفوظة؛ لم تُعتمد منها شروط تفصيلية قابلة للمطابقة هنا.' if archival else 'لا يتوفر وصف موثّق لهذا البند في السجل المعروض.')+'</p>')
        bits.append('</section>')
    return page_shell('سجل العطر '+code,''.join(bits))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app,host='0.0.0.0',port=int(os.getenv('PORT','8000')))

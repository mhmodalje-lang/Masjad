"""
Router: prayer
"""
from fastapi import APIRouter, HTTPException, Query, Depends, BackgroundTasks
from deps import db, get_user, logger, security, verify_jwt, create_jwt, hash_password, check_password, ADMIN_EMAILS, STRIPE_API_KEY, EMERGENT_LLM_KEY, haversine, query_overpass, clean_time, OVERPASS_ENDPOINTS, VAPID_PUBLIC_KEY, VAPID_PRIVATE_KEY, VAPID_EMAIL, FIREBASE_PROJECT_ID, RESEND_API_KEY, GEMINI_API_KEY
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, date, timedelta
import uuid
import random
import math
import re
import httpx
import os
import json as json_module
import asyncio

router = APIRouter(tags=["Prayer & Mosques"])

class PushSubscription(BaseModel):
    endpoint: str
    p256dh: str
    auth: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    method: Optional[int] = 3
    school: Optional[int] = 0
    timezone: Optional[str] = "Asia/Riyadh"
    user_id: Optional[str] = None

class MosqueTimesRequest(BaseModel):
    mosqueName: str
    latitude: float
    longitude: float
    method: int = 3
    school: int = 0
    mosqueUuid: Optional[str] = None

class DhikrAIRequest(BaseModel):
    time_of_day: str = "morning"
    occasion: Optional[str] = None
    language: str = "ar"
    count: int = 5

@router.get("/prayer-times")
async def prayer_times(lat: float = Query(...), lon: float = Query(...), method: int = Query(4), school: int = Query(0)):
    """Get prayer times using Aladhan API"""
    try:
        today = date.today()
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get(f"https://api.aladhan.com/v1/timings/{today.day}-{today.month}-{today.year}",
                params={"latitude": lat, "longitude": lon, "method": method, "school": school})
            r.raise_for_status()
            data = r.json()["data"]

        timings = data["timings"]
        hijri = data["date"]["hijri"]
        
        return {
            "success": True,
            "source": "aladhan",
            "times": {
                "fajr": clean_time(timings["Fajr"]),
                "sunrise": clean_time(timings["Sunrise"]),
                "dhuhr": clean_time(timings["Dhuhr"]),
                "asr": clean_time(timings["Asr"]),
                "maghrib": clean_time(timings["Maghrib"]),
                "isha": clean_time(timings["Isha"]),
                "midnight": clean_time(timings.get("Midnight", "")),
            },
            "hijri": {
                "date": f"{hijri['day']} {hijri['month']['ar']} {hijri['year']} هـ",
                "day": hijri["day"],
                "month_ar": hijri["month"]["ar"],
                "month_en": hijri["month"]["en"],
                "month_num": hijri["month"]["number"],
                "year": hijri["year"],
            },
            "meta": data.get("meta", {})
        }
    except Exception as e:
        raise HTTPException(500, f"خطأ في جلب أوقات الصلاة: {str(e)}")

# ==================== MOSQUE SEARCH ====================
@router.get("/mosques/search")
async def search_mosques(
    lat: float = Query(...), lon: float = Query(...),
    radius: int = Query(5000), query: Optional[str] = Query(None)
):
    """Search mosques using Mawaqit API first, fallback to Overpass"""
    
    # Try Mawaqit first (has real prayer times!)
    try:
        async with httpx.AsyncClient(timeout=20) as c:
            params = {"lat": lat, "lon": lon, "radius": radius}
            if query:
                params["word"] = query
            r = await c.get("https://mawaqit.net/api/2.0/mosque/search", params=params)
            if r.status_code == 200:
                mosques_raw = r.json()
                mosques = []
                for m in mosques_raw:
                    mosque = {
                        "osm_id": m.get("uuid", str(uuid.uuid4())),
                        "mawaqit_uuid": m.get("uuid"),
                        "name": m.get("name", ""),
                        "address": m.get("localisation", ""),
                        "latitude": float(m.get("latitude", 0)),
                        "longitude": float(m.get("longitude", 0)),
                        "websiteUrl": m.get("site"),
                        "phone": m.get("phone"),
                        "image": m.get("image"),
                        "hasAutoSync": True,
                        "hasMawaqit": True,
                        "times": m.get("times", []),
                        "iqama": m.get("iqama", []),
                        "jumua": m.get("jumua"),
                        "facilities": {
                            "womenSpace": m.get("womenSpace", False),
                            "parking": m.get("parking", False),
                            "ablutions": m.get("ablutions", False),
                            "handicapAccessibility": m.get("handicapAccessibility", False),
                            "childrenCourses": m.get("childrenCourses", False),
                            "adultCourses": m.get("adultCourses", False),
                        },
                        "_dist": float(m.get("proximity", 9999)) / 1000,
                    }
                    mosques.append(mosque)
                
                mosques.sort(key=lambda x: x["_dist"])
                return {"mosques": mosques[:50], "count": len(mosques), "source": "mawaqit"}
    except Exception as e:
        logger.warning(f"Mawaqit search failed: {e}")

    # Fallback to Overpass API
    try:
        if query:
            overpass_q = f'[out:json][timeout:20];(node["amenity"="place_of_worship"]["religion"="muslim"]["name"~"{query}",i](around:{radius},{lat},{lon});way["amenity"="place_of_worship"]["religion"="muslim"]["name"~"{query}",i](around:{radius},{lat},{lon}););out center body;'
        else:
            overpass_q = f'[out:json][timeout:20];(node["amenity"="place_of_worship"]["religion"="muslim"](around:{radius},{lat},{lon});way["amenity"="place_of_worship"]["religion"="muslim"](around:{radius},{lat},{lon}););out center body;'
        
        data = await query_overpass(overpass_q)
        mosques = []
        for el in (data or {}).get("elements", []):
            tags = el.get("tags", {})
            name = tags.get("name") or tags.get("name:ar")
            if not name:
                continue
            e_lat = el.get("lat") or el.get("center", {}).get("lat", 0)
            e_lon = el.get("lon") or el.get("center", {}).get("lon", 0)
            mosques.append({
                "osm_id": str(el.get("id")),
                "name": name,
                "address": tags.get("addr:street", "") + " " + tags.get("addr:city", ""),
                "latitude": e_lat, "longitude": e_lon,
                "hasAutoSync": False, "hasMawaqit": False,
                "_dist": haversine(lat, lon, e_lat, e_lon)
            })
        mosques.sort(key=lambda x: x["_dist"])
        return {"mosques": mosques[:50], "count": len(mosques), "source": "openstreetmap"}
    except Exception as e:
        raise HTTPException(500, f"خطأ في البحث: {str(e)}")

@router.post("/mosques/prayer-times")
async def mosque_times(req: MosqueTimesRequest):
    """Get mosque prayer times from Mawaqit or Aladhan"""
    
    # If we have UUID, use Mawaqit directly
    if req.mosqueUuid:
        try:
            async with httpx.AsyncClient(timeout=15) as c:
                r = await c.get(f"https://mawaqit.net/api/2.0/mosque/{req.mosqueUuid}/prayer-times")
                if r.status_code == 200:
                    data = r.json()
                    today_day = date.today().day
                    times_raw = data.get("times", {})
                    
                    if isinstance(times_raw, dict):
                        today_times = times_raw.get(str(today_day))
                    elif isinstance(times_raw, list) and len(times_raw) >= today_day:
                        today_times = times_raw[today_day - 1]
                    else:
                        today_times = None
                    
                    if today_times and len(today_times) >= 5:
                        keys = ["fajr", "sunrise", "dhuhr", "asr", "maghrib", "isha"]
                        times_map = {keys[i]: today_times[i] for i in range(min(len(keys), len(today_times)))}
                        return {
                            "success": True, "source": "mawaqit",
                            "times": times_map,
                            "jumua": data.get("jumua"),
                            "iqama": data.get("iqama"),
                        }
        except Exception as e:
            logger.warning(f"Mawaqit times error: {e}")

    # Try Mawaqit search by name
    try:
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get("https://mawaqit.net/api/2.0/mosque/search",
                params={"lat": req.latitude, "lon": req.longitude, "word": req.mosqueName[:20]})
            if r.status_code == 200:
                mosques = r.json()
                for m in mosques[:3]:
                    m_lat, m_lon = float(m.get("latitude", 0)), float(m.get("longitude", 0))
                    if haversine(req.latitude, req.longitude, m_lat, m_lon) < 0.5:
                        times = m.get("times", [])
                        if len(times) >= 5:
                            keys = ["fajr", "sunrise", "dhuhr", "asr", "maghrib", "isha"]
                            return {
                                "success": True, "source": "mawaqit",
                                "times": {keys[i]: times[i] for i in range(min(6, len(times)))},
                                "jumua": m.get("jumua"),
                                "iqama": m.get("iqama"),
                            }
    except Exception:
        pass

    # Fallback to Aladhan
    try:
        today = date.today()
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get(f"https://api.aladhan.com/v1/timings/{today.day}-{today.month}-{today.year}",
                params={"latitude": req.latitude, "longitude": req.longitude, "method": req.method, "school": req.school})
            r.raise_for_status()
            t = r.json()["data"]["timings"]
            return {
                "success": True, "source": "calculated",
                "times": {
                    "fajr": clean_time(t["Fajr"]), "sunrise": clean_time(t["Sunrise"]),
                    "dhuhr": clean_time(t["Dhuhr"]), "asr": clean_time(t["Asr"]),
                    "maghrib": clean_time(t["Maghrib"]), "isha": clean_time(t["Isha"]),
                }
            }
    except Exception as e:
        raise HTTPException(500, str(e))

# ==================== PUSH NOTIFICATIONS ====================
@router.get("/push/vapid-key")
async def get_vapid_key():
    return {"publicKey": VAPID_PUBLIC_KEY}

@router.post("/push/subscribe")
async def subscribe_push(sub: PushSubscription, user: dict = Depends(get_user)):
    """Save push subscription to DB"""
    doc = {
        "id": str(uuid.uuid4()),
        "endpoint": sub.endpoint,
        "p256dh": sub.p256dh,
        "auth": sub.auth,
        "latitude": sub.latitude,
        "longitude": sub.longitude,
        "method": sub.method,
        "school": sub.school,
        "timezone": sub.timezone,
        "user_id": user["id"] if user else sub.user_id,
        "created_at": datetime.utcnow().isoformat(),
        "active": True,
    }
    await db.push_subscriptions.update_one(
        {"endpoint": sub.endpoint}, {"$set": doc}, upsert=True
    )
    return {"success": True, "message": "تم تسجيل الإشعارات بنجاح"}

@router.post("/push/test")
async def test_push(data: dict, user: dict = Depends(get_user)):
    """Send a test push notification"""
    endpoint = data.get("endpoint")
    if not endpoint:
        raise HTTPException(400, "endpoint مطلوب")
    
    sub = await db.push_subscriptions.find_one({"endpoint": endpoint})
    if not sub:
        raise HTTPException(404, "الاشتراك غير موجود")
    
    result = await send_push_notification(sub, {
        "title": "أذان وحكاية 🕌",
        "body": "تم تفعيل الإشعارات بنجاح!",
        "icon": "/pwa-icon-192.png",
        "badge": "/pwa-icon-192.png",
        "tag": "test",
    })
    return {"success": result}

async def send_push_notification(sub: dict, payload: dict) -> bool:
    """Send a web push notification using pywebpush"""
    try:
        from pywebpush import webpush, WebPushException
        webpush(
            subscription_info={
                "endpoint": sub["endpoint"],
                "keys": {"p256dh": sub["p256dh"], "auth": sub["auth"]},
            },
            data=json_module.dumps(payload),
            vapid_private_key=VAPID_PRIVATE_KEY,
            vapid_claims={"sub": VAPID_EMAIL},
        )
        return True
    except Exception as e:
        logger.error(f"Push failed: {e}")
        return False

@router.post("/push/send-prayer")
async def send_prayer_notifications(data: dict):
    """Send prayer time notifications to all subscribed users"""
    prayer_name = data.get("prayer", "")
    prayer_ar = {"fajr": "الفجر", "dhuhr": "الظهر", "asr": "العصر", "maghrib": "المغرب", "isha": "العشاء"}.get(prayer_name, prayer_name)
    
    subs = await db.push_subscriptions.find({"active": True}).to_list(None)
    sent = 0
    for sub in subs:
        payload = {
            "title": f"🕌 حان وقت صلاة {prayer_ar}",
            "body": "استعد للصلاة، حي على الصلاة، حي على الفلاح",
            "icon": "/pwa-icon-192.png",
            "badge": "/pwa-icon-192.png",
            "tag": f"prayer-{prayer_name}",
            "requireInteraction": True,
            "vibrate": [200, 100, 200, 100, 200],
            "actions": [{"action": "open", "title": "فتح التطبيق"}],
            "data": {"prayer": prayer_name, "type": "athan"}
        }
        if await send_push_notification(sub, payload):
            sent += 1
    
    return {"success": True, "sent": sent, "total": len(subs)}

@router.get("/hijri-date")
async def hijri_date(lat: float = Query(24.68), lon: float = Query(46.72)):
    try:
        today = date.today()
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get(f"https://api.aladhan.com/v1/timings/{today.day}-{today.month}-{today.year}",
                params={"latitude": lat, "longitude": lon, "method": 4})
            r.raise_for_status()
            hijri = r.json()["data"]["date"]["hijri"]
        return {
            "hijriDate": f"{hijri['day']} {hijri['month']['ar']} {hijri['year']} هـ",
            "day": hijri["day"], "month_ar": hijri["month"]["ar"],
            "month_en": hijri["month"]["en"], "year": hijri["year"],
            "month_num": hijri["month"]["number"],
        }
    except Exception as e:
        raise HTTPException(500, str(e))

# ==================== DAILY HADITH ====================
STATIC_HADITHS = [
    {"text": "إِنَّمَا الأَعْمَالُ بِالنِّيَّاتِ، وَإِنَّمَا لِكُلِّ امْرِئٍ مَا نَوَى", "narrator": "عمر بن الخطاب", "source": "صحيح البخاري", "number": "1"},
    {"text": "مَنْ كَانَ يُؤْمِنُ بِاللهِ وَالْيَوْمِ الآخِرِ فَلْيَقُلْ خَيْرًا أَوْ لِيَصْمُتْ", "narrator": "أبو هريرة", "source": "صحيح البخاري ومسلم", "number": "15"},
    {"text": "لا يُؤْمِنُ أَحَدُكُمْ حَتَّى يُحِبَّ لِأَخِيهِ مَا يُحِبُّ لِنَفْسِهِ", "narrator": "أنس بن مالك", "source": "صحيح البخاري ومسلم", "number": "13"},
    {"text": "الْمُسْلِمُ مَنْ سَلِمَ الْمُسْلِمُونَ مِنْ لِسَانِهِ وَيَدِهِ", "narrator": "عبد الله بن عمرو", "source": "صحيح البخاري", "number": "10"},
    {"text": "مَنْ سَلَكَ طَرِيقًا يَلْتَمِسُ فِيهِ عِلْمًا سَهَّلَ اللهُ لَهُ بِهِ طَرِيقًا إِلَى الجَنَّةِ", "narrator": "أبو هريرة", "source": "صحيح مسلم", "number": "2699"},
    {"text": "إِنَّ اللهَ لا يَنْظُرُ إِلَى صُوَرِكُمْ وَأَمْوَالِكُمْ، وَلَكِنْ يَنْظُرُ إِلَى قُلُوبِكُمْ وَأَعْمَالِكُمْ", "narrator": "أبو هريرة", "source": "صحيح مسلم", "number": "2564"},
    {"text": "الطُّهُورُ شَطْرُ الإِيمَانِ، وَالحَمْدُ لِلَّهِ تَمْلأُ المِيزَانَ", "narrator": "أبو مالك الأشعري", "source": "صحيح مسلم", "number": "223"},
    {"text": "خَيْرُكُمْ مَنْ تَعَلَّمَ القُرْآنَ وَعَلَّمَهُ", "narrator": "عثمان بن عفان", "source": "صحيح البخاري", "number": "5027"},
    {"text": "أَحَبُّ الأَعْمَالِ إِلَى اللهِ أَدْوَمُهَا وَإِنْ قَلَّ", "narrator": "عائشة", "source": "صحيح البخاري ومسلم", "number": "6464"},
    {"text": "الدُّنْيَا سِجْنُ الْمُؤْمِنِ وَجَنَّةُ الْكَافِرِ", "narrator": "أبو هريرة", "source": "صحيح مسلم", "number": "2956"},
    {"text": "مَنْ صَلَّى عَلَيَّ صَلاةً صَلَّى اللهُ عَلَيْهِ بِهَا عَشْرًا", "narrator": "أبو هريرة", "source": "صحيح مسلم", "number": "408"},
    {"text": "الصَّلَوَاتُ الْخَمْسُ وَالْجُمُعَةُ إِلَى الْجُمُعَةِ كَفَّارَاتٌ لِمَا بَيْنَهُنَّ مَا اجْتُنِبَتِ الْكَبَائِرُ", "narrator": "أبو هريرة", "source": "صحيح مسلم", "number": "233"},
    {"text": "إِذَا مَاتَ الإِنْسَانُ انْقَطَعَ عَمَلُهُ إِلا مِنْ ثَلاثٍ: صَدَقَةٍ جَارِيَةٍ، أَوْ عِلْمٍ يُنْتَفَعُ بِهِ، أَوْ وَلَدٍ صَالِحٍ يَدْعُو لَهُ", "narrator": "أبو هريرة", "source": "صحيح مسلم", "number": "1631"},
    {"text": "مَا نَقَصَتْ صَدَقَةٌ مِنْ مَالٍ وَمَا زَادَ اللهُ عَبْدًا بِعَفْوٍ إِلا عِزًّا", "narrator": "أبو هريرة", "source": "صحيح مسلم", "number": "2588"},
    {"text": "كَلِمَتَانِ خَفِيفَتَانِ عَلَى اللِّسَانِ ثَقِيلَتَانِ فِي المِيزَانِ: سُبْحَانَ اللهِ وَبِحَمْدِهِ سُبْحَانَ اللهِ العَظِيمِ", "narrator": "أبو هريرة", "source": "صحيح البخاري ومسلم", "number": "6406"},
    {"text": "لَا تَحَاسَدُوا وَلَا تَنَاجَشُوا وَلَا تَبَاغَضُوا وَلَا تَدَابَرُوا وَكُونُوا عِبَادَ اللهِ إِخْوَانًا", "narrator": "أبو هريرة", "source": "صحيح مسلم", "number": "2564b"},
    {"text": "اقْرَأُوا الْقُرْآنَ فَإِنَّهُ يَأْتِي يَوْمَ الْقِيَامَةِ شَفِيعًا لِأَصْحَابِهِ", "narrator": "أبو أمامة", "source": "صحيح مسلم", "number": "804"},
    {"text": "مَنْ يُرِدِ اللهُ بِهِ خَيْرًا يُفَقِّهْهُ فِي الدِّينِ", "narrator": "معاوية بن أبي سفيان", "source": "صحيح البخاري", "number": "71"},
    {"text": "الْمُؤْمِنُ الْقَوِيُّ خَيْرٌ وَأَحَبُّ إِلَى اللهِ مِنَ الْمُؤْمِنِ الضَّعِيفِ وَفِي كُلٍّ خَيْرٌ", "narrator": "أبو هريرة", "source": "صحيح مسلم", "number": "2664"},
    {"text": "بُنِيَ الإِسْلامُ عَلَى خَمْسٍ: شَهَادَةِ أَنْ لا إِلَهَ إِلا اللهُ وَأَنَّ مُحَمَّدًا رَسُولُ اللهِ وَإِقَامِ الصَّلاةِ وَإِيتَاءِ الزَّكَاةِ وَصَوْمِ رَمَضَانَ وَحَجِّ الْبَيْتِ", "narrator": "ابن عمر", "source": "صحيح البخاري ومسلم", "number": "8"},
    {"text": "مَثَلُ الَّذِي يَذْكُرُ رَبَّهُ وَالَّذِي لا يَذْكُرُ رَبَّهُ مَثَلُ الْحَيِّ وَالْمَيِّتِ", "narrator": "أبو موسى الأشعري", "source": "صحيح البخاري", "number": "6407"},
]

HADITH_TRANSLATIONS = {
    "1": {
        "en": {"text": "Actions are judged by intentions, and everyone will be rewarded according to what they intended.", "narrator": "Umar ibn Al-Khattab", "source": "Sahih Al-Bukhari"},
        "de": {"text": "Die Taten werden nach den Absichten beurteilt, und jeder wird nach dem belohnt, was er beabsichtigt hat.", "narrator": "Umar ibn Al-Khattab", "source": "Sahih Al-Bukhari"},
        "fr": {"text": "Les actes ne valent que par leurs intentions, et chacun sera rétribué selon ce qu'il a eu l'intention de faire.", "narrator": "Omar ibn Al-Khattab", "source": "Sahih Al-Boukhari"},
        "tr": {"text": "Ameller niyetlere göredir ve herkes niyet ettiğinin karşılığını alacaktır.", "narrator": "Ömer ibn Hattab", "source": "Sahih Buhari"},
        "ru": {"text": "Дела оцениваются по намерениям, и каждый получит то, что он намеревался.", "narrator": "Умар ибн аль-Хаттаб", "source": "Сахих аль-Бухари"},
        "sv": {"text": "Handlingar bedöms efter avsikter, och var och en belönas efter sin avsikt.", "narrator": "Umar ibn Al-Khattab", "source": "Sahih Al-Bukhari"},
        "nl": {"text": "Daden worden beoordeeld op intenties, en iedereen wordt beloond naar wat hij bedoelde.", "narrator": "Umar ibn Al-Khattab", "source": "Sahih Al-Bukhari"},
        "el": {"text": "Οι πράξεις κρίνονται από τις προθέσεις και καθένας ανταμείβεται σύμφωνα με αυτό που σκόπευε.", "narrator": "Ουμάρ ιμπν Αλ-Χαττάμπ", "source": "Σαχίχ Αλ-Μπουχάρι"},
    },
    "15": {
        "en": {"text": "Whoever believes in Allah and the Last Day, let him speak good or remain silent.", "narrator": "Abu Hurairah", "source": "Sahih Al-Bukhari & Muslim"},
        "de": {"text": "Wer an Allah und den Jüngsten Tag glaubt, soll Gutes sprechen oder schweigen.", "narrator": "Abu Hurairah", "source": "Sahih Al-Bukhari & Muslim"},
        "fr": {"text": "Quiconque croit en Allah et au Jour dernier, qu'il dise du bien ou qu'il se taise.", "narrator": "Abu Hurairah", "source": "Sahih Al-Boukhari & Mouslim"},
        "tr": {"text": "Allah'a ve ahiret gününe iman eden kimse ya hayır söylesin ya da sussun.", "narrator": "Ebu Hureyre", "source": "Sahih Buhari & Müslim"},
        "ru": {"text": "Кто верит в Аллаха и Судный день, пусть говорит благое или молчит.", "narrator": "Абу Хурайра", "source": "Сахих аль-Бухари и Муслим"},
        "sv": {"text": "Den som tror på Allah och den Yttersta dagen, låt honom tala gott eller vara tyst.", "narrator": "Abu Hurairah", "source": "Sahih Al-Bukhari & Muslim"},
        "nl": {"text": "Wie in Allah en de Laatste Dag gelooft, laat hem goed spreken of zwijgen.", "narrator": "Abu Hurairah", "source": "Sahih Al-Bukhari & Muslim"},
        "el": {"text": "Όποιος πιστεύει στον Αλλάχ και την Τελευταία Ημέρα, ας λέει καλά ή ας σιωπά.", "narrator": "Αμπού Χουράιρα", "source": "Σαχίχ Αλ-Μπουχάρι & Μούσλιμ"},
    },
    "13": {
        "en": {"text": "None of you truly believes until he loves for his brother what he loves for himself.", "narrator": "Anas ibn Malik", "source": "Sahih Al-Bukhari & Muslim"},
        "de": {"text": "Keiner von euch glaubt wahrhaft, bis er für seinen Bruder wünscht, was er für sich selbst wünscht.", "narrator": "Anas ibn Malik", "source": "Sahih Al-Bukhari & Muslim"},
        "fr": {"text": "Aucun d'entre vous ne croit véritablement tant qu'il n'aime pas pour son frère ce qu'il aime pour lui-même.", "narrator": "Anas ibn Malik", "source": "Sahih Al-Boukhari & Mouslim"},
        "tr": {"text": "Sizden biriniz kendisi için istediğini kardeşi için de istemedikçe gerçek manada iman etmiş olmaz.", "narrator": "Enes bin Malik", "source": "Sahih Buhari & Müslim"},
        "ru": {"text": "Никто из вас не уверует по-настоящему, пока не полюбит для своего брата то, что любит для себя.", "narrator": "Анас ибн Малик", "source": "Сахих аль-Бухари и Муслим"},
        "sv": {"text": "Ingen av er tror verkligen förrän han önskar sin broder det han önskar sig själv.", "narrator": "Anas ibn Malik", "source": "Sahih Al-Bukhari & Muslim"},
        "nl": {"text": "Niemand van jullie gelooft werkelijk totdat hij voor zijn broeder wenst wat hij voor zichzelf wenst.", "narrator": "Anas ibn Malik", "source": "Sahih Al-Bukhari & Muslim"},
        "el": {"text": "Κανείς από εσάς δεν πιστεύει πραγματικά μέχρι να αγαπήσει για τον αδελφό του αυτό που αγαπά για τον εαυτό του.", "narrator": "Άνας ιμπν Μάλικ", "source": "Σαχίχ Αλ-Μπουχάρι & Μούσλιμ"},
    },
    "10": {
        "en": {"text": "A Muslim is one from whose tongue and hands other Muslims are safe.", "narrator": "Abdullah ibn Amr", "source": "Sahih Al-Bukhari"},
        "sv": {"text": "En muslim är den vars tunga och händer andra muslimer är trygga från.", "narrator": "Abdullah ibn Amr", "source": "Sahih Al-Bukhari"},
        "nl": {"text": "Een moslim is degene voor wiens tong en handen andere moslims veilig zijn.", "narrator": "Abdullah ibn Amr", "source": "Sahih Al-Bukhari"},
        "el": {"text": "Μουσουλμάνος είναι αυτός από τη γλώσσα και τα χέρια του οποίου οι άλλοι μουσουλμάνοι είναι ασφαλείς.", "narrator": "Αμπντουλλάχ ιμπν Αμρ", "source": "Σαχίχ Αλ-Μπουχάρι"},
        "de": {"text": "Ein Muslim ist derjenige, vor dessen Zunge und Hand andere Muslime sicher sind.", "narrator": "Abdullah ibn Amr", "source": "Sahih Al-Bukhari"},
        "fr": {"text": "Le musulman est celui dont la langue et les mains ne nuisent pas aux autres musulmans.", "narrator": "Abdullah ibn Amr", "source": "Sahih Al-Boukhari"},
        "tr": {"text": "Müslüman, dilinden ve elinden diğer Müslümanların güvende olduğu kimsedir.", "narrator": "Abdullah bin Amr", "source": "Sahih Buhari"},
        "ru": {"text": "Мусульманин — тот, от чьего языка и рук другие мусульмане в безопасности.", "narrator": "Абдуллах ибн Амр", "source": "Сахих аль-Бухари"},
    },
    "2699": {
        "en": {"text": "Whoever takes a path seeking knowledge, Allah will make easy for him a path to Paradise.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"},
        "sv": {"text": "Den som tar en väg för att söka kunskap, Allah underlättar för honom vägen till Paradiset.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"},
        "nl": {"text": "Wie een pad bewandelt op zoek naar kennis, Allah maakt het pad naar het Paradijs gemakkelijk.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"},
        "el": {"text": "Όποιος ακολουθεί ένα μονοπάτι αναζητώντας γνώση, ο Αλλάχ θα του διευκολύνει το μονοπάτι προς τον Παράδεισο.", "narrator": "Αμπού Χουράιρα", "source": "Σαχίχ Μούσλιμ"},
        "de": {"text": "Wer einen Weg einschlägt, um Wissen zu suchen, dem erleichtert Allah den Weg zum Paradies.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"},
        "fr": {"text": "Quiconque emprunte un chemin à la recherche de la science, Allah lui facilitera un chemin vers le Paradis.", "narrator": "Abu Hurairah", "source": "Sahih Mouslim"},
        "tr": {"text": "Kim ilim öğrenmek için bir yola çıkarsa, Allah ona cennetin yolunu kolaylaştırır.", "narrator": "Ebu Hureyre", "source": "Sahih Müslim"},
        "ru": {"text": "Кто встал на путь поиска знания, Аллах облегчит ему путь в Рай.", "narrator": "Абу Хурайра", "source": "Сахих Муслим"},
    },
    "2564": {
        "en": {"text": "Allah does not look at your appearance or wealth, but rather He looks at your hearts and deeds.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"},
        "sv": {"text": "Allah ser inte till ert utseende eller er rikedom, utan Han ser till era hjärtan och handlingar.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"},
        "nl": {"text": "Allah kijkt niet naar jullie uiterlijk of rijkdom, maar naar jullie harten en daden.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"},
        "el": {"text": "Ο Αλλάχ δεν κοιτάζει την εμφάνισή σας ή τον πλούτο σας, αλλά κοιτάζει τις καρδιές και τις πράξεις σας.", "narrator": "Αμπού Χουράιρα", "source": "Σαχίχ Μούσλιμ"},
        "de": {"text": "Allah schaut nicht auf euer Aussehen oder Vermögen, sondern auf eure Herzen und Taten.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"},
        "fr": {"text": "Allah ne regarde ni votre apparence ni vos richesses, mais Il regarde vos cœurs et vos actes.", "narrator": "Abu Hurairah", "source": "Sahih Mouslim"},
        "tr": {"text": "Allah sizin dış görünüşünüze ve mallarınıza bakmaz, kalplerinize ve amellerinize bakar.", "narrator": "Ebu Hureyre", "source": "Sahih Müslim"},
        "ru": {"text": "Аллах не смотрит на вашу внешность и богатство, а смотрит на ваши сердца и дела.", "narrator": "Абу Хурайра", "source": "Сахих Муслим"},
    },
    "223": {"en": {"text": "Purification is half of faith, and praise be to Allah fills the scale.", "narrator": "Abu Malik Al-Ash'ari", "source": "Sahih Muslim"}, "sv": {"text": "Rening är halva tron, och lovprisning av Allah fyller vågskålen.", "narrator": "Abu Malik Al-Ash'ari", "source": "Sahih Muslim"}, "nl": {"text": "Reiniging is de helft van het geloof, en lof aan Allah vult de weegschaal.", "narrator": "Abu Malik Al-Ash'ari", "source": "Sahih Muslim"}, "el": {"text": "Η κάθαρση είναι το ήμισυ της πίστης, και η δοξολογία του Αλλάχ γεμίζει τη ζυγαριά.", "narrator": "Αμπού Μάλικ Αλ-Ασ'αρί", "source": "Σαχίχ Μούσλιμ"}, "de": {"text": "Reinigung ist die Hälfte des Glaubens, und Alhamdulillah füllt die Waage.", "narrator": "Abu Malik Al-Ash'ari", "source": "Sahih Muslim"}, "fr": {"text": "La purification est la moitié de la foi, et la louange à Allah remplit la balance.", "narrator": "Abu Malik Al-Ash'ari", "source": "Sahih Mouslim"}, "tr": {"text": "Temizlik imanın yarısıdır ve Allah'a hamd etmek mizanı doldurur.", "narrator": "Ebu Malik el-Eş'arî", "source": "Sahih Müslim"}, "ru": {"text": "Очищение — половина веры, и восхваление Аллаха заполняет весы.", "narrator": "Абу Малик аль-Ашари", "source": "Сахих Муслим"}},
    "5027": {"en": {"text": "The best among you are those who learn the Quran and teach it.", "narrator": "Uthman ibn Affan", "source": "Sahih Al-Bukhari"}, "sv": {"text": "De bästa bland er är de som lär sig Koranen och lär ut den.", "narrator": "Uthman ibn Affan", "source": "Sahih Al-Bukhari"}, "nl": {"text": "De besten onder jullie zijn degenen die de Koran leren en onderwijzen.", "narrator": "Uthman ibn Affan", "source": "Sahih Al-Bukhari"}, "el": {"text": "Οι καλύτεροι μεταξύ σας είναι εκείνοι που μαθαίνουν το Κοράνι και το διδάσκουν.", "narrator": "Ουθμάν ιμπν Αφφάν", "source": "Σαχίχ Αλ-Μπουχάρι"}, "de": {"text": "Die Besten unter euch sind diejenigen, die den Quran lernen und lehren.", "narrator": "Uthman ibn Affan", "source": "Sahih Al-Bukhari"}, "fr": {"text": "Les meilleurs d'entre vous sont ceux qui apprennent le Coran et l'enseignent.", "narrator": "Uthman ibn Affan", "source": "Sahih Al-Boukhari"}, "tr": {"text": "Sizin en hayırlınız Kur'an'ı öğrenen ve öğretendir.", "narrator": "Osman bin Affan", "source": "Sahih Buhari"}, "ru": {"text": "Лучшие среди вас — те, кто изучает Коран и обучает ему.", "narrator": "Усман ибн Аффан", "source": "Сахих аль-Бухари"}},
    "6464": {"en": {"text": "The most beloved of deeds to Allah are the most consistent, even if small.", "narrator": "Aisha", "source": "Sahih Al-Bukhari & Muslim"}, "sv": {"text": "De mest älskade handlingarna hos Allah är de mest regelbundna, även om de är små.", "narrator": "Aisha", "source": "Sahih Al-Bukhari & Muslim"}, "nl": {"text": "De meest geliefde daden bij Allah zijn de meest consistente, zelfs als ze klein zijn.", "narrator": "Aisha", "source": "Sahih Al-Bukhari & Muslim"}, "el": {"text": "Οι πιο αγαπημένες πράξεις στον Αλλάχ είναι οι πιο σταθερές, ακόμα κι αν είναι μικρές.", "narrator": "Αΐσα", "source": "Σαχίχ Αλ-Μπουχάρι & Μούσλιμ"}, "de": {"text": "Die Allah liebsten Taten sind die beständigsten, auch wenn sie klein sind.", "narrator": "Aisha", "source": "Sahih Al-Bukhari & Muslim"}, "fr": {"text": "Les actes les plus aimés d'Allah sont les plus réguliers, même s'ils sont petits.", "narrator": "Aïcha", "source": "Sahih Al-Boukhari & Mouslim"}, "tr": {"text": "Allah'a en sevimli ameller az da olsa devamlı olanlarıdır.", "narrator": "Aişe", "source": "Sahih Buhari & Müslim"}, "ru": {"text": "Самые любимые дела пред Аллахом — самые постоянные, даже если малые.", "narrator": "Аиша", "source": "Сахих аль-Бухари и Муслим"}},
    "2956": {"en": {"text": "This world is a prison for the believer and a paradise for the disbeliever.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "sv": {"text": "Denna värld är ett fängelse för den troende och ett paradis för den otroende.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "nl": {"text": "Deze wereld is een gevangenis voor de gelovige en een paradijs voor de ongelovige.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "el": {"text": "Αυτός ο κόσμος είναι φυλακή για τον πιστό και παράδεισος για τον άπιστο.", "narrator": "Αμπού Χουράιρα", "source": "Σαχίχ Μούσλιμ"}, "de": {"text": "Diese Welt ist ein Gefängnis für den Gläubigen und ein Paradies für den Ungläubigen.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "fr": {"text": "Ce monde est une prison pour le croyant et un paradis pour le mécréant.", "narrator": "Abu Hurairah", "source": "Sahih Mouslim"}, "tr": {"text": "Dünya mümin için zindan, kâfir için cennettir.", "narrator": "Ebu Hureyre", "source": "Sahih Müslim"}, "ru": {"text": "Этот мир — тюрьма для верующего и рай для неверующего.", "narrator": "Абу Хурайра", "source": "Сахих Муслим"}},
    "408": {"en": {"text": "Whoever sends blessings upon me once, Allah will send blessings upon him tenfold.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "sv": {"text": "Den som sänder välsignelser över mig en gång, Allah sänder välsignelser över honom tio gånger.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "nl": {"text": "Wie eenmaal zegeningen over mij uitspreekt, Allah zegent hem tienvoudig.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "el": {"text": "Όποιος στέλνει ευλογίες σε μένα μία φορά, ο Αλλάχ θα του στείλει ευλογίες δεκαπλάσια.", "narrator": "Αμπού Χουράιρα", "source": "Σαχίχ Μούσλιμ"}, "de": {"text": "Wer einmal Segen über mich spricht, dem sendet Allah zehnfach Segen.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "fr": {"text": "Quiconque prie sur moi une fois, Allah priera sur lui dix fois.", "narrator": "Abu Hurairah", "source": "Sahih Mouslim"}, "tr": {"text": "Kim bana bir kez salât ederse, Allah ona on kez salât eder.", "narrator": "Ebu Hureyre", "source": "Sahih Müslim"}, "ru": {"text": "Кто благословит меня один раз, Аллах благословит его десятикратно.", "narrator": "Абу Хурайра", "source": "Сахих Муслим"}},
    "233": {"en": {"text": "The five daily prayers and Friday to Friday are expiation for sins committed between them, as long as major sins are avoided.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "sv": {"text": "De fem dagliga bönerna och fredag till fredag är försoning för synder emellan dem, så länge stora synder undviks.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "nl": {"text": "De vijf dagelijkse gebeden en vrijdag tot vrijdag zijn boetedoening voor zonden ertussen, zolang grote zonden worden vermeden.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "el": {"text": "Οι πέντε καθημερινές προσευχές και Παρασκευή με Παρασκευή είναι εξιλέωση για τις αμαρτίες μεταξύ τους, εφόσον αποφεύγονται οι μεγάλες αμαρτίες.", "narrator": "Αμπού Χουράιρα", "source": "Σαχίχ Μούσλιμ"}, "de": {"text": "Die fünf täglichen Gebete und Freitag zu Freitag sind Sühne für die Sünden dazwischen, solange große Sünden vermieden werden.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "fr": {"text": "Les cinq prières quotidiennes et vendredi en vendredi expient les péchés commis entre elles, tant que les grands péchés sont évités.", "narrator": "Abu Hurairah", "source": "Sahih Mouslim"}, "tr": {"text": "Beş vakit namaz ve cuma namazı aralarındaki günahlara kefârettir, büyük günahlardan kaçınıldığı sürece.", "narrator": "Ebu Hureyre", "source": "Sahih Müslim"}, "ru": {"text": "Пять ежедневных молитв и от пятницы до пятницы — искупление грехов между ними, если избегаются большие грехи.", "narrator": "Абу Хурайра", "source": "Сахих Муслим"}},
    "1631": {"en": {"text": "When a person dies, their deeds end except for three: ongoing charity, beneficial knowledge, or a righteous child who prays for them.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "sv": {"text": "När en person dör upphör hans handlingar utom tre: pågående välgörenhet, nyttig kunskap, eller ett rättfärdigt barn som ber för honom.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "nl": {"text": "Wanneer een persoon sterft, stoppen zijn daden behalve drie: doorlopende liefdadigheid, nuttige kennis, of een rechtschapen kind dat voor hem bidt.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "el": {"text": "Όταν ένας άνθρωπος πεθάνει, οι πράξεις του τελειώνουν εκτός από τρεις: συνεχής ελεημοσύνη, ωφέλιμη γνώση, ή ένα δίκαιο παιδί που προσεύχεται γι' αυτόν.", "narrator": "Αμπού Χουράιρα", "source": "Σαχίχ Μούσλιμ"}, "de": {"text": "Wenn ein Mensch stirbt, enden seine Taten außer dreien: fortlaufende Wohltätigkeit, nützliches Wissen, oder ein rechtschaffenes Kind, das für ihn betet.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "fr": {"text": "Quand une personne meurt, ses actes cessent sauf trois: une charité continue, un savoir utile, ou un enfant pieux qui prie pour elle.", "narrator": "Abu Hurairah", "source": "Sahih Mouslim"}, "tr": {"text": "İnsan öldüğünde ameli kesilir, ancak üçü hariç: sadaka-i câriye, faydalı ilim veya kendisine dua eden hayırlı evlat.", "narrator": "Ebu Hureyre", "source": "Sahih Müslim"}, "ru": {"text": "Когда человек умирает, его дела прекращаются, кроме трёх: непрерывная милостыня, полезное знание, или праведный ребёнок, который молится за него.", "narrator": "Абу Хурайра", "source": "Сахих Муслим"}},
    "2588": {"en": {"text": "Charity does not decrease wealth, and Allah increases a servant in honor through forgiveness.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "sv": {"text": "Välgörenhet minskar inte rikedom, och Allah ökar en tjänares ära genom förlåtelse.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "nl": {"text": "Liefdadigheid vermindert geen rijkdom, en Allah verhoogt een dienaar in eer door vergeving.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "el": {"text": "Η ελεημοσύνη δεν μειώνει τον πλούτο, και ο Αλλάχ αυξάνει έναν δούλο σε τιμή μέσω της συγχώρεσης.", "narrator": "Αμπού Χουράιρα", "source": "Σαχίχ Μούσλιμ"}, "de": {"text": "Wohltätigkeit mindert keinen Reichtum, und Allah erhöht einen Diener an Ehre durch Vergebung.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "fr": {"text": "L'aumône ne diminue pas la richesse, et Allah augmente l'honneur d'un serviteur par le pardon.", "narrator": "Abu Hurairah", "source": "Sahih Mouslim"}, "tr": {"text": "Sadaka malı eksiltmez, Allah affıyla kulunun izzetini artırır.", "narrator": "Ebu Hureyre", "source": "Sahih Müslim"}, "ru": {"text": "Милостыня не уменьшает богатство, и Аллах увеличивает честь раба через прощение.", "narrator": "Абу Хурайра", "source": "Сахих Муслим"}},
    "6406": {"en": {"text": "Two words are light on the tongue, heavy on the scale: SubhanAllah wa bihamdihi, SubhanAllah al-Adheem.", "narrator": "Abu Hurairah", "source": "Sahih Al-Bukhari & Muslim"}, "sv": {"text": "Två ord som är lätta på tungan, tunga på vågskålen: SubhanAllah wa bihamdihi, SubhanAllah al-Adheem.", "narrator": "Abu Hurairah", "source": "Sahih Al-Bukhari & Muslim"}, "nl": {"text": "Twee woorden licht op de tong, zwaar op de weegschaal: SubhanAllah wa bihamdihi, SubhanAllah al-Adheem.", "narrator": "Abu Hurairah", "source": "Sahih Al-Bukhari & Muslim"}, "el": {"text": "Δύο λέξεις ελαφριές στη γλώσσα, βαριές στη ζυγαριά: SubhanAllah wa bihamdihi, SubhanAllah al-Adheem.", "narrator": "Αμπού Χουράιρα", "source": "Σαχίχ Αλ-Μπουχάρι & Μούσλιμ"}, "de": {"text": "Zwei Worte, leicht auf der Zunge, schwer auf der Waage: SubhanAllah wa bihamdihi, SubhanAllah al-Adheem.", "narrator": "Abu Hurairah", "source": "Sahih Al-Bukhari & Muslim"}, "fr": {"text": "Deux mots légers sur la langue, lourds sur la balance: SubhanAllah wa bihamdihi, SubhanAllah al-Adheem.", "narrator": "Abu Hurairah", "source": "Sahih Al-Boukhari & Mouslim"}, "tr": {"text": "İki kelime dilde hafif, terazide ağır: SubhanAllah wa bihamdihi, SubhanAllah al-Adheem.", "narrator": "Ebu Hureyre", "source": "Sahih Buhari & Müslim"}, "ru": {"text": "Два слова легки на языке, тяжелы на весах: SubhanAllah wa bihamdihi, SubhanAllah al-Adheem.", "narrator": "Абу Хурайра", "source": "Сахих аль-Бухари и Муслим"}},
    "2564b": {"en": {"text": "Do not envy one another, do not inflate prices, do not hate one another, do not turn away from one another, and be servants of Allah as brothers.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "sv": {"text": "Avunda inte varandra, höj inte priser, hata inte varandra, vänd inte ryggen åt varandra, och var Allahs tjänare som bröder.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "nl": {"text": "Benijd elkaar niet, verhoog geen prijzen, haat elkaar niet, keer elkaar niet de rug toe, en wees dienaren van Allah als broeders.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "el": {"text": "Μη φθονείτε ο ένας τον άλλο, μην ανεβάζετε τιμές, μη μισείτε ο ένας τον άλλο, μην γυρίζετε την πλάτη ο ένας στον άλλο, και γίνετε δούλοι του Αλλάχ ως αδελφοί.", "narrator": "Αμπού Χουράιρα", "source": "Σαχίχ Μούσλιμ"}, "de": {"text": "Seid nicht neidisch aufeinander, treibt die Preise nicht hoch, hasst einander nicht, wendet euch nicht voneinander ab, und seid Diener Allahs als Brüder.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "fr": {"text": "Ne vous enviez pas, ne gonflez pas les prix, ne vous haïssez pas, ne vous tournez pas le dos, et soyez des serviteurs d'Allah en frères.", "narrator": "Abu Hurairah", "source": "Sahih Mouslim"}, "tr": {"text": "Birbirinize haset etmeyin, fiyatları şişirmeyin, birbirinize buğzetmeyin, birbirinize sırtınızı dönmeyin ve Allah'ın kulları olarak kardeş olun.", "narrator": "Ebu Hureyre", "source": "Sahih Müslim"}, "ru": {"text": "Не завидуйте друг другу, не взвинчивайте цены, не ненавидьте друг друга, не отворачивайтесь друг от друга и будьте рабами Аллаха — братьями.", "narrator": "Абу Хурайра", "source": "Сахих Муслим"}},
    "804": {"en": {"text": "Read the Quran, for it will come as an intercessor for its companions on the Day of Resurrection.", "narrator": "Abu Umamah", "source": "Sahih Muslim"}, "sv": {"text": "Läs Koranen, ty den kommer som förespråkare för sina följeslagare på Uppståndelsens dag.", "narrator": "Abu Umamah", "source": "Sahih Muslim"}, "nl": {"text": "Lees de Koran, want hij zal komen als voorspreker voor zijn metgezellen op de Dag der Opstanding.", "narrator": "Abu Umamah", "source": "Sahih Muslim"}, "el": {"text": "Διαβάστε το Κοράνι, γιατί θα έρθει ως μεσίτης για τους συντρόφους του την Ημέρα της Ανάστασης.", "narrator": "Αμπού Ουμάμα", "source": "Σαχίχ Μούσλιμ"}, "de": {"text": "Lest den Quran, denn er wird am Tag der Auferstehung als Fürsprecher für seine Gefährten kommen.", "narrator": "Abu Umamah", "source": "Sahih Muslim"}, "fr": {"text": "Lisez le Coran, car il viendra comme intercesseur pour ses compagnons le Jour de la Résurrection.", "narrator": "Abu Umamah", "source": "Sahih Mouslim"}, "tr": {"text": "Kur'an okuyun, çünkü kıyamet günü ona sahip olanlara şefaatçi olarak gelecektir.", "narrator": "Ebu Ümame", "source": "Sahih Müslim"}, "ru": {"text": "Читайте Коран, ибо он придёт в День Воскресения как заступник за тех, кто его читал.", "narrator": "Абу Умама", "source": "Сахих Муслим"}},
    "71": {"en": {"text": "When Allah wishes good for someone, He grants him understanding of the religion.", "narrator": "Mu'awiyah ibn Abi Sufyan", "source": "Sahih Al-Bukhari"}, "sv": {"text": "När Allah vill gott för någon, skänker Han honom förståelse av religionen.", "narrator": "Mu'awiyah ibn Abi Sufyan", "source": "Sahih Al-Bukhari"}, "nl": {"text": "Wanneer Allah goed wil voor iemand, schenkt Hij hem begrip van de religie.", "narrator": "Mu'awiyah ibn Abi Sufyan", "source": "Sahih Al-Bukhari"}, "el": {"text": "Όταν ο Αλλάχ θέλει καλό για κάποιον, του χαρίζει κατανόηση της θρησκείας.", "narrator": "Μουαγουίγια ιμπν Αμπί Σουφιάν", "source": "Σαχίχ Αλ-Μπουχάρι"}, "de": {"text": "Wenn Allah jemandem Gutes will, gewährt Er ihm Verständnis der Religion.", "narrator": "Mu'awiyah ibn Abi Sufyan", "source": "Sahih Al-Bukhari"}, "fr": {"text": "Quand Allah veut du bien pour quelqu'un, Il lui accorde la compréhension de la religion.", "narrator": "Mu'awiyah ibn Abi Sufyan", "source": "Sahih Al-Boukhari"}, "tr": {"text": "Allah bir kişiye hayır dilerse, onu dinde fakih kılar.", "narrator": "Muaviye bin Ebu Süfyan", "source": "Sahih Buhari"}, "ru": {"text": "Когда Аллах желает блага кому-то, Он дарует ему понимание религии.", "narrator": "Муавия ибн Абу Суфьян", "source": "Сахих аль-Бухари"}},
    "2664": {"en": {"text": "The strong believer is better and more beloved to Allah than the weak believer, and in each there is good.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "sv": {"text": "Den starke troende är bättre och mer älskad av Allah än den svage troende, och i vardera finns gott.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "nl": {"text": "De sterke gelovige is beter en meer geliefd bij Allah dan de zwakke gelovige, en in elk van beiden is goed.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "el": {"text": "Ο δυνατός πιστός είναι καλύτερος και πιο αγαπητός στον Αλλάχ από τον αδύναμο πιστό, και σε καθέναν υπάρχει καλό.", "narrator": "Αμπού Χουράιρα", "source": "Σαχίχ Μούσλιμ"}, "de": {"text": "Der starke Gläubige ist besser und Allah lieber als der schwache Gläubige, und in jedem ist Gutes.", "narrator": "Abu Hurairah", "source": "Sahih Muslim"}, "fr": {"text": "Le croyant fort est meilleur et plus aimé d'Allah que le croyant faible, et en chacun il y a du bien.", "narrator": "Abu Hurairah", "source": "Sahih Mouslim"}, "tr": {"text": "Kuvvetli mümin Allah'a zayıf müminden daha hayırlı ve daha sevimlidir, her ikisinde de hayır vardır.", "narrator": "Ebu Hureyre", "source": "Sahih Müslim"}, "ru": {"text": "Сильный верующий лучше и любимее Аллахом, чем слабый, и в каждом есть благо.", "narrator": "Абу Хурайра", "source": "Сахих Муслим"}},
    "8": {"en": {"text": "Islam is built upon five pillars: testifying that there is no god but Allah and Muhammad is His Messenger, establishing prayer, paying Zakat, fasting Ramadan, and making pilgrimage to the House.", "narrator": "Ibn Umar", "source": "Sahih Al-Bukhari & Muslim"}, "sv": {"text": "Islam bygger på fem pelare: att vittna att det inte finns någon gud utom Allah och att Muhammad är Hans sändebud, att förrätta bönen, att betala Zakat, att fasta under Ramadan och att vallfärda till Huset.", "narrator": "Ibn Umar", "source": "Sahih Al-Bukhari & Muslim"}, "nl": {"text": "De Islam is gebouwd op vijf zuilen: getuigen dat er geen god is dan Allah en dat Mohammed Zijn Boodschapper is, het gebed verrichten, Zakat betalen, vasten in Ramadan, en bedevaart naar het Huis.", "narrator": "Ibn Umar", "source": "Sahih Al-Bukhari & Muslim"}, "el": {"text": "Το Ισλάμ χτίστηκε πάνω σε πέντε πυλώνες: η μαρτυρία ότι δεν υπάρχει θεός εκτός του Αλλάχ και ο Μουχάμμαντ είναι ο Απεσταλμένος Του, η εκτέλεση της προσευχής, η πληρωμή Ζακάτ, η νηστεία του Ραμαζανιού και το προσκύνημα στο Σπίτι.", "narrator": "Ιμπν Ουμάρ", "source": "Σαχίχ Αλ-Μπουχάρι & Μούσλιμ"}, "de": {"text": "Der Islam basiert auf fünf Säulen: Das Bezeugnis, dass es keinen Gott außer Allah gibt und Muhammad Sein Gesandter ist, das Gebet zu verrichten, die Zakat zu entrichten, im Ramadan zu fasten und die Pilgerfahrt zum Haus zu unternehmen.", "narrator": "Ibn Umar", "source": "Sahih Al-Bukhari & Muslim"}, "fr": {"text": "L'Islam est bâti sur cinq piliers: témoigner qu'il n'y a de dieu qu'Allah et que Muhammad est Son Messager, accomplir la prière, payer la Zakat, jeûner le Ramadan et faire le pèlerinage à la Maison.", "narrator": "Ibn Umar", "source": "Sahih Al-Boukhari & Mouslim"}, "tr": {"text": "İslam beş esas üzerine kurulmuştur: Allah'tan başka ilah olmadığına ve Muhammed'in O'nun Resûlü olduğuna şehadet etmek, namaz kılmak, zekât vermek, Ramazan orucu tutmak ve Kâbe'yi haccetmek.", "narrator": "İbn Ömer", "source": "Sahih Buhari & Müslim"}, "ru": {"text": "Ислам построен на пяти столпах: свидетельство, что нет бога кроме Аллаха и Мухаммад — Его Посланник, совершение молитвы, выплата закята, пост в Рамадан и паломничество к Дому.", "narrator": "Ибн Умар", "source": "Сахих аль-Бухари и Муслим"}},
    "6407": {"en": {"text": "The likeness of the one who remembers his Lord and the one who does not is like the living and the dead.", "narrator": "Abu Musa Al-Ash'ari", "source": "Sahih Al-Bukhari"}, "sv": {"text": "Liknelsen mellan den som minns sin Herre och den som inte gör det är som den levande och den döde.", "narrator": "Abu Musa Al-Ash'ari", "source": "Sahih Al-Bukhari"}, "nl": {"text": "De gelijkenis van degene die zijn Heer gedenkt en degene die dat niet doet is als de levende en de dode.", "narrator": "Abu Musa Al-Ash'ari", "source": "Sahih Al-Bukhari"}, "el": {"text": "Η ομοιότητα αυτού που μνημονεύει τον Κύριό του και αυτού που δεν το κάνει είναι σαν τον ζωντανό και τον νεκρό.", "narrator": "Αμπού Μούσα Αλ-Ασ'αρί", "source": "Σαχίχ Αλ-Μπουχάρι"}, "de": {"text": "Das Gleichnis dessen, der seines Herrn gedenkt, und dessen, der es nicht tut, ist wie das des Lebenden und des Toten.", "narrator": "Abu Musa Al-Ash'ari", "source": "Sahih Al-Bukhari"}, "fr": {"text": "L'exemple de celui qui se souvient de son Seigneur et celui qui ne le fait pas est comme le vivant et le mort.", "narrator": "Abu Musa Al-Ash'ari", "source": "Sahih Al-Boukhari"}, "tr": {"text": "Rabbini zikredenle zikretmeyenin misali, diri ile ölünün misali gibidir.", "narrator": "Ebu Musa el-Eş'arî", "source": "Sahih Buhari"}, "ru": {"text": "Подобие поминающего Господа и не поминающего — как живой и мёртвый.", "narrator": "Абу Муса аль-Ашари", "source": "Сахих аль-Бухари"}},
}

# daily-hadith endpoint moved to quran_hadith.py router

"""
Router: ai
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
import logging

class DhikrAIRequest(BaseModel):
    time_of_day: str = "morning"
    occasion: Optional[str] = None
    language: str = "ar"
    count: int = 5

router = APIRouter(tags=["AI Assistant"])

@router.post("/ai/ask")
async def ai_ask(data: dict, user: dict = Depends(get_user)):
    """AI Islamic assistant. 5 free questions, then requires credits. Max 20/day."""
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    
    question = data.get("question", "").strip()
    session_id = data.get("session_id", str(uuid.uuid4()))
    if not question:
        raise HTTPException(400, "يجب كتابة السؤال")
    
    today = date.today().isoformat()
    
    # Count today's questions
    today_count = await db.ai_questions.count_documents({"user_id": user["id"], "date": today})
    
    if today_count >= 20:
        return {"answer": "", "error": "daily_limit", "message": "وصلت للحد الأقصى (20 سؤال). عُد غداً إن شاء الله.", "remaining": 0}
    
    # Check if needs credits (after 5 free)
    needs_credits = today_count >= 5
    if needs_credits:
        wallet = await db.wallets.find_one({"user_id": user["id"]})
        user_credits = wallet.get("credits", 0) if wallet else 0
        if user_credits < 5:
            return {"answer": "", "error": "no_credits", "message": "انتهت أسئلتك المجانية. شاهد فيديوهات لكسب نقاط أو اشترِ نقاطاً.", "remaining": 0, "credits": user_credits}
        # Deduct 5 credits per question
        await db.wallets.update_one({"user_id": user["id"]}, {"$inc": {"credits": -5}})
    
    # Call GPT-5.2 via emergent integrations
    try:
        from emergentintegrations.llm.chat import LlmChat, UserMessage as LlmUserMessage
        
        system_prompt = """أنت مساعد إسلامي متخصص. تجيب فقط على الأسئلة المتعلقة بالإسلام والشريعة والقرآن والسنة والفقه والعقيدة والسيرة النبوية والأخلاق الإسلامية.
إذا سُئلت عن موضوع غير إسلامي، أجب بلطف: "أنا مختص بالأسئلة الإسلامية فقط. كيف أساعدك في أمور دينك؟"
أجب بالعربية دائماً. كن دقيقاً واذكر المصادر (القرآن، الحديث) كلما أمكن. لا تفتِ بدون دليل شرعي."""
        
        EMERGENT_KEY = os.environ.get("EMERGENT_LLM_KEY", "")
        
        chat = LlmChat(
            api_key=EMERGENT_KEY,
            session_id=f"islamic_assistant_{user['id']}_{session_id}",
            system_message=system_prompt,
        ).with_model("openai", "gpt-5.2")
        
        user_msg = LlmUserMessage(text=question)
        answer = await chat.send_message(user_msg)
        
    except Exception as e:
        logger.error(f"AI error: {e}")
        answer = "عذراً، حدث خطأ في الاتصال بالمساعد. حاول مرة أخرى."
    
    # Save question
    await db.ai_questions.insert_one({
        "user_id": user["id"],
        "session_id": session_id,
        "question": question,
        "answer": answer,
        "date": today,
        "credits_used": 5 if needs_credits else 0,
        "created_at": datetime.utcnow().isoformat(),
    })
    
    remaining = 20 - today_count - 1
    free_remaining = max(0, 5 - today_count - 1)
    
    return {
        "answer": answer,
        "remaining": remaining,
        "free_remaining": free_remaining,
        "credits_used": 5 if needs_credits else 0,
        "session_id": session_id,
    }

@router.get("/ai/history")
async def ai_history(user: dict = Depends(get_user), session_id: str = ""):
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    query = {"user_id": user["id"]}
    if session_id:
        query["session_id"] = session_id
    history = await db.ai_questions.find(query, {"_id": 0}).sort("created_at", -1).to_list(50)
    return {"history": history}


@router.post("/ai/daily-athkar")
async def get_daily_athkar(req: DhikrAIRequest):
    """Generate contextual daily Athkar using Gemini AI"""
    
    prompts = {
        "morning": "أعطني 5 أذكار صباح مختلفة مع فضلها من الكتاب والسنة، بشكل JSON array من objects {text, virtue, count, reference}",
        "evening": "أعطني 5 أذكار مساء مختلفة مع فضلها من الكتاب والسنة، بشكل JSON array من objects {text, virtue, count, reference}",
        "after_prayer": "أعطني 5 أذكار بعد الصلاة مع فضلها، بشكل JSON array من objects {text, virtue, count, reference}",
        "sleep": "أعطني 5 أذكار النوم مع فضلها، بشكل JSON array من objects {text, virtue, count, reference}",
        "general": "أعطني 5 أذكار عامة يومية مع فضلها، بشكل JSON array من objects {text, virtue, count, reference}",
    }
    
    prompt = prompts.get(req.time_of_day, prompts["general"])
    if req.occasion:
        prompt += f". المناسبة: {req.occasion}"
    
    # Try Emergent LLM with Gemini
    if EMERGENT_LLM_KEY:
        try:
            from emergentintegrations.llm.chat import LlmChat, UserMessage
            chat = LlmChat(
                api_key=EMERGENT_LLM_KEY,
                session_id=f"athkar-{req.time_of_day}-{date.today().isoformat()}",
                system_message="أنت عالم إسلامي متخصص في الأذكار والأدعية من الكتاب والسنة. أجب دائماً بـ JSON array صحيح فقط بدون أي نص إضافي."
            ).with_model("gemini", "gemini-2.0-flash")
            
            response = await chat.send_message(UserMessage(text=prompt))
            if response:
                json_match = re.search(r'\[.*\]', response, re.DOTALL)
                if json_match:
                    athkar = json_module.loads(json_match.group())
                    return {"success": True, "source": "gemini", "athkar": athkar, "time_of_day": req.time_of_day}
        except Exception as e:
            logger.warning(f"Emergent Gemini failed: {e}")
    
    # Fallback to static athkar
    return {
        "success": True, "source": "static",
        "time_of_day": req.time_of_day,
        "athkar": get_static_athkar(req.time_of_day)
    }

def get_static_athkar(time_of_day: str) -> list:
    morning = [
        {"text": "أَصْبَحْنَا وَأَصْبَحَ الْمُلْكُ لِلَّهِ وَالْحَمْدُ لِلَّهِ، لَا إِلَهَ إِلَّا اللهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ", "virtue": "يُقال عند الصباح", "count": 1, "reference": "رواه مسلم"},
        {"text": "اللَّهُمَّ بِكَ أَصْبَحْنَا، وَبِكَ أَمْسَيْنَا، وَبِكَ نَحْيَا، وَبِكَ نَمُوتُ وَإِلَيْكَ النُّشُورُ", "virtue": "من أذكار الصباح", "count": 1, "reference": "رواه الترمذي"},
        {"text": "اللَّهُمَّ أَنْتَ رَبِّي لَا إِلَهَ إِلَّا أَنْتَ، خَلَقْتَنِي وَأَنَا عَبْدُكَ، وَأَنَا عَلَى عَهْدِكَ وَوَعْدِكَ مَا اسْتَطَعْتُ", "virtue": "سيد الاستغفار", "count": 1, "reference": "رواه البخاري"},
        {"text": "أَعُوذُ بِكَلِمَاتِ اللهِ التَّامَّاتِ مِنْ شَرِّ مَا خَلَقَ", "virtue": "حماية من الشر", "count": 3, "reference": "رواه مسلم"},
        {"text": "بِسْمِ اللهِ الَّذِي لَا يَضُرُّ مَعَ اسْمِهِ شَيْءٌ فِي الْأَرْضِ وَلَا فِي السَّمَاءِ وَهُوَ السَّمِيعُ الْعَلِيمُ", "virtue": "من قالها 3 مرات لم تضره مصيبة", "count": 3, "reference": "رواه أبو داود والترمذي"},
    ]
    evening = [
        {"text": "أَمْسَيْنَا وَأَمْسَى الْمُلْكُ لِلَّهِ وَالْحَمْدُ لِلَّهِ، لَا إِلَهَ إِلَّا اللهُ وَحْدَهُ لَا شَرِيكَ لَهُ", "virtue": "يُقال عند المساء", "count": 1, "reference": "رواه مسلم"},
        {"text": "اللَّهُمَّ بِكَ أَمْسَيْنَا، وَبِكَ أَصْبَحْنَا، وَبِكَ نَحْيَا، وَبِكَ نَمُوتُ وَإِلَيْكَ الْمَصِيرُ", "virtue": "من أذكار المساء", "count": 1, "reference": "رواه الترمذي"},
        {"text": "اللَّهُمَّ عَافِنِي فِي بَدَنِي، اللَّهُمَّ عَافِنِي فِي سَمْعِي، اللَّهُمَّ عَافِنِي فِي بَصَرِي", "virtue": "طلب العافية", "count": 3, "reference": "رواه أبو داود"},
        {"text": "أَعُوذُ بِكَلِمَاتِ اللهِ التَّامَّاتِ مِنْ شَرِّ مَا خَلَقَ", "virtue": "حماية من الشر", "count": 3, "reference": "رواه مسلم"},
        {"text": "حَسْبُنَا اللهُ وَنِعْمَ الْوَكِيلُ", "virtue": "من قالها صباحاً ومساءً كفاه الله", "count": 7, "reference": "رواه أبو داود"},
    ]
    return evening if "evening" in time_of_day else morning

@router.post("/ai/smart-reminder")
async def smart_reminder(data: dict):
    """Generate smart contextual Islamic reminder"""
    context = data.get("context", {})
    prayer = context.get("nextPrayer", "")
    minutes_left = context.get("minutesLeft", 0)
    
    prompt = f"أعطني تذكير إسلامي قصير (جملة واحدة) مناسب لشخص يبقى {minutes_left} دقيقة قبل صلاة {prayer}. أجب بالعربية فقط."
    
    if EMERGENT_LLM_KEY:
        try:
            from emergentintegrations.llm.chat import LlmChat, UserMessage
            chat = LlmChat(
                api_key=EMERGENT_LLM_KEY,
                session_id=f"reminder-{prayer}-{datetime.now().isoformat()}",
                system_message="أنت مذكّر إسلامي لطيف. أجب بجملة واحدة فقط بالعربية."
            ).with_model("gemini", "gemini-2.0-flash")
            
            response = await chat.send_message(UserMessage(text=prompt))
            if response:
                return {"reminder": response.strip()}
        except Exception as e:
            logger.warning(f"Emergent reminder failed: {e}")
    
    reminders = [
        "تذكر أن الصلاة عماد الدين، استعد لها بالوضوء",
        "قال النبي ﷺ: أبرد بالظهر فإن شدة الحر من فيح جهنم",
        "الصلاة على وقتها من أحب الأعمال إلى الله",
        "لا تؤخر صلاتك، فإن الموت لا يستأذن",
    ]
    import random
    return {"reminder": random.choice(reminders)}

# ==================== HIJRI DATE ====================

@router.get("/ai/daily-dua")
async def get_daily_dua():
    """Get AI-generated daily dua"""
    try:
        from emergentintegrations.llm.chat import LlmChat, UserMessage
        chat = LlmChat(api_key=EMERGENT_LLM_KEY, session_id=f"daily-dua-{date.today().isoformat()}", system_message="أنت عالم إسلامي. أعط أدعية صحيحة. أجب بـ JSON فقط.").with_model("gemini", "gemini-2.0-flash")
        prompt = """اختر دعاء إسلامي صحيح من القرآن أو السنة. أعطني:
1. نص الدعاء بالعربية فقط
2. المصدر (القرآن أو الحديث)

أجب بصيغة JSON فقط:
{"text": "نص الدعاء", "source": "المصدر"}"""
        response = await chat.chat([UserMessage(content=prompt)])
        import re
        match = re.search(r'\{[^}]+\}', response.content)
        if match:
            data = json_module.loads(match.group())
            return {"dua": data}
    except Exception as e:
        logging.error(f"Daily dua error: {e}")
    return {"dua": {"text": "رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الْآخِرَةِ حَسَنَةً وَقِنَا عَذَابَ النَّارِ", "source": "سورة البقرة 201"}}

@router.get("/ai/verse-of-day")
async def get_verse_of_day(language: str = Query("ar")):
    """Get AI-selected verse of the day with translation"""
    try:
        from emergentintegrations.llm.chat import LlmChat, UserMessage
        chat = LlmChat(api_key=EMERGENT_LLM_KEY, session_id=f"verse-of-day-{language}-{date.today().isoformat()}", system_message="أنت عالم قرآن. أعط آيات ملهمة. أجب بـ JSON فقط.").with_model("gemini", "gemini-2.0-flash")
        
        lang_names = {"en": "English", "de": "German", "fr": "French", "ru": "Russian", "tr": "Turkish", "nl": "Dutch", "sv": "Swedish", "el": "Greek"}
        
        if language == "ar":
            prompt = """اختر آية قرآنية ملهمة ومؤثرة. أعطني:
1. نص الآية بالعربية
2. اسم السورة
3. رقم الآية

أجب بصيغة JSON فقط:
{"text": "نص الآية", "surah": "اسم السورة", "ayah": رقم_الآية}"""
        else:
            lang_name = lang_names.get(language, "English")
            prompt = f"""Select an inspiring Quran verse. Give me:
1. The Arabic text of the verse
2. The {lang_name} translation of the verse
3. The Surah name in {lang_name} transliteration (e.g., "At-Talaq", "Al-Baqarah")
4. The Ayah number

Reply ONLY in JSON:
{{"text": "Arabic verse text", "translation": "{lang_name} translation", "surah": "Surah name in {lang_name}", "ayah": ayah_number}}"""
        
        response = await chat.chat([UserMessage(content=prompt)])
        import re
        match = re.search(r'\{[^}]+\}', response.content)
        if match:
            data = json_module.loads(match.group())
            return {"verse": data}
    except Exception as e:
        logging.error(f"Verse error: {e}")
    
    # Fallback with translation
    fallback_translations = {
        "en": {"translation": "And whoever fears Allah - He will make for him a way out", "surah": "At-Talaq"},
        "de": {"translation": "Und wer Allah fürchtet, dem wird Er einen Ausweg schaffen", "surah": "At-Talaq"},
        "fr": {"translation": "Et quiconque craint Allah, Il lui donnera une issue", "surah": "At-Talaq"},
        "ru": {"translation": "Тому, кто боится Аллаха, Он создаст выход", "surah": "Ат-Таляк"},
        "tr": {"translation": "Kim Allah'tan korkarsa, Allah ona bir çıkış yolu yaratır", "surah": "Talak"},
        "nl": {"translation": "En wie Allah vreest, Hij zal hem een uitweg verschaffen", "surah": "At-Talaq"},
        "sv": {"translation": "Och den som fruktar Allah, Han ska ge honom en utväg", "surah": "At-Talaq"},
        "el": {"translation": "Και όποιος φοβάται τον Αλλάχ, Αυτός θα του δώσει διέξοδο", "surah": "Ατ-Ταλάκ"},
    }
    fb = fallback_translations.get(language, fallback_translations["en"])
    if language == "ar":
        return {"verse": {"text": "وَمَن يَتَوَكَّلْ عَلَى اللَّهِ فَهُوَ حَسْبُهُ", "surah": "الطلاق", "ayah": 3}}
    return {"verse": {"text": "وَمَن يَتَوَكَّلْ عَلَى اللَّهِ فَهُوَ حَسْبُهُ", "translation": fb["translation"], "surah": fb["surah"], "ayah": 3}}

@router.get("/ai/hadith-of-day")
async def get_hadith_of_day(language: str = Query("ar")):
    """Get AI-selected hadith of the day with translation"""
    try:
        from emergentintegrations.llm.chat import LlmChat, UserMessage
        chat = LlmChat(api_key=EMERGENT_LLM_KEY, session_id=f"hadith-of-day-{language}-{date.today().isoformat()}", system_message="أنت عالم حديث. أعط أحاديث صحيحة. أجب بـ JSON فقط.").with_model("gemini", "gemini-2.0-flash")
        
        lang_names = {"en": "English", "de": "German", "fr": "French", "ru": "Russian", "tr": "Turkish", "nl": "Dutch", "sv": "Swedish", "el": "Greek"}
        
        if language == "ar":
            prompt = """اختر حديث نبوي صحيح ومشهور. أعطني:
1. نص الحديث مختصر
2. اسم الراوي
3. المصدر (البخاري/مسلم/الترمذي...)

أجب بصيغة JSON فقط:
{"text": "نص الحديث", "narrator": "اسم الراوي", "source": "المصدر"}"""
        else:
            lang_name = lang_names.get(language, "English")
            prompt = f"""Select a famous authentic hadith of Prophet Muhammad (PBUH). Give me:
1. The Arabic text of the hadith (short)
2. The {lang_name} translation
3. The narrator name in {lang_name}
4. The source in {lang_name} (e.g., "Sahih Bukhari", "Sahih Muslim")

Reply ONLY in JSON:
{{"text": "Arabic hadith text", "translation": "{lang_name} translation", "narrator": "Narrator in {lang_name}", "source": "Source in {lang_name}"}}"""
        
        response = await chat.chat([UserMessage(content=prompt)])
        import re
        match = re.search(r'\{[^}]+\}', response.content)
        if match:
            data = json_module.loads(match.group())
            return {"hadith": data}
    except Exception as e:
        logging.error(f"Hadith error: {e}")
    
    fallback_translations = {
        "en": {"translation": "The best of you are those who learn the Quran and teach it", "narrator": "Uthman ibn Affan", "source": "Sahih Bukhari"},
        "de": {"translation": "Die Besten unter euch sind diejenigen, die den Quran lernen und lehren", "narrator": "Uthman ibn Affan", "source": "Sahih Bukhari"},
        "fr": {"translation": "Les meilleurs d'entre vous sont ceux qui apprennent le Coran et l'enseignent", "narrator": "Uthman ibn Affan", "source": "Sahih Bukhari"},
        "ru": {"translation": "Лучшие из вас те, кто изучает Коран и обучает ему", "narrator": "Усман ибн Аффан", "source": "Сахих Бухари"},
        "tr": {"translation": "Sizin en hayırlınız Kuran'ı öğrenen ve öğretendir", "narrator": "Osman bin Affan", "source": "Sahih Buhari"},
        "nl": {"translation": "De besten onder jullie zijn degenen die de Koran leren en onderwijzen", "narrator": "Uthman ibn Affan", "source": "Sahih Bukhari"},
        "sv": {"translation": "De bästa bland er är de som lär sig Koranen och lär ut den", "narrator": "Uthman ibn Affan", "source": "Sahih Bukhari"},
        "el": {"translation": "Οι καλύτεροι από εσάς είναι αυτοί που μαθαίνουν το Κοράνι και το διδάσκουν", "narrator": "Ουθμάν ιμπν Αφφάν", "source": "Σαχίχ Μπουχάρι"},
    }
    fb = fallback_translations.get(language, fallback_translations.get("en", {}))
    if language == "ar":
        return {"hadith": {"text": "خيركم من تعلم القرآن وعلمه", "narrator": "عثمان بن عفان", "source": "صحيح البخاري"}}
    return {"hadith": {"text": "خيركم من تعلم القرآن وعلمه", "translation": fb.get("translation", ""), "narrator": fb.get("narrator", "Uthman ibn Affan"), "source": fb.get("source", "Sahih Bukhari")}}

# ==================== VOICE SEARCH AI (بحث صوتي ذكي) ====================

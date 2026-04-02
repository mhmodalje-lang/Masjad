"""
Router: ai
"""
from fastapi import APIRouter, HTTPException, Query, Depends
from deps import db, get_user, logger, EMERGENT_LLM_KEY
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
import uuid
import random
import re
import os
import json as json_module

class DhikrAIRequest(BaseModel):
    time_of_day: str = "morning"
    occasion: Optional[str] = None
    language: str = "ar"
    count: int = 5

router = APIRouter(tags=["AI Assistant"])

async def _check_ai_rate_limit(user_id: str, today: str) -> dict | None:
    """Check daily question limit and credit requirements. Returns error dict or None."""
    today_count = await db.ai_questions.count_documents({"user_id": user_id, "date": today})
    if today_count >= 20:
        return {"answer": "", "error": "daily_limit", "message": "وصلت للحد الأقصى (20 سؤال). عُد غداً إن شاء الله.", "remaining": 0}
    if today_count >= 5:
        wallet = await db.wallets.find_one({"user_id": user_id})
        credits = wallet.get("credits", 0) if wallet else 0
        if credits < 5:
            return {"answer": "", "error": "no_credits", "message": "انتهت أسئلتك المجانية. شاهد فيديوهات لكسب نقاط أو اشترِ نقاطاً.", "remaining": 0, "credits": credits}
        await db.wallets.update_one({"user_id": user_id}, {"$inc": {"credits": -5}})
    return None


async def _call_ai_model(question: str, user_id: str, session_id: str) -> str:
    """Call the AI model and return the answer text."""
    from emergentintegrations.llm.chat import LlmChat, UserMessage as LlmUserMessage
    system_prompt = """أنت مساعد إسلامي متخصص. تجيب فقط على الأسئلة المتعلقة بالإسلام والشريعة والقرآن والسنة والفقه والعقيدة والسيرة النبوية والأخلاق الإسلامية.
إذا سُئلت عن موضوع غير إسلامي، أجب بلطف: "أنا مختص بالأسئلة الإسلامية فقط. كيف أساعدك في أمور دينك؟"
أجب بالعربية دائماً. كن دقيقاً واذكر المصادر (القرآن، الحديث) كلما أمكن. لا تفتِ بدون دليل شرعي."""
    chat = LlmChat(
        api_key=os.environ.get("EMERGENT_LLM_KEY", ""),
        session_id=f"islamic_assistant_{user_id}_{session_id}",
        system_message=system_prompt,
    ).with_model("openai", "gpt-5.2")
    return await chat.send_message(LlmUserMessage(text=question))


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
    today_count = await db.ai_questions.count_documents({"user_id": user["id"], "date": today})
    
    # Rate limit check
    limit_error = await _check_ai_rate_limit(user["id"], today)
    if limit_error:
        return limit_error
    
    needs_credits = today_count >= 5
    
    # Call AI
    try:
        answer = await _call_ai_model(question, user["id"], session_id)
    except Exception as e:
        logger.error(f"AI error: {e}")
        answer = "عذراً، حدث خطأ في الاتصال بالمساعد. حاول مرة أخرى."
    
    # Save
    await db.ai_questions.insert_one({
        "user_id": user["id"], "session_id": session_id,
        "question": question, "answer": answer, "date": today,
        "credits_used": 5 if needs_credits else 0,
        "created_at": datetime.utcnow().isoformat(),
    })
    
    return {
        "answer": answer,
        "remaining": 20 - today_count - 1,
        "free_remaining": max(0, 5 - today_count - 1),
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
    return {"reminder": random.choice(reminders)}

# ==================== HIJRI DATE ====================

@router.get("/ai/daily-dua")
async def get_daily_dua():
    """Get daily dua — rotates through curated collection based on date"""
    DUAS = [
        {"text": "رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الْآخِرَةِ حَسَنَةً وَقِنَا عَذَابَ النَّارِ", "source": "سورة البقرة 201"},
        {"text": "رَبِّ اشْرَحْ لِي صَدْرِي وَيَسِّرْ لِي أَمْرِي وَاحْلُلْ عُقْدَةً مِّن لِّسَانِي يَفْقَهُوا قَوْلِي", "source": "سورة طه 25-28"},
        {"text": "رَبِّ زِدْنِي عِلْمًا", "source": "سورة طه 114"},
        {"text": "اللَّهُمَّ إِنِّي أَسْأَلُكَ الْهُدَى وَالتُّقَى وَالْعَفَافَ وَالْغِنَى", "source": "صحيح مسلم"},
        {"text": "رَبَّنَا هَبْ لَنَا مِنْ أَزْوَاجِنَا وَذُرِّيَّاتِنَا قُرَّةَ أَعْيُنٍ وَاجْعَلْنَا لِلْمُتَّقِينَ إِمَامًا", "source": "سورة الفرقان 74"},
        {"text": "اللَّهُمَّ إِنِّي أَعُوذُ بِكَ مِنْ الْهَمِّ وَالْحُزْنِ وَالْعَجْزِ وَالْكَسَلِ", "source": "صحيح البخاري"},
        {"text": "رَبِّ أَوْزِعْنِي أَنْ أَشْكُرَ نِعْمَتَكَ الَّتِي أَنْعَمْتَ عَلَيَّ وَعَلَىٰ وَالِدَيَّ", "source": "سورة النمل 19"},
        {"text": "حَسْبُنَا اللَّهُ وَنِعْمَ الْوَكِيلُ", "source": "سورة آل عمران 173"},
        {"text": "اللَّهُمَّ اهْدِنِي وَسَدِّدْنِي", "source": "صحيح مسلم"},
        {"text": "رَبَّنَا لَا تُزِغْ قُلُوبَنَا بَعْدَ إِذْ هَدَيْتَنَا وَهَبْ لَنَا مِن لَّدُنكَ رَحْمَةً", "source": "سورة آل عمران 8"},
        {"text": "اللَّهُمَّ أَعِنِّي عَلَى ذِكْرِكَ وَشُكْرِكَ وَحُسْنِ عِبَادَتِكَ", "source": "سنن أبي داود"},
        {"text": "رَبِّ اجْعَلْنِي مُقِيمَ الصَّلَاةِ وَمِن ذُرِّيَّتِي رَبَّنَا وَتَقَبَّلْ دُعَاءِ", "source": "سورة إبراهيم 40"},
        {"text": "اللَّهُمَّ إِنَّكَ عَفُوٌّ تُحِبُّ الْعَفْوَ فَاعْفُ عَنِّي", "source": "سنن الترمذي"},
        {"text": "رَبَّنَا اغْفِرْ لَنَا ذُنُوبَنَا وَإِسْرَافَنَا فِي أَمْرِنَا وَثَبِّتْ أَقْدَامَنَا", "source": "سورة آل عمران 147"},
        {"text": "لَا إِلَهَ إِلَّا أَنتَ سُبْحَانَكَ إِنِّي كُنتُ مِنَ الظَّالِمِينَ", "source": "سورة الأنبياء 87"},
        {"text": "اللَّهُمَّ إِنِّي أَسْأَلُكَ الْعَافِيَةَ فِي الدُّنْيَا وَالْآخِرَةِ", "source": "سنن ابن ماجه"},
        {"text": "رَبِّ هَبْ لِي مِن لَّدُنكَ ذُرِّيَّةً طَيِّبَةً إِنَّكَ سَمِيعُ الدُّعَاءِ", "source": "سورة آل عمران 38"},
        {"text": "اللَّهُمَّ إِنِّي أَسْأَلُكَ عِلْمًا نَافِعًا وَرِزْقًا طَيِّبًا وَعَمَلًا مُتَقَبَّلًا", "source": "سنن ابن ماجه"},
        {"text": "رَبَّنَا ظَلَمْنَا أَنفُسَنَا وَإِن لَّمْ تَغْفِرْ لَنَا وَتَرْحَمْنَا لَنَكُونَنَّ مِنَ الْخَاسِرِينَ", "source": "سورة الأعراف 23"},
        {"text": "اللَّهُمَّ أَصْلِحْ لِي دِينِي الَّذِي هُوَ عِصْمَةُ أَمْرِي وَأَصْلِحْ لِي دُنْيَايَ الَّتِي فِيهَا مَعَاشِي", "source": "صحيح مسلم"},
        {"text": "رَبَّنَا لَا تُؤَاخِذْنَا إِن نَّسِينَا أَوْ أَخْطَأْنَا", "source": "سورة البقرة 286"},
        {"text": "اللَّهُمَّ إِنِّي أَعُوذُ بِكَ مِنْ عِلْمٍ لَا يَنْفَعُ وَمِنْ قَلْبٍ لَا يَخْشَعُ", "source": "صحيح مسلم"},
        {"text": "رَبِّ أَدْخِلْنِي مُدْخَلَ صِدْقٍ وَأَخْرِجْنِي مُخْرَجَ صِدْقٍ وَاجْعَل لِّي مِن لَّدُنكَ سُلْطَانًا نَّصِيرًا", "source": "سورة الإسراء 80"},
        {"text": "اللَّهُمَّ بَاعِدْ بَيْنِي وَبَيْنَ خَطَايَايَ كَمَا بَاعَدْتَ بَيْنَ الْمَشْرِقِ وَالْمَغْرِبِ", "source": "صحيح البخاري"},
        {"text": "رَبَّنَا أَفْرِغْ عَلَيْنَا صَبْرًا وَثَبِّتْ أَقْدَامَنَا وَانصُرْنَا عَلَى الْقَوْمِ الْكَافِرِينَ", "source": "سورة البقرة 250"},
        {"text": "اللَّهُمَّ اغْفِرْ لِي وَارْحَمْنِي وَاهْدِنِي وَارْزُقْنِي وَعَافِنِي", "source": "صحيح مسلم"},
        {"text": "رَبَّنَا اصْرِفْ عَنَّا عَذَابَ جَهَنَّمَ إِنَّ عَذَابَهَا كَانَ غَرَامًا", "source": "سورة الفرقان 65"},
        {"text": "اللَّهُمَّ إِنِّي أَسْأَلُكَ الثَّبَاتَ فِي الْأَمْرِ وَالْعَزِيمَةَ عَلَى الرُّشْدِ", "source": "سنن النسائي"},
        {"text": "رَبِّ إِنِّي لِمَا أَنزَلْتَ إِلَيَّ مِنْ خَيْرٍ فَقِيرٌ", "source": "سورة القصص 24"},
        {"text": "اللَّهُمَّ مُصَرِّفَ الْقُلُوبِ صَرِّفْ قُلُوبَنَا عَلَى طَاعَتِكَ", "source": "صحيح مسلم"},
        {"text": "اللَّهُمَّ آتِ نَفْسِي تَقْوَاهَا وَزَكِّهَا أَنْتَ خَيْرُ مَن زَكَّاهَا أَنْتَ وَلِيُّهَا وَمَوْلَاهَا", "source": "صحيح مسلم"},
        {"text": "رَبَّنَا تَقَبَّلْ مِنَّا إِنَّكَ أَنتَ السَّمِيعُ الْعَلِيمُ وَتُبْ عَلَيْنَا إِنَّكَ أَنتَ التَّوَّابُ الرَّحِيمُ", "source": "سورة البقرة 127-128"},
        {"text": "اللَّهُمَّ إِنِّي أَعُوذُ بِكَ مِنَ الْبُخْلِ وَأَعُوذُ بِكَ مِنَ الْجُبْنِ وَأَعُوذُ بِكَ أَنْ أُرَدَّ إِلَى أَرْذَلِ الْعُمُرِ", "source": "صحيح البخاري"},
        {"text": "رَبَّنَا وَلَا تُحَمِّلْنَا مَا لَا طَاقَةَ لَنَا بِهِ وَاعْفُ عَنَّا وَاغْفِرْ لَنَا وَارْحَمْنَا أَنتَ مَوْلَانَا", "source": "سورة البقرة 286"},
        {"text": "اللَّهُمَّ اقْسِمْ لَنَا مِنْ خَشْيَتِكَ مَا تَحُولُ بِهِ بَيْنَنَا وَبَيْنَ مَعَاصِيكَ", "source": "سنن الترمذي"},
    ]
    day_index = (date.today() - date(2025, 1, 1)).days % len(DUAS)
    return {"success": True, "dua": DUAS[day_index]}

@router.get("/ai/verse-of-day")
async def get_verse_of_day(language: str = Query("ar")):
    """Get verse of the day — rotates through 30 curated verses daily"""
    VERSES = [
        {"text": "وَمَن يَتَوَكَّلْ عَلَى اللَّهِ فَهُوَ حَسْبُهُ", "surah_ar": "الطلاق", "surah_en": "At-Talaq", "surah_number": 65, "ayah": 3, "tr_en": "And whoever relies upon Allah - then He is sufficient for him"},
        {"text": "إِنَّ مَعَ الْعُسْرِ يُسْرًا", "surah_ar": "الشرح", "surah_en": "Ash-Sharh", "surah_number": 94, "ayah": 6, "tr_en": "Indeed, with hardship comes ease"},
        {"text": "وَلَا تَيْأَسُوا مِن رَّوْحِ اللَّهِ", "surah_ar": "يوسف", "surah_en": "Yusuf", "surah_number": 12, "ayah": 87, "tr_en": "Do not despair of the mercy of Allah"},
        {"text": "فَاذْكُرُونِي أَذْكُرْكُمْ وَاشْكُرُوا لِي وَلَا تَكْفُرُونِ", "surah_ar": "البقرة", "surah_en": "Al-Baqarah", "surah_number": 2, "ayah": 152, "tr_en": "So remember Me; I will remember you. Be grateful to Me"},
        {"text": "وَاصْبِرْ فَإِنَّ اللَّهَ لَا يُضِيعُ أَجْرَ الْمُحْسِنِينَ", "surah_ar": "هود", "surah_en": "Hud", "surah_number": 11, "ayah": 115, "tr_en": "And be patient, for indeed, Allah does not allow to be lost the reward of those who do good"},
        {"text": "رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الْآخِرَةِ حَسَنَةً وَقِنَا عَذَابَ النَّارِ", "surah_ar": "البقرة", "surah_en": "Al-Baqarah", "surah_number": 2, "ayah": 201, "tr_en": "Our Lord, give us in this world that which is good and in the Hereafter that which is good"},
        {"text": "وَإِذَا سَأَلَكَ عِبَادِي عَنِّي فَإِنِّي قَرِيبٌ", "surah_ar": "البقرة", "surah_en": "Al-Baqarah", "surah_number": 2, "ayah": 186, "tr_en": "When My servants ask about Me, I am indeed near"},
        {"text": "وَمَا أَرْسَلْنَاكَ إِلَّا رَحْمَةً لِّلْعَالَمِينَ", "surah_ar": "الأنبياء", "surah_en": "Al-Anbiya", "surah_number": 21, "ayah": 107, "tr_en": "We have not sent you except as a mercy to the worlds"},
        {"text": "إِنَّ اللَّهَ مَعَ الصَّابِرِينَ", "surah_ar": "البقرة", "surah_en": "Al-Baqarah", "surah_number": 2, "ayah": 153, "tr_en": "Indeed, Allah is with the patient"},
        {"text": "وَلَسَوْفَ يُعْطِيكَ رَبُّكَ فَتَرْضَىٰ", "surah_ar": "الضحى", "surah_en": "Ad-Duha", "surah_number": 93, "ayah": 5, "tr_en": "And your Lord is going to give you, and you will be satisfied"},
        {"text": "قُلْ هُوَ اللَّهُ أَحَدٌ", "surah_ar": "الإخلاص", "surah_en": "Al-Ikhlas", "surah_number": 112, "ayah": 1, "tr_en": "Say: He is Allah, the One"},
        {"text": "وَنَحْنُ أَقْرَبُ إِلَيْهِ مِنْ حَبْلِ الْوَرِيدِ", "surah_ar": "ق", "surah_en": "Qaf", "surah_number": 50, "ayah": 16, "tr_en": "We are closer to him than his jugular vein"},
        {"text": "فَإِنَّ ذِكْرَى تَنفَعُ الْمُؤْمِنِينَ", "surah_ar": "الذاريات", "surah_en": "Adh-Dhariyat", "surah_number": 51, "ayah": 55, "tr_en": "For indeed, the reminder benefits the believers"},
        {"text": "وَاللَّهُ يُحِبُّ الْمُحْسِنِينَ", "surah_ar": "آل عمران", "surah_en": "Ali Imran", "surah_number": 3, "ayah": 134, "tr_en": "And Allah loves the doers of good"},
        {"text": "ادْعُونِي أَسْتَجِبْ لَكُمْ", "surah_ar": "غافر", "surah_en": "Ghafir", "surah_number": 40, "ayah": 60, "tr_en": "Call upon Me; I will respond to you"},
        {"text": "لَا يُكَلِّفُ اللَّهُ نَفْسًا إِلَّا وُسْعَهَا", "surah_ar": "البقرة", "surah_en": "Al-Baqarah", "surah_number": 2, "ayah": 286, "tr_en": "Allah does not burden a soul beyond that it can bear"},
        {"text": "سَيَجْعَلُ اللَّهُ بَعْدَ عُسْرٍ يُسْرًا", "surah_ar": "الطلاق", "surah_en": "At-Talaq", "surah_number": 65, "ayah": 7, "tr_en": "Allah will bring about ease after hardship"},
        {"text": "يَا أَيُّهَا الَّذِينَ آمَنُوا اسْتَعِينُوا بِالصَّبْرِ وَالصَّلَاةِ", "surah_ar": "البقرة", "surah_en": "Al-Baqarah", "surah_number": 2, "ayah": 153, "tr_en": "O you who believe, seek help through patience and prayer"},
        {"text": "وَهُوَ مَعَكُمْ أَيْنَ مَا كُنتُمْ", "surah_ar": "الحديد", "surah_en": "Al-Hadid", "surah_number": 57, "ayah": 4, "tr_en": "And He is with you wherever you are"},
        {"text": "إِنَّا فَتَحْنَا لَكَ فَتْحًا مُّبِينًا", "surah_ar": "الفتح", "surah_en": "Al-Fath", "surah_number": 48, "ayah": 1, "tr_en": "Indeed, We have given you a clear conquest"},
        {"text": "وَرَحْمَتِي وَسِعَتْ كُلَّ شَيْءٍ", "surah_ar": "الأعراف", "surah_en": "Al-A'raf", "surah_number": 7, "ayah": 156, "tr_en": "My mercy encompasses all things"},
        {"text": "أَلَا بِذِكْرِ اللَّهِ تَطْمَئِنُّ الْقُلُوبُ", "surah_ar": "الرعد", "surah_en": "Ar-Ra'd", "surah_number": 13, "ayah": 28, "tr_en": "Verily, in the remembrance of Allah do hearts find rest"},
        {"text": "وَمَن يَتَّقِ اللَّهَ يَجْعَل لَّهُ مَخْرَجًا", "surah_ar": "الطلاق", "surah_en": "At-Talaq", "surah_number": 65, "ayah": 2, "tr_en": "Whoever fears Allah, He will make a way out for him"},
        {"text": "وَقُل رَّبِّ زِدْنِي عِلْمًا", "surah_ar": "طه", "surah_en": "Ta-Ha", "surah_number": 20, "ayah": 114, "tr_en": "And say, My Lord, increase me in knowledge"},
        {"text": "إِنَّ اللَّهَ لَا يُغَيِّرُ مَا بِقَوْمٍ حَتَّىٰ يُغَيِّرُوا مَا بِأَنفُسِهِمْ", "surah_ar": "الرعد", "surah_en": "Ar-Ra'd", "surah_number": 13, "ayah": 11, "tr_en": "Indeed, Allah will not change the condition of a people until they change what is in themselves"},
        {"text": "فَبِأَيِّ آلَاءِ رَبِّكُمَا تُكَذِّبَانِ", "surah_ar": "الرحمن", "surah_en": "Ar-Rahman", "surah_number": 55, "ayah": 13, "tr_en": "So which of the favors of your Lord would you deny?"},
        {"text": "وَاسْتَغْفِرِ اللَّهَ إِنَّ اللَّهَ كَانَ غَفُورًا رَّحِيمًا", "surah_ar": "النساء", "surah_en": "An-Nisa", "surah_number": 4, "ayah": 106, "tr_en": "And seek forgiveness of Allah. Indeed, Allah is Forgiving and Merciful"},
        {"text": "وَعَسَىٰ أَن تَكْرَهُوا شَيْئًا وَهُوَ خَيْرٌ لَّكُمْ", "surah_ar": "البقرة", "surah_en": "Al-Baqarah", "surah_number": 2, "ayah": 216, "tr_en": "Perhaps you dislike a thing and it is good for you"},
        {"text": "وَمَن يُؤْمِن بِاللَّهِ يَهْدِ قَلْبَهُ", "surah_ar": "التغابن", "surah_en": "At-Taghabun", "surah_number": 64, "ayah": 11, "tr_en": "And whoever believes in Allah - He will guide his heart"},
        {"text": "وَإِنَّكَ لَعَلَىٰ خُلُقٍ عَظِيمٍ", "surah_ar": "القلم", "surah_en": "Al-Qalam", "surah_number": 68, "ayah": 4, "tr_en": "And indeed, you are of a great moral character"},
    ]
    day_index = (date.today() - date(2025, 1, 1)).days % len(VERSES)
    v = VERSES[day_index]
    result = {"text": v["text"], "surah": v["surah_ar"] if language == "ar" else v["surah_en"], "surah_number": v["surah_number"], "ayah": v["ayah"]}
    if language != "ar":
        result["translation"] = v["tr_en"]
    return {"success": True, "verse": result}

@router.get("/ai/hadith-of-day")
async def get_hadith_of_day(language: str = Query("ar")):
    """Get hadith of the day — rotates through 30 curated hadiths daily"""
    HADITHS = [
        {"text": "خيركم من تعلم القرآن وعلمه", "narrator_ar": "عثمان بن عفان", "narrator_en": "Uthman ibn Affan", "source_ar": "صحيح البخاري", "source_en": "Sahih Bukhari", "tr_en": "The best of you are those who learn the Quran and teach it"},
        {"text": "إنما الأعمال بالنيات", "narrator_ar": "عمر بن الخطاب", "narrator_en": "Umar ibn Al-Khattab", "source_ar": "صحيح البخاري", "source_en": "Sahih Bukhari", "tr_en": "Actions are judged by intentions"},
        {"text": "من كان يؤمن بالله واليوم الآخر فليقل خيراً أو ليصمت", "narrator_ar": "أبو هريرة", "narrator_en": "Abu Hurairah", "source_ar": "صحيح البخاري", "source_en": "Sahih Bukhari", "tr_en": "Whoever believes in Allah and the Last Day, let him speak good or keep silent"},
        {"text": "لا يؤمن أحدكم حتى يحب لأخيه ما يحب لنفسه", "narrator_ar": "أنس بن مالك", "narrator_en": "Anas ibn Malik", "source_ar": "صحيح البخاري", "source_en": "Sahih Bukhari", "tr_en": "None of you truly believes until he loves for his brother what he loves for himself"},
        {"text": "الدين النصيحة", "narrator_ar": "تميم الداري", "narrator_en": "Tamim Ad-Dari", "source_ar": "صحيح مسلم", "source_en": "Sahih Muslim", "tr_en": "Religion is sincerity/good counsel"},
        {"text": "المسلم من سلم المسلمون من لسانه ويده", "narrator_ar": "عبدالله بن عمرو", "narrator_en": "Abdullah ibn Amr", "source_ar": "صحيح البخاري", "source_en": "Sahih Bukhari", "tr_en": "A Muslim is one from whose tongue and hand other Muslims are safe"},
        {"text": "تبسُّمك في وجه أخيك صدقة", "narrator_ar": "أبو ذر الغفاري", "narrator_en": "Abu Dharr", "source_ar": "سنن الترمذي", "source_en": "Tirmidhi", "tr_en": "Your smile in the face of your brother is charity"},
        {"text": "اتق الله حيثما كنت وأتبع السيئة الحسنة تمحها وخالق الناس بخلق حسن", "narrator_ar": "أبو ذر", "narrator_en": "Abu Dharr", "source_ar": "سنن الترمذي", "source_en": "Tirmidhi", "tr_en": "Fear Allah wherever you are, follow a bad deed with a good deed to erase it, and treat people with good character"},
        {"text": "إن الله رفيق يحب الرفق في الأمر كله", "narrator_ar": "عائشة", "narrator_en": "Aisha", "source_ar": "صحيح البخاري", "source_en": "Sahih Bukhari", "tr_en": "Allah is gentle and loves gentleness in all things"},
        {"text": "الطهور شطر الإيمان", "narrator_ar": "أبو مالك الأشعري", "narrator_en": "Abu Malik Al-Ash'ari", "source_ar": "صحيح مسلم", "source_en": "Sahih Muslim", "tr_en": "Purification is half of faith"},
        {"text": "من سلك طريقاً يلتمس فيه علماً سهل الله له طريقاً إلى الجنة", "narrator_ar": "أبو هريرة", "narrator_en": "Abu Hurairah", "source_ar": "صحيح مسلم", "source_en": "Sahih Muslim", "tr_en": "Whoever takes a path seeking knowledge, Allah will make his path to Paradise easy"},
        {"text": "ما نقصت صدقة من مال", "narrator_ar": "أبو هريرة", "narrator_en": "Abu Hurairah", "source_ar": "صحيح مسلم", "source_en": "Sahih Muslim", "tr_en": "Charity does not decrease wealth"},
        {"text": "خيركم خيركم لأهله وأنا خيركم لأهلي", "narrator_ar": "عائشة", "narrator_en": "Aisha", "source_ar": "سنن الترمذي", "source_en": "Tirmidhi", "tr_en": "The best of you are the best to their families, and I am the best to my family"},
        {"text": "الكلمة الطيبة صدقة", "narrator_ar": "أبو هريرة", "narrator_en": "Abu Hurairah", "source_ar": "صحيح البخاري", "source_en": "Sahih Bukhari", "tr_en": "A good word is charity"},
        {"text": "من حسن إسلام المرء تركه ما لا يعنيه", "narrator_ar": "أبو هريرة", "narrator_en": "Abu Hurairah", "source_ar": "سنن الترمذي", "source_en": "Tirmidhi", "tr_en": "Part of someone's being a good Muslim is leaving alone what does not concern him"},
        {"text": "لا تغضب", "narrator_ar": "أبو هريرة", "narrator_en": "Abu Hurairah", "source_ar": "صحيح البخاري", "source_en": "Sahih Bukhari", "tr_en": "Do not get angry"},
        {"text": "ما ملأ آدمي وعاءً شراً من بطنه", "narrator_ar": "المقدام بن معدي كرب", "narrator_en": "Al-Miqdam", "source_ar": "سنن الترمذي", "source_en": "Tirmidhi", "tr_en": "A human being fills no worse vessel than his stomach"},
        {"text": "المؤمن القوي خير وأحب إلى الله من المؤمن الضعيف", "narrator_ar": "أبو هريرة", "narrator_en": "Abu Hurairah", "source_ar": "صحيح مسلم", "source_en": "Sahih Muslim", "tr_en": "The strong believer is better and more beloved to Allah than the weak believer"},
        {"text": "إن الله جميل يحب الجمال", "narrator_ar": "عبدالله بن مسعود", "narrator_en": "Ibn Mas'ud", "source_ar": "صحيح مسلم", "source_en": "Sahih Muslim", "tr_en": "Allah is beautiful and loves beauty"},
        {"text": "الدعاء هو العبادة", "narrator_ar": "النعمان بن بشير", "narrator_en": "An-Nu'man ibn Bashir", "source_ar": "سنن الترمذي", "source_en": "Tirmidhi", "tr_en": "Supplication is the essence of worship"},
        {"text": "من صلى الفجر في جماعة فهو في ذمة الله", "narrator_ar": "جندب بن عبدالله", "narrator_en": "Jundub", "source_ar": "صحيح مسلم", "source_en": "Sahih Muslim", "tr_en": "Whoever prays Fajr in congregation is under Allah's protection"},
        {"text": "أفضل الصدقة أن تُشبع كبداً جائعة", "narrator_ar": "أنس بن مالك", "narrator_en": "Anas ibn Malik", "source_ar": "سنن البيهقي", "source_en": "Al-Bayhaqi", "tr_en": "The best charity is to satisfy a hungry person"},
        {"text": "إذا مات ابن آدم انقطع عمله إلا من ثلاث: صدقة جارية أو علم ينتفع به أو ولد صالح يدعو له", "narrator_ar": "أبو هريرة", "narrator_en": "Abu Hurairah", "source_ar": "صحيح مسلم", "source_en": "Sahih Muslim", "tr_en": "When a person dies, their deeds end except for three: ongoing charity, beneficial knowledge, or a righteous child who prays for them"},
        {"text": "أحب الناس إلى الله أنفعهم للناس", "narrator_ar": "عبدالله بن عمر", "narrator_en": "Ibn Umar", "source_ar": "الطبراني", "source_en": "At-Tabarani", "tr_en": "The most beloved people to Allah are those who are most beneficial to people"},
        {"text": "ما من مسلم يغرس غرساً فيأكل منه إنسان أو طائر إلا كان له صدقة", "narrator_ar": "أنس بن مالك", "narrator_en": "Anas ibn Malik", "source_ar": "صحيح البخاري", "source_en": "Sahih Bukhari", "tr_en": "No Muslim plants a tree from which a person or bird eats except that it is charity for him"},
        {"text": "ليس الشديد بالصرعة إنما الشديد الذي يملك نفسه عند الغضب", "narrator_ar": "أبو هريرة", "narrator_en": "Abu Hurairah", "source_ar": "صحيح البخاري", "source_en": "Sahih Bukhari", "tr_en": "The strong person is not the one who can wrestle, but the one who controls himself when angry"},
        {"text": "المسلم أخو المسلم لا يظلمه ولا يسلمه", "narrator_ar": "عبدالله بن عمر", "narrator_en": "Ibn Umar", "source_ar": "صحيح البخاري", "source_en": "Sahih Bukhari", "tr_en": "A Muslim is a brother to another Muslim - he neither wrongs him nor surrenders him"},
        {"text": "استفت قلبك وإن أفتاك الناس وأفتوك", "narrator_ar": "وابصة بن معبد", "narrator_en": "Wabisah", "source_ar": "مسند أحمد", "source_en": "Musnad Ahmad", "tr_en": "Consult your heart even if people give you verdicts"},
        {"text": "أقرب ما يكون العبد من ربه وهو ساجد فأكثروا الدعاء", "narrator_ar": "أبو هريرة", "narrator_en": "Abu Hurairah", "source_ar": "صحيح مسلم", "source_en": "Sahih Muslim", "tr_en": "The closest a servant is to his Lord is during prostration, so increase supplication"},
        {"text": "من صام رمضان إيماناً واحتساباً غُفر له ما تقدم من ذنبه", "narrator_ar": "أبو هريرة", "narrator_en": "Abu Hurairah", "source_ar": "صحيح البخاري", "source_en": "Sahih Bukhari", "tr_en": "Whoever fasts Ramadan with faith and seeking reward, his previous sins will be forgiven"},
    ]
    day_index = (date.today() - date(2025, 1, 1)).days % len(HADITHS)
    h = HADITHS[day_index]
    result = {"text": h["text"], "narrator": h["narrator_ar"] if language == "ar" else h["narrator_en"], "source": h["source_ar"] if language == "ar" else h["source_en"]}
    if language != "ar":
        result["translation"] = h["tr_en"]
    return {"success": True, "hadith": result}

# ==================== VOICE SEARCH AI (بحث صوتي ذكي) ====================

"""
أكاديمية نور - AI Features Router
AI-powered Islamic education for children
Using Emergent LLM Key with OpenAI gpt-4.1-mini for speed
"""

import os
import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

from emergentintegrations.llm.chat import LlmChat, UserMessage

router = APIRouter()

API_KEY = os.environ.get("EMERGENT_LLM_KEY", "")

# ═══════════════════════════════════════════════════════════════
# SYSTEM PROMPTS - Islamic Education AI for Children
# ═══════════════════════════════════════════════════════════════

QURAN_HELPER_SYSTEM = """أنت "معلم نور" - مساعد ذكي لتحفيظ القرآن الكريم للأطفال.

القواعد:
- تحدث بلغة بسيطة مناسبة للأطفال (٥-١٢ سنة)
- استخدم التشجيع والمدح دائماً
- عند اختبار الحفظ: اعطِ أول كلمات من الآية واطلب الإكمال
- صحّح الأخطاء بلطف مع شرح المعنى
- اذكر فضل السورة إن وجد
- استخدم إيموجي مناسبة: ⭐🌟✨📖🤲
- لا تستخدم أي محتوى غير إسلامي
- أجب بالعربية إلا إذا سُئلت بالإنجليزية
- شجّع الطفل على التكرار والمراجعة"""

ARABIC_TUTOR_SYSTEM = """أنت "معلمة نور" - معلمة اللغة العربية الذكية للأطفال.

القواعد:
- علّم الحروف العربية والكلمات بطريقة ممتعة
- استخدم أمثلة من القرآن والحياة اليومية
- اشرح قواعد النحو والصرف ببساطة شديدة
- أعطِ تمارين تفاعلية (أكمل الكلمة، ما ضد، جمع/مفرد)
- استخدم إيموجي تعليمية: ✏️📝🔤⭐🌟
- شجّع الطفل دائماً وامدحه
- أجب بالعربية الفصحى البسيطة
- ركّز على المفردات الإسلامية والقرآنية
- عند السؤال عن حرف: اذكر شكله، نطقه، مثال من القرآن"""

STORY_GENERATOR_SYSTEM = """أنت "راوي نور" - حكواتي إسلامي ذكي للأطفال.

القواعد:
- أنشئ قصصاً إسلامية تربوية قصيرة (١٥٠-٣٠٠ كلمة)
- القصص مستوحاة من القرآن والسنة والسيرة النبوية
- استخدم لغة بسيطة جميلة مناسبة للأطفال
- كل قصة تحتوي: عنوان، محتوى، درس مستفاد، آية أو حديث
- الشخصيات: أنبياء، صحابة، أطفال مسلمين
- القيم: الصدق، الأمانة، الإحسان، بر الوالدين، الصلاة
- استخدم إيموجي: 📖🌟⭐🕌🤲✨🌙
- تنسيق الإجابة:
  🏷️ العنوان: [عنوان القصة]
  📖 القصة: [نص القصة]
  💡 الدرس المستفاد: [الدرس]
  📌 المرجع: [آية أو حديث]
- لا تكرر نفس القصة
- أجب بالعربية"""

ISLAMIC_QA_SYSTEM = """أنت "عالم نور" - مساعد الأسئلة الإسلامية للأطفال.

القواعد:
- أجب عن الأسئلة الإسلامية بطريقة مبسطة للأطفال (٥-١٢ سنة)
- استند إلى القرآن والسنة الصحيحة فقط
- اذكر المصدر (آية قرآنية أو حديث صحيح)
- إذا لم تعرف الإجابة، قل "اسأل معلمك أو والديك"
- لا تفتِ في مسائل خلافية - وجّه لسؤال العلماء
- استخدم لغة بسيطة وإيموجي: 🤲📖🕌⭐✨
- شجّع حب التعلم والسؤال
- أجب بالعربية إلا إذا سُئلت بالإنجليزية"""


# ═══════════════════════════════════════════════════════════════
# REQUEST/RESPONSE MODELS
# ═══════════════════════════════════════════════════════════════

class AIMessage(BaseModel):
    message: str
    session_id: Optional[str] = None
    locale: Optional[str] = "ar"

class AIStoryRequest(BaseModel):
    topic: Optional[str] = None
    age_group: Optional[str] = "7-10"
    locale: Optional[str] = "ar"

class AIResponse(BaseModel):
    success: bool
    response: str
    session_id: str


# ═══════════════════════════════════════════════════════════════
# HELPER: Create LLM Chat instance
# ═══════════════════════════════════════════════════════════════

def create_chat(system_message: str, session_id: str) -> LlmChat:
    chat = LlmChat(
        api_key=API_KEY,
        session_id=session_id,
        system_message=system_message
    )
    chat.with_model("openai", "gpt-4.1-mini")
    return chat


# ═══════════════════════════════════════════════════════════════
# ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@router.post("/kids-ai/quran-helper")
async def quran_helper(req: AIMessage):
    """AI Quran memorization helper for kids."""
    try:
        sid = req.session_id or f"quran-{uuid.uuid4().hex[:8]}"
        chat = create_chat(QURAN_HELPER_SYSTEM, sid)
        msg = UserMessage(text=req.message)
        response = await chat.send_message(msg)
        return AIResponse(success=True, response=response, session_id=sid)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/kids-ai/arabic-tutor")
async def arabic_tutor(req: AIMessage):
    """AI Arabic language tutor for kids."""
    try:
        sid = req.session_id or f"arabic-{uuid.uuid4().hex[:8]}"
        chat = create_chat(ARABIC_TUTOR_SYSTEM, sid)
        msg = UserMessage(text=req.message)
        response = await chat.send_message(msg)
        return AIResponse(success=True, response=response, session_id=sid)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/kids-ai/story-generator")
async def story_generator(req: AIStoryRequest):
    """AI Islamic story generator for kids."""
    try:
        sid = f"story-{uuid.uuid4().hex[:8]}"
        chat = create_chat(STORY_GENERATOR_SYSTEM, sid)
        
        if req.topic:
            prompt = f"اكتب قصة إسلامية للأطفال عن: {req.topic}. الفئة العمرية: {req.age_group} سنوات."
        else:
            prompt = f"اكتب قصة إسلامية تربوية جديدة ومشوقة للأطفال. الفئة العمرية: {req.age_group} سنوات. اختر موضوعاً مختلفاً في كل مرة."
        
        if req.locale != "ar":
            prompt += " Please write in English."
        
        msg = UserMessage(text=prompt)
        response = await chat.send_message(msg)
        return AIResponse(success=True, response=response, session_id=sid)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/kids-ai/islamic-qa")
async def islamic_qa(req: AIMessage):
    """AI Islamic Q&A for kids."""
    try:
        sid = req.session_id or f"qa-{uuid.uuid4().hex[:8]}"
        chat = create_chat(ISLAMIC_QA_SYSTEM, sid)
        msg = UserMessage(text=req.message)
        response = await chat.send_message(msg)
        return AIResponse(success=True, response=response, session_id=sid)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

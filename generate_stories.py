"""Script to generate AI stories for all categories and languages"""
import asyncio
import os
import sys
import uuid
import random
import json
from datetime import datetime

# Add backend to path
sys.path.insert(0, '/app/backend')
from dotenv import load_dotenv
load_dotenv('/app/backend/.env')

from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = os.environ.get("MONGO_URL", "")
EMERGENT_LLM_KEY = os.environ.get("EMERGENT_LLM_KEY", "")

client = AsyncIOMotorClient(MONGO_URL)
db_name = MONGO_URL.split("/")[-1].split("?")[0] if "/" in MONGO_URL else "app_db"
db = client[db_name]

STORY_CATEGORIES_INFO = {
    "istighfar": {"label": "قصص الاستغفار", "prompt": "قصص حقيقية ومؤثرة عن الاستغفار وفضله وكيف غير حياة أشخاص حقيقيين. قصص عن أثر الاستغفار في تفريج الهموم وفتح أبواب الرزق والشفاء"},
    "sahaba": {"label": "قصص الصحابة", "prompt": "قصص حقيقية من سيرة الصحابة رضي الله عنهم وبطولاتهم وتضحياتهم ومواقفهم المؤثرة في الإسلام"},
    "quran": {"label": "قصص القرآن", "prompt": "قصص مذكورة في القرآن الكريم مع شرح العبر والدروس المستفادة منها بأسلوب قصصي شيق"},
    "prophets": {"label": "قصص الأنبياء", "prompt": "قصص الأنبياء والرسل عليهم السلام ومعجزاتهم ودعوتهم ومواقفهم مع أقوامهم"},
    "ruqyah": {"label": "قصص الرقية", "prompt": "قصص حقيقية عن الشفاء بالرقية الشرعية والقرآن الكريم والأذكار وتجارب أشخاص شفاهم الله"},
    "rizq": {"label": "قصص الرزق", "prompt": "قصص حقيقية عن سعة الرزق والبركة فيه وكيف جاء الرزق من حيث لا يحتسب بفضل التوكل والدعاء"},
    "tawba": {"label": "قصص التوبة", "prompt": "قصص حقيقية مؤثرة عن التوبة والرجوع إلى الله وكيف تغيرت حياة أشخاص بعد التوبة النصوحة"},
    "miracles": {"label": "معجزات وعبر", "prompt": "قصص عن معجزات إلهية وعبر ومواقف عجيبة تدل على قدرة الله وحكمته"},
    "general": {"label": "قصص عامة", "prompt": "قصص إسلامية متنوعة عن الإيمان والأخلاق والمعاملات والحياة اليومية بمنظور إسلامي"},
}

SUPPORTED_STORY_LANGS = {
    "ar": {"name": "أذان وحكاية", "instruction": "اكتب القصص باللغة العربية الفصحى بأسلوب أدبي مشوق"},
    "en": {"name": "Azan & Hikaya", "instruction": "Write the stories in fluent English with an engaging narrative style"},
    "de": {"name": "Azan & Hikaya", "instruction": "Schreibe die Geschichten auf fließendem Deutsch mit einem fesselnden Erzählstil"},
    "fr": {"name": "Azan & Hikaya", "instruction": "Écrivez les histoires en français courant avec un style narratif captivant"},
    "tr": {"name": "Azan & Hikaya", "instruction": "Hikayeleri akıcı Türkçe ile ilgi çekici bir anlatım tarzıyla yazın"},
    "ru": {"name": "Azan & Hikaya", "instruction": "Напишите истории на беглом русском языке с увлекательным повествовательным стилем"},
    "sv": {"name": "Azan & Hikaya", "instruction": "Skriv berättelserna på flytande svenska med en engagerande berättarstil"},
    "nl": {"name": "Azan & Hikaya", "instruction": "Schrijf de verhalen in vloeiend Nederlands met een boeiende vertelstijl"},
    "el": {"name": "Azan & Hikaya", "instruction": "Γράψτε τις ιστορίες σε άπταιστα ελληνικά με ένα συναρπαστικό αφηγηματικό ύφος"},
}

async def generate_batch(category, batch_num, count, lang):
    from emergentintegrations.llm.chat import LlmChat, UserMessage
    
    cat_info = STORY_CATEGORIES_INFO[category]
    lang_info = SUPPORTED_STORY_LANGS[lang]
    
    chat = LlmChat(
        api_key=EMERGENT_LLM_KEY,
        session_id=f"gen-{category}-{lang}-{batch_num}-{uuid.uuid4().hex[:6]}",
        system_message=f"""{lang_info['instruction']}.
You are a professional Islamic story writer. Write realistic, touching and engaging stories.
The stories must be:
- Based on real events or inspired by reality
- Written in an engaging literary style
- Contain a useful moral and lesson
- Suitable for all ages
- Diverse within the requested category
- Each story 150-400 words long

Return ONLY a JSON array, no extra text."""
    )
    chat.with_model("openai", "gpt-4.1-mini")
    
    prompt = f"""Write {count} stories in category: {cat_info['label']}
Topic: {cat_info['prompt']}
Language: {lang_info['instruction']}
Batch #{batch_num} - make stories unique and different.

Return JSON array ONLY:
[
  {{"title": "Story title in {lang}", "content": "Full story text in {lang}"}}
]"""
    
    try:
        response = await chat.send_message(UserMessage(text=prompt))
        text = response.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1] if "\n" in text else text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()
            if text.startswith("json"):
                text = text[4:].strip()
        return json.loads(text)
    except Exception as e:
        print(f"  ERROR batch {batch_num}: {e}")
        return []

async def generate_for_category_lang(category, lang, count_per_batch=10, total=20):
    lang_info = SUPPORTED_STORY_LANGS[lang]
    batches = (total + count_per_batch - 1) // count_per_batch
    generated = 0
    
    for batch_num in range(1, batches + 1):
        count = min(count_per_batch, total - generated)
        print(f"  [{category}/{lang}] Batch {batch_num}/{batches} ({count} stories)...")
        stories = await generate_batch(category, batch_num, count, lang)
        
        for s in stories:
            if not s.get("title") or not s.get("content"):
                continue
            post_id = str(uuid.uuid4())
            doc = {
                "id": post_id,
                "author_id": "system",
                "author_name": lang_info["name"],
                "author_avatar": None,
                "title": s["title"],
                "content": s["content"],
                "category": category,
                "media_type": "text",
                "image_url": None,
                "video_url": None,
                "embed_url": None,
                "thumbnail_url": None,
                "is_embed": False,
                "views_count": random.randint(50, 500),
                "created_at": datetime.utcnow().isoformat(),
                "shares_count": random.randint(5, 50),
                "is_story": True,
                "status": "approved",
                "generated_by": "ai",
                "language": lang,
            }
            await db.posts.insert_one(doc)
            generated += 1
        
        print(f"  [{category}/{lang}] {generated}/{total} done")
        await asyncio.sleep(1)
    
    return generated

async def main():
    # Generate for Arabic first (primary), then other languages
    langs = ["ar", "en", "fr", "de", "tr", "ru", "sv", "nl", "el"]
    count_ar = 30  # Start with 30 per category for Arabic
    count_other = 15  # 15 per category for other languages
    
    total_generated = 0
    
    for lang in langs:
        count = count_ar if lang == "ar" else count_other
        print(f"\n{'='*50}")
        print(f"Language: {lang} ({count} stories per category)")
        print(f"{'='*50}")
        
        for cat in STORY_CATEGORIES_INFO:
            print(f"\nCategory: {cat} ({STORY_CATEGORIES_INFO[cat]['label']})")
            n = await generate_for_category_lang(cat, lang, count_per_batch=10, total=count)
            total_generated += n
            print(f"  ✅ {n} stories generated for {cat}/{lang}")
    
    print(f"\n🎉 Total generated: {total_generated} stories")
    
    # Show count
    count = await db.posts.count_documents({"is_story": True, "generated_by": "ai"})
    print(f"📊 Total AI stories in DB: {count}")

if __name__ == "__main__":
    asyncio.run(main())

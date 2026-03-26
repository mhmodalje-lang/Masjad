"""
Enrich Noor Academy content with proper educational methodology.
Generates rich teaching content for all 240 lessons in Arabic + English.
Uses LLM to transform bare text into real educational material.
"""
import json
import asyncio
import os
import sys
import time

sys.path.insert(0, '/app/backend')
os.environ.setdefault('EMERGENT_LLM_KEY', 'sk-emergent-6369fFa9e095f91F0A')

from emergentintegrations.llm.chat import LlmChat, UserMessage

API_KEY = os.environ.get('EMERGENT_LLM_KEY')

# Import all lesson data to get titles and current content
from data.noor_academy_v2 import (
    NOORANIYA_ALL_LESSONS, ADAB_ALL_LESSONS
)
from data.noor_academy_extended import NOORANIYA_ALL_LESSONS_EXTENDED
from data.noor_academy_aqeedah_fiqh_seerah import AQEEDAH_LESSONS_L2, AQEEDAH_LESSONS_L3
from data.noor_academy_aqeedah_complete import AQEEDAH_L1_COMPLETE, AQEEDAH_L4_COMPLETE, AQEEDAH_L5_COMPLETE
from data.noor_academy_fiqh_content import FIQH_COMPLETE_LESSONS
from data.noor_academy_seerah_content import SEERAH_COMPLETE_LESSONS

ALL_NOORANIYA = NOORANIYA_ALL_LESSONS + NOORANIYA_ALL_LESSONS_EXTENDED
ALL_AQEEDAH = AQEEDAH_L1_COMPLETE + AQEEDAH_LESSONS_L2 + AQEEDAH_LESSONS_L3 + AQEEDAH_L4_COMPLETE + AQEEDAH_L5_COMPLETE
ALL_FIQH = FIQH_COMPLETE_LESSONS
ALL_SEERAH = SEERAH_COMPLETE_LESSONS
ALL_ADAB = ADAB_ALL_LESSONS

SYSTEM_PROMPT = """أنت خبير تعليمي إسلامي متخصص في تعليم الأطفال (6-14 سنة). مهمتك تحويل المحتوى المختصر إلى درس تعليمي غني وشامل.

## قواعد المحتوى:
1. اكتب بأسلوب بسيط ومشوق للأطفال
2. ابدأ بمقدمة تجذب انتباه الطفل (قصة قصيرة أو سؤال أو موقف)
3. اشرح المفهوم خطوة بخطوة بأمثلة من حياة الطفل اليومية
4. أضف قصة إسلامية مرتبطة بالموضوع
5. أضف نصيحة عملية يطبقها الطفل في حياته
6. اجعل المحتوى ممتعاً وتفاعلياً
7. الطول: كل حقل 2-4 جمل (ليس طويلاً جداً)

## بنية المخرج (JSON):
أرجع كائن JSON بالحقول التالية (عربي + إنجليزي):
{
  "intro": {"ar": "مقدمة تشويقية...", "en": "Engaging intro..."},
  "story": {"ar": "قصة قصيرة مرتبطة...", "en": "Short related story..."},
  "explanation": {"ar": "شرح مبسط خطوة بخطوة...", "en": "Simple step-by-step explanation..."},
  "importance": {"ar": "لماذا هذا مهم في حياتنا...", "en": "Why this matters in our life..."},
  "examples": [
    {"ar": "مثال عملي 1", "en": "Practical example 1"},
    {"ar": "مثال عملي 2", "en": "Practical example 2"}
  ],
  "tip": {"ar": "نصيحة عملية...", "en": "Practical tip..."}
}

أرجع JSON فقط بدون أي شرح إضافي."""


async def enrich_lessons(track_name, lessons, batch_size=3):
    """Enrich a batch of lessons with educational content."""
    enriched = {}
    total = len(lessons)
    
    for i in range(0, total, batch_size):
        batch = lessons[i:i+batch_size]
        batch_ids = [l['id'] for l in batch]
        
        # Skip already enriched
        if all(str(lid) in enriched for lid in batch_ids):
            continue
            
        print(f"  [{track_name}] Enriching lessons {batch_ids} ({i+1}-{min(i+batch_size, total)}/{total})...")
        
        # Build prompt
        lessons_desc = []
        for l in batch:
            title_ar = l['title'].get('ar', '') if isinstance(l['title'], dict) else l['title']
            title_en = l['title'].get('en', '') if isinstance(l['title'], dict) else ''
            content_summary = {}
            for k, v in l.get('content', {}).items():
                if isinstance(v, dict) and 'ar' in v:
                    content_summary[k] = v['ar']
                elif isinstance(v, list):
                    content_summary[k] = [item.get('ar', item) if isinstance(item, dict) else item for item in v[:3]]
                elif isinstance(v, str):
                    content_summary[k] = v[:100]
            
            lessons_desc.append(f"""
درس {l['id']}: {title_ar} ({title_en})
المحتوى الحالي: {json.dumps(content_summary, ensure_ascii=False)[:300]}
""")
        
        prompt = f"""حوّل هذه الدروس إلى محتوى تعليمي غني للأطفال.

مسار: {track_name}
{''.join(lessons_desc)}

أرجع JSON object واحد بهذا الشكل:
{{
  "{batch[0]['id']}": {{ "intro": {{"ar": "...", "en": "..."}}, "story": {{"ar": "...", "en": "..."}}, "explanation": {{"ar": "...", "en": "..."}}, "importance": {{"ar": "...", "en": "..."}}, "examples": [{{"ar": "...", "en": "..."}}, {{"ar": "...", "en": "..."}}], "tip": {{"ar": "...", "en": "..."}} }}
  {', '.join(f'"{l["id"]}": {{...}}' for l in batch[1:])}
}}

أرجع JSON فقط:"""

        chat = LlmChat(
            api_key=API_KEY,
            session_id=f"enrich-{track_name}-{i}",
            system_message=SYSTEM_PROMPT
        )
        chat.with_model("openai", "gpt-4.1-mini")
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = await chat.send_message(UserMessage(text=prompt))
                text = response.strip()
                if text.startswith('```'):
                    text = text.split('\n', 1)[1] if '\n' in text else text[3:]
                    if text.endswith('```'):
                        text = text[:-3]
                    text = text.strip()
                    if text.startswith('json'):
                        text = text[4:].strip()
                
                result = json.loads(text)
                
                for lid in batch_ids:
                    key = str(lid)
                    if key in result:
                        enriched[key] = result[key]
                    else:
                        print(f"    WARNING: Lesson {lid} not in response")
                
                break
            except Exception as e:
                print(f"    Retry {attempt+1}: {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(2)
        
        await asyncio.sleep(0.3)
    
    return enriched


async def main():
    output_path = '/app/backend/data/academy_enriched.json'
    
    # Load existing if any
    if os.path.exists(output_path):
        with open(output_path, 'r', encoding='utf-8') as f:
            all_enriched = json.load(f)
        print(f"Loaded existing: {len(all_enriched)} tracks")
    else:
        all_enriched = {}
    
    tracks = {
        'aqeedah': ALL_AQEEDAH,
        'fiqh': ALL_FIQH,
        'seerah': ALL_SEERAH,
        'nooraniya': ALL_NOORANIYA,
        'adab': ALL_ADAB,
    }
    
    for track_name, lessons in tracks.items():
        print(f"\n{'='*50}")
        print(f"Track: {track_name} ({len(lessons)} lessons)")
        print(f"{'='*50}")
        
        if track_name in all_enriched and len(all_enriched[track_name]) >= len(lessons):
            print(f"  Already enriched ({len(all_enriched[track_name])} lessons). Skipping.")
            continue
        
        existing = all_enriched.get(track_name, {})
        
        # Filter out already enriched
        to_enrich = [l for l in lessons if str(l['id']) not in existing]
        
        if not to_enrich:
            print(f"  All lessons already enriched.")
            continue
            
        print(f"  {len(to_enrich)} lessons to enrich...")
        
        result = await enrich_lessons(track_name, to_enrich, batch_size=3)
        
        # Merge with existing
        if track_name not in all_enriched:
            all_enriched[track_name] = {}
        all_enriched[track_name].update(result)
        
        # Save after each track
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(all_enriched, f, ensure_ascii=False, indent=1)
        
        print(f"  Saved {len(all_enriched[track_name])} enriched lessons for {track_name}")
    
    # Final stats
    print(f"\n{'='*50}")
    print(f"ENRICHMENT COMPLETE!")
    total = 0
    for track, data in all_enriched.items():
        print(f"  {track}: {len(data)} lessons enriched")
        total += len(data)
    print(f"  TOTAL: {total} lessons")
    print(f"{'='*50}")


if __name__ == '__main__':
    asyncio.run(main())

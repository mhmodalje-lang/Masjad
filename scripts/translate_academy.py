"""
Translate all 913 unique strings to 7 languages using LLM.
Uses batches of ~30 strings per API call for efficiency.
Output: academy_translations.json
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

LANG_NAMES = {
    'de': 'German',
    'fr': 'French', 
    'tr': 'Turkish',
    'ru': 'Russian',
    'sv': 'Swedish',
    'nl': 'Dutch',
    'el': 'Greek'
}

BATCH_SIZE = 40  # strings per batch

SYSTEM_PROMPT = """You are an expert translator specializing in Islamic educational content for children.

RULES:
1. Translate the given English texts to {lang_name} ({lang_code}).
2. The content is for Islamic education (Quran, Aqeedah, Fiqh, Seerah, Arabic) for children aged 6-14.
3. Keep Islamic terms like Allah, Quran, Sunnah, Hadith, Salah, Wudu, etc. as-is (don't translate them).
4. For Quranic verses (text between ﴿﴾), translate the MEANING only, keep the Arabic verse markers.
5. Use simple, clear language appropriate for children.
6. Be culturally sensitive and religiously accurate.
7. The Arabic text is provided for context — translate from English, not Arabic.
8. Return ONLY a JSON array of translated strings, in the SAME ORDER as input.
9. Each element should be just the translated string, nothing else.
10. Do NOT add explanations or notes.
11. Keep numbers, dates, and proper nouns as-is.
12. For quiz options, keep them short and clear."""


async def translate_batch(strings_batch, lang_code, lang_name, batch_num, total_batches):
    """Translate a batch of strings to a target language."""
    chat = LlmChat(
        api_key=API_KEY,
        session_id=f"translate-{lang_code}-batch-{batch_num}",
        system_message=SYSTEM_PROMPT.format(lang_name=lang_name, lang_code=lang_code)
    )
    chat.with_model("openai", "gpt-4.1-mini")
    
    # Build the prompt with numbered strings
    lines = []
    for i, s in enumerate(strings_batch):
        lines.append(f'{i+1}. EN: "{s["en"]}"')
        if s.get("ar"):
            lines.append(f'   AR context: {s["ar"]}')
    
    prompt = f"""Translate these {len(strings_batch)} texts to {lang_name}.
Return a JSON array with exactly {len(strings_batch)} translated strings.

{chr(10).join(lines)}

Return ONLY the JSON array, no markdown, no explanation:"""
    
    user_msg = UserMessage(text=prompt)
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = await chat.send_message(user_msg)
            
            # Parse the response - try to extract JSON array
            text = response.strip()
            # Remove markdown code fences if present
            if text.startswith('```'):
                text = text.split('\n', 1)[1] if '\n' in text else text[3:]
                if text.endswith('```'):
                    text = text[:-3]
                text = text.strip()
                if text.startswith('json'):
                    text = text[4:].strip()
            
            translations = json.loads(text)
            
            if len(translations) != len(strings_batch):
                print(f"  WARNING: Expected {len(strings_batch)} translations, got {len(translations)} for {lang_code} batch {batch_num}")
                # Pad or truncate
                while len(translations) < len(strings_batch):
                    translations.append(strings_batch[len(translations)]["en"])
                translations = translations[:len(strings_batch)]
            
            return translations
            
        except Exception as e:
            print(f"  Retry {attempt+1}/{max_retries} for {lang_code} batch {batch_num}: {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(2)
    
    # Fallback: return English texts
    print(f"  FAILED: {lang_code} batch {batch_num} — using English fallback")
    return [s["en"] for s in strings_batch]


async def main():
    # Load strings to translate
    with open('/app/backend/data/strings_to_translate.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    strings = data['strings']
    total = len(strings)
    print(f"Total strings to translate: {total}")
    print(f"Target languages: {list(LANG_NAMES.keys())}")
    print(f"Batch size: {BATCH_SIZE}")
    
    # Split into batches
    batches = []
    for i in range(0, total, BATCH_SIZE):
        batches.append(strings[i:i+BATCH_SIZE])
    
    total_batches = len(batches)
    print(f"Total batches per language: {total_batches}")
    print(f"Total API calls: {total_batches * len(LANG_NAMES)}")
    
    # Load existing translations if any
    output_path = '/app/backend/data/academy_translations.json'
    if os.path.exists(output_path):
        with open(output_path, 'r', encoding='utf-8') as f:
            translations = json.load(f)
        print(f"Loaded existing translations: {len(translations)} entries")
    else:
        translations = {}
    
    # Translate for each language
    for lang_code, lang_name in LANG_NAMES.items():
        print(f"\n{'='*60}")
        print(f"Translating to {lang_name} ({lang_code})...")
        print(f"{'='*60}")
        
        # Check how many already translated
        already_done = sum(1 for s in strings if s['en'] in translations and lang_code in translations[s['en']])
        if already_done == total:
            print(f"  All {total} strings already translated to {lang_name}. Skipping.")
            continue
        
        start_time = time.time()
        
        for batch_idx, batch in enumerate(batches):
            # Skip if all strings in batch already translated
            all_done = all(s['en'] in translations and lang_code in translations[s['en']] for s in batch)
            if all_done:
                continue
            
            print(f"  Batch {batch_idx+1}/{total_batches} ({len(batch)} strings)...")
            
            translated = await translate_batch(batch, lang_code, lang_name, batch_idx, total_batches)
            
            # Store translations
            for s, t in zip(batch, translated):
                en_key = s['en']
                if en_key not in translations:
                    translations[en_key] = {}
                translations[en_key][lang_code] = t
            
            # Save after each batch (incremental)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(translations, f, ensure_ascii=False, indent=1)
            
            # Rate limiting
            await asyncio.sleep(0.5)
        
        elapsed = time.time() - start_time
        print(f"  {lang_name} done in {elapsed:.1f}s")
    
    # Final save
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(translations, f, ensure_ascii=False, indent=1)
    
    # Stats
    print(f"\n{'='*60}")
    print(f"TRANSLATION COMPLETE!")
    print(f"Total entries: {len(translations)}")
    for lang_code in LANG_NAMES:
        count = sum(1 for v in translations.values() if lang_code in v)
        print(f"  {lang_code}: {count}/{total} strings translated")
    print(f"Saved to: {output_path}")
    print(f"{'='*60}")


if __name__ == '__main__':
    asyncio.run(main())

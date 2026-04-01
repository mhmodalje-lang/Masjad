"""
Batch translator for Noor Academy content.
Translates missing texts in academy_translations.json using Emergent LLM.
"""
import asyncio
import json
import os
import sys

sys.path.insert(0, '/app/backend')
from dotenv import load_dotenv
load_dotenv('/app/backend/.env')

from emergentintegrations.llm.chat import LlmChat, UserMessage

EMERGENT_KEY = os.environ.get('EMERGENT_LLM_KEY', '')
TRANSLATIONS_PATH = '/app/backend/data/academy_translations.json'

LANG_NAMES = {
    'tr': 'Turkish', 'ru': 'Russian', 'sv': 'Swedish',
    'nl': 'Dutch', 'el': 'Greek', 'fr': 'French'
}

async def translate_batch(texts: list, target_lang: str, lang_name: str) -> dict:
    """Translate a batch of English texts to target language."""
    chat = LlmChat(
        api_key=EMERGENT_KEY,
        session_id=f"translate-{target_lang}-{hash(str(texts[:3]))}",
        system_message=f"""You are a professional translator for an Islamic educational app for children.
Translate the following English texts to {lang_name}. 
Rules:
- Keep Islamic terms (Allah, Quran, Hadith, Sunnah, etc.) as-is or use the standard {lang_name} transliteration
- Keep Arabic text/letters as-is (don't translate Arabic script)
- Keep the tone child-friendly and educational
- Return ONLY a valid JSON object mapping each English text to its {lang_name} translation
- No explanations, just the JSON"""
    ).with_model("gemini", "gemini-2.5-flash")

    # Build the prompt
    numbered = {}
    for i, text in enumerate(texts):
        numbered[str(i)] = text
    
    prompt = f"Translate these {len(texts)} English texts to {lang_name}. Return a JSON object with the same keys:\n\n{json.dumps(numbered, ensure_ascii=False)}"
    
    msg = UserMessage(text=prompt)
    response = await chat.send_message(msg)
    
    # Parse JSON response
    try:
        # Clean response - remove markdown code blocks if present
        clean = response.strip()
        if clean.startswith('```'):
            clean = clean.split('\n', 1)[1] if '\n' in clean else clean[3:]
            if clean.endswith('```'):
                clean = clean[:-3]
            clean = clean.strip()
            if clean.startswith('json'):
                clean = clean[4:].strip()
        
        result = json.loads(clean)
        translations = {}
        for i, text in enumerate(texts):
            translated = result.get(str(i), '')
            if translated:
                translations[text] = translated
        return translations
    except json.JSONDecodeError as e:
        print(f"  JSON parse error: {e}")
        return {}

async def main():
    with open(TRANSLATIONS_PATH) as f:
        all_translations = json.load(f)
    
    target_langs = ['tr', 'ru', 'sv', 'nl', 'el', 'fr']
    batch_size = 20  # Translate 20 texts at a time
    
    for lang in target_langs:
        lang_name = LANG_NAMES[lang]
        
        # Find missing texts
        missing = []
        for text, langs in all_translations.items():
            if lang not in langs:
                missing.append(text)
        
        if not missing:
            print(f"✅ {lang_name} ({lang}): All translations complete!")
            continue
        
        print(f"\n🔄 {lang_name} ({lang}): {len(missing)} texts to translate")
        
        translated_count = 0
        for i in range(0, len(missing), batch_size):
            batch = missing[i:i + batch_size]
            try:
                results = await translate_batch(batch, lang, lang_name)
                for en_text, translated in results.items():
                    if en_text in all_translations:
                        all_translations[en_text][lang] = translated
                        translated_count += 1
                
                print(f"  Batch {i//batch_size + 1}/{(len(missing) + batch_size - 1)//batch_size}: +{len(results)} translations")
                
                # Save periodically every 5 batches
                if (i // batch_size) % 5 == 4:
                    with open(TRANSLATIONS_PATH, 'w', encoding='utf-8') as f:
                        json.dump(all_translations, f, ensure_ascii=False, indent=None)
                    print(f"  💾 Saved progress ({translated_count} total for {lang})")
                
            except Exception as e:
                print(f"  ❌ Batch error: {e}")
                await asyncio.sleep(2)
                continue
            
            await asyncio.sleep(0.5)  # Rate limiting
        
        print(f"✅ {lang_name}: {translated_count} new translations added")
    
    # Final save
    with open(TRANSLATIONS_PATH, 'w', encoding='utf-8') as f:
        json.dump(all_translations, f, ensure_ascii=False, indent=None)
    print(f"\n💾 All translations saved to {TRANSLATIONS_PATH}")

if __name__ == "__main__":
    asyncio.run(main())

"""
Batch translate dua translations from English to all target languages
using OpenAI GPT via emergentintegrations with Islamic context.
"""
import asyncio
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'backend'))
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / 'backend' / '.env')

from emergentintegrations.llm.chat import LlmChat, UserMessage

EMERGENT_LLM_KEY = os.environ.get('EMERGENT_LLM_KEY')
LOCALES_DIR = Path(__file__).parent.parent / 'frontend' / 'src' / 'locales'

# Languages to translate to (excluding ar and en which are source)
TARGET_LANGUAGES = {
    'sv': 'Swedish',
    'nl': 'Dutch', 
    'el': 'Greek',
    'de': 'German',
    'ru': 'Russian',
    'fr': 'French',
    'tr': 'Turkish',
}

async def translate_batch(texts: dict, target_lang: str, target_name: str) -> dict:
    """Translate a batch of key-value pairs to the target language."""
    chat = LlmChat(
        api_key=EMERGENT_LLM_KEY,
        session_id=f"translate-duas-{target_lang}-{id(texts)}",
        system_message=f"""You are a professional Islamic text translator. Translate the given English Islamic texts to {target_name}.

RULES:
1. Preserve the spiritual and Islamic meaning accurately
2. Use proper Islamic terminology in {target_name}
3. Keep proper nouns (Allah, Muhammad, Ibrahim, etc.) in their commonly accepted form in {target_name}
4. Do NOT translate Arabic Quran references or hadith source names - keep them as-is
5. Return ONLY valid JSON - no markdown, no explanation
6. The output must be a JSON object with the same keys, but values translated to {target_name}"""
    )

    # Split into smaller chunks (max ~30 items per request)
    chunk_size = 30
    keys = list(texts.keys())
    all_translated = {}

    for i in range(0, len(keys), chunk_size):
        chunk_keys = keys[i:i + chunk_size]
        chunk = {k: texts[k] for k in chunk_keys}
        
        prompt = f"Translate these Islamic texts to {target_name}. Return ONLY a JSON object with the same keys and translated values:\n\n{json.dumps(chunk, ensure_ascii=False, indent=2)}"
        
        try:
            response = await chat.send_message(UserMessage(text=prompt))
            # Extract JSON from response
            resp_text = response.strip()
            # Remove markdown code blocks if present
            if resp_text.startswith('```'):
                resp_text = resp_text.split('\n', 1)[1] if '\n' in resp_text else resp_text[3:]
                if resp_text.endswith('```'):
                    resp_text = resp_text[:-3]
                resp_text = resp_text.strip()
            
            translated = json.loads(resp_text)
            all_translated.update(translated)
            print(f"  [{target_lang}] Translated chunk {i//chunk_size + 1}/{(len(keys) + chunk_size - 1)//chunk_size}")
        except Exception as e:
            print(f"  [{target_lang}] Error translating chunk {i//chunk_size + 1}: {e}")
            # Keep English as fallback for failed chunks
            all_translated.update(chunk)
    
    return all_translated


async def main():
    print("=" * 60)
    print("BATCH DUA TRANSLATION SCRIPT")
    print("=" * 60)
    
    # Load English translations as source
    en_path = LOCALES_DIR / 'en.json'
    with open(en_path, 'r') as f:
        en_data = json.load(f)
    
    # Extract dua-related keys (translationKeys from duas.ts)
    dua_keys = {k: v for k, v in en_data.items() if k.startswith('dua')}
    print(f"\nFound {len(dua_keys)} dua-related keys to translate")
    
    for lang_code, lang_name in TARGET_LANGUAGES.items():
        print(f"\n--- Translating to {lang_name} ({lang_code}) ---")
        
        # Load current locale file
        locale_path = LOCALES_DIR / f'{lang_code}.json'
        with open(locale_path, 'r') as f:
            locale_data = json.load(f)
        
        # Find keys that are still English (not translated yet)
        # A key is "not translated" if its value matches the English value
        keys_to_translate = {}
        for k, en_val in dua_keys.items():
            current_val = locale_data.get(k, '')
            # If the value is the same as English, it needs translation
            if current_val == en_val or not current_val:
                keys_to_translate[k] = en_val
        
        if not keys_to_translate:
            print(f"  All dua keys already translated for {lang_code}!")
            continue
        
        print(f"  {len(keys_to_translate)} keys need translation")
        
        translated = await translate_batch(keys_to_translate, lang_code, lang_name)
        
        # Update locale file
        for k, v in translated.items():
            locale_data[k] = v
        
        with open(locale_path, 'w') as f:
            json.dump(locale_data, f, ensure_ascii=False, indent=2)
        
        print(f"  Updated {locale_path.name} with {len(translated)} translations")
    
    print("\n" + "=" * 60)
    print("TRANSLATION COMPLETE!")
    print("=" * 60)


if __name__ == '__main__':
    asyncio.run(main())

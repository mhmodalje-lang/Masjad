"""
Fix Arabic text in English locale file and translate to all languages.
"""
import asyncio
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'backend'))
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / 'backend' / '.env')

from emergentintegrations.llm.chat import LlmChat, UserMessage

EMERGENT_LLM_KEY = os.environ.get('EMERGENT_LLM_KEY')
LOCALES_DIR = Path(__file__).parent.parent / 'frontend' / 'src' / 'locales'

TARGET_LANGUAGES = {
    'en': 'English',
    'sv': 'Swedish',
    'nl': 'Dutch',
    'el': 'Greek',
    'de': 'German',
    'ru': 'Russian',
    'fr': 'French',
    'tr': 'Turkish',
}

arabic_pattern = re.compile(r'[\u0600-\u06FF]')

async def translate_chunk(keys_values: dict, target_lang: str, target_name: str, session_suffix: str) -> dict:
    chat = LlmChat(
        api_key=EMERGENT_LLM_KEY,
        session_id=f"fix-arabic-{target_lang}-{session_suffix}",
        system_message=f"""You are a professional Islamic text translator specializing in {target_name} translations.

RULES:
1. Translate Arabic Islamic duas/prayers/supplications to {target_name}
2. Preserve the spiritual Islamic meaning with utmost accuracy
3. Keep proper nouns like Allah, Muhammad in their accepted {target_name} form
4. For short dhikr (like "SubhanAllah"), provide the meaning translation
5. Return ONLY a valid JSON object with same keys and translated values
6. No markdown, no explanation - just the JSON"""
    )

    prompt = f"Translate these Arabic Islamic texts to {target_name}. Return ONLY a JSON object:\n\n{json.dumps(keys_values, ensure_ascii=False, indent=2)}"
    
    try:
        response = await chat.send_message(UserMessage(text=prompt))
        resp_text = response.strip()
        if resp_text.startswith('```'):
            lines = resp_text.split('\n')
            resp_text = '\n'.join(lines[1:])
            if resp_text.endswith('```'):
                resp_text = resp_text[:-3]
            resp_text = resp_text.strip()
        return json.loads(resp_text)
    except Exception as e:
        print(f"  Error: {e}")
        return keys_values


async def main():
    print("=" * 60)
    print("FIX ARABIC TEXT IN ALL LOCALE FILES")
    print("=" * 60)

    # Load English to find Arabic-text keys
    with open(LOCALES_DIR / 'en.json', 'r') as f:
        en_data = json.load(f)

    arabic_keys = {k: v for k, v in en_data.items() if k.startswith('dua') and arabic_pattern.search(str(v))}
    print(f"\nFound {len(arabic_keys)} keys with Arabic text in en.json")

    # Process each language
    for lang_code, lang_name in TARGET_LANGUAGES.items():
        print(f"\n--- Translating {len(arabic_keys)} keys to {lang_name} ({lang_code}) ---")
        
        locale_path = LOCALES_DIR / f'{lang_code}.json'
        with open(locale_path, 'r') as f:
            locale_data = json.load(f)

        # Split into chunks of 25
        keys = list(arabic_keys.keys())
        all_translated = {}
        
        for i in range(0, len(keys), 25):
            chunk_keys = keys[i:i + 25]
            chunk = {k: arabic_keys[k] for k in chunk_keys}
            result = await translate_chunk(chunk, lang_code, lang_name, str(i))
            all_translated.update(result)
            print(f"  Chunk {i//25 + 1}/{(len(keys) + 24)//25} done")

        for k, v in all_translated.items():
            locale_data[k] = v

        with open(locale_path, 'w') as f:
            json.dump(locale_data, f, ensure_ascii=False, indent=2)
        print(f"  Updated {lang_code}.json")

    print("\n" + "=" * 60)
    print("ALL ARABIC TEXT FIXED!")
    print("=" * 60)

if __name__ == '__main__':
    asyncio.run(main())

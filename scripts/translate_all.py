"""
Comprehensive translation script for all 9 languages.
Translates all untranslated (English-same) keys using LLM.
"""
import json, os, re, asyncio

from emergentintegrations.llm.chat import LlmChat, UserMessage

API_KEY = "sk-emergent-72d7cF9FbB1E629002"
LOCALES_DIR = '/app/frontend/src/locales'

# Language names for LLM prompt
LANG_NAMES = {
    'de': 'German',
    'de-AT': 'Austrian German',
    'fr': 'French',
    'nl': 'Dutch',
    'sv': 'Swedish',
    'el': 'Greek',
    'ru': 'Russian',
    'tr': 'Turkish',
}

def load_locales():
    locales = {}
    for fname in sorted(os.listdir(LOCALES_DIR)):
        if fname.endswith('.json'):
            lang = fname.replace('.json', '')
            with open(f'{LOCALES_DIR}/{fname}', encoding='utf-8') as f:
                locales[lang] = json.load(f)
    return locales

def find_untranslated(en_data, lang_data, lang_code):
    """Find keys where the translation is same as English (untranslated)."""
    untranslated = {}
    skip_patterns = ['arabic', 'urdu', 'english', 'french', 'german', 'turkish',
                     'russian', 'swedish', 'dutch', 'greek', 'indonesian',
                     'iban', 'appName', 'appTitle', 'alhamdulillah', 'allahuAkbar',
                     'subhanAllah', 'bismillah', 'assalamu', 'jazakAllah',
                     'masjid', 'halal', 'haram', 'hajj', 'umrah', 'zakat',
                     'sadaqah', 'sunnah', 'fajr', 'dhuhr', 'asr', 'maghrib', 'isha',
                     'WhatsApp', 'Email', 'IBAN', 'PayPal', 'YouTube', 'Facebook',
                     'Instagram', 'TikTok', 'Telegram', 'Gmail']
    
    for k, v in en_data.items():
        if k not in lang_data:
            untranslated[k] = v
            continue
        lang_val = lang_data[k]
        if not lang_val or lang_val.strip() == '':
            untranslated[k] = v
            continue
        if lang_val == v and len(v) > 3:
            if any(p.lower() in k.lower() or p.lower() in v.lower() for p in skip_patterns):
                continue
            untranslated[k] = v
    
    return untranslated

async def translate_batch(keys_values: dict, target_lang: str, lang_name: str) -> dict:
    """Translate a batch of key-value pairs to the target language."""
    chat = LlmChat(
        api_key=API_KEY,
        session_id=f"translate-{target_lang}-{id(keys_values)}",
        system_message=f"""You are an expert translator for an Islamic mobile app called "Azan & Hikaya". 
Translate the following English UI strings to {lang_name}. 
Rules:
1. Keep Islamic terms like Allah, Quran, Hadith, Surah, Ayah, Dua, Dhikr, Tasbeeh in their common transliterated form for {lang_name}
2. Keep proper nouns in their common {lang_name} form
3. Keep any HTML tags, emojis, or special formatting as-is
4. Keep placeholder variables like {{{{count}}}}, {{{{name}}}} etc as-is
5. Be natural and fluent in {lang_name}
6. Return ONLY a valid JSON object with the same keys but translated values
7. Do NOT add any text before or after the JSON"""
    )

    json_str = json.dumps(keys_values, ensure_ascii=False, indent=2)
    msg = UserMessage(text=f"Translate these UI strings to {lang_name}. Return ONLY valid JSON:\n\n{json_str}")
    
    response = await chat.send_message(msg)
    
    try:
        json_match = re.search(r'\{[\s\S]*\}', response)
        if json_match:
            translated = json.loads(json_match.group())
            return translated
    except json.JSONDecodeError:
        pass
    
    return {}

async def translate_language(en_data, lang_data, lang_code, lang_name):
    """Translate all untranslated keys for a language."""
    untranslated = find_untranslated(en_data, lang_data, lang_code)
    
    if not untranslated:
        print(f"  OK {lang_code} ({lang_name}): No untranslated keys")
        return lang_data, 0
    
    print(f"  TRANSLATING {lang_code} ({lang_name}): {len(untranslated)} keys")
    
    batch_size = 60
    keys = list(untranslated.keys())
    total_translated = 0
    
    for i in range(0, len(keys), batch_size):
        batch_keys = keys[i:i+batch_size]
        batch = {k: untranslated[k] for k in batch_keys}
        
        try:
            translated = await translate_batch(batch, lang_code, lang_name)
            if translated:
                for k, v in translated.items():
                    if k in untranslated and v and len(v) > 0:
                        lang_data[k] = v
                        total_translated += 1
                print(f"    Batch {i//batch_size + 1}: {len(translated)}/{len(batch)} done")
            else:
                print(f"    Batch {i//batch_size + 1}: Failed")
        except Exception as e:
            print(f"    Batch {i//batch_size + 1}: Error: {str(e)[:100]}")
    
    return lang_data, total_translated

async def main():
    locales = load_locales()
    en = locales['en']
    
    print("=" * 60)
    print("COMPREHENSIVE TRANSLATION - ALL LANGUAGES")
    print("=" * 60)
    
    total_fixed = 0
    langs_to_fix = ['el', 'nl', 'sv', 'de-AT', 'fr', 'de', 'ru', 'tr']
    
    for lang_code in langs_to_fix:
        if lang_code not in locales or lang_code not in LANG_NAMES:
            continue
        
        lang_data = locales[lang_code]
        lang_name = LANG_NAMES[lang_code]
        
        updated_data, count = await translate_language(en, lang_data, lang_code, lang_name)
        
        if count > 0:
            with open(f'{LOCALES_DIR}/{lang_code}.json', 'w', encoding='utf-8') as f:
                json.dump(updated_data, f, ensure_ascii=False, indent=2)
            print(f"  SAVED {lang_code}.json ({count} new translations)")
            total_fixed += count
    
    print(f"\nTOTAL: {total_fixed} translations added")

if __name__ == '__main__':
    asyncio.run(main())

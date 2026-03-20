#!/usr/bin/env python3
"""
Batch translate missing locale keys using GPT-5.2 via Emergent LLM Key.
Also creates Austrian-German (de-AT) locale.
"""
import json
import os
import sys
import asyncio
from dotenv import load_dotenv

load_dotenv('/app/backend/.env')

from emergentintegrations.llm.chat import LlmChat, UserMessage

API_KEY = os.environ.get('EMERGENT_LLM_KEY')
LOCALES_DIR = '/app/frontend/src/locales'

# Language configs for translation
LANG_CONFIG = {
    'ar': {
        'name': 'Arabic',
        'native': 'العربية',
        'system': 'You are an expert Arabic translator specializing in Islamic apps. Translate UI strings to Modern Standard Arabic. For Islamic terms, use the proper Arabic terminology (e.g., الصلاة, الزكاة, القرآن). Keep translations natural and culturally appropriate for Arabic-speaking Muslims.'
    },
    'de': {
        'name': 'German',
        'native': 'Deutsch',
        'system': 'You are an expert German translator specializing in Islamic apps. Translate UI strings to standard German (Hochdeutsch). Use proper German grammar with correct noun genders and cases. For Islamic terms, use commonly accepted German transliterations (e.g., Gebet for Prayer, Koran for Quran). Keep translations natural for German-speaking Muslims.'
    },
    'el': {
        'name': 'Greek',
        'native': 'Ελληνικά',
        'system': 'You are an expert Greek translator specializing in Islamic apps. Translate UI strings to Modern Greek. For Islamic terms, use commonly used Greek transliterations. Keep translations natural for Greek-speaking Muslims.'
    },
    'fr': {
        'name': 'French',
        'native': 'Français',
        'system': 'You are an expert French translator specializing in Islamic apps. Translate UI strings to standard French. Use proper French grammar with correct articles and agreements. For Islamic terms, use commonly accepted French translations (e.g., Prière for Prayer, Coran for Quran). Keep translations natural for French-speaking Muslims.'
    },
    'ru': {
        'name': 'Russian',
        'native': 'Русский',
        'system': 'You are an expert Russian translator specializing in Islamic apps. Translate UI strings to standard Russian. Use proper Russian grammar with correct cases and agreements. For Islamic terms, use commonly accepted Russian transliterations (e.g., Намаз for Prayer, Коран for Quran). Keep translations natural for Russian-speaking Muslims.'
    },
    'tr': {
        'name': 'Turkish',
        'native': 'Türkçe',
        'system': 'You are an expert Turkish translator specializing in Islamic apps. Translate UI strings to standard Turkish. Use proper Turkish grammar with vowel harmony. For Islamic terms, use commonly used Turkish terms (e.g., Namaz for Prayer, Kuran for Quran, İmsak, Öğle, İkindi, Akşam, Yatsı for prayer names). Keep translations natural for Turkish-speaking Muslims.'
    },
    'sv': {
        'name': 'Swedish',
        'native': 'Svenska',
        'system': 'You are an expert Swedish translator specializing in Islamic apps. Translate UI strings to standard Swedish. For Islamic terms, use commonly accepted Swedish translations. Keep translations natural for Swedish-speaking Muslims.'
    },
    'nl': {
        'name': 'Dutch',
        'native': 'Nederlands',
        'system': 'You are an expert Dutch translator specializing in Islamic apps. Translate UI strings to standard Dutch. For Islamic terms, use commonly accepted Dutch translations. Keep translations natural for Dutch-speaking Muslims.'
    },
    'de-AT': {
        'name': 'Austrian German',
        'native': 'Österreichisches Deutsch',
        'system': 'You are an expert Austrian German translator specializing in Islamic apps. Translate UI strings to Austrian German dialect. Use Austrian-specific terms: Jänner (not Januar), Feber (not Februar), heuer (not dieses Jahr), Erdäpfel (not Kartoffeln), Paradeiser (not Tomaten), Sackerl (not Tüte), Beisl (not Kneipe), Topfen (not Quark), Schlagobers (not Sahne), Palatschinken (not Pfannkuchen). Use Austrian greeting style "Grüß Gott" and "Servus". For Islamic terms, use the same as German but with Austrian flavor. Keep translations warm and natural for Austrian Muslims in Wien, Graz, Linz, etc.'
    }
}

async def translate_batch(lang_code: str, keys_dict: dict, batch_size: int = 50) -> dict:
    """Translate a batch of keys for a specific language."""
    config = LANG_CONFIG[lang_code]
    all_translations = {}
    
    keys_list = list(keys_dict.items())
    total_batches = (len(keys_list) + batch_size - 1) // batch_size
    
    for i in range(0, len(keys_list), batch_size):
        batch = dict(keys_list[i:i+batch_size])
        batch_num = (i // batch_size) + 1
        print(f"  [{lang_code}] Translating batch {batch_num}/{total_batches} ({len(batch)} keys)...")
        
        chat = LlmChat(
            api_key=API_KEY,
            session_id=f"translate-{lang_code}-{batch_num}",
            system_message=config['system']
        )
        chat.with_model("openai", "gpt-5.2")
        
        prompt = f"""Translate the following JSON key-value pairs from English to {config['name']} ({config['native']}).

RULES:
1. Return ONLY valid JSON - no markdown, no code blocks, no explanation
2. Keep the JSON keys EXACTLY the same (don't translate keys)
3. Translate only the values
4. For Islamic terms, use culturally appropriate {config['name']} terminology
5. Keep translations concise (similar length to English)
6. Do NOT add quotes around the entire JSON, return raw JSON object

Input:
{json.dumps(batch, ensure_ascii=False, indent=2)}"""

        msg = UserMessage(text=prompt)
        
        try:
            response = await chat.send_message(msg)
            # Clean the response - remove markdown code blocks if present
            cleaned = response.strip()
            if cleaned.startswith('```'):
                cleaned = cleaned.split('\n', 1)[1] if '\n' in cleaned else cleaned[3:]
                if cleaned.endswith('```'):
                    cleaned = cleaned[:-3]
                cleaned = cleaned.strip()
            if cleaned.startswith('json'):
                cleaned = cleaned[4:].strip()
            
            translated = json.loads(cleaned)
            all_translations.update(translated)
            print(f"  [{lang_code}] Batch {batch_num} OK: {len(translated)} keys translated")
        except Exception as e:
            print(f"  [{lang_code}] Batch {batch_num} ERROR: {e}")
            # Fallback: use English values
            all_translations.update(batch)
    
    return all_translations


async def main():
    print("=" * 60)
    print("TRANSLATION SYNC - Filling missing keys for all languages")
    print("=" * 60)
    
    # Load English reference
    with open(f'{LOCALES_DIR}/en.json') as f:
        en = json.load(f)
    print(f"Reference (en): {len(en)} keys\n")
    
    # Process each language with missing keys
    languages_to_process = ['ar', 'de', 'el', 'fr', 'ru', 'tr']
    
    for lang in languages_to_process:
        locale_path = f'{LOCALES_DIR}/{lang}.json'
        with open(locale_path) as f:
            current = json.load(f)
        
        missing_keys = {k: en[k] for k in en if k not in current}
        
        if not missing_keys:
            print(f"[{lang}] Already complete ({len(current)} keys)")
            continue
        
        print(f"\n[{lang}] Translating {len(missing_keys)} missing keys...")
        translations = await translate_batch(lang, missing_keys)
        
        # Merge translations into current locale
        current.update(translations)
        
        # Sort keys to match English order
        sorted_locale = {k: current[k] for k in sorted(current.keys())}
        
        with open(locale_path, 'w') as f:
            json.dump(sorted_locale, f, ensure_ascii=False, indent=2)
        
        print(f"[{lang}] DONE: {len(sorted_locale)} total keys (added {len(translations)})")
    
    # Create Austrian German (de-AT) based on German (de)
    print(f"\n{'='*60}")
    print("Creating Austrian German (de-AT) locale...")
    print("=" * 60)
    
    with open(f'{LOCALES_DIR}/de.json') as f:
        de = json.load(f)
    
    # Translate ALL keys from English to Austrian German
    print(f"[de-AT] Translating all {len(en)} keys to Austrian German...")
    
    # Start from German as base, then adapt
    de_at = dict(de)  # Copy German as base
    
    # Now translate a selection of keys that would differ in Austrian German
    # Focus on month names, common UI terms, greetings, etc.
    austrian_adaptation_keys = {}
    
    # Select keys that are likely to differ between German and Austrian German
    adaptation_candidates = [
        'welcome', 'greeting', 'january', 'february', 'settings', 'home',
        'search', 'profile', 'save', 'cancel', 'delete', 'add', 'edit',
        'back', 'next', 'loading', 'error', 'success', 'confirm',
        'prayerTimes', 'fajr', 'dhuhr', 'asr', 'maghrib', 'isha',
        'quran', 'duas', 'tasbeeh', 'qibla', 'more', 'explore',
        'ramadan', 'zakat', 'sadaqah', 'hajj', 'umrah',
        'appName', 'appDescription', 'installApp', 'update',
        'language', 'notifications', 'theme', 'about',
    ]
    
    # Get all keys that exist in en for Austrian adaptation
    for key in en:
        austrian_adaptation_keys[key] = en[key]
    
    # Translate all keys for de-AT
    translations = await translate_batch('de-AT', austrian_adaptation_keys, batch_size=80)
    de_at.update(translations)
    
    # Ensure all en keys exist
    for key in en:
        if key not in de_at:
            de_at[key] = de.get(key, en[key])
    
    sorted_de_at = {k: de_at[k] for k in sorted(de_at.keys())}
    
    with open(f'{LOCALES_DIR}/de-AT.json', 'w') as f:
        json.dump(sorted_de_at, f, ensure_ascii=False, indent=2)
    
    print(f"[de-AT] DONE: {len(sorted_de_at)} total keys")
    
    # Sync sv and nl - add any missing keys from en
    for lang in ['sv', 'nl']:
        locale_path = f'{LOCALES_DIR}/{lang}.json'
        with open(locale_path) as f:
            current = json.load(f)
        missing = {k: en[k] for k in en if k not in current}
        if missing:
            print(f"\n[{lang}] Adding {len(missing)} missing keys...")
            translations = await translate_batch(lang, missing)
            current.update(translations)
            sorted_locale = {k: current[k] for k in sorted(current.keys())}
            with open(locale_path, 'w') as f:
                json.dump(sorted_locale, f, ensure_ascii=False, indent=2)
            print(f"[{lang}] DONE: {len(sorted_locale)} total keys")
        else:
            print(f"[{lang}] Already complete")
    
    # Final verification
    print(f"\n{'='*60}")
    print("FINAL VERIFICATION")
    print("=" * 60)
    
    all_files = ['ar', 'de', 'de-AT', 'el', 'en', 'fr', 'nl', 'ru', 'sv', 'tr']
    for lang in all_files:
        path = f'{LOCALES_DIR}/{lang}.json'
        if os.path.exists(path):
            with open(path) as f:
                data = json.load(f)
            missing = set(en.keys()) - set(data.keys())
            status = "✅ COMPLETE" if not missing else f"❌ MISSING {len(missing)} keys"
            print(f"  {lang}: {len(data)} keys - {status}")
        else:
            print(f"  {lang}: ❌ FILE NOT FOUND")

if __name__ == '__main__':
    asyncio.run(main())

"""Batch translate missing academy content using deep-translator (free Google Translate)."""
import json, time, sys
from deep_translator import GoogleTranslator

TRANSLATIONS_PATH = '/app/backend/data/academy_translations.json'
TARGET_LANGS = ['tr', 'ru', 'sv', 'nl', 'el', 'fr']
LANG_CODES = {'tr': 'tr', 'ru': 'ru', 'sv': 'sv', 'nl': 'nl', 'el': 'el', 'fr': 'fr'}

def translate_text(text, target_lang):
    """Translate text from English to target language."""
    try:
        if len(text) > 4500:
            text = text[:4500]
        result = GoogleTranslator(source='en', target=target_lang).translate(text)
        return result
    except Exception as e:
        print(f"  Error translating: {e}")
        return None

def main():
    with open(TRANSLATIONS_PATH, 'r', encoding='utf-8') as f:
        all_trans = json.load(f)
    
    total_added = 0
    
    for lang in TARGET_LANGS:
        missing_texts = []
        for en_text, langs in all_trans.items():
            if lang not in langs:
                missing_texts.append(en_text)
        
        if not missing_texts:
            print(f"✅ {lang}: Complete!")
            continue
        
        print(f"\n🔄 {lang}: {len(missing_texts)} texts to translate")
        count = 0
        
        for i, en_text in enumerate(missing_texts):
            translated = translate_text(en_text, LANG_CODES[lang])
            if translated:
                all_trans[en_text][lang] = translated
                count += 1
                total_added += 1
            
            if (i + 1) % 50 == 0:
                print(f"  Progress: {i+1}/{len(missing_texts)} ({count} translated)")
                # Save periodically
                with open(TRANSLATIONS_PATH, 'w', encoding='utf-8') as f:
                    json.dump(all_trans, f, ensure_ascii=False)
                time.sleep(1)  # Rate limit
            
            if (i + 1) % 10 == 0:
                time.sleep(0.3)
        
        print(f"✅ {lang}: {count} new translations")
        # Save after each language
        with open(TRANSLATIONS_PATH, 'w', encoding='utf-8') as f:
            json.dump(all_trans, f, ensure_ascii=False)
    
    print(f"\n💾 Total added: {total_added}")
    with open(TRANSLATIONS_PATH, 'w', encoding='utf-8') as f:
        json.dump(all_trans, f, ensure_ascii=False)

if __name__ == "__main__":
    main()

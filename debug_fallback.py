#!/usr/bin/env python3

# Test the fallback logic
TAFSIR_RESOURCE_IDS = {
    "ar": 16,    # Tafsir Al-Muyassar (التفسير الميسر)
    "en": 169,   # Ibn Kathir (Abridged)
    "ru": 170,   # Al-Sa'di (Russian)
    "de": 169,   # Fallback → English Ibn Kathir
    "fr": 169,   # Fallback → English Ibn Kathir
    "tr": 169,   # Fallback → English Ibn Kathir
    "sv": 169,   # Fallback → English Ibn Kathir
    "nl": 169,   # Fallback → English Ibn Kathir
    "el": 169,   # Fallback → English Ibn Kathir
}

def test_fallback_logic(language):
    base_lang = language.split('-')[0]  # Handle de-AT -> de
    tafsir_id = TAFSIR_RESOURCE_IDS.get(base_lang, TAFSIR_RESOURCE_IDS["en"])
    is_fallback = base_lang not in TAFSIR_RESOURCE_IDS or (base_lang != "ar" and base_lang != "en" and base_lang != "ru")
    
    print(f"Language: {language}")
    print(f"Base lang: {base_lang}")
    print(f"Tafsir ID: {tafsir_id}")
    print(f"base_lang not in TAFSIR_RESOURCE_IDS: {base_lang not in TAFSIR_RESOURCE_IDS}")
    print(f"base_lang != 'ar' and base_lang != 'en' and base_lang != 'ru': {base_lang != 'ar' and base_lang != 'en' and base_lang != 'ru'}")
    print(f"Is fallback: {is_fallback}")
    print("---")

# Test different languages
test_fallback_logic("ar")
test_fallback_logic("en") 
test_fallback_logic("ru")
test_fallback_logic("de")
test_fallback_logic("fr")
test_fallback_logic("zh")  # Not in the dict
"""
Extract all unique translatable English strings from Noor Academy data files.
Outputs a JSON file with all unique strings to translate.
"""
import sys
sys.path.insert(0, '/app/backend')

import json

# Import all lesson data
from data.noor_academy_v2 import (
    ACADEMY_TRACKS, NOORANIYA_LEVELS, NOORANIYA_ALL_LESSONS,
    AQEEDAH_LEVELS, FIQH_LEVELS, SEERAH_LEVELS,
    TEACHING_METHODS, ADAB_ALL_LESSONS
)
from data.noor_academy_extended import NOORANIYA_ALL_LESSONS_EXTENDED
from data.noor_academy_aqeedah_fiqh_seerah import (
    AQEEDAH_LESSONS_L2, AQEEDAH_LESSONS_L3
)
from data.noor_academy_aqeedah_complete import (
    AQEEDAH_L1_COMPLETE, AQEEDAH_L4_COMPLETE, AQEEDAH_L5_COMPLETE
)
from data.noor_academy_fiqh_content import FIQH_COMPLETE_LESSONS as FIQH_ALL_LESSONS
from data.noor_academy_seerah_content import SEERAH_COMPLETE_LESSONS as SEERAH_ALL_LESSONS

AQEEDAH_ALL_LESSONS = AQEEDAH_L1_COMPLETE + AQEEDAH_LESSONS_L2 + AQEEDAH_LESSONS_L3 + AQEEDAH_L4_COMPLETE + AQEEDAH_L5_COMPLETE

TARGET_LANGS = ['de', 'fr', 'tr', 'ru', 'sv', 'nl', 'el']

def extract_translatable_strings(obj, strings_set, path=""):
    """Recursively extract all {ar: ..., en: ...} dicts that need translation."""
    if isinstance(obj, dict):
        # Check if this is a translatable dict
        if 'en' in obj and isinstance(obj.get('en'), str):
            en_text = obj['en'].strip()
            ar_text = obj.get('ar', '').strip()
            if en_text:
                # Check if it needs translation (missing any target language)
                needs_translation = any(lang not in obj for lang in TARGET_LANGS)
                if needs_translation:
                    strings_set.add((en_text, ar_text))
        
        # Recurse into values
        for key, val in obj.items():
            if key not in ('ar', 'en', 'de', 'fr', 'tr', 'ru', 'sv', 'nl', 'el'):
                extract_translatable_strings(val, strings_set, f"{path}.{key}")
    
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            extract_translatable_strings(item, strings_set, f"{path}[{i}]")

all_strings = set()

# Extract from all tracks
print("Extracting from Nooraniya base lessons...")
for lesson in NOORANIYA_ALL_LESSONS:
    extract_translatable_strings(lesson, all_strings)

print("Extracting from Nooraniya extended lessons...")
for lesson in NOORANIYA_ALL_LESSONS_EXTENDED:
    extract_translatable_strings(lesson, all_strings)

print("Extracting from Aqeedah lessons...")
for lesson in AQEEDAH_ALL_LESSONS:
    extract_translatable_strings(lesson, all_strings)

print("Extracting from Fiqh lessons...")
for lesson in FIQH_ALL_LESSONS:
    extract_translatable_strings(lesson, all_strings)

print("Extracting from Seerah lessons...")
for lesson in SEERAH_ALL_LESSONS:
    extract_translatable_strings(lesson, all_strings)

print("Extracting from Adab lessons...")
for lesson in ADAB_ALL_LESSONS:
    extract_translatable_strings(lesson, all_strings)

# Extract from levels and tracks
for level_list in [NOORANIYA_LEVELS, AQEEDAH_LEVELS, FIQH_LEVELS, SEERAH_LEVELS]:
    for level in level_list:
        extract_translatable_strings(level, all_strings)

for track in ACADEMY_TRACKS:
    extract_translatable_strings(track, all_strings)

for method_key, method_val in TEACHING_METHODS.items():
    extract_translatable_strings(method_val, all_strings)

# Convert to list and sort
strings_list = [{"en": en, "ar": ar} for en, ar in all_strings]
strings_list.sort(key=lambda x: x['en'])

print(f"\nTotal unique translatable strings: {len(strings_list)}")

# Save to JSON
output = {
    "total": len(strings_list),
    "target_languages": TARGET_LANGS,
    "strings": strings_list
}

with open('/app/backend/data/strings_to_translate.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Saved to /app/backend/data/strings_to_translate.json")

# Print some stats
print(f"\nSample strings (first 10):")
for s in strings_list[:10]:
    print(f"  EN: {s['en'][:80]}")
    print(f"  AR: {s['ar'][:80]}")
    print()

"""
Router: arabic_academy
"""
from fastapi import APIRouter, HTTPException, Query, Depends, BackgroundTasks
from deps import db, get_user, logger, security, verify_jwt, create_jwt, hash_password, check_password, ADMIN_EMAILS, STRIPE_API_KEY, EMERGENT_LLM_KEY, haversine, query_overpass, clean_time, OVERPASS_ENDPOINTS, VAPID_PUBLIC_KEY, VAPID_PRIVATE_KEY, VAPID_EMAIL, FIREBASE_PROJECT_ID, RESEND_API_KEY, GEMINI_API_KEY
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, date, timedelta
import uuid
import random
import math
import re
import httpx
import os
import json as json_module

router = APIRouter(tags=["Arabic Academy"])

ARABIC_LETTERS = [
    {"id": 1, "letter": "ا", "name_ar": "ألف", "name_en": "Alif", "transliteration": "a", "form_isolated": "ا", "form_initial": "ا", "form_medial": "ـا", "form_final": "ـا", "example_word": "أسد", "example_meaning": "Lion", "audio_hint": "ah"},
    {"id": 2, "letter": "ب", "name_ar": "باء", "name_en": "Ba", "transliteration": "b", "form_isolated": "ب", "form_initial": "بـ", "form_medial": "ـبـ", "form_final": "ـب", "example_word": "بيت", "example_meaning": "House", "audio_hint": "bah"},
    {"id": 3, "letter": "ت", "name_ar": "تاء", "name_en": "Ta", "transliteration": "t", "form_isolated": "ت", "form_initial": "تـ", "form_medial": "ـتـ", "form_final": "ـت", "example_word": "تفاح", "example_meaning": "Apple", "audio_hint": "tah"},
    {"id": 4, "letter": "ث", "name_ar": "ثاء", "name_en": "Tha", "transliteration": "th", "form_isolated": "ث", "form_initial": "ثـ", "form_medial": "ـثـ", "form_final": "ـث", "example_word": "ثعلب", "example_meaning": "Fox", "audio_hint": "thah"},
    {"id": 5, "letter": "ج", "name_ar": "جيم", "name_en": "Jim", "transliteration": "j", "form_isolated": "ج", "form_initial": "جـ", "form_medial": "ـجـ", "form_final": "ـج", "example_word": "جمل", "example_meaning": "Camel", "audio_hint": "jeem"},
    {"id": 6, "letter": "ح", "name_ar": "حاء", "name_en": "Ha", "transliteration": "ḥ", "form_isolated": "ح", "form_initial": "حـ", "form_medial": "ـحـ", "form_final": "ـح", "example_word": "حصان", "example_meaning": "Horse", "audio_hint": "hah"},
    {"id": 7, "letter": "خ", "name_ar": "خاء", "name_en": "Kha", "transliteration": "kh", "form_isolated": "خ", "form_initial": "خـ", "form_medial": "ـخـ", "form_final": "ـخ", "example_word": "خروف", "example_meaning": "Sheep", "audio_hint": "khah"},
    {"id": 8, "letter": "د", "name_ar": "دال", "name_en": "Dal", "transliteration": "d", "form_isolated": "د", "form_initial": "د", "form_medial": "ـد", "form_final": "ـد", "example_word": "ديك", "example_meaning": "Rooster", "audio_hint": "daal"},
    {"id": 9, "letter": "ذ", "name_ar": "ذال", "name_en": "Dhal", "transliteration": "dh", "form_isolated": "ذ", "form_initial": "ذ", "form_medial": "ـذ", "form_final": "ـذ", "example_word": "ذئب", "example_meaning": "Wolf", "audio_hint": "dhaal"},
    {"id": 10, "letter": "ر", "name_ar": "راء", "name_en": "Ra", "transliteration": "r", "form_isolated": "ر", "form_initial": "ر", "form_medial": "ـر", "form_final": "ـر", "example_word": "رمان", "example_meaning": "Pomegranate", "audio_hint": "raa"},
    {"id": 11, "letter": "ز", "name_ar": "زاي", "name_en": "Zay", "transliteration": "z", "form_isolated": "ز", "form_initial": "ز", "form_medial": "ـز", "form_final": "ـز", "example_word": "زهرة", "example_meaning": "Flower", "audio_hint": "zaay"},
    {"id": 12, "letter": "س", "name_ar": "سين", "name_en": "Sin", "transliteration": "s", "form_isolated": "س", "form_initial": "سـ", "form_medial": "ـسـ", "form_final": "ـس", "example_word": "سمك", "example_meaning": "Fish", "audio_hint": "seen"},
    {"id": 13, "letter": "ش", "name_ar": "شين", "name_en": "Shin", "transliteration": "sh", "form_isolated": "ش", "form_initial": "شـ", "form_medial": "ـشـ", "form_final": "ـش", "example_word": "شمس", "example_meaning": "Sun", "audio_hint": "sheen"},
    {"id": 14, "letter": "ص", "name_ar": "صاد", "name_en": "Sad", "transliteration": "ṣ", "form_isolated": "ص", "form_initial": "صـ", "form_medial": "ـصـ", "form_final": "ـص", "example_word": "صقر", "example_meaning": "Falcon", "audio_hint": "saad"},
    {"id": 15, "letter": "ض", "name_ar": "ضاد", "name_en": "Dad", "transliteration": "ḍ", "form_isolated": "ض", "form_initial": "ضـ", "form_medial": "ـضـ", "form_final": "ـض", "example_word": "ضفدع", "example_meaning": "Frog", "audio_hint": "daad"},
    {"id": 16, "letter": "ط", "name_ar": "طاء", "name_en": "Tah", "transliteration": "ṭ", "form_isolated": "ط", "form_initial": "طـ", "form_medial": "ـطـ", "form_final": "ـط", "example_word": "طائر", "example_meaning": "Bird", "audio_hint": "taa"},
    {"id": 17, "letter": "ظ", "name_ar": "ظاء", "name_en": "Zah", "transliteration": "ẓ", "form_isolated": "ظ", "form_initial": "ظـ", "form_medial": "ـظـ", "form_final": "ـظ", "example_word": "ظبي", "example_meaning": "Gazelle", "audio_hint": "zhaa"},
    {"id": 18, "letter": "ع", "name_ar": "عين", "name_en": "Ain", "transliteration": "'", "form_isolated": "ع", "form_initial": "عـ", "form_medial": "ـعـ", "form_final": "ـع", "example_word": "عنب", "example_meaning": "Grapes", "audio_hint": "ain"},
    {"id": 19, "letter": "غ", "name_ar": "غين", "name_en": "Ghain", "transliteration": "gh", "form_isolated": "غ", "form_initial": "غـ", "form_medial": "ـغـ", "form_final": "ـغ", "example_word": "غزال", "example_meaning": "Deer", "audio_hint": "ghain"},
    {"id": 20, "letter": "ف", "name_ar": "فاء", "name_en": "Fa", "transliteration": "f", "form_isolated": "ف", "form_initial": "فـ", "form_medial": "ـفـ", "form_final": "ـف", "example_word": "فيل", "example_meaning": "Elephant", "audio_hint": "faa"},
    {"id": 21, "letter": "ق", "name_ar": "قاف", "name_en": "Qaf", "transliteration": "q", "form_isolated": "ق", "form_initial": "قـ", "form_medial": "ـقـ", "form_final": "ـق", "example_word": "قمر", "example_meaning": "Moon", "audio_hint": "qaaf"},
    {"id": 22, "letter": "ك", "name_ar": "كاف", "name_en": "Kaf", "transliteration": "k", "form_isolated": "ك", "form_initial": "كـ", "form_medial": "ـكـ", "form_final": "ـك", "example_word": "كتاب", "example_meaning": "Book", "audio_hint": "kaaf"},
    {"id": 23, "letter": "ل", "name_ar": "لام", "name_en": "Lam", "transliteration": "l", "form_isolated": "ل", "form_initial": "لـ", "form_medial": "ـلـ", "form_final": "ـل", "example_word": "ليمون", "example_meaning": "Lemon", "audio_hint": "laam"},
    {"id": 24, "letter": "م", "name_ar": "ميم", "name_en": "Mim", "transliteration": "m", "form_isolated": "م", "form_initial": "مـ", "form_medial": "ـمـ", "form_final": "ـم", "example_word": "مسجد", "example_meaning": "Mosque", "audio_hint": "meem"},
    {"id": 25, "letter": "ن", "name_ar": "نون", "name_en": "Nun", "transliteration": "n", "form_isolated": "ن", "form_initial": "نـ", "form_medial": "ـنـ", "form_final": "ـن", "example_word": "نجمة", "example_meaning": "Star", "audio_hint": "noon"},
    {"id": 26, "letter": "ه", "name_ar": "هاء", "name_en": "Ha2", "transliteration": "h", "form_isolated": "ه", "form_initial": "هـ", "form_medial": "ـهـ", "form_final": "ـه", "example_word": "هلال", "example_meaning": "Crescent", "audio_hint": "haa"},
    {"id": 27, "letter": "و", "name_ar": "واو", "name_en": "Waw", "transliteration": "w", "form_isolated": "و", "form_initial": "و", "form_medial": "ـو", "form_final": "ـو", "example_word": "وردة", "example_meaning": "Rose", "audio_hint": "waaw"},
    {"id": 28, "letter": "ي", "name_ar": "ياء", "name_en": "Ya", "transliteration": "y", "form_isolated": "ي", "form_initial": "يـ", "form_medial": "ـيـ", "form_final": "ـي", "example_word": "يد", "example_meaning": "Hand", "audio_hint": "yaa"},
]

QURAN_VOCAB = [
    {"id": 1, "word": "بِسْمِ", "transliteration": "Bismi", "meaning": "In the name of", "surah": "Al-Fatiha", "ayah": 1},
    {"id": 2, "word": "اللَّهِ", "transliteration": "Allah", "meaning": "God", "surah": "Al-Fatiha", "ayah": 1},
    {"id": 3, "word": "الرَّحْمَنِ", "transliteration": "Ar-Rahman", "meaning": "The Most Gracious", "surah": "Al-Fatiha", "ayah": 1},
    {"id": 4, "word": "الرَّحِيمِ", "transliteration": "Ar-Raheem", "meaning": "The Most Merciful", "surah": "Al-Fatiha", "ayah": 1},
    {"id": 5, "word": "الْحَمْدُ", "transliteration": "Al-Hamdu", "meaning": "All praise", "surah": "Al-Fatiha", "ayah": 2},
    {"id": 6, "word": "رَبِّ", "transliteration": "Rabbi", "meaning": "Lord of", "surah": "Al-Fatiha", "ayah": 2},
    {"id": 7, "word": "الْعَالَمِينَ", "transliteration": "Al-Alameen", "meaning": "The Worlds", "surah": "Al-Fatiha", "ayah": 2},
    {"id": 8, "word": "مَالِكِ", "transliteration": "Maliki", "meaning": "Master of", "surah": "Al-Fatiha", "ayah": 4},
    {"id": 9, "word": "يَوْمِ", "transliteration": "Yawmi", "meaning": "Day of", "surah": "Al-Fatiha", "ayah": 4},
    {"id": 10, "word": "الدِّينِ", "transliteration": "Ad-Deen", "meaning": "Judgment", "surah": "Al-Fatiha", "ayah": 4},
    {"id": 11, "word": "إِيَّاكَ", "transliteration": "Iyyaka", "meaning": "You alone", "surah": "Al-Fatiha", "ayah": 5},
    {"id": 12, "word": "نَعْبُدُ", "transliteration": "Na'budu", "meaning": "We worship", "surah": "Al-Fatiha", "ayah": 5},
    {"id": 13, "word": "نَسْتَعِينُ", "transliteration": "Nasta'een", "meaning": "We seek help", "surah": "Al-Fatiha", "ayah": 5},
    {"id": 14, "word": "اهْدِنَا", "transliteration": "Ihdina", "meaning": "Guide us", "surah": "Al-Fatiha", "ayah": 6},
    {"id": 15, "word": "الصِّرَاطَ", "transliteration": "As-Sirat", "meaning": "The path", "surah": "Al-Fatiha", "ayah": 6},
    {"id": 16, "word": "الْمُسْتَقِيمَ", "transliteration": "Al-Mustaqeem", "meaning": "The straight", "surah": "Al-Fatiha", "ayah": 6},
    {"id": 17, "word": "جَنَّة", "transliteration": "Jannah", "meaning": "Paradise", "surah": "Various", "ayah": 0},
    {"id": 18, "word": "صَلَاة", "transliteration": "Salah", "meaning": "Prayer", "surah": "Various", "ayah": 0},
    {"id": 19, "word": "زَكَاة", "transliteration": "Zakah", "meaning": "Charity", "surah": "Various", "ayah": 0},
    {"id": 20, "word": "صِيَام", "transliteration": "Siyam", "meaning": "Fasting", "surah": "Various", "ayah": 0},
]

LIVE_STREAMS = [
    {
        "id": "makkah",
        "name_ar": "بث مباشر من مكة المكرمة",
        "name_en": "Makkah Live",
        "name_de": "Mekka Live",
        "name_ru": "Мекка в прямом эфире",
        "name_fr": "La Mecque en direct",
        "name_tr": "Mekke Canlı",
        "name_sv": "Mecka Live",
        "name_nl": "Mekka Live",
        "name_el": "Μέκκα Ζωντανά",
        "youtube_channel": "SaudiQuranTv",
        "embed_id": "gAzq1ch5RnY",
        "thumbnail": "https://i.ytimg.com/vi/gAzq1ch5RnY/maxresdefault_live.jpg",
        "city": "Makkah",
        "country": "Saudi Arabia",
        "category": "haramain",
        "is_247": True
    },
    {
        "id": "madinah",
        "name_ar": "بث مباشر من المدينة المنورة",
        "name_en": "Madinah Live",
        "name_de": "Medina Live",
        "name_ru": "Медина в прямом эфире",
        "name_fr": "Médine en direct",
        "name_tr": "Medine Canlı",
        "name_sv": "Medina Live",
        "name_nl": "Medina Live",
        "name_el": "Μεδίνα Ζωντανά",
        "youtube_channel": "SaudiSunnahTv",
        "embed_id": "VO359jOBfCk",
        "thumbnail": "https://i.ytimg.com/vi/VO359jOBfCk/maxresdefault_live.jpg",
        "city": "Madinah",
        "country": "Saudi Arabia",
        "category": "haramain",
        "is_247": True
    },
    {
        "id": "alaqsa",
        "name_ar": "بث مباشر من المسجد الأقصى",
        "name_en": "Al-Aqsa Mosque Live",
        "name_de": "Al-Aqsa-Moschee Live",
        "name_ru": "Мечеть Аль-Акса в прямом эфире",
        "name_fr": "Mosquée Al-Aqsa en direct",
        "name_tr": "Mescid-i Aksa Canlı",
        "name_sv": "Al-Aqsa-moskén Live",
        "name_nl": "Al-Aqsa Moskee Live",
        "name_el": "Τζαμί Αλ-Άκσα Ζωντανά",
        "youtube_channel": "AlAqsaTV",
        "embed_id": "jBYrnVptmCo",
        "thumbnail": "https://i.ytimg.com/vi/jBYrnVptmCo/maxresdefault_live.jpg",
        "city": "Jerusalem",
        "country": "Palestine",
        "category": "holy",
        "is_247": True
    },
    {
        "id": "umayyad",
        "name_ar": "بث مباشر من الجامع الأموي",
        "name_en": "Umayyad Mosque Live",
        "name_de": "Umayyaden-Moschee Live",
        "name_ru": "Мечеть Омейядов в прямом эфире",
        "name_fr": "Mosquée des Omeyyades en direct",
        "name_tr": "Emevi Camii Canlı",
        "name_sv": "Umayyadmoskén Live",
        "name_nl": "Umayyad Moskee Live",
        "name_el": "Τζαμί Ομεϋάδ Ζωντανά",
        "youtube_channel": "UmayyadMosque",
        "embed_id": "wQMmHBBl3cA",
        "thumbnail": "https://i.ytimg.com/vi/wQMmHBBl3cA/maxresdefault_live.jpg",
        "city": "Damascus",
        "country": "Syria",
        "category": "historic",
        "is_247": False
    },
    {
        "id": "cologne",
        "name_ar": "بث مباشر من مسجد كولونيا الكبير",
        "name_en": "Cologne Central Mosque Live",
        "name_de": "DITIB-Zentralmoschee Köln Live",
        "name_ru": "Центральная мечеть Кёльна в прямом эфире",
        "name_fr": "Mosquée centrale de Cologne en direct",
        "name_tr": "Köln Merkez Camii Canlı",
        "name_sv": "Kölns Centralmoské Live",
        "name_nl": "Centrale Moskee Keulen Live",
        "name_el": "Κεντρικό Τζαμί Κολωνίας Ζωντανά",
        "youtube_channel": "DitibCologne",
        "embed_id": "o4N9vYUFHzA",
        "thumbnail": "https://i.ytimg.com/vi/o4N9vYUFHzA/maxresdefault_live.jpg",
        "city": "Cologne",
        "country": "Germany",
        "category": "europe",
        "is_247": False
    }
]

@router.get("/arabic-academy/letters")
async def get_arabic_letters():
    """Get all 28 Arabic letters with forms and examples"""
    return {"success": True, "letters": ARABIC_LETTERS, "total": len(ARABIC_LETTERS)}

@router.get("/arabic-academy/vocab")
async def get_quran_vocab():
    """Get Quranic vocabulary words"""
    return {"success": True, "words": QURAN_VOCAB, "total": len(QURAN_VOCAB)}

@router.get("/arabic-academy/daily-word")
async def get_daily_word():
    """Get a daily Quranic vocabulary word"""
    today = date.today()
    idx = today.toordinal() % len(QURAN_VOCAB)
    word = QURAN_VOCAB[idx]
    return {"success": True, "word": word, "day_index": idx}

ARABIC_NUMBERS = [
    {"id": i, "number": i, "arabic": n[0], "word_ar": n[1], "word_en": n[2], "transliteration": n[3]}
    for i, n in enumerate([
        ("٠", "صفر", "Zero", "Sifr"), ("١", "واحد", "One", "Wahid"), ("٢", "اثنان", "Two", "Ithnan"),
        ("٣", "ثلاثة", "Three", "Thalatha"), ("٤", "أربعة", "Four", "Arba'a"), ("٥", "خمسة", "Five", "Khamsa"),
        ("٦", "ستة", "Six", "Sitta"), ("٧", "سبعة", "Seven", "Sab'a"), ("٨", "ثمانية", "Eight", "Thamaniya"),
        ("٩", "تسعة", "Nine", "Tis'a"), ("١٠", "عشرة", "Ten", "Ashara"),
        ("٢٠", "عشرون", "Twenty", "Ishrun"), ("٣٠", "ثلاثون", "Thirty", "Thalathun"),
        ("٤٠", "أربعون", "Forty", "Arba'un"), ("٥٠", "خمسون", "Fifty", "Khamsun"),
        ("١٠٠", "مائة", "Hundred", "Mi'a"), ("١٠٠٠", "ألف", "Thousand", "Alf"),
    ], start=0)
]

VOCAB_CATEGORIES = {
    "animals": [
        {"id": "a1", "word": "قِطَّة", "transliteration": "Qitta", "meaning_en": "Cat", "meaning_de": "Katze", "meaning_fr": "Chat", "meaning_tr": "Kedi", "meaning_ru": "Кошка", "emoji": "🐱"},
        {"id": "a2", "word": "كَلْب", "transliteration": "Kalb", "meaning_en": "Dog", "meaning_de": "Hund", "meaning_fr": "Chien", "meaning_tr": "Köpek", "meaning_ru": "Собака", "emoji": "🐕"},
        {"id": "a3", "word": "أَسَد", "transliteration": "Asad", "meaning_en": "Lion", "meaning_de": "Löwe", "meaning_fr": "Lion", "meaning_tr": "Aslan", "meaning_ru": "Лев", "emoji": "🦁"},
        {"id": "a4", "word": "فِيل", "transliteration": "Fiil", "meaning_en": "Elephant", "meaning_de": "Elefant", "meaning_fr": "Éléphant", "meaning_tr": "Fil", "meaning_ru": "Слон", "emoji": "🐘"},
        {"id": "a5", "word": "طَائِر", "transliteration": "Taa'ir", "meaning_en": "Bird", "meaning_de": "Vogel", "meaning_fr": "Oiseau", "meaning_tr": "Kuş", "meaning_ru": "Птица", "emoji": "🐦"},
        {"id": "a6", "word": "سَمَكَة", "transliteration": "Samaka", "meaning_en": "Fish", "meaning_de": "Fisch", "meaning_fr": "Poisson", "meaning_tr": "Balık", "meaning_ru": "Рыба", "emoji": "🐟"},
        {"id": "a7", "word": "حِصَان", "transliteration": "Hisan", "meaning_en": "Horse", "meaning_de": "Pferd", "meaning_fr": "Cheval", "meaning_tr": "At", "meaning_ru": "Лошадь", "emoji": "🐴"},
        {"id": "a8", "word": "أَرْنَب", "transliteration": "Arnab", "meaning_en": "Rabbit", "meaning_de": "Kaninchen", "meaning_fr": "Lapin", "meaning_tr": "Tavşan", "meaning_ru": "Кролик", "emoji": "🐰"},
        {"id": "a9", "word": "بَقَرَة", "transliteration": "Baqara", "meaning_en": "Cow", "meaning_de": "Kuh", "meaning_fr": "Vache", "meaning_tr": "İnek", "meaning_ru": "Корова", "emoji": "🐄"},
        {"id": "a10", "word": "خَرُوف", "transliteration": "Kharuf", "meaning_en": "Sheep", "meaning_de": "Schaf", "meaning_fr": "Mouton", "meaning_tr": "Koyun", "meaning_ru": "Овца", "emoji": "🐑"},
    ],
    "food": [
        {"id": "f1", "word": "تُفَّاحَة", "transliteration": "Tuffaha", "meaning_en": "Apple", "meaning_de": "Apfel", "meaning_fr": "Pomme", "meaning_tr": "Elma", "meaning_ru": "Яблоко", "emoji": "🍎"},
        {"id": "f2", "word": "مَوْز", "transliteration": "Mawz", "meaning_en": "Banana", "meaning_de": "Banane", "meaning_fr": "Banane", "meaning_tr": "Muz", "meaning_ru": "Банан", "emoji": "🍌"},
        {"id": "f3", "word": "خُبْز", "transliteration": "Khubz", "meaning_en": "Bread", "meaning_de": "Brot", "meaning_fr": "Pain", "meaning_tr": "Ekmek", "meaning_ru": "Хлеб", "emoji": "🍞"},
        {"id": "f4", "word": "مَاء", "transliteration": "Maa'", "meaning_en": "Water", "meaning_de": "Wasser", "meaning_fr": "Eau", "meaning_tr": "Su", "meaning_ru": "Вода", "emoji": "💧"},
        {"id": "f5", "word": "حَلِيب", "transliteration": "Haleeb", "meaning_en": "Milk", "meaning_de": "Milch", "meaning_fr": "Lait", "meaning_tr": "Süt", "meaning_ru": "Молоко", "emoji": "🥛"},
        {"id": "f6", "word": "أُرْز", "transliteration": "Urz", "meaning_en": "Rice", "meaning_de": "Reis", "meaning_fr": "Riz", "meaning_tr": "Pirinç", "meaning_ru": "Рис", "emoji": "🍚"},
        {"id": "f7", "word": "بَيْض", "transliteration": "Bayd", "meaning_en": "Eggs", "meaning_de": "Eier", "meaning_fr": "Œufs", "meaning_tr": "Yumurta", "meaning_ru": "Яйца", "emoji": "🥚"},
        {"id": "f8", "word": "عَسَل", "transliteration": "Asal", "meaning_en": "Honey", "meaning_de": "Honig", "meaning_fr": "Miel", "meaning_tr": "Bal", "meaning_ru": "Мёд", "emoji": "🍯"},
        {"id": "f9", "word": "بُرْتُقَالَة", "transliteration": "Burtuqala", "meaning_en": "Orange", "meaning_de": "Orange", "meaning_fr": "Orange", "meaning_tr": "Portakal", "meaning_ru": "Апельсин", "emoji": "🍊"},
        {"id": "f10", "word": "عِنَب", "transliteration": "Inab", "meaning_en": "Grapes", "meaning_de": "Trauben", "meaning_fr": "Raisins", "meaning_tr": "Üzüm", "meaning_ru": "Виноград", "emoji": "🍇"},
    ],
    "body": [
        {"id": "b1", "word": "رَأْس", "transliteration": "Ra's", "meaning_en": "Head", "meaning_de": "Kopf", "meaning_fr": "Tête", "meaning_tr": "Baş", "meaning_ru": "Голова", "emoji": "🗣️"},
        {"id": "b2", "word": "يَد", "transliteration": "Yad", "meaning_en": "Hand", "meaning_de": "Hand", "meaning_fr": "Main", "meaning_tr": "El", "meaning_ru": "Рука", "emoji": "✋"},
        {"id": "b3", "word": "عَيْن", "transliteration": "Ayn", "meaning_en": "Eye", "meaning_de": "Auge", "meaning_fr": "Œil", "meaning_tr": "Göz", "meaning_ru": "Глаз", "emoji": "👁️"},
        {"id": "b4", "word": "أُذُن", "transliteration": "Udhun", "meaning_en": "Ear", "meaning_de": "Ohr", "meaning_fr": "Oreille", "meaning_tr": "Kulak", "meaning_ru": "Ухо", "emoji": "👂"},
        {"id": "b5", "word": "قَلْب", "transliteration": "Qalb", "meaning_en": "Heart", "meaning_de": "Herz", "meaning_fr": "Cœur", "meaning_tr": "Kalp", "meaning_ru": "Сердце", "emoji": "❤️"},
        {"id": "b6", "word": "قَدَم", "transliteration": "Qadam", "meaning_en": "Foot", "meaning_de": "Fuß", "meaning_fr": "Pied", "meaning_tr": "Ayak", "meaning_ru": "Нога", "emoji": "🦶"},
        {"id": "b7", "word": "أَنْف", "transliteration": "Anf", "meaning_en": "Nose", "meaning_de": "Nase", "meaning_fr": "Nez", "meaning_tr": "Burun", "meaning_ru": "Нос", "emoji": "👃"},
        {"id": "b8", "word": "فَم", "transliteration": "Fam", "meaning_en": "Mouth", "meaning_de": "Mund", "meaning_fr": "Bouche", "meaning_tr": "Ağız", "meaning_ru": "Рот", "emoji": "👄"},
    ],
    "family": [
        {"id": "fm1", "word": "أَب", "transliteration": "Ab", "meaning_en": "Father", "meaning_de": "Vater", "meaning_fr": "Père", "meaning_tr": "Baba", "meaning_ru": "Отец", "emoji": "👨"},
        {"id": "fm2", "word": "أُمّ", "transliteration": "Umm", "meaning_en": "Mother", "meaning_de": "Mutter", "meaning_fr": "Mère", "meaning_tr": "Anne", "meaning_ru": "Мать", "emoji": "👩"},
        {"id": "fm3", "word": "أَخ", "transliteration": "Akh", "meaning_en": "Brother", "meaning_de": "Bruder", "meaning_fr": "Frère", "meaning_tr": "Kardeş", "meaning_ru": "Брат", "emoji": "👦"},
        {"id": "fm4", "word": "أُخْت", "transliteration": "Ukht", "meaning_en": "Sister", "meaning_de": "Schwester", "meaning_fr": "Sœur", "meaning_tr": "Kız kardeş", "meaning_ru": "Сестра", "emoji": "👧"},
        {"id": "fm5", "word": "جَدّ", "transliteration": "Jadd", "meaning_en": "Grandfather", "meaning_de": "Großvater", "meaning_fr": "Grand-père", "meaning_tr": "Dede", "meaning_ru": "Дед", "emoji": "👴"},
        {"id": "fm6", "word": "جَدَّة", "transliteration": "Jadda", "meaning_en": "Grandmother", "meaning_de": "Großmutter", "meaning_fr": "Grand-mère", "meaning_tr": "Nine", "meaning_ru": "Бабушка", "emoji": "👵"},
        {"id": "fm7", "word": "طِفْل", "transliteration": "Tifl", "meaning_en": "Child", "meaning_de": "Kind", "meaning_fr": "Enfant", "meaning_tr": "Çocuk", "meaning_ru": "Ребёнок", "emoji": "👶"},
        {"id": "fm8", "word": "عَائِلَة", "transliteration": "Aa'ila", "meaning_en": "Family", "meaning_de": "Familie", "meaning_fr": "Famille", "meaning_tr": "Aile", "meaning_ru": "Семья", "emoji": "👨‍👩‍👧‍👦"},
    ],
    "nature": [
        {"id": "n1", "word": "شَمْس", "transliteration": "Shams", "meaning_en": "Sun", "meaning_de": "Sonne", "meaning_fr": "Soleil", "meaning_tr": "Güneş", "meaning_ru": "Солнце", "emoji": "☀️"},
        {"id": "n2", "word": "قَمَر", "transliteration": "Qamar", "meaning_en": "Moon", "meaning_de": "Mond", "meaning_fr": "Lune", "meaning_tr": "Ay", "meaning_ru": "Луна", "emoji": "🌙"},
        {"id": "n3", "word": "نَجْمَة", "transliteration": "Najma", "meaning_en": "Star", "meaning_de": "Stern", "meaning_fr": "Étoile", "meaning_tr": "Yıldız", "meaning_ru": "Звезда", "emoji": "⭐"},
        {"id": "n4", "word": "سَمَاء", "transliteration": "Samaa'", "meaning_en": "Sky", "meaning_de": "Himmel", "meaning_fr": "Ciel", "meaning_tr": "Gökyüzü", "meaning_ru": "Небо", "emoji": "🌤️"},
        {"id": "n5", "word": "مَطَر", "transliteration": "Matar", "meaning_en": "Rain", "meaning_de": "Regen", "meaning_fr": "Pluie", "meaning_tr": "Yağmur", "meaning_ru": "Дождь", "emoji": "🌧️"},
        {"id": "n6", "word": "بَحْر", "transliteration": "Bahr", "meaning_en": "Sea", "meaning_de": "Meer", "meaning_fr": "Mer", "meaning_tr": "Deniz", "meaning_ru": "Море", "emoji": "🌊"},
        {"id": "n7", "word": "جَبَل", "transliteration": "Jabal", "meaning_en": "Mountain", "meaning_de": "Berg", "meaning_fr": "Montagne", "meaning_tr": "Dağ", "meaning_ru": "Гора", "emoji": "⛰️"},
        {"id": "n8", "word": "شَجَرَة", "transliteration": "Shajara", "meaning_en": "Tree", "meaning_de": "Baum", "meaning_fr": "Arbre", "meaning_tr": "Ağaç", "meaning_ru": "Дерево", "emoji": "🌳"},
        {"id": "n9", "word": "زَهْرَة", "transliteration": "Zahra", "meaning_en": "Flower", "meaning_de": "Blume", "meaning_fr": "Fleur", "meaning_tr": "Çiçek", "meaning_ru": "Цветок", "emoji": "🌸"},
        {"id": "n10", "word": "أَرْض", "transliteration": "Ard", "meaning_en": "Earth", "meaning_de": "Erde", "meaning_fr": "Terre", "meaning_tr": "Toprak", "meaning_ru": "Земля", "emoji": "🌍"},
    ],
    "colors": [
        {"id": "c1", "word": "أَحْمَر", "transliteration": "Ahmar", "meaning_en": "Red", "meaning_de": "Rot", "meaning_fr": "Rouge", "meaning_tr": "Kırmızı", "meaning_ru": "Красный", "emoji": "🔴"},
        {"id": "c2", "word": "أَزْرَق", "transliteration": "Azraq", "meaning_en": "Blue", "meaning_de": "Blau", "meaning_fr": "Bleu", "meaning_tr": "Mavi", "meaning_ru": "Синий", "emoji": "🔵"},
        {"id": "c3", "word": "أَخْضَر", "transliteration": "Akhdar", "meaning_en": "Green", "meaning_de": "Grün", "meaning_fr": "Vert", "meaning_tr": "Yeşil", "meaning_ru": "Зелёный", "emoji": "🟢"},
        {"id": "c4", "word": "أَصْفَر", "transliteration": "Asfar", "meaning_en": "Yellow", "meaning_de": "Gelb", "meaning_fr": "Jaune", "meaning_tr": "Sarı", "meaning_ru": "Жёлтый", "emoji": "🟡"},
        {"id": "c5", "word": "أَبْيَض", "transliteration": "Abyad", "meaning_en": "White", "meaning_de": "Weiß", "meaning_fr": "Blanc", "meaning_tr": "Beyaz", "meaning_ru": "Белый", "emoji": "⚪"},
        {"id": "c6", "word": "أَسْوَد", "transliteration": "Aswad", "meaning_en": "Black", "meaning_de": "Schwarz", "meaning_fr": "Noir", "meaning_tr": "Siyah", "meaning_ru": "Чёрный", "emoji": "⚫"},
        {"id": "c7", "word": "بُرْتُقَالِي", "transliteration": "Burtuqali", "meaning_en": "Orange", "meaning_de": "Orange", "meaning_fr": "Orange", "meaning_tr": "Turuncu", "meaning_ru": "Оранжевый", "emoji": "🟠"},
        {"id": "c8", "word": "بَنَفْسَجِي", "transliteration": "Banafsaji", "meaning_en": "Purple", "meaning_de": "Lila", "meaning_fr": "Violet", "meaning_tr": "Mor", "meaning_ru": "Фиолетовый", "emoji": "🟣"},
    ],
    "home": [
        {"id": "h1", "word": "بَيْت", "transliteration": "Bayt", "meaning_en": "House", "meaning_de": "Haus", "meaning_fr": "Maison", "meaning_tr": "Ev", "meaning_ru": "Дом", "emoji": "🏠"},
        {"id": "h2", "word": "بَاب", "transliteration": "Bab", "meaning_en": "Door", "meaning_de": "Tür", "meaning_fr": "Porte", "meaning_tr": "Kapı", "meaning_ru": "Дверь", "emoji": "🚪"},
        {"id": "h3", "word": "كُرْسِي", "transliteration": "Kursi", "meaning_en": "Chair", "meaning_de": "Stuhl", "meaning_fr": "Chaise", "meaning_tr": "Sandalye", "meaning_ru": "Стул", "emoji": "🪑"},
        {"id": "h4", "word": "طَاوِلَة", "transliteration": "Tawila", "meaning_en": "Table", "meaning_de": "Tisch", "meaning_fr": "Table", "meaning_tr": "Masa", "meaning_ru": "Стол", "emoji": "🪵"},
        {"id": "h5", "word": "سَرِير", "transliteration": "Sareer", "meaning_en": "Bed", "meaning_de": "Bett", "meaning_fr": "Lit", "meaning_tr": "Yatak", "meaning_ru": "Кровать", "emoji": "🛏️"},
        {"id": "h6", "word": "نَافِذَة", "transliteration": "Nafidha", "meaning_en": "Window", "meaning_de": "Fenster", "meaning_fr": "Fenêtre", "meaning_tr": "Pencere", "meaning_ru": "Окно", "emoji": "🪟"},
        {"id": "h7", "word": "مَسْجِد", "transliteration": "Masjid", "meaning_en": "Mosque", "meaning_de": "Moschee", "meaning_fr": "Mosquée", "meaning_tr": "Cami", "meaning_ru": "Мечеть", "emoji": "🕌"},
        {"id": "h8", "word": "كِتَاب", "transliteration": "Kitab", "meaning_en": "Book", "meaning_de": "Buch", "meaning_fr": "Livre", "meaning_tr": "Kitap", "meaning_ru": "Книга", "emoji": "📖"},
    ],
    "verbs": [
        {"id": "v1", "word": "كَتَبَ", "transliteration": "Kataba", "meaning_en": "Wrote", "meaning_de": "Schrieb", "meaning_fr": "A écrit", "meaning_tr": "Yazdı", "meaning_ru": "Написал", "emoji": "✍️"},
        {"id": "v2", "word": "قَرَأَ", "transliteration": "Qara'a", "meaning_en": "Read", "meaning_de": "Las", "meaning_fr": "A lu", "meaning_tr": "Okudu", "meaning_ru": "Читал", "emoji": "📖"},
        {"id": "v3", "word": "أَكَلَ", "transliteration": "Akala", "meaning_en": "Ate", "meaning_de": "Aß", "meaning_fr": "A mangé", "meaning_tr": "Yedi", "meaning_ru": "Ел", "emoji": "🍽️"},
        {"id": "v4", "word": "شَرِبَ", "transliteration": "Shariba", "meaning_en": "Drank", "meaning_de": "Trank", "meaning_fr": "A bu", "meaning_tr": "İçti", "meaning_ru": "Пил", "emoji": "🥤"},
        {"id": "v5", "word": "ذَهَبَ", "transliteration": "Dhahaba", "meaning_en": "Went", "meaning_de": "Ging", "meaning_fr": "Est allé", "meaning_tr": "Gitti", "meaning_ru": "Пошёл", "emoji": "🚶"},
        {"id": "v6", "word": "جَلَسَ", "transliteration": "Jalasa", "meaning_en": "Sat", "meaning_de": "Saß", "meaning_fr": "S'est assis", "meaning_tr": "Oturdu", "meaning_ru": "Сел", "emoji": "🪑"},
        {"id": "v7", "word": "نَامَ", "transliteration": "Nama", "meaning_en": "Slept", "meaning_de": "Schlief", "meaning_fr": "A dormi", "meaning_tr": "Uyudu", "meaning_ru": "Спал", "emoji": "😴"},
        {"id": "v8", "word": "لَعِبَ", "transliteration": "La'iba", "meaning_en": "Played", "meaning_de": "Spielte", "meaning_fr": "A joué", "meaning_tr": "Oynadı", "meaning_ru": "Играл", "emoji": "⚽"},
    ],
    "greetings": [
        {"id": "g1", "word": "السَّلَامُ عَلَيْكُم", "transliteration": "As-Salamu Alaykum", "meaning_en": "Peace be upon you", "meaning_de": "Friede sei mit euch", "meaning_fr": "Paix sur vous", "meaning_tr": "Selamun aleyküm", "meaning_ru": "Мир вам", "emoji": "🤝"},
        {"id": "g2", "word": "صَبَاحُ الْخَيْر", "transliteration": "Sabah Al-Khayr", "meaning_en": "Good morning", "meaning_de": "Guten Morgen", "meaning_fr": "Bonjour", "meaning_tr": "Günaydın", "meaning_ru": "Доброе утро", "emoji": "🌅"},
        {"id": "g3", "word": "مَسَاءُ الْخَيْر", "transliteration": "Masa' Al-Khayr", "meaning_en": "Good evening", "meaning_de": "Guten Abend", "meaning_fr": "Bonsoir", "meaning_tr": "İyi akşamlar", "meaning_ru": "Добрый вечер", "emoji": "🌆"},
        {"id": "g4", "word": "شُكْرًا", "transliteration": "Shukran", "meaning_en": "Thank you", "meaning_de": "Danke", "meaning_fr": "Merci", "meaning_tr": "Teşekkürler", "meaning_ru": "Спасибо", "emoji": "🙏"},
        {"id": "g5", "word": "مَعَ السَّلَامَة", "transliteration": "Ma'a As-Salama", "meaning_en": "Goodbye", "meaning_de": "Auf Wiedersehen", "meaning_fr": "Au revoir", "meaning_tr": "Güle güle", "meaning_ru": "До свидания", "emoji": "👋"},
        {"id": "g6", "word": "مِنْ فَضْلِك", "transliteration": "Min Fadlik", "meaning_en": "Please", "meaning_de": "Bitte", "meaning_fr": "S'il vous plaît", "meaning_tr": "Lütfen", "meaning_ru": "Пожалуйста", "emoji": "😊"},
    ],
}

SENTENCE_TEMPLATES = [
    {"id": "s1", "words_ar": ["أَنَا", "أُحِبُّ", "التُّفَّاح"], "words_en": ["I", "love", "apples"], "sentence_ar": "أَنَا أُحِبُّ التُّفَّاح", "sentence_en": "I love apples", "difficulty": 1},
    {"id": "s2", "words_ar": ["هَذَا", "كِتَاب", "جَمِيل"], "words_en": ["This is", "a book", "beautiful"], "sentence_ar": "هَذَا كِتَاب جَمِيل", "sentence_en": "This is a beautiful book", "difficulty": 1},
    {"id": "s3", "words_ar": ["الْوَلَد", "يَلْعَبُ", "فِي الْحَدِيقَة"], "words_en": ["The boy", "plays", "in the park"], "sentence_ar": "الْوَلَد يَلْعَبُ فِي الْحَدِيقَة", "sentence_en": "The boy plays in the park", "difficulty": 2},
    {"id": "s4", "words_ar": ["ذَهَبْتُ", "إِلَى", "الْمَسْجِد"], "words_en": ["I went", "to", "the mosque"], "sentence_ar": "ذَهَبْتُ إِلَى الْمَسْجِد", "sentence_en": "I went to the mosque", "difficulty": 1},
    {"id": "s5", "words_ar": ["الشَّمْسُ", "سَاطِعَة", "الْيَوْم"], "words_en": ["The sun", "is bright", "today"], "sentence_ar": "الشَّمْسُ سَاطِعَة الْيَوْم", "sentence_en": "The sun is bright today", "difficulty": 2},
    {"id": "s6", "words_ar": ["أُمِّي", "تَطْبَخُ", "طَعَامًا", "لَذِيذًا"], "words_en": ["My mother", "cooks", "food", "delicious"], "sentence_ar": "أُمِّي تَطْبَخُ طَعَامًا لَذِيذًا", "sentence_en": "My mother cooks delicious food", "difficulty": 2},
    {"id": "s7", "words_ar": ["الْقَمَر", "جَمِيل", "فِي اللَّيْل"], "words_en": ["The moon", "is beautiful", "at night"], "sentence_ar": "الْقَمَر جَمِيل فِي اللَّيْل", "sentence_en": "The moon is beautiful at night", "difficulty": 2},
    {"id": "s8", "words_ar": ["بِسْمِ اللَّه", "الرَّحْمَن", "الرَّحِيم"], "words_en": ["In the name of Allah", "the Most Gracious", "the Most Merciful"], "sentence_ar": "بِسْمِ اللَّه الرَّحْمَن الرَّحِيم", "sentence_en": "In the name of Allah, the Most Gracious, the Most Merciful", "difficulty": 1},
    {"id": "s9", "words_ar": ["قَرَأَ", "الطِّفْل", "الْقُرْآن"], "words_en": ["Read", "the child", "the Quran"], "sentence_ar": "قَرَأَ الطِّفْل الْقُرْآن", "sentence_en": "The child read the Quran", "difficulty": 2},
    {"id": "s10", "words_ar": ["الْمَاء", "ضَرُورِيّ", "لِلْحَيَاة"], "words_en": ["Water", "is essential", "for life"], "sentence_ar": "الْمَاء ضَرُورِيّ لِلْحَيَاة", "sentence_en": "Water is essential for life", "difficulty": 3},
]

# Build 90-day curriculum
def build_90_day_curriculum():
    days = []
    day_num = 0
    # Level 1: Alphabet (Days 1-30) - 28 letters + 2 review
    for i, letter in enumerate(ARABIC_LETTERS):
        day_num += 1
        days.append({"day": day_num, "level": 1, "type": "letter", "content_id": letter["id"],
                      "title_en": f"Letter: {letter['name_en']}", "title_ar": f"حرف: {letter['name_ar']}", "xp": 10})
    days.append({"day": 29, "level": 1, "type": "review", "content_id": 0, "title_en": "Alphabet Review 1", "title_ar": "مراجعة الأبجدية ١", "xp": 20})
    days.append({"day": 30, "level": 1, "type": "review", "content_id": 0, "title_en": "Alphabet Review 2", "title_ar": "مراجعة الأبجدية ٢", "xp": 20})
    

@router.get("/arabic-academy/letters")
async def get_arabic_letters():
    """Get all 28 Arabic letters with forms and examples"""
    return {"success": True, "letters": ARABIC_LETTERS, "total": len(ARABIC_LETTERS)}

@router.get("/arabic-academy/vocab")
async def get_quran_vocab():
    """Get Quranic vocabulary words"""
    return {"success": True, "words": QURAN_VOCAB, "total": len(QURAN_VOCAB)}

@router.get("/arabic-academy/daily-word")
async def get_daily_word():
    """Get a daily Quranic word based on day of year"""
    day_of_year = datetime.utcnow().timetuple().tm_yday
    word = QURAN_VOCAB[day_of_year % len(QURAN_VOCAB)]
    return {"success": True, "word": word}

@router.get("/arabic-academy/progress/{user_id}")
async def get_academy_progress(user_id: str):
    """Get user's Arabic Academy progress"""
    progress = await db.arabic_progress.find_one({"user_id": user_id})
    if not progress:
        progress = {
            "user_id": user_id,
            "completed_letters": [],
            "completed_vocab": [],
            "stars": 0,
            "streak": 0,
            "total_xp": 0,
            "level": 1,
            "golden_bricks": 0,
            "last_activity": None
        }
    progress.pop("_id", None)
    return {"success": True, "progress": progress}

@router.post("/arabic-academy/progress")
async def save_academy_progress(data: dict):
    """Save user's Arabic Academy progress"""
    user_id = data.get("user_id", "guest")
    update_data = {
        "user_id": user_id,
        "completed_letters": data.get("completed_letters", []),
        "completed_vocab": data.get("completed_vocab", []),
        "stars": data.get("stars", 0),
        "streak": data.get("streak", 0),
        "total_xp": data.get("total_xp", 0),
        "level": data.get("level", 1),
        "golden_bricks": data.get("golden_bricks", 0),
        "last_activity": datetime.utcnow().isoformat()
    }
    await db.arabic_progress.update_one(
        {"user_id": user_id},
        {"$set": update_data},
        upsert=True
    )
    return {"success": True, "message": "Progress saved"}

@router.get("/arabic-academy/quiz/{letter_id}")
async def get_letter_quiz(letter_id: int):
    """Get quiz for a specific letter"""
    letter = next((lt for lt in ARABIC_LETTERS if lt["id"] == letter_id), None)
    if not letter:
        raise HTTPException(status_code=404, detail="Letter not found")
    
    other_letters = [lt for lt in ARABIC_LETTERS if lt["id"] != letter_id]
    wrong_answers = random.sample(other_letters, min(3, len(other_letters)))
    
    options = [{"letter": letter["letter"], "name_ar": letter["name_ar"], "name_en": letter["name_en"], "correct": True}]
    for w in wrong_answers:
        options.append({"letter": w["letter"], "name_ar": w["name_ar"], "name_en": w["name_en"], "correct": False})
    random.shuffle(options)
    
    return {
        "success": True,
        "quiz": {
            "question_letter": letter,
            "options": options,
            "type": "identify"
        }
    }

# ==================== CURRICULUM 90-DAY ====================

ARABIC_NUMBERS = [
    {"id": i, "number": i, "arabic": n[0], "word_ar": n[1], "word_en": n[2], "transliteration": n[3]}
    for i, n in enumerate([
        ("٠", "صفر", "Zero", "Sifr"), ("١", "واحد", "One", "Wahid"), ("٢", "اثنان", "Two", "Ithnan"),
        ("٣", "ثلاثة", "Three", "Thalatha"), ("٤", "أربعة", "Four", "Arba'a"), ("٥", "خمسة", "Five", "Khamsa"),
        ("٦", "ستة", "Six", "Sitta"), ("٧", "سبعة", "Seven", "Sab'a"), ("٨", "ثمانية", "Eight", "Thamaniya"),
        ("٩", "تسعة", "Nine", "Tis'a"), ("١٠", "عشرة", "Ten", "Ashara"),
        ("٢٠", "عشرون", "Twenty", "Ishrun"), ("٣٠", "ثلاثون", "Thirty", "Thalathun"),
        ("٤٠", "أربعون", "Forty", "Arba'un"), ("٥٠", "خمسون", "Fifty", "Khamsun"),
        ("١٠٠", "مائة", "Hundred", "Mi'a"), ("١٠٠٠", "ألف", "Thousand", "Alf"),
    ], start=0)
]

VOCAB_CATEGORIES = {
    "animals": [
        {"id": "a1", "word": "قِطَّة", "transliteration": "Qitta", "meaning_en": "Cat", "meaning_de": "Katze", "meaning_fr": "Chat", "meaning_tr": "Kedi", "meaning_ru": "Кошка", "emoji": "🐱"},
        {"id": "a2", "word": "كَلْب", "transliteration": "Kalb", "meaning_en": "Dog", "meaning_de": "Hund", "meaning_fr": "Chien", "meaning_tr": "Köpek", "meaning_ru": "Собака", "emoji": "🐕"},
        {"id": "a3", "word": "أَسَد", "transliteration": "Asad", "meaning_en": "Lion", "meaning_de": "Löwe", "meaning_fr": "Lion", "meaning_tr": "Aslan", "meaning_ru": "Лев", "emoji": "🦁"},
        {"id": "a4", "word": "فِيل", "transliteration": "Fiil", "meaning_en": "Elephant", "meaning_de": "Elefant", "meaning_fr": "Éléphant", "meaning_tr": "Fil", "meaning_ru": "Слон", "emoji": "🐘"},
        {"id": "a5", "word": "طَائِر", "transliteration": "Taa'ir", "meaning_en": "Bird", "meaning_de": "Vogel", "meaning_fr": "Oiseau", "meaning_tr": "Kuş", "meaning_ru": "Птица", "emoji": "🐦"},
        {"id": "a6", "word": "سَمَكَة", "transliteration": "Samaka", "meaning_en": "Fish", "meaning_de": "Fisch", "meaning_fr": "Poisson", "meaning_tr": "Balık", "meaning_ru": "Рыба", "emoji": "🐟"},
        {"id": "a7", "word": "حِصَان", "transliteration": "Hisan", "meaning_en": "Horse", "meaning_de": "Pferd", "meaning_fr": "Cheval", "meaning_tr": "At", "meaning_ru": "Лошадь", "emoji": "🐴"},
        {"id": "a8", "word": "أَرْنَب", "transliteration": "Arnab", "meaning_en": "Rabbit", "meaning_de": "Kaninchen", "meaning_fr": "Lapin", "meaning_tr": "Tavşan", "meaning_ru": "Кролик", "emoji": "🐰"},
        {"id": "a9", "word": "بَقَرَة", "transliteration": "Baqara", "meaning_en": "Cow", "meaning_de": "Kuh", "meaning_fr": "Vache", "meaning_tr": "İnek", "meaning_ru": "Корова", "emoji": "🐄"},
        {"id": "a10", "word": "خَرُوف", "transliteration": "Kharuf", "meaning_en": "Sheep", "meaning_de": "Schaf", "meaning_fr": "Mouton", "meaning_tr": "Koyun", "meaning_ru": "Овца", "emoji": "🐑"},
    ],
    "food": [
        {"id": "f1", "word": "تُفَّاحَة", "transliteration": "Tuffaha", "meaning_en": "Apple", "meaning_de": "Apfel", "meaning_fr": "Pomme", "meaning_tr": "Elma", "meaning_ru": "Яблоко", "emoji": "🍎"},
        {"id": "f2", "word": "مَوْز", "transliteration": "Mawz", "meaning_en": "Banana", "meaning_de": "Banane", "meaning_fr": "Banane", "meaning_tr": "Muz", "meaning_ru": "Банан", "emoji": "🍌"},
        {"id": "f3", "word": "خُبْز", "transliteration": "Khubz", "meaning_en": "Bread", "meaning_de": "Brot", "meaning_fr": "Pain", "meaning_tr": "Ekmek", "meaning_ru": "Хлеб", "emoji": "🍞"},
        {"id": "f4", "word": "مَاء", "transliteration": "Maa'", "meaning_en": "Water", "meaning_de": "Wasser", "meaning_fr": "Eau", "meaning_tr": "Su", "meaning_ru": "Вода", "emoji": "💧"},
        {"id": "f5", "word": "حَلِيب", "transliteration": "Haleeb", "meaning_en": "Milk", "meaning_de": "Milch", "meaning_fr": "Lait", "meaning_tr": "Süt", "meaning_ru": "Молоко", "emoji": "🥛"},
        {"id": "f6", "word": "أُرْز", "transliteration": "Urz", "meaning_en": "Rice", "meaning_de": "Reis", "meaning_fr": "Riz", "meaning_tr": "Pirinç", "meaning_ru": "Рис", "emoji": "🍚"},
        {"id": "f7", "word": "بَيْض", "transliteration": "Bayd", "meaning_en": "Eggs", "meaning_de": "Eier", "meaning_fr": "Œufs", "meaning_tr": "Yumurta", "meaning_ru": "Яйца", "emoji": "🥚"},
        {"id": "f8", "word": "عَسَل", "transliteration": "Asal", "meaning_en": "Honey", "meaning_de": "Honig", "meaning_fr": "Miel", "meaning_tr": "Bal", "meaning_ru": "Мёд", "emoji": "🍯"},
        {"id": "f9", "word": "بُرْتُقَالَة", "transliteration": "Burtuqala", "meaning_en": "Orange", "meaning_de": "Orange", "meaning_fr": "Orange", "meaning_tr": "Portakal", "meaning_ru": "Апельсин", "emoji": "🍊"},
        {"id": "f10", "word": "عِنَب", "transliteration": "Inab", "meaning_en": "Grapes", "meaning_de": "Trauben", "meaning_fr": "Raisins", "meaning_tr": "Üzüm", "meaning_ru": "Виноград", "emoji": "🍇"},
    ],
    "body": [
        {"id": "b1", "word": "رَأْس", "transliteration": "Ra's", "meaning_en": "Head", "meaning_de": "Kopf", "meaning_fr": "Tête", "meaning_tr": "Baş", "meaning_ru": "Голова", "emoji": "🗣️"},
        {"id": "b2", "word": "يَد", "transliteration": "Yad", "meaning_en": "Hand", "meaning_de": "Hand", "meaning_fr": "Main", "meaning_tr": "El", "meaning_ru": "Рука", "emoji": "✋"},
        {"id": "b3", "word": "عَيْن", "transliteration": "Ayn", "meaning_en": "Eye", "meaning_de": "Auge", "meaning_fr": "Œil", "meaning_tr": "Göz", "meaning_ru": "Глаз", "emoji": "👁️"},
        {"id": "b4", "word": "أُذُن", "transliteration": "Udhun", "meaning_en": "Ear", "meaning_de": "Ohr", "meaning_fr": "Oreille", "meaning_tr": "Kulak", "meaning_ru": "Ухо", "emoji": "👂"},
        {"id": "b5", "word": "قَلْب", "transliteration": "Qalb", "meaning_en": "Heart", "meaning_de": "Herz", "meaning_fr": "Cœur", "meaning_tr": "Kalp", "meaning_ru": "Сердце", "emoji": "❤️"},
        {"id": "b6", "word": "قَدَم", "transliteration": "Qadam", "meaning_en": "Foot", "meaning_de": "Fuß", "meaning_fr": "Pied", "meaning_tr": "Ayak", "meaning_ru": "Нога", "emoji": "🦶"},
        {"id": "b7", "word": "أَنْف", "transliteration": "Anf", "meaning_en": "Nose", "meaning_de": "Nase", "meaning_fr": "Nez", "meaning_tr": "Burun", "meaning_ru": "Нос", "emoji": "👃"},
        {"id": "b8", "word": "فَم", "transliteration": "Fam", "meaning_en": "Mouth", "meaning_de": "Mund", "meaning_fr": "Bouche", "meaning_tr": "Ağız", "meaning_ru": "Рот", "emoji": "👄"},
    ],
    "family": [
        {"id": "fm1", "word": "أَب", "transliteration": "Ab", "meaning_en": "Father", "meaning_de": "Vater", "meaning_fr": "Père", "meaning_tr": "Baba", "meaning_ru": "Отец", "emoji": "👨"},
        {"id": "fm2", "word": "أُمّ", "transliteration": "Umm", "meaning_en": "Mother", "meaning_de": "Mutter", "meaning_fr": "Mère", "meaning_tr": "Anne", "meaning_ru": "Мать", "emoji": "👩"},
        {"id": "fm3", "word": "أَخ", "transliteration": "Akh", "meaning_en": "Brother", "meaning_de": "Bruder", "meaning_fr": "Frère", "meaning_tr": "Kardeş", "meaning_ru": "Брат", "emoji": "👦"},
        {"id": "fm4", "word": "أُخْت", "transliteration": "Ukht", "meaning_en": "Sister", "meaning_de": "Schwester", "meaning_fr": "Sœur", "meaning_tr": "Kız kardeş", "meaning_ru": "Сестра", "emoji": "👧"},
        {"id": "fm5", "word": "جَدّ", "transliteration": "Jadd", "meaning_en": "Grandfather", "meaning_de": "Großvater", "meaning_fr": "Grand-père", "meaning_tr": "Dede", "meaning_ru": "Дед", "emoji": "👴"},
        {"id": "fm6", "word": "جَدَّة", "transliteration": "Jadda", "meaning_en": "Grandmother", "meaning_de": "Großmutter", "meaning_fr": "Grand-mère", "meaning_tr": "Nine", "meaning_ru": "Бабушка", "emoji": "👵"},
        {"id": "fm7", "word": "طِفْل", "transliteration": "Tifl", "meaning_en": "Child", "meaning_de": "Kind", "meaning_fr": "Enfant", "meaning_tr": "Çocuk", "meaning_ru": "Ребёнок", "emoji": "👶"},
        {"id": "fm8", "word": "عَائِلَة", "transliteration": "Aa'ila", "meaning_en": "Family", "meaning_de": "Familie", "meaning_fr": "Famille", "meaning_tr": "Aile", "meaning_ru": "Семья", "emoji": "👨‍👩‍👧‍👦"},
    ],
    "nature": [
        {"id": "n1", "word": "شَمْس", "transliteration": "Shams", "meaning_en": "Sun", "meaning_de": "Sonne", "meaning_fr": "Soleil", "meaning_tr": "Güneş", "meaning_ru": "Солнце", "emoji": "☀️"},
        {"id": "n2", "word": "قَمَر", "transliteration": "Qamar", "meaning_en": "Moon", "meaning_de": "Mond", "meaning_fr": "Lune", "meaning_tr": "Ay", "meaning_ru": "Луна", "emoji": "🌙"},
        {"id": "n3", "word": "نَجْمَة", "transliteration": "Najma", "meaning_en": "Star", "meaning_de": "Stern", "meaning_fr": "Étoile", "meaning_tr": "Yıldız", "meaning_ru": "Звезда", "emoji": "⭐"},
        {"id": "n4", "word": "سَمَاء", "transliteration": "Samaa'", "meaning_en": "Sky", "meaning_de": "Himmel", "meaning_fr": "Ciel", "meaning_tr": "Gökyüzü", "meaning_ru": "Небо", "emoji": "🌤️"},
        {"id": "n5", "word": "مَطَر", "transliteration": "Matar", "meaning_en": "Rain", "meaning_de": "Regen", "meaning_fr": "Pluie", "meaning_tr": "Yağmur", "meaning_ru": "Дождь", "emoji": "🌧️"},
        {"id": "n6", "word": "بَحْر", "transliteration": "Bahr", "meaning_en": "Sea", "meaning_de": "Meer", "meaning_fr": "Mer", "meaning_tr": "Deniz", "meaning_ru": "Море", "emoji": "🌊"},
        {"id": "n7", "word": "جَبَل", "transliteration": "Jabal", "meaning_en": "Mountain", "meaning_de": "Berg", "meaning_fr": "Montagne", "meaning_tr": "Dağ", "meaning_ru": "Гора", "emoji": "⛰️"},
        {"id": "n8", "word": "شَجَرَة", "transliteration": "Shajara", "meaning_en": "Tree", "meaning_de": "Baum", "meaning_fr": "Arbre", "meaning_tr": "Ağaç", "meaning_ru": "Дерево", "emoji": "🌳"},
        {"id": "n9", "word": "زَهْرَة", "transliteration": "Zahra", "meaning_en": "Flower", "meaning_de": "Blume", "meaning_fr": "Fleur", "meaning_tr": "Çiçek", "meaning_ru": "Цветок", "emoji": "🌸"},
        {"id": "n10", "word": "أَرْض", "transliteration": "Ard", "meaning_en": "Earth", "meaning_de": "Erde", "meaning_fr": "Terre", "meaning_tr": "Toprak", "meaning_ru": "Земля", "emoji": "🌍"},
    ],
    "colors": [
        {"id": "c1", "word": "أَحْمَر", "transliteration": "Ahmar", "meaning_en": "Red", "meaning_de": "Rot", "meaning_fr": "Rouge", "meaning_tr": "Kırmızı", "meaning_ru": "Красный", "emoji": "🔴"},
        {"id": "c2", "word": "أَزْرَق", "transliteration": "Azraq", "meaning_en": "Blue", "meaning_de": "Blau", "meaning_fr": "Bleu", "meaning_tr": "Mavi", "meaning_ru": "Синий", "emoji": "🔵"},
        {"id": "c3", "word": "أَخْضَر", "transliteration": "Akhdar", "meaning_en": "Green", "meaning_de": "Grün", "meaning_fr": "Vert", "meaning_tr": "Yeşil", "meaning_ru": "Зелёный", "emoji": "🟢"},
        {"id": "c4", "word": "أَصْفَر", "transliteration": "Asfar", "meaning_en": "Yellow", "meaning_de": "Gelb", "meaning_fr": "Jaune", "meaning_tr": "Sarı", "meaning_ru": "Жёлтый", "emoji": "🟡"},
        {"id": "c5", "word": "أَبْيَض", "transliteration": "Abyad", "meaning_en": "White", "meaning_de": "Weiß", "meaning_fr": "Blanc", "meaning_tr": "Beyaz", "meaning_ru": "Белый", "emoji": "⚪"},
        {"id": "c6", "word": "أَسْوَد", "transliteration": "Aswad", "meaning_en": "Black", "meaning_de": "Schwarz", "meaning_fr": "Noir", "meaning_tr": "Siyah", "meaning_ru": "Чёрный", "emoji": "⚫"},
        {"id": "c7", "word": "بُرْتُقَالِي", "transliteration": "Burtuqali", "meaning_en": "Orange", "meaning_de": "Orange", "meaning_fr": "Orange", "meaning_tr": "Turuncu", "meaning_ru": "Оранжевый", "emoji": "🟠"},
        {"id": "c8", "word": "بَنَفْسَجِي", "transliteration": "Banafsaji", "meaning_en": "Purple", "meaning_de": "Lila", "meaning_fr": "Violet", "meaning_tr": "Mor", "meaning_ru": "Фиолетовый", "emoji": "🟣"},
    ],
    "home": [
        {"id": "h1", "word": "بَيْت", "transliteration": "Bayt", "meaning_en": "House", "meaning_de": "Haus", "meaning_fr": "Maison", "meaning_tr": "Ev", "meaning_ru": "Дом", "emoji": "🏠"},
        {"id": "h2", "word": "بَاب", "transliteration": "Bab", "meaning_en": "Door", "meaning_de": "Tür", "meaning_fr": "Porte", "meaning_tr": "Kapı", "meaning_ru": "Дверь", "emoji": "🚪"},
        {"id": "h3", "word": "كُرْسِي", "transliteration": "Kursi", "meaning_en": "Chair", "meaning_de": "Stuhl", "meaning_fr": "Chaise", "meaning_tr": "Sandalye", "meaning_ru": "Стул", "emoji": "🪑"},
        {"id": "h4", "word": "طَاوِلَة", "transliteration": "Tawila", "meaning_en": "Table", "meaning_de": "Tisch", "meaning_fr": "Table", "meaning_tr": "Masa", "meaning_ru": "Стол", "emoji": "🪵"},
        {"id": "h5", "word": "سَرِير", "transliteration": "Sareer", "meaning_en": "Bed", "meaning_de": "Bett", "meaning_fr": "Lit", "meaning_tr": "Yatak", "meaning_ru": "Кровать", "emoji": "🛏️"},
        {"id": "h6", "word": "نَافِذَة", "transliteration": "Nafidha", "meaning_en": "Window", "meaning_de": "Fenster", "meaning_fr": "Fenêtre", "meaning_tr": "Pencere", "meaning_ru": "Окно", "emoji": "🪟"},
        {"id": "h7", "word": "مَسْجِد", "transliteration": "Masjid", "meaning_en": "Mosque", "meaning_de": "Moschee", "meaning_fr": "Mosquée", "meaning_tr": "Cami", "meaning_ru": "Мечеть", "emoji": "🕌"},
        {"id": "h8", "word": "كِتَاب", "transliteration": "Kitab", "meaning_en": "Book", "meaning_de": "Buch", "meaning_fr": "Livre", "meaning_tr": "Kitap", "meaning_ru": "Книга", "emoji": "📖"},
    ],
    "verbs": [
        {"id": "v1", "word": "كَتَبَ", "transliteration": "Kataba", "meaning_en": "Wrote", "meaning_de": "Schrieb", "meaning_fr": "A écrit", "meaning_tr": "Yazdı", "meaning_ru": "Написал", "emoji": "✍️"},
        {"id": "v2", "word": "قَرَأَ", "transliteration": "Qara'a", "meaning_en": "Read", "meaning_de": "Las", "meaning_fr": "A lu", "meaning_tr": "Okudu", "meaning_ru": "Читал", "emoji": "📖"},
        {"id": "v3", "word": "أَكَلَ", "transliteration": "Akala", "meaning_en": "Ate", "meaning_de": "Aß", "meaning_fr": "A mangé", "meaning_tr": "Yedi", "meaning_ru": "Ел", "emoji": "🍽️"},
        {"id": "v4", "word": "شَرِبَ", "transliteration": "Shariba", "meaning_en": "Drank", "meaning_de": "Trank", "meaning_fr": "A bu", "meaning_tr": "İçti", "meaning_ru": "Пил", "emoji": "🥤"},
        {"id": "v5", "word": "ذَهَبَ", "transliteration": "Dhahaba", "meaning_en": "Went", "meaning_de": "Ging", "meaning_fr": "Est allé", "meaning_tr": "Gitti", "meaning_ru": "Пошёл", "emoji": "🚶"},
        {"id": "v6", "word": "جَلَسَ", "transliteration": "Jalasa", "meaning_en": "Sat", "meaning_de": "Saß", "meaning_fr": "S'est assis", "meaning_tr": "Oturdu", "meaning_ru": "Сел", "emoji": "🪑"},
        {"id": "v7", "word": "نَامَ", "transliteration": "Nama", "meaning_en": "Slept", "meaning_de": "Schlief", "meaning_fr": "A dormi", "meaning_tr": "Uyudu", "meaning_ru": "Спал", "emoji": "😴"},
        {"id": "v8", "word": "لَعِبَ", "transliteration": "La'iba", "meaning_en": "Played", "meaning_de": "Spielte", "meaning_fr": "A joué", "meaning_tr": "Oynadı", "meaning_ru": "Играл", "emoji": "⚽"},
    ],
    "greetings": [
        {"id": "g1", "word": "السَّلَامُ عَلَيْكُم", "transliteration": "As-Salamu Alaykum", "meaning_en": "Peace be upon you", "meaning_de": "Friede sei mit euch", "meaning_fr": "Paix sur vous", "meaning_tr": "Selamun aleyküm", "meaning_ru": "Мир вам", "emoji": "🤝"},
        {"id": "g2", "word": "صَبَاحُ الْخَيْر", "transliteration": "Sabah Al-Khayr", "meaning_en": "Good morning", "meaning_de": "Guten Morgen", "meaning_fr": "Bonjour", "meaning_tr": "Günaydın", "meaning_ru": "Доброе утро", "emoji": "🌅"},
        {"id": "g3", "word": "مَسَاءُ الْخَيْر", "transliteration": "Masa' Al-Khayr", "meaning_en": "Good evening", "meaning_de": "Guten Abend", "meaning_fr": "Bonsoir", "meaning_tr": "İyi akşamlar", "meaning_ru": "Добрый вечер", "emoji": "🌆"},
        {"id": "g4", "word": "شُكْرًا", "transliteration": "Shukran", "meaning_en": "Thank you", "meaning_de": "Danke", "meaning_fr": "Merci", "meaning_tr": "Teşekkürler", "meaning_ru": "Спасибо", "emoji": "🙏"},
        {"id": "g5", "word": "مَعَ السَّلَامَة", "transliteration": "Ma'a As-Salama", "meaning_en": "Goodbye", "meaning_de": "Auf Wiedersehen", "meaning_fr": "Au revoir", "meaning_tr": "Güle güle", "meaning_ru": "До свидания", "emoji": "👋"},
        {"id": "g6", "word": "مِنْ فَضْلِك", "transliteration": "Min Fadlik", "meaning_en": "Please", "meaning_de": "Bitte", "meaning_fr": "S'il vous plaît", "meaning_tr": "Lütfen", "meaning_ru": "Пожалуйста", "emoji": "😊"},
    ],
}

SENTENCE_TEMPLATES = [
    {"id": "s1", "words_ar": ["أَنَا", "أُحِبُّ", "التُّفَّاح"], "words_en": ["I", "love", "apples"], "sentence_ar": "أَنَا أُحِبُّ التُّفَّاح", "sentence_en": "I love apples", "difficulty": 1},
    {"id": "s2", "words_ar": ["هَذَا", "كِتَاب", "جَمِيل"], "words_en": ["This is", "a book", "beautiful"], "sentence_ar": "هَذَا كِتَاب جَمِيل", "sentence_en": "This is a beautiful book", "difficulty": 1},
    {"id": "s3", "words_ar": ["الْوَلَد", "يَلْعَبُ", "فِي الْحَدِيقَة"], "words_en": ["The boy", "plays", "in the park"], "sentence_ar": "الْوَلَد يَلْعَبُ فِي الْحَدِيقَة", "sentence_en": "The boy plays in the park", "difficulty": 2},
    {"id": "s4", "words_ar": ["ذَهَبْتُ", "إِلَى", "الْمَسْجِد"], "words_en": ["I went", "to", "the mosque"], "sentence_ar": "ذَهَبْتُ إِلَى الْمَسْجِد", "sentence_en": "I went to the mosque", "difficulty": 1},
    {"id": "s5", "words_ar": ["الشَّمْسُ", "سَاطِعَة", "الْيَوْم"], "words_en": ["The sun", "is bright", "today"], "sentence_ar": "الشَّمْسُ سَاطِعَة الْيَوْم", "sentence_en": "The sun is bright today", "difficulty": 2},
    {"id": "s6", "words_ar": ["أُمِّي", "تَطْبَخُ", "طَعَامًا", "لَذِيذًا"], "words_en": ["My mother", "cooks", "food", "delicious"], "sentence_ar": "أُمِّي تَطْبَخُ طَعَامًا لَذِيذًا", "sentence_en": "My mother cooks delicious food", "difficulty": 2},
    {"id": "s7", "words_ar": ["الْقَمَر", "جَمِيل", "فِي اللَّيْل"], "words_en": ["The moon", "is beautiful", "at night"], "sentence_ar": "الْقَمَر جَمِيل فِي اللَّيْل", "sentence_en": "The moon is beautiful at night", "difficulty": 2},
    {"id": "s8", "words_ar": ["بِسْمِ اللَّه", "الرَّحْمَن", "الرَّحِيم"], "words_en": ["In the name of Allah", "the Most Gracious", "the Most Merciful"], "sentence_ar": "بِسْمِ اللَّه الرَّحْمَن الرَّحِيم", "sentence_en": "In the name of Allah, the Most Gracious, the Most Merciful", "difficulty": 1},
    {"id": "s9", "words_ar": ["قَرَأَ", "الطِّفْل", "الْقُرْآن"], "words_en": ["Read", "the child", "the Quran"], "sentence_ar": "قَرَأَ الطِّفْل الْقُرْآن", "sentence_en": "The child read the Quran", "difficulty": 2},
    {"id": "s10", "words_ar": ["الْمَاء", "ضَرُورِيّ", "لِلْحَيَاة"], "words_en": ["Water", "is essential", "for life"], "sentence_ar": "الْمَاء ضَرُورِيّ لِلْحَيَاة", "sentence_en": "Water is essential for life", "difficulty": 3},
]

# Build 90-day curriculum
def build_90_day_curriculum():
    days = []
    day_num = 0
    # Level 1: Alphabet (Days 1-30) - 28 letters + 2 review
    for i, letter in enumerate(ARABIC_LETTERS):
        day_num += 1
        days.append({"day": day_num, "level": 1, "type": "letter", "content_id": letter["id"],
                      "title_en": f"Letter: {letter['name_en']}", "title_ar": f"حرف: {letter['name_ar']}", "xp": 10})
    days.append({"day": 29, "level": 1, "type": "review", "content_id": 0, "title_en": "Alphabet Review 1", "title_ar": "مراجعة الأبجدية ١", "xp": 20})
    days.append({"day": 30, "level": 1, "type": "review", "content_id": 0, "title_en": "Alphabet Review 2", "title_ar": "مراجعة الأبجدية ٢", "xp": 20})
    
    # Level 2: Numbers (Days 31-42)
    for i, num in enumerate(ARABIC_NUMBERS):
        day_num = 31 + i
        if day_num > 42:
            break
        days.append({"day": day_num, "level": 2, "type": "number", "content_id": num["id"],
                      "title_en": f"Number: {num['word_en']}", "title_ar": f"رقم: {num['word_ar']}", "xp": 10})
    
    # Level 3: Vocabulary (Days 43-78)
    all_vocab = []
    for cat_words in VOCAB_CATEGORIES.values():
        all_vocab.extend(cat_words)
    for i in range(36):
        day_num = 43 + i
        vocab_idx = i % len(all_vocab)
        v = all_vocab[vocab_idx]
        days.append({"day": day_num, "level": 3, "type": "vocab", "content_id": v["id"],
                      "title_en": f"Word: {v['meaning_en']}", "title_ar": f"كلمة: {v['word']}", "xp": 10})
    
    # Level 4: Sentences (Days 79-90)
    for i in range(12):
        day_num = 79 + i
        sent_idx = i % len(SENTENCE_TEMPLATES)
        s = SENTENCE_TEMPLATES[sent_idx]
        days.append({"day": day_num, "level": 4, "type": "sentence", "content_id": s["id"],
                      "title_en": f"Sentence: {s['sentence_en'][:30]}...", "title_ar": f"جملة: {s['sentence_ar'][:30]}...", "xp": 15})
    
    return days

CURRICULUM_90 = build_90_day_curriculum()

@router.get("/arabic-academy/curriculum")
async def get_curriculum():
    """Get the full 90-day curriculum"""
    return {"success": True, "curriculum": CURRICULUM_90, "total_days": len(CURRICULUM_90)}

@router.get("/arabic-academy/curriculum/day/{day}")
async def get_curriculum_day(day: int):
    """Get specific day lesson"""
    lesson = next((d for d in CURRICULUM_90 if d["day"] == day), None)
    if not lesson:
        raise HTTPException(status_code=404, detail="Day not found")
    
    content = None
    if lesson["type"] == "letter":
        content = next((lt for lt in ARABIC_LETTERS if lt["id"] == lesson["content_id"]), None)
    elif lesson["type"] == "number":
        content = next((n for n in ARABIC_NUMBERS if n["id"] == lesson["content_id"]), None)
    elif lesson["type"] == "vocab":
        for cat_words in VOCAB_CATEGORIES.values():
            found = next((v for v in cat_words if v["id"] == lesson["content_id"]), None)
            if found:
                content = found
                break
    elif lesson["type"] == "sentence":
        content = next((s for s in SENTENCE_TEMPLATES if s["id"] == lesson["content_id"]), None)
    
    return {"success": True, "lesson": lesson, "content": content}

@router.get("/arabic-academy/numbers")
async def get_arabic_numbers():
    """Get all Arabic numbers"""
    return {"success": True, "numbers": ARABIC_NUMBERS, "total": len(ARABIC_NUMBERS)}

@router.get("/arabic-academy/vocabulary")
async def get_vocabulary(category: str = "all"):
    """Get vocabulary by category"""
    if category == "all":
        all_words = []
        for cat, words in VOCAB_CATEGORIES.items():
            for w in words:
                all_words.append({**w, "category": cat})
        return {"success": True, "words": all_words, "total": len(all_words), "categories": list(VOCAB_CATEGORIES.keys())}
    elif category in VOCAB_CATEGORIES:
        words = [{**w, "category": category} for w in VOCAB_CATEGORIES[category]]
        return {"success": True, "words": words, "total": len(words), "categories": list(VOCAB_CATEGORIES.keys())}
    raise HTTPException(status_code=404, detail="Category not found")

@router.get("/arabic-academy/sentences")
async def get_sentences(difficulty: int = 0):
    """Get sentence building templates"""
    sentences = SENTENCE_TEMPLATES
    if difficulty > 0:
        sentences = [s for s in sentences if s["difficulty"] == difficulty]
    return {"success": True, "sentences": sentences, "total": len(sentences)}

@router.post("/arabic-academy/progress-v2")
async def save_progress_v2(data: dict):
    """Save enhanced progress with growth tree and day tracking"""
    user_id = data.get("user_id", "guest")
    update = {
        "user_id": user_id,
        "completed_days": data.get("completed_days", []),
        "completed_letters": data.get("completed_letters", []),
        "completed_numbers": data.get("completed_numbers", []),
        "completed_vocab": data.get("completed_vocab", []),
        "completed_sentences": data.get("completed_sentences", []),
        "stars": data.get("stars", 0),
        "total_xp": data.get("total_xp", 0),
        "golden_bricks": data.get("golden_bricks", 0),
        "tree_level": data.get("tree_level", 1),
        "streak": data.get("streak", 0),
        "last_activity": datetime.utcnow().isoformat(),
    }
    await db.arabic_progress.update_one({"user_id": user_id}, {"$set": update}, upsert=True)
    return {"success": True, "message": "Progress saved"}

@router.get("/arabic-academy/progress-v2/{user_id}")
async def get_progress_v2(user_id: str):
    """Get enhanced progress"""
    progress = await db.arabic_progress.find_one({"user_id": user_id})
    if not progress:
        progress = {
            "user_id": user_id, "completed_days": [], "completed_letters": [], "completed_numbers": [],
            "completed_vocab": [], "completed_sentences": [], "stars": 0, "total_xp": 0,
            "golden_bricks": 0, "tree_level": 1, "streak": 0, "last_activity": None
        }
    progress.pop("_id", None)
    return {"success": True, "progress": progress}

# ==================== LIVE STREAMS (MongoDB-backed + Admin CRUD) ====================

DEFAULT_STREAMS = [
    {
        "id": str(uuid.uuid4())[:8],
        "name": "Makkah Live - الحرم المكي",
        "embed_type": "channel",
        "embed_value": "UC2l1w7FCuff2-h429sAUSXQ",
        "thumbnail": "",
        "city": "Makkah",
        "country": "Saudi Arabia",
        "category": "haramain",
        "is_247": True,
        "is_active": True,
        "sort_order": 1
    },
    {
        "id": str(uuid.uuid4())[:8],
        "name": "Madinah Live - المسجد النبوي",
        "embed_type": "video",
        "embed_value": "rHWSRMcGGBQ",
        "thumbnail": "",
        "city": "Madinah",
        "country": "Saudi Arabia",
        "category": "haramain",
        "is_247": True,
        "is_active": True,
        "sort_order": 2
    },
    {
        "id": str(uuid.uuid4())[:8],
        "name": "Al-Aqsa Mosque Live - المسجد الأقصى",
        "embed_type": "channel",
        "embed_value": "UC2l1w7FCuff2-h429sAUSXQ",
        "thumbnail": "",
        "city": "Jerusalem",
        "country": "Palestine",
        "category": "holy",
        "is_247": True,
        "is_active": True,
        "sort_order": 3
    },
]


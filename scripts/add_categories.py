#!/usr/bin/env python3
"""Add story/sohba category + Noor translations to ALL locale files."""
import json, os

BASE_DIR = '/app/frontend/src/locales'

# Category translations for all languages
CATEGORY_TRANSLATIONS = {
    "ar": {
        "storyCatGeneral": "عام", "storyCatIstighfar": "قصص الاستغفار", "storyCatSahaba": "قصص الصحابة",
        "storyCatQuran": "قصص القرآن", "storyCatProphets": "قصص الأنبياء", "storyCatRuqyah": "قصص الرقية",
        "storyCatRizq": "قصص الرزق", "storyCatTawba": "قصص التوبة", "storyCatMiracles": "معجزات وعبر",
        "storyCatEmbed": "فيديوهات",
        "sohbaCatGeneral": "عام", "sohbaCatQuran": "القرآن الكريم", "sohbaCatHadith": "الحديث الشريف",
        "sohbaCatRamadan": "رمضان", "sohbaCatDua": "الدعاء والأذكار", "sohbaCatStories": "قصص وعبر",
        "sohbaCatHajj": "الحج والعمرة", "sohbaCatHalal": "السفر الحلال", "sohbaCatFamily": "الأسرة المسلمة",
        "sohbaCatYouth": "الشباب",
        "noorGreetingSv": "Hej! Jag är Noor!", "noorGreetingNl": "Hallo! Ik ben Noor!",
        "noorGreetingEl": "Γεια! Είμαι ο Νουρ!",
    },
    "en": {
        "storyCatGeneral": "General", "storyCatIstighfar": "Istighfar Stories", "storyCatSahaba": "Companions Stories",
        "storyCatQuran": "Quran Stories", "storyCatProphets": "Prophet Stories", "storyCatRuqyah": "Ruqyah Stories",
        "storyCatRizq": "Provision Stories", "storyCatTawba": "Repentance Stories", "storyCatMiracles": "Miracles & Lessons",
        "storyCatEmbed": "Videos",
        "sohbaCatGeneral": "General", "sohbaCatQuran": "Holy Quran", "sohbaCatHadith": "Noble Hadith",
        "sohbaCatRamadan": "Ramadan", "sohbaCatDua": "Duas & Adhkar", "sohbaCatStories": "Stories & Lessons",
        "sohbaCatHajj": "Hajj & Umrah", "sohbaCatHalal": "Halal Travel", "sohbaCatFamily": "Muslim Family",
        "sohbaCatYouth": "Youth",
    },
    "de": {
        "storyCatGeneral": "Allgemein", "storyCatIstighfar": "Istighfar-Geschichten", "storyCatSahaba": "Gefährten-Geschichten",
        "storyCatQuran": "Koran-Geschichten", "storyCatProphets": "Propheten-Geschichten", "storyCatRuqyah": "Ruqyah-Geschichten",
        "storyCatRizq": "Versorgung-Geschichten", "storyCatTawba": "Reue-Geschichten", "storyCatMiracles": "Wunder & Lehren",
        "storyCatEmbed": "Videos",
        "sohbaCatGeneral": "Allgemein", "sohbaCatQuran": "Heiliger Quran", "sohbaCatHadith": "Edler Hadith",
        "sohbaCatRamadan": "Ramadan", "sohbaCatDua": "Duas & Adhkar", "sohbaCatStories": "Geschichten & Lehren",
        "sohbaCatHajj": "Hajj & Umrah", "sohbaCatHalal": "Halal-Reisen", "sohbaCatFamily": "Muslimische Familie",
        "sohbaCatYouth": "Jugend",
    },
    "fr": {
        "storyCatGeneral": "Général", "storyCatIstighfar": "Histoires d'Istighfar", "storyCatSahaba": "Histoires des Compagnons",
        "storyCatQuran": "Histoires du Coran", "storyCatProphets": "Histoires des Prophètes", "storyCatRuqyah": "Histoires de Ruqyah",
        "storyCatRizq": "Histoires de Subsistance", "storyCatTawba": "Histoires de Repentir", "storyCatMiracles": "Miracles & Leçons",
        "storyCatEmbed": "Vidéos",
        "sohbaCatGeneral": "Général", "sohbaCatQuran": "Saint Coran", "sohbaCatHadith": "Noble Hadith",
        "sohbaCatRamadan": "Ramadan", "sohbaCatDua": "Duas & Adhkar", "sohbaCatStories": "Histoires & Leçons",
        "sohbaCatHajj": "Hajj & Omra", "sohbaCatHalal": "Voyage Halal", "sohbaCatFamily": "Famille Musulmane",
        "sohbaCatYouth": "Jeunesse",
    },
    "tr": {
        "storyCatGeneral": "Genel", "storyCatIstighfar": "İstiğfar Hikayeleri", "storyCatSahaba": "Sahabe Hikayeleri",
        "storyCatQuran": "Kur'an Kıssaları", "storyCatProphets": "Peygamber Kıssaları", "storyCatRuqyah": "Rukye Hikayeleri",
        "storyCatRizq": "Rızık Hikayeleri", "storyCatTawba": "Tövbe Hikayeleri", "storyCatMiracles": "Mucizeler ve İbretler",
        "storyCatEmbed": "Videolar",
        "sohbaCatGeneral": "Genel", "sohbaCatQuran": "Kur'an-ı Kerim", "sohbaCatHadith": "Hadis-i Şerif",
        "sohbaCatRamadan": "Ramazan", "sohbaCatDua": "Dua ve Zikir", "sohbaCatStories": "Kıssalar ve İbretler",
        "sohbaCatHajj": "Hac ve Umre", "sohbaCatHalal": "Helal Seyahat", "sohbaCatFamily": "Müslüman Aile",
        "sohbaCatYouth": "Gençlik",
    },
    "ru": {
        "storyCatGeneral": "Общие", "storyCatIstighfar": "Истории Истигфара", "storyCatSahaba": "Истории Сахабов",
        "storyCatQuran": "Истории Корана", "storyCatProphets": "Истории Пророков", "storyCatRuqyah": "Истории Рукьи",
        "storyCatRizq": "Истории Ризка", "storyCatTawba": "Истории Покаяния", "storyCatMiracles": "Чудеса и Уроки",
        "storyCatEmbed": "Видео",
        "sohbaCatGeneral": "Общие", "sohbaCatQuran": "Священный Коран", "sohbaCatHadith": "Благородный Хадис",
        "sohbaCatRamadan": "Рамадан", "sohbaCatDua": "Дуа и Зикр", "sohbaCatStories": "Истории и Уроки",
        "sohbaCatHajj": "Хадж и Умра", "sohbaCatHalal": "Халяль путешествия", "sohbaCatFamily": "Мусульманская семья",
        "sohbaCatYouth": "Молодёжь",
    },
    "sv": {
        "storyCatGeneral": "Allmänt", "storyCatIstighfar": "Istighfar-berättelser", "storyCatSahaba": "Sahaba-berättelser",
        "storyCatQuran": "Koranberättelser", "storyCatProphets": "Profetberättelser", "storyCatRuqyah": "Ruqyah-berättelser",
        "storyCatRizq": "Försörjningsberättelser", "storyCatTawba": "Ångerberättelser", "storyCatMiracles": "Mirakel och lärdomar",
        "storyCatEmbed": "Videor",
        "sohbaCatGeneral": "Allmänt", "sohbaCatQuran": "Heliga Koranen", "sohbaCatHadith": "Ädla Hadith",
        "sohbaCatRamadan": "Ramadan", "sohbaCatDua": "Duas och Adhkar", "sohbaCatStories": "Berättelser och lärdomar",
        "sohbaCatHajj": "Hajj och Umrah", "sohbaCatHalal": "Halalresor", "sohbaCatFamily": "Muslimsk familj",
        "sohbaCatYouth": "Ungdom",
    },
    "nl": {
        "storyCatGeneral": "Algemeen", "storyCatIstighfar": "Istighfar-verhalen", "storyCatSahaba": "Metgezellenverhalen",
        "storyCatQuran": "Koranverhalen", "storyCatProphets": "Profetengeschiedenissen", "storyCatRuqyah": "Ruqyah-verhalen",
        "storyCatRizq": "Voorzieningsverhalen", "storyCatTawba": "Berouwverhalen", "storyCatMiracles": "Wonderen en lessen",
        "storyCatEmbed": "Video's",
        "sohbaCatGeneral": "Algemeen", "sohbaCatQuran": "Heilige Koran", "sohbaCatHadith": "Nobele Hadith",
        "sohbaCatRamadan": "Ramadan", "sohbaCatDua": "Duas en Adhkar", "sohbaCatStories": "Verhalen en lessen",
        "sohbaCatHajj": "Hadj en Umrah", "sohbaCatHalal": "Halal reizen", "sohbaCatFamily": "Moslimfamilie",
        "sohbaCatYouth": "Jongeren",
    },
    "el": {
        "storyCatGeneral": "Γενικά", "storyCatIstighfar": "Ιστορίες Ιστιγκφάρ", "storyCatSahaba": "Ιστορίες Σαχάμπα",
        "storyCatQuran": "Ιστορίες Κορανίου", "storyCatProphets": "Ιστορίες Προφητών", "storyCatRuqyah": "Ιστορίες Ρουκγιά",
        "storyCatRizq": "Ιστορίες Προνοίας", "storyCatTawba": "Ιστορίες Μετάνοιας", "storyCatMiracles": "Θαύματα και μαθήματα",
        "storyCatEmbed": "Βίντεο",
        "sohbaCatGeneral": "Γενικά", "sohbaCatQuran": "Ιερό Κοράνι", "sohbaCatHadith": "Ευγενές Χαντίθ",
        "sohbaCatRamadan": "Ραμαζάνι", "sohbaCatDua": "Ντουά και Adhkar", "sohbaCatStories": "Ιστορίες και μαθήματα",
        "sohbaCatHajj": "Χατζ και Ούμρα", "sohbaCatHalal": "Χαλάλ ταξίδια", "sohbaCatFamily": "Μουσουλμανική οικογένεια",
        "sohbaCatYouth": "Νεολαία",
    },
}

for lang, translations in CATEGORY_TRANSLATIONS.items():
    filepath = os.path.join(BASE_DIR, f'{lang}.json')
    if not os.path.exists(filepath):
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    added = 0
    for key, value in translations.items():
        if key not in data:
            data[key] = value
            added += 1
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"{lang}.json: {added} category keys added")

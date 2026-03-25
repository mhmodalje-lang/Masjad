"""
Arabic Academy Multilingual Data — 2026 Educational Standard
All content filtered by locale: ar, en, de, fr, tr, ru, sv, nl, el
Each user sees ONLY their language + Arabic. No mixed languages.
"""

# ═══════════════════════════════════════════════════════════════
# ARABIC LETTERS — Translated names and example meanings (9 langs)
# ═══════════════════════════════════════════════════════════════
LETTER_TRANSLATIONS = {
    1: {"name": {"en": "Alif", "de": "Alif", "fr": "Alif", "tr": "Elif", "ru": "Алиф", "sv": "Alif", "nl": "Alif", "el": "Αλίφ"},
        "example_meaning": {"en": "Lion", "de": "Löwe", "fr": "Lion", "tr": "Aslan", "ru": "Лев", "sv": "Lejon", "nl": "Leeuw", "el": "Λιοντάρι"}},
    2: {"name": {"en": "Ba", "de": "Ba", "fr": "Ba", "tr": "Be", "ru": "Ба", "sv": "Ba", "nl": "Ba", "el": "Μπα"},
        "example_meaning": {"en": "House", "de": "Haus", "fr": "Maison", "tr": "Ev", "ru": "Дом", "sv": "Hus", "nl": "Huis", "el": "Σπίτι"}},
    3: {"name": {"en": "Ta", "de": "Ta", "fr": "Ta", "tr": "Te", "ru": "Та", "sv": "Ta", "nl": "Ta", "el": "Τα"},
        "example_meaning": {"en": "Apple", "de": "Apfel", "fr": "Pomme", "tr": "Elma", "ru": "Яблоко", "sv": "Äpple", "nl": "Appel", "el": "Μήλο"}},
    4: {"name": {"en": "Tha", "de": "Tha", "fr": "Tha", "tr": "Se", "ru": "Са", "sv": "Tha", "nl": "Tha", "el": "Θα"},
        "example_meaning": {"en": "Fox", "de": "Fuchs", "fr": "Renard", "tr": "Tilki", "ru": "Лиса", "sv": "Räv", "nl": "Vos", "el": "Αλεπού"}},
    5: {"name": {"en": "Jim", "de": "Dschim", "fr": "Jim", "tr": "Cim", "ru": "Джим", "sv": "Jim", "nl": "Jim", "el": "Τζιμ"},
        "example_meaning": {"en": "Camel", "de": "Kamel", "fr": "Chameau", "tr": "Deve", "ru": "Верблюд", "sv": "Kamel", "nl": "Kameel", "el": "Καμήλα"}},
    6: {"name": {"en": "Ha", "de": "Ha", "fr": "Ha", "tr": "Ha", "ru": "Ха", "sv": "Ha", "nl": "Ha", "el": "Χα"},
        "example_meaning": {"en": "Horse", "de": "Pferd", "fr": "Cheval", "tr": "At", "ru": "Лошадь", "sv": "Häst", "nl": "Paard", "el": "Άλογο"}},
    7: {"name": {"en": "Kha", "de": "Cha", "fr": "Kha", "tr": "Hı", "ru": "Ха", "sv": "Kha", "nl": "Kha", "el": "Χα"},
        "example_meaning": {"en": "Sheep", "de": "Schaf", "fr": "Mouton", "tr": "Koyun", "ru": "Овца", "sv": "Får", "nl": "Schaap", "el": "Πρόβατο"}},
    8: {"name": {"en": "Dal", "de": "Dal", "fr": "Dal", "tr": "Dal", "ru": "Даль", "sv": "Dal", "nl": "Dal", "el": "Νταλ"},
        "example_meaning": {"en": "Rooster", "de": "Hahn", "fr": "Coq", "tr": "Horoz", "ru": "Петух", "sv": "Tupp", "nl": "Haan", "el": "Κόκορας"}},
    9: {"name": {"en": "Dhal", "de": "Dhal", "fr": "Dhal", "tr": "Zel", "ru": "Заль", "sv": "Dhal", "nl": "Dhal", "el": "Ντζαλ"},
        "example_meaning": {"en": "Wolf", "de": "Wolf", "fr": "Loup", "tr": "Kurt", "ru": "Волк", "sv": "Varg", "nl": "Wolf", "el": "Λύκος"}},
    10: {"name": {"en": "Ra", "de": "Ra", "fr": "Ra", "tr": "Re", "ru": "Ра", "sv": "Ra", "nl": "Ra", "el": "Ρα"},
         "example_meaning": {"en": "Pomegranate", "de": "Granatapfel", "fr": "Grenade", "tr": "Nar", "ru": "Гранат", "sv": "Granatäpple", "nl": "Granaatappel", "el": "Ρόδι"}},
    11: {"name": {"en": "Zay", "de": "Zay", "fr": "Zay", "tr": "Ze", "ru": "Зай", "sv": "Zay", "nl": "Zay", "el": "Ζάι"},
         "example_meaning": {"en": "Flower", "de": "Blume", "fr": "Fleur", "tr": "Çiçek", "ru": "Цветок", "sv": "Blomma", "nl": "Bloem", "el": "Λουλούδι"}},
    12: {"name": {"en": "Sin", "de": "Sin", "fr": "Sin", "tr": "Sin", "ru": "Син", "sv": "Sin", "nl": "Sin", "el": "Σιν"},
         "example_meaning": {"en": "Fish", "de": "Fisch", "fr": "Poisson", "tr": "Balık", "ru": "Рыба", "sv": "Fisk", "nl": "Vis", "el": "Ψάρι"}},
    13: {"name": {"en": "Shin", "de": "Schin", "fr": "Shin", "tr": "Şın", "ru": "Шин", "sv": "Shin", "nl": "Sjin", "el": "Σιν"},
         "example_meaning": {"en": "Sun", "de": "Sonne", "fr": "Soleil", "tr": "Güneş", "ru": "Солнце", "sv": "Sol", "nl": "Zon", "el": "Ήλιος"}},
    14: {"name": {"en": "Sad", "de": "Sad", "fr": "Sad", "tr": "Sad", "ru": "Сад", "sv": "Sad", "nl": "Sad", "el": "Σαντ"},
         "example_meaning": {"en": "Falcon", "de": "Falke", "fr": "Faucon", "tr": "Şahin", "ru": "Сокол", "sv": "Falk", "nl": "Valk", "el": "Γεράκι"}},
    15: {"name": {"en": "Dad", "de": "Dad", "fr": "Dad", "tr": "Dad", "ru": "Дад", "sv": "Dad", "nl": "Dad", "el": "Ντατ"},
         "example_meaning": {"en": "Frog", "de": "Frosch", "fr": "Grenouille", "tr": "Kurbağa", "ru": "Лягушка", "sv": "Groda", "nl": "Kikker", "el": "Βάτραχος"}},
    16: {"name": {"en": "Tah", "de": "Tah", "fr": "Tah", "tr": "Tı", "ru": "Та", "sv": "Tah", "nl": "Tah", "el": "Τα"},
         "example_meaning": {"en": "Bird", "de": "Vogel", "fr": "Oiseau", "tr": "Kuş", "ru": "Птица", "sv": "Fågel", "nl": "Vogel", "el": "Πουλί"}},
    17: {"name": {"en": "Zah", "de": "Zah", "fr": "Zah", "tr": "Zı", "ru": "За", "sv": "Zah", "nl": "Zah", "el": "Ζα"},
         "example_meaning": {"en": "Gazelle", "de": "Gazelle", "fr": "Gazelle", "tr": "Ceylan", "ru": "Газель", "sv": "Gasell", "nl": "Gazelle", "el": "Γαζέλα"}},
    18: {"name": {"en": "Ain", "de": "Ain", "fr": "Ain", "tr": "Ayn", "ru": "Айн", "sv": "Ain", "nl": "Ain", "el": "Αϊν"},
         "example_meaning": {"en": "Grapes", "de": "Trauben", "fr": "Raisins", "tr": "Üzüm", "ru": "Виноград", "sv": "Druvor", "nl": "Druiven", "el": "Σταφύλια"}},
    19: {"name": {"en": "Ghain", "de": "Ghain", "fr": "Ghain", "tr": "Gayn", "ru": "Гайн", "sv": "Ghain", "nl": "Ghain", "el": "Γκάιν"},
         "example_meaning": {"en": "Deer", "de": "Hirsch", "fr": "Cerf", "tr": "Geyik", "ru": "Олень", "sv": "Hjort", "nl": "Hert", "el": "Ελάφι"}},
    20: {"name": {"en": "Fa", "de": "Fa", "fr": "Fa", "tr": "Fe", "ru": "Фа", "sv": "Fa", "nl": "Fa", "el": "Φα"},
         "example_meaning": {"en": "Elephant", "de": "Elefant", "fr": "Éléphant", "tr": "Fil", "ru": "Слон", "sv": "Elefant", "nl": "Olifant", "el": "Ελέφαντας"}},
    21: {"name": {"en": "Qaf", "de": "Qaf", "fr": "Qaf", "tr": "Kaf", "ru": "Каф", "sv": "Qaf", "nl": "Qaf", "el": "Καφ"},
         "example_meaning": {"en": "Moon", "de": "Mond", "fr": "Lune", "tr": "Ay", "ru": "Луна", "sv": "Måne", "nl": "Maan", "el": "Φεγγάρι"}},
    22: {"name": {"en": "Kaf", "de": "Kaf", "fr": "Kaf", "tr": "Kef", "ru": "Каф", "sv": "Kaf", "nl": "Kaf", "el": "Καφ"},
         "example_meaning": {"en": "Book", "de": "Buch", "fr": "Livre", "tr": "Kitap", "ru": "Книга", "sv": "Bok", "nl": "Boek", "el": "Βιβλίο"}},
    23: {"name": {"en": "Lam", "de": "Lam", "fr": "Lam", "tr": "Lam", "ru": "Лям", "sv": "Lam", "nl": "Lam", "el": "Λαμ"},
         "example_meaning": {"en": "Lemon", "de": "Zitrone", "fr": "Citron", "tr": "Limon", "ru": "Лимон", "sv": "Citron", "nl": "Citroen", "el": "Λεμόνι"}},
    24: {"name": {"en": "Mim", "de": "Mim", "fr": "Mim", "tr": "Mim", "ru": "Мим", "sv": "Mim", "nl": "Mim", "el": "Μιμ"},
         "example_meaning": {"en": "Mosque", "de": "Moschee", "fr": "Mosquée", "tr": "Cami", "ru": "Мечеть", "sv": "Moské", "nl": "Moskee", "el": "Τζαμί"}},
    25: {"name": {"en": "Nun", "de": "Nun", "fr": "Noun", "tr": "Nun", "ru": "Нун", "sv": "Nun", "nl": "Nun", "el": "Νουν"},
         "example_meaning": {"en": "Star", "de": "Stern", "fr": "Étoile", "tr": "Yıldız", "ru": "Звезда", "sv": "Stjärna", "nl": "Ster", "el": "Αστέρι"}},
    26: {"name": {"en": "Ha", "de": "Ha", "fr": "Ha", "tr": "He", "ru": "Ха", "sv": "Ha", "nl": "Ha", "el": "Χα"},
         "example_meaning": {"en": "Crescent", "de": "Halbmond", "fr": "Croissant", "tr": "Hilal", "ru": "Полумесяц", "sv": "Halvmåne", "nl": "Halve maan", "el": "Ημισέληνος"}},
    27: {"name": {"en": "Waw", "de": "Waw", "fr": "Waw", "tr": "Vav", "ru": "Вав", "sv": "Waw", "nl": "Waw", "el": "Βαβ"},
         "example_meaning": {"en": "Rose", "de": "Rose", "fr": "Rose", "tr": "Gül", "ru": "Роза", "sv": "Ros", "nl": "Roos", "el": "Τριαντάφυλλο"}},
    28: {"name": {"en": "Ya", "de": "Ya", "fr": "Ya", "tr": "Ye", "ru": "Йа", "sv": "Ya", "nl": "Ya", "el": "Για"},
         "example_meaning": {"en": "Hand", "de": "Hand", "fr": "Main", "tr": "El", "ru": "Рука", "sv": "Hand", "nl": "Hand", "el": "Χέρι"}},
}

# ═══════════════════════════════════════════════════════════════
# ARABIC NUMBERS — Translated words (9 langs)
# ═══════════════════════════════════════════════════════════════
NUMBER_TRANSLATIONS = {
    0: {"en": "Zero", "de": "Null", "fr": "Zéro", "tr": "Sıfır", "ru": "Ноль", "sv": "Noll", "nl": "Nul", "el": "Μηδέν"},
    1: {"en": "One", "de": "Eins", "fr": "Un", "tr": "Bir", "ru": "Один", "sv": "Ett", "nl": "Een", "el": "Ένα"},
    2: {"en": "Two", "de": "Zwei", "fr": "Deux", "tr": "İki", "ru": "Два", "sv": "Två", "nl": "Twee", "el": "Δύο"},
    3: {"en": "Three", "de": "Drei", "fr": "Trois", "tr": "Üç", "ru": "Три", "sv": "Tre", "nl": "Drie", "el": "Τρία"},
    4: {"en": "Four", "de": "Vier", "fr": "Quatre", "tr": "Dört", "ru": "Четыре", "sv": "Fyra", "nl": "Vier", "el": "Τέσσερα"},
    5: {"en": "Five", "de": "Fünf", "fr": "Cinq", "tr": "Beş", "ru": "Пять", "sv": "Fem", "nl": "Vijf", "el": "Πέντε"},
    6: {"en": "Six", "de": "Sechs", "fr": "Six", "tr": "Altı", "ru": "Шесть", "sv": "Sex", "nl": "Zes", "el": "Έξι"},
    7: {"en": "Seven", "de": "Sieben", "fr": "Sept", "tr": "Yedi", "ru": "Семь", "sv": "Sju", "nl": "Zeven", "el": "Επτά"},
    8: {"en": "Eight", "de": "Acht", "fr": "Huit", "tr": "Sekiz", "ru": "Восемь", "sv": "Åtta", "nl": "Acht", "el": "Οκτώ"},
    9: {"en": "Nine", "de": "Neun", "fr": "Neuf", "tr": "Dokuz", "ru": "Девять", "sv": "Nio", "nl": "Negen", "el": "Εννέα"},
    10: {"en": "Ten", "de": "Zehn", "fr": "Dix", "tr": "On", "ru": "Десять", "sv": "Tio", "nl": "Tien", "el": "Δέκα"},
    11: {"en": "Twenty", "de": "Zwanzig", "fr": "Vingt", "tr": "Yirmi", "ru": "Двадцать", "sv": "Tjugo", "nl": "Twintig", "el": "Είκοσι"},
    12: {"en": "Thirty", "de": "Dreißig", "fr": "Trente", "tr": "Otuz", "ru": "Тридцать", "sv": "Trettio", "nl": "Dertig", "el": "Τριάντα"},
    13: {"en": "Forty", "de": "Vierzig", "fr": "Quarante", "tr": "Kırk", "ru": "Сорок", "sv": "Fyrtio", "nl": "Veertig", "el": "Σαράντα"},
    14: {"en": "Fifty", "de": "Fünfzig", "fr": "Cinquante", "tr": "Elli", "ru": "Пятьдесят", "sv": "Femtio", "nl": "Vijftig", "el": "Πενήντα"},
    15: {"en": "Hundred", "de": "Hundert", "fr": "Cent", "tr": "Yüz", "ru": "Сто", "sv": "Hundra", "nl": "Honderd", "el": "Εκατό"},
    16: {"en": "Thousand", "de": "Tausend", "fr": "Mille", "tr": "Bin", "ru": "Тысяча", "sv": "Tusen", "nl": "Duizend", "el": "Χίλια"},
}

# ═══════════════════════════════════════════════════════════════
# VOCABULARY CATEGORIES — Complete 9-language translations
# Categories: animals, food, body, family, nature, colors, home, verbs, greetings
# ═══════════════════════════════════════════════════════════════
VOCAB_TRANSLATIONS = {
    # ── Animals ──
    "a1": {"word": "قِطَّة", "transliteration": "Qitta", "emoji": "🐱", "cat": "animals",
           "meaning": {"en": "Cat", "de": "Katze", "fr": "Chat", "tr": "Kedi", "ru": "Кошка", "sv": "Katt", "nl": "Kat", "el": "Γάτα"}},
    "a2": {"word": "كَلْب", "transliteration": "Kalb", "emoji": "🐕", "cat": "animals",
           "meaning": {"en": "Dog", "de": "Hund", "fr": "Chien", "tr": "Köpek", "ru": "Собака", "sv": "Hund", "nl": "Hond", "el": "Σκύλος"}},
    "a3": {"word": "أَسَد", "transliteration": "Asad", "emoji": "🦁", "cat": "animals",
           "meaning": {"en": "Lion", "de": "Löwe", "fr": "Lion", "tr": "Aslan", "ru": "Лев", "sv": "Lejon", "nl": "Leeuw", "el": "Λιοντάρι"}},
    "a4": {"word": "فِيل", "transliteration": "Fiil", "emoji": "🐘", "cat": "animals",
           "meaning": {"en": "Elephant", "de": "Elefant", "fr": "Éléphant", "tr": "Fil", "ru": "Слон", "sv": "Elefant", "nl": "Olifant", "el": "Ελέφαντας"}},
    "a5": {"word": "طَائِر", "transliteration": "Taa'ir", "emoji": "🐦", "cat": "animals",
           "meaning": {"en": "Bird", "de": "Vogel", "fr": "Oiseau", "tr": "Kuş", "ru": "Птица", "sv": "Fågel", "nl": "Vogel", "el": "Πουλί"}},
    "a6": {"word": "سَمَكَة", "transliteration": "Samaka", "emoji": "🐟", "cat": "animals",
           "meaning": {"en": "Fish", "de": "Fisch", "fr": "Poisson", "tr": "Balık", "ru": "Рыба", "sv": "Fisk", "nl": "Vis", "el": "Ψάρι"}},
    "a7": {"word": "حِصَان", "transliteration": "Hisan", "emoji": "🐴", "cat": "animals",
           "meaning": {"en": "Horse", "de": "Pferd", "fr": "Cheval", "tr": "At", "ru": "Лошадь", "sv": "Häst", "nl": "Paard", "el": "Άλογο"}},
    "a8": {"word": "أَرْنَب", "transliteration": "Arnab", "emoji": "🐰", "cat": "animals",
           "meaning": {"en": "Rabbit", "de": "Kaninchen", "fr": "Lapin", "tr": "Tavşan", "ru": "Кролик", "sv": "Kanin", "nl": "Konijn", "el": "Κουνέλι"}},
    "a9": {"word": "بَقَرَة", "transliteration": "Baqara", "emoji": "🐄", "cat": "animals",
           "meaning": {"en": "Cow", "de": "Kuh", "fr": "Vache", "tr": "İnek", "ru": "Корова", "sv": "Ko", "nl": "Koe", "el": "Αγελάδα"}},
    "a10": {"word": "خَرُوف", "transliteration": "Kharuf", "emoji": "🐑", "cat": "animals",
            "meaning": {"en": "Sheep", "de": "Schaf", "fr": "Mouton", "tr": "Koyun", "ru": "Овца", "sv": "Får", "nl": "Schaap", "el": "Πρόβατο"}},
    # ── Food ──
    "f1": {"word": "تُفَّاحَة", "transliteration": "Tuffaha", "emoji": "🍎", "cat": "food",
           "meaning": {"en": "Apple", "de": "Apfel", "fr": "Pomme", "tr": "Elma", "ru": "Яблоко", "sv": "Äpple", "nl": "Appel", "el": "Μήλο"}},
    "f2": {"word": "مَوْز", "transliteration": "Mawz", "emoji": "🍌", "cat": "food",
           "meaning": {"en": "Banana", "de": "Banane", "fr": "Banane", "tr": "Muz", "ru": "Банан", "sv": "Banan", "nl": "Banaan", "el": "Μπανάνα"}},
    "f3": {"word": "خُبْز", "transliteration": "Khubz", "emoji": "🍞", "cat": "food",
           "meaning": {"en": "Bread", "de": "Brot", "fr": "Pain", "tr": "Ekmek", "ru": "Хлеб", "sv": "Bröd", "nl": "Brood", "el": "Ψωμί"}},
    "f4": {"word": "مَاء", "transliteration": "Maa'", "emoji": "💧", "cat": "food",
           "meaning": {"en": "Water", "de": "Wasser", "fr": "Eau", "tr": "Su", "ru": "Вода", "sv": "Vatten", "nl": "Water", "el": "Νερό"}},
    "f5": {"word": "حَلِيب", "transliteration": "Haleeb", "emoji": "🥛", "cat": "food",
           "meaning": {"en": "Milk", "de": "Milch", "fr": "Lait", "tr": "Süt", "ru": "Молоко", "sv": "Mjölk", "nl": "Melk", "el": "Γάλα"}},
    "f6": {"word": "أُرْز", "transliteration": "Urz", "emoji": "🍚", "cat": "food",
           "meaning": {"en": "Rice", "de": "Reis", "fr": "Riz", "tr": "Pirinç", "ru": "Рис", "sv": "Ris", "nl": "Rijst", "el": "Ρύζι"}},
    "f7": {"word": "بَيْض", "transliteration": "Bayd", "emoji": "🥚", "cat": "food",
           "meaning": {"en": "Eggs", "de": "Eier", "fr": "Œufs", "tr": "Yumurta", "ru": "Яйца", "sv": "Ägg", "nl": "Eieren", "el": "Αυγά"}},
    "f8": {"word": "عَسَل", "transliteration": "Asal", "emoji": "🍯", "cat": "food",
           "meaning": {"en": "Honey", "de": "Honig", "fr": "Miel", "tr": "Bal", "ru": "Мёд", "sv": "Honung", "nl": "Honing", "el": "Μέλι"}},
    "f9": {"word": "بُرْتُقَالَة", "transliteration": "Burtuqala", "emoji": "🍊", "cat": "food",
           "meaning": {"en": "Orange", "de": "Orange", "fr": "Orange", "tr": "Portakal", "ru": "Апельсин", "sv": "Apelsin", "nl": "Sinaasappel", "el": "Πορτοκάλι"}},
    "f10": {"word": "عِنَب", "transliteration": "Inab", "emoji": "🍇", "cat": "food",
            "meaning": {"en": "Grapes", "de": "Trauben", "fr": "Raisins", "tr": "Üzüm", "ru": "Виноград", "sv": "Druvor", "nl": "Druiven", "el": "Σταφύλια"}},
    # ── Body ──
    "b1": {"word": "رَأْس", "transliteration": "Ra's", "emoji": "🗣️", "cat": "body",
           "meaning": {"en": "Head", "de": "Kopf", "fr": "Tête", "tr": "Baş", "ru": "Голова", "sv": "Huvud", "nl": "Hoofd", "el": "Κεφάλι"}},
    "b2": {"word": "يَد", "transliteration": "Yad", "emoji": "✋", "cat": "body",
           "meaning": {"en": "Hand", "de": "Hand", "fr": "Main", "tr": "El", "ru": "Рука", "sv": "Hand", "nl": "Hand", "el": "Χέρι"}},
    "b3": {"word": "عَيْن", "transliteration": "Ayn", "emoji": "👁️", "cat": "body",
           "meaning": {"en": "Eye", "de": "Auge", "fr": "Œil", "tr": "Göz", "ru": "Глаз", "sv": "Öga", "nl": "Oog", "el": "Μάτι"}},
    "b4": {"word": "أُذُن", "transliteration": "Udhun", "emoji": "👂", "cat": "body",
           "meaning": {"en": "Ear", "de": "Ohr", "fr": "Oreille", "tr": "Kulak", "ru": "Ухо", "sv": "Öra", "nl": "Oor", "el": "Αυτί"}},
    "b5": {"word": "قَلْب", "transliteration": "Qalb", "emoji": "❤️", "cat": "body",
           "meaning": {"en": "Heart", "de": "Herz", "fr": "Cœur", "tr": "Kalp", "ru": "Сердце", "sv": "Hjärta", "nl": "Hart", "el": "Καρδιά"}},
    "b6": {"word": "قَدَم", "transliteration": "Qadam", "emoji": "🦶", "cat": "body",
           "meaning": {"en": "Foot", "de": "Fuß", "fr": "Pied", "tr": "Ayak", "ru": "Нога", "sv": "Fot", "nl": "Voet", "el": "Πόδι"}},
    "b7": {"word": "أَنْف", "transliteration": "Anf", "emoji": "👃", "cat": "body",
           "meaning": {"en": "Nose", "de": "Nase", "fr": "Nez", "tr": "Burun", "ru": "Нос", "sv": "Näsa", "nl": "Neus", "el": "Μύτη"}},
    "b8": {"word": "فَم", "transliteration": "Fam", "emoji": "👄", "cat": "body",
           "meaning": {"en": "Mouth", "de": "Mund", "fr": "Bouche", "tr": "Ağız", "ru": "Рот", "sv": "Mun", "nl": "Mond", "el": "Στόμα"}},
    # ── Family ──
    "fm1": {"word": "أَب", "transliteration": "Ab", "emoji": "👨", "cat": "family",
            "meaning": {"en": "Father", "de": "Vater", "fr": "Père", "tr": "Baba", "ru": "Отец", "sv": "Pappa", "nl": "Vader", "el": "Πατέρας"}},
    "fm2": {"word": "أُمّ", "transliteration": "Umm", "emoji": "👩", "cat": "family",
            "meaning": {"en": "Mother", "de": "Mutter", "fr": "Mère", "tr": "Anne", "ru": "Мать", "sv": "Mamma", "nl": "Moeder", "el": "Μητέρα"}},
    "fm3": {"word": "أَخ", "transliteration": "Akh", "emoji": "👦", "cat": "family",
            "meaning": {"en": "Brother", "de": "Bruder", "fr": "Frère", "tr": "Kardeş", "ru": "Брат", "sv": "Bror", "nl": "Broer", "el": "Αδερφός"}},
    "fm4": {"word": "أُخْت", "transliteration": "Ukht", "emoji": "👧", "cat": "family",
            "meaning": {"en": "Sister", "de": "Schwester", "fr": "Sœur", "tr": "Kız kardeş", "ru": "Сестра", "sv": "Syster", "nl": "Zus", "el": "Αδερφή"}},
    "fm5": {"word": "جَدّ", "transliteration": "Jadd", "emoji": "👴", "cat": "family",
            "meaning": {"en": "Grandfather", "de": "Großvater", "fr": "Grand-père", "tr": "Dede", "ru": "Дедушка", "sv": "Farfar", "nl": "Opa", "el": "Παππούς"}},
    "fm6": {"word": "جَدَّة", "transliteration": "Jadda", "emoji": "👵", "cat": "family",
            "meaning": {"en": "Grandmother", "de": "Großmutter", "fr": "Grand-mère", "tr": "Nine", "ru": "Бабушка", "sv": "Farmor", "nl": "Oma", "el": "Γιαγιά"}},
    "fm7": {"word": "طِفْل", "transliteration": "Tifl", "emoji": "👶", "cat": "family",
            "meaning": {"en": "Child", "de": "Kind", "fr": "Enfant", "tr": "Çocuk", "ru": "Ребёнок", "sv": "Barn", "nl": "Kind", "el": "Παιδί"}},
    "fm8": {"word": "عَائِلَة", "transliteration": "Aa'ila", "emoji": "👨‍👩‍👧‍👦", "cat": "family",
            "meaning": {"en": "Family", "de": "Familie", "fr": "Famille", "tr": "Aile", "ru": "Семья", "sv": "Familj", "nl": "Familie", "el": "Οικογένεια"}},
    # ── Nature ──
    "n1": {"word": "شَمْس", "transliteration": "Shams", "emoji": "☀️", "cat": "nature",
           "meaning": {"en": "Sun", "de": "Sonne", "fr": "Soleil", "tr": "Güneş", "ru": "Солнце", "sv": "Sol", "nl": "Zon", "el": "Ήλιος"}},
    "n2": {"word": "قَمَر", "transliteration": "Qamar", "emoji": "🌙", "cat": "nature",
           "meaning": {"en": "Moon", "de": "Mond", "fr": "Lune", "tr": "Ay", "ru": "Луна", "sv": "Måne", "nl": "Maan", "el": "Φεγγάρι"}},
    "n3": {"word": "نَجْمَة", "transliteration": "Najma", "emoji": "⭐", "cat": "nature",
           "meaning": {"en": "Star", "de": "Stern", "fr": "Étoile", "tr": "Yıldız", "ru": "Звезда", "sv": "Stjärna", "nl": "Ster", "el": "Αστέρι"}},
    "n4": {"word": "سَمَاء", "transliteration": "Samaa'", "emoji": "🌤️", "cat": "nature",
           "meaning": {"en": "Sky", "de": "Himmel", "fr": "Ciel", "tr": "Gökyüzü", "ru": "Небо", "sv": "Himmel", "nl": "Lucht", "el": "Ουρανός"}},
    "n5": {"word": "مَطَر", "transliteration": "Matar", "emoji": "🌧️", "cat": "nature",
           "meaning": {"en": "Rain", "de": "Regen", "fr": "Pluie", "tr": "Yağmur", "ru": "Дождь", "sv": "Regn", "nl": "Regen", "el": "Βροχή"}},
    "n6": {"word": "بَحْر", "transliteration": "Bahr", "emoji": "🌊", "cat": "nature",
           "meaning": {"en": "Sea", "de": "Meer", "fr": "Mer", "tr": "Deniz", "ru": "Море", "sv": "Hav", "nl": "Zee", "el": "Θάλασσα"}},
    "n7": {"word": "جَبَل", "transliteration": "Jabal", "emoji": "⛰️", "cat": "nature",
           "meaning": {"en": "Mountain", "de": "Berg", "fr": "Montagne", "tr": "Dağ", "ru": "Гора", "sv": "Berg", "nl": "Berg", "el": "Βουνό"}},
    "n8": {"word": "شَجَرَة", "transliteration": "Shajara", "emoji": "🌳", "cat": "nature",
           "meaning": {"en": "Tree", "de": "Baum", "fr": "Arbre", "tr": "Ağaç", "ru": "Дерево", "sv": "Träd", "nl": "Boom", "el": "Δέντρο"}},
    "n9": {"word": "زَهْرَة", "transliteration": "Zahra", "emoji": "🌸", "cat": "nature",
           "meaning": {"en": "Flower", "de": "Blume", "fr": "Fleur", "tr": "Çiçek", "ru": "Цветок", "sv": "Blomma", "nl": "Bloem", "el": "Λουλούδι"}},
    "n10": {"word": "أَرْض", "transliteration": "Ard", "emoji": "🌍", "cat": "nature",
            "meaning": {"en": "Earth", "de": "Erde", "fr": "Terre", "tr": "Toprak", "ru": "Земля", "sv": "Jord", "nl": "Aarde", "el": "Γη"}},
    # ── Colors ──
    "c1": {"word": "أَحْمَر", "transliteration": "Ahmar", "emoji": "🔴", "cat": "colors",
           "meaning": {"en": "Red", "de": "Rot", "fr": "Rouge", "tr": "Kırmızı", "ru": "Красный", "sv": "Röd", "nl": "Rood", "el": "Κόκκινο"}},
    "c2": {"word": "أَزْرَق", "transliteration": "Azraq", "emoji": "🔵", "cat": "colors",
           "meaning": {"en": "Blue", "de": "Blau", "fr": "Bleu", "tr": "Mavi", "ru": "Синий", "sv": "Blå", "nl": "Blauw", "el": "Μπλε"}},
    "c3": {"word": "أَخْضَر", "transliteration": "Akhdar", "emoji": "🟢", "cat": "colors",
           "meaning": {"en": "Green", "de": "Grün", "fr": "Vert", "tr": "Yeşil", "ru": "Зелёный", "sv": "Grön", "nl": "Groen", "el": "Πράσινο"}},
    "c4": {"word": "أَصْفَر", "transliteration": "Asfar", "emoji": "🟡", "cat": "colors",
           "meaning": {"en": "Yellow", "de": "Gelb", "fr": "Jaune", "tr": "Sarı", "ru": "Жёлтый", "sv": "Gul", "nl": "Geel", "el": "Κίτρινο"}},
    "c5": {"word": "أَبْيَض", "transliteration": "Abyad", "emoji": "⚪", "cat": "colors",
           "meaning": {"en": "White", "de": "Weiß", "fr": "Blanc", "tr": "Beyaz", "ru": "Белый", "sv": "Vit", "nl": "Wit", "el": "Λευκό"}},
    "c6": {"word": "أَسْوَد", "transliteration": "Aswad", "emoji": "⚫", "cat": "colors",
           "meaning": {"en": "Black", "de": "Schwarz", "fr": "Noir", "tr": "Siyah", "ru": "Чёрный", "sv": "Svart", "nl": "Zwart", "el": "Μαύρο"}},
    "c7": {"word": "بُرْتُقَالِي", "transliteration": "Burtuqali", "emoji": "🟠", "cat": "colors",
           "meaning": {"en": "Orange", "de": "Orange", "fr": "Orange", "tr": "Turuncu", "ru": "Оранжевый", "sv": "Orange", "nl": "Oranje", "el": "Πορτοκαλί"}},
    "c8": {"word": "بَنَفْسَجِي", "transliteration": "Banafsaji", "emoji": "🟣", "cat": "colors",
           "meaning": {"en": "Purple", "de": "Lila", "fr": "Violet", "tr": "Mor", "ru": "Фиолетовый", "sv": "Lila", "nl": "Paars", "el": "Μωβ"}},
    # ── Home ──
    "h1": {"word": "بَيْت", "transliteration": "Bayt", "emoji": "🏠", "cat": "home",
           "meaning": {"en": "House", "de": "Haus", "fr": "Maison", "tr": "Ev", "ru": "Дом", "sv": "Hus", "nl": "Huis", "el": "Σπίτι"}},
    "h2": {"word": "بَاب", "transliteration": "Bab", "emoji": "🚪", "cat": "home",
           "meaning": {"en": "Door", "de": "Tür", "fr": "Porte", "tr": "Kapı", "ru": "Дверь", "sv": "Dörr", "nl": "Deur", "el": "Πόρτα"}},
    "h3": {"word": "كُرْسِي", "transliteration": "Kursi", "emoji": "🪑", "cat": "home",
           "meaning": {"en": "Chair", "de": "Stuhl", "fr": "Chaise", "tr": "Sandalye", "ru": "Стул", "sv": "Stol", "nl": "Stoel", "el": "Καρέκλα"}},
    "h4": {"word": "طَاوِلَة", "transliteration": "Tawila", "emoji": "🪵", "cat": "home",
           "meaning": {"en": "Table", "de": "Tisch", "fr": "Table", "tr": "Masa", "ru": "Стол", "sv": "Bord", "nl": "Tafel", "el": "Τραπέζι"}},
    "h5": {"word": "سَرِير", "transliteration": "Sareer", "emoji": "🛏️", "cat": "home",
           "meaning": {"en": "Bed", "de": "Bett", "fr": "Lit", "tr": "Yatak", "ru": "Кровать", "sv": "Säng", "nl": "Bed", "el": "Κρεβάτι"}},
    "h6": {"word": "نَافِذَة", "transliteration": "Nafidha", "emoji": "🪟", "cat": "home",
           "meaning": {"en": "Window", "de": "Fenster", "fr": "Fenêtre", "tr": "Pencere", "ru": "Окно", "sv": "Fönster", "nl": "Raam", "el": "Παράθυρο"}},
    "h7": {"word": "مَسْجِد", "transliteration": "Masjid", "emoji": "🕌", "cat": "home",
           "meaning": {"en": "Mosque", "de": "Moschee", "fr": "Mosquée", "tr": "Cami", "ru": "Мечеть", "sv": "Moské", "nl": "Moskee", "el": "Τζαμί"}},
    "h8": {"word": "كِتَاب", "transliteration": "Kitab", "emoji": "📖", "cat": "home",
           "meaning": {"en": "Book", "de": "Buch", "fr": "Livre", "tr": "Kitap", "ru": "Книга", "sv": "Bok", "nl": "Boek", "el": "Βιβλίο"}},
    # ── Verbs ──
    "v1": {"word": "كَتَبَ", "transliteration": "Kataba", "emoji": "✍️", "cat": "verbs",
           "meaning": {"en": "Wrote", "de": "Schrieb", "fr": "A écrit", "tr": "Yazdı", "ru": "Написал", "sv": "Skrev", "nl": "Schreef", "el": "Έγραψε"}},
    "v2": {"word": "قَرَأَ", "transliteration": "Qara'a", "emoji": "📖", "cat": "verbs",
           "meaning": {"en": "Read", "de": "Las", "fr": "A lu", "tr": "Okudu", "ru": "Читал", "sv": "Läste", "nl": "Las", "el": "Διάβασε"}},
    "v3": {"word": "أَكَلَ", "transliteration": "Akala", "emoji": "🍽️", "cat": "verbs",
           "meaning": {"en": "Ate", "de": "Aß", "fr": "A mangé", "tr": "Yedi", "ru": "Ел", "sv": "Åt", "nl": "At", "el": "Έφαγε"}},
    "v4": {"word": "شَرِبَ", "transliteration": "Shariba", "emoji": "🥤", "cat": "verbs",
           "meaning": {"en": "Drank", "de": "Trank", "fr": "A bu", "tr": "İçti", "ru": "Пил", "sv": "Drack", "nl": "Dronk", "el": "Ήπιε"}},
    "v5": {"word": "ذَهَبَ", "transliteration": "Dhahaba", "emoji": "🚶", "cat": "verbs",
           "meaning": {"en": "Went", "de": "Ging", "fr": "Est allé", "tr": "Gitti", "ru": "Пошёл", "sv": "Gick", "nl": "Ging", "el": "Πήγε"}},
    "v6": {"word": "جَلَسَ", "transliteration": "Jalasa", "emoji": "🪑", "cat": "verbs",
           "meaning": {"en": "Sat", "de": "Saß", "fr": "S'est assis", "tr": "Oturdu", "ru": "Сел", "sv": "Satt", "nl": "Zat", "el": "Κάθισε"}},
    "v7": {"word": "نَامَ", "transliteration": "Nama", "emoji": "😴", "cat": "verbs",
           "meaning": {"en": "Slept", "de": "Schlief", "fr": "A dormi", "tr": "Uyudu", "ru": "Спал", "sv": "Sov", "nl": "Sliep", "el": "Κοιμήθηκε"}},
    "v8": {"word": "لَعِبَ", "transliteration": "La'iba", "emoji": "⚽", "cat": "verbs",
           "meaning": {"en": "Played", "de": "Spielte", "fr": "A joué", "tr": "Oynadı", "ru": "Играл", "sv": "Spelade", "nl": "Speelde", "el": "Έπαιξε"}},
    # ── Greetings ──
    "g1": {"word": "السَّلَامُ عَلَيْكُم", "transliteration": "As-Salamu Alaykum", "emoji": "🤝", "cat": "greetings",
           "meaning": {"en": "Peace be upon you", "de": "Friede sei mit euch", "fr": "Paix sur vous", "tr": "Selamün aleyküm", "ru": "Мир вам", "sv": "Frid vare med er", "nl": "Vrede zij met u", "el": "Ειρήνη σε εσάς"}},
    "g2": {"word": "صَبَاحُ الْخَيْر", "transliteration": "Sabah Al-Khayr", "emoji": "🌅", "cat": "greetings",
           "meaning": {"en": "Good morning", "de": "Guten Morgen", "fr": "Bonjour", "tr": "Günaydın", "ru": "Доброе утро", "sv": "God morgon", "nl": "Goedemorgen", "el": "Καλημέρα"}},
    "g3": {"word": "مَسَاءُ الْخَيْر", "transliteration": "Masa' Al-Khayr", "emoji": "🌆", "cat": "greetings",
           "meaning": {"en": "Good evening", "de": "Guten Abend", "fr": "Bonsoir", "tr": "İyi akşamlar", "ru": "Добрый вечер", "sv": "God kväll", "nl": "Goedenavond", "el": "Καλησπέρα"}},
    "g4": {"word": "شُكْرًا", "transliteration": "Shukran", "emoji": "🙏", "cat": "greetings",
           "meaning": {"en": "Thank you", "de": "Danke", "fr": "Merci", "tr": "Teşekkürler", "ru": "Спасибо", "sv": "Tack", "nl": "Dank u", "el": "Ευχαριστώ"}},
    "g5": {"word": "مَعَ السَّلَامَة", "transliteration": "Ma'a As-Salama", "emoji": "👋", "cat": "greetings",
           "meaning": {"en": "Goodbye", "de": "Auf Wiedersehen", "fr": "Au revoir", "tr": "Güle güle", "ru": "До свидания", "sv": "Hej då", "nl": "Tot ziens", "el": "Αντίο"}},
    "g6": {"word": "مِنْ فَضْلِك", "transliteration": "Min Fadlik", "emoji": "😊", "cat": "greetings",
           "meaning": {"en": "Please", "de": "Bitte", "fr": "S'il vous plaît", "tr": "Lütfen", "ru": "Пожалуйста", "sv": "Snälla", "nl": "Alstublieft", "el": "Παρακαλώ"}},
}

# ═══════════════════════════════════════════════════════════════
# SENTENCES — Translated to all 9 languages
# ═══════════════════════════════════════════════════════════════
SENTENCE_TRANSLATIONS = [
    {"id": "s1", "words_ar": ["أَنَا", "أُحِبُّ", "التُّفَّاح"], "sentence_ar": "أَنَا أُحِبُّ التُّفَّاح", "difficulty": 1,
     "translation": {"en": "I love apples", "de": "Ich liebe Äpfel", "fr": "J'aime les pommes", "tr": "Elmaları severim", "ru": "Я люблю яблоки", "sv": "Jag älskar äpplen", "nl": "Ik hou van appels", "el": "Αγαπώ τα μήλα"}},
    {"id": "s2", "words_ar": ["هَذَا", "كِتَاب", "جَمِيل"], "sentence_ar": "هَذَا كِتَاب جَمِيل", "difficulty": 1,
     "translation": {"en": "This is a beautiful book", "de": "Das ist ein schönes Buch", "fr": "C'est un beau livre", "tr": "Bu güzel bir kitap", "ru": "Это красивая книга", "sv": "Det här är en vacker bok", "nl": "Dit is een mooi boek", "el": "Αυτό είναι ένα όμορφο βιβλίο"}},
    {"id": "s3", "words_ar": ["الْوَلَد", "يَلْعَبُ", "فِي الْحَدِيقَة"], "sentence_ar": "الْوَلَد يَلْعَبُ فِي الْحَدِيقَة", "difficulty": 2,
     "translation": {"en": "The boy plays in the park", "de": "Der Junge spielt im Park", "fr": "Le garçon joue dans le parc", "tr": "Çocuk parkta oynuyor", "ru": "Мальчик играет в парке", "sv": "Pojken leker i parken", "nl": "De jongen speelt in het park", "el": "Το αγόρι παίζει στο πάρκο"}},
    {"id": "s4", "words_ar": ["ذَهَبْتُ", "إِلَى", "الْمَسْجِد"], "sentence_ar": "ذَهَبْتُ إِلَى الْمَسْجِد", "difficulty": 1,
     "translation": {"en": "I went to the mosque", "de": "Ich ging zur Moschee", "fr": "Je suis allé à la mosquée", "tr": "Camiye gittim", "ru": "Я пошёл в мечеть", "sv": "Jag gick till moskén", "nl": "Ik ging naar de moskee", "el": "Πήγα στο τζαμί"}},
    {"id": "s5", "words_ar": ["الشَّمْسُ", "سَاطِعَة", "الْيَوْم"], "sentence_ar": "الشَّمْسُ سَاطِعَة الْيَوْم", "difficulty": 2,
     "translation": {"en": "The sun is bright today", "de": "Die Sonne scheint heute", "fr": "Le soleil brille aujourd'hui", "tr": "Bugün güneş parlak", "ru": "Сегодня солнце яркое", "sv": "Solen skiner idag", "nl": "De zon schijnt vandaag", "el": "Ο ήλιος λάμπει σήμερα"}},
    {"id": "s6", "words_ar": ["أُمِّي", "تَطْبَخُ", "طَعَامًا", "لَذِيذًا"], "sentence_ar": "أُمِّي تَطْبَخُ طَعَامًا لَذِيذًا", "difficulty": 2,
     "translation": {"en": "My mother cooks delicious food", "de": "Meine Mutter kocht leckeres Essen", "fr": "Ma mère cuisine de délicieux repas", "tr": "Annem lezzetli yemek pişiriyor", "ru": "Мама готовит вкусную еду", "sv": "Min mamma lagar god mat", "nl": "Mijn moeder kookt heerlijk eten", "el": "Η μητέρα μου μαγειρεύει νόστιμο φαγητό"}},
    {"id": "s7", "words_ar": ["الْقَمَر", "جَمِيل", "فِي اللَّيْل"], "sentence_ar": "الْقَمَر جَمِيل فِي اللَّيْل", "difficulty": 2,
     "translation": {"en": "The moon is beautiful at night", "de": "Der Mond ist schön in der Nacht", "fr": "La lune est belle la nuit", "tr": "Gece ay güzeldir", "ru": "Луна красива ночью", "sv": "Månen är vacker på natten", "nl": "De maan is mooi 's nachts", "el": "Το φεγγάρι είναι όμορφο τη νύχτα"}},
    {"id": "s8", "words_ar": ["بِسْمِ اللَّه", "الرَّحْمَن", "الرَّحِيم"], "sentence_ar": "بِسْمِ اللَّه الرَّحْمَن الرَّحِيم", "difficulty": 1,
     "translation": {"en": "In the name of Allah, the Most Gracious, the Most Merciful", "de": "Im Namen Allahs, des Allerbarmers, des Barmherzigen", "fr": "Au nom d'Allah, le Tout Miséricordieux, le Très Miséricordieux", "tr": "Rahman ve Rahim olan Allah'ın adıyla", "ru": "Во имя Аллаха, Милостивого, Милосердного", "sv": "I Allahs, den Nåderikes, den Barmhärtiges namn", "nl": "In de naam van Allah, de Erbarmer, de Barmhartige", "el": "Στο όνομα του Αλλάχ, του Ελεήμονα, του Οικτίρμονα"}},
    {"id": "s9", "words_ar": ["قَرَأَ", "الطِّفْل", "الْقُرْآن"], "sentence_ar": "قَرَأَ الطِّفْل الْقُرْآن", "difficulty": 2,
     "translation": {"en": "The child read the Quran", "de": "Das Kind las den Koran", "fr": "L'enfant a lu le Coran", "tr": "Çocuk Kuran okudu", "ru": "Ребёнок читал Коран", "sv": "Barnet läste Koranen", "nl": "Het kind las de Koran", "el": "Το παιδί διάβασε το Κοράνι"}},
    {"id": "s10", "words_ar": ["الْمَاء", "ضَرُورِيّ", "لِلْحَيَاة"], "sentence_ar": "الْمَاء ضَرُورِيّ لِلْحَيَاة", "difficulty": 3,
     "translation": {"en": "Water is essential for life", "de": "Wasser ist lebenswichtig", "fr": "L'eau est essentielle à la vie", "tr": "Su hayat için gereklidir", "ru": "Вода необходима для жизни", "sv": "Vatten är nödvändigt för livet", "nl": "Water is essentieel voor het leven", "el": "Το νερό είναι απαραίτητο για τη ζωή"}},
]


# ═══════════════════════════════════════════════════════════════
# HELPER: Resolve locale (de-AT → de, etc.)
# ═══════════════════════════════════════════════════════════════
SUPPORTED_LOCALES = ["ar", "en", "de", "fr", "tr", "ru", "sv", "nl", "el"]

def resolve_locale(locale: str) -> str:
    """Normalize locale code: de-AT→de, etc. Falls back to 'en'."""
    base = locale.split("-")[0].lower().strip()
    return base if base in SUPPORTED_LOCALES else "en"


def localize_letter(letter: dict, locale: str) -> dict:
    """Return a letter dict with only the requested language's translations."""
    lang = resolve_locale(locale)
    lt = LETTER_TRANSLATIONS.get(letter["id"], {})
    result = {
        "id": letter["id"],
        "letter": letter["letter"],
        "name_ar": letter["name_ar"],
        "name": lt.get("name", {}).get(lang, letter.get("name_en", "")),
        "transliteration": letter["transliteration"],
        "form_isolated": letter["form_isolated"],
        "form_initial": letter["form_initial"],
        "form_medial": letter["form_medial"],
        "form_final": letter["form_final"],
        "example_word": letter["example_word"],
        "example_meaning": lt.get("example_meaning", {}).get(lang, letter.get("example_meaning", "")),
        "audio_hint": letter["audio_hint"],
    }
    return result


def localize_vocab(vocab_id: str, locale: str) -> dict:
    """Return a vocabulary word with only the requested language's meaning."""
    lang = resolve_locale(locale)
    v = VOCAB_TRANSLATIONS.get(vocab_id, {})
    return {
        "id": vocab_id,
        "word": v.get("word", ""),
        "transliteration": v.get("transliteration", ""),
        "meaning": v.get("meaning", {}).get(lang, ""),
        "emoji": v.get("emoji", ""),
        "category": v.get("cat", ""),
    }


def localize_number(num_entry: dict, idx: int, locale: str) -> dict:
    """Return a number entry with only the requested language."""
    lang = resolve_locale(locale)
    trans = NUMBER_TRANSLATIONS.get(idx, {})
    return {
        "id": num_entry.get("id", idx),
        "number": num_entry.get("number", idx),
        "arabic": num_entry.get("arabic", ""),
        "word_ar": num_entry.get("word_ar", ""),
        "word": trans.get(lang, num_entry.get("word_en", "")),
        "transliteration": num_entry.get("transliteration", ""),
    }


def localize_sentence(sent: dict, locale: str) -> dict:
    """Return a sentence with only the requested language."""
    lang = resolve_locale(locale)
    return {
        "id": sent["id"],
        "words_ar": sent["words_ar"],
        "sentence_ar": sent["sentence_ar"],
        "translation": sent.get("translation", {}).get(lang, ""),
        "difficulty": sent["difficulty"],
    }

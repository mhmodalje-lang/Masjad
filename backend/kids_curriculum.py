"""
World-Class Arabic & Islamic Curriculum Engine
===============================================
1000+ structured daily lessons from absolute zero to fluency
Designed for non-Arabic speaking children worldwide
Supports 9 languages for instructions
Progressive pedagogy: Letters → Words → Sentences → Reading → Quran → Islam
"""
import random
from typing import Optional
from localization_engine import t, get_cat_name

# ═══════════════════════════════════════════════════════════════
# CURRICULUM STRUCTURE - 15 STAGES, 1000+ LESSONS
# ═══════════════════════════════════════════════════════════════

CURRICULUM_STAGES = [
    {"id": "S01", "days": [1, 56], "emoji": "🔤", "color": "#3B82F6",
     "title": {"ar": "الحروف العربية", "en": "Arabic Alphabet", "de": "Arabisches Alphabet", "fr": "Alphabet arabe", "tr": "Arap Alfabesi", "ru": "Арабский алфавит", "sv": "Arabiskt alfabet", "nl": "Arabisch alfabet", "el": "Αραβικό αλφάβητο"},
     "desc": {"ar": "تعلم الحروف العربية الـ 28 وأشكالها وأصواتها", "en": "Learn all 28 Arabic letters, their forms and sounds", "de": "Lerne alle 28 arabischen Buchstaben", "fr": "Apprenez les 28 lettres arabes", "tr": "28 Arap harfini öğrenin", "ru": "Изучите все 28 арабских букв"}},
    {"id": "S02", "days": [57, 84], "emoji": "🎵", "color": "#8B5CF6",
     "title": {"ar": "الحركات والتشكيل", "en": "Vowels & Diacritics", "de": "Vokale & Diakritika", "fr": "Voyelles & Diacritiques", "tr": "Sesli Harfler", "ru": "Гласные и диакритика"},
     "desc": {"ar": "الفتحة والكسرة والضمة والسكون والشدة والتنوين", "en": "Fatha, Kasra, Damma, Sukun, Shadda & Tanween", "de": "Fatha, Kasra, Damma, Sukun, Shadda & Tanween", "fr": "Fatha, Kasra, Damma, Sukun, Shadda & Tanween", "tr": "Fatha, Kasra, Damma, Sukun, Şedde, Tenvin", "ru": "Фатха, Касра, Дамма, Сукун, Шадда и Танвин"}},
    {"id": "S03", "days": [85, 112], "emoji": "🔢", "color": "#06B6D4",
     "title": {"ar": "الأرقام العربية", "en": "Arabic Numbers", "de": "Arabische Zahlen", "fr": "Chiffres arabes", "tr": "Arapça Sayılar", "ru": "Арабские цифры"},
     "desc": {"ar": "تعلم الأرقام من ٠ إلى ١٠٠ والعدّ", "en": "Learn numbers from 0 to 100 and counting", "de": "Lerne Zahlen von 0 bis 100", "fr": "Apprenez les chiffres de 0 à 100", "tr": "0'dan 100'e sayıları öğrenin", "ru": "Изучите числа от 0 до 100"}},
    {"id": "S04", "days": [113, 210], "emoji": "📝", "color": "#F59E0B",
     "title": {"ar": "الكلمات الأولى", "en": "First Words", "de": "Erste Wörter", "fr": "Premiers mots", "tr": "İlk Kelimeler", "ru": "Первые слова"},
     "desc": {"ar": "ألوان، حيوانات، عائلة، جسم، طعام، بيت، طبيعة", "en": "Colors, Animals, Family, Body, Food, Home, Nature", "de": "Farben, Tiere, Familie, Körper, Essen, Haus, Natur", "fr": "Couleurs, Animaux, Famille, Corps, Nourriture, Maison, Nature", "tr": "Renkler, Hayvanlar, Aile, Vücut, Yiyecek, Ev, Doğa", "ru": "Цвета, Животные, Семья, Тело, Еда, Дом, Природа"}},
    {"id": "S05", "days": [211, 266], "emoji": "💬", "color": "#10B981",
     "title": {"ar": "الجمل البسيطة", "en": "Simple Sentences", "de": "Einfache Sätze", "fr": "Phrases simples", "tr": "Basit Cümleler", "ru": "Простые предложения"},
     "desc": {"ar": "التحيات، التعريف بالنفس، الأسئلة الأساسية", "en": "Greetings, introductions, basic questions", "de": "Grüße, Vorstellungen, einfache Fragen", "fr": "Salutations, présentations, questions de base", "tr": "Selamlaşma, tanışma, temel sorular", "ru": "Приветствия, представление, основные вопросы"}},
    {"id": "S06", "days": [267, 308], "emoji": "📖", "color": "#EF4444",
     "title": {"ar": "تمرين القراءة", "en": "Reading Practice", "de": "Leseübung", "fr": "Exercice de lecture", "tr": "Okuma Alıştırması", "ru": "Практика чтения"},
     "desc": {"ar": "قراءة كلمات وجمل وفقرات قصيرة", "en": "Reading words, sentences and short paragraphs", "de": "Wörter, Sätze und kurze Absätze lesen", "fr": "Lire des mots, phrases et courts paragraphes", "tr": "Kelime, cümle ve kısa paragraf okuma", "ru": "Чтение слов, предложений и коротких абзацев"}},
    {"id": "S07", "days": [309, 378], "emoji": "🤲", "color": "#059669",
     "title": {"ar": "أساسيات الإسلام", "en": "Islamic Foundations", "de": "Islamische Grundlagen", "fr": "Fondements de l'Islam", "tr": "İslam Temelleri", "ru": "Основы Ислама"},
     "desc": {"ar": "أركان الإسلام، الإيمان، الوضوء، الصلاة، رمضان", "en": "Pillars of Islam, Faith, Wudu, Prayer, Ramadan", "de": "Säulen des Islam, Glaube, Wudu, Gebet, Ramadan", "fr": "Piliers de l'Islam, Foi, Wudu, Prière, Ramadan", "tr": "İslam'ın Şartları, İman, Abdest, Namaz, Ramazan", "ru": "Столпы Ислама, Вера, Вуду, Молитва, Рамадан"}},
    {"id": "S08", "days": [379, 490], "emoji": "📖", "color": "#7C3AED",
     "title": {"ar": "حفظ القرآن", "en": "Quran Memorization", "de": "Koran-Memorierung", "fr": "Mémorisation du Coran", "tr": "Kur'an Ezberleme", "ru": "Заучивание Корана"},
     "desc": {"ar": "سور جزء عمّ مع التجويد المبسط", "en": "Juz Amma surahs with basic Tajweed", "de": "Juz Amma Suren mit einfachem Tajweed", "fr": "Sourates Juz Amma avec Tajweed de base", "tr": "Cüz Amma sureleri ve temel Tecvid", "ru": "Суры Джуз Амма с основами Таджвида"}},
    {"id": "S09", "days": [491, 560], "emoji": "🤲", "color": "#0EA5E9",
     "title": {"ar": "الأدعية والأذكار", "en": "Duas & Daily Phrases", "de": "Duas & Tägliche Phrasen", "fr": "Duas & Phrases quotidiennes", "tr": "Dualar & Günlük İfadeler", "ru": "Дуа и ежедневные фразы"},
     "desc": {"ar": "أدعية يومية وعبارات إسلامية أساسية", "en": "Daily duas and essential Islamic phrases", "de": "Tägliche Duas und islamische Ausdrücke", "fr": "Duas quotidiennes et phrases islamiques essentielles", "tr": "Günlük dualar ve İslami ifadeler", "ru": "Ежедневные дуа и исламские фразы"}},
    {"id": "S10", "days": [561, 630], "emoji": "📜", "color": "#D97706",
     "title": {"ar": "الأحاديث والأخلاق", "en": "Hadiths & Morals", "de": "Hadithe & Moral", "fr": "Hadiths & Morale", "tr": "Hadisler & Ahlak", "ru": "Хадисы и нравственность"},
     "desc": {"ar": "أحاديث نبوية مبسطة ودروس أخلاقية", "en": "Simplified Prophet's hadiths and moral lessons", "de": "Vereinfachte Hadithe und moralische Lektionen", "fr": "Hadiths simplifiés et leçons morales", "tr": "Basitleştirilmiş hadisler ve ahlaki dersler", "ru": "Упрощённые хадисы и нравственные уроки"}},
    {"id": "S11", "days": [631, 720], "emoji": "🕌", "color": "#9333EA",
     "title": {"ar": "قصص الأنبياء", "en": "Prophet Stories", "de": "Prophetengeschichten", "fr": "Histoires des Prophètes", "tr": "Peygamber Kıssaları", "ru": "Истории пророков"},
     "desc": {"ar": "قصص الأنبياء الـ 25 المذكورين في القرآن", "en": "Stories of all 25 prophets in the Quran", "de": "Geschichten aller 25 Propheten im Koran", "fr": "Histoires des 25 prophètes du Coran", "tr": "Kur'an'daki 25 peygamberin kıssaları", "ru": "Истории всех 25 пророков Корана"}},
    {"id": "S12", "days": [721, 810], "emoji": "🌙", "color": "#DC2626",
     "title": {"ar": "الحياة الإسلامية", "en": "Islamic Life", "de": "Islamisches Leben", "fr": "Vie islamique", "tr": "İslami Yaşam", "ru": "Исламская жизнь"},
     "desc": {"ar": "رمضان، الحج، الأعياد، التقويم الإسلامي", "en": "Ramadan, Hajj, Eids, Islamic calendar", "de": "Ramadan, Hadsch, Eid-Feste, islamischer Kalender", "fr": "Ramadan, Hajj, Fêtes de l'Aïd, calendrier islamique", "tr": "Ramazan, Hac, Bayramlar, İslami takvim", "ru": "Рамадан, Хадж, праздники, исламский календарь"}},
    {"id": "S13", "days": [811, 900], "emoji": "📚", "color": "#0D9488",
     "title": {"ar": "عربي متقدم", "en": "Advanced Arabic", "de": "Fortgeschrittenes Arabisch", "fr": "Arabe avancé", "tr": "İleri Arapça", "ru": "Продвинутый арабский"},
     "desc": {"ar": "قواعد أساسية، أفعال، محادثات", "en": "Basic grammar, verbs, conversations", "de": "Grundgrammatik, Verben, Gespräche", "fr": "Grammaire de base, verbes, conversations", "tr": "Temel gramer, fiiller, konuşmalar", "ru": "Базовая грамматика, глаголы, разговоры"}},
    {"id": "S14", "days": [901, 960], "emoji": "🏆", "color": "#B45309",
     "title": {"ar": "قرآن متقدم", "en": "Advanced Quran", "de": "Fortgeschrittener Koran", "fr": "Coran avancé", "tr": "İleri Kur'an", "ru": "Продвинутый Коран"},
     "desc": {"ar": "سور أطول، تفسير مبسط، تجويد متقدم", "en": "Longer surahs, simple Tafsir, advanced Tajweed", "de": "Längere Suren, einfacher Tafsir, fortgeschrittenes Tajweed", "fr": "Sourates plus longues, Tafsir simple, Tajweed avancé", "tr": "Uzun sureler, basit Tefsir, ileri Tecvid", "ru": "Длинные суры, простой Тафсир, продвинутый Таджвид"}},
    {"id": "S15", "days": [961, 1000], "emoji": "🎓", "color": "#4F46E5",
     "title": {"ar": "الإتقان والتخرج", "en": "Mastery & Graduation", "de": "Meisterschaft & Abschluss", "fr": "Maîtrise & Diplôme", "tr": "Ustalık & Mezuniyet", "ru": "Мастерство и выпускной"},
     "desc": {"ar": "مراجعة شاملة واختبارات وشهادة إتقان", "en": "Comprehensive review, tests & mastery certificate", "de": "Umfassende Wiederholung, Tests & Meisterschaftszertifikat", "fr": "Révision complète, tests & certificat de maîtrise", "tr": "Kapsamlı tekrar, sınavlar ve ustalık sertifikası", "ru": "Полный обзор, тесты и сертификат мастерства"}},
]

# ═══════════════════════════════════════════════════════════════
# CONTENT DATA POOLS - FULL 9-LANGUAGE SUPPORT
# ═══════════════════════════════════════════════════════════════

# Multi-language word translations for letter examples
# Format: {"ar": ..., "en": ..., "de": ..., "fr": ..., "tr": ..., "ru": ..., "sv": ..., "nl": ..., "el": ...}
WORD_TRANSLATIONS = {
    "Lion":{"de":"Löwe","fr":"Lion","tr":"Aslan","ru":"Лев","sv":"Lejon","nl":"Leeuw","el":"Λιοντάρι"},
    "Duck":{"de":"Ente","fr":"Canard","tr":"Ördek","ru":"Утка","sv":"Anka","nl":"Eend","el":"Πάπια"},
    "Apple":{"de":"Apfel","fr":"Pomme","tr":"Elma","ru":"Яблоко","sv":"Äpple","nl":"Appel","el":"Μήλο"},
    "Fox":{"de":"Fuchs","fr":"Renard","tr":"Tilki","ru":"Лиса","sv":"Räv","nl":"Vos","el":"Αλεπού"},
    "Camel":{"de":"Kamel","fr":"Chameau","tr":"Deve","ru":"Верблюд","sv":"Kamel","nl":"Kameel","el":"Καμήλα"},
    "Horse":{"de":"Pferd","fr":"Cheval","tr":"At","ru":"Лошадь","sv":"Häst","nl":"Paard","el":"Άλογο"},
    "Sheep":{"de":"Schaf","fr":"Mouton","tr":"Koyun","ru":"Овца","sv":"Får","nl":"Schaap","el":"Πρόβατο"},
    "Chicken":{"de":"Huhn","fr":"Poulet","tr":"Tavuk","ru":"Курица","sv":"Kyckling","nl":"Kip","el":"Κοτόπουλο"},
    "Corn":{"de":"Mais","fr":"Maïs","tr":"Mısır","ru":"Кукуруза","sv":"Majs","nl":"Maïs","el":"Καλαμπόκι"},
    "Pomegranate":{"de":"Granatapfel","fr":"Grenade","tr":"Nar","ru":"Гранат","sv":"Granatäpple","nl":"Granaatappel","el":"Ρόδι"},
    "Giraffe":{"de":"Giraffe","fr":"Girafe","tr":"Zürafa","ru":"Жираф","sv":"Giraff","nl":"Giraf","el":"Καμηλοπάρδαλη"},
    "Fish":{"de":"Fisch","fr":"Poisson","tr":"Balık","ru":"Рыба","sv":"Fisk","nl":"Vis","el":"Ψάρι"},
    "Sun":{"de":"Sonne","fr":"Soleil","tr":"Güneş","ru":"Солнце","sv":"Sol","nl":"Zon","el":"Ήλιος"},
    "Falcon":{"de":"Falke","fr":"Faucon","tr":"Şahin","ru":"Сокол","sv":"Falk","nl":"Valk","el":"Γεράκι"},
    "Frog":{"de":"Frosch","fr":"Grenouille","tr":"Kurbağa","ru":"Лягушка","sv":"Groda","nl":"Kikker","el":"Βάτραχος"},
    "Bird":{"de":"Vogel","fr":"Oiseau","tr":"Kuş","ru":"Птица","sv":"Fågel","nl":"Vogel","el":"Πουλί"},
    "Envelope":{"de":"Umschlag","fr":"Enveloppe","tr":"Zarf","ru":"Конверт","sv":"Kuvert","nl":"Envelop","el":"Φάκελος"},
    "Grapes":{"de":"Trauben","fr":"Raisins","tr":"Üzüm","ru":"Виноград","sv":"Druvor","nl":"Druiven","el":"Σταφύλια"},
    "Gazelle":{"de":"Gazelle","fr":"Gazelle","tr":"Ceylan","ru":"Газель","sv":"Gasell","nl":"Gazelle","el":"Γαζέλα"},
    "Butterfly":{"de":"Schmetterling","fr":"Papillon","tr":"Kelebek","ru":"Бабочка","sv":"Fjäril","nl":"Vlinder","el":"Πεταλούδα"},
    "Moon":{"de":"Mond","fr":"Lune","tr":"Ay","ru":"Луна","sv":"Måne","nl":"Maan","el":"Φεγγάρι"},
    "Book":{"de":"Buch","fr":"Livre","tr":"Kitap","ru":"Книга","sv":"Bok","nl":"Boek","el":"Βιβλίο"},
    "Lemon":{"de":"Zitrone","fr":"Citron","tr":"Limon","ru":"Лимон","sv":"Citron","nl":"Citroen","el":"Λεμόνι"},
    "Mosque":{"de":"Moschee","fr":"Mosquée","tr":"Cami","ru":"Мечеть","sv":"Moské","nl":"Moskee","el":"Τζαμί"},
    "Star":{"de":"Stern","fr":"Étoile","tr":"Yıldız","ru":"Звезда","sv":"Stjärna","nl":"Ster","el":"Αστέρι"},
    "Crescent":{"de":"Halbmond","fr":"Croissant","tr":"Hilal","ru":"Полумесяц","sv":"Halvmåne","nl":"Halve maan","el":"Ημισέληνος"},
    "Rose":{"de":"Rose","fr":"Rose","tr":"Gül","ru":"Роза","sv":"Ros","nl":"Roos","el":"Τριαντάφυλλο"},
    "Hand":{"de":"Hand","fr":"Main","tr":"El","ru":"Рука","sv":"Hand","nl":"Hand","el":"Χέρι"},
    # HARAKAT meanings
    "door":{"de":"Tür","fr":"porte","tr":"kapı","ru":"дверь","sv":"dörr","nl":"deur","el":"πόρτα"},
    "girl":{"de":"Mädchen","fr":"fille","tr":"kız","ru":"девочка","sv":"flicka","nl":"meisje","el":"κορίτσι"},
    "orange":{"de":"Orange","fr":"orange","tr":"portakal","ru":"апельсин","sv":"apelsin","nl":"sinaasappel","el":"πορτοκάλι"},
    "patience":{"de":"Geduld","fr":"patience","tr":"sabır","ru":"терпение","sv":"tålamod","nl":"geduld","el":"υπομονή"},
    "Lord":{"de":"Herr","fr":"Seigneur","tr":"Rab","ru":"Господь","sv":"Herre","nl":"Heer","el":"Κύριος"},
    "a book":{"de":"ein Buch","fr":"un livre","tr":"bir kitap","ru":"книга","sv":"en bok","nl":"een boek","el":"ένα βιβλίο"},
    # Vocab: Colors
    "Red":{"de":"Rot","fr":"Rouge","tr":"Kırmızı","ru":"Красный","sv":"Röd","nl":"Rood","el":"Κόκκινο"},
    "Blue":{"de":"Blau","fr":"Bleu","tr":"Mavi","ru":"Синий","sv":"Blå","nl":"Blauw","el":"Μπλε"},
    "Green":{"de":"Grün","fr":"Vert","tr":"Yeşil","ru":"Зелёный","sv":"Grön","nl":"Groen","el":"Πράσινο"},
    "Yellow":{"de":"Gelb","fr":"Jaune","tr":"Sarı","ru":"Жёлтый","sv":"Gul","nl":"Geel","el":"Κίτρινο"},
    "Orange":{"de":"Orange","fr":"Orange","tr":"Turuncu","ru":"Оранжевый","sv":"Orange","nl":"Oranje","el":"Πορτοκαλί"},
    "Purple":{"de":"Lila","fr":"Violet","tr":"Mor","ru":"Фиолетовый","sv":"Lila","nl":"Paars","el":"Μωβ"},
    "White":{"de":"Weiß","fr":"Blanc","tr":"Beyaz","ru":"Белый","sv":"Vit","nl":"Wit","el":"Λευκό"},
    "Black":{"de":"Schwarz","fr":"Noir","tr":"Siyah","ru":"Чёрный","sv":"Svart","nl":"Zwart","el":"Μαύρο"},
    "Pink":{"de":"Rosa","fr":"Rose","tr":"Pembe","ru":"Розовый","sv":"Rosa","nl":"Roze","el":"Ροζ"},
    "Brown":{"de":"Braun","fr":"Marron","tr":"Kahverengi","ru":"Коричневый","sv":"Brun","nl":"Bruin","el":"Καφέ"},
    # Vocab: Animals
    "Cat":{"de":"Katze","fr":"Chat","tr":"Kedi","ru":"Кошка","sv":"Katt","nl":"Kat","el":"Γάτα"},
    "Dog":{"de":"Hund","fr":"Chien","tr":"Köpek","ru":"Собака","sv":"Hund","nl":"Hond","el":"Σκύλος"},
    "Elephant":{"de":"Elefant","fr":"Éléphant","tr":"Fil","ru":"Слон","sv":"Elefant","nl":"Olifant","el":"Ελέφαντας"},
    "Bee":{"de":"Biene","fr":"Abeille","tr":"Arı","ru":"Пчела","sv":"Bi","nl":"Bij","el":"Μέλισσα"},
    "Ant":{"de":"Ameise","fr":"Fourmi","tr":"Karınca","ru":"Муравей","sv":"Myra","nl":"Mier","el":"Μυρμήγκι"},
    "Rabbit":{"de":"Hase","fr":"Lapin","tr":"Tavşan","ru":"Кролик","sv":"Kanin","nl":"Konijn","el":"Κουνέλι"},
    "Cow":{"de":"Kuh","fr":"Vache","tr":"İnek","ru":"Корова","sv":"Ko","nl":"Koe","el":"Αγελάδα"},
    # Vocab: Family
    "Father":{"de":"Vater","fr":"Père","tr":"Baba","ru":"Отец","sv":"Pappa","nl":"Vader","el":"Πατέρας"},
    "Mother":{"de":"Mutter","fr":"Mère","tr":"Anne","ru":"Мать","sv":"Mamma","nl":"Moeder","el":"Μητέρα"},
    "Brother":{"de":"Bruder","fr":"Frère","tr":"Erkek kardeş","ru":"Брат","sv":"Bror","nl":"Broer","el":"Αδελφός"},
    "Sister":{"de":"Schwester","fr":"Sœur","tr":"Kız kardeş","ru":"Сестра","sv":"Syster","nl":"Zus","el":"Αδελφή"},
    "Grandfather":{"de":"Großvater","fr":"Grand-père","tr":"Büyükbaba","ru":"Дедушка","sv":"Farfar","nl":"Opa","el":"Παππούς"},
    "Grandmother":{"de":"Großmutter","fr":"Grand-mère","tr":"Büyükanne","ru":"Бабушка","sv":"Farmor","nl":"Oma","el":"Γιαγιά"},
    "Uncle":{"de":"Onkel","fr":"Oncle","tr":"Amca","ru":"Дядя","sv":"Farbror","nl":"Oom","el":"Θείος"},
    "Aunt":{"de":"Tante","fr":"Tante","tr":"Teyze","ru":"Тётя","sv":"Faster","nl":"Tante","el":"Θεία"},
    "Son":{"de":"Sohn","fr":"Fils","tr":"Oğul","ru":"Сын","sv":"Son","nl":"Zoon","el":"Γιος"},
    "Daughter":{"de":"Tochter","fr":"Fille","tr":"Kız","ru":"Дочь","sv":"Dotter","nl":"Dochter","el":"Κόρη"},
    # Body, Food, Home, Nature, School, Greetings
    "Head":{"de":"Kopf","fr":"Tête","tr":"Baş","ru":"Голова","sv":"Huvud","nl":"Hoofd","el":"Κεφάλι"},
    "Eye":{"de":"Auge","fr":"Œil","tr":"Göz","ru":"Глаз","sv":"Öga","nl":"Oog","el":"Μάτι"},
    "Nose":{"de":"Nase","fr":"Nez","tr":"Burun","ru":"Нос","sv":"Näsa","nl":"Neus","el":"Μύτη"},
    "Mouth":{"de":"Mund","fr":"Bouche","tr":"Ağız","ru":"Рот","sv":"Mun","nl":"Mond","el":"Στόμα"},
    "Ear":{"de":"Ohr","fr":"Oreille","tr":"Kulak","ru":"Ухо","sv":"Öra","nl":"Oor","el":"Αυτί"},
    "Foot":{"de":"Fuß","fr":"Pied","tr":"Ayak","ru":"Нога","sv":"Fot","nl":"Voet","el":"Πόδι"},
    "Heart":{"de":"Herz","fr":"Cœur","tr":"Kalp","ru":"Сердце","sv":"Hjärta","nl":"Hart","el":"Καρδιά"},
    "Hair":{"de":"Haar","fr":"Cheveux","tr":"Saç","ru":"Волосы","sv":"Hår","nl":"Haar","el":"Μαλλιά"},
    "Finger":{"de":"Finger","fr":"Doigt","tr":"Parmak","ru":"Палец","sv":"Finger","nl":"Vinger","el":"Δάχτυλο"},
    "Banana":{"de":"Banane","fr":"Banane","tr":"Muz","ru":"Банан","sv":"Banan","nl":"Banaan","el":"Μπανάνα"},
    "Bread":{"de":"Brot","fr":"Pain","tr":"Ekmek","ru":"Хлеб","sv":"Bröd","nl":"Brood","el":"Ψωμί"},
    "Milk":{"de":"Milch","fr":"Lait","tr":"Süt","ru":"Молоко","sv":"Mjölk","nl":"Melk","el":"Γάλα"},
    "Water":{"de":"Wasser","fr":"Eau","tr":"Su","ru":"Вода","sv":"Vatten","nl":"Water","el":"Νερό"},
    "Rice":{"de":"Reis","fr":"Riz","tr":"Pirinç","ru":"Рис","sv":"Ris","nl":"Rijst","el":"Ρύζι"},
    "Egg":{"de":"Ei","fr":"Œuf","tr":"Yumurta","ru":"Яйцо","sv":"Ägg","nl":"Ei","el":"Αυγό"},
    "Date":{"de":"Dattel","fr":"Datte","tr":"Hurma","ru":"Финик","sv":"Dadel","nl":"Dadel","el":"Χουρμάς"},
    "Honey":{"de":"Honig","fr":"Miel","tr":"Bal","ru":"Мёд","sv":"Honung","nl":"Honing","el":"Μέλι"},
    "House":{"de":"Haus","fr":"Maison","tr":"Ev","ru":"Дом","sv":"Hus","nl":"Huis","el":"Σπίτι"},
    "Door":{"de":"Tür","fr":"Porte","tr":"Kapı","ru":"Дверь","sv":"Dörr","nl":"Deur","el":"Πόρτα"},
    "Window":{"de":"Fenster","fr":"Fenêtre","tr":"Pencere","ru":"Окно","sv":"Fönster","nl":"Raam","el":"Παράθυρο"},
    "Chair":{"de":"Stuhl","fr":"Chaise","tr":"Sandalye","ru":"Стул","sv":"Stol","nl":"Stoel","el":"Καρέκλα"},
    "Table":{"de":"Tisch","fr":"Table","tr":"Masa","ru":"Стол","sv":"Bord","nl":"Tafel","el":"Τραπέζι"},
    "Bed":{"de":"Bett","fr":"Lit","tr":"Yatak","ru":"Кровать","sv":"Säng","nl":"Bed","el":"Κρεβάτι"},
    "Kitchen":{"de":"Küche","fr":"Cuisine","tr":"Mutfak","ru":"Кухня","sv":"Kök","nl":"Keuken","el":"Κουζίνα"},
    "Bathroom":{"de":"Badezimmer","fr":"Salle de bain","tr":"Banyo","ru":"Ванная","sv":"Badrum","nl":"Badkamer","el":"Μπάνιο"},
    "Room":{"de":"Zimmer","fr":"Chambre","tr":"Oda","ru":"Комната","sv":"Rum","nl":"Kamer","el":"Δωμάτιο"},
    "Garden":{"de":"Garten","fr":"Jardin","tr":"Bahçe","ru":"Сад","sv":"Trädgård","nl":"Tuin","el":"Κήπος"},
    "Tree":{"de":"Baum","fr":"Arbre","tr":"Ağaç","ru":"Дерево","sv":"Träd","nl":"Boom","el":"Δέντρο"},
    "Flower":{"de":"Blume","fr":"Fleur","tr":"Çiçek","ru":"Цветок","sv":"Blomma","nl":"Bloem","el":"Λουλούδι"},
    "Sea":{"de":"Meer","fr":"Mer","tr":"Deniz","ru":"Море","sv":"Hav","nl":"Zee","el":"Θάλασσα"},
    "Mountain":{"de":"Berg","fr":"Montagne","tr":"Dağ","ru":"Гора","sv":"Berg","nl":"Berg","el":"Βουνό"},
    "River":{"de":"Fluss","fr":"Rivière","tr":"Nehir","ru":"Река","sv":"Flod","nl":"Rivier","el":"Ποτάμι"},
    "Sky":{"de":"Himmel","fr":"Ciel","tr":"Gökyüzü","ru":"Небо","sv":"Himmel","nl":"Lucht","el":"Ουρανός"},
    "Rain":{"de":"Regen","fr":"Pluie","tr":"Yağmur","ru":"Дождь","sv":"Regn","nl":"Regen","el":"Βροχή"},
    "School":{"de":"Schule","fr":"École","tr":"Okul","ru":"Школа","sv":"Skola","nl":"School","el":"Σχολείο"},
    "Pen":{"de":"Stift","fr":"Stylo","tr":"Kalem","ru":"Ручка","sv":"Penna","nl":"Pen","el":"Στυλό"},
    "Teacher":{"de":"Lehrer","fr":"Professeur","tr":"Öğretmen","ru":"Учитель","sv":"Lärare","nl":"Leraar","el":"Δάσκαλος"},
    "Student":{"de":"Schüler","fr":"Élève","tr":"Öğrenci","ru":"Ученик","sv":"Elev","nl":"Leerling","el":"Μαθητής"},
    "Class":{"de":"Klasse","fr":"Classe","tr":"Sınıf","ru":"Класс","sv":"Klass","nl":"Klas","el":"Τάξη"},
    "Homework":{"de":"Hausaufgabe","fr":"Devoir","tr":"Ödev","ru":"Домашнее задание","sv":"Läxa","nl":"Huiswerk","el":"Εργασία"},
    "Exam":{"de":"Prüfung","fr":"Examen","tr":"Sınav","ru":"Экзамен","sv":"Prov","nl":"Examen","el":"Εξέταση"},
    "Peace be upon you":{"de":"Friede sei mit dir","fr":"La paix soit sur vous","tr":"Selam olsun","ru":"Мир вам","sv":"Frid vare med dig","nl":"Vrede zij met u","el":"Ειρήνη σε εσένα"},
    "And upon you peace":{"de":"Und Friede mit dir","fr":"Et sur vous la paix","tr":"Ve aleykümselam","ru":"И вам мир","sv":"Och med dig frid","nl":"En met u vrede","el":"Και σε εσένα ειρήνη"},
    "Good morning":{"de":"Guten Morgen","fr":"Bonjour","tr":"Günaydın","ru":"Доброе утро","sv":"God morgon","nl":"Goedemorgen","el":"Καλημέρα"},
    "Good evening":{"de":"Guten Abend","fr":"Bonsoir","tr":"İyi akşamlar","ru":"Добрый вечер","sv":"God kväll","nl":"Goedenavond","el":"Καλησπέρα"},
    "Goodbye":{"de":"Auf Wiedersehen","fr":"Au revoir","tr":"Hoşça kal","ru":"До свидания","sv":"Hejdå","nl":"Tot ziens","el":"Αντίο"},
    "Thank you":{"de":"Danke","fr":"Merci","tr":"Teşekkürler","ru":"Спасибо","sv":"Tack","nl":"Dank u","el":"Ευχαριστώ"},
    "You're welcome":{"de":"Bitte","fr":"De rien","tr":"Rica ederim","ru":"Пожалуйста","sv":"Varsågod","nl":"Graag gedaan","el":"Παρακαλώ"},
    "Please":{"de":"Bitte","fr":"S'il vous plaît","tr":"Lütfen","ru":"Пожалуйста","sv":"Snälla","nl":"Alstublieft","el":"Παρακαλώ"},
    "Yes":{"de":"Ja","fr":"Oui","tr":"Evet","ru":"Да","sv":"Ja","nl":"Ja","el":"Ναι"},
    "No":{"de":"Nein","fr":"Non","tr":"Hayır","ru":"Нет","sv":"Nej","nl":"Nee","el":"Όχι"},
}

def _tw(en_word: str, lang: str) -> str:
    """Translate a word to the target language. Falls back: lang -> ar name -> en."""
    if lang == "en":
        return en_word
    if lang == "ar":
        return en_word  # Will use ar field directly
    entry = WORD_TRANSLATIONS.get(en_word, {})
    return entry.get(lang, entry.get(lang.split("-")[0], en_word))

# "Letter" prefix translations
LETTER_PREFIX = {"ar":"حرف","en":"Letter","de":"Buchstabe","fr":"Lettre","tr":"Harf","ru":"Буква","sv":"Bokstav","nl":"Letter","el":"Γράμμα","de-AT":"Buchstabe"}
FORMS_PREFIX = {"ar":"أشكال","en":"Forms of","de":"Formen von","fr":"Formes de","tr":"Biçimleri:","ru":"Формы","sv":"Former av","nl":"Vormen van","el":"Μορφές","de-AT":"Formen von"}
REVIEW_FORMS = {"ar":"مراجعة الأشكال","en":"Review Letter Forms","de":"Buchstabenformen wiederholen","fr":"Révision des formes","tr":"Harf Formlarını Tekrarla","ru":"Повторение форм букв","sv":"Repetera bokstavsformer","nl":"Lettervorm herhaling","el":"Επανάληψη μορφών","de-AT":"Buchstabenformen wiederholen"}
WRITING_PRACTICE = {"ar":"تمرين كتابة وتوصيل","en":"Writing & Connection Practice","de":"Schreib- & Verbindungsübung","fr":"Exercice d'écriture","tr":"Yazma & Bağlantı Alıştırması","ru":"Практика письма и соединения","sv":"Skriv- & kopplingsövning","nl":"Schrijf- & verbindingsoefening","el":"Εξάσκηση γραφής","de-AT":"Schreib- & Verbindungsübung"}
VOWELS_REVIEW = {"ar":"مراجعة الحركات","en":"Vowels Review","de":"Vokal-Wiederholung","fr":"Révision des voyelles","tr":"Sesli Harf Tekrarı","ru":"Повторение гласных","sv":"Vokal-repetition","nl":"Klinker herhaling","el":"Επανάληψη φωνηέντων","de-AT":"Vokal-Wiederholung"}

LETTERS_28 = [
    {"letter":"أ","name_ar":"ألف","name_en":"Alif","sound":"/a/","word":"أسد","word_en":"Lion","emoji":"🦁","forms":["ـا","ا","أ"]},
    {"letter":"ب","name_ar":"باء","name_en":"Ba","sound":"/b/","word":"بطة","word_en":"Duck","emoji":"🦆","forms":["ـب","ـبـ","بـ"]},
    {"letter":"ت","name_ar":"تاء","name_en":"Ta","sound":"/t/","word":"تفاحة","word_en":"Apple","emoji":"🍎","forms":["ـت","ـتـ","تـ"]},
    {"letter":"ث","name_ar":"ثاء","name_en":"Tha","sound":"/th/","word":"ثعلب","word_en":"Fox","emoji":"🦊","forms":["ـث","ـثـ","ثـ"]},
    {"letter":"ج","name_ar":"جيم","name_en":"Jim","sound":"/j/","word":"جمل","word_en":"Camel","emoji":"🐫","forms":["ـج","ـجـ","جـ"]},
    {"letter":"ح","name_ar":"حاء","name_en":"Ha","sound":"/ḥ/","word":"حصان","word_en":"Horse","emoji":"🐴","forms":["ـح","ـحـ","حـ"]},
    {"letter":"خ","name_ar":"خاء","name_en":"Kha","sound":"/kh/","word":"خروف","word_en":"Sheep","emoji":"🐑","forms":["ـخ","ـخـ","خـ"]},
    {"letter":"د","name_ar":"دال","name_en":"Dal","sound":"/d/","word":"دجاجة","word_en":"Chicken","emoji":"🐔","forms":["ـد","د"]},
    {"letter":"ذ","name_ar":"ذال","name_en":"Dhal","sound":"/dh/","word":"ذرة","word_en":"Corn","emoji":"🌽","forms":["ـذ","ذ"]},
    {"letter":"ر","name_ar":"راء","name_en":"Ra","sound":"/r/","word":"رمان","word_en":"Pomegranate","emoji":"🍎","forms":["ـر","ر"]},
    {"letter":"ز","name_ar":"زاي","name_en":"Zay","sound":"/z/","word":"زرافة","word_en":"Giraffe","emoji":"🦒","forms":["ـز","ز"]},
    {"letter":"س","name_ar":"سين","name_en":"Sin","sound":"/s/","word":"سمكة","word_en":"Fish","emoji":"🐟","forms":["ـس","ـسـ","سـ"]},
    {"letter":"ش","name_ar":"شين","name_en":"Shin","sound":"/sh/","word":"شمس","word_en":"Sun","emoji":"☀️","forms":["ـش","ـشـ","شـ"]},
    {"letter":"ص","name_ar":"صاد","name_en":"Sad","sound":"/ṣ/","word":"صقر","word_en":"Falcon","emoji":"🦅","forms":["ـص","ـصـ","صـ"]},
    {"letter":"ض","name_ar":"ضاد","name_en":"Dad","sound":"/ḍ/","word":"ضفدع","word_en":"Frog","emoji":"🐸","forms":["ـض","ـضـ","ضـ"]},
    {"letter":"ط","name_ar":"طاء","name_en":"Taa","sound":"/ṭ/","word":"طائر","word_en":"Bird","emoji":"🐦","forms":["ـط","ـطـ","طـ"]},
    {"letter":"ظ","name_ar":"ظاء","name_en":"Dhaa","sound":"/ẓ/","word":"ظرف","word_en":"Envelope","emoji":"✉️","forms":["ـظ","ـظـ","ظـ"]},
    {"letter":"ع","name_ar":"عين","name_en":"Ayn","sound":"/ʿ/","word":"عنب","word_en":"Grapes","emoji":"🍇","forms":["ـع","ـعـ","عـ"]},
    {"letter":"غ","name_ar":"غين","name_en":"Ghayn","sound":"/gh/","word":"غزال","word_en":"Gazelle","emoji":"🦌","forms":["ـغ","ـغـ","غـ"]},
    {"letter":"ف","name_ar":"فاء","name_en":"Fa","sound":"/f/","word":"فراشة","word_en":"Butterfly","emoji":"🦋","forms":["ـف","ـفـ","فـ"]},
    {"letter":"ق","name_ar":"قاف","name_en":"Qaf","sound":"/q/","word":"قمر","word_en":"Moon","emoji":"🌙","forms":["ـق","ـقـ","قـ"]},
    {"letter":"ك","name_ar":"كاف","name_en":"Kaf","sound":"/k/","word":"كتاب","word_en":"Book","emoji":"📖","forms":["ـك","ـكـ","كـ"]},
    {"letter":"ل","name_ar":"لام","name_en":"Lam","sound":"/l/","word":"ليمون","word_en":"Lemon","emoji":"🍋","forms":["ـل","ـلـ","لـ"]},
    {"letter":"م","name_ar":"ميم","name_en":"Mim","sound":"/m/","word":"مسجد","word_en":"Mosque","emoji":"🕌","forms":["ـم","ـمـ","مـ"]},
    {"letter":"ن","name_ar":"نون","name_en":"Nun","sound":"/n/","word":"نجمة","word_en":"Star","emoji":"⭐","forms":["ـن","ـنـ","نـ"]},
    {"letter":"هـ","name_ar":"هاء","name_en":"Ha","sound":"/h/","word":"هلال","word_en":"Crescent","emoji":"🌙","forms":["ـه","ـهـ","هـ"]},
    {"letter":"و","name_ar":"واو","name_en":"Waw","sound":"/w/","word":"وردة","word_en":"Rose","emoji":"🌹","forms":["ـو","و"]},
    {"letter":"ي","name_ar":"ياء","name_en":"Ya","sound":"/y/","word":"يد","word_en":"Hand","emoji":"✋","forms":["ـي","ـيـ","يـ"]},
]

HARAKAT = [
    {"name_ar":"فتحة","name_en":"Fatha","symbol":"َ","sound":"a","example":"بَ","example_word":"بَابٌ","meaning":"door"},
    {"name_ar":"كسرة","name_en":"Kasra","symbol":"ِ","sound":"i","example":"بِ","example_word":"بِنتٌ","meaning":"girl"},
    {"name_ar":"ضمة","name_en":"Damma","symbol":"ُ","sound":"u","example":"بُ","example_word":"بُرتقال","meaning":"orange"},
    {"name_ar":"سكون","name_en":"Sukun","symbol":"ْ","sound":"(stop)","example":"بْ","example_word":"صَبْر","meaning":"patience"},
    {"name_ar":"شدة","name_en":"Shadda","symbol":"ّ","sound":"(double)","example":"بّ","example_word":"رَبّ","meaning":"Lord"},
    {"name_ar":"تنوين فتح","name_en":"Tanween Fath","symbol":"ً","sound":"an","example":"بً","example_word":"كِتَابًا","meaning":"a book"},
    {"name_ar":"تنوين كسر","name_en":"Tanween Kasr","symbol":"ٍ","sound":"in","example":"بٍ","example_word":"كِتَابٍ","meaning":"a book"},
    {"name_ar":"تنوين ضم","name_en":"Tanween Damm","symbol":"ٌ","sound":"un","example":"بٌ","example_word":"كِتَابٌ","meaning":"a book"},
]

VOCAB_CATEGORIES = {
    "colors": [
        {"ar":"أحمر","en":"Red","emoji":"🔴"},{"ar":"أزرق","en":"Blue","emoji":"🔵"},
        {"ar":"أخضر","en":"Green","emoji":"🟢"},{"ar":"أصفر","en":"Yellow","emoji":"🟡"},
        {"ar":"برتقالي","en":"Orange","emoji":"🟠"},{"ar":"بنفسجي","en":"Purple","emoji":"🟣"},
        {"ar":"أبيض","en":"White","emoji":"⚪"},{"ar":"أسود","en":"Black","emoji":"⚫"},
        {"ar":"وردي","en":"Pink","emoji":"🩷"},{"ar":"بني","en":"Brown","emoji":"🟤"},
    ],
    "animals": [
        {"ar":"أسد","en":"Lion","emoji":"🦁"},{"ar":"قط","en":"Cat","emoji":"🐱"},
        {"ar":"كلب","en":"Dog","emoji":"🐶"},{"ar":"حصان","en":"Horse","emoji":"🐴"},
        {"ar":"جمل","en":"Camel","emoji":"🐫"},{"ar":"فيل","en":"Elephant","emoji":"🐘"},
        {"ar":"سمكة","en":"Fish","emoji":"🐟"},{"ar":"فراشة","en":"Butterfly","emoji":"🦋"},
        {"ar":"نحلة","en":"Bee","emoji":"🐝"},{"ar":"نملة","en":"Ant","emoji":"🐜"},
        {"ar":"أرنب","en":"Rabbit","emoji":"🐰"},{"ar":"بقرة","en":"Cow","emoji":"🐄"},
        {"ar":"خروف","en":"Sheep","emoji":"🐑"},{"ar":"طائر","en":"Bird","emoji":"🐦"},
    ],
    "family": [
        {"ar":"أب","en":"Father","emoji":"👨"},{"ar":"أم","en":"Mother","emoji":"👩"},
        {"ar":"أخ","en":"Brother","emoji":"👦"},{"ar":"أخت","en":"Sister","emoji":"👧"},
        {"ar":"جد","en":"Grandfather","emoji":"👴"},{"ar":"جدة","en":"Grandmother","emoji":"👵"},
        {"ar":"عم","en":"Uncle","emoji":"👨‍🦱"},{"ar":"خالة","en":"Aunt","emoji":"👩‍🦱"},
        {"ar":"ابن","en":"Son","emoji":"👦"},{"ar":"بنت","en":"Daughter","emoji":"👧"},
    ],
    "body": [
        {"ar":"رأس","en":"Head","emoji":"🗣️"},{"ar":"عين","en":"Eye","emoji":"👁️"},
        {"ar":"أنف","en":"Nose","emoji":"👃"},{"ar":"فم","en":"Mouth","emoji":"👄"},
        {"ar":"أذن","en":"Ear","emoji":"👂"},{"ar":"يد","en":"Hand","emoji":"✋"},
        {"ar":"قدم","en":"Foot","emoji":"🦶"},{"ar":"قلب","en":"Heart","emoji":"❤️"},
        {"ar":"شعر","en":"Hair","emoji":"💇"},{"ar":"إصبع","en":"Finger","emoji":"☝️"},
    ],
    "food": [
        {"ar":"تفاحة","en":"Apple","emoji":"🍎"},{"ar":"موزة","en":"Banana","emoji":"🍌"},
        {"ar":"خبز","en":"Bread","emoji":"🍞"},{"ar":"حليب","en":"Milk","emoji":"🥛"},
        {"ar":"ماء","en":"Water","emoji":"💧"},{"ar":"أرز","en":"Rice","emoji":"🍚"},
        {"ar":"بيضة","en":"Egg","emoji":"🥚"},{"ar":"تمر","en":"Date","emoji":"🌴"},
        {"ar":"عسل","en":"Honey","emoji":"🍯"},{"ar":"سمك","en":"Fish","emoji":"🐟"},
    ],
    "home": [
        {"ar":"بيت","en":"House","emoji":"🏠"},{"ar":"باب","en":"Door","emoji":"🚪"},
        {"ar":"نافذة","en":"Window","emoji":"🪟"},{"ar":"كرسي","en":"Chair","emoji":"🪑"},
        {"ar":"طاولة","en":"Table","emoji":"🪵"},{"ar":"سرير","en":"Bed","emoji":"🛏️"},
        {"ar":"مطبخ","en":"Kitchen","emoji":"🍳"},{"ar":"حمام","en":"Bathroom","emoji":"🚿"},
        {"ar":"غرفة","en":"Room","emoji":"🏠"},{"ar":"حديقة","en":"Garden","emoji":"🌳"},
    ],
    "nature": [
        {"ar":"شمس","en":"Sun","emoji":"☀️"},{"ar":"قمر","en":"Moon","emoji":"🌙"},
        {"ar":"نجمة","en":"Star","emoji":"⭐"},{"ar":"شجرة","en":"Tree","emoji":"🌳"},
        {"ar":"وردة","en":"Flower","emoji":"🌹"},{"ar":"بحر","en":"Sea","emoji":"🌊"},
        {"ar":"جبل","en":"Mountain","emoji":"🏔️"},{"ar":"نهر","en":"River","emoji":"🏞️"},
        {"ar":"سماء","en":"Sky","emoji":"🌤️"},{"ar":"مطر","en":"Rain","emoji":"🌧️"},
    ],
    "school": [
        {"ar":"مدرسة","en":"School","emoji":"🏫"},{"ar":"كتاب","en":"Book","emoji":"📖"},
        {"ar":"قلم","en":"Pen","emoji":"🖊️"},{"ar":"معلم","en":"Teacher","emoji":"👨‍🏫"},
        {"ar":"طالب","en":"Student","emoji":"🧑‍🎓"},{"ar":"فصل","en":"Class","emoji":"🏫"},
        {"ar":"واجب","en":"Homework","emoji":"📝"},{"ar":"امتحان","en":"Exam","emoji":"📋"},
    ],
    "greetings": [
        {"ar":"السلام عليكم","en":"Peace be upon you","emoji":"👋"},
        {"ar":"وعليكم السلام","en":"And upon you peace","emoji":"🤝"},
        {"ar":"صباح الخير","en":"Good morning","emoji":"🌅"},
        {"ar":"مساء الخير","en":"Good evening","emoji":"🌆"},
        {"ar":"مع السلامة","en":"Goodbye","emoji":"👋"},
        {"ar":"شكراً","en":"Thank you","emoji":"🙏"},
        {"ar":"عفواً","en":"You're welcome","emoji":"😊"},
        {"ar":"من فضلك","en":"Please","emoji":"🙏"},
        {"ar":"نعم","en":"Yes","emoji":"✅"},
        {"ar":"لا","en":"No","emoji":"❌"},
    ],
}

NUMBERS_FULL = [
    {"num":i,"ar":ar,"en":en,"display":d} for i,(ar,en,d) in enumerate([
        ("صفر","Zero","٠"),("واحد","One","١"),("اثنان","Two","٢"),("ثلاثة","Three","٣"),
        ("أربعة","Four","٤"),("خمسة","Five","٥"),("ستة","Six","٦"),("سبعة","Seven","٧"),
        ("ثمانية","Eight","٨"),("تسعة","Nine","٩"),("عشرة","Ten","١٠"),
        ("أحد عشر","Eleven","١١"),("اثنا عشر","Twelve","١٢"),("ثلاثة عشر","Thirteen","١٣"),
        ("أربعة عشر","Fourteen","١٤"),("خمسة عشر","Fifteen","١٥"),("ستة عشر","Sixteen","١٦"),
        ("سبعة عشر","Seventeen","١٧"),("ثمانية عشر","Eighteen","١٨"),("تسعة عشر","Nineteen","١٩"),
        ("عشرون","Twenty","٢٠"),
    ])
]

SENTENCES_BASIC = [
    {"ar":"هذا كتاب","en":"This is a book","emoji":"📖"},
    {"ar":"هذه تفاحة","en":"This is an apple","emoji":"🍎"},
    {"ar":"أنا سعيد","en":"I am happy","emoji":"😊"},
    {"ar":"ما اسمك؟","en":"What is your name?","emoji":"❓"},
    {"ar":"اسمي أحمد","en":"My name is Ahmad","emoji":"👦"},
    {"ar":"كم عمرك؟","en":"How old are you?","emoji":"🎂"},
    {"ar":"أين المسجد؟","en":"Where is the mosque?","emoji":"🕌"},
    {"ar":"الحمد لله","en":"Praise be to Allah","emoji":"🙏"},
    {"ar":"إن شاء الله","en":"God willing","emoji":"🤲"},
    {"ar":"ما شاء الله","en":"What Allah willed","emoji":"✨"},
    {"ar":"بارك الله فيك","en":"May Allah bless you","emoji":"🌟"},
    {"ar":"جزاك الله خيراً","en":"May Allah reward you","emoji":"💝"},
    {"ar":"أحب أمي وأبي","en":"I love my mom and dad","emoji":"❤️"},
    {"ar":"أنا أتعلم العربية","en":"I am learning Arabic","emoji":"📚"},
    {"ar":"الطقس جميل اليوم","en":"The weather is beautiful today","emoji":"☀️"},
]


# ═══════════════════════════════════════════════════════════════
# CURRICULUM ENGINE - Generates structured lessons
# ═══════════════════════════════════════════════════════════════

def get_curriculum_overview(locale: str = "en") -> dict:
    """Get the full curriculum overview with stages."""
    lang = locale if locale in ["ar","en","de","fr","tr","ru","sv","nl","el"] else "en"
    stages = []
    for s in CURRICULUM_STAGES:
        start, end = s["days"]
        stages.append({
            "id": s["id"],
            "emoji": s["emoji"],
            "color": s["color"],
            "title": s["title"].get(lang, s["title"]["en"]),
            "description": s["desc"].get(lang, s["desc"]["en"]),
            "day_start": start,
            "day_end": end,
            "total_lessons": end - start + 1,
        })
    return {"stages": stages, "total_days": 1000, "total_stages": 15}


def get_stage_for_day(day: int) -> dict:
    """Get which stage a day belongs to."""
    for s in CURRICULUM_STAGES:
        if s["days"][0] <= day <= s["days"][1]:
            return s
    return CURRICULUM_STAGES[-1]


def generate_lesson(day: int, locale: str = "en") -> dict:
    """Generate a structured lesson for a specific day."""
    lang = locale if locale in ["ar","en","de","fr","tr","ru","sv","nl","el"] else "en"
    stage = get_stage_for_day(day)
    stage_id = stage["id"]
    stage_start = stage["days"][0]
    lesson_in_stage = day - stage_start  # 0-indexed within stage
    
    lesson = {
        "day": day,
        "stage": {
            "id": stage_id,
            "emoji": stage["emoji"],
            "color": stage["color"],
            "title": stage["title"].get(lang, stage["title"]["en"]),
        },
        "lesson_number_in_stage": lesson_in_stage + 1,
        "total_in_stage": stage["days"][1] - stage_start + 1,
        "sections": [],
    }
    
    # ═══ STAGE 1: ARABIC ALPHABET (Days 1-56) ═══
    if stage_id == "S01":
        if lesson_in_stage < 28:
            # Day 1-28: One letter per day
            lt = LETTERS_28[lesson_in_stage]
            lp = LETTER_PREFIX.get(lang, LETTER_PREFIX["en"])
            lt_name = lt["name_ar"] if lang == "ar" else lt["name_en"]
            lesson["title"] = {lang: f"{lp} {lt_name}"}
            word_translated = _tw(lt["word_en"], lang) if lang != "ar" else lt["word"]
            lesson["sections"] = [
                {"type": "learn", "emoji": "📝", "title": t("meet_the_letter", lang),
                 "content": {"letter": lt["letter"], "name_ar": lt["name_ar"], "name": lt_name,
                             "sound": lt["sound"], "example_word": lt["word"], "example_translated": word_translated,
                             "example_emoji": lt["emoji"]}},
                {"type": "listen", "emoji": "🔊", "title": t("listen_repeat", lang),
                 "content": {"text": lt["letter"], "word": lt["word"], "tip": t("tip_tap_letter", lang)}},
                {"type": "quiz", "emoji": "❓", "title": t("test_yourself", lang),
                 "content": {"question": t("quiz_which_letter_sounds", lang, sound=lt['sound']),
                             "correct": lt["letter"],
                             "options": _make_letter_options(lt["letter"], lesson_in_stage)}},
                {"type": "write", "emoji": "✍️", "title": t("practice_writing", lang),
                 "content": {"letter": lt["letter"], "tip": t("tip_write_letter_5", lang)}},
            ]
        elif lesson_in_stage < 42:
            # Day 29-42: Letter forms (beginning, middle, end)
            idx = (lesson_in_stage - 28) * 2
            if idx < 28:
                lt = LETTERS_28[idx]
                lt2 = LETTERS_28[min(idx+1, 27)]
                fp = FORMS_PREFIX.get(lang, FORMS_PREFIX["en"])
                n1 = lt["name_ar"] if lang == "ar" else lt["name_en"]
                n2 = lt2["name_ar"] if lang == "ar" else lt2["name_en"]
                lesson["title"] = {lang: f"{fp} {n1} & {n2}" if lang != "ar" else f"أشكال {n1} و{n2}"}
                lesson["sections"] = [
                    {"type": "learn", "emoji": "📝", "title": t("learn", lang),
                     "content": {"letters": [
                         {"letter": lt["letter"], "forms": lt["forms"], "name": n1},
                         {"letter": lt2["letter"], "forms": lt2["forms"], "name": n2},
                     ]}},
                    {"type": "practice", "emoji": "🎯", "title": t("test", lang),
                     "content": {"tip": t("learn", lang)}},
                ]
            else:
                lesson["title"] = {lang: REVIEW_FORMS.get(lang, REVIEW_FORMS["en"])}
                lesson["sections"] = [{"type": "review", "emoji": "🔄", "title": t("comprehensive_review", lang),
                     "content": {"tip": t("review", lang)}}]
        else:
            review_idx = (lesson_in_stage - 42) * 2
            lt = LETTERS_28[min(review_idx, 27)]
            lesson["title"] = {lang: WRITING_PRACTICE.get(lang, WRITING_PRACTICE["en"])}
            word_translated = _tw(lt["word_en"], lang) if lang != "ar" else lt["word"]
            lesson["sections"] = [
                {"type": "connect", "emoji": "🔗", "title": t("learn", lang),
                 "content": {"tip": t("learn", lang)}},
                {"type": "write", "emoji": "✍️", "title": t("practice_writing", lang),
                 "content": {"word": lt["word"], "word_translated": word_translated, "tip": t("tip_write_letter_5", lang)}},
            ]
    
    # ═══ STAGE 2: VOWELS (Days 57-84) ═══
    elif stage_id == "S02":
        h_idx = lesson_in_stage % len(HARAKAT)
        h = HARAKAT[h_idx]
        if lesson_in_stage < len(HARAKAT) * 3:
            h_name = h["name_ar"] if lang == "ar" else h["name_en"]
            lesson["title"] = {lang: h_name}
            meaning_translated = _tw(h["meaning"], lang) if lang != "ar" else h["meaning"]
            lesson["sections"] = [
                {"type": "learn", "emoji": "🎵", "title": t("learn", lang),
                 "content": {"name_ar": h["name_ar"], "name": h_name, "symbol": h["symbol"],
                             "sound": h["sound"], "example": h["example"],
                             "example_word": h["example_word"], "meaning": meaning_translated}},
                {"type": "practice", "emoji": "🎯", "title": t("test", lang),
                 "content": {"tip": t("listen_repeat", lang),
                             "items": [f"{lt['letter']}{h['symbol']}" for lt in LETTERS_28[:7]]}},
                {"type": "quiz", "emoji": "❓", "title": t("test_yourself", lang),
                 "content": {"question": t("quiz_which_letter_sounds", lang, sound=h['symbol']),
                             "correct": h["sound"], "options": [h["sound"], HARAKAT[(h_idx+1)%len(HARAKAT)]["sound"], HARAKAT[(h_idx+2)%len(HARAKAT)]["sound"]]}},
            ]
        else:
            lesson["title"] = {lang: VOWELS_REVIEW.get(lang, VOWELS_REVIEW["en"])}
            lesson["sections"] = [{"type": "review", "emoji": "🔄", "title": t("review", lang),
                 "content": {"items": [{"name": h["name_ar"] if lang == "ar" else h["name_en"], "symbol": h["symbol"], "sound": h["sound"]} for h in HARAKAT]}}]
    
    # ═══ STAGE 3: NUMBERS (Days 85-112) ═══
    elif stage_id == "S03":
        n_idx = lesson_in_stage % len(NUMBERS_FULL)
        n = NUMBERS_FULL[n_idx]
        lesson["title"] = {"ar": f"العدد {n['ar']}", "en": f"Number {n['en']}"}
        lesson["sections"] = [
            {"type": "learn", "emoji": "🔢", "title": t("learn", lang),
             "content": {"number": n["num"], "arabic": n["ar"], "english": n["en"], "display": n["display"]}},
            {"type": "practice", "emoji": "🎯", "title": t("listen_repeat", lang),
             "content": {"tip": t("listen_repeat", lang)}},
            {"type": "quiz", "emoji": "❓", "title": t("test", lang),
             "content": {"question": t("quiz_what_number", lang, number=n['display']),
                         "correct": n["ar"], "options": [n["ar"], NUMBERS_FULL[(n_idx+1)%len(NUMBERS_FULL)]["ar"], NUMBERS_FULL[(n_idx+2)%len(NUMBERS_FULL)]["ar"]]}},
        ]
    
    # ═══ STAGE 4: FIRST WORDS (Days 113-210) ═══
    elif stage_id == "S04":
        cats = list(VOCAB_CATEGORIES.keys())
        cat_idx = lesson_in_stage // 14
        word_idx = lesson_in_stage % 14
        cat = cats[min(cat_idx, len(cats)-1)]
        words = VOCAB_CATEGORIES[cat]
        word = words[word_idx % len(words)]
        
        cat_locale = get_cat_name(cat, lang)
        
        lesson["title"] = {"ar": f"{get_cat_name(cat, 'ar')}: {word['ar']}", "en": f"{get_cat_name(cat, 'en')}: {word['en']}"}
        lesson["sections"] = [
            {"type": "learn", "emoji": word.get("emoji","📝"), "title": f"{t('new_word', lang)}: {word['ar']}",
             "content": {"arabic": word["ar"], "english": word["en"], "emoji": word.get("emoji",""), "category": cat, "category_locale": cat_locale}},
            {"type": "listen", "emoji": "🔊", "title": t("listen_repeat", lang),
             "content": {"text": word["ar"], "tip": t("tip_say_word", lang)}},
            {"type": "quiz", "emoji": "❓", "title": t("test_yourself", lang),
             "content": {"question": t("quiz_what_in_arabic", lang, emoji=word.get('emoji', word['en'])),
                         "correct": word["ar"],
                         "options": [word["ar"]] + [w["ar"] for w in random.sample([w2 for w2 in words if w2["ar"]!=word["ar"]], min(2, len(words)-1))]}},
        ]
    
    # ═══ STAGE 5: SIMPLE SENTENCES (Days 211-266) ═══
    elif stage_id == "S05":
        s_idx = lesson_in_stage % len(SENTENCES_BASIC)
        sent = SENTENCES_BASIC[s_idx]
        lesson["title"] = {"ar": sent["ar"], "en": sent["en"]}
        lesson["sections"] = [
            {"type": "learn", "emoji": sent["emoji"], "title": t("new_sentence", lang),
             "content": {"arabic": sent["ar"], "english": sent["en"], "emoji": sent["emoji"]}},
            {"type": "listen", "emoji": "🔊", "title": t("listen_repeat", lang),
             "content": {"text": sent["ar"], "tip": t("tip_repeat_sentence", lang)}},
            {"type": "practice", "emoji": "✍️", "title": t("write_sentence", lang),
             "content": {"tip": t("tip_write_sentence_3", lang), "sentence": sent["ar"]}},
        ]
    
    # ═══ STAGES 6-15: Use content from kids_learning.py ═══
    else:
        # For stages 6+, create dynamic content based on the stage
        lesson["title"] = {"ar": f"درس {lesson_in_stage + 1}", "en": f"Lesson {lesson_in_stage + 1}"}
        lesson["sections"] = _build_advanced_sections(stage_id, lesson_in_stage, lang)
    
    # Add progress tracking fields
    lesson["total_sections"] = len(lesson["sections"])
    lesson["xp_reward"] = 10 + (5 * len(lesson["sections"]))
    
    return lesson


def _make_letter_options(correct: str, idx: int) -> list:
    """Make quiz options for letter identification."""
    options = [correct]
    all_letters = [l["letter"] for l in LETTERS_28]
    others = [l for l in all_letters if l != correct]
    random.shuffle(others)
    options.extend(others[:3])
    random.shuffle(options)
    return options


def _build_advanced_sections(stage_id: str, lesson_idx: int, lang: str) -> list:
    """Build sections for advanced stages (6-15)."""
    sections = []
    
    if stage_id == "S06":  # Reading Practice
        words = []
        for cat in VOCAB_CATEGORIES.values():
            words.extend(cat)
        w = words[lesson_idx % len(words)]
        sections = [
            {"type": "read", "emoji": "📖", "title": t("read_word", lang),
             "content": {"arabic": w["ar"], "english": w["en"], "emoji": w.get("emoji","")}},
            {"type": "listen", "emoji": "🔊", "title": t("listen_repeat", lang),
             "content": {"text": w["ar"]}},
        ]
    
    elif stage_id == "S07":  # Islamic Foundations
        topics = ["shahada","salah","zakat","sawm","hajj","wudu","iman","mosque","quran_intro","islamic_months"]
        topic = topics[lesson_idx % len(topics)]
        topic_content = {
            "shahada": {"ar":"الشهادتان: أشهد أن لا إله إلا الله وأن محمداً رسول الله","en":"The Two Testimonies: I bear witness there is no god but Allah and Muhammad is His messenger"},
            "salah": {"ar":"الصلاة: خمس صلوات في اليوم - الفجر، الظهر، العصر، المغرب، العشاء","en":"Prayer: Five daily prayers - Fajr, Dhuhr, Asr, Maghrib, Isha"},
            "zakat": {"ar":"الزكاة: إعطاء جزء من المال للفقراء","en":"Zakat: Giving a portion of wealth to the poor"},
            "sawm": {"ar":"الصوم: الامتناع عن الطعام والشراب في رمضان من الفجر للمغرب","en":"Fasting: Abstaining from food and drink in Ramadan from dawn to sunset"},
            "hajj": {"ar":"الحج: زيارة مكة المكرمة مرة في العمر لمن استطاع","en":"Hajj: Visiting Makkah once in a lifetime for those who can"},
            "wudu": {"ar":"الوضوء: غسل أجزاء من الجسم استعداداً للصلاة","en":"Wudu: Washing parts of the body in preparation for prayer"},
            "iman": {"ar":"أركان الإيمان الستة: الإيمان بالله والملائكة والكتب والرسل واليوم الآخر والقدر","en":"Six Pillars of Faith: Belief in Allah, Angels, Books, Messengers, Last Day, and Divine Decree"},
            "mosque": {"ar":"المسجد: بيت الله حيث يصلي المسلمون ويتعلمون","en":"The Mosque: House of Allah where Muslims pray and learn"},
            "quran_intro": {"ar":"القرآن الكريم: كلام الله المنزل على محمد ﷺ فيه 114 سورة","en":"The Holy Quran: Allah's word revealed to Muhammad ﷺ, containing 114 surahs"},
            "islamic_months": {"ar":"الأشهر الهجرية: محرم، صفر، ربيع الأول... رمضان، شوال، ذو القعدة، ذو الحجة","en":"Islamic Months: Muharram, Safar, Rabi al-Awwal... Ramadan, Shawwal, Dhul-Qi'dah, Dhul-Hijjah"},
        }
        tc = topic_content.get(topic, topic_content["shahada"])
        sections = [
            {"type": "learn", "emoji": "🤲", "title": t("learn", lang),
             "content": {"arabic": tc["ar"], "english": tc["en"]}},
            {"type": "memorize", "emoji": "🧠", "title": t("memorize", lang),
             "content": {"text": tc["ar"], "tip": t("tip_read_3_memory", lang)}},
        ]
    
    elif stage_id in ["S08","S14"]:  # Quran Memorization
        from kids_learning import QURAN_SURAHS_FOR_KIDS
        s_idx = lesson_idx // 7
        a_idx = lesson_idx % 7
        if s_idx < len(QURAN_SURAHS_FOR_KIDS):
            surah = QURAN_SURAHS_FOR_KIDS[s_idx]
            ayah = surah["ayahs"][a_idx % len(surah["ayahs"])]
            sections = [
                {"type": "quran", "emoji": "📖", "title": t("memorize_prefix", lang, name=surah['name_en']),
                 "content": {"surah": surah["name_en"], "ayah_num": ayah["num"],
                             "arabic": ayah["ar"], "translation": ayah.get(lang, ayah["en"])}},
                {"type": "listen", "emoji": "🔊", "title": t("listen", lang),
                 "content": {"text": ayah["ar"]}},
                {"type": "memorize", "emoji": "🧠", "title": t("recite", lang),
                 "content": {"tip": t("tip_close_eyes_recite", lang)}},
            ]
        else:
            sections = [{"type": "review", "emoji": "🔄", "title": t("review", lang), "content": {}}]
    
    elif stage_id == "S09":  # Duas
        from kids_learning import KIDS_DUAS
        d = KIDS_DUAS[lesson_idx % len(KIDS_DUAS)]
        sections = [
            {"type": "dua", "emoji": d["emoji"], "title": d["title"].get(lang, d["title"]["en"]),
             "content": {"arabic": d["ar"], "transliteration": d["transliteration"], "meaning": d.get(lang, d["en"])}},
            {"type": "memorize", "emoji": "🧠", "title": t("memorize_dua", lang),
             "content": {"tip": t("tip_repeat_dua_5", lang)}},
        ]
    
    elif stage_id == "S10":  # Hadiths
        from kids_learning import KIDS_HADITHS
        h = KIDS_HADITHS[lesson_idx % len(KIDS_HADITHS)]
        sections = [
            {"type": "hadith", "emoji": h["emoji"], "title": t("todays_hadith", lang),
             "content": {"arabic": h["ar"], "translation": h.get(lang, h["en"]), "source": h["source"],
                         "lesson": h["lesson"].get(lang, h["lesson"]["en"])}},
            {"type": "reflect", "emoji": "💭", "title": t("reflect", lang),
             "content": {"tip": t("tip_apply_hadith", lang)}},
        ]
    
    elif stage_id == "S11":  # Prophet Stories
        from kids_learning_extended import ALL_PROPHETS
        p = ALL_PROPHETS[lesson_idx % len(ALL_PROPHETS)]
        sections = [
            {"type": "story", "emoji": p["emoji"], "title": p["name"].get(lang, p["name"]["en"]),
             "content": {"name": p["name"].get(lang, p["name"]["en"]), "title": p["title"].get(lang, p["title"]["en"]),
                         "summary": p["summary"].get(lang, p["summary"]["en"]),
                         "lesson": p["lesson"].get(lang, p["lesson"]["en"]), "quran_ref": p["quran_ref"]}},
        ]
    
    elif stage_id == "S12":  # Islamic Life
        topics = [
            {"emoji":"🌙","ar":"رمضان شهر الصيام والقرآن والعبادة. نصوم من الفجر إلى المغرب","en":"Ramadan is the month of fasting, Quran and worship. We fast from dawn to sunset"},
            {"emoji":"🕋","ar":"الحج: ملايين المسلمين يزورون مكة كل عام لأداء مناسك الحج","en":"Hajj: Millions of Muslims visit Makkah every year to perform the pilgrimage"},
            {"emoji":"🎉","ar":"عيد الفطر: نفرح بعد رمضان، نصلي صلاة العيد ونزور الأهل","en":"Eid Al-Fitr: We celebrate after Ramadan, pray Eid prayer and visit family"},
            {"emoji":"🐑","ar":"عيد الأضحى: نتذكر قصة إبراهيم وإسماعيل ونضحي","en":"Eid Al-Adha: We remember Ibrahim and Ismail's story and offer sacrifice"},
            {"emoji":"🕌","ar":"يوم الجمعة: أفضل أيام الأسبوع، نصلي صلاة الجمعة في المسجد","en":"Friday: The best day of the week, we pray Jumu'ah prayer at the mosque"},
        ]
        topic_item = topics[lesson_idx % len(topics)]
        sections = [
            {"type": "learn", "emoji": topic_item["emoji"], "title": t("learn", lang),
             "content": {"arabic": topic_item["ar"], "english": topic_item["en"]}},
        ]
    
    elif stage_id == "S13":  # Advanced Arabic
        sections = [
            {"type": "grammar", "emoji": "📚", "title": t("grammar", lang),
             "content": {"tip": t("tip_learn_grammar", lang)}},
        ]
    
    elif stage_id == "S15":  # Mastery
        sections = [
            {"type": "review", "emoji": "🎓", "title": t("comprehensive_review", lang),
             "content": {"tip": t("tip_review_all", lang)}},
        ]
    
    if not sections:
        sections = [{"type": "learn", "emoji": "📝", "title": t("lesson", lang), "content": {}}]
    
    return sections

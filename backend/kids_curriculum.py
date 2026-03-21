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
     "desc": {"ar": "تعلم الحروف العربية الـ 28 وأشكالها وأصواتها", "en": "Learn all 28 Arabic letters, their forms and sounds", "de": "Lerne alle 28 arabischen Buchstaben", "fr": "Apprenez les 28 lettres arabes", "tr": "28 Arap harfini öğrenin", "ru": "Изучите все 28 арабских букв", "sv": "Lär dig alla 28 arabiska bokstäver, deras former och ljud", "nl": "Leer alle 28 Arabische letters, hun vormen en klanken", "el": "Μάθε όλα τα 28 αραβικά γράμματα, τις μορφές και τους ήχους τους"}},
    {"id": "S02", "days": [57, 84], "emoji": "🎵", "color": "#8B5CF6",
     "title": {"ar": "الحركات والتشكيل", "en": "Vowels & Diacritics", "de": "Vokale & Diakritika", "fr": "Voyelles & Diacritiques", "tr": "Sesli Harfler", "ru": "Гласные и диакритика", "sv": "Vokaler & diakritiska tecken", "nl": "Klinkers & diakritische tekens", "el": "Φωνήεντα & διακριτικά"},
     "desc": {"ar": "الفتحة والكسرة والضمة والسكون والشدة والتنوين", "en": "Fatha, Kasra, Damma, Sukun, Shadda & Tanween", "de": "Fatha, Kasra, Damma, Sukun, Shadda & Tanween", "fr": "Fatha, Kasra, Damma, Sukun, Shadda & Tanween", "tr": "Fatha, Kasra, Damma, Sukun, Şedde, Tenvin", "ru": "Фатха, Касра, Дамма, Сукун, Шадда и Танвин", "sv": "Fatha, Kasra, Damma, Sukun, Shadda & Tanween", "nl": "Fatha, Kasra, Damma, Sukun, Shadda & Tanween", "el": "Φάθα, Κάσρα, Ντάμμα, Σουκούν, Σάντα & Τανουίν"}},
    {"id": "S03", "days": [85, 112], "emoji": "🔢", "color": "#06B6D4",
     "title": {"ar": "الأرقام العربية", "en": "Arabic Numbers", "de": "Arabische Zahlen", "fr": "Chiffres arabes", "tr": "Arapça Sayılar", "ru": "Арабские цифры", "sv": "Arabiska siffror", "nl": "Arabische cijfers", "el": "Αραβικοί αριθμοί"},
     "desc": {"ar": "تعلم الأرقام من ٠ إلى ١٠٠ والعدّ", "en": "Learn numbers from 0 to 100 and counting", "de": "Lerne Zahlen von 0 bis 100", "fr": "Apprenez les chiffres de 0 à 100", "tr": "0'dan 100'e sayıları öğrenin", "ru": "Изучите числа от 0 до 100", "sv": "Lär dig siffror från 0 till 100", "nl": "Leer cijfers van 0 tot 100", "el": "Μάθε αριθμούς από 0 έως 100"}},
    {"id": "S04", "days": [113, 210], "emoji": "📝", "color": "#F59E0B",
     "title": {"ar": "الكلمات الأولى", "en": "First Words", "de": "Erste Wörter", "fr": "Premiers mots", "tr": "İlk Kelimeler", "ru": "Первые слова", "sv": "Första orden", "nl": "Eerste woorden", "el": "Πρώτες λέξεις"},
     "desc": {"ar": "ألوان، حيوانات، عائلة، جسم، طعام، بيت، طبيعة", "en": "Colors, Animals, Family, Body, Food, Home, Nature", "de": "Farben, Tiere, Familie, Körper, Essen, Haus, Natur", "fr": "Couleurs, Animaux, Famille, Corps, Nourriture, Maison, Nature", "tr": "Renkler, Hayvanlar, Aile, Vücut, Yiyecek, Ev, Doğa", "ru": "Цвета, Животные, Семья, Тело, Еда, Дом, Природа", "sv": "Färger, Djur, Familj, Kropp, Mat, Hem, Natur", "nl": "Kleuren, Dieren, Familie, Lichaam, Eten, Huis, Natuur", "el": "Χρώματα, Ζώα, Οικογένεια, Σώμα, Φαγητό, Σπίτι, Φύση"}},
    {"id": "S05", "days": [211, 266], "emoji": "💬", "color": "#10B981",
     "title": {"ar": "الجمل البسيطة", "en": "Simple Sentences", "de": "Einfache Sätze", "fr": "Phrases simples", "tr": "Basit Cümleler", "ru": "Простые предложения", "sv": "Enkla meningar", "nl": "Eenvoudige zinnen", "el": "Απλές προτάσεις"},
     "desc": {"ar": "التحيات، التعريف بالنفس، الأسئلة الأساسية", "en": "Greetings, introductions, basic questions", "de": "Grüße, Vorstellungen, einfache Fragen", "fr": "Salutations, présentations, questions de base", "tr": "Selamlaşma, tanışma, temel sorular", "ru": "Приветствия, представление, основные вопросы", "sv": "Hälsningar, presentationer, grundläggande frågor", "nl": "Begroetingen, voorstellingen, basisvragen", "el": "Χαιρετισμοί, συστάσεις, βασικές ερωτήσεις"}},
    {"id": "S06", "days": [267, 308], "emoji": "📖", "color": "#EF4444",
     "title": {"ar": "تمرين القراءة", "en": "Reading Practice", "de": "Leseübung", "fr": "Exercice de lecture", "tr": "Okuma Alıştırması", "ru": "Практика чтения", "sv": "Läsövning", "nl": "Leesoefening", "el": "Εξάσκηση ανάγνωσης"},
     "desc": {"ar": "قراءة كلمات وجمل وفقرات قصيرة", "en": "Reading words, sentences and short paragraphs", "de": "Wörter, Sätze und kurze Absätze lesen", "fr": "Lire des mots, phrases et courts paragraphes", "tr": "Kelime, cümle ve kısa paragraf okuma", "ru": "Чтение слов, предложений и коротких абзацев", "sv": "Läsa ord, meningar och korta stycken", "nl": "Woorden, zinnen en korte alinea's lezen", "el": "Ανάγνωση λέξεων, προτάσεων και σύντομων παραγράφων"}},
    {"id": "S07", "days": [309, 378], "emoji": "🤲", "color": "#059669",
     "title": {"ar": "أساسيات الإسلام", "en": "Islamic Foundations", "de": "Islamische Grundlagen", "fr": "Fondements de l'Islam", "tr": "İslam Temelleri", "ru": "Основы Ислама", "sv": "Islams grunder", "nl": "Islamitische grondslagen", "el": "Θεμέλια του Ισλάμ"},
     "desc": {"ar": "أركان الإسلام، الإيمان، الوضوء، الصلاة، رمضان", "en": "Pillars of Islam, Faith, Wudu, Prayer, Ramadan", "de": "Säulen des Islam, Glaube, Wudu, Gebet, Ramadan", "fr": "Piliers de l'Islam, Foi, Wudu, Prière, Ramadan", "tr": "İslam'ın Şartları, İman, Abdest, Namaz, Ramazan", "ru": "Столпы Ислама, Вера, Вуду, Молитва, Рамадан", "sv": "Islams pelare, Tro, Wudu, Bön, Ramadan", "nl": "Zuilen van de Islam, Geloof, Woedoe, Gebed, Ramadan", "el": "Πυλώνες του Ισλάμ, Πίστη, Γουντού, Προσευχή, Ραμαζάνι"}},
    {"id": "S08", "days": [379, 490], "emoji": "📖", "color": "#7C3AED",
     "title": {"ar": "حفظ القرآن", "en": "Quran Memorization", "de": "Koran-Memorierung", "fr": "Mémorisation du Coran", "tr": "Kur'an Ezberleme", "ru": "Заучивание Корана", "sv": "Koranmemorering", "nl": "Koran memoriseren", "el": "Απομνημόνευση Κορανίου"},
     "desc": {"ar": "سور جزء عمّ مع التجويد المبسط", "en": "Juz Amma surahs with basic Tajweed", "de": "Juz Amma Suren mit einfachem Tajweed", "fr": "Sourates Juz Amma avec Tajweed de base", "tr": "Cüz Amma sureleri ve temel Tecvid", "ru": "Суры Джуз Амма с основами Таджвида", "sv": "Juz Amma-suror med grundläggande Tajweed", "nl": "Juz Amma soera's met basis Tajweed", "el": "Σούρες Τζουζ Άμμα με βασικό Τατζουίντ"}},
    {"id": "S09", "days": [491, 560], "emoji": "🤲", "color": "#0EA5E9",
     "title": {"ar": "الأدعية والأذكار", "en": "Duas & Daily Phrases", "de": "Duas & Tägliche Phrasen", "fr": "Duas & Phrases quotidiennes", "tr": "Dualar & Günlük İfadeler", "ru": "Дуа и ежедневные фразы", "sv": "Duas & dagliga fraser", "nl": "Duas & dagelijkse uitdrukkingen", "el": "Ντουάς & καθημερινές φράσεις"},
     "desc": {"ar": "أدعية يومية وعبارات إسلامية أساسية", "en": "Daily duas and essential Islamic phrases", "de": "Tägliche Duas und islamische Ausdrücke", "fr": "Duas quotidiennes et phrases islamiques essentielles", "tr": "Günlük dualar ve İslami ifadeler", "ru": "Ежедневные дуа и исламские фразы", "sv": "Dagliga duas och grundläggande islamiska fraser", "nl": "Dagelijkse duas en essentiële islamitische uitdrukkingen", "el": "Καθημερινά ντουά και βασικές ισλαμικές φράσεις"}},
    {"id": "S10", "days": [561, 630], "emoji": "📜", "color": "#D97706",
     "title": {"ar": "الأحاديث والأخلاق", "en": "Hadiths & Morals", "de": "Hadithe & Moral", "fr": "Hadiths & Morale", "tr": "Hadisler & Ahlak", "ru": "Хадисы и нравственность", "sv": "Hadither & moral", "nl": "Hadiths & moraal", "el": "Χαντίθ & ηθική"},
     "desc": {"ar": "أحاديث نبوية مبسطة ودروس أخلاقية", "en": "Simplified Prophet's hadiths and moral lessons", "de": "Vereinfachte Hadithe und moralische Lektionen", "fr": "Hadiths simplifiés et leçons morales", "tr": "Basitleştirilmiş hadisler ve ahlaki dersler", "ru": "Упрощённые хадисы и нравственные уроки", "sv": "Förenklade hadither och moraliska lektioner", "nl": "Vereenvoudigde hadiths en morele lessen", "el": "Απλοποιημένα χαντίθ και ηθικά μαθήματα"}},
    {"id": "S11", "days": [631, 720], "emoji": "🕌", "color": "#9333EA",
     "title": {"ar": "قصص الأنبياء", "en": "Prophet Stories", "de": "Prophetengeschichten", "fr": "Histoires des Prophètes", "tr": "Peygamber Kıssaları", "ru": "Истории пророков", "sv": "Profetberättelser", "nl": "Profetverhalen", "el": "Ιστορίες προφητών"},
     "desc": {"ar": "قصص الأنبياء الـ 25 المذكورين في القرآن", "en": "Stories of all 25 prophets in the Quran", "de": "Geschichten aller 25 Propheten im Koran", "fr": "Histoires des 25 prophètes du Coran", "tr": "Kur'an'daki 25 peygamberin kıssaları", "ru": "Истории всех 25 пророков Корана", "sv": "Berättelser om alla 25 profeter i Koranen", "nl": "Verhalen van alle 25 profeten in de Koran", "el": "Ιστορίες όλων των 25 προφητών στο Κοράνι"}},
    {"id": "S12", "days": [721, 810], "emoji": "🌙", "color": "#DC2626",
     "title": {"ar": "الحياة الإسلامية", "en": "Islamic Life", "de": "Islamisches Leben", "fr": "Vie islamique", "tr": "İslami Yaşam", "ru": "Исламская жизнь", "sv": "Islamiskt liv", "nl": "Islamitisch leven", "el": "Ισλαμική ζωή"},
     "desc": {"ar": "رمضان، الحج، الأعياد، التقويم الإسلامي", "en": "Ramadan, Hajj, Eids, Islamic calendar", "de": "Ramadan, Hadsch, Eid-Feste, islamischer Kalender", "fr": "Ramadan, Hajj, Fêtes de l'Aïd, calendrier islamique", "tr": "Ramazan, Hac, Bayramlar, İslami takvim", "ru": "Рамадан, Хадж, праздники, исламский календарь", "sv": "Ramadan, Hajj, Eid-högtider, islamisk kalender", "nl": "Ramadan, Hadj, Eid-feesten, islamitische kalender", "el": "Ραμαζάνι, Χατζ, Εΐντ, ισλαμικό ημερολόγιο"}},
    {"id": "S13", "days": [811, 900], "emoji": "📚", "color": "#0D9488",
     "title": {"ar": "عربي متقدم", "en": "Advanced Arabic", "de": "Fortgeschrittenes Arabisch", "fr": "Arabe avancé", "tr": "İleri Arapça", "ru": "Продвинутый арабский", "sv": "Avancerad arabiska", "nl": "Gevorderd Arabisch", "el": "Προχωρημένα αραβικά"},
     "desc": {"ar": "قواعد أساسية، أفعال، محادثات", "en": "Basic grammar, verbs, conversations", "de": "Grundgrammatik, Verben, Gespräche", "fr": "Grammaire de base, verbes, conversations", "tr": "Temel gramer, fiiller, konuşmalar", "ru": "Базовая грамматика, глаголы, разговоры", "sv": "Grundgrammatik, verb, konversationer", "nl": "Basisgrammatica, werkwoorden, gesprekken", "el": "Βασική γραμματική, ρήματα, συνομιλίες"}},
    {"id": "S14", "days": [901, 960], "emoji": "🏆", "color": "#B45309",
     "title": {"ar": "قرآن متقدم", "en": "Advanced Quran", "de": "Fortgeschrittener Koran", "fr": "Coran avancé", "tr": "İleri Kur'an", "ru": "Продвинутый Коран", "sv": "Avancerad Koran", "nl": "Gevorderde Koran", "el": "Προχωρημένο Κοράνι"},
     "desc": {"ar": "سور أطول، تفسير مبسط، تجويد متقدم", "en": "Longer surahs, simple Tafsir, advanced Tajweed", "de": "Längere Suren, einfacher Tafsir, fortgeschrittenes Tajweed", "fr": "Sourates plus longues, Tafsir simple, Tajweed avancé", "tr": "Uzun sureler, basit Tefsir, ileri Tecvid", "ru": "Длинные суры, простой Тафсир, продвинутый Таджвид", "sv": "Längre suror, enkel Tafsir, avancerad Tajweed", "nl": "Langere soera's, eenvoudige Tafsir, gevorderde Tajweed", "el": "Μεγαλύτερες σούρες, απλό Ταφσίρ, προχωρημένο Τατζουίντ"}},
    {"id": "S15", "days": [961, 1000], "emoji": "🎓", "color": "#4F46E5",
     "title": {"ar": "الإتقان والتخرج", "en": "Mastery & Graduation", "de": "Meisterschaft & Abschluss", "fr": "Maîtrise & Diplôme", "tr": "Ustalık & Mezuniyet", "ru": "Мастерство и выпускной", "sv": "Mästerskap & examen", "nl": "Meesterschap & diploma", "el": "Κυριαρχία & αποφοίτηση"},
     "desc": {"ar": "مراجعة شاملة واختبارات وشهادة إتقان", "en": "Comprehensive review, tests & mastery certificate", "de": "Umfassende Wiederholung, Tests & Meisterschaftszertifikat", "fr": "Révision complète, tests & certificat de maîtrise", "tr": "Kapsamlı tekrar, sınavlar ve ustalık sertifikası", "ru": "Полный обзор, тесты и сертификат мастерства", "sv": "Omfattande genomgång, prov & mästerskapscertifikat", "nl": "Uitgebreide herhaling, toetsen & meesterschapscertificaat", "el": "Ολοκληρωμένη επανάληψη, τεστ & πιστοποιητικό κυριαρχίας"}},
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

def _tw(en_word: str, lang: str, ar_word: str = "") -> str:
    """Translate a word to the target language. Falls back: lang -> ar (NO English fallback)."""
    if lang == "en":
        return en_word
    if lang == "ar":
        return ar_word or en_word
    entry = WORD_TRANSLATIONS.get(en_word, {})
    return entry.get(lang, entry.get(lang.split("-")[0], ar_word or en_word))

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

# Multi-language number name translations
NUMBER_NAME_TRANSLATIONS = {
    "Zero":{"de":"Null","fr":"Zéro","tr":"Sıfır","ru":"Ноль","sv":"Noll","nl":"Nul","el":"Μηδέν"},
    "One":{"de":"Eins","fr":"Un","tr":"Bir","ru":"Один","sv":"Ett","nl":"Een","el":"Ένα"},
    "Two":{"de":"Zwei","fr":"Deux","tr":"İki","ru":"Два","sv":"Två","nl":"Twee","el":"Δύο"},
    "Three":{"de":"Drei","fr":"Trois","tr":"Üç","ru":"Три","sv":"Tre","nl":"Drie","el":"Τρία"},
    "Four":{"de":"Vier","fr":"Quatre","tr":"Dört","ru":"Четыре","sv":"Fyra","nl":"Vier","el":"Τέσσερα"},
    "Five":{"de":"Fünf","fr":"Cinq","tr":"Beş","ru":"Пять","sv":"Fem","nl":"Vijf","el":"Πέντε"},
    "Six":{"de":"Sechs","fr":"Six","tr":"Altı","ru":"Шесть","sv":"Sex","nl":"Zes","el":"Έξι"},
    "Seven":{"de":"Sieben","fr":"Sept","tr":"Yedi","ru":"Семь","sv":"Sju","nl":"Zeven","el":"Επτά"},
    "Eight":{"de":"Acht","fr":"Huit","tr":"Sekiz","ru":"Восемь","sv":"Åtta","nl":"Acht","el":"Οκτώ"},
    "Nine":{"de":"Neun","fr":"Neuf","tr":"Dokuz","ru":"Девять","sv":"Nio","nl":"Negen","el":"Εννέα"},
    "Ten":{"de":"Zehn","fr":"Dix","tr":"On","ru":"Десять","sv":"Tio","nl":"Tien","el":"Δέκα"},
    "Eleven":{"de":"Elf","fr":"Onze","tr":"On bir","ru":"Одиннадцать","sv":"Elva","nl":"Elf","el":"Έντεκα"},
    "Twelve":{"de":"Zwölf","fr":"Douze","tr":"On iki","ru":"Двенадцать","sv":"Tolv","nl":"Twaalf","el":"Δώδεκα"},
    "Thirteen":{"de":"Dreizehn","fr":"Treize","tr":"On üç","ru":"Тринадцать","sv":"Tretton","nl":"Dertien","el":"Δεκατρία"},
    "Fourteen":{"de":"Vierzehn","fr":"Quatorze","tr":"On dört","ru":"Четырнадцать","sv":"Fjorton","nl":"Veertien","el":"Δεκατέσσερα"},
    "Fifteen":{"de":"Fünfzehn","fr":"Quinze","tr":"On beş","ru":"Пятнадцать","sv":"Femton","nl":"Vijftien","el":"Δεκαπέντε"},
    "Sixteen":{"de":"Sechzehn","fr":"Seize","tr":"On altı","ru":"Шестнадцать","sv":"Sexton","nl":"Zestien","el":"Δεκαέξι"},
    "Seventeen":{"de":"Siebzehn","fr":"Dix-sept","tr":"On yedi","ru":"Семнадцать","sv":"Sjutton","nl":"Zeventien","el":"Δεκαεπτά"},
    "Eighteen":{"de":"Achtzehn","fr":"Dix-huit","tr":"On sekiz","ru":"Восемнадцать","sv":"Arton","nl":"Achttien","el":"Δεκαοκτώ"},
    "Nineteen":{"de":"Neunzehn","fr":"Dix-neuf","tr":"On dokuz","ru":"Девятнадцать","sv":"Nitton","nl":"Negentien","el":"Δεκαεννέα"},
    "Twenty":{"de":"Zwanzig","fr":"Vingt","tr":"Yirmi","ru":"Двадцать","sv":"Tjugo","nl":"Twintig","el":"Είκοσι"},
}

# Number prefix translations
NUMBER_PREFIX = {"ar":"العدد","en":"Number","de":"Zahl","fr":"Nombre","tr":"Sayı","ru":"Число","sv":"Nummer","nl":"Nummer","el":"Αριθμός"}

def _translate_number_name(en_name: str, lang: str) -> str:
    """Translate a number name to the target language. Falls back to Arabic."""
    if lang == "en":
        return en_name
    if lang == "ar":
        return ""  # Arabic name is in separate 'arabic' field
    return NUMBER_NAME_TRANSLATIONS.get(en_name, {}).get(lang, "")

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

# Multi-language sentence translations
SENTENCE_TRANSLATIONS = {
    "This is a book":{"de":"Das ist ein Buch","fr":"C'est un livre","tr":"Bu bir kitap","ru":"Это книга","sv":"Det här är en bok","nl":"Dit is een boek","el":"Αυτό είναι ένα βιβλίο"},
    "This is an apple":{"de":"Das ist ein Apfel","fr":"C'est une pomme","tr":"Bu bir elma","ru":"Это яблоко","sv":"Det här är ett äpple","nl":"Dit is een appel","el":"Αυτό είναι ένα μήλο"},
    "I am happy":{"de":"Ich bin glücklich","fr":"Je suis heureux","tr":"Mutluyum","ru":"Я счастлив","sv":"Jag är glad","nl":"Ik ben blij","el":"Είμαι χαρούμενος"},
    "What is your name?":{"de":"Wie heißt du?","fr":"Comment t'appelles-tu ?","tr":"Adın ne?","ru":"Как тебя зовут?","sv":"Vad heter du?","nl":"Hoe heet je?","el":"Πώς σε λένε;"},
    "My name is Ahmad":{"de":"Mein Name ist Ahmad","fr":"Je m'appelle Ahmad","tr":"Benim adım Ahmad","ru":"Меня зовут Ахмад","sv":"Jag heter Ahmad","nl":"Mijn naam is Ahmad","el":"Με λένε Αχμάντ"},
    "How old are you?":{"de":"Wie alt bist du?","fr":"Quel âge as-tu ?","tr":"Kaç yaşındasın?","ru":"Сколько тебе лет?","sv":"Hur gammal är du?","nl":"Hoe oud ben je?","el":"Πόσο χρονών είσαι;"},
    "Where is the mosque?":{"de":"Wo ist die Moschee?","fr":"Où est la mosquée ?","tr":"Cami nerede?","ru":"Где мечеть?","sv":"Var är moskén?","nl":"Waar is de moskee?","el":"Πού είναι το τζαμί;"},
    "Praise be to Allah":{"de":"Lob sei Allah","fr":"Louange à Allah","tr":"Allah'a hamd olsun","ru":"Хвала Аллаху","sv":"All lov tillkommer Allah","nl":"Lof zij Allah","el":"Δόξα στον Αλλάχ"},
    "God willing":{"de":"So Gott will","fr":"Si Dieu le veut","tr":"İnşallah","ru":"Если Аллах пожелает","sv":"Om Gud vill","nl":"Als God het wil","el":"Αν θέλει ο Θεός"},
    "What Allah willed":{"de":"Was Allah wollte","fr":"Ce qu'Allah a voulu","tr":"Maşallah","ru":"Что пожелал Аллах","sv":"Vad Allah ville","nl":"Wat Allah wilde","el":"Ό,τι θέλησε ο Αλλάχ"},
    "May Allah bless you":{"de":"Möge Allah dich segnen","fr":"Qu'Allah te bénisse","tr":"Allah seni mübarek kılsın","ru":"Да благословит тебя Аллах","sv":"Må Allah välsigna dig","nl":"Moge Allah je zegenen","el":"Να σε ευλογεί ο Αλλάχ"},
    "May Allah reward you":{"de":"Möge Allah dich belohnen","fr":"Qu'Allah te récompense","tr":"Allah seni mükâfatlandırsın","ru":"Да вознаградит тебя Аллах","sv":"Må Allah belöna dig","nl":"Moge Allah je belonen","el":"Να σε ανταμείψει ο Αλλάχ"},
    "I love my mom and dad":{"de":"Ich liebe meine Mama und meinen Papa","fr":"J'aime ma maman et mon papa","tr":"Annemi ve babamı seviyorum","ru":"Я люблю маму и папу","sv":"Jag älskar min mamma och pappa","nl":"Ik hou van mijn mama en papa","el":"Αγαπώ τη μαμά και τον μπαμπά μου"},
    "I am learning Arabic":{"de":"Ich lerne Arabisch","fr":"J'apprends l'arabe","tr":"Arapça öğreniyorum","ru":"Я изучаю арабский","sv":"Jag lär mig arabiska","nl":"Ik leer Arabisch","el":"Μαθαίνω αραβικά"},
    "The weather is beautiful today":{"de":"Das Wetter ist heute schön","fr":"Le temps est beau aujourd'hui","tr":"Bugün hava güzel","ru":"Сегодня прекрасная погода","sv":"Vädret är vackert idag","nl":"Het weer is vandaag mooi","el":"Ο καιρός είναι όμορφος σήμερα"},
}

def _translate_sentence(en_sentence: str, lang: str, ar_sentence: str = "") -> str:
    """Translate a sentence to the target language. Falls back to Arabic."""
    if lang == "en":
        return en_sentence
    if lang == "ar":
        return ar_sentence
    return SENTENCE_TRANSLATIONS.get(en_sentence, {}).get(lang, ar_sentence or en_sentence)


# ═══════════════════════════════════════════════════════════════
# CURRICULUM ENGINE - Generates structured lessons
# ═══════════════════════════════════════════════════════════════

def get_curriculum_overview(locale: str = "en") -> dict:
    """Get the full curriculum overview with stages."""
    lang = locale if locale in ["ar","en","de","fr","tr","ru","sv","nl","el"] else "ar"
    stages = []
    for s in CURRICULUM_STAGES:
        start, end = s["days"]
        stages.append({
            "id": s["id"],
            "emoji": s["emoji"],
            "color": s["color"],
            "title": s["title"].get(lang, s["title"]["ar"]),
            "description": s["desc"].get(lang, s["desc"]["ar"]),
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
    lang = locale if locale in ["ar","en","de","fr","tr","ru","sv","nl","el"] else "ar"
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
            "title": stage["title"].get(lang, stage["title"]["ar"]),
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
            lp = LETTER_PREFIX.get(lang, LETTER_PREFIX["ar"])
            lt_name = lt["name_ar"] if lang == "ar" else lt["name_en"]
            lesson["title"] = {lang: f"{lp} {lt_name}", "ar": f"حرف {lt['name_ar']}"}
            word_translated = _tw(lt["word_en"], lang, lt["word"]) if lang != "ar" else lt["word"]
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
                fp = FORMS_PREFIX.get(lang, FORMS_PREFIX["ar"])
                n1 = lt["name_ar"] if lang == "ar" else lt["name_en"]
                n2 = lt2["name_ar"] if lang == "ar" else lt2["name_en"]
                lesson["title"] = {lang: f"{fp} {n1} & {n2}" if lang != "ar" else f"أشكال {n1} و{n2}", "ar": f"أشكال {lt['name_ar']} و{lt2['name_ar']}"}
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
                lesson["title"] = {lang: REVIEW_FORMS.get(lang, REVIEW_FORMS["ar"]), "ar": REVIEW_FORMS["ar"]}
                lesson["sections"] = [{"type": "review", "emoji": "🔄", "title": t("comprehensive_review", lang),
                     "content": {"tip": t("review", lang)}}]
        else:
            review_idx = (lesson_in_stage - 42) * 2
            lt = LETTERS_28[min(review_idx, 27)]
            lesson["title"] = {lang: WRITING_PRACTICE.get(lang, WRITING_PRACTICE["ar"]), "ar": WRITING_PRACTICE["ar"]}
            word_translated = _tw(lt["word_en"], lang, lt["word"]) if lang != "ar" else lt["word"]
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
            lesson["title"] = {lang: h_name, "ar": h["name_ar"]}
            meaning_translated = _tw(h["meaning"], lang, h["meaning"]) if lang != "ar" else h["meaning"]
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
            lesson["title"] = {lang: VOWELS_REVIEW.get(lang, VOWELS_REVIEW["ar"]), "ar": VOWELS_REVIEW["ar"]}
            lesson["sections"] = [{"type": "review", "emoji": "🔄", "title": t("review", lang),
                 "content": {"items": [{"name": h["name_ar"] if lang == "ar" else h["name_en"], "symbol": h["symbol"], "sound": h["sound"]} for h in HARAKAT]}}]
    
    # ═══ STAGE 3: NUMBERS (Days 85-112) ═══
    elif stage_id == "S03":
        n_idx = lesson_in_stage % len(NUMBERS_FULL)
        n = NUMBERS_FULL[n_idx]
        n_translated = _translate_number_name(n["en"], lang) or n["ar"]
        n_prefix = NUMBER_PREFIX.get(lang, NUMBER_PREFIX["ar"])
        lesson["title"] = {lang: f"{n_prefix} {n_translated}", "ar": f"العدد {n['ar']}"}
        lesson["sections"] = [
            {"type": "learn", "emoji": "🔢", "title": t("learn", lang),
             "content": {"number": n["num"], "arabic": n["ar"], "translated": n_translated, "display": n["display"]}},
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
        word_translated = _tw(word["en"], lang, word["ar"])
        
        lesson["title"] = {lang: f"{cat_locale}: {word_translated}", "ar": f"{get_cat_name(cat, 'ar')}: {word['ar']}"}
        lesson["sections"] = [
            {"type": "learn", "emoji": word.get("emoji","📝"), "title": f"{t('new_word', lang)}: {word['ar']}",
             "content": {"arabic": word["ar"], "translated": word_translated, "emoji": word.get("emoji",""), "category": cat, "category_locale": cat_locale}},
            {"type": "listen", "emoji": "🔊", "title": t("listen_repeat", lang),
             "content": {"text": word["ar"], "tip": t("tip_say_word", lang)}},
            {"type": "quiz", "emoji": "❓", "title": t("test_yourself", lang),
             "content": {"question": t("quiz_what_in_arabic", lang, emoji=word.get('emoji', word_translated)),
                         "correct": word["ar"],
                         "options": [word["ar"]] + [w["ar"] for w in random.sample([w2 for w2 in words if w2["ar"]!=word["ar"]], min(2, len(words)-1))]}},
        ]
    
    # ═══ STAGE 5: SIMPLE SENTENCES (Days 211-266) ═══
    elif stage_id == "S05":
        s_idx = lesson_in_stage % len(SENTENCES_BASIC)
        sent = SENTENCES_BASIC[s_idx]
        sent_translated = _translate_sentence(sent["en"], lang, sent["ar"])
        lesson["title"] = {lang: sent_translated, "ar": sent["ar"]}
        lesson["sections"] = [
            {"type": "learn", "emoji": sent["emoji"], "title": t("new_sentence", lang),
             "content": {"arabic": sent["ar"], "translated": sent_translated, "emoji": sent["emoji"]}},
            {"type": "listen", "emoji": "🔊", "title": t("listen_repeat", lang),
             "content": {"text": sent["ar"], "tip": t("tip_repeat_sentence", lang)}},
            {"type": "practice", "emoji": "✍️", "title": t("write_sentence", lang),
             "content": {"tip": t("tip_write_sentence_3", lang), "sentence": sent["ar"]}},
        ]
    
    # ═══ STAGES 6-15: Use content from kids_learning.py ═══
    else:
        # For stages 6+, create dynamic content based on the stage
        lesson_prefix = t("lesson_prefix", lang, num=lesson_in_stage + 1)
        lesson["title"] = {lang: lesson_prefix, "ar": f"درس {lesson_in_stage + 1}"}
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
        w_translated = _tw(w["en"], lang, w["ar"])
        sections = [
            {"type": "read", "emoji": "📖", "title": t("read_word", lang),
             "content": {"arabic": w["ar"], "translated": w_translated, "emoji": w.get("emoji","")}},
            {"type": "listen", "emoji": "🔊", "title": t("listen_repeat", lang),
             "content": {"text": w["ar"]}},
        ]
    
    elif stage_id == "S07":  # Islamic Foundations
        topics = ["shahada","salah","zakat","sawm","hajj","wudu","iman","mosque","quran_intro","islamic_months"]
        topic = topics[lesson_idx % len(topics)]
        topic_content = {
            "shahada": {"ar":"الشهادتان: أشهد أن لا إله إلا الله وأن محمداً رسول الله","en":"The Two Testimonies: I bear witness there is no god but Allah and Muhammad is His messenger","de":"Die zwei Bekenntnisse: Ich bezeuge, dass es keinen Gott gibt außer Allah und dass Muhammad Sein Gesandter ist","fr":"Les deux témoignages: J'atteste qu'il n'y a de dieu qu'Allah et que Muhammad est Son messager","tr":"İki Şehadet: Allah'tan başka ilah olmadığına ve Muhammed'in O'nun elçisi olduğuna şehadet ederim","ru":"Два свидетельства: Свидетельствую, что нет бога, кроме Аллаха, и что Мухаммад — Его посланник","sv":"De två vittnesbörden: Jag vittnar att det inte finns någon gud utom Allah och att Muhammad är Hans sändebud","nl":"De twee getuigenissen: Ik getuig dat er geen god is dan Allah en dat Mohammed Zijn boodschapper is","el":"Οι δύο μαρτυρίες: Μαρτυρώ ότι δεν υπάρχει θεός εκτός του Αλλάχ και ότι ο Μωχάμεντ είναι ο απεσταλμένος Του"},
            "salah": {"ar":"الصلاة: خمس صلوات في اليوم - الفجر، الظهر، العصر، المغرب، العشاء","en":"Prayer: Five daily prayers - Fajr, Dhuhr, Asr, Maghrib, Isha","de":"Gebet: Fünf tägliche Gebete - Fajr, Dhuhr, Asr, Maghrib, Isha","fr":"Prière: Cinq prières quotidiennes - Fajr, Dhuhr, Asr, Maghrib, Isha","tr":"Namaz: Günde beş vakit namaz - Sabah, Öğle, İkindi, Akşam, Yatsı","ru":"Молитва: Пять ежедневных молитв - Фаджр, Зухр, Аср, Магриб, Иша","sv":"Bön: Fem dagliga böner - Fajr, Dhuhr, Asr, Maghrib, Isha","nl":"Gebed: Vijf dagelijkse gebeden - Fajr, Dhuhr, Asr, Maghrib, Isha","el":"Προσευχή: Πέντε καθημερινές προσευχές - Φατζρ, Ντουχρ, Ασρ, Μαγκρίμπ, Ίσα"},
            "zakat": {"ar":"الزكاة: إعطاء جزء من المال للفقراء","en":"Zakat: Giving a portion of wealth to the poor","de":"Zakat: Einen Teil des Vermögens den Armen geben","fr":"Zakat: Donner une partie de ses richesses aux pauvres","tr":"Zekat: Malın bir kısmını fakirlere vermek","ru":"Закят: Отдать часть имущества бедным","sv":"Zakat: Ge en del av sin rikedom till de fattiga","nl":"Zakat: Een deel van het vermogen aan de armen geven","el":"Ζακάτ: Δίνοντας μέρος του πλούτου στους φτωχούς"},
            "sawm": {"ar":"الصوم: الامتناع عن الطعام والشراب في رمضان من الفجر للمغرب","en":"Fasting: Abstaining from food and drink in Ramadan from dawn to sunset","de":"Fasten: Verzicht auf Essen und Trinken im Ramadan von der Morgendämmerung bis zum Sonnenuntergang","fr":"Jeûne: S'abstenir de manger et boire pendant le Ramadan de l'aube au coucher du soleil","tr":"Oruç: Ramazan'da fecirden akşama kadar yeme içmeden uzak durmak","ru":"Пост: Воздержание от еды и питья в Рамадан от рассвета до заката","sv":"Fasta: Avstå från mat och dryck under Ramadan från gryning till solnedgång","nl":"Vasten: Onthouding van eten en drinken in Ramadan van zonsopgang tot zonsondergang","el":"Νηστεία: Αποχή από φαγητό και ποτό στο Ραμαζάνι από την αυγή ως τη δύση"},
            "hajj": {"ar":"الحج: زيارة مكة المكرمة مرة في العمر لمن استطاع","en":"Hajj: Visiting Makkah once in a lifetime for those who can","de":"Hadsch: Einmal im Leben Makkah besuchen, für diejenigen, die es können","fr":"Hajj: Visiter La Mecque une fois dans sa vie pour ceux qui le peuvent","tr":"Hac: Gücü yetenlerin ömürde bir kez Mekke'yi ziyaret etmesi","ru":"Хадж: Посещение Мекки раз в жизни для тех, кто может","sv":"Hajj: Besöka Mecka en gång i livet för de som kan","nl":"Hadj: Mekka eenmaal in het leven bezoeken voor wie het kan","el":"Χατζ: Επίσκεψη στη Μέκκα μία φορά στη ζωή για όσους μπορούν"},
            "wudu": {"ar":"الوضوء: غسل أجزاء من الجسم استعداداً للصلاة","en":"Wudu: Washing parts of the body in preparation for prayer","de":"Wudu: Waschen von Körperteilen zur Vorbereitung auf das Gebet","fr":"Wudu: Laver certaines parties du corps en préparation de la prière","tr":"Abdest: Namaza hazırlık olarak vücudun bazı bölümlerini yıkamak","ru":"Вуду: Омовение частей тела перед молитвой","sv":"Wudu: Tvätta delar av kroppen som förberedelse för bön","nl":"Woedoe: Lichaamsdelen wassen ter voorbereiding op het gebed","el":"Γουντού: Πλύσιμο μερών του σώματος ως προετοιμασία για προσευχή"},
            "iman": {"ar":"أركان الإيمان الستة: الإيمان بالله والملائكة والكتب والرسل واليوم الآخر والقدر","en":"Six Pillars of Faith: Belief in Allah, Angels, Books, Messengers, Last Day, and Divine Decree","de":"Sechs Säulen des Glaubens: Glaube an Allah, Engel, Bücher, Gesandte, den Jüngsten Tag und die göttliche Bestimmung","fr":"Six piliers de la foi: Croyance en Allah, les Anges, les Livres, les Messagers, le Jour dernier et le Décret divin","tr":"İmanın Altı Şartı: Allah'a, meleklere, kitaplara, peygamberlere, ahiret gününe ve kadere iman","ru":"Шесть столпов веры: Вера в Аллаха, ангелов, Писания, посланников, Судный день и предопределение","sv":"Sex trosartiklar: Tro på Allah, änglarna, Böckerna, Sändebuden, den Yttersta dagen och det gudomliga dekretet","nl":"Zes geloofsartikelen: Geloof in Allah, de engelen, de Boeken, de Boodschappers, de Laatste Dag en het goddelijk besluit","el":"Έξι πυλώνες πίστης: Πίστη στον Αλλάχ, τους αγγέλους, τα Βιβλία, τους Απεσταλμένους, την Τελευταία Ημέρα και τη θεία μοίρα"},
            "mosque": {"ar":"المسجد: بيت الله حيث يصلي المسلمون ويتعلمون","en":"The Mosque: House of Allah where Muslims pray and learn","de":"Die Moschee: Haus Allahs, in dem Muslime beten und lernen","fr":"La Mosquée: Maison d'Allah où les musulmans prient et apprennent","tr":"Cami: Müslümanların namaz kıldığı ve öğrendiği Allah'ın evi","ru":"Мечеть: Дом Аллаха, где мусульмане молятся и учатся","sv":"Moskén: Allahs hus där muslimer ber och lär sig","nl":"De Moskee: Huis van Allah waar moslims bidden en leren","el":"Το Τζαμί: Οίκος του Αλλάχ όπου οι μουσουλμάνοι προσεύχονται και μαθαίνουν"},
            "quran_intro": {"ar":"القرآن الكريم: كلام الله المنزل على محمد ﷺ فيه 114 سورة","en":"The Holy Quran: Allah's word revealed to Muhammad ﷺ, containing 114 surahs","de":"Der Heilige Koran: Allahs Wort, offenbart an Muhammad ﷺ, mit 114 Suren","fr":"Le Saint Coran: Parole d'Allah révélée à Muhammad ﷺ, contenant 114 sourates","tr":"Kur'an-ı Kerim: Hz. Muhammed'e ﷺ indirilen Allah'ın sözü, 114 sure içerir","ru":"Священный Коран: Слово Аллаха, ниспосланное Мухаммаду ﷺ, содержащее 114 сур","sv":"Den heliga Koranen: Allahs ord uppenbarade för Muhammad ﷺ, innehåller 114 suror","nl":"De Heilige Koran: Allahs woord geopenbaard aan Muhammad ﷺ, bevat 114 soera's","el":"Το Ιερό Κοράνι: Ο λόγος του Αλλάχ που αποκαλύφθηκε στον Μωχάμεντ ﷺ, περιέχει 114 σούρες"},
            "islamic_months": {"ar":"الأشهر الهجرية: محرم، صفر، ربيع الأول... رمضان، شوال، ذو القعدة، ذو الحجة","en":"Islamic Months: Muharram, Safar, Rabi al-Awwal... Ramadan, Shawwal, Dhul-Qi'dah, Dhul-Hijjah","de":"Islamische Monate: Muharram, Safar, Rabi al-Awwal... Ramadan, Schawwal, Dhul-Qi'da, Dhul-Hiddscha","fr":"Mois islamiques: Muharram, Safar, Rabi al-Awwal... Ramadan, Chawwal, Dhul-Qi'da, Dhul-Hijja","tr":"Hicri Aylar: Muharrem, Safer, Rebiülevvel... Ramazan, Şevval, Zilkade, Zilhicce","ru":"Исламские месяцы: Мухаррам, Сафар, Раби аль-Авваль... Рамадан, Шавваль, Зуль-Каада, Зуль-Хиджа","sv":"Islamiska månader: Muharram, Safar, Rabi al-Awwal... Ramadan, Shawwal, Dhul-Qi'dah, Dhul-Hijjah","nl":"Islamitische maanden: Muharram, Safar, Rabi al-Awwal... Ramadan, Shawwal, Dhul-Qi'dah, Dhul-Hijjah","el":"Ισλαμικοί μήνες: Μουχάρραμ, Σαφάρ, Ράμπι αλ-Αουάλ... Ραμαζάνι, Σαουάλ, Ζουλ-Κίντα, Ζουλ-Χίτζα"},
        }
        tc = topic_content.get(topic, topic_content["shahada"])
        sections = [
            {"type": "learn", "emoji": "🤲", "title": t("learn", lang),
             "content": {"arabic": tc["ar"], "translated": tc.get(lang, tc["ar"])}},
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
                {"type": "quran", "emoji": "📖", "title": t("memorize_prefix", lang, name=surah.get('name_ar', surah['name_en'])),
                 "content": {"surah": surah.get("name_ar", surah["name_en"]), "ayah_num": ayah["num"],
                             "arabic": ayah["ar"], "translation": ayah.get(lang, ayah.get("ar", ayah["en"]))}},
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
            {"type": "dua", "emoji": d["emoji"], "title": d["title"].get(lang, d["title"]["ar"]),
             "content": {"arabic": d["ar"], "transliteration": d["transliteration"], "meaning": d.get(lang, d.get("ar", d["en"]))}},
            {"type": "memorize", "emoji": "🧠", "title": t("memorize_dua", lang),
             "content": {"tip": t("tip_repeat_dua_5", lang)}},
        ]
    
    elif stage_id == "S10":  # Hadiths
        from kids_learning import KIDS_HADITHS
        h = KIDS_HADITHS[lesson_idx % len(KIDS_HADITHS)]
        sections = [
            {"type": "hadith", "emoji": h["emoji"], "title": t("todays_hadith", lang),
             "content": {"arabic": h["ar"], "translation": h.get(lang, h.get("ar", h["en"])), "source": h["source"],
                         "lesson": h["lesson"].get(lang, h["lesson"].get("ar", h["lesson"]["en"]))}},
            {"type": "reflect", "emoji": "💭", "title": t("reflect", lang),
             "content": {"tip": t("tip_apply_hadith", lang)}},
        ]
    
    elif stage_id == "S11":  # Prophet Stories
        from kids_learning_extended import ALL_PROPHETS, get_prophet_field
        p = ALL_PROPHETS[lesson_idx % len(ALL_PROPHETS)]
        p_name = get_prophet_field(p, "name", lang) or p["name"].get(lang, p["name"].get("ar", p["name"]["en"]))
        p_title = get_prophet_field(p, "title", lang) or p["title"].get(lang, p["title"].get("ar", p["title"]["en"]))
        p_summary = get_prophet_field(p, "summary", lang)
        p_lesson = get_prophet_field(p, "lesson", lang)
        sections = [
            {"type": "story", "emoji": p["emoji"], "title": p_name,
             "content": {"name": p_name, "title": p_title,
                         "summary": p_summary,
                         "lesson": p_lesson, "quran_ref": p["quran_ref"]}},
        ]
    
    elif stage_id == "S12":  # Islamic Life
        topics = [
            {"emoji":"🌙","ar":"رمضان شهر الصيام والقرآن والعبادة. نصوم من الفجر إلى المغرب","en":"Ramadan is the month of fasting, Quran and worship. We fast from dawn to sunset","de":"Ramadan ist der Monat des Fastens, des Korans und der Anbetung. Wir fasten von der Morgendämmerung bis zum Sonnenuntergang","fr":"Le Ramadan est le mois du jeûne, du Coran et de l'adoration. Nous jeûnons de l'aube au coucher du soleil","tr":"Ramazan oruç, Kur'an ve ibadet ayıdır. Fecirden akşama kadar oruç tutarız","ru":"Рамадан — месяц поста, Корана и поклонения. Мы постимся от рассвета до заката","sv":"Ramadan är månaden för fasta, Koranen och tillbedjan. Vi fastar från gryning till solnedgång","nl":"Ramadan is de maand van vasten, Koran en aanbidding. We vasten van dageraad tot zonsondergang","el":"Το Ραμαζάνι είναι ο μήνας νηστείας, Κορανίου και λατρείας. Νηστεύουμε από την αυγή ως τη δύση"},
            {"emoji":"🕋","ar":"الحج: ملايين المسلمين يزورون مكة كل عام لأداء مناسك الحج","en":"Hajj: Millions of Muslims visit Makkah every year to perform the pilgrimage","de":"Hadsch: Millionen Muslime besuchen jedes Jahr Mekka zur Pilgerfahrt","fr":"Hajj: Des millions de musulmans visitent La Mecque chaque année pour le pèlerinage","tr":"Hac: Her yıl milyonlarca Müslüman hac için Mekke'yi ziyaret eder","ru":"Хадж: Миллионы мусульман ежегодно посещают Мекку для паломничества","sv":"Hajj: Miljontals muslimer besöker Mecka varje år för pilgrimsfärden","nl":"Hadj: Miljoenen moslims bezoeken elk jaar Mekka voor de bedevaart","el":"Χατζ: Εκατομμύρια μουσουλμάνοι επισκέπτονται τη Μέκκα κάθε χρόνο για το προσκύνημα"},
            {"emoji":"🎉","ar":"عيد الفطر: نفرح بعد رمضان، نصلي صلاة العيد ونزور الأهل","en":"Eid Al-Fitr: We celebrate after Ramadan, pray Eid prayer and visit family","de":"Eid Al-Fitr: Wir feiern nach dem Ramadan, beten das Eid-Gebet und besuchen die Familie","fr":"Aïd Al-Fitr: Nous célébrons après le Ramadan, prions la prière de l'Aïd et rendons visite à la famille","tr":"Ramazan Bayramı: Ramazan'dan sonra kutlarız, bayram namazı kılarız ve aileyi ziyaret ederiz","ru":"Ид аль-Фитр: Мы празднуем после Рамадана, совершаем праздничную молитву и навещаем семью","sv":"Eid Al-Fitr: Vi firar efter Ramadan, ber Eid-bönen och besöker familjen","nl":"Eid Al-Fitr: We vieren na Ramadan, bidden het Eid-gebed en bezoeken familie","el":"Εΐντ Αλ-Φιτρ: Γιορτάζουμε μετά το Ραμαζάνι, κάνουμε την προσευχή του Εΐντ και επισκεπτόμαστε την οικογένεια"},
            {"emoji":"🐑","ar":"عيد الأضحى: نتذكر قصة إبراهيم وإسماعيل ونضحي","en":"Eid Al-Adha: We remember Ibrahim and Ismail's story and offer sacrifice","de":"Eid Al-Adha: Wir erinnern uns an die Geschichte von Ibrahim und Ismail und opfern","fr":"Aïd Al-Adha: Nous nous souvenons de l'histoire d'Ibrahim et Ismaïl et offrons un sacrifice","tr":"Kurban Bayramı: İbrahim ve İsmail'in kıssasını hatırlarız ve kurban keseriz","ru":"Ид аль-Адха: Мы вспоминаем историю Ибрахима и Исмаила и приносим жертву","sv":"Eid Al-Adha: Vi minns berättelsen om Ibrahim och Ismail och offrar","nl":"Eid Al-Adha: We herdenken het verhaal van Ibrahim en Ismail en brengen een offer","el":"Εΐντ Αλ-Άντχα: Θυμόμαστε την ιστορία του Ιμπραχίμ και του Ισμαήλ και προσφέρουμε θυσία"},
            {"emoji":"🕌","ar":"يوم الجمعة: أفضل أيام الأسبوع، نصلي صلاة الجمعة في المسجد","en":"Friday: The best day of the week, we pray Jumu'ah prayer at the mosque","de":"Freitag: Der beste Tag der Woche, wir beten das Freitagsgebet in der Moschee","fr":"Vendredi: Le meilleur jour de la semaine, nous prions la prière du vendredi à la mosquée","tr":"Cuma: Haftanın en hayırlı günü, camide Cuma namazı kılarız","ru":"Пятница: Лучший день недели, мы совершаем пятничную молитву в мечети","sv":"Fredag: Veckans bästa dag, vi ber fredagsbönen i moskén","nl":"Vrijdag: De beste dag van de week, we bidden het vrijdaggebed in de moskee","el":"Παρασκευή: Η καλύτερη μέρα της εβδομάδας, κάνουμε την προσευχή Τζούμα στο τζαμί"},
        ]
        topic_item = topics[lesson_idx % len(topics)]
        topic_translated = topic_item.get(lang, topic_item["ar"])
        sections = [
            {"type": "learn", "emoji": topic_item["emoji"], "title": t("learn", lang),
             "content": {"arabic": topic_item["ar"], "translated": topic_translated}},
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

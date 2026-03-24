"""
Comprehensive Arabic & Quran Learning Course Engine
From Zero to C1 — The world's first gamified Islamic learning curriculum
Supports 9 languages for instructions, Arabic content for learning
"""
import random

# ═══════════════════════════════════════════════════════
# COURSE LEVELS: Foundation → A1 → A2 → B1 → B2 → C1
# ═══════════════════════════════════════════════════════

COURSE_LEVELS = [
    {"id": "foundation", "name": {"ar": "التمهيدي", "en": "Foundation", "fr": "Fondation", "de": "Grundlagen", "tr": "Temel", "ru": "Основы", "sv": "Grundnivå", "nl": "Basis", "el": "Θεμέλια"}, "emoji": "🌱", "color": "emerald", "units": 6, "desc": {"ar":"الحروف والأصوات","en":"Letters & Sounds","fr":"Lettres et sons","de":"Buchstaben & Laute","tr":"Harfler ve Sesler","ru":"Буквы и звуки","sv":"Bokstäver och ljud","nl":"Letters en klanken","el":"Γράμματα και ήχοι"}},
    {"id": "a1", "name": {"ar": "المبتدئ ١", "en": "Beginner A1", "fr": "Débutant A1", "de": "Anfänger A1", "tr": "Başlangıç A1", "ru": "Начальный A1", "sv": "Nybörjare A1", "nl": "Beginner A1", "el": "Αρχάριος A1"}, "emoji": "🌿", "color": "teal", "units": 6, "desc": {"ar":"مفردات أساسية","en":"Basic Vocabulary","fr":"Vocabulaire de base","de":"Grundwortschatz","tr":"Temel Kelimeler","ru":"Базовый словарь","sv":"Grundläggande ordförråd","nl":"Basiswoordenschat","el":"Βασικό λεξιλόγιο"}},
    {"id": "a2", "name": {"ar": "المبتدئ ٢", "en": "Beginner A2", "fr": "Débutant A2", "de": "Anfänger A2", "tr": "Başlangıç A2", "ru": "Начальный A2", "sv": "Nybörjare A2", "nl": "Beginner A2", "el": "Αρχάριος A2"}, "emoji": "🌳", "color": "cyan", "units": 6, "desc": {"ar":"جمل بسيطة","en":"Simple Sentences","fr":"Phrases simples","de":"Einfache Sätze","tr":"Basit Cümleler","ru":"Простые предложения","sv":"Enkla meningar","nl":"Eenvoudige zinnen","el":"Απλές προτάσεις"}},
    {"id": "b1", "name": {"ar": "المتوسط ١", "en": "Intermediate B1", "fr": "Intermédiaire B1", "de": "Mittelstufe B1", "tr": "Orta B1", "ru": "Средний B1", "sv": "Mellannivå B1", "nl": "Gemiddeld B1", "el": "Μεσαίο B1"}, "emoji": "🌲", "color": "blue", "units": 6, "desc": {"ar":"قواعد وقراءة","en":"Grammar & Reading","fr":"Grammaire et lecture","de":"Grammatik & Lesen","tr":"Dilbilgisi ve Okuma","ru":"Грамматика и чтение","sv":"Grammatik och läsning","nl":"Grammatica en lezen","el":"Γραμματική και ανάγνωση"}},
    {"id": "b2", "name": {"ar": "المتوسط ٢", "en": "Intermediate B2", "fr": "Intermédiaire B2", "de": "Mittelstufe B2", "tr": "Orta B2", "ru": "Средний B2", "sv": "Mellannivå B2", "nl": "Gemiddeld B2", "el": "Μεσαίο B2"}, "emoji": "🏔️", "color": "indigo", "units": 6, "desc": {"ar":"محادثة وكتابة","en":"Conversation & Writing","fr":"Conversation et écriture","de":"Konversation & Schreiben","tr":"Konuşma ve Yazma","ru":"Разговор и письмо","sv":"Konversation och skrift","nl":"Conversatie en schrijven","el":"Συνομιλία και γραφή"}},
    {"id": "c1", "name": {"ar": "المتقدم", "en": "Advanced C1", "fr": "Avancé C1", "de": "Fortgeschritten C1", "tr": "İleri C1", "ru": "Продвинутый C1", "sv": "Avancerad C1", "nl": "Gevorderd C1", "el": "Προχωρημένο C1"}, "emoji": "⭐", "color": "amber", "units": 6, "desc": {"ar":"بلاغة وتحليل","en":"Rhetoric & Analysis","fr":"Rhétorique et analyse","de":"Rhetorik & Analyse","tr":"Retorik ve Analiz","ru":"Риторика и анализ","sv":"Retorik och analys","nl":"Retoriek en analyse","el":"Ρητορική και ανάλυση"}},
]

# ═══════════════════════════════════════════════════════
# ARABIC ALPHABET — Complete with all forms
# ═══════════════════════════════════════════════════════

ARABIC_LETTERS = [
    {"letter": "ا", "name": "Alif", "sound": "a", "transliteration": {"en":"Alif","fr":"Alif","de":"Alif","tr":"Elif","ru":"Алиф","sv":"Alif","nl":"Alif","el":"Αλίφ"}, "forms": {"isolated": "ا", "initial": "ا", "medial": "ـا", "final": "ـا"}, "emoji": "🐪", "word": {"ar": "أسد", "en": "Lion"}},
    {"letter": "ب", "name": "Ba", "sound": "b", "transliteration": {"en":"Ba","fr":"Ba","de":"Ba","tr":"Be","ru":"Ба","sv":"Ba","nl":"Ba","el":"Μπα"}, "forms": {"isolated": "ب", "initial": "بـ", "medial": "ـبـ", "final": "ـب"}, "emoji": "🏠", "word": {"ar": "بيت", "en": "House"}},
    {"letter": "ت", "name": "Ta", "sound": "t", "transliteration": {"en":"Ta","fr":"Ta","de":"Ta","tr":"Te","ru":"Та","sv":"Ta","nl":"Ta","el":"Τα"}, "forms": {"isolated": "ت", "initial": "تـ", "medial": "ـتـ", "final": "ـت"}, "emoji": "🍎", "word": {"ar": "تفاحة", "en": "Apple"}},
    {"letter": "ث", "name": "Tha", "sound": "th", "transliteration": {"en":"Tha","fr":"Tha","de":"Tha","tr":"Se","ru":"Са","sv":"Tha","nl":"Tha","el":"Θα"}, "forms": {"isolated": "ث", "initial": "ثـ", "medial": "ـثـ", "final": "ـث"}, "emoji": "🦊", "word": {"ar": "ثعلب", "en": "Fox"}},
    {"letter": "ج", "name": "Jim", "sound": "j", "transliteration": {"en":"Jim","fr":"Jim","de":"Dschim","tr":"Cim","ru":"Джим","sv":"Jim","nl":"Jim","el":"Τζιμ"}, "forms": {"isolated": "ج", "initial": "جـ", "medial": "ـجـ", "final": "ـج"}, "emoji": "🐫", "word": {"ar": "جمل", "en": "Camel"}},
    {"letter": "ح", "name": "Ha", "sound": "ḥ", "transliteration": {"en":"Ha","fr":"Ha","de":"Ha","tr":"Ha","ru":"Ха","sv":"Ha","nl":"Ha","el":"Χα"}, "forms": {"isolated": "ح", "initial": "حـ", "medial": "ـحـ", "final": "ـح"}, "emoji": "🐴", "word": {"ar": "حصان", "en": "Horse"}},
    {"letter": "خ", "name": "Kha", "sound": "kh", "transliteration": {"en":"Kha","fr":"Kha","de":"Cha","tr":"Hı","ru":"Ха","sv":"Kha","nl":"Kha","el":"Χα"}, "forms": {"isolated": "خ", "initial": "خـ", "medial": "ـخـ", "final": "ـخ"}, "emoji": "🍞", "word": {"ar": "خبز", "en": "Bread"}},
    {"letter": "د", "name": "Dal", "sound": "d", "transliteration": {"en":"Dal","fr":"Dal","de":"Dal","tr":"Dal","ru":"Даль","sv":"Dal","nl":"Dal","el":"Νταλ"}, "forms": {"isolated": "د", "initial": "د", "medial": "ـد", "final": "ـد"}, "emoji": "🐻", "word": {"ar": "دب", "en": "Bear"}},
    {"letter": "ذ", "name": "Dhal", "sound": "dh", "transliteration": {"en":"Dhal","fr":"Dhal","de":"Dhal","tr":"Zel","ru":"Заль","sv":"Dhal","nl":"Dhal","el":"Ζαλ"}, "forms": {"isolated": "ذ", "initial": "ذ", "medial": "ـذ", "final": "ـذ"}, "emoji": "🐺", "word": {"ar": "ذئب", "en": "Wolf"}},
    {"letter": "ر", "name": "Ra", "sound": "r", "transliteration": {"en":"Ra","fr":"Ra","de":"Ra","tr":"Ra","ru":"Ра","sv":"Ra","nl":"Ra","el":"Ρα"}, "forms": {"isolated": "ر", "initial": "ر", "medial": "ـر", "final": "ـر"}, "emoji": "👨", "word": {"ar": "رجل", "en": "Man"}},
    {"letter": "ز", "name": "Zay", "sound": "z", "transliteration": {"en":"Zay","fr":"Zay","de":"Zay","tr":"Ze","ru":"Зай","sv":"Zay","nl":"Zay","el":"Ζάι"}, "forms": {"isolated": "ز", "initial": "ز", "medial": "ـز", "final": "ـز"}, "emoji": "🌸", "word": {"ar": "زهرة", "en": "Flower"}},
    {"letter": "س", "name": "Sin", "sound": "s", "transliteration": {"en":"Sin","fr":"Sin","de":"Sin","tr":"Sin","ru":"Син","sv":"Sin","nl":"Sin","el":"Σιν"}, "forms": {"isolated": "س", "initial": "سـ", "medial": "ـسـ", "final": "ـس"}, "emoji": "🐟", "word": {"ar": "سمكة", "en": "Fish"}},
    {"letter": "ش", "name": "Shin", "sound": "sh", "transliteration": {"en":"Shin","fr":"Shin","de":"Schin","tr":"Şın","ru":"Шин","sv":"Shin","nl":"Shin","el":"Σιν"}, "forms": {"isolated": "ش", "initial": "شـ", "medial": "ـشـ", "final": "ـش"}, "emoji": "☀️", "word": {"ar": "شمس", "en": "Sun"}},
    {"letter": "ص", "name": "Sad", "sound": "ṣ", "transliteration": {"en":"Sad","fr":"Sad","de":"Sad","tr":"Sad","ru":"Сад","sv":"Sad","nl":"Sad","el":"Σαντ"}, "forms": {"isolated": "ص", "initial": "صـ", "medial": "ـصـ", "final": "ـص"}, "emoji": "🧑", "word": {"ar": "صبي", "en": "Boy"}},
    {"letter": "ض", "name": "Dad", "sound": "ḍ", "transliteration": {"en":"Dad","fr":"Dad","de":"Dad","tr":"Dad","ru":"Дад","sv":"Dad","nl":"Dad","el":"Ντα"}, "forms": {"isolated": "ض", "initial": "ضـ", "medial": "ـضـ", "final": "ـض"}, "emoji": "🐸", "word": {"ar": "ضفدع", "en": "Frog"}},
    {"letter": "ط", "name": "Ta (emphatic)", "sound": "ṭ", "transliteration": {"en":"Ta","fr":"Ta","de":"Ta","tr":"Tı","ru":"Та","sv":"Ta","nl":"Ta","el":"Τα"}, "forms": {"isolated": "ط", "initial": "طـ", "medial": "ـطـ", "final": "ـط"}, "emoji": "🐦", "word": {"ar": "طائر", "en": "Bird"}},
    {"letter": "ظ", "name": "Dha (emphatic)", "sound": "ẓ", "transliteration": {"en":"Dha","fr":"Dha","de":"Dha","tr":"Zı","ru":"За","sv":"Dha","nl":"Dha","el":"Ζα"}, "forms": {"isolated": "ظ", "initial": "ظـ", "medial": "ـظـ", "final": "ـظ"}, "emoji": "🫎", "word": {"ar": "ظبي", "en": "Deer"}},
    {"letter": "ع", "name": "Ayn", "sound": "ʿ", "transliteration": {"en":"Ayn","fr":"Ayn","de":"Ayn","tr":"Ayn","ru":"Айн","sv":"Ayn","nl":"Ayn","el":"Αΐν"}, "forms": {"isolated": "ع", "initial": "عـ", "medial": "ـعـ", "final": "ـع"}, "emoji": "👁️", "word": {"ar": "عين", "en": "Eye"}},
    {"letter": "غ", "name": "Ghayn", "sound": "gh", "transliteration": {"en":"Ghayn","fr":"Ghayn","de":"Ghain","tr":"Gayn","ru":"Гайн","sv":"Ghayn","nl":"Ghayn","el":"Γάιν"}, "forms": {"isolated": "غ", "initial": "غـ", "medial": "ـغـ", "final": "ـغ"}, "emoji": "☁️", "word": {"ar": "غيمة", "en": "Cloud"}},
    {"letter": "ف", "name": "Fa", "sound": "f", "transliteration": {"en":"Fa","fr":"Fa","de":"Fa","tr":"Fe","ru":"Фа","sv":"Fa","nl":"Fa","el":"Φα"}, "forms": {"isolated": "ف", "initial": "فـ", "medial": "ـفـ", "final": "ـف"}, "emoji": "🐘", "word": {"ar": "فيل", "en": "Elephant"}},
    {"letter": "ق", "name": "Qaf", "sound": "q", "transliteration": {"en":"Qaf","fr":"Qaf","de":"Qaf","tr":"Kaf","ru":"Каф","sv":"Qaf","nl":"Qaf","el":"Καφ"}, "forms": {"isolated": "ق", "initial": "قـ", "medial": "ـقـ", "final": "ـق"}, "emoji": "🐈", "word": {"ar": "قطة", "en": "Cat"}},
    {"letter": "ك", "name": "Kaf", "sound": "k", "transliteration": {"en":"Kaf","fr":"Kaf","de":"Kaf","tr":"Kef","ru":"Каф","sv":"Kaf","nl":"Kaf","el":"Καφ"}, "forms": {"isolated": "ك", "initial": "كـ", "medial": "ـكـ", "final": "ـك"}, "emoji": "📖", "word": {"ar": "كتاب", "en": "Book"}},
    {"letter": "ل", "name": "Lam", "sound": "l", "transliteration": {"en":"Lam","fr":"Lam","de":"Lam","tr":"Lam","ru":"Лям","sv":"Lam","nl":"Lam","el":"Λαμ"}, "forms": {"isolated": "ل", "initial": "لـ", "medial": "ـلـ", "final": "ـل"}, "emoji": "🍋", "word": {"ar": "ليمون", "en": "Lemon"}},
    {"letter": "م", "name": "Mim", "sound": "m", "transliteration": {"en":"Mim","fr":"Mim","de":"Mim","tr":"Mim","ru":"Мим","sv":"Mim","nl":"Mim","el":"Μιμ"}, "forms": {"isolated": "م", "initial": "مـ", "medial": "ـمـ", "final": "ـم"}, "emoji": "🌙", "word": {"ar": "قمر", "en": "Moon"}},
    {"letter": "ن", "name": "Nun", "sound": "n", "transliteration": {"en":"Nun","fr":"Nun","de":"Nun","tr":"Nun","ru":"Нун","sv":"Nun","nl":"Nun","el":"Νουν"}, "forms": {"isolated": "ن", "initial": "نـ", "medial": "ـنـ", "final": "ـن"}, "emoji": "⭐", "word": {"ar": "نجمة", "en": "Star"}},
    {"letter": "ه", "name": "Ha", "sound": "h", "transliteration": {"en":"Ha","fr":"Ha","de":"Ha","tr":"He","ru":"Ха","sv":"Ha","nl":"Ha","el":"Χα"}, "forms": {"isolated": "ه", "initial": "هـ", "medial": "ـهـ", "final": "ـه"}, "emoji": "🎁", "word": {"ar": "هدية", "en": "Gift"}},
    {"letter": "و", "name": "Waw", "sound": "w", "transliteration": {"en":"Waw","fr":"Waw","de":"Waw","tr":"Vav","ru":"Вав","sv":"Waw","nl":"Waw","el":"Ουάου"}, "forms": {"isolated": "و", "initial": "و", "medial": "ـو", "final": "ـو"}, "emoji": "🌹", "word": {"ar": "وردة", "en": "Rose"}},
    {"letter": "ي", "name": "Ya", "sound": "y", "transliteration": {"en":"Ya","fr":"Ya","de":"Ya","tr":"Ye","ru":"Йа","sv":"Ya","nl":"Ya","el":"Για"}, "forms": {"isolated": "ي", "initial": "يـ", "medial": "ـيـ", "final": "ـي"}, "emoji": "✋", "word": {"ar": "يد", "en": "Hand"}},
]

# ═══════════════════════════════════════════════════════
# COURSE UNITS FOR EACH LEVEL
# ═══════════════════════════════════════════════════════

COURSE_UNITS = {
    "foundation": [
        {"id": "f1", "title": {"ar":"الحروف أ-ث","en":"Letters Alif-Tha","fr":"Lettres Alif-Tha","de":"Buchstaben Alif-Tha","tr":"Harfler Elif-Se","ru":"Буквы Алиф-Са","sv":"Bokstäver Alif-Tha","nl":"Letters Alif-Tha","el":"Γράμματα Αλίφ-Θα"}, "lessons": 7, "letters": [0,1,2,3], "type": "alphabet"},
        {"id": "f2", "title": {"ar":"الحروف ج-ذ","en":"Letters Jim-Dhal","fr":"Lettres Jim-Dhal","de":"Buchstaben Jim-Dhal","tr":"Harfler Cim-Zel","ru":"Буквы Джим-Заль","sv":"Bokstäver Jim-Dhal","nl":"Letters Jim-Dhal","el":"Γράμματα Τζιμ-Ζαλ"}, "lessons": 7, "letters": [4,5,6,7,8], "type": "alphabet"},
        {"id": "f3", "title": {"ar":"الحروف ر-ش","en":"Letters Ra-Shin","fr":"Lettres Ra-Shin","de":"Buchstaben Ra-Schin","tr":"Harfler Ra-Şın","ru":"Буквы Ра-Шин","sv":"Bokstäver Ra-Shin","nl":"Letters Ra-Shin","el":"Γράμματα Ρα-Σιν"}, "lessons": 7, "letters": [9,10,11,12], "type": "alphabet"},
        {"id": "f4", "title": {"ar":"الحروف ص-غ","en":"Letters Sad-Ghayn","fr":"Lettres Sad-Ghayn","de":"Buchstaben Sad-Ghain","tr":"Harfler Sad-Gayn","ru":"Буквы Сад-Гайн","sv":"Bokstäver Sad-Ghayn","nl":"Letters Sad-Ghayn","el":"Γράμματα Σαντ-Γάιν"}, "lessons": 7, "letters": [13,14,15,16,17,18], "type": "alphabet"},
        {"id": "f5", "title": {"ar":"الحروف ف-ي","en":"Letters Fa-Ya","fr":"Lettres Fa-Ya","de":"Buchstaben Fa-Ya","tr":"Harfler Fe-Ye","ru":"Буквы Фа-Йа","sv":"Bokstäver Fa-Ya","nl":"Letters Fa-Ya","el":"Γράμματα Φα-Για"}, "lessons": 7, "letters": [19,20,21,22,23,24,25,26,27], "type": "alphabet"},
        {"id": "f6", "title": {"ar":"الحركات والتشكيل","en":"Vowel Marks","fr":"Marques de voyelles","de":"Vokalzeichen","tr":"Hareke İşaretleri","ru":"Огласовки","sv":"Vokalmarkeringar","nl":"Klinkermarkeringen","el":"Σημάδια φωνηέντων"}, "lessons": 5, "type": "vowels"},
    ],
    "a1": [
        {"id": "a1_1", "title": {"ar":"التحيات والتعارف","en":"Greetings & Introductions","fr":"Salutations","de":"Begrüßungen","tr":"Selamlaşma","ru":"Приветствия","sv":"Hälsningar","nl":"Begroetingen","el":"Χαιρετισμοί"}, "lessons": 6, "type": "vocabulary"},
        {"id": "a1_2", "title": {"ar":"العائلة","en":"Family Members","fr":"La famille","de":"Familie","tr":"Aile","ru":"Семья","sv":"Familj","nl":"Familie","el":"Οικογένεια"}, "lessons": 6, "type": "vocabulary"},
        {"id": "a1_3", "title": {"ar":"الألوان والأرقام","en":"Colors & Numbers","fr":"Couleurs et chiffres","de":"Farben & Zahlen","tr":"Renkler ve Sayılar","ru":"Цвета и числа","sv":"Färger och siffror","nl":"Kleuren en cijfers","el":"Χρώματα και αριθμοί"}, "lessons": 6, "type": "vocabulary"},
        {"id": "a1_4", "title": {"ar":"الحيوانات","en":"Animals","fr":"Les animaux","de":"Tiere","tr":"Hayvanlar","ru":"Животные","sv":"Djur","nl":"Dieren","el":"Ζώα"}, "lessons": 6, "type": "vocabulary"},
        {"id": "a1_5", "title": {"ar":"سورة الفاتحة","en":"Surah Al-Fatiha","fr":"Sourate Al-Fatiha","de":"Sure Al-Fatiha","tr":"Fatiha Suresi","ru":"Сура Аль-Фатиха","sv":"Surah Al-Fatiha","nl":"Soera Al-Fatiha","el":"Σούρα Αλ-Φάτιχα"}, "lessons": 5, "type": "quran"},
        {"id": "a1_6", "title": {"ar":"أدعية يومية","en":"Daily Duas","fr":"Douas quotidiennes","de":"Tägliche Duas","tr":"Günlük Dualar","ru":"Ежедневные дуа","sv":"Dagliga duas","nl":"Dagelijkse doea's","el":"Καθημερινά ντουά"}, "lessons": 5, "type": "dua"},
    ],
    "a2": [
        {"id": "a2_1", "title": {"ar":"جسم الإنسان","en":"Human Body","fr":"Le corps humain","de":"Der menschliche Körper","tr":"İnsan Vücudu","ru":"Тело человека","sv":"Människokroppen","nl":"Menselijk lichaam","el":"Ανθρώπινο σώμα"}, "lessons": 6, "type": "vocabulary"},
        {"id": "a2_2", "title": {"ar":"الطعام والشراب","en":"Food & Drinks","fr":"Nourriture et boissons","de":"Essen & Trinken","tr":"Yiyecek ve İçecek","ru":"Еда и напитки","sv":"Mat och dryck","nl":"Eten en drinken","el":"Φαγητό και ποτά"}, "lessons": 6, "type": "vocabulary"},
        {"id": "a2_3", "title": {"ar":"الأفعال الأساسية","en":"Basic Verbs","fr":"Verbes de base","de":"Grundverben","tr":"Temel Fiiller","ru":"Основные глаголы","sv":"Grundläggande verb","nl":"Basiswerkwoorden","el":"Βασικά ρήματα"}, "lessons": 6, "type": "grammar"},
        {"id": "a2_4", "title": {"ar":"بناء الجمل","en":"Sentence Building","fr":"Construction de phrases","de":"Satzbau","tr":"Cümle Kurma","ru":"Построение предложений","sv":"Meningsbyggnad","nl":"Zinnen bouwen","el":"Δόμηση προτάσεων"}, "lessons": 6, "type": "grammar"},
        {"id": "a2_5", "title": {"ar":"سورة الإخلاص والفلق والناس","en":"Surahs Ikhlas, Falaq, Nas","fr":"Sourates Ikhlas, Falaq, Nas","de":"Suren Ikhlas, Falaq, Nas","tr":"İhlas, Felak, Nas Sureleri","ru":"Суры Ихлас, Фалак, Нас","sv":"Suror Ikhlas, Falaq, Nas","nl":"Soera's Ikhlas, Falaq, Nas","el":"Σούρες Ιχλάς, Φαλάκ, Νας"}, "lessons": 5, "type": "quran"},
        {"id": "a2_6", "title": {"ar":"أركان الإسلام","en":"Pillars of Islam","fr":"Piliers de l'Islam","de":"Säulen des Islam","tr":"İslam'ın Şartları","ru":"Столпы Ислама","sv":"Islams pelare","nl":"Zuilen van de Islam","el":"Πυλώνες του Ισλάμ"}, "lessons": 5, "type": "islam"},
    ],
    "b1": [
        {"id": "b1_1", "title": {"ar":"الأفعال: ماضي ومضارع","en":"Verbs: Past & Present","fr":"Verbes: passé et présent","de":"Verben: Vergangenheit & Gegenwart","tr":"Fiiller: Geçmiş ve Şimdiki","ru":"Глаголы: прошедшее и настоящее","sv":"Verb: dåtid och nutid","nl":"Werkwoorden: verleden en heden","el":"Ρήματα: παρελθόν και παρόν"}, "lessons": 6, "type": "grammar"},
        {"id": "b1_2", "title": {"ar":"الصفات والموصوف","en":"Adjectives & Descriptions","fr":"Adjectifs et descriptions","de":"Adjektive & Beschreibungen","tr":"Sıfatlar ve Tanımlamalar","ru":"Прилагательные и описания","sv":"Adjektiv och beskrivningar","nl":"Bijvoeglijke naamwoorden","el":"Επίθετα και περιγραφές"}, "lessons": 6, "type": "grammar"},
        {"id": "b1_3", "title": {"ar":"قراءة قصص قصيرة","en":"Reading Short Stories","fr":"Lire des histoires courtes","de":"Kurzgeschichten lesen","tr":"Kısa Hikayeler Okuma","ru":"Чтение коротких рассказов","sv":"Läsa korta berättelser","nl":"Korte verhalen lezen","el":"Ανάγνωση σύντομων ιστοριών"}, "lessons": 6, "type": "reading"},
        {"id": "b1_4", "title": {"ar":"المحادثة اليومية","en":"Daily Conversation","fr":"Conversation quotidienne","de":"Tägliche Konversation","tr":"Günlük Konuşma","ru":"Повседневный разговор","sv":"Daglig konversation","nl":"Dagelijks gesprek","el":"Καθημερινή συνομιλία"}, "lessons": 6, "type": "conversation"},
        {"id": "b1_5", "title": {"ar":"جزء عم","en":"Juz Amma","fr":"Juz Amma","de":"Juz Amma","tr":"Amme Cüzü","ru":"Джуз Амма","sv":"Juz Amma","nl":"Juz Amma","el":"Τζουζ Άμμα"}, "lessons": 6, "type": "quran"},
        {"id": "b1_6", "title": {"ar":"قصص الأنبياء","en":"Stories of Prophets","fr":"Histoires des prophètes","de":"Prophetengeschichten","tr":"Peygamber Kıssaları","ru":"Истории пророков","sv":"Profeternas berättelser","nl":"Profetenverhalen","el":"Ιστορίες προφητών"}, "lessons": 6, "type": "islam"},
    ],
    "b2": [
        {"id": "b2_1", "title": {"ar":"الأفعال المتقدمة","en":"Advanced Verbs","fr":"Verbes avancés","de":"Fortgeschrittene Verben","tr":"İleri Fiiller","ru":"Продвинутые глаголы","sv":"Avancerade verb","nl":"Gevorderde werkwoorden","el":"Προχωρημένα ρήματα"}, "lessons": 6, "type": "grammar"},
        {"id": "b2_2", "title": {"ar":"كتابة الفقرات","en":"Paragraph Writing","fr":"Écriture de paragraphes","de":"Absätze schreiben","tr":"Paragraf Yazma","ru":"Написание абзацев","sv":"Styckesskrivning","nl":"Alinea's schrijven","el":"Γραφή παραγράφων"}, "lessons": 6, "type": "writing"},
        {"id": "b2_3", "title": {"ar":"النقاش والحوار","en":"Discussion & Dialogue","fr":"Discussion et dialogue","de":"Diskussion & Dialog","tr":"Tartışma ve Diyalog","ru":"Дискуссия и диалог","sv":"Diskussion och dialog","nl":"Discussie en dialoog","el":"Συζήτηση και διάλογος"}, "lessons": 6, "type": "conversation"},
        {"id": "b2_4", "title": {"ar":"قراءة النصوص","en":"Text Comprehension","fr":"Compréhension de texte","de":"Textverständnis","tr":"Metin Anlama","ru":"Понимание текста","sv":"Textförståelse","nl":"Tekstbegrip","el":"Κατανόηση κειμένου"}, "lessons": 6, "type": "reading"},
        {"id": "b2_5", "title": {"ar":"تفسير سور مختارة","en":"Selected Surahs Tafsir","fr":"Tafsir de sourates choisies","de":"Tafsir ausgewählter Suren","tr":"Seçilmiş Surelerin Tefsiri","ru":"Тафсир избранных сур","sv":"Tafsir av utvalda suror","nl":"Tafsir van geselecteerde soera's","el":"Ταφσίρ επιλεγμένων σούρων"}, "lessons": 6, "type": "quran"},
        {"id": "b2_6", "title": {"ar":"الفقه الإسلامي المبسط","en":"Simplified Islamic Jurisprudence","fr":"Jurisprudence islamique simplifiée","de":"Vereinfachte islamische Rechtswissenschaft","tr":"Basitleştirilmiş İslam Hukuku","ru":"Упрощенное исламское право","sv":"Förenklad islamisk rättslära","nl":"Vereenvoudigd islamitisch recht","el":"Απλοποιημένη ισλαμική νομολογία"}, "lessons": 6, "type": "islam"},
    ],
    "c1": [
        {"id": "c1_1", "title": {"ar":"البلاغة العربية","en":"Arabic Rhetoric","fr":"Rhétorique arabe","de":"Arabische Rhetorik","tr":"Arap Retoriği","ru":"Арабская риторика","sv":"Arabisk retorik","nl":"Arabische retoriek","el":"Αραβική ρητορική"}, "lessons": 6, "type": "advanced"},
        {"id": "c1_2", "title": {"ar":"تحليل النصوص الأدبية","en":"Literary Text Analysis","fr":"Analyse de textes littéraires","de":"Literarische Textanalyse","tr":"Edebi Metin Analizi","ru":"Анализ литературных текстов","sv":"Litterär textanalys","nl":"Literaire tekstanalyse","el":"Ανάλυση λογοτεχνικών κειμένων"}, "lessons": 6, "type": "advanced"},
        {"id": "c1_3", "title": {"ar":"الكتابة الإبداعية","en":"Creative Writing","fr":"Écriture créative","de":"Kreatives Schreiben","tr":"Yaratıcı Yazma","ru":"Творческое письмо","sv":"Kreativt skrivande","nl":"Creatief schrijven","el":"Δημιουργική γραφή"}, "lessons": 6, "type": "writing"},
        {"id": "c1_4", "title": {"ar":"المناظرة والخطابة","en":"Debate & Public Speaking","fr":"Débat et discours public","de":"Debatte & Rhetorik","tr":"Münazara ve Hitabet","ru":"Дебаты и публичные выступления","sv":"Debatt och talekonst","nl":"Debat en spreken in het openbaar","el":"Αντιπαράθεση και δημόσια ομιλία"}, "lessons": 6, "type": "advanced"},
        {"id": "c1_5", "title": {"ar":"إعراب القرآن الكريم","en":"Quranic Arabic Grammar","fr":"Grammaire arabe coranique","de":"Koranische arabische Grammatik","tr":"Kur'an Arapça Grameri","ru":"Грамматика коранического арабского","sv":"Koranisk arabisk grammatik","nl":"Koranische Arabische grammatica","el":"Κορανική αραβική γραμματική"}, "lessons": 6, "type": "quran"},
        {"id": "c1_6", "title": {"ar":"مقاصد الشريعة","en":"Purposes of Islamic Law","fr":"Objectifs de la loi islamique","de":"Ziele des islamischen Rechts","tr":"İslam Hukukunun Amaçları","ru":"Цели исламского права","sv":"Islamisk lags syften","nl":"Doelen van islamitisch recht","el":"Σκοποί του ισλαμικού δικαίου"}, "lessons": 6, "type": "islam"},
    ],
}


def get_course_overview(locale: str = "en"):
    """Get the full course structure overview."""
    lang = locale if locale != "de-AT" else "de"
    levels = []
    for lv in COURSE_LEVELS:
        units = COURSE_UNITS.get(lv["id"], [])
        total_lessons = sum(u["lessons"] for u in units)
        levels.append({
            "id": lv["id"],
            "name": lv["name"].get(lang, lv["name"]["en"]),
            "emoji": lv["emoji"],
            "color": lv["color"],
            "desc": lv["desc"].get(lang, lv["desc"]["en"]),
            "units_count": len(units),
            "total_lessons": total_lessons,
            "units": [
                {
                    "id": u["id"],
                    "title": u["title"].get(lang, u["title"]["en"]),
                    "lessons": u["lessons"],
                    "type": u.get("type", "general"),
                }
                for u in units
            ],
        })
    return levels


def get_alphabet_lesson(letter_index: int, locale: str = "en"):
    """Get a specific Arabic letter lesson with all forms and examples."""
    if letter_index < 0 or letter_index >= len(ARABIC_LETTERS):
        return None
    lang = locale if locale != "de-AT" else "de"
    lt = ARABIC_LETTERS[letter_index]
    return {
        "letter": lt["letter"],
        "name": lt["transliteration"].get(lang, lt["name"]),
        "sound": lt["sound"],
        "forms": lt["forms"],
        "emoji": lt["emoji"],
        "example_word": lt["word"]["ar"],
        "example_translation": lt["word"]["en"],
        "index": letter_index,
        "total": len(ARABIC_LETTERS),
    }


def generate_letter_games(letter_index: int, locale: str = "en"):
    """Generate interactive games for learning a specific Arabic letter."""
    if letter_index < 0 or letter_index >= len(ARABIC_LETTERS):
        return []
    lang = locale if locale != "de-AT" else "de"
    lt = ARABIC_LETTERS[letter_index]
    random.seed(letter_index)

    games = []

    # Game 1: Letter Recognition Quiz
    other_indices = [i for i in range(len(ARABIC_LETTERS)) if i != letter_index]
    wrong = random.sample(other_indices, 3)
    options = [lt["letter"]] + [ARABIC_LETTERS[i]["letter"] for i in wrong]
    random.shuffle(options)
    correct_idx = options.index(lt["letter"])
    q_texts = {
        "ar": f"أين حرف {lt['name']}؟",
        "en": f"Where is the letter {lt['transliteration'].get('en', lt['name'])}?",
        "fr": f"Où est la lettre {lt['transliteration'].get('fr', lt['name'])} ?",
        "de": f"Wo ist der Buchstabe {lt['transliteration'].get('de', lt['name'])}?",
        "tr": f"{lt['transliteration'].get('tr', lt['name'])} harfi nerede?",
        "ru": f"Где буква {lt['transliteration'].get('ru', lt['name'])}?",
        "sv": f"Var är bokstaven {lt['transliteration'].get('sv', lt['name'])}?",
        "nl": f"Waar is de letter {lt['transliteration'].get('nl', lt['name'])}?",
        "el": f"Πού είναι το γράμμα {lt['transliteration'].get('el', lt['name'])};",
    }
    games.append({
        "type": "quiz",
        "id": f"letter_quiz_{letter_index}",
        "title": q_texts.get(lang, q_texts["en"]),
        "question": q_texts.get(lang, q_texts["en"]),
        "options": options,
        "correct_index": correct_idx,
        "xp": 10,
        "emoji": "🔤",
    })

    # Game 2: Letter Forms Memory Match
    form_names = {"ar": ["معزول", "بداية", "وسط", "نهاية"], "en": ["Isolated", "Initial", "Medial", "Final"]}
    forms = list(lt["forms"].values())
    cards = []
    labels = form_names.get(lang, form_names["en"])
    for i, (form, label) in enumerate(zip(forms, labels)):
        cards.append({"id": f"f{i}", "content": form, "pair_id": f"p{i}", "type": "emoji"})
        cards.append({"id": f"l{i}", "content": label, "pair_id": f"p{i}", "type": "text"})
    random.shuffle(cards)
    games.append({
        "type": "memory",
        "id": f"letter_memory_{letter_index}",
        "title": {"ar": "طابق أشكال الحرف", "en": "Match Letter Forms", "fr": "Associer les formes", "de": "Formen zuordnen", "tr": "Harf Formlarını Eşleştir", "ru": "Сопоставь формы", "sv": "Matcha bokstavsformer", "nl": "Vormen matchen", "el": "Ταίριαξε τις μορφές"}.get(lang, "Match Letter Forms"),
        "cards": cards,
        "total_pairs": 4,
        "xp": 15,
        "emoji": "🎴",
    })

    # Game 3: Word Recognition
    word_q = {
        "ar": f"أي كلمة تبدأ بحرف {lt['letter']}؟",
        "en": f"Which word starts with {lt['transliteration'].get('en', lt['name'])}?",
        "fr": f"Quel mot commence par {lt['transliteration'].get('fr', lt['name'])} ?",
        "de": f"Welches Wort beginnt mit {lt['transliteration'].get('de', lt['name'])}?",
        "tr": f"Hangi kelime {lt['transliteration'].get('tr', lt['name'])} ile başlar?",
        "ru": f"Какое слово начинается на {lt['transliteration'].get('ru', lt['name'])}?",
        "sv": f"Vilket ord börjar med {lt['transliteration'].get('sv', lt['name'])}?",
        "nl": f"Welk woord begint met {lt['transliteration'].get('nl', lt['name'])}?",
        "el": f"Ποια λέξη ξεκινά με {lt['transliteration'].get('el', lt['name'])};",
    }
    word_options = [lt["word"]["ar"]] + [ARABIC_LETTERS[i]["word"]["ar"] for i in random.sample(other_indices, 3)]
    random.shuffle(word_options)
    games.append({
        "type": "quiz",
        "id": f"letter_word_{letter_index}",
        "title": word_q.get(lang, word_q["en"]),
        "question": word_q.get(lang, word_q["en"]),
        "options": [f"{w} {ARABIC_LETTERS[[x['word']['ar'] for x in ARABIC_LETTERS].index(w)]['emoji']}" for w in word_options],
        "correct_index": word_options.index(lt["word"]["ar"]),
        "xp": 10,
        "emoji": "📝",
    })

    return games

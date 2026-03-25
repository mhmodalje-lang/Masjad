"""
Noor Academy V2 — Modern Islamic Education Platform (2026)
==========================================================
5 Learning Tracks with Modern Teaching Methods:
  Track 1: القاعدة النورانية — Nooraniya (Learn to Read Quran from Zero)
  Track 2: العقيدة — Aqeedah (Islamic Belief System)
  Track 3: الفقه المبسّط — Fiqh (Islamic Jurisprudence for Kids)
  Track 4: السيرة النبوية — Seerah (Prophet Muhammad's Biography)
  Track 5: الآداب الإسلامية — Adab (Islamic Manners & Ethics)

Teaching Methods (2026):
  - Micro-Learning: 5-minute bite-sized lessons
  - Gamification: XP, badges, streaks, levels
  - Spaced Repetition: Review at optimal intervals
  - Interactive Quizzes: Multiple formats
  - Visual Learning: Color-coded, emoji-rich
  - Story-Based: Learn through narratives
  - Audio Cues: Listen & repeat markers
  - Progress Tracking: Clear advancement

ALL content in 9 languages. NEVER show Arabic to non-Arabic users.
"""

# ═══════════════════════════════════════════════════════════════
# ACADEMY TRACKS OVERVIEW
# ═══════════════════════════════════════════════════════════════

ACADEMY_TRACKS = [
    {
        "id": "nooraniya",
        "emoji": "📖",
        "color": "#7C3AED",
        "icon": "book-open",
        "order": 1,
        "title": {
            "ar": "القاعدة النورانية", "en": "Nooraniya — Learn to Read Quran",
            "de": "Nooraniya — Koran lesen lernen", "fr": "Nooraniya — Apprendre à lire le Coran",
            "tr": "Kaide-i Nuraniye — Kur'an Okumayı Öğren", "ru": "Нураний — Учимся читать Коран",
            "sv": "Nooraniya — Lär dig läsa Koranen", "nl": "Nooraniya — Leer de Koran lezen",
            "el": "Νουράνιγια — Μάθε να διαβάζεις το Κοράνι",
        },
        "desc": {
            "ar": "من الصفر حتى قراءة القرآن بطلاقة — خطوة بخطوة",
            "en": "From zero to fluent Quran reading — step by step",
            "de": "Von Null bis zum fließenden Koranlesen — Schritt für Schritt",
            "fr": "De zéro à la lecture fluide du Coran — étape par étape",
            "tr": "Sıfırdan akıcı Kur'an okumaya — adım adım",
            "ru": "От нуля до свободного чтения Корана — шаг за шагом",
            "sv": "Från noll till flytande Koranläsning — steg för steg",
            "nl": "Van nul tot vloeiend Koran lezen — stap voor stap",
            "el": "Από το μηδέν ως την ευχερή ανάγνωση Κορανίου",
        },
        "total_levels": 7,
        "total_lessons": 70,
        "age_range": "4-16",
        "method": "nooraniya",
    },
    {
        "id": "aqeedah",
        "emoji": "🤲",
        "color": "#059669",
        "icon": "heart",
        "order": 2,
        "title": {
            "ar": "العقيدة الإسلامية", "en": "Islamic Belief (Aqeedah)",
            "de": "Islamischer Glaube (Aqeedah)", "fr": "Croyance islamique (Aqeedah)",
            "tr": "İslam Akaidi", "ru": "Исламское вероучение (Акида)",
            "sv": "Islamisk tro (Aqeedah)", "nl": "Islamitisch geloof (Aqeedah)",
            "el": "Ισλαμική πίστη (Ακίντα)",
        },
        "desc": {
            "ar": "التوحيد وأسماء الله الحسنى وأركان الإيمان",
            "en": "Tawheed, 99 Names of Allah & Pillars of Faith",
            "de": "Tawheed, 99 Namen Allahs & Säulen des Glaubens",
            "fr": "Tawheed, 99 Noms d'Allah & Piliers de la Foi",
            "tr": "Tevhid, Esmaül Hüsna ve İmanın Şartları",
            "ru": "Таухид, 99 Имён Аллаха и Столпы Веры",
            "sv": "Tawheed, 99 namn på Allah & Trosartiklar",
            "nl": "Tawheed, 99 Namen van Allah & Geloofsartikelen",
            "el": "Ταουχίντ, 99 Ονόματα του Αλλάχ & Πυλώνες Πίστης",
        },
        "total_levels": 5,
        "total_lessons": 50,
        "age_range": "5-16",
        "method": "conceptual",
    },
    {
        "id": "fiqh",
        "emoji": "⚖️",
        "color": "#0EA5E9",
        "icon": "scale",
        "order": 3,
        "title": {
            "ar": "الفقه المبسّط", "en": "Islamic Jurisprudence (Fiqh)",
            "de": "Islamische Rechtslehre (Fiqh)", "fr": "Jurisprudence islamique (Fiqh)",
            "tr": "Temel Fıkıh", "ru": "Исламское право (Фикх)",
            "sv": "Islamisk rättslära (Fiqh)", "nl": "Islamitische jurisprudentie (Fiqh)",
            "el": "Ισλαμική νομολογία (Φικχ)",
        },
        "desc": {
            "ar": "الطهارة والصلاة والصيام والزكاة — بالتفصيل المبسّط",
            "en": "Purification, Prayer, Fasting & Zakat — simplified details",
            "de": "Reinigung, Gebet, Fasten & Zakat — vereinfacht",
            "fr": "Purification, Prière, Jeûne & Zakat — simplifié",
            "tr": "Taharet, Namaz, Oruç ve Zekât — basitleştirilmiş",
            "ru": "Очищение, Молитва, Пост и Закят — упрощённо",
            "sv": "Rening, Bön, Fasta & Zakat — förenklat",
            "nl": "Reiniging, Gebed, Vasten & Zakat — vereenvoudigd",
            "el": "Κάθαρση, Προσευχή, Νηστεία & Ζακάτ — απλοποιημένο",
        },
        "total_levels": 4,
        "total_lessons": 40,
        "age_range": "6-16",
        "method": "practical",
    },
    {
        "id": "seerah",
        "emoji": "🕌",
        "color": "#D97706",
        "icon": "mosque",
        "order": 4,
        "title": {
            "ar": "السيرة النبوية", "en": "Prophet's Biography (Seerah)",
            "de": "Prophetenbiographie (Seerah)", "fr": "Biographie du Prophète (Seerah)",
            "tr": "Siyer-i Nebi", "ru": "Жизнеописание Пророка (Сира)",
            "sv": "Profetens biografi (Seerah)", "nl": "Biografie van de Profeet (Seerah)",
            "el": "Βιογραφία του Προφήτη (Σίρα)",
        },
        "desc": {
            "ar": "حياة النبي محمد ﷺ من الميلاد إلى الوفاة — بأسلوب قصصي",
            "en": "Life of Prophet Muhammad ﷺ from birth to passing — story-based",
            "de": "Leben des Propheten Muhammad ﷺ — als Geschichte erzählt",
            "fr": "Vie du Prophète Muhammad ﷺ — racontée en histoires",
            "tr": "Hz. Muhammed'in ﷺ hayatı — hikâye anlatımıyla",
            "ru": "Жизнь Пророка Мухаммада ﷺ — в формате рассказов",
            "sv": "Profeten Muhammads ﷺ liv — berättat som historia",
            "nl": "Leven van Profeet Muhammad ﷺ — als verhaal verteld",
            "el": "Ζωή του Προφήτη Μωχάμεντ ﷺ — σε μορφή ιστορίας",
        },
        "total_levels": 6,
        "total_lessons": 60,
        "age_range": "5-16",
        "method": "story-based",
    },
    {
        "id": "adab",
        "emoji": "🌟",
        "color": "#EC4899",
        "icon": "star",
        "order": 5,
        "title": {
            "ar": "الآداب الإسلامية", "en": "Islamic Manners (Adab)",
            "de": "Islamische Umgangsformen (Adab)", "fr": "Bonnes manières islamiques (Adab)",
            "tr": "İslami Adap", "ru": "Исламские манеры (Адаб)",
            "sv": "Islamiska seder (Adab)", "nl": "Islamitische manieren (Adab)",
            "el": "Ισλαμικοί τρόποι (Αντάμπ)",
        },
        "desc": {
            "ar": "آداب الطعام والمسجد والنوم والتحية وأكثر — 20 أدب أساسي",
            "en": "Eating, mosque, sleeping, greeting etiquette & more — 20 essential manners",
            "de": "Ess-, Moschee-, Schlaf-, Begrüßungsetikette & mehr — 20 Grundregeln",
            "fr": "Étiquette du repas, mosquée, sommeil, salutations & plus — 20 règles",
            "tr": "Yemek, cami, uyku, selamlama adabı ve daha fazlası — 20 temel adap",
            "ru": "Этикет еды, мечети, сна, приветствия и др. — 20 основных правил",
            "sv": "Mat-, moské-, sömn-, hälsningsetikett & mer — 20 grundregler",
            "nl": "Eet-, moskee-, slaap-, begroetingsetiquette & meer — 20 basisregels",
            "el": "Εθιμοτυπία φαγητού, τζαμιού, ύπνου, χαιρετισμού — 20 βασικοί κανόνες",
        },
        "total_levels": 4,
        "total_lessons": 20,
        "age_range": "4-16",
        "method": "practice-based",
    },
]

# ═══════════════════════════════════════════════════════════════
# TRACK 1: NOORANIYA — القاعدة النورانية
# ═══════════════════════════════════════════════════════════════

NOORANIYA_LEVELS = [
    {
        "level": 1, "emoji": "🔤", "color": "#3B82F6",
        "title": {"ar": "الحروف المفردة", "en": "Individual Letters", "de": "Einzelne Buchstaben", "fr": "Lettres individuelles", "tr": "Tek Harfler", "ru": "Отдельные буквы", "sv": "Enskilda bokstäver", "nl": "Individuele letters", "el": "Μεμονωμένα γράμματα"},
        "desc": {"ar": "تعرّف على الحروف العربية الـ 28 بأصواتها الصحيحة من مخارجها", "en": "Learn all 28 Arabic letters with correct pronunciation from their articulation points", "de": "Lerne alle 28 Buchstaben mit korrekter Aussprache", "fr": "Apprenez les 28 lettres avec la bonne prononciation", "tr": "28 harfi doğru telaffuzlarıyla öğrenin", "ru": "Изучите 28 букв с правильным произношением", "sv": "Lär dig alla 28 bokstäver med korrekt uttal", "nl": "Leer alle 28 letters met correcte uitspraak", "el": "Μάθε τα 28 γράμματα με σωστή προφορά"},
        "lessons": 10,
        "skills": ["letter_recognition", "pronunciation", "writing"],
    },
    {
        "level": 2, "emoji": "🔗", "color": "#8B5CF6",
        "title": {"ar": "الحروف المركّبة", "en": "Letter Combinations", "de": "Buchstabenkombinationen", "fr": "Combinaisons de lettres", "tr": "Harf Birleşimleri", "ru": "Сочетания букв", "sv": "Bokstavskombinationer", "nl": "Lettercombinaties", "el": "Συνδυασμοί γραμμάτων"},
        "desc": {"ar": "تعلّم كيف تتصل الحروف ببعضها: بداية، وسط، نهاية", "en": "Learn how letters connect: beginning, middle, end positions", "de": "Lerne wie Buchstaben sich verbinden: Anfang, Mitte, Ende", "fr": "Apprenez comment les lettres se connectent: début, milieu, fin", "tr": "Harflerin nasıl bağlandığını öğrenin: baş, orta, son", "ru": "Узнайте как буквы соединяются: начало, середина, конец", "sv": "Lär dig hur bokstäver kopplas: början, mitten, slut", "nl": "Leer hoe letters verbinden: begin, midden, eind", "el": "Μάθε πώς συνδέονται τα γράμματα: αρχή, μέση, τέλος"},
        "lessons": 10,
        "skills": ["connecting_letters", "word_formation", "reading_flow"],
    },
    {
        "level": 3, "emoji": "🎵", "color": "#06B6D4",
        "title": {"ar": "الحركات القصيرة والطويلة", "en": "Short & Long Vowels", "de": "Kurze & Lange Vokale", "fr": "Voyelles courtes & longues", "tr": "Kısa ve Uzun Sesli Harfler", "ru": "Краткие и долгие гласные", "sv": "Korta & långa vokaler", "nl": "Korte & lange klinkers", "el": "Βραχέα & μακρά φωνήεντα"},
        "desc": {"ar": "الفتحة والكسرة والضمة + حروف المد: ا، و، ي", "en": "Fatha, Kasra, Damma + Madd letters: Alif, Waw, Ya", "de": "Fatha, Kasra, Damma + Dehnungsbuchstaben", "fr": "Fatha, Kasra, Damma + lettres d'allongement", "tr": "Fatha, Kasra, Damma + Med harfleri: Elif, Vav, Ya", "ru": "Фатха, Касра, Дамма + буквы удлинения", "sv": "Fatha, Kasra, Damma + förlängningsbokstäver", "nl": "Fatha, Kasra, Damma + verlengingsletters", "el": "Φάθα, Κάσρα, Ντάμμα + γράμματα επιμήκυνσης"},
        "lessons": 10,
        "skills": ["harakat", "madd", "rhythm"],
    },
    {
        "level": 4, "emoji": "⚡", "color": "#F59E0B",
        "title": {"ar": "التنوين والشدة والسكون", "en": "Tanween, Shadda & Sukun", "de": "Tanween, Shadda & Sukun", "fr": "Tanween, Shadda & Sukun", "tr": "Tenvin, Şedde ve Sükûn", "ru": "Танвин, Шадда и Сукун", "sv": "Tanween, Shadda & Sukun", "nl": "Tanween, Shadda & Sukun", "el": "Τανουίν, Σάντα & Σουκούν"},
        "desc": {"ar": "أحكام التنوين الثلاثة والشدة والسكون وتطبيقاتها", "en": "Three types of Tanween, Shadda doubling & Sukun stopping", "de": "Drei Tanween-Arten, Shadda-Verdoppelung & Sukun-Stop", "fr": "Trois types de Tanween, doublement Shadda & arrêt Sukun", "tr": "Üç tür Tenvin, Şedde ikileştirme ve Sükûn durağı", "ru": "Три вида Танвина, удвоение Шадда и остановка Сукун", "sv": "Tre typer av Tanween, Shadda-fördubbling & Sukun-stopp", "nl": "Drie types Tanween, Shadda-verdubbeling & Sukun-stop", "el": "Τρεις τύποι Τανουίν, διπλασιασμός Σάντα & στάση Σουκούν"},
        "lessons": 10,
        "skills": ["tanween", "shadda", "sukun", "precision"],
    },
    {
        "level": 5, "emoji": "📝", "color": "#10B981",
        "title": {"ar": "قراءة الكلمات القرآنية", "en": "Reading Quranic Words", "de": "Koranische Wörter lesen", "fr": "Lire des mots coraniques", "tr": "Kur'an Kelimeleri Okuma", "ru": "Чтение коранических слов", "sv": "Läsa koraniska ord", "nl": "Koranische woorden lezen", "el": "Ανάγνωση κορανικών λέξεων"},
        "desc": {"ar": "تطبيق القواعد السابقة على كلمات من القرآن الكريم", "en": "Apply previous rules to actual words from the Holy Quran", "de": "Bisherige Regeln auf Koranwörter anwenden", "fr": "Appliquer les règles sur des mots du Coran", "tr": "Önceki kuralları Kur'an kelimelerine uygulayın", "ru": "Применение правил к словам из Корана", "sv": "Tillämpa reglerna på ord från Koranen", "nl": "Regels toepassen op woorden uit de Koran", "el": "Εφαρμογή κανόνων σε κορανικές λέξεις"},
        "lessons": 10,
        "skills": ["word_reading", "quran_vocabulary", "fluency"],
    },
    {
        "level": 6, "emoji": "📖", "color": "#EF4444",
        "title": {"ar": "قراءة الآيات", "en": "Reading Verses", "de": "Verse lesen", "fr": "Lire des versets", "tr": "Ayet Okuma", "ru": "Чтение аятов", "sv": "Läsa verser", "nl": "Verzen lezen", "el": "Ανάγνωση στίχων"},
        "desc": {"ar": "قراءة آيات كاملة من القرآن مع تطبيق أحكام التجويد الأساسية", "en": "Read complete Quran verses with basic Tajweed rules applied", "de": "Komplette Koranverse mit Grundtajweed lesen", "fr": "Lire des versets complets avec règles de Tajweed de base", "tr": "Temel Tecvid kurallarıyla tam ayetler okuyun", "ru": "Чтение полных аятов с базовыми правилами Таджвида", "sv": "Läs kompletta verser med grundläggande Tajweed", "nl": "Lees complete verzen met basis Tajweed", "el": "Ανάγνωση πλήρων στίχων με βασικό Τατζουίντ"},
        "lessons": 10,
        "skills": ["verse_reading", "basic_tajweed", "comprehension"],
    },
    {
        "level": 7, "emoji": "🎓", "color": "#7C3AED",
        "title": {"ar": "التجويد والإتقان", "en": "Tajweed & Mastery", "de": "Tajweed & Meisterschaft", "fr": "Tajweed & Maîtrise", "tr": "Tecvid ve Ustalık", "ru": "Таджвид и Мастерство", "sv": "Tajweed & Mästerskap", "nl": "Tajweed & Meesterschap", "el": "Τατζουίντ & Κατάκτηση"},
        "desc": {"ar": "أحكام التجويد المتقدمة: إدغام، إخفاء، إقلاب، قلقلة", "en": "Advanced Tajweed: Idgham, Ikhfa, Iqlab, Qalqalah", "de": "Fortgeschrittenes Tajweed: Idgham, Ikhfa, Iqlab, Qalqalah", "fr": "Tajweed avancé: Idgham, Ikhfa, Iqlab, Qalqalah", "tr": "İleri Tecvid: İdğam, İhfa, İklab, Kalkale", "ru": "Продвинутый Таджвид: Идгам, Ихфа, Иклаб, Калькала", "sv": "Avancerad Tajweed: Idgham, Ikhfa, Iqlab, Qalqalah", "nl": "Gevorderd Tajweed: Idgham, Ikhfa, Iqlab, Qalqalah", "el": "Προχωρημένο Τατζουίντ: Ιντγάμ, Ιχφά, Ικλάμπ, Καλκαλά"},
        "lessons": 10,
        "skills": ["idgham", "ikhfa", "iqlab", "qalqalah", "mastery"],
    },
]

# Nooraniya lesson content — Level 1 sample (10 lessons)
NOORANIYA_LESSONS = [
    # Level 1: Individual Letters
    {"id": 1, "level": 1, "lesson": 1, "emoji": "🔤",
     "title": {"ar": "حروف الألف إلى الخاء", "en": "Letters Alif to Kha", "de": "Buchstaben Alif bis Kha", "fr": "Lettres Alif à Kha", "tr": "Elif'ten Ha'ya Harfler", "ru": "Буквы Алиф — Ха", "sv": "Bokstäver Alif till Kha", "nl": "Letters Alif tot Kha", "el": "Γράμματα Αλίφ ως Χα"},
     "method": "visual_audio",
     "content": {
         "letters": ["أ", "ب", "ت", "ث", "ج", "ح", "خ"],
         "phonetics": ["/a/", "/b/", "/t/", "/th/", "/j/", "/ḥ/", "/kh/"],
         "names": {"ar": ["ألف", "باء", "تاء", "ثاء", "جيم", "حاء", "خاء"], "en": ["Alif", "Ba", "Ta", "Tha", "Jim", "Ha", "Kha"]},
         "tip": {"ar": "انطق كل حرف من مخرجه الصحيح. استمع ثم أعد النطق.", "en": "Pronounce each letter from its correct articulation point. Listen then repeat.", "de": "Sprich jeden Buchstaben korrekt aus. Höre zu und wiederhole.", "fr": "Prononcez chaque lettre correctement. Écoutez puis répétez.", "tr": "Her harfi doğru mahrecinden söyleyin. Dinleyin ve tekrarlayın.", "ru": "Произносите каждую букву правильно. Слушайте и повторяйте.", "sv": "Uttala varje bokstav korrekt. Lyssna och upprepa.", "nl": "Spreek elke letter correct uit. Luister en herhaal.", "el": "Πρόφερε κάθε γράμμα σωστά. Άκου και επανάλαβε."},
     },
     "quiz": {"type": "match_sound", "question": {"ar": "أي حرف صوته /b/؟", "en": "Which letter sounds /b/?", "de": "Welcher Buchstabe klingt /b/?", "fr": "Quelle lettre sonne /b/?", "tr": "Hangi harfin sesi /b/?", "ru": "Какая буква звучит /b/?", "sv": "Vilken bokstav låter /b/?", "nl": "Welke letter klinkt /b/?", "el": "Ποιο γράμμα ακούγεται /b/?"}, "correct": "ب", "options": ["أ", "ب", "ت", "ث"]},
     "xp": 15,
    },
    {"id": 2, "level": 1, "lesson": 2, "emoji": "🔤",
     "title": {"ar": "حروف الدال إلى الغين", "en": "Letters Dal to Ghayn", "de": "Buchstaben Dal bis Ghayn", "fr": "Lettres Dal à Ghayn", "tr": "Dal'dan Gayın'a Harfler", "ru": "Буквы Даль — Гайн", "sv": "Bokstäver Dal till Ghayn", "nl": "Letters Dal tot Ghayn", "el": "Γράμματα Νταλ ως Γαΐν"},
     "method": "visual_audio",
     "content": {
         "letters": ["د", "ذ", "ر", "ز", "س", "ش", "ص", "ض", "ط", "ظ", "ع", "غ"],
         "phonetics": ["/d/", "/dh/", "/r/", "/z/", "/s/", "/sh/", "/ṣ/", "/ḍ/", "/ṭ/", "/ẓ/", "/ʿ/", "/gh/"],
         "names": {"ar": ["دال", "ذال", "راء", "زاي", "سين", "شين", "صاد", "ضاد", "طاء", "ظاء", "عين", "غين"], "en": ["Dal", "Dhal", "Ra", "Zay", "Sin", "Shin", "Sad", "Dad", "Taa", "Dhaa", "Ayn", "Ghayn"]},
         "tip": {"ar": "ركّز على الفرق بين: س/ص، ت/ط، د/ض — الحروف المفخّمة والمرققة", "en": "Focus on the difference between: S/Ṣ, T/Ṭ, D/Ḍ — emphatic vs light letters", "de": "Achte auf den Unterschied: S/Ṣ, T/Ṭ, D/Ḍ", "fr": "Concentrez-vous sur la différence: S/Ṣ, T/Ṭ, D/Ḍ", "tr": "Aradaki farka dikkat edin: S/Ṣ, T/Ṭ, D/Ḍ", "ru": "Обратите внимание на разницу: С/Ṣ, Т/Ṭ, Д/Ḍ", "sv": "Fokusera på skillnaden: S/Ṣ, T/Ṭ, D/Ḍ", "nl": "Let op het verschil: S/Ṣ, T/Ṭ, D/Ḍ", "el": "Εστίασε στη διαφορά: S/Ṣ, T/Ṭ, D/Ḍ"},
     },
     "quiz": {"type": "match_sound", "question": {"ar": "أي حرف هو حرف الضاد؟", "en": "Which is the letter Dad (Ḍ)?", "de": "Welcher ist der Buchstabe Dad (Ḍ)?", "fr": "Laquelle est la lettre Dad (Ḍ)?", "tr": "Dad (Ḍ) harfi hangisidir?", "ru": "Какая буква — Дад (Ḍ)?", "sv": "Vilken är bokstaven Dad (Ḍ)?", "nl": "Welke is de letter Dad (Ḍ)?", "el": "Ποιο είναι το γράμμα Νταντ (Ḍ)?"}, "correct": "ض", "options": ["د", "ض", "ظ", "ذ"]},
     "xp": 15,
    },
    {"id": 3, "level": 1, "lesson": 3, "emoji": "🔤",
     "title": {"ar": "حروف الفاء إلى الياء", "en": "Letters Fa to Ya", "de": "Buchstaben Fa bis Ya", "fr": "Lettres Fa à Ya", "tr": "Fa'dan Ya'ya Harfler", "ru": "Буквы Фа — Йа", "sv": "Bokstäver Fa till Ya", "nl": "Letters Fa tot Ya", "el": "Γράμματα Φα ως Γιά"},
     "method": "visual_audio",
     "content": {
         "letters": ["ف", "ق", "ك", "ل", "م", "ن", "هـ", "و", "ي"],
         "phonetics": ["/f/", "/q/", "/k/", "/l/", "/m/", "/n/", "/h/", "/w/", "/y/"],
         "names": {"ar": ["فاء", "قاف", "كاف", "لام", "ميم", "نون", "هاء", "واو", "ياء"], "en": ["Fa", "Qaf", "Kaf", "Lam", "Mim", "Nun", "Ha", "Waw", "Ya"]},
         "tip": {"ar": "أكملت الأبجدية! الآن راجع جميع الحروف بالترتيب", "en": "You completed the alphabet! Now review all letters in order", "de": "Du hast das Alphabet geschafft! Wiederhole alle Buchstaben", "fr": "Vous avez terminé l'alphabet ! Révisez toutes les lettres", "tr": "Alfabeyi tamamladınız! Şimdi tüm harfleri tekrarlayın", "ru": "Вы завершили алфавит! Повторите все буквы", "sv": "Du har klarat alfabetet! Repetera alla bokstäver", "nl": "Je hebt het alfabet voltooid! Herhaal alle letters", "el": "Ολοκλήρωσες το αλφάβητο! Επανάλαβε όλα τα γράμματα"},
     },
     "quiz": {"type": "sequence", "question": {"ar": "رتّب الحروف: ف، ل، ك، ق", "en": "Arrange the letters: F, L, K, Q", "de": "Ordne: F, L, K, Q", "fr": "Arrangez: F, L, K, Q", "tr": "Sıralayın: F, L, K, Q", "ru": "Расположите: Ф, Л, К, К", "sv": "Ordna: F, L, K, Q", "nl": "Rangschik: F, L, K, Q", "el": "Τοποθέτησε: Φ, Λ, Κ, Κ"}, "correct": ["ف", "ق", "ك", "ل"], "options": ["ل", "ق", "ف", "ك"]},
     "xp": 15,
    },
    {"id": 4, "level": 1, "lesson": 4, "emoji": "🎯",
     "title": {"ar": "مخارج الحروف — مجموعة الحلق", "en": "Articulation Points — Throat Letters", "de": "Artikulationspunkte — Kehlbuchstaben", "fr": "Points d'articulation — Lettres gutturales", "tr": "Mahreçler — Gırtlak Harfleri", "ru": "Точки артикуляции — Горловые буквы", "sv": "Artikulationspunkter — Halsbokstäver", "nl": "Articulatiepunten — Keelletters", "el": "Σημεία άρθρωσης — Λαρυγγικά"},
     "method": "interactive_diagram",
     "content": {
         "group": "throat",
         "letters": ["ء", "هـ", "ع", "ح", "غ", "خ"],
         "positions": {"ar": ["أقصى الحلق", "أقصى الحلق", "وسط الحلق", "وسط الحلق", "أدنى الحلق", "أدنى الحلق"], "en": ["Deepest throat", "Deepest throat", "Middle throat", "Middle throat", "Nearest throat", "Nearest throat"]},
         "tip": {"ar": "ضع يدك على حلقك وانطق كل حرف — ستشعر بالاهتزاز في مكان مختلف!", "en": "Place your hand on your throat and pronounce each letter — you'll feel vibration in different spots!", "de": "Lege deine Hand auf den Hals und sprich — du spürst Vibrationen!", "fr": "Placez votre main sur la gorge et prononcez — sentez les vibrations!", "tr": "Elinizi boğazınıza koyun ve söyleyin — farklı yerlerde titreşim hissedeceksiniz!", "ru": "Положите руку на горло и произносите — почувствуете вибрацию!", "sv": "Lägg handen på halsen och uttala — känn vibrationen!", "nl": "Leg je hand op je keel en spreek uit — voel de trillingen!", "el": "Βάλε το χέρι στον λαιμό και πρόφερε — θα νιώσεις δονήσεις!"},
     },
     "quiz": {"type": "categorize", "question": {"ar": "صنّف: أي حرف من وسط الحلق؟", "en": "Categorize: Which letter is from the middle throat?", "de": "Kategorisiere: Welcher Buchstabe kommt aus der Halsmitte?", "fr": "Catégorisez: Quelle lettre vient du milieu de la gorge?", "tr": "Sınıflandırın: Hangi harf gırtlağın ortasından?", "ru": "Классифицируйте: Какая буква из середины горла?", "sv": "Kategorisera: Vilken bokstav från mitten av halsen?", "nl": "Categoriseer: Welke letter uit het midden van de keel?", "el": "Ποιο γράμμα είναι από τη μέση του λαιμού;"}, "correct": "ع", "options": ["ء", "ع", "غ", "خ"]},
     "xp": 20,
    },
    {"id": 5, "level": 1, "lesson": 5, "emoji": "🎯",
     "title": {"ar": "مخارج الحروف — اللسان والشفتان", "en": "Articulation Points — Tongue & Lips", "de": "Artikulation — Zunge & Lippen", "fr": "Articulation — Langue & Lèvres", "tr": "Mahreçler — Dil ve Dudaklar", "ru": "Артикуляция — Язык и губы", "sv": "Artikulation — Tunga & Läppar", "nl": "Articulatie — Tong & Lippen", "el": "Άρθρωση — Γλώσσα & Χείλη"},
     "method": "interactive_diagram",
     "content": {
         "groups": [
             {"name": {"ar": "طرف اللسان", "en": "Tip of tongue"}, "letters": ["ت", "د", "ط", "ن", "ر", "ل"]},
             {"name": {"ar": "وسط اللسان", "en": "Middle of tongue"}, "letters": ["ج", "ش", "ي"]},
             {"name": {"ar": "الشفتان", "en": "Lips"}, "letters": ["ب", "م", "و", "ف"]},
         ],
         "tip": {"ar": "راقب حركة فمك في المرآة أثناء النطق!", "en": "Watch your mouth movement in the mirror while pronouncing!", "de": "Beobachte deine Mundbewegung im Spiegel!", "fr": "Regardez votre bouche dans le miroir!", "tr": "Söylerken ağız hareketinizi aynada izleyin!", "ru": "Наблюдайте за движением рта в зеркале!", "sv": "Se munrörelsen i spegeln!", "nl": "Bekijk je mondbeweging in de spiegel!", "el": "Παρατήρησε τη στοματική σου κίνηση!"},
     },
     "quiz": {"type": "categorize", "question": {"ar": "أي حرف مخرجه الشفتان؟", "en": "Which letter comes from the lips?", "de": "Welcher Buchstabe kommt von den Lippen?", "fr": "Quelle lettre vient des lèvres?", "tr": "Hangi harf dudaklardan çıkar?", "ru": "Какая буква произносится губами?", "sv": "Vilken bokstav från läpparna?", "nl": "Welke letter van de lippen?", "el": "Ποιο γράμμα από τα χείλη;"}, "correct": "ب", "options": ["ب", "ت", "ج", "ع"]},
     "xp": 20,
    },
    {"id": 6, "level": 1, "lesson": 6, "emoji": "✍️", "title": {"ar": "تمرين كتابة الحروف (١)", "en": "Letter Writing Practice (1)", "de": "Schreibübung (1)", "fr": "Exercice d'écriture (1)", "tr": "Harf Yazma Alıştırması (1)", "ru": "Практика написания (1)", "sv": "Skrivövning (1)", "nl": "Schrijfoefening (1)", "el": "Εξάσκηση γραφής (1)"}, "method": "tracing", "content": {"letters": ["أ", "ب", "ت", "ث", "ج", "ح", "خ"], "tip": {"ar": "اتبع الخطوط المنقطة لكتابة كل حرف", "en": "Follow the dotted lines to write each letter", "de": "Folge den punktierten Linien", "fr": "Suivez les lignes pointillées", "tr": "Noktalı çizgileri takip edin", "ru": "Следуйте пунктирным линиям", "sv": "Följ de prickade linjerna", "nl": "Volg de stippellijnen", "el": "Ακολούθησε τις διακεκομμένες γραμμές"}}, "quiz": {"type": "write", "question": {"ar": "اكتب حرف الباء", "en": "Write the letter Ba", "de": "Schreibe Ba", "fr": "Écrivez Ba", "tr": "Ba harfini yazın", "ru": "Напишите Ба", "sv": "Skriv Ba", "nl": "Schrijf Ba", "el": "Γράψε Μπά"}, "correct": "ب"}, "xp": 15},
    {"id": 7, "level": 1, "lesson": 7, "emoji": "✍️", "title": {"ar": "تمرين كتابة الحروف (٢)", "en": "Letter Writing Practice (2)", "de": "Schreibübung (2)", "fr": "Exercice d'écriture (2)", "tr": "Harf Yazma Alıştırması (2)", "ru": "Практика написания (2)", "sv": "Skrivövning (2)", "nl": "Schrijfoefening (2)", "el": "Εξάσκηση γραφής (2)"}, "method": "tracing", "content": {"letters": ["د", "ذ", "ر", "ز", "س", "ش", "ص", "ض"], "tip": {"ar": "لاحظ الفرق بين: ر/ز (النقطة) و س/ش (النقاط الثلاث)", "en": "Notice the difference: R/Z (dot) and S/Sh (three dots)", "de": "Beachte den Unterschied: R/Z und S/Sh", "fr": "Notez la différence: R/Z et S/Sh", "tr": "Farka dikkat edin: R/Z ve S/Ş", "ru": "Заметьте разницу: Р/З и С/Ш", "sv": "Notera skillnaden: R/Z och S/Sh", "nl": "Let op het verschil: R/Z en S/Sh", "el": "Πρόσεξε τη διαφορά: Ρ/Ζ και Σ/Σχ"}}, "quiz": {"type": "write", "question": {"ar": "اكتب حرف الشين", "en": "Write Shin", "de": "Schreibe Shin", "fr": "Écrivez Shin", "tr": "Şin harfini yazın", "ru": "Напишите Шин", "sv": "Skriv Shin", "nl": "Schrijf Shin", "el": "Γράψε Σιν"}, "correct": "ش"}, "xp": 15},
    {"id": 8, "level": 1, "lesson": 8, "emoji": "🎮", "title": {"ar": "لعبة تمييز الحروف المتشابهة", "en": "Similar Letters Game", "de": "Ähnliche-Buchstaben-Spiel", "fr": "Jeu des lettres similaires", "tr": "Benzer Harfler Oyunu", "ru": "Игра: похожие буквы", "sv": "Spel: liknande bokstäver", "nl": "Vergelijkbare-letters-spel", "el": "Παιχνίδι παρόμοιων γραμμάτων"}, "method": "game", "content": {"pairs": [["ب", "ت", "ث"], ["ج", "ح", "خ"], ["د", "ذ"], ["ر", "ز"], ["س", "ش"], ["ص", "ض"], ["ط", "ظ"], ["ع", "غ"]], "tip": {"ar": "الفرق بين هذه الحروف هو النقاط فقط! ركّز على عدد النقاط ومكانها", "en": "The difference is only the dots! Focus on the number and position of dots", "de": "Der Unterschied sind nur die Punkte! Achte auf Anzahl und Position", "fr": "La différence ne sont que les points ! Concentrez-vous sur leur nombre et position", "tr": "Fark sadece noktalar! Sayılarına ve yerlerine dikkat edin", "ru": "Разница только в точках! Следите за количеством и позицией", "sv": "Skillnaden är bara prickarna! Fokusera på antal och position", "nl": "Het verschil zijn alleen de punten! Let op aantal en positie", "el": "Η διαφορά είναι μόνο οι τελείες!"}}, "quiz": {"type": "pairs", "question": {"ar": "أي حرفين من نفس العائلة؟", "en": "Which two letters are from the same family?", "de": "Welche zwei Buchstaben sind verwandt?", "fr": "Quelles lettres sont de la même famille?", "tr": "Hangi iki harf aynı aileden?", "ru": "Какие две буквы из одной семьи?", "sv": "Vilka bokstäver är från samma familj?", "nl": "Welke letters horen bij dezelfde familie?", "el": "Ποια γράμματα ανήκουν στην ίδια οικογένεια?"}, "correct": ["ج", "ح"], "options": ["ج", "ح", "د", "ر"]}, "xp": 25},
    {"id": 9, "level": 1, "lesson": 9, "emoji": "🔊", "title": {"ar": "تمرين استماع وتمييز الأصوات", "en": "Listening & Sound Recognition", "de": "Hör- & Klangübung", "fr": "Exercice d'écoute et de sons", "tr": "Dinleme ve Ses Tanıma", "ru": "Слушание и распознавание звуков", "sv": "Lyssnings- & ljudövning", "nl": "Luister- & klankoefening", "el": "Ακρόαση & αναγνώριση ήχων"}, "method": "audio_match", "content": {"focus": "emphatic_vs_light", "pairs": [{"light": "س", "emphatic": "ص"}, {"light": "ت", "emphatic": "ط"}, {"light": "د", "emphatic": "ض"}, {"light": "ذ", "emphatic": "ظ"}], "tip": {"ar": "الحروف المفخّمة تُنطق بتضخيم الصوت ورفع اللسان نحو سقف الفم", "en": "Emphatic letters are pronounced with a heavier sound, raising the tongue toward the palate", "de": "Emphatische Buchstaben werden schwerer ausgesprochen", "fr": "Les lettres emphatiques sont prononcées plus lourdement", "tr": "Kalın harfler daha ağır sesle söylenir", "ru": "Эмфатические буквы произносятся тяжелее", "sv": "Emfatiska bokstäver uttalas tyngre", "nl": "Emfatische letters worden zwaarder uitgesproken", "el": "Τα εμφατικά γράμματα προφέρονται βαρύτερα"}}, "quiz": {"type": "audio_match", "question": {"ar": "استمع: هل هذا حرف مفخّم أم مرقّق؟", "en": "Listen: Is this an emphatic or light letter?", "de": "Höre: Ist das emphatisch oder leicht?", "fr": "Écoutez: emphatique ou léger?", "tr": "Dinleyin: Bu kalın mı ince mi?", "ru": "Слушайте: эмфатическая или лёгкая?", "sv": "Lyssna: emfatisk eller lätt?", "nl": "Luister: emfatisch of licht?", "el": "Ακούστε: εμφατικό ή ελαφρύ;"}, "correct": "emphatic", "letter": "ص"}, "xp": 20},
    {"id": 10, "level": 1, "lesson": 10, "emoji": "🏆", "title": {"ar": "اختبار المستوى الأول", "en": "Level 1 Assessment", "de": "Stufe 1 Bewertung", "fr": "Évaluation Niveau 1", "tr": "Seviye 1 Değerlendirmesi", "ru": "Тест Уровня 1", "sv": "Nivå 1 bedömning", "nl": "Niveau 1 toets", "el": "Αξιολόγηση Επιπέδου 1"}, "method": "assessment", "content": {"sections": ["letter_recognition", "sound_matching", "writing", "categorization"], "pass_score": 70, "tip": {"ar": "أجب على جميع الأسئلة. تحتاج 70% للانتقال للمستوى التالي!", "en": "Answer all questions. You need 70% to advance to the next level!", "de": "Beantworte alle Fragen. 70% zum Weiterkommen!", "fr": "Répondez à toutes les questions. 70% pour avancer!", "tr": "Tüm soruları cevaplayın. İlerlemek için %70 gerekli!", "ru": "Ответьте на все вопросы. 70% для перехода!", "sv": "Svara på alla frågor. 70% för att gå vidare!", "nl": "Beantwoord alle vragen. 70% om verder te gaan!", "el": "Απάντησε σε όλα. 70% για να προχωρήσεις!"}}, "quiz": {"type": "comprehensive", "total_questions": 15}, "xp": 50},
]

# ═══════════════════════════════════════════════════════════════
# TRACK 2: AQEEDAH — العقيدة
# ═══════════════════════════════════════════════════════════════

AQEEDAH_LEVELS = [
    {"level": 1, "emoji": "☝️", "color": "#059669", "title": {"ar": "التوحيد — معرفة الله", "en": "Tawheed — Knowing Allah", "de": "Tawheed — Allah kennenlernen", "fr": "Tawheed — Connaître Allah", "tr": "Tevhid — Allah'ı Tanımak", "ru": "Таухид — Познание Аллаха", "sv": "Tawheed — Att känna Allah", "nl": "Tawheed — Allah leren kennen", "el": "Ταουχίντ — Γνωρίζοντας τον Αλλάχ"}, "lessons": 10},
    {"level": 2, "emoji": "✨", "color": "#0EA5E9", "title": {"ar": "أسماء الله الحسنى", "en": "99 Beautiful Names of Allah", "de": "99 Schöne Namen Allahs", "fr": "99 Beaux Noms d'Allah", "tr": "Esmaül Hüsna — 99 İsim", "ru": "99 Прекрасных Имён Аллаха", "sv": "99 Vackra namn på Allah", "nl": "99 Mooie Namen van Allah", "el": "99 Όμορφα Ονόματα του Αλλάχ"}, "lessons": 10},
    {"level": 3, "emoji": "👼", "color": "#8B5CF6", "title": {"ar": "أركان الإيمان الستة", "en": "Six Pillars of Faith", "de": "Sechs Säulen des Glaubens", "fr": "Six Piliers de la Foi", "tr": "İmanın Altı Şartı", "ru": "Шесть Столпов Веры", "sv": "Sex trosartiklar", "nl": "Zes geloofsartikelen", "el": "Έξι πυλώνες πίστης"}, "lessons": 12},
    {"level": 4, "emoji": "🕋", "color": "#D97706", "title": {"ar": "أركان الإسلام الخمسة", "en": "Five Pillars of Islam", "de": "Fünf Säulen des Islam", "fr": "Cinq Piliers de l'Islam", "tr": "İslam'ın Beş Şartı", "ru": "Пять Столпов Ислама", "sv": "Islams fem pelare", "nl": "Vijf zuilen van de Islam", "el": "Πέντε πυλώνες του Ισλάμ"}, "lessons": 10},
    {"level": 5, "emoji": "🎓", "color": "#EF4444", "title": {"ar": "مراجعة شاملة واختبار", "en": "Comprehensive Review & Test", "de": "Umfassende Wiederholung & Test", "fr": "Révision complète & Test", "tr": "Kapsamlı Tekrar ve Sınav", "ru": "Полный обзор и тест", "sv": "Omfattande genomgång & test", "nl": "Uitgebreide herhaling & toets", "el": "Ολοκληρωμένη επανάληψη & τεστ"}, "lessons": 8},
]

# ═══════════════════════════════════════════════════════════════
# TRACK 3: FIQH — الفقه المبسّط
# ═══════════════════════════════════════════════════════════════

FIQH_LEVELS = [
    {"level": 1, "emoji": "💧", "color": "#0EA5E9", "title": {"ar": "الطهارة — الوضوء والغسل", "en": "Purification — Wudu & Ghusl", "de": "Reinigung — Wudu & Ghusl", "fr": "Purification — Wudu & Ghusl", "tr": "Taharet — Abdest ve Gusül", "ru": "Очищение — Вуду и Гусль", "sv": "Rening — Wudu & Ghusl", "nl": "Reiniging — Woedoe & Ghusl", "el": "Κάθαρση — Γουντού & Γκουσλ"}, "lessons": 10},
    {"level": 2, "emoji": "🕌", "color": "#059669", "title": {"ar": "الصلاة — بالتفصيل الكامل", "en": "Prayer — Complete Detail", "de": "Gebet — Vollständig", "fr": "Prière — Détail complet", "tr": "Namaz — Tam Detaylı", "ru": "Молитва — Подробно", "sv": "Bön — Fullständig", "nl": "Gebed — Volledig", "el": "Προσευχή — Πλήρης"}, "lessons": 12},
    {"level": 3, "emoji": "🌙", "color": "#7C3AED", "title": {"ar": "الصيام — أحكام رمضان", "en": "Fasting — Rules of Ramadan", "de": "Fasten — Ramadan-Regeln", "fr": "Jeûne — Règles du Ramadan", "tr": "Oruç — Ramazan Kuralları", "ru": "Пост — Правила Рамадана", "sv": "Fasta — Ramadanregler", "nl": "Vasten — Ramadanregels", "el": "Νηστεία — Κανόνες Ραμαζανιού"}, "lessons": 8},
    {"level": 4, "emoji": "💰", "color": "#D97706", "title": {"ar": "الزكاة والصدقة", "en": "Zakat & Charity", "de": "Zakat & Wohltätigkeit", "fr": "Zakat & Charité", "tr": "Zekât ve Sadaka", "ru": "Закят и Благотворительность", "sv": "Zakat & Välgörenhet", "nl": "Zakat & Liefdadigheid", "el": "Ζακάτ & Φιλανθρωπία"}, "lessons": 10},
]

# ═══════════════════════════════════════════════════════════════
# TRACK 4: SEERAH — السيرة النبوية
# ═══════════════════════════════════════════════════════════════

SEERAH_LEVELS = [
    {"level": 1, "emoji": "👶", "color": "#EC4899", "title": {"ar": "الميلاد والطفولة", "en": "Birth & Childhood", "de": "Geburt & Kindheit", "fr": "Naissance & Enfance", "tr": "Doğum ve Çocukluk", "ru": "Рождение и детство", "sv": "Födelse & barndom", "nl": "Geboorte & jeugd", "el": "Γέννηση & παιδική ηλικία"}, "lessons": 10},
    {"level": 2, "emoji": "📜", "color": "#7C3AED", "title": {"ar": "النبوة وبداية الدعوة", "en": "Prophethood & The Call", "de": "Prophetentum & Der Ruf", "fr": "Prophétie & L'Appel", "tr": "Peygamberlik ve Davet", "ru": "Пророчество и Призыв", "sv": "Profetskap & Kallelsen", "nl": "Profeetschap & De Roeping", "el": "Προφητεία & Η Κλήση"}, "lessons": 10},
    {"level": 3, "emoji": "🐪", "color": "#D97706", "title": {"ar": "الهجرة إلى المدينة", "en": "The Hijrah to Madinah", "de": "Die Hijra nach Medina", "fr": "L'Hégire à Médine", "tr": "Medine'ye Hicret", "ru": "Хиджра в Медину", "sv": "Hijrah till Madinah", "nl": "De Hijrah naar Madinah", "el": "Η Χίτζρα στη Μεδίνα"}, "lessons": 10},
    {"level": 4, "emoji": "⚔️", "color": "#EF4444", "title": {"ar": "بناء الدولة والغزوات", "en": "Building the State & Battles", "de": "Staatsaufbau & Schlachten", "fr": "Construction de l'État & Batailles", "tr": "Devlet Kuruluşu ve Gazalar", "ru": "Строительство государства и сражения", "sv": "Statsbyggnad & slag", "nl": "Staatsopbouw & veldslagen", "el": "Οικοδόμηση κράτους & μάχες"}, "lessons": 10},
    {"level": 5, "emoji": "🕋", "color": "#059669", "title": {"ar": "فتح مكة والأحداث الأخيرة", "en": "Conquest of Makkah & Final Events", "de": "Eroberung von Mekka & letzte Ereignisse", "fr": "Conquête de La Mecque & événements finaux", "tr": "Mekke'nin Fethi ve Son Olaylar", "ru": "Завоевание Мекки и последние события", "sv": "Erövringen av Mecka & sista händelserna", "nl": "Verovering van Mekka & laatste gebeurtenissen", "el": "Κατάκτηση της Μέκκας & τελευταία γεγονότα"}, "lessons": 10},
    {"level": 6, "emoji": "💝", "color": "#EC4899", "title": {"ar": "أخلاق النبي ﷺ وصفاته", "en": "The Prophet's ﷺ Character & Qualities", "de": "Charakter & Eigenschaften des Propheten ﷺ", "fr": "Caractère & Qualités du Prophète ﷺ", "tr": "Hz. Peygamber'in ﷺ Ahlakı", "ru": "Характер и качества Пророка ﷺ", "sv": "Profetens ﷺ karaktär & egenskaper", "nl": "Karakter & eigenschappen van de Profeet ﷺ", "el": "Χαρακτήρας & ιδιότητες του Προφήτη ﷺ"}, "lessons": 10},
]

# ═══════════════════════════════════════════════════════════════
# TRACK 5: ADAB — الآداب الإسلامية (20 Essential Manners)
# ═══════════════════════════════════════════════════════════════

ADAB_LESSONS = [
    {"id": 1, "emoji": "🍽️", "title": {"ar": "آداب الطعام والشراب", "en": "Eating & Drinking Etiquette", "de": "Ess- & Trinketikette", "fr": "Étiquette du repas", "tr": "Yeme-İçme Adabı", "ru": "Этикет еды и питья", "sv": "Mat- & dryckesetikett", "nl": "Eet- & drinketiquette", "el": "Εθιμοτυπία φαγητού"},
     "rules": {
         "ar": ["قل بسم الله قبل الأكل", "كل بيمينك", "كل مما يليك", "لا تعب الطعام", "قل الحمد لله بعد الأكل"],
         "en": ["Say Bismillah before eating", "Eat with your right hand", "Eat from what is nearest to you", "Don't criticize food", "Say Alhamdulillah after eating"],
         "de": ["Sage Bismillah vor dem Essen", "Iss mit der rechten Hand", "Iss von dem was vor dir liegt", "Kritisiere kein Essen", "Sage Alhamdulillah nach dem Essen"],
         "fr": ["Dis Bismillah avant de manger", "Mange de la main droite", "Mange ce qui est devant toi", "Ne critique pas la nourriture", "Dis Alhamdulillah après manger"],
         "tr": ["Yemekten önce Bismillah de", "Sağ elinle ye", "Önündekinden ye", "Yemeği kötüleme", "Yemekten sonra Elhamdülillah de"],
         "ru": ["Скажи Бисмиллях перед едой", "Ешь правой рукой", "Ешь то что перед тобой", "Не критикуй еду", "Скажи Альхамдулиллях после еды"],
         "sv": ["Säg Bismillah före maten", "Ät med höger hand", "Ät det som är närmast dig", "Kritisera inte maten", "Säg Alhamdulillah efter maten"],
         "nl": ["Zeg Bismillah voor het eten", "Eet met je rechterhand", "Eet van wat voor je staat", "Bekritiseer het eten niet", "Zeg Alhamdulillah na het eten"],
         "el": ["Πες Μπισμιλλάχ πριν φας", "Φάε με το δεξί χέρι", "Φάε αυτό που είναι κοντά σου", "Μην κριτικάρεις το φαγητό", "Πες Αλχαμντουλιλλάχ μετά"],
     },
     "hadith": {"ar": "قال النبي ﷺ: «يا غلام، سمّ الله، وكل بيمينك، وكل مما يليك» — متفق عليه", "en": "The Prophet ﷺ said: \"O boy, mention Allah's name, eat with your right hand, and eat from what is nearest to you\" — Agreed upon", "de": "Der Prophet ﷺ sagte: \"O Junge, nenne Allahs Namen, iss mit rechts und iss was vor dir liegt\"", "fr": "Le Prophète ﷺ a dit: \"O garçon, mentionne le nom d'Allah, mange de la main droite et mange ce qui est devant toi\"", "tr": "Hz. Peygamber ﷺ buyurdu: \"Ey çocuk, Allah'ın adını an, sağ elinle ye, önündekinden ye\"", "ru": "Пророк ﷺ сказал: «О мальчик, назови имя Аллаха, ешь правой рукой и ешь то, что перед тобой»", "sv": "Profeten ﷺ sade: \"O pojke, nämn Allahs namn, ät med höger hand och ät det som är närmast\"", "nl": "De Profeet ﷺ zei: \"O jongen, noem Allahs naam, eet met rechts en eet wat voor je staat\"", "el": "Ο Προφήτης ﷺ είπε: «Αγόρι μου, ανάφερε το όνομα του Αλλάχ, φάε με το δεξί και φάε αυτό που είναι μπροστά σου»"},
    },
    {"id": 2, "emoji": "🕌", "title": {"ar": "آداب المسجد", "en": "Mosque Etiquette", "de": "Moschee-Etikette", "fr": "Étiquette de la mosquée", "tr": "Cami Adabı", "ru": "Этикет мечети", "sv": "Moskéetikett", "nl": "Moskee-etiquette", "el": "Εθιμοτυπία τζαμιού"},
     "rules": {"ar": ["ادخل بالرجل اليمنى وقل دعاء الدخول", "لا ترفع صوتك", "صلّ تحية المسجد", "لا تمر أمام المصلّي", "اخرج بالرجل اليسرى وقل دعاء الخروج"], "en": ["Enter with right foot and say entry dua", "Don't raise your voice", "Pray Tahiyyat al-Masjid", "Don't pass in front of someone praying", "Exit with left foot and say exit dua"], "de": ["Betritt mit dem rechten Fuß", "Sei leise", "Bete Tahiyyat al-Masjid", "Gehe nicht vor Betenden vorbei", "Verlasse mit dem linken Fuß"], "fr": ["Entrez du pied droit", "Ne parlez pas fort", "Priez Tahiyyat", "Ne passez pas devant quelqu'un en prière", "Sortez du pied gauche"], "tr": ["Sağ ayakla girin", "Sesinizi yükseltmeyin", "Tahiyyetü'l-mescid namazı kılın", "Namaz kılanın önünden geçmeyin", "Sol ayakla çıkın"], "ru": ["Входите с правой ноги", "Не повышайте голос", "Совершите Тахият аль-Масджид", "Не проходите перед молящимся", "Выходите с левой ноги"], "sv": ["Gå in med höger fot", "Var tyst", "Be Tahiyyat", "Gå inte framför den som ber", "Gå ut med vänster fot"], "nl": ["Ga naar binnen met rechts", "Wees stil", "Bid Tahiyyat", "Loop niet voor een biddende", "Ga naar buiten met links"], "el": ["Μπες με το δεξί πόδι", "Μη φωνάζεις", "Κάνε Ταχιγιάτ", "Μη περνάς μπροστά από κάποιον που προσεύχεται", "Βγες με το αριστερό πόδι"]},
     "hadith": {"ar": "قال النبي ﷺ: «إذا دخل أحدكم المسجد فليركع ركعتين قبل أن يجلس» — متفق عليه", "en": "The Prophet ﷺ said: \"When one of you enters the mosque, pray two rak'ahs before sitting\" — Agreed upon", "de": "Der Prophet ﷺ sagte: \"Wenn ihr die Moschee betretet, betet zwei Rak'ah\"", "fr": "Le Prophète ﷺ a dit: \"Quand vous entrez à la mosquée, priez deux rak'ahs\"", "tr": "Hz. Peygamber ﷺ buyurdu: \"Biriniz mescide girdiğinde oturmadan önce iki rekât namaz kılsın\"", "ru": "Пророк ﷺ сказал: «Войдя в мечеть, совершите два ракаата»", "sv": "Profeten ﷺ sade: \"Bed två rak'ah innan ni sätter er\"", "nl": "De Profeet ﷺ zei: \"Bid twee rak'ah voordat je gaat zitten\"", "el": "Ο Προφήτης ﷺ είπε: «Κάντε δύο ρακάτ πριν καθίσετε»"},
    },
    {"id": 3, "emoji": "😴", "title": {"ar": "آداب النوم", "en": "Sleep Etiquette", "de": "Schlafetikette", "fr": "Étiquette du sommeil", "tr": "Uyku Adabı", "ru": "Этикет сна", "sv": "Sömnetikett", "nl": "Slaapetiquette", "el": "Εθιμοτυπία ύπνου"},
     "rules": {"ar": ["نم على الجنب الأيمن", "اقرأ أذكار النوم وآية الكرسي", "انفض فراشك ثلاثاً", "توضأ قبل النوم", "قل دعاء النوم: باسمك اللهم أموت وأحيا"], "en": ["Sleep on your right side", "Recite sleep adhkar and Ayat al-Kursi", "Dust your bed three times", "Make wudu before sleeping", "Say sleep dua: In Your name O Allah I die and live"], "de": ["Schlafe auf der rechten Seite", "Lies Schlaf-Adhkar und Ayat al-Kursi", "Schüttle dein Bett dreimal aus", "Mache Wudu vor dem Schlafen", "Sage das Schlaf-Dua"], "fr": ["Dormez sur le côté droit", "Récitez les adhkar du sommeil", "Secouez votre lit trois fois", "Faites le wudu avant de dormir", "Dites le dua du sommeil"], "tr": ["Sağ tarafınıza yatın", "Uyku dualarını ve Ayetel Kürsi'yi okuyun", "Yatağınızı üç kez silkeleyin", "Yatmadan önce abdest alın", "Uyku duasını okuyun"], "ru": ["Спите на правом боку", "Читайте зикр перед сном", "Встряхните постель трижды", "Совершите вуду перед сном", "Прочитайте дуа перед сном"], "sv": ["Sov på höger sida", "Läs sömn-adhkar", "Skaka sängen tre gånger", "Gör wudu före sömn", "Läs sömn-dua"], "nl": ["Slaap op je rechterzij", "Lees slaap-adhkar", "Schud je bed drie keer", "Doe woedoe voor het slapen", "Zeg slaap-dua"], "el": ["Κοιμήσου στη δεξιά πλευρά", "Διάβασε αντκάρ ύπνου", "Τίναξε το κρεβάτι τρεις φορές", "Κάνε γουντού πριν τον ύπνο", "Πες ντουά ύπνου"]},
     "hadith": {"ar": "كان النبي ﷺ إذا أوى إلى فراشه نفض فراشه بداخلة إزاره ثلاثاً — متفق عليه", "en": "The Prophet ﷺ would dust his bed three times before lying down — Agreed upon", "de": "Der Prophet ﷺ schüttelte sein Bett dreimal aus — Übereinstimmend", "fr": "Le Prophète ﷺ secouait son lit trois fois — Unanime", "tr": "Hz. Peygamber ﷺ yatağını üç kez silkelerdi — Müttefekun Aleyh", "ru": "Пророк ﷺ встряхивал постель трижды — Согласованный", "sv": "Profeten ﷺ skakade sin säng tre gånger — Överenskommen", "nl": "De Profeet ﷺ schudde zijn bed drie keer — Overeengekomen", "el": "Ο Προφήτης ﷺ τίναζε το κρεβάτι τρεις φορές"},
    },
    {"id": 4, "emoji": "👋", "title": {"ar": "آداب السلام والتحية", "en": "Greeting Etiquette", "de": "Begrüßungsetikette", "fr": "Étiquette de salutation", "tr": "Selamlama Adabı", "ru": "Этикет приветствия", "sv": "Hälsningsetikett", "nl": "Begroetingsetiquette", "el": "Εθιμοτυπία χαιρετισμού"},
     "rules": {"ar": ["ابدأ بالسلام عند اللقاء", "الصغير يسلّم على الكبير", "الماشي يسلّم على الجالس", "القليل يسلّم على الكثير", "ردّ السلام واجب"], "en": ["Start with Salam when meeting", "Younger greets the elder", "Walking person greets the sitting", "Few greet the many", "Returning Salam is obligatory"], "de": ["Beginne mit Salam", "Jüngere grüßen Ältere", "Gehende grüßen Sitzende", "Wenige grüßen Viele", "Salam erwidern ist Pflicht"], "fr": ["Commencez par le Salam", "Le jeune salue l'aîné", "Le marcheur salue l'assis", "Le peu salue le beaucoup", "Répondre au Salam est obligatoire"], "tr": ["Karşılaşınca selam verin", "Küçük büyüğe selam verir", "Yürüyen oturana selam verir", "Az çok olana selam verir", "Selama karşılık vermek farzdır"], "ru": ["Начинайте с Салама", "Младший приветствует старшего", "Идущий приветствует сидящего", "Меньшинство приветствует большинство", "Ответить на Салам обязательно"], "sv": ["Börja med Salam", "Yngre hälsar äldre", "Gående hälsar sittande", "Få hälsar många", "Svara på Salam är obligatoriskt"], "nl": ["Begin met Salaam", "Jongere groet oudere", "Lopende groet zittende", "Weinigen groeten velen", "Salaam beantwoorden is verplicht"], "el": ["Ξεκίνα με Σαλάμ", "Ο νεότερος χαιρετά τον μεγαλύτερο", "Ο περπατών χαιρετά τον καθήμενο", "Οι λίγοι χαιρετούν τους πολλούς", "Η απάντηση στο Σαλάμ είναι υποχρεωτική"]},
     "hadith": {"ar": "قال النبي ﷺ: «أفشوا السلام بينكم» — صحيح مسلم", "en": "The Prophet ﷺ said: \"Spread the Salam among yourselves\" — Sahih Muslim", "de": "Der Prophet ﷺ sagte: \"Verbreitet den Salam unter euch\"", "fr": "Le Prophète ﷺ a dit: \"Répandez le Salam entre vous\"", "tr": "Hz. Peygamber ﷺ buyurdu: \"Aranızda selamı yayın\"", "ru": "Пророк ﷺ сказал: «Распространяйте Салам между собой»", "sv": "Profeten ﷺ sade: \"Sprid Salam bland er\"", "nl": "De Profeet ﷺ zei: \"Verspreid de Salaam onder jullie\"", "el": "Ο Προφήτης ﷺ είπε: «Διαδώστε το Σαλάμ μεταξύ σας»"},
    },
    {"id": 5, "emoji": "🚿", "title": {"ar": "آداب الخلاء والنظافة", "en": "Bathroom & Hygiene Etiquette", "de": "Bad- & Hygieneetikette", "fr": "Étiquette des toilettes", "tr": "Tuvalet ve Temizlik Adabı", "ru": "Этикет туалета и гигиены", "sv": "Toalett- & hygienetikett", "nl": "Toilet- & hygiëne-etiquette", "el": "Εθιμοτυπία τουαλέτας"},
     "rules": {"ar": ["ادخل بالرجل اليسرى", "قل دعاء الدخول", "لا تستقبل القبلة", "استخدم اليد اليسرى", "اغسل يديك جيداً"], "en": ["Enter with left foot", "Say entry dua", "Don't face the Qibla", "Use left hand", "Wash hands well"], "de": ["Betritt mit links", "Sage das Dua", "Nicht Richtung Qibla", "Benutze die linke Hand", "Wasche Hände gut"], "fr": ["Entrez du pied gauche", "Dites le dua", "Ne faites pas face à la Qibla", "Utilisez la main gauche", "Lavez bien vos mains"], "tr": ["Sol ayakla girin", "Giriş duasını okuyun", "Kıbleye dönmeyin", "Sol elinizi kullanın", "Ellerinizi iyi yıkayın"], "ru": ["Входите с левой ноги", "Скажите дуа", "Не поворачивайтесь к Кибле", "Используйте левую руку", "Хорошо мойте руки"], "sv": ["Gå in med vänster fot", "Säg dua", "Vänd inte mot Qibla", "Använd vänster hand", "Tvätta händerna väl"], "nl": ["Ga met links naar binnen", "Zeg het dua", "Kijk niet richting Qibla", "Gebruik linkerhand", "Was handen goed"], "el": ["Μπες με το αριστερό πόδι", "Πες ντουά", "Μη γυρίσεις προς Κίμπλα", "Χρησιμοποίησε αριστερό χέρι", "Πλύνε τα χέρια καλά"]},
     "hadith": {"ar": "كان النبي ﷺ إذا دخل الخلاء قال: اللهم إني أعوذ بك من الخبث والخبائث — متفق عليه", "en": "The Prophet ﷺ would say when entering: 'O Allah, I seek refuge from evil' — Agreed upon", "de": "Der Prophet ﷺ sagte beim Betreten: 'O Allah, ich suche Zuflucht vor dem Bösen'", "fr": "Le Prophète ﷺ disait en entrant: 'Ô Allah, je cherche refuge contre le mal'", "tr": "Hz. Peygamber ﷺ girerken: 'Allah'ım kötülükten sana sığınırım' derdi", "ru": "Пророк ﷺ говорил при входе: 'О Аллах, я прибегаю к Тебе от зла'", "sv": "Profeten ﷺ sade vid ingång: 'O Allah, jag söker tillflykt från ondska'", "nl": "De Profeet ﷺ zei bij binnenkomst: 'O Allah, ik zoek toevlucht tegen het kwaad'", "el": "Ο Προφήτης ﷺ έλεγε: 'Ω Αλλάχ, καταφεύγω σε Εσένα από το κακό'"},
    },
    {"id": 6, "emoji": "👕", "title": {"ar": "آداب اللباس", "en": "Clothing Etiquette", "de": "Kleidungsetikette", "fr": "Étiquette vestimentaire", "tr": "Giyim Adabı", "ru": "Этикет одежды", "sv": "Klädetikett", "nl": "Kledingetiquette", "el": "Εθιμοτυπία ρούχων"},
     "rules": {"ar": ["ابدأ باليمين عند اللبس", "ابدأ باليسار عند الخلع", "قل دعاء اللبس", "البس ما يستر ويجمّل", "لا تسرف في الملابس"], "en": ["Start with right when dressing", "Start with left when undressing", "Say the dressing dua", "Wear what covers and beautifies", "Don't be extravagant"], "de": ["Beginne rechts beim Anziehen", "Beginne links beim Ausziehen", "Sage das Anzieh-Dua", "Trage was bedeckt und verschönert", "Sei nicht verschwenderisch"], "fr": ["Commencez par la droite en s'habillant", "Commencez par la gauche en se déshabillant", "Dites le dua", "Portez ce qui couvre et embellit", "Ne soyez pas extravagant"], "tr": ["Giyerken sağdan başlayın", "Çıkarırken soldan başlayın", "Giyinme duasını okuyun", "Örten ve güzelleştiren giyin", "İsraf etmeyin"], "ru": ["Начинайте одеваться с правой стороны", "Снимайте с левой стороны", "Произнесите дуа одевания", "Носите скромное и красивое", "Не расточительствуйте"], "sv": ["Börja med höger vid påklädning", "Börja med vänster vid avklädning", "Säg klädnings-dua", "Bär det som täcker och förskönar", "Var inte extravagant"], "nl": ["Begin rechts bij het aankleden", "Begin links bij het uitkleden", "Zeg kleed-dua", "Draag wat bedekt en verfraait", "Wees niet buitensporig"], "el": ["Ξεκίνα με το δεξί στο ντύσιμο", "Ξεκίνα με το αριστερό στο γδύσιμο", "Πες ντουά ρούχων", "Φόρα ό,τι καλύπτει και ομορφαίνει", "Μην είσαι σπάταλος"]},
     "hadith": {"ar": "كان النبي ﷺ يبدأ بالميامن في لبسه ووضوئه وشأنه كله — متفق عليه", "en": "The Prophet ﷺ would start with the right in all matters — Agreed upon", "de": "Der Prophet ﷺ begann in allen Dingen mit rechts", "fr": "Le Prophète ﷺ commençait par la droite en toute chose", "tr": "Hz. Peygamber ﷺ her işe sağdan başlardı", "ru": "Пророк ﷺ начинал с правой стороны во всём", "sv": "Profeten ﷺ började med höger i allt", "nl": "De Profeet ﷺ begon met rechts in alles", "el": "Ο Προφήτης ﷺ ξεκινούσε με το δεξί σε όλα"},
    },
    {"id": 7, "emoji": "🤧", "title": {"ar": "آداب العطاس والتثاؤب", "en": "Sneezing & Yawning Etiquette", "de": "Nies- & Gähnetikette", "fr": "Étiquette de l'éternuement", "tr": "Hapşırma ve Esneme Adabı", "ru": "Этикет чихания и зевоты", "sv": "Nysnings- & gäspningsetikett", "nl": "Nies- & geeuweetiquette", "el": "Εθιμοτυπία φταρνίσματος"},
     "rules": {"ar": ["إذا عطست قل الحمد لله", "يقال لك يرحمك الله", "تردّ يهديكم الله", "غطّ فمك عند العطاس", "ادفع التثاؤب وغطّ فمك"], "en": ["When sneezing say Alhamdulillah", "Others say Yarhamukallah", "Reply Yahdikumullah", "Cover your mouth when sneezing", "Suppress yawning and cover your mouth"], "de": ["Sage Alhamdulillah beim Niesen", "Andere sagen Yarhamukallah", "Antworte Yahdikumullah", "Bedecke den Mund beim Niesen", "Unterdrücke Gähnen"], "fr": ["Dis Alhamdulillah en éternuant", "On te dit Yarhamukallah", "Réponds Yahdikumullah", "Couvre ta bouche", "Retiens le bâillement"], "tr": ["Hapşırınca Elhamdülillah de", "Sana Yerhamükellah denir", "Sen de Yehdikümullah de", "Hapşırırken ağzını kapat", "Esnemeyi engelle ve ağzını kapat"], "ru": ["При чихании скажи Альхамдулиллях", "Тебе скажут Ярхамукаллах", "Ответь Яхдикумуллах", "Прикрой рот при чихании", "Сдерживай зевоту"], "sv": ["Säg Alhamdulillah vid nysning", "Andra säger Yarhamukallah", "Svara Yahdikumullah", "Täck munnen vid nysning", "Dämpa gäspning"], "nl": ["Zeg Alhamdulillah bij niezen", "Anderen zeggen Yarhamukallah", "Antwoord Yahdikumullah", "Bedek je mond bij niezen", "Onderdruk geeuwen"], "el": ["Πες Αλχαμντουλιλλάχ όταν φτερνίζεσαι", "Σου λένε Γιαρχαμουκαλλάχ", "Απάντησε Γιαχντικουμουλλάχ", "Κάλυψε το στόμα", "Καταπίεσε το χασμουρητό"]},
     "hadith": {"ar": "قال النبي ﷺ: «إذا عطس أحدكم فليقل الحمد لله» — البخاري", "en": "The Prophet ﷺ said: \"When one of you sneezes, say Alhamdulillah\" — Bukhari", "de": "Der Prophet ﷺ sagte: \"Wenn einer von euch niest, sage Alhamdulillah\"", "fr": "Le Prophète ﷺ a dit: \"Quand l'un de vous éternue, dites Alhamdulillah\"", "tr": "Hz. Peygamber ﷺ buyurdu: \"Biriniz hapşırınca Elhamdülillah desin\"", "ru": "Пророк ﷺ сказал: «Когда чихнёте, скажите Альхамдулиллях»", "sv": "Profeten ﷺ sade: \"Säg Alhamdulillah vid nysning\"", "nl": "De Profeet ﷺ zei: \"Zeg Alhamdulillah als je niest\"", "el": "Ο Προφήτης ﷺ είπε: «Πείτε Αλχαμντουλιλλάχ όταν φτερνίζεστε»"},
    },
    {"id": 8, "emoji": "🚶", "title": {"ar": "آداب الطريق", "en": "Road & Street Etiquette", "de": "Straßenetikette", "fr": "Étiquette de la rue", "tr": "Yol Adabı", "ru": "Этикет дороги", "sv": "Vägetikett", "nl": "Straatetiquette", "el": "Εθιμοτυπία δρόμου"},
     "rules": {"ar": ["غضّ البصر", "كفّ الأذى عن الناس", "أزل الأذى من الطريق", "ردّ السلام", "أمر بالمعروف وانه عن المنكر"], "en": ["Lower your gaze", "Don't harm others", "Remove harm from the road", "Return greetings", "Enjoin good and forbid evil"], "de": ["Senke den Blick", "Schade niemandem", "Räume Hindernisse weg", "Erwidere Grüße", "Gebiete Gutes"], "fr": ["Baissez le regard", "Ne nuisez à personne", "Enlevez les obstacles", "Rendez les salutations", "Ordonnez le bien"], "tr": ["Gözünüzü sakının", "İnsanlara zarar vermeyin", "Yoldan eziyeti kaldırın", "Selamı alın", "İyiliği emredin kötülükten nehyedin"], "ru": ["Опускайте взгляд", "Не вредите другим", "Убирайте препятствия", "Отвечайте на приветствия", "Призывайте к добру"], "sv": ["Sänk blicken", "Skada inte andra", "Ta bort hinder", "Svara på hälsningar", "Påbjud gott"], "nl": ["Sla de blik neer", "Schaad anderen niet", "Ruim obstakels op", "Beantwoord groeten", "Beveel het goede"], "el": ["Χαμήλωσε το βλέμμα", "Μη βλάπτεις άλλους", "Απομάκρυνε εμπόδια", "Απάντα στους χαιρετισμούς", "Πρόσταξε το καλό"]},
     "hadith": {"ar": "قال النبي ﷺ: «إماطة الأذى عن الطريق صدقة» — متفق عليه", "en": "The Prophet ﷺ said: \"Removing harm from the road is charity\" — Agreed upon", "de": "Der Prophet ﷺ sagte: \"Hindernisse von der Straße zu räumen ist Sadaqa\"", "fr": "Le Prophète ﷺ a dit: \"Enlever un obstacle de la route est une aumône\"", "tr": "Hz. Peygamber ﷺ buyurdu: \"Yoldan eziyeti kaldırmak sadakadır\"", "ru": "Пророк ﷺ сказал: «Убрать вред с дороги — садака»", "sv": "Profeten ﷺ sade: \"Att ta bort hinder är sadaqah\"", "nl": "De Profeet ﷺ zei: \"Een obstakel verwijderen is sadaqah\"", "el": "Ο Προφήτης ﷺ είπε: «Η απομάκρυνση εμποδίου είναι σαντάκα»"},
    },
    {"id": 9, "emoji": "📚", "title": {"ar": "آداب طلب العلم", "en": "Seeking Knowledge Etiquette", "de": "Etikette des Wissenserwerbs", "fr": "Étiquette de la quête du savoir", "tr": "İlim Öğrenme Adabı", "ru": "Этикет поиска знаний", "sv": "Kunskapssökandets etikett", "nl": "Etiquette van kennisverwerving", "el": "Εθιμοτυπία αναζήτησης γνώσης"},
     "rules": {"ar": ["أخلص النية لله", "احترم المعلم", "اصبر وثابر", "اعمل بما تعلمت", "علّم غيرك"], "en": ["Purify your intention for Allah", "Respect the teacher", "Be patient and persistent", "Act upon what you learn", "Teach others"], "de": ["Reine Absicht für Allah", "Respektiere den Lehrer", "Sei geduldig", "Handle nach dem Gelernten", "Lehre andere"], "fr": ["Purifie ton intention", "Respecte le professeur", "Sois patient", "Agis selon ce que tu apprends", "Enseigne aux autres"], "tr": ["Niyetini Allah için halis kıl", "Hocana saygı göster", "Sabırlı ve azimli ol", "Öğrendiğinle amel et", "Başkalarına öğret"], "ru": ["Очисти намерение для Аллаха", "Уважай учителя", "Будь терпелив", "Действуй по знаниям", "Учи других"], "sv": ["Rena din avsikt för Allah", "Respektera läraren", "Var tålmodig", "Agera på vad du lär", "Lär andra"], "nl": ["Zuiver je intentie", "Respecteer de leraar", "Wees geduldig", "Handel naar wat je leert", "Onderwijs anderen"], "el": ["Καθάρισε την πρόθεσή σου", "Σεβάσου τον δάσκαλο", "Κάνε υπομονή", "Εφάρμοσε αυτά που μαθαίνεις", "Δίδαξε άλλους"]},
     "hadith": {"ar": "قال النبي ﷺ: «من سلك طريقاً يلتمس فيه علماً سهّل الله له طريقاً إلى الجنة» — صحيح مسلم", "en": "The Prophet ﷺ said: \"Whoever takes a path seeking knowledge, Allah makes easy for them a path to Paradise\" — Sahih Muslim", "de": "Der Prophet ﷺ sagte: \"Wer einen Weg zum Wissen geht, dem erleichtert Allah den Weg zum Paradies\"", "fr": "Le Prophète ﷺ a dit: \"Celui qui emprunte un chemin pour chercher la science, Allah lui facilite un chemin vers le Paradis\"", "tr": "Hz. Peygamber ﷺ buyurdu: \"Kim ilim için bir yola girerse Allah ona cennete giden yolu kolaylaştırır\"", "ru": "Пророк ﷺ сказал: «Кто встал на путь знаний, тому Аллах облегчит путь в Рай»", "sv": "Profeten ﷺ sade: \"Den som tar en väg för kunskap, Allah underlättar vägen till Paradiset\"", "nl": "De Profeet ﷺ zei: \"Wie een pad naar kennis bewandelt, Allah vergemakkelijkt het pad naar het Paradijs\"", "el": "Ο Προφήτης ﷺ είπε: «Όποιος ακολουθεί δρόμο γνώσης, ο Αλλάχ διευκολύνει τον δρόμο προς τον Παράδεισο»"},
    },
    {"id": 10, "emoji": "🤒", "title": {"ar": "آداب عيادة المريض", "en": "Visiting the Sick Etiquette", "de": "Krankenbesuch-Etikette", "fr": "Étiquette de visite du malade", "tr": "Hasta Ziyareti Adabı", "ru": "Этикет посещения больного", "sv": "Sjukbesöksetikett", "nl": "Ziekenbezoek-etiquette", "el": "Εθιμοτυπία επίσκεψης ασθενούς"},
     "rules": {"ar": ["زر المريض وادع له بالشفاء", "لا تطل الزيارة", "ادع له بالدعاء المأثور", "ارفع معنوياته", "اسأل عن حاله"], "en": ["Visit the sick and pray for healing", "Don't stay too long", "Recite the prophetic dua", "Lift their spirits", "Ask about their condition"], "de": ["Besuche den Kranken", "Bleibe nicht zu lang", "Lies das Dua", "Hebe die Stimmung", "Frage nach dem Befinden"], "fr": ["Visitez le malade", "Ne restez pas longtemps", "Récitez le dua", "Remontez le moral", "Demandez des nouvelles"], "tr": ["Hastayı ziyaret edip şifa dileyin", "Uzun kalmayın", "Peygamber duasını okuyun", "Moralini yükseltin", "Durumunu sorun"], "ru": ["Навестите больного", "Не задерживайтесь долго", "Прочитайте дуа", "Поднимите настроение", "Спросите о состоянии"], "sv": ["Besök den sjuke", "Stanna inte för länge", "Läs dua", "Lyft deras ande", "Fråga om deras tillstånd"], "nl": ["Bezoek de zieke", "Blijf niet te lang", "Lees het dua", "Vrolijk hem/haar op", "Vraag naar zijn toestand"], "el": ["Επισκέψου τον ασθενή", "Μη μένεις πολύ", "Διάβασε ντουά", "Ανέβασε το ηθικό", "Ρώτα για την κατάστασή του"]},
     "hadith": {"ar": "قال النبي ﷺ: «إذا دخلتم على المريض فنفّسوا له في أجله» — رواه الترمذي", "en": "The Prophet ﷺ said: \"When visiting the sick, give them hope\" — Tirmidhi", "de": "Der Prophet ﷺ sagte: \"Gebt dem Kranken Hoffnung\"", "fr": "Le Prophète ﷺ a dit: \"Donnez espoir au malade\"", "tr": "Hz. Peygamber ﷺ buyurdu: \"Hastayı ziyaret ettiğinizde ona ümit verin\"", "ru": "Пророк ﷺ сказал: «Дайте больному надежду»", "sv": "Profeten ﷺ sade: \"Ge den sjuke hopp\"", "nl": "De Profeet ﷺ zei: \"Geef de zieke hoop\"", "el": "Ο Προφήτης ﷺ είπε: «Δώστε ελπίδα στον ασθενή»"},
    },
]

# ═══════════════════════════════════════════════════════════════
# TEACHING METHOD DESCRIPTORS (2026 Modern Methods)
# ═══════════════════════════════════════════════════════════════

TEACHING_METHODS = {
    "visual_audio": {"ar": "تعلّم بصري وسمعي", "en": "Visual & Audio Learning", "icon": "👁️🔊"},
    "interactive_diagram": {"ar": "مخطط تفاعلي", "en": "Interactive Diagram", "icon": "📊"},
    "tracing": {"ar": "تتبع الحروف", "en": "Letter Tracing", "icon": "✍️"},
    "game": {"ar": "تعلّم باللعب", "en": "Game-Based Learning", "icon": "🎮"},
    "audio_match": {"ar": "مطابقة صوتية", "en": "Audio Matching", "icon": "🔊"},
    "assessment": {"ar": "اختبار تقييمي", "en": "Assessment", "icon": "🏆"},
    "story_based": {"ar": "تعلّم بالقصص", "en": "Story-Based Learning", "icon": "📖"},
    "practice_based": {"ar": "تعلّم بالتطبيق", "en": "Practice-Based", "icon": "🎯"},
    "spaced_repetition": {"ar": "التكرار المتباعد", "en": "Spaced Repetition", "icon": "🔄"},
    "micro_learning": {"ar": "تعلّم مصغّر", "en": "Micro-Learning (5 min)", "icon": "⚡"},
}

# Badge system for gamification
ACADEMY_BADGES = [
    {"id": "first_letter", "emoji": "🔤", "title": {"ar": "أول حرف", "en": "First Letter"}, "condition": "complete_lesson_1"},
    {"id": "alphabet_master", "emoji": "📖", "title": {"ar": "سيد الأبجدية", "en": "Alphabet Master"}, "condition": "complete_nooraniya_level_1"},
    {"id": "quran_reader", "emoji": "📖", "title": {"ar": "قارئ القرآن", "en": "Quran Reader"}, "condition": "complete_nooraniya_level_6"},
    {"id": "tajweed_expert", "emoji": "🎓", "title": {"ar": "خبير التجويد", "en": "Tajweed Expert"}, "condition": "complete_nooraniya_level_7"},
    {"id": "tawheed_star", "emoji": "☝️", "title": {"ar": "نجم التوحيد", "en": "Tawheed Star"}, "condition": "complete_aqeedah_level_1"},
    {"id": "names_of_allah", "emoji": "✨", "title": {"ar": "حافظ الأسماء", "en": "Names Memorizer"}, "condition": "complete_aqeedah_level_2"},
    {"id": "prayer_champion", "emoji": "🕌", "title": {"ar": "بطل الصلاة", "en": "Prayer Champion"}, "condition": "complete_fiqh_level_2"},
    {"id": "seerah_scholar", "emoji": "📜", "title": {"ar": "عالم السيرة", "en": "Seerah Scholar"}, "condition": "complete_seerah"},
    {"id": "adab_hero", "emoji": "🌟", "title": {"ar": "بطل الآداب", "en": "Adab Hero"}, "condition": "complete_all_adab"},
    {"id": "digital_shield", "emoji": "🛡️", "title": {"ar": "درع الوعي", "en": "Digital Shield"}, "condition": "complete_digital_shield"},
    {"id": "noor_graduate", "emoji": "🎓", "title": {"ar": "خريج أكاديمية نور", "en": "Noor Academy Graduate"}, "condition": "complete_all_tracks"},
]

"""
Noor Academy V2 — Fiqh (Islamic Jurisprudence) Complete Content
================================================================
40 lessons across 4 levels with full multilingual content
"""

# ═══════════════════════════════════════════════════════════════
# FIQH LEVEL 1: PURIFICATION (TAHARAH) — 10 lessons
# ═══════════════════════════════════════════════════════════════

FIQH_L1_LESSONS = [
    {
        "id": 1, "level": 1, "lesson": 1, "emoji": "💧",
        "title": {"ar": "الطهارة — مقدمة", "en": "Purification — Introduction", "de": "Reinigung — Einführung", "fr": "Purification — Introduction", "tr": "Taharet — Giriş", "ru": "Очищение — Введение", "sv": "Rening — Introduktion", "nl": "Reiniging — Introductie", "el": "Κάθαρση — Εισαγωγή"},
        "method": "conceptual",
        "content": {
            "intro": {"ar": "الطهارة شرط لصحة الصلاة، وهي من أهم أحكام الإسلام", "en": "Purification is a condition for valid prayer, and it's one of the most important rulings in Islam"},
            "types": [
                {"name": {"ar": "الطهارة من الحدث الأصغر", "en": "Minor ritual impurity"}, "method": {"ar": "الوضوء", "en": "Wudu (ablution)"}},
                {"name": {"ar": "الطهارة من الحدث الأكبر", "en": "Major ritual impurity"}, "method": {"ar": "الغسل", "en": "Ghusl (full body wash)"}},
                {"name": {"ar": "الطهارة من النجاسة", "en": "Physical impurity"}, "method": {"ar": "إزالة النجاسة بالماء", "en": "Removing impurity with water"}}
            ],
            "hadith": {"ar": "قال النبي ﷺ: «لا تُقبل صلاة بغير طهور»", "en": "The Prophet ﷺ said: 'No prayer is accepted without purification'"}
        },
        "quiz": {"type": "select", "question": {"ar": "ما شرط صحة الصلاة؟", "en": "What is the condition for valid prayer?"}, "correct": {"ar": "الطهارة", "en": "Purification"}, "options": [{"ar": "الطهارة", "en": "Purification"}, {"ar": "الأكل", "en": "Eating"}, {"ar": "النوم", "en": "Sleeping"}]},
        "xp": 20
    },
    {
        "id": 2, "level": 1, "lesson": 2, "emoji": "🚿",
        "title": {"ar": "الوضوء — الأركان", "en": "Wudu — The Pillars", "de": "Wudu — Die Säulen", "fr": "Ablution — Les piliers", "tr": "Abdest — Farzları", "ru": "Вуду — Столпы", "sv": "Wudu — Pelarna", "nl": "Wudu — De pilaren", "el": "Γουντού — Πυλώνες"},
        "method": "practice-based",
        "content": {
            "steps": [
                {"num": 1, "action": {"ar": "النية في القلب", "en": "Intention in the heart"}, "detail": {"ar": "ننوي الوضوء لله تعالى", "en": "Intend wudu for Allah's sake"}},
                {"num": 2, "action": {"ar": "غسل الوجه", "en": "Wash the face"}, "detail": {"ar": "من منبت الشعر إلى الذقن", "en": "From hairline to chin"}},
                {"num": 3, "action": {"ar": "غسل اليدين إلى المرفقين", "en": "Wash hands to elbows"}, "detail": {"ar": "البدء باليمنى", "en": "Start with the right"}},
                {"num": 4, "action": {"ar": "مسح الرأس", "en": "Wipe the head"}, "detail": {"ar": "بالماء مرة واحدة", "en": "With water once"}},
                {"num": 5, "action": {"ar": "غسل الرجلين إلى الكعبين", "en": "Wash feet to ankles"}, "detail": {"ar": "البدء باليمنى", "en": "Start with the right"}}
            ],
            "sunnah": {"ar": "التسمية، السواك، غسل الكفين، المضمضة، الاستنشاق", "en": "Saying Bismillah, Siwak, washing palms, rinsing mouth, sniffing water"}
        },
        "quiz": {"type": "sequence", "question": {"ar": "رتّب أركان الوضوء", "en": "Arrange the pillars of wudu"}, "correct_order": ["النية", "غسل الوجه", "غسل اليدين", "مسح الرأس", "غسل الرجلين"]},
        "xp": 25
    },
    {
        "id": 3, "level": 1, "lesson": 3, "emoji": "❌",
        "title": {"ar": "نواقض الوضوء", "en": "What Breaks Wudu", "de": "Was Wudu bricht", "fr": "Ce qui annule les ablutions", "tr": "Abdesti Bozan Şeyler", "ru": "Что нарушает Вуду", "sv": "Vad som bryter Wudu", "nl": "Wat Wudu verbreekt", "el": "Τι ακυρώνει Γουντού"},
        "method": "conceptual",
        "content": {
            "nullifiers": [
                {"ar": "الخارج من السبيلين", "en": "Anything exiting from the private parts"},
                {"ar": "النوم العميق", "en": "Deep sleep"},
                {"ar": "زوال العقل", "en": "Loss of consciousness"},
                {"ar": "أكل لحم الجِمال عند بعض العلماء", "en": "Eating camel meat (according to some scholars)"}
            ],
            "tip": {"ar": "إذا شككت هل انتقض وضوؤك أم لا، فالأصل بقاء الوضوء", "en": "If you doubt whether your wudu broke, the default is it remains valid"}
        },
        "quiz": {"type": "select", "question": {"ar": "أي مما يلي ينقض الوضوء؟", "en": "Which of the following breaks wudu?"}, "correct": {"ar": "النوم العميق", "en": "Deep sleep"}, "options": [{"ar": "النوم العميق", "en": "Deep sleep"}, {"ar": "الأكل", "en": "Eating"}, {"ar": "الشرب", "en": "Drinking"}]},
        "xp": 20
    },
    {
        "id": 4, "level": 1, "lesson": 4, "emoji": "🏜️",
        "title": {"ar": "التيمم — البديل عن الماء", "en": "Tayammum — Alternative to Water", "de": "Tayammum — Alternative zum Wasser", "fr": "Tayammum — Alternative à l'eau", "tr": "Teyemmüm — Suya Alternatif", "ru": "Таяммум — Альтернатива воде", "sv": "Tayammum — Alternativ till vatten", "nl": "Tayammum — Alternatief voor water", "el": "Ταγιαμμούμ — Εναλλακτικά νερού"},
        "method": "practice-based",
        "content": {
            "when": {"ar": "عند عدم وجود الماء أو عدم القدرة على استعماله", "en": "When water is unavailable or cannot be used"},
            "steps": [
                {"num": 1, "action": {"ar": "النية", "en": "Intention"}},
                {"num": 2, "action": {"ar": "ضرب الكفين على التراب الطاهر", "en": "Strike palms on clean earth"}},
                {"num": 3, "action": {"ar": "مسح الوجه", "en": "Wipe the face"}},
                {"num": 4, "action": {"ar": "مسح الكفين", "en": "Wipe the palms"}}
            ],
            "verse": {"ar": "﴿فَتَيَمَّمُوا صَعِيدًا طَيِّبًا﴾", "en": "\"Then seek clean earth\" (Quran 4:43)"}
        },
        "quiz": {"type": "select", "question": {"ar": "متى نتيمم؟", "en": "When do we perform Tayammum?"}, "correct": {"ar": "عند عدم وجود الماء", "en": "When water is unavailable"}, "options": [{"ar": "عند عدم وجود الماء", "en": "When water is unavailable"}, {"ar": "دائماً", "en": "Always"}, {"ar": "في الصيف فقط", "en": "Only in summer"}]},
        "xp": 20
    },
    {
        "id": 5, "level": 1, "lesson": 5, "emoji": "🛁",
        "title": {"ar": "الغسل — متى وكيف", "en": "Ghusl — When and How", "de": "Ghusl — Wann und Wie", "fr": "Ghusl — Quand et Comment", "tr": "Gusül — Ne Zaman ve Nasıl", "ru": "Гусль — Когда и Как", "sv": "Ghusl — När och Hur", "nl": "Ghusl — Wanneer en Hoe", "el": "Γκουσλ — Πότε και Πώς"},
        "method": "practice-based",
        "content": {
            "obligatory_cases": [
                {"ar": "الجنابة", "en": "Janabah (major impurity)"},
                {"ar": "الحيض للمرأة", "en": "Menstruation (for women)"},
                {"ar": "النفاس", "en": "Postpartum bleeding"}
            ],
            "recommended": [
                {"ar": "غسل الجمعة", "en": "Friday ghusl"},
                {"ar": "غسل العيدين", "en": "Eid ghusl"},
                {"ar": "غسل الإحرام", "en": "Ihram ghusl"}
            ],
            "method": {"ar": "النية ثم غسل اليدين ثم الوضوء ثم إفاضة الماء على الجسم كله", "en": "Intention, wash hands, perform wudu, then pour water over entire body"}
        },
        "quiz": {"type": "select", "question": {"ar": "أي من التالي يوجب الغسل؟", "en": "Which requires ghusl?"}, "correct": {"ar": "الجنابة", "en": "Janabah"}, "options": [{"ar": "الجنابة", "en": "Janabah"}, {"ar": "الأكل", "en": "Eating"}, {"ar": "النوم", "en": "Sleeping"}]},
        "xp": 20
    },
    {
        "id": 6, "level": 1, "lesson": 6, "emoji": "💦",
        "title": {"ar": "أنواع المياه", "en": "Types of Water", "de": "Arten von Wasser", "fr": "Types d'eau", "tr": "Su Çeşitleri", "ru": "Виды воды", "sv": "Typer av vatten", "nl": "Soorten water", "el": "Είδη νερού"},
        "method": "conceptual",
        "content": {
            "types": [
                {"name": {"ar": "الماء الطهور", "en": "Pure water"}, "ruling": {"ar": "طاهر في نفسه مُطهّر لغيره — يصح الوضوء به", "en": "Pure itself and purifies others — valid for wudu"}},
                {"name": {"ar": "الماء النجس", "en": "Impure water"}, "ruling": {"ar": "تغيّر لونه أو طعمه أو رائحته بالنجاسة — لا يصح الوضوء به", "en": "Changed in color, taste or smell by impurity — not valid for wudu"}}
            ],
            "verse": {"ar": "﴿وَأَنزَلْنَا مِنَ السَّمَاءِ مَاءً طَهُورًا﴾", "en": "\"And We sent down from the sky purifying water\" (Quran 25:48)"}
        },
        "quiz": {"type": "select", "question": {"ar": "أي ماء يصح للوضوء؟", "en": "Which water is valid for wudu?"}, "correct": {"ar": "الماء الطهور", "en": "Pure water"}, "options": [{"ar": "الماء الطهور", "en": "Pure water"}, {"ar": "الماء النجس", "en": "Impure water"}, {"ar": "العصير", "en": "Juice"}]},
        "xp": 20
    },
    {
        "id": 7, "level": 1, "lesson": 7, "emoji": "🧹",
        "title": {"ar": "إزالة النجاسة", "en": "Removing Impurities", "de": "Unreinheiten entfernen", "fr": "Enlever les impuretés", "tr": "Necaset Temizleme", "ru": "Удаление нечистот", "sv": "Avlägsna orenheter", "nl": "Onzuiverheden verwijderen", "el": "Αφαίρεση ακαθαρσιών"},
        "method": "conceptual",
        "content": {
            "types": [
                {"name": {"ar": "البول", "en": "Urine"}, "removal": {"ar": "يُغسل بالماء", "en": "Washed with water"}},
                {"name": {"ar": "الدم", "en": "Blood"}, "removal": {"ar": "يُغسل بالماء البارد", "en": "Washed with cold water"}},
                {"name": {"ar": "نجاسة الكلب", "en": "Dog impurity"}, "removal": {"ar": "سبع غسلات إحداها بالتراب", "en": "Seven washes, one with earth"}}
            ],
            "rule": {"ar": "الأصل في الأشياء الطهارة حتى يثبت العكس", "en": "The default state of things is purity until proven otherwise"}
        },
        "quiz": {"type": "true_false", "question": {"ar": "الأصل في الأشياء الطهارة", "en": "The default state of things is purity"}, "correct": True},
        "xp": 20
    },
    {
        "id": 8, "level": 1, "lesson": 8, "emoji": "🪥",
        "title": {"ar": "سنن الفطرة", "en": "Natural Hygiene Practices", "de": "Natürliche Hygienepraktiken", "fr": "Pratiques d'hygiène naturelles", "tr": "Fıtrat Sünnetleri", "ru": "Естественная гигиена", "sv": "Naturlig hygien", "nl": "Natuurlijke hygiëne", "el": "Φυσική υγιεινή"},
        "method": "practice-based",
        "content": {
            "practices": [
                {"ar": "السواك — تنظيف الأسنان", "en": "Siwak — cleaning teeth"},
                {"ar": "قص الأظافر", "en": "Trimming nails"},
                {"ar": "نتف الإبط", "en": "Removing armpit hair"},
                {"ar": "الختان", "en": "Circumcision"},
                {"ar": "الاستنجاء", "en": "Cleaning after using toilet"}
            ],
            "hadith": {"ar": "قال النبي ﷺ: «خمس من الفطرة: الختان والاستحداد وتقليم الأظافر ونتف الإبط وقص الشارب»", "en": "The Prophet ﷺ said: 'Five are from natural hygiene: circumcision, shaving pubic hair, trimming nails, removing armpit hair, and trimming the mustache'"}
        },
        "quiz": {"type": "select", "question": {"ar": "أي مما يلي من سنن الفطرة؟", "en": "Which is from natural hygiene?"}, "correct": {"ar": "قص الأظافر", "en": "Trimming nails"}, "options": [{"ar": "قص الأظافر", "en": "Trimming nails"}, {"ar": "النوم كثيراً", "en": "Sleeping a lot"}, {"ar": "الأكل كثيراً", "en": "Eating a lot"}]},
        "xp": 20
    },
    {
        "id": 9, "level": 1, "lesson": 9, "emoji": "🚻",
        "title": {"ar": "آداب قضاء الحاجة", "en": "Etiquette of Using the Restroom", "de": "Toilettenregeln", "fr": "Règles des toilettes", "tr": "Tuvalet Adabı", "ru": "Этикет туалета", "sv": "Toalettregler", "nl": "Toiletregels", "el": "Κανόνες τουαλέτας"},
        "method": "practice-based",
        "content": {
            "etiquettes": [
                {"ar": "الدخول بالرجل اليسرى", "en": "Enter with left foot"},
                {"ar": "قول: بسم الله اللهم إني أعوذ بك من الخبث والخبائث", "en": "Say: Bismillah, O Allah I seek refuge in You from evil"},
                {"ar": "عدم استقبال القبلة أو استدبارها", "en": "Don't face or turn back to Qibla"},
                {"ar": "الاستنجاء بالماء أو الاستجمار", "en": "Clean with water or stones"},
                {"ar": "الخروج بالرجل اليمنى", "en": "Exit with right foot"},
                {"ar": "قول: غفرانك", "en": "Say: Ghufranaka (Your forgiveness)"}
            ]
        },
        "quiz": {"type": "select", "question": {"ar": "بأي رجل ندخل الحمام؟", "en": "Which foot do we enter restroom with?"}, "correct": {"ar": "اليسرى", "en": "Left"}, "options": [{"ar": "اليسرى", "en": "Left"}, {"ar": "اليمنى", "en": "Right"}, {"ar": "أي رجل", "en": "Either"}]},
        "xp": 20
    },
    {
        "id": 10, "level": 1, "lesson": 10, "emoji": "🏆",
        "title": {"ar": "اختبار الطهارة — المستوى الأول", "en": "Purification Assessment — Level 1", "de": "Reinigung Bewertung — Stufe 1", "fr": "Évaluation Purification — Niveau 1", "tr": "Taharet Değerlendirmesi — Seviye 1", "ru": "Тест по Очищению — Уровень 1", "sv": "Rening bedömning — Nivå 1", "nl": "Reiniging toets — Niveau 1", "el": "Αξιολόγηση Κάθαρσης — Επίπεδο 1"},
        "method": "assessment",
        "content": {"sections": ["wudu", "tayammum", "ghusl", "water_types", "impurities"], "pass_score": 75},
        "quiz": {"type": "comprehensive", "total_questions": 20},
        "xp": 50
    },
]

# ═══════════════════════════════════════════════════════════════
# FIQH LEVEL 2: PRAYER (SALAH) — 12 lessons
# ═══════════════════════════════════════════════════════════════

FIQH_L2_LESSONS = [
    {
        "id": 11, "level": 2, "lesson": 1, "emoji": "🕌",
        "title": {"ar": "الصلاة — مكانتها في الإسلام", "en": "Prayer — Its Place in Islam", "de": "Gebet — Seine Stellung im Islam", "fr": "Prière — Sa place en Islam", "tr": "Namaz — İslam'daki Yeri", "ru": "Молитва — Её место в Исламе", "sv": "Bön — Dess plats i Islam", "nl": "Gebed — Zijn plaats in de Islam", "el": "Προσευχή — Θέση στο Ισλάμ"},
        "method": "conceptual",
        "content": {
            "importance": {"ar": "الصلاة عمود الدين وأول ما يُحاسب عليه العبد يوم القيامة", "en": "Prayer is the pillar of religion and the first thing a person is judged on, on Judgment Day"},
            "five_prayers": [
                {"name": {"ar": "الفجر", "en": "Fajr"}, "rakaat": 2, "time": {"ar": "من طلوع الفجر إلى شروق الشمس", "en": "From dawn to sunrise"}},
                {"name": {"ar": "الظهر", "en": "Dhuhr"}, "rakaat": 4, "time": {"ar": "من زوال الشمس إلى وقت العصر", "en": "From noon to Asr time"}},
                {"name": {"ar": "العصر", "en": "Asr"}, "rakaat": 4, "time": {"ar": "من وقت العصر إلى غروب الشمس", "en": "From Asr time to sunset"}},
                {"name": {"ar": "المغرب", "en": "Maghrib"}, "rakaat": 3, "time": {"ar": "من غروب الشمس إلى مغيب الشفق", "en": "From sunset to twilight"}},
                {"name": {"ar": "العشاء", "en": "Isha"}, "rakaat": 4, "time": {"ar": "من مغيب الشفق إلى نصف الليل", "en": "From twilight to midnight"}}
            ],
            "hadith": {"ar": "قال النبي ﷺ: «العهد الذي بيننا وبينهم الصلاة فمن تركها فقد كفر»", "en": "The Prophet ﷺ said: 'The covenant between us and them is prayer; whoever abandons it has disbelieved'"}
        },
        "quiz": {"type": "select", "question": {"ar": "كم عدد الصلوات المفروضة؟", "en": "How many obligatory prayers are there?"}, "correct": "5", "options": ["3", "4", "5", "7"]},
        "xp": 25
    },
    {
        "id": 12, "level": 2, "lesson": 2, "emoji": "🧭",
        "title": {"ar": "شروط الصلاة", "en": "Conditions of Prayer", "de": "Bedingungen des Gebets", "fr": "Conditions de la prière", "tr": "Namazın Şartları", "ru": "Условия молитвы", "sv": "Bönens villkor", "nl": "Voorwaarden van het gebed", "el": "Συνθήκες προσευχής"},
        "method": "conceptual",
        "content": {
            "conditions": [
                {"ar": "الإسلام", "en": "Being Muslim"},
                {"ar": "العقل", "en": "Sanity"},
                {"ar": "التمييز", "en": "Age of discernment"},
                {"ar": "دخول الوقت", "en": "Time has entered"},
                {"ar": "الطهارة", "en": "Purification"},
                {"ar": "استقبال القبلة", "en": "Facing the Qibla"},
                {"ar": "ستر العورة", "en": "Covering the awrah"},
                {"ar": "النية", "en": "Intention"}
            ]
        },
        "quiz": {"type": "select", "question": {"ar": "أي اتجاه نستقبل في الصلاة؟", "en": "Which direction do we face in prayer?"}, "correct": {"ar": "القبلة (الكعبة)", "en": "Qibla (Ka'bah)"}, "options": [{"ar": "القبلة (الكعبة)", "en": "Qibla"}, {"ar": "الشمال", "en": "North"}, {"ar": "أي اتجاه", "en": "Any direction"}]},
        "xp": 25
    },
    {
        "id": 13, "level": 2, "lesson": 3, "emoji": "🙏",
        "title": {"ar": "أركان الصلاة", "en": "Pillars of Prayer", "de": "Säulen des Gebets", "fr": "Piliers de la prière", "tr": "Namazın Rükünleri", "ru": "Столпы молитвы", "sv": "Bönens pelare", "nl": "Pilaren van het gebed", "el": "Πυλώνες προσευχής"},
        "method": "practice-based",
        "content": {
            "pillars": [
                {"ar": "القيام مع القدرة", "en": "Standing if able"},
                {"ar": "تكبيرة الإحرام", "en": "Opening Takbeer"},
                {"ar": "قراءة الفاتحة", "en": "Reading Al-Fatiha"},
                {"ar": "الركوع", "en": "Bowing (Ruku)"},
                {"ar": "الاعتدال من الركوع", "en": "Rising from bowing"},
                {"ar": "السجود", "en": "Prostration (Sujud)"},
                {"ar": "الجلوس بين السجدتين", "en": "Sitting between prostrations"},
                {"ar": "التشهد الأخير", "en": "Final Tashahhud"},
                {"ar": "التسليم", "en": "Tasleem (Salam)"}
            ]
        },
        "quiz": {"type": "select", "question": {"ar": "ما أول ركن في الصلاة بعد القيام؟", "en": "What is the first pillar after standing?"}, "correct": {"ar": "تكبيرة الإحرام", "en": "Opening Takbeer"}, "options": [{"ar": "تكبيرة الإحرام", "en": "Opening Takbeer"}, {"ar": "الركوع", "en": "Bowing"}, {"ar": "السجود", "en": "Prostration"}]},
        "xp": 25
    },
    {
        "id": 14, "level": 2, "lesson": 4, "emoji": "📿",
        "title": {"ar": "صفة الصلاة — خطوة بخطوة", "en": "How to Pray — Step by Step", "de": "Wie man betet — Schritt für Schritt", "fr": "Comment prier — Étape par étape", "tr": "Namaz Nasıl Kılınır — Adım Adım", "ru": "Как молиться — Шаг за шагом", "sv": "Hur man ber — Steg för steg", "nl": "Hoe te bidden — Stap voor stap", "el": "Πώς προσευχόμαστε — Βήμα βήμα"},
        "method": "practice-based",
        "content": {
            "steps": [
                {"num": 1, "action": {"ar": "الوقوف واستقبال القبلة", "en": "Stand facing Qibla"}},
                {"num": 2, "action": {"ar": "تكبيرة الإحرام: الله أكبر", "en": "Say Allahu Akbar"}},
                {"num": 3, "action": {"ar": "قراءة دعاء الاستفتاح ثم الفاتحة", "en": "Recite opening supplication then Al-Fatiha"}},
                {"num": 4, "action": {"ar": "الركوع: سبحان ربي العظيم", "en": "Bow: Subhana Rabbiyal Adheem"}},
                {"num": 5, "action": {"ar": "الرفع: سمع الله لمن حمده", "en": "Rise: Sami Allahu liman hamidah"}},
                {"num": 6, "action": {"ar": "السجود: سبحان ربي الأعلى", "en": "Prostrate: Subhana Rabbiyal A'la"}},
                {"num": 7, "action": {"ar": "الجلوس بين السجدتين: رب اغفر لي", "en": "Sit: Rabbi ighfir li"}},
                {"num": 8, "action": {"ar": "السجود الثاني", "en": "Second prostration"}},
                {"num": 9, "action": {"ar": "التشهد والتسليم", "en": "Tashahhud and Salam"}}
            ]
        },
        "quiz": {"type": "select", "question": {"ar": "ماذا نقول في الركوع؟", "en": "What do we say in bowing?"}, "correct": {"ar": "سبحان ربي العظيم", "en": "Subhana Rabbiyal Adheem"}, "options": [{"ar": "سبحان ربي العظيم", "en": "Subhana Rabbiyal Adheem"}, {"ar": "سبحان ربي الأعلى", "en": "Subhana Rabbiyal A'la"}, {"ar": "الله أكبر", "en": "Allahu Akbar"}]},
        "xp": 30
    },
    {
        "id": 15, "level": 2, "lesson": 5, "emoji": "🤲",
        "title": {"ar": "سنن الصلاة ومستحباتها", "en": "Sunnah Acts of Prayer", "de": "Sunnah-Handlungen des Gebets", "fr": "Actes Sunnah de la prière", "tr": "Namazın Sünnetleri", "ru": "Сунна молитвы", "sv": "Bönens Sunnah", "nl": "Soennah van het gebed", "el": "Σούνα προσευχής"},
        "method": "conceptual",
        "content": {
            "sunnahs": [
                {"ar": "رفع اليدين عند التكبير", "en": "Raising hands during Takbeer"},
                {"ar": "وضع اليد اليمنى على اليسرى", "en": "Placing right hand over left"},
                {"ar": "دعاء الاستفتاح", "en": "Opening supplication"},
                {"ar": "قراءة سورة بعد الفاتحة", "en": "Reciting a surah after Al-Fatiha"},
                {"ar": "التأمين بعد الفاتحة", "en": "Saying Ameen after Al-Fatiha"},
                {"ar": "التسبيح ثلاثاً في الركوع والسجود", "en": "Saying Tasbeeh three times in bowing and prostration"}
            ]
        },
        "quiz": {"type": "true_false", "question": {"ar": "من السنة قراءة سورة بعد الفاتحة", "en": "It's Sunnah to recite a surah after Al-Fatiha"}, "correct": True},
        "xp": 20
    },
    {
        "id": 16, "level": 2, "lesson": 6, "emoji": "⚠️",
        "title": {"ar": "مبطلات الصلاة", "en": "What Invalidates Prayer", "de": "Was das Gebet ungültig macht", "fr": "Ce qui invalide la prière", "tr": "Namazı Bozan Şeyler", "ru": "Что нарушает молитву", "sv": "Vad som ogiltigförklarar bön", "nl": "Wat gebed ongeldig maakt", "el": "Τι ακυρώνει την προσευχή"},
        "method": "conceptual",
        "content": {
            "invalidators": [
                {"ar": "الكلام عمداً", "en": "Speaking intentionally"},
                {"ar": "الأكل والشرب", "en": "Eating or drinking"},
                {"ar": "الحركة الكثيرة المتوالية", "en": "Excessive continuous movement"},
                {"ar": "ترك ركن عمداً", "en": "Intentionally omitting a pillar"},
                {"ar": "الضحك", "en": "Laughing"},
                {"ar": "انتقاض الوضوء", "en": "Wudu breaking"}
            ]
        },
        "quiz": {"type": "select", "question": {"ar": "أي مما يلي يُبطل الصلاة؟", "en": "Which invalidates prayer?"}, "correct": {"ar": "الكلام عمداً", "en": "Speaking intentionally"}, "options": [{"ar": "الكلام عمداً", "en": "Speaking"}, {"ar": "السعال", "en": "Coughing"}, {"ar": "البكاء من خشية الله", "en": "Crying from fear of Allah"}]},
        "xp": 20
    },
    {
        "id": 17, "level": 2, "lesson": 7, "emoji": "👥",
        "title": {"ar": "صلاة الجماعة", "en": "Congregational Prayer", "de": "Gemeinschaftsgebet", "fr": "Prière en congrégation", "tr": "Cemaatle Namaz", "ru": "Коллективная молитва", "sv": "Gemensam bön", "nl": "Gezamenlijk gebed", "el": "Συλλογική προσευχή"},
        "method": "conceptual",
        "content": {
            "virtue": {"ar": "صلاة الجماعة أفضل من صلاة الفرد بسبع وعشرين درجة", "en": "Congregational prayer is 27 times better than praying alone"},
            "rules": [
                {"ar": "الإمام يقف أمام المأمومين", "en": "Imam stands in front of followers"},
                {"ar": "المأمومون يقفون خلف الإمام في صفوف مستوية", "en": "Followers stand behind imam in straight rows"},
                {"ar": "نتابع الإمام ولا نسبقه", "en": "We follow the imam, don't precede him"}
            ]
        },
        "quiz": {"type": "select", "question": {"ar": "صلاة الجماعة أفضل بكم درجة؟", "en": "Congregational prayer is better by how many degrees?"}, "correct": "27", "options": ["10", "25", "27", "50"]},
        "xp": 25
    },
    {
        "id": 18, "level": 2, "lesson": 8, "emoji": "🌅",
        "title": {"ar": "صلاة الجمعة والعيدين", "en": "Friday Prayer and Eid Prayer", "de": "Freitagsgebet und Eidgebet", "fr": "Prière du vendredi et de l'Aïd", "tr": "Cuma ve Bayram Namazı", "ru": "Пятничная молитва и молитва Ид", "sv": "Fredagsbön och Eid-bön", "nl": "Vrijdaggebed en Eid-gebed", "el": "Παρασκευινή και Εΐντ προσευχή"},
        "method": "conceptual",
        "content": {
            "jumuah": {"ar": "صلاة الجمعة فرض على كل مسلم بالغ ذكر — ركعتان بعد خطبتين", "en": "Friday prayer is obligatory for every adult Muslim male — 2 rak'ahs after 2 sermons"},
            "eid": {"ar": "صلاة العيد سنة مؤكدة — ركعتان مع تكبيرات زائدة", "en": "Eid prayer is a confirmed Sunnah — 2 rak'ahs with extra Takbeers"}
        },
        "quiz": {"type": "select", "question": {"ar": "كم ركعة صلاة الجمعة؟", "en": "How many rak'ahs in Friday prayer?"}, "correct": "2", "options": ["2", "3", "4"]},
        "xp": 25
    },
    {
        "id": 19, "level": 2, "lesson": 9, "emoji": "🌙",
        "title": {"ar": "صلاة التراويح والتهجد", "en": "Taraweeh and Tahajjud", "de": "Tarawih und Tahajjud", "fr": "Tarawih et Tahajjud", "tr": "Teravih ve Teheccüd", "ru": "Таравих и Тахаджуд", "sv": "Tarawih och Tahajjud", "nl": "Tarawih en Tahajjud", "el": "Ταραουίχ και Ταχατζούντ"},
        "method": "conceptual",
        "content": {
            "taraweeh": {"ar": "صلاة التراويح سنة مؤكدة في رمضان — تُصلى بعد العشاء جماعة في المسجد", "en": "Taraweeh is a confirmed Sunnah in Ramadan — prayed after Isha in congregation at the mosque"},
            "tahajjud": {"ar": "صلاة التهجد في آخر الليل — من أفضل الصلوات بعد الفريضة", "en": "Tahajjud at the last third of the night — among the best prayers after obligatory ones"},
            "hadith": {"ar": "قال النبي ﷺ: «من قام رمضان إيماناً واحتساباً غُفر له ما تقدم من ذنبه»", "en": "The Prophet ﷺ said: 'Whoever stands in prayer during Ramadan with faith and seeking reward, his past sins will be forgiven'"}
        },
        "quiz": {"type": "select", "question": {"ar": "متى تُصلى التراويح؟", "en": "When is Taraweeh prayed?"}, "correct": {"ar": "في رمضان بعد العشاء", "en": "In Ramadan after Isha"}, "options": [{"ar": "في رمضان بعد العشاء", "en": "Ramadan after Isha"}, {"ar": "كل يوم", "en": "Every day"}, {"ar": "في الصباح", "en": "In the morning"}]},
        "xp": 25
    },
    {
        "id": 20, "level": 2, "lesson": 10, "emoji": "🙇",
        "title": {"ar": "سجود السهو والتلاوة", "en": "Prostration of Forgetfulness and Recitation", "de": "Vergesslichkeitsniederwerfung", "fr": "Prosternation d'oubli", "tr": "Sehiv ve Tilâvet Secdesi", "ru": "Суджуд ас-Сахв", "sv": "Sujud as-Sahw", "nl": "Sujud as-Sahw", "el": "Σουτζούντ ας-Σάχου"},
        "method": "conceptual",
        "content": {
            "sahw": {"ar": "سجود السهو: سجدتان عند الزيادة أو النقص أو الشك في الصلاة", "en": "Sujud as-Sahw: two prostrations when adding, omitting or doubting in prayer"},
            "tilawah": {"ar": "سجود التلاوة: سجدة واحدة عند قراءة آية فيها سجدة", "en": "Sujud at-Tilawah: one prostration when reciting an ayah of prostration"}
        },
        "quiz": {"type": "select", "question": {"ar": "متى نسجد سجود السهو؟", "en": "When do we perform Sujud as-Sahw?"}, "correct": {"ar": "عند الزيادة أو النقص في الصلاة", "en": "When adding or omitting in prayer"}, "options": [{"ar": "عند الزيادة أو النقص في الصلاة", "en": "Adding/omitting"}, {"ar": "كل صلاة", "en": "Every prayer"}, {"ar": "في رمضان", "en": "In Ramadan"}]},
        "xp": 25
    },
    {
        "id": 21, "level": 2, "lesson": 11, "emoji": "✈️",
        "title": {"ar": "صلاة المسافر والمريض", "en": "Prayer of the Traveler and the Sick", "de": "Gebet des Reisenden und Kranken", "fr": "Prière du voyageur et du malade", "tr": "Yolcu ve Hasta Namazı", "ru": "Молитва путника и больного", "sv": "Resandes och sjukas bön", "nl": "Gebed van reiziger en zieke", "el": "Προσευχή ταξιδιώτη και ασθενούς"},
        "method": "conceptual",
        "content": {
            "traveler": {"ar": "يجوز للمسافر قصر الصلاة الرباعية إلى ركعتين، والجمع بين الظهر والعصر أو المغرب والعشاء", "en": "The traveler may shorten 4-rak'ah prayers to 2, and combine Dhuhr with Asr or Maghrib with Isha"},
            "sick": {"ar": "يصلي المريض على حسب حاله: قائماً فإن لم يستطع فجالساً فإن لم يستطع فعلى جنبه", "en": "The sick person prays according to their ability: standing, if not then sitting, if not then on their side"}
        },
        "quiz": {"type": "select", "question": {"ar": "كم ركعة يصلي المسافر الظهر؟", "en": "How many rak'ahs does a traveler pray for Dhuhr?"}, "correct": "2", "options": ["2", "3", "4"]},
        "xp": 25
    },
    {
        "id": 22, "level": 2, "lesson": 12, "emoji": "🏆",
        "title": {"ar": "اختبار الصلاة — المستوى الثاني", "en": "Prayer Assessment — Level 2", "de": "Gebet Bewertung — Stufe 2", "fr": "Évaluation Prière — Niveau 2", "tr": "Namaz Değerlendirmesi — Seviye 2", "ru": "Тест по Молитве — Уровень 2", "sv": "Bön bedömning — Nivå 2", "nl": "Gebed toets — Niveau 2", "el": "Αξιολόγηση Προσευχής — Επίπεδο 2"},
        "method": "assessment",
        "content": {"sections": ["conditions", "pillars", "description", "congregational", "special_prayers"], "pass_score": 75},
        "quiz": {"type": "comprehensive", "total_questions": 25},
        "xp": 60
    },
]

# ═══════════════════════════════════════════════════════════════
# FIQH LEVEL 3: FASTING (SIYAM) — 8 lessons
# ═══════════════════════════════════════════════════════════════

FIQH_L3_LESSONS = [
    {"id": 23, "level": 3, "lesson": 1, "emoji": "🌙", "title": {"ar": "الصيام — فرضيته وفضله", "en": "Fasting — Obligation and Virtue", "de": "Fasten — Pflicht und Tugend", "fr": "Jeûne — Obligation et vertu", "tr": "Oruç — Farz Oluşu ve Fazileti", "ru": "Пост — Обязанность и добродетель", "sv": "Fasta — Plikt och dygd", "nl": "Vasten — Verplichting en deugd", "el": "Νηστεία — Υποχρέωση και αρετή"}, "method": "conceptual", "content": {"verse": {"ar": "﴿يَا أَيُّهَا الَّذِينَ آمَنُوا كُتِبَ عَلَيْكُمُ الصِّيَامُ كَمَا كُتِبَ عَلَى الَّذِينَ مِن قَبْلِكُمْ لَعَلَّكُمْ تَتَّقُونَ﴾", "en": "O you who believe, fasting is prescribed for you as it was for those before you, that you may become righteous (2:183)"}, "virtues": [{"ar": "الصيام جُنّة — وقاية من النار", "en": "Fasting is a shield — protection from Hellfire"}, {"ar": "للصائم فرحتان: فرحة عند فطره وفرحة عند لقاء ربه", "en": "The fasting person has two joys: at iftar and when meeting their Lord"}, {"ar": "باب الريان يدخل منه الصائمون فقط", "en": "The Rayyan gate — only fasting people enter through it"}]}, "quiz": {"type": "select", "question": {"ar": "ما اسم الباب الذي يدخل منه الصائمون الجنة؟", "en": "What is the name of the gate fasting people enter Paradise through?"}, "correct": {"ar": "الريان", "en": "Ar-Rayyan"}, "options": [{"ar": "الريان", "en": "Ar-Rayyan"}, {"ar": "السلام", "en": "As-Salam"}, {"ar": "الفردوس", "en": "Al-Firdaws"}]}, "xp": 25},
    {"id": 24, "level": 3, "lesson": 2, "emoji": "⏰", "title": {"ar": "أركان الصيام وشروطه", "en": "Pillars and Conditions of Fasting", "de": "Säulen und Bedingungen des Fastens", "fr": "Piliers et conditions du jeûne", "tr": "Orucun Rükünleri ve Şartları", "ru": "Столпы и условия поста", "sv": "Fastans pelare och villkor", "nl": "Pilaren en voorwaarden van vasten", "el": "Πυλώνες και συνθήκες νηστείας"}, "method": "conceptual", "content": {"pillars": [{"ar": "النية قبل الفجر", "en": "Intention before Fajr"}, {"ar": "الإمساك عن المفطرات من الفجر إلى المغرب", "en": "Abstaining from nullifiers from Fajr to Maghrib"}], "conditions": [{"ar": "الإسلام", "en": "Being Muslim"}, {"ar": "البلوغ", "en": "Maturity"}, {"ar": "العقل", "en": "Sanity"}, {"ar": "القدرة على الصيام", "en": "Ability to fast"}, {"ar": "الإقامة (ليس مسافراً)", "en": "Being resident (not traveling)"}]}, "quiz": {"type": "select", "question": {"ar": "متى تكون نية صيام رمضان؟", "en": "When is the intention for Ramadan fasting?"}, "correct": {"ar": "قبل الفجر", "en": "Before Fajr"}, "options": [{"ar": "قبل الفجر", "en": "Before Fajr"}, {"ar": "بعد الشروق", "en": "After sunrise"}, {"ar": "عند المغرب", "en": "At Maghrib"}]}, "xp": 25},
    {"id": 25, "level": 3, "lesson": 3, "emoji": "❌", "title": {"ar": "مفسدات الصيام", "en": "What Breaks the Fast", "de": "Was das Fasten bricht", "fr": "Ce qui rompt le jeûne", "tr": "Orucu Bozan Şeyler", "ru": "Что нарушает пост", "sv": "Vad som bryter fastan", "nl": "Wat het vasten verbreekt", "el": "Τι σπάει τη νηστεία"}, "method": "conceptual", "content": {"nullifiers": [{"ar": "الأكل أو الشرب عمداً", "en": "Eating or drinking intentionally"}, {"ar": "القيء عمداً", "en": "Intentional vomiting"}, {"ar": "الحيض والنفاس", "en": "Menstruation and postpartum bleeding"}], "allowed": [{"ar": "الأكل أو الشرب ناسياً", "en": "Eating/drinking forgetfully"}, {"ar": "القيء غير المتعمد", "en": "Unintentional vomiting"}, {"ar": "السواك", "en": "Using Siwak"}]}, "quiz": {"type": "true_false", "question": {"ar": "إذا أكل الصائم ناسياً فصيامه صحيح", "en": "If a fasting person eats forgetfully, their fast is still valid"}, "correct": True}, "xp": 20},
    {"id": 26, "level": 3, "lesson": 4, "emoji": "🍽️", "title": {"ar": "سنن الصيام وآدابه", "en": "Sunnah Acts and Etiquettes of Fasting", "de": "Sunnah und Etikette des Fastens", "fr": "Sunna et étiquettes du jeûne", "tr": "Oruç Sünnet ve Adabı", "ru": "Сунна и этикет поста", "sv": "Fastans Sunnah och etikett", "nl": "Soennah en etiquette van vasten", "el": "Σούνα και εθιμοτυπία νηστείας"}, "method": "practice-based", "content": {"sunnahs": [{"ar": "تعجيل الفطر", "en": "Hastening to break the fast"}, {"ar": "تأخير السحور", "en": "Delaying Suhoor"}, {"ar": "الإفطار على تمر أو ماء", "en": "Breaking fast with dates or water"}, {"ar": "الدعاء عند الإفطار", "en": "Supplication when breaking fast"}, {"ar": "الجود والكرم", "en": "Generosity"}], "dua": {"ar": "ذهب الظمأ وابتلّت العروق وثبت الأجر إن شاء الله", "en": "The thirst has gone, the veins are moistened, and the reward is certain if Allah wills"}}, "quiz": {"type": "select", "question": {"ar": "على ماذا نفطر؟", "en": "What do we break fast with?"}, "correct": {"ar": "تمر أو ماء", "en": "Dates or water"}, "options": [{"ar": "تمر أو ماء", "en": "Dates or water"}, {"ar": "عصير", "en": "Juice"}, {"ar": "أي طعام", "en": "Any food"}]}, "xp": 20},
    {"id": 27, "level": 3, "lesson": 5, "emoji": "🎁", "title": {"ar": "ليلة القدر", "en": "Laylat al-Qadr", "de": "Laylat al-Qadr", "fr": "Nuit du Destin", "tr": "Kadir Gecesi", "ru": "Ночь Предопределения", "sv": "Laylat al-Qadr", "nl": "Laylat al-Qadr", "el": "Λάιλατ αλ-Κάντρ"}, "method": "story_based", "content": {"verse": {"ar": "﴿لَيْلَةُ الْقَدْرِ خَيْرٌ مِّنْ أَلْفِ شَهْرٍ﴾", "en": "The Night of Decree is better than a thousand months (97:3)"}, "info": {"ar": "ليلة القدر في العشر الأواخر من رمضان، وأرجاها ليالي الأوتار", "en": "Laylat al-Qadr is in the last 10 nights of Ramadan, most likely the odd nights"}, "dua": {"ar": "اللهم إنك عفو تحب العفو فاعفُ عني", "en": "O Allah, You are forgiving and love forgiveness, so forgive me"}}, "quiz": {"type": "select", "question": {"ar": "ليلة القدر خير من كم شهر؟", "en": "Laylat al-Qadr is better than how many months?"}, "correct": "1000", "options": ["100", "500", "1000", "10000"]}, "xp": 25},
    {"id": 28, "level": 3, "lesson": 6, "emoji": "💰", "title": {"ar": "زكاة الفطر", "en": "Zakat al-Fitr", "de": "Zakat al-Fitr", "fr": "Zakat al-Fitr", "tr": "Fıtır Sadakası", "ru": "Закят аль-Фитр", "sv": "Zakat al-Fitr", "nl": "Zakat al-Fitr", "el": "Ζακάτ αλ-Φιτρ"}, "method": "conceptual", "content": {"ruling": {"ar": "زكاة الفطر واجبة على كل مسلم يملك قوت يومه وليلته", "en": "Zakat al-Fitr is obligatory on every Muslim who has food for the day and night"}, "amount": {"ar": "صاع من غالب قوت أهل البلد (حوالي 3 كيلو من الأرز أو التمر)", "en": "A Sa' of the staple food of the land (about 3kg of rice or dates)"}, "time": {"ar": "تُخرج قبل صلاة العيد", "en": "Paid before Eid prayer"}}, "quiz": {"type": "select", "question": {"ar": "متى تُخرج زكاة الفطر؟", "en": "When is Zakat al-Fitr paid?"}, "correct": {"ar": "قبل صلاة العيد", "en": "Before Eid prayer"}, "options": [{"ar": "قبل صلاة العيد", "en": "Before Eid"}, {"ar": "بعد رمضان بشهر", "en": "A month after Ramadan"}, {"ar": "في أي وقت", "en": "Anytime"}]}, "xp": 25},
    {"id": 29, "level": 3, "lesson": 7, "emoji": "📅", "title": {"ar": "صيام التطوع", "en": "Voluntary Fasting", "de": "Freiwilliges Fasten", "fr": "Jeûne volontaire", "tr": "Nafile Oruç", "ru": "Добровольный пост", "sv": "Frivillig fasta", "nl": "Vrijwillig vasten", "el": "Εθελοντική νηστεία"}, "method": "conceptual", "content": {"types": [{"name": {"ar": "صيام يوم عرفة", "en": "Fasting day of Arafah"}, "virtue": {"ar": "يكفّر ذنوب سنتين", "en": "Expiates sins of two years"}}, {"name": {"ar": "صيام عاشوراء", "en": "Fasting Ashura"}, "virtue": {"ar": "يكفّر ذنوب سنة", "en": "Expiates sins of one year"}}, {"name": {"ar": "صيام الإثنين والخميس", "en": "Monday and Thursday fasting"}, "virtue": {"ar": "تُعرض الأعمال فيهما على الله", "en": "Deeds are presented to Allah on these days"}}, {"name": {"ar": "صيام ثلاثة أيام من كل شهر", "en": "3 days each month"}, "virtue": {"ar": "كصيام الدهر", "en": "Like fasting forever"}}]}, "quiz": {"type": "select", "question": {"ar": "صيام يوم عرفة يكفّر ذنوب كم سنة؟", "en": "Day of Arafah fasting expiates how many years?"}, "correct": "2", "options": ["1", "2", "3", "5"]}, "xp": 20},
    {"id": 30, "level": 3, "lesson": 8, "emoji": "🏆", "title": {"ar": "اختبار الصيام — المستوى الثالث", "en": "Fasting Assessment — Level 3", "de": "Fasten Bewertung — Stufe 3", "fr": "Évaluation Jeûne — Niveau 3", "tr": "Oruç Değerlendirmesi — Seviye 3", "ru": "Тест по Посту — Уровень 3", "sv": "Fasta bedömning — Nivå 3", "nl": "Vasten toets — Niveau 3", "el": "Αξιολόγηση Νηστείας — Επίπεδο 3"}, "method": "assessment", "content": {"sections": ["obligation", "pillars", "nullifiers", "sunnah", "laylat_qadr", "zakat_fitr"], "pass_score": 75}, "quiz": {"type": "comprehensive", "total_questions": 20}, "xp": 50},
]

# ═══════════════════════════════════════════════════════════════
# FIQH LEVEL 4: ZAKAT & HAJJ — 10 lessons
# ═══════════════════════════════════════════════════════════════

FIQH_L4_LESSONS = [
    {"id": 31, "level": 4, "lesson": 1, "emoji": "💰", "title": {"ar": "الزكاة — الركن الثالث", "en": "Zakat — The Third Pillar", "de": "Zakat — Die dritte Säule", "fr": "Zakat — Le troisième pilier", "tr": "Zekât — Üçüncü Şart", "ru": "Закят — Третий Столп", "sv": "Zakat — Tredje pelaren", "nl": "Zakat — Derde pilaar", "el": "Ζακάτ — Τρίτος πυλώνας"}, "method": "conceptual", "content": {"definition": {"ar": "الزكاة هي إخراج قدر معلوم من المال لمستحقيه إذا بلغ النصاب وحال عليه الحول", "en": "Zakat is giving a specific amount of wealth to those entitled when it reaches the Nisab and a year passes"}, "categories": [{"ar": "الفقراء والمساكين", "en": "The poor and needy"}, {"ar": "العاملون عليها", "en": "Zakat collectors"}, {"ar": "المؤلفة قلوبهم", "en": "Those whose hearts are to be reconciled"}, {"ar": "في الرقاب", "en": "Freeing slaves"}, {"ar": "الغارمون", "en": "Those in debt"}, {"ar": "في سبيل الله", "en": "In the cause of Allah"}, {"ar": "ابن السبيل", "en": "The traveler"}], "rate": {"ar": "2.5% من الأموال إذا بلغت النصاب", "en": "2.5% of wealth when it reaches Nisab"}}, "quiz": {"type": "select", "question": {"ar": "ما نسبة الزكاة من المال؟", "en": "What is the Zakat rate on money?"}, "correct": "2.5%", "options": ["1%", "2.5%", "5%", "10%"]}, "xp": 25},
    {"id": 32, "level": 4, "lesson": 2, "emoji": "📊", "title": {"ar": "أنواع الأموال التي تجب فيها الزكاة", "en": "Types of Wealth Subject to Zakat", "de": "Arten von Vermögen für Zakat", "fr": "Types de richesse soumis à la Zakat", "tr": "Zekât Gereken Mal Çeşitleri", "ru": "Виды имущества для Закята", "sv": "Typer av tillgångar för Zakat", "nl": "Soorten vermogen voor Zakat", "el": "Τύποι περιουσίας για Ζακάτ"}, "method": "conceptual", "content": {"types": [{"name": {"ar": "النقود (الذهب والفضة والعملات)", "en": "Money (gold, silver, currency)"}, "nisab": {"ar": "85 غرام ذهب", "en": "85 grams of gold"}}, {"name": {"ar": "عروض التجارة", "en": "Trade goods"}, "nisab": {"ar": "قيمة 85 غرام ذهب", "en": "Value of 85 grams gold"}}, {"name": {"ar": "الزروع والثمار", "en": "Crops and fruits"}, "rate": {"ar": "5% أو 10% حسب طريقة الري", "en": "5% or 10% depending on irrigation"}}, {"name": {"ar": "الأنعام (الإبل والبقر والغنم)", "en": "Livestock (camels, cattle, sheep)"}}]}, "quiz": {"type": "select", "question": {"ar": "ما نصاب الذهب للزكاة؟", "en": "What is gold Nisab for Zakat?"}, "correct": {"ar": "85 غرام", "en": "85 grams"}, "options": [{"ar": "85 غرام", "en": "85 grams"}, {"ar": "50 غرام", "en": "50 grams"}, {"ar": "100 غرام", "en": "100 grams"}]}, "xp": 25},
    {"id": 33, "level": 4, "lesson": 3, "emoji": "🕋", "title": {"ar": "الحج — الركن الخامس", "en": "Hajj — The Fifth Pillar", "de": "Hajj — Die fünfte Säule", "fr": "Hajj — Le cinquième pilier", "tr": "Hac — Beşinci Şart", "ru": "Хадж — Пятый Столп", "sv": "Hajj — Femte pelaren", "nl": "Hadj — Vijfde pilaar", "el": "Χατζ — Πέμπτος πυλώνας"}, "method": "story_based", "content": {"definition": {"ar": "الحج هو قصد بيت الله الحرام لأداء مناسك مخصوصة في وقت مخصوص", "en": "Hajj is traveling to the Sacred House of Allah to perform specific rites at a specific time"}, "condition": {"ar": "واجب مرة في العمر على المسلم البالغ العاقل المستطيع", "en": "Obligatory once in a lifetime for every sane, adult Muslim who is able"}, "hadith": {"ar": "قال النبي ﷺ: «الحج المبرور ليس له جزاء إلا الجنة»", "en": "The Prophet ﷺ said: 'An accepted Hajj has no reward except Paradise'"}}, "quiz": {"type": "select", "question": {"ar": "كم مرة يجب الحج في العمر؟", "en": "How many times is Hajj obligatory?"}, "correct": {"ar": "مرة واحدة", "en": "Once"}, "options": [{"ar": "مرة واحدة", "en": "Once"}, {"ar": "كل سنة", "en": "Every year"}, {"ar": "خمس مرات", "en": "Five times"}]}, "xp": 25},
    {"id": 34, "level": 4, "lesson": 4, "emoji": "📋", "title": {"ar": "أركان الحج ومناسكه", "en": "Pillars and Rites of Hajj", "de": "Säulen und Riten der Hadsch", "fr": "Piliers et rites du Hajj", "tr": "Haccın Rükünleri", "ru": "Столпы и обряды Хаджа", "sv": "Hajj pelare och riter", "nl": "Pilaren en rituelen van Hadj", "el": "Πυλώνες και τελετουργίες Χατζ"}, "method": "practice-based", "content": {"pillars": [{"ar": "الإحرام", "en": "Ihram (entering state of pilgrimage)"}, {"ar": "الوقوف بعرفة", "en": "Standing at Arafah"}, {"ar": "طواف الإفاضة", "en": "Tawaf al-Ifadah"}, {"ar": "السعي بين الصفا والمروة", "en": "Sa'i between Safa and Marwah"}], "sequence": [{"ar": "يوم 8: التوجه لمنى", "en": "Day 8: Go to Mina"}, {"ar": "يوم 9: الوقوف بعرفة", "en": "Day 9: Stand at Arafah"}, {"ar": "ليلة 10: المبيت بمزدلفة", "en": "Night 10: Stay at Muzdalifah"}, {"ar": "يوم 10: رمي جمرة العقبة والنحر والحلق والطواف", "en": "Day 10: Stone, sacrifice, shave, Tawaf"}, {"ar": "أيام 11-13: رمي الجمرات", "en": "Days 11-13: Stone the Jamarat"}]}, "quiz": {"type": "select", "question": {"ar": "ما أهم ركن في الحج؟", "en": "What is the most important pillar of Hajj?"}, "correct": {"ar": "الوقوف بعرفة", "en": "Standing at Arafah"}, "options": [{"ar": "الوقوف بعرفة", "en": "Arafah"}, {"ar": "الطواف", "en": "Tawaf"}, {"ar": "رمي الجمرات", "en": "Stoning"}]}, "xp": 30},
    {"id": 35, "level": 4, "lesson": 5, "emoji": "🧕", "title": {"ar": "العمرة", "en": "Umrah", "de": "Umrah", "fr": "Oumra", "tr": "Umre", "ru": "Умра", "sv": "Umrah", "nl": "Umrah", "el": "Ούμρα"}, "method": "practice-based", "content": {"definition": {"ar": "العمرة هي الحج الأصغر — تُسن في أي وقت من السنة", "en": "Umrah is the minor pilgrimage — recommended at any time of year"}, "steps": [{"ar": "الإحرام من الميقات", "en": "Ihram from Miqat"}, {"ar": "الطواف بالبيت 7 أشواط", "en": "Tawaf 7 times around Ka'bah"}, {"ar": "السعي بين الصفا والمروة 7 أشواط", "en": "Sa'i 7 times between Safa and Marwah"}, {"ar": "الحلق أو التقصير", "en": "Shaving or trimming hair"}]}, "quiz": {"type": "select", "question": {"ar": "كم شوطاً نطوف حول الكعبة؟", "en": "How many rounds do we make around Ka'bah?"}, "correct": "7", "options": ["3", "5", "7", "10"]}, "xp": 25},
    {"id": 36, "level": 4, "lesson": 6, "emoji": "⛔", "title": {"ar": "محظورات الإحرام", "en": "Prohibitions During Ihram", "de": "Verbote während Ihram", "fr": "Interdits pendant l'Ihram", "tr": "İhram Yasakları", "ru": "Запреты во время Ихрама", "sv": "Förbud under Ihram", "nl": "Verboden tijdens Ihram", "el": "Απαγορεύσεις κατά τη διάρκεια Ιχράμ"}, "method": "conceptual", "content": {"prohibitions": [{"ar": "حلق الشعر", "en": "Shaving hair"}, {"ar": "قص الأظافر", "en": "Trimming nails"}, {"ar": "الطيب (العطر)", "en": "Perfume"}, {"ar": "لبس المخيط للرجال", "en": "Sewn clothes for men"}, {"ar": "تغطية الرأس للرجال", "en": "Covering head for men"}, {"ar": "صيد البر", "en": "Hunting land animals"}]}, "quiz": {"type": "true_false", "question": {"ar": "يجوز للمُحرم استعمال العطر", "en": "A person in Ihram may use perfume"}, "correct": False}, "xp": 20},
    {"id": 37, "level": 4, "lesson": 7, "emoji": "🎮", "title": {"ar": "لعبة: ترتيب مناسك الحج", "en": "Game: Arrange Hajj Rites", "de": "Spiel: Hajj-Riten ordnen", "fr": "Jeu: Ordonner les rites du Hajj", "tr": "Oyun: Hac Menâsikini Sırala", "ru": "Игра: Расположи обряды Хаджа", "sv": "Spel: Ordna Hajj-riter", "nl": "Spel: Rangschik Hadj-rituelen", "el": "Παιχνίδι: Ταξινόμηση τελετών Χατζ"}, "method": "game", "content": {"game_type": "sequence", "correct_order": [{"ar": "الإحرام", "en": "Ihram"}, {"ar": "منى يوم 8", "en": "Mina Day 8"}, {"ar": "عرفة يوم 9", "en": "Arafah Day 9"}, {"ar": "مزدلفة", "en": "Muzdalifah"}, {"ar": "رمي جمرة العقبة", "en": "Stone Jamrah"}, {"ar": "الذبح", "en": "Sacrifice"}, {"ar": "الحلق", "en": "Shave"}, {"ar": "طواف الإفاضة", "en": "Tawaf al-Ifadah"}]}, "quiz": {"type": "sequence", "total_items": 8}, "xp": 30},
    {"id": 38, "level": 4, "lesson": 8, "emoji": "🐑", "title": {"ar": "الأضحية", "en": "Udhiyah (Sacrifice)", "de": "Opfertier", "fr": "Sacrifice", "tr": "Kurban", "ru": "Жертвоприношение", "sv": "Offertjur", "nl": "Offerdier", "el": "Θυσία"}, "method": "conceptual", "content": {"ruling": {"ar": "الأضحية سنة مؤكدة عن القادر في عيد الأضحى", "en": "Udhiyah is a confirmed Sunnah for those who can afford it on Eid al-Adha"}, "conditions": {"ar": "أن تكون بهيمة الأنعام (إبل أو بقر أو غنم) سليمة من العيوب", "en": "Must be livestock (camel, cattle, sheep) free from defects"}, "distribution": {"ar": "يُستحب تقسيمها أثلاثاً: ثلث للأهل وثلث للهدية وثلث للفقراء", "en": "Recommended to divide into thirds: family, gifts, and the poor"}}, "quiz": {"type": "select", "question": {"ar": "متى تُذبح الأضحية؟", "en": "When is the sacrifice made?"}, "correct": {"ar": "عيد الأضحى", "en": "Eid al-Adha"}, "options": [{"ar": "عيد الأضحى", "en": "Eid al-Adha"}, {"ar": "عيد الفطر", "en": "Eid al-Fitr"}, {"ar": "رمضان", "en": "Ramadan"}]}, "xp": 25},
    {"id": 39, "level": 4, "lesson": 9, "emoji": "📖", "title": {"ar": "أحكام متفرقة — الأيمان والنذور", "en": "Miscellaneous Rulings — Oaths and Vows", "de": "Verschiedene Urteile — Eide", "fr": "Règles diverses — Serments", "tr": "Çeşitli Hükümler — Yeminler", "ru": "Различные решения — Клятвы", "sv": "Diverse regler — Eder", "nl": "Diverse regels — Eden", "el": "Διάφοροι κανόνες — Όρκοι"}, "method": "conceptual", "content": {"oath": {"ar": "اليمين هو الحلف بالله — لا يجوز الحلف بغير الله", "en": "An oath is swearing by Allah — it's not permissible to swear by other than Allah"}, "expiation": {"ar": "كفارة اليمين: إطعام عشرة مساكين أو كسوتهم أو تحرير رقبة، فإن لم يجد فصيام ثلاثة أيام", "en": "Expiation for oath: feed 10 poor, clothe them, or free a slave; if unable, fast 3 days"}}, "quiz": {"type": "true_false", "question": {"ar": "يجوز الحلف بغير الله", "en": "It's permissible to swear by other than Allah"}, "correct": False}, "xp": 20},
    {"id": 40, "level": 4, "lesson": 10, "emoji": "🏆", "title": {"ar": "اختبار شامل — المستوى الرابع", "en": "Comprehensive Assessment — Level 4", "de": "Gesamtbewertung — Stufe 4", "fr": "Évaluation complète — Niveau 4", "tr": "Kapsamlı Değerlendirme — Seviye 4", "ru": "Полный Тест — Уровень 4", "sv": "Omfattande bedömning — Nivå 4", "nl": "Uitgebreide toets — Niveau 4", "el": "Περιεκτική Αξιολόγηση — Επίπεδο 4"}, "method": "assessment", "content": {"sections": ["zakat", "hajj", "umrah", "udhiyah", "oaths"], "pass_score": 75}, "quiz": {"type": "comprehensive", "total_questions": 25}, "xp": 60},
]

# Combined
FIQH_COMPLETE_LESSONS = FIQH_L1_LESSONS + FIQH_L2_LESSONS + FIQH_L3_LESSONS + FIQH_L4_LESSONS

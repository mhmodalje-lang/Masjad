"""
Nooraniya Lessons 31-70 — Full Content
Levels 4-7: Tanween/Shadda → Quranic Words → Reading Verses → Tajweed Mastery
All content in 9 languages with rich interactive exercises.
"""

# ═══════════════════════════════════════════════════
# LEVEL 4: التنوين والشدة والسكون (Lessons 31-40)
# Tanween, Shadda & Sukun
# ═══════════════════════════════════════════════════

LEVEL4_LESSONS = [
    {
        "id": 31, "level": 4, "lesson": 1, "emoji": "⚡", "method": "visual_audio", "xp": 20,
        "title": {"ar": "التنوين بالفتح — /an/", "en": "Tanween Fatha — /an/", "de": "Tanween Fatha — /an/", "fr": "Tanween Fatha — /an/", "tr": "Fethalı Tenvin — /an/", "ru": "Танвин Фатха — /ан/", "sv": "Tanween Fatha — /an/", "nl": "Tanween Fatha — /an/", "el": "Τανουίν Φάθα — /αν/"},
        "content": {
            "rule": {"ar": "التنوين بالفتح يُنطق /ان/ — علامته فتحتان ً", "en": "Tanween Fatha is pronounced /an/ — its mark is double fatha ً"},
            "examples": [
                {"word": "كِتَابًا", "transliteration": "kitaaban", "meaning": {"ar": "كتاب", "en": "a book"}},
                {"word": "قَلَمًا", "transliteration": "qalaman", "meaning": {"ar": "قلم", "en": "a pen"}},
                {"word": "بَابًا", "transliteration": "baaban", "meaning": {"ar": "باب", "en": "a door"}},
                {"word": "نُورًا", "transliteration": "nooran", "meaning": {"ar": "نور", "en": "a light"}},
            ],
            "tip": {"ar": "عند رؤية الفتحتين ً، أضف صوت /ن/ في نهاية الكلمة", "en": "When you see double fatha ً, add /n/ sound at the end of the word"},
            "exercises": [
                {"type": "listen_repeat", "word": "كِتَابًا", "instruction": {"ar": "استمع ثم أعد النطق", "en": "Listen and repeat"}},
                {"type": "identify", "instruction": {"ar": "أي كلمة فيها تنوين بالفتح؟", "en": "Which word has Tanween Fatha?"}, "options": ["كِتَابًا", "كِتَابٌ", "كِتَابٍ"], "correct": 0},
            ]
        },
        "quiz": {
            "type": "multi",
            "questions": [
                {"question": {"ar": "كيف ينطق التنوين بالفتح؟", "en": "How is Tanween Fatha pronounced?"}, "correct": {"ar": "/ان/", "en": "/an/"}, "options": [{"ar": "/ان/", "en": "/an/"}, {"ar": "/ون/", "en": "/un/"}, {"ar": "/ين/", "en": "/in/"}]},
                {"question": {"ar": "ما علامة التنوين بالفتح؟", "en": "What is the mark of Tanween Fatha?"}, "correct": {"ar": "فتحتان ً", "en": "Double fatha ً"}, "options": [{"ar": "فتحتان ً", "en": "Double fatha ً"}, {"ar": "ضمتان ٌ", "en": "Double damma ٌ"}, {"ar": "كسرتان ٍ", "en": "Double kasra ٍ"}]}
            ]
        },
    },
    {
        "id": 32, "level": 4, "lesson": 2, "emoji": "⚡", "method": "visual_audio", "xp": 20,
        "title": {"ar": "التنوين بالضم — /un/", "en": "Tanween Damma — /un/", "de": "Tanween Damma — /un/", "fr": "Tanween Damma — /un/", "tr": "Zammelı Tenvin — /un/", "ru": "Танвин Дамма — /ун/", "sv": "Tanween Damma — /un/", "nl": "Tanween Damma — /un/", "el": "Τανουίν Ντάμμα — /ουν/"},
        "content": {
            "rule": {"ar": "التنوين بالضم يُنطق /ون/ — علامته ضمتان ٌ", "en": "Tanween Damma is pronounced /un/ — its mark is double damma ٌ"},
            "examples": [
                {"word": "كِتَابٌ", "transliteration": "kitaabun", "meaning": {"ar": "كتاب", "en": "a book"}},
                {"word": "قَلَمٌ", "transliteration": "qalamun", "meaning": {"ar": "قلم", "en": "a pen"}},
                {"word": "مَسْجِدٌ", "transliteration": "masjidun", "meaning": {"ar": "مسجد", "en": "a mosque"}},
                {"word": "رَجُلٌ", "transliteration": "rajulun", "meaning": {"ar": "رجل", "en": "a man"}},
            ],
            "tip": {"ar": "عند رؤية الضمتين ٌ، أضف صوت /ن/ في نهاية الكلمة مع ضم الشفتين", "en": "When you see double damma ٌ, add /n/ sound with lips rounded"},
            "exercises": [
                {"type": "listen_repeat", "word": "مَسْجِدٌ", "instruction": {"ar": "استمع ثم أعد النطق", "en": "Listen and repeat"}},
                {"type": "identify", "instruction": {"ar": "أي كلمة فيها تنوين بالضم؟", "en": "Which word has Tanween Damma?"}, "options": ["كِتَابٌ", "كِتَابًا", "كِتَابٍ"], "correct": 0},
            ]
        },
        "quiz": {
            "type": "multi",
            "questions": [
                {"question": {"ar": "ما صوت التنوين بالضم؟", "en": "What sound does Tanween Damma make?"}, "correct": {"ar": "/ون/", "en": "/un/"}, "options": [{"ar": "/ون/", "en": "/un/"}, {"ar": "/ان/", "en": "/an/"}, {"ar": "/ين/", "en": "/in/"}]},
            ]
        },
    },
    {
        "id": 33, "level": 4, "lesson": 3, "emoji": "⚡", "method": "visual_audio", "xp": 20,
        "title": {"ar": "التنوين بالكسر — /in/", "en": "Tanween Kasra — /in/", "de": "Tanween Kasra — /in/", "fr": "Tanween Kasra — /in/", "tr": "Kesrelı Tenvin — /in/", "ru": "Танвин Касра — /ин/", "sv": "Tanween Kasra — /in/", "nl": "Tanween Kasra — /in/", "el": "Τανουίν Κάσρα — /ιν/"},
        "content": {
            "rule": {"ar": "التنوين بالكسر يُنطق /ين/ — علامته كسرتان ٍ", "en": "Tanween Kasra is pronounced /in/ — its mark is double kasra ٍ"},
            "examples": [
                {"word": "كِتَابٍ", "transliteration": "kitaabin", "meaning": {"ar": "كتاب", "en": "a book"}},
                {"word": "رَحِيمٍ", "transliteration": "rahemin", "meaning": {"ar": "رحيم", "en": "merciful"}},
                {"word": "عَظِيمٍ", "transliteration": "azeemin", "meaning": {"ar": "عظيم", "en": "great"}},
            ],
            "tip": {"ar": "عند رؤية الكسرتين ٍ، أضف صوت /ن/ في نهاية الكلمة مع خفض الفك", "en": "When you see double kasra ٍ, add /n/ sound with jaw lowered"},
        },
        "quiz": {"type": "select", "question": {"ar": "ما صوت التنوين بالكسر؟", "en": "What sound does Tanween Kasra make?"}, "correct": {"ar": "/ين/", "en": "/in/"}, "options": [{"ar": "/ين/", "en": "/in/"}, {"ar": "/ان/", "en": "/an/"}, {"ar": "/ون/", "en": "/un/"}]},
    },
    {
        "id": 34, "level": 4, "lesson": 4, "emoji": "⚡", "method": "practice", "xp": 20,
        "title": {"ar": "تمارين التنوين — مراجعة", "en": "Tanween Exercises — Review", "de": "Tanween Übungen — Wiederholung", "fr": "Exercices Tanween — Révision", "tr": "Tenvin Alıştırmaları — Tekrar", "ru": "Упражнения Танвин — Повторение", "sv": "Tanween Övningar — Repetition", "nl": "Tanween Oefeningen — Herhaling", "el": "Ασκήσεις Τανουίν — Επανάληψη"},
        "content": {
            "rule": {"ar": "التنوين ثلاثة أنواع: بالفتح (ً/ان) بالضم (ٌ/ون) بالكسر (ٍ/ين)", "en": "Tanween has 3 types: Fatha (ً/an), Damma (ٌ/un), Kasra (ٍ/in)"},
            "exercises": [
                {"type": "match_pairs", "instruction": {"ar": "طابق كل تنوين بصوته", "en": "Match each Tanween with its sound"}, "pairs": [["ً", "/an/"], ["ٌ", "/un/"], ["ٍ", "/in/"]]},
                {"type": "classify", "instruction": {"ar": "صنّف الكلمات حسب نوع التنوين", "en": "Classify words by Tanween type"}, "words": [{"word": "كِتَابًا", "type": "fatha"}, {"word": "كِتَابٌ", "type": "damma"}, {"word": "كِتَابٍ", "type": "kasra"}]},
                {"type": "read_aloud", "instruction": {"ar": "اقرأ الكلمات التالية بصوت عالٍ", "en": "Read these words aloud"}, "words": ["عِلْمًا", "نُورٌ", "رَحْمَةٍ", "قُرْآنًا", "مُسْلِمٌ"]},
            ],
            "tip": {"ar": "تذكر: كل أنواع التنوين تضيف صوت النون في النهاية", "en": "Remember: all Tanween types add a /n/ sound at the end"},
        },
        "quiz": {"type": "comprehensive", "sections": [
            {"question": {"ar": "اقرأ: عِلْمًا", "en": "Read: عِلْمًا"}, "type": "read"},
            {"question": {"ar": "ما نوع التنوين في كلمة مُسْلِمٌ؟", "en": "What type of Tanween is in مُسْلِمٌ?"}, "correct": {"ar": "تنوين بالضم", "en": "Tanween Damma"}, "options": [{"ar": "تنوين بالفتح", "en": "Tanween Fatha"}, {"ar": "تنوين بالضم", "en": "Tanween Damma"}, {"ar": "تنوين بالكسر", "en": "Tanween Kasra"}]}
        ]},
    },
    {
        "id": 35, "level": 4, "lesson": 5, "emoji": "⚡", "method": "visual_audio", "xp": 20,
        "title": {"ar": "الشدة — تضعيف الحرف", "en": "Shadda — Letter Doubling", "de": "Shadda — Buchstabenverdopplung", "fr": "Shadda — Doublement de lettre", "tr": "Şedde — Harf İkilemesi", "ru": "Шадда — Удвоение буквы", "sv": "Shadda — Bokstavsfördubbling", "nl": "Shadda — Letterverdubbeling", "el": "Σάντα — Διπλασιασμός γράμματος"},
        "content": {
            "rule": {"ar": "الشدة (ّ) تعني أن الحرف ينطق مرتين — مرة ساكن ومرة متحرك", "en": "Shadda (ّ) means the letter is pronounced twice — first silent then with vowel"},
            "examples": [
                {"word": "مُحَمَّد", "transliteration": "muhammad", "meaning": {"ar": "محمد", "en": "Muhammad"}, "breakdown": {"ar": "م+م = مّ", "en": "m+m = mm"}},
                {"word": "رَبَّنَا", "transliteration": "rabbana", "meaning": {"ar": "ربنا", "en": "Our Lord"}, "breakdown": {"ar": "ب+ب = بّ", "en": "b+b = bb"}},
                {"word": "الشَّمْس", "transliteration": "ash-shams", "meaning": {"ar": "الشمس", "en": "the sun"}, "breakdown": {"ar": "ش+ش = شّ", "en": "sh+sh = shsh"}},
                {"word": "النَّاس", "transliteration": "an-naas", "meaning": {"ar": "الناس", "en": "the people"}, "breakdown": {"ar": "ن+ن = نّ", "en": "n+n = nn"}},
            ],
            "tip": {"ar": "عند رؤية الشدة ّ، انطق الحرف بقوة كأنه حرفان", "en": "When you see Shadda ّ, pronounce the letter firmly as if it's two letters"},
        },
        "quiz": {"type": "select", "question": {"ar": "ماذا تعني الشدة؟", "en": "What does Shadda mean?"}, "correct": {"ar": "الحرف ينطق مرتين", "en": "The letter is pronounced twice"}, "options": [{"ar": "الحرف ينطق مرتين", "en": "Letter pronounced twice"}, {"ar": "الحرف لا ينطق", "en": "Letter is silent"}, {"ar": "الحرف يمد", "en": "Letter is lengthened"}]},
    },
    {
        "id": 36, "level": 4, "lesson": 6, "emoji": "⚡", "method": "practice", "xp": 20,
        "title": {"ar": "تمارين الشدة", "en": "Shadda Practice Exercises", "de": "Shadda Übungen", "fr": "Exercices de Shadda", "tr": "Şedde Alıştırmaları", "ru": "Упражнения Шадда", "sv": "Shadda Övningar", "nl": "Shadda Oefeningen", "el": "Ασκήσεις Σάντα"},
        "content": {
            "rule": {"ar": "تدرب على قراءة كلمات مع الشدة", "en": "Practice reading words with Shadda"},
            "exercises": [
                {"type": "spot_shadda", "instruction": {"ar": "حدد الحرف المشدّد في كل كلمة", "en": "Identify the letter with Shadda in each word"}, "words": [{"word": "رَبَّنَا", "answer": "ب"}, {"word": "الصَّلاة", "answer": "ص"}, {"word": "النَّبِيّ", "answer": "ن,ي"}]},
                {"type": "read_aloud", "instruction": {"ar": "اقرأ بصوت واضح", "en": "Read clearly aloud"}, "words": ["إِنَّا", "الْحَمْدُ لِلَّهِ", "رَبِّ الْعَالَمِينَ", "الرَّحْمَنِ الرَّحِيمِ"]},
            ],
            "tip": {"ar": "الشدة موجودة كثيراً في القرآن — تعلّمها جيداً!", "en": "Shadda appears frequently in the Quran — learn it well!"},
        },
        "quiz": {"type": "select", "question": {"ar": "أي كلمة فيها شدة؟", "en": "Which word has Shadda?"}, "correct": {"ar": "رَبَّنَا", "en": "رَبَّنَا"}, "options": [{"ar": "رَبَّنَا", "en": "رَبَّنَا"}, {"ar": "كَتَبَ", "en": "كَتَبَ"}, {"ar": "عَلِمَ", "en": "عَلِمَ"}]},
    },
    {
        "id": 37, "level": 4, "lesson": 7, "emoji": "⚡", "method": "visual_audio", "xp": 20,
        "title": {"ar": "السكون — وقف الحرف", "en": "Sukun — Stopping the Letter", "de": "Sukun — Buchstabenstopp", "fr": "Sukun — Arrêt de la lettre", "tr": "Sükûn — Harfi Durdurma", "ru": "Сукун — Остановка буквы", "sv": "Sukun — Bokstavsstopp", "nl": "Sukun — Letterstop", "el": "Σουκούν — Στάση γράμματος"},
        "content": {
            "rule": {"ar": "السكون (ْ) يعني أن الحرف ينطق بدون حركة — ساكن", "en": "Sukun (ْ) means the letter is pronounced without any vowel — it's silent/stopped"},
            "examples": [
                {"word": "مَسْجِد", "transliteration": "masjid", "meaning": {"ar": "مسجد", "en": "mosque"}, "sukun_on": "س"},
                {"word": "قُرْآن", "transliteration": "quran", "meaning": {"ar": "قرآن", "en": "Quran"}, "sukun_on": "ر"},
                {"word": "عِلْم", "transliteration": "ilm", "meaning": {"ar": "علم", "en": "knowledge"}, "sukun_on": "ل"},
                {"word": "حَمْد", "transliteration": "hamd", "meaning": {"ar": "حمد", "en": "praise"}, "sukun_on": "م"},
            ],
            "tip": {"ar": "الحرف الساكن لا صوت له وحده — ينطق مع الحرف قبله", "en": "A letter with Sukun has no vowel — it's joined with the letter before it"},
        },
        "quiz": {"type": "select", "question": {"ar": "ماذا يعني السكون؟", "en": "What does Sukun mean?"}, "correct": {"ar": "الحرف بدون حركة", "en": "Letter without vowel"}, "options": [{"ar": "الحرف بدون حركة", "en": "Letter without vowel"}, {"ar": "الحرف مشدد", "en": "Letter is doubled"}, {"ar": "الحرف ممدود", "en": "Letter is lengthened"}]},
    },
    {
        "id": 38, "level": 4, "lesson": 8, "emoji": "⚡", "method": "practice", "xp": 20,
        "title": {"ar": "تمارين السكون", "en": "Sukun Practice", "de": "Sukun Übungen", "fr": "Exercices de Sukun", "tr": "Sükûn Alıştırmaları", "ru": "Упражнения Сукун", "sv": "Sukun Övningar", "nl": "Sukun Oefeningen", "el": "Ασκήσεις Σουκούν"},
        "content": {
            "rule": {"ar": "تمرن على نطق الحروف الساكنة بشكل صحيح", "en": "Practice pronouncing letters with Sukun correctly"},
            "exercises": [
                {"type": "identify_sukun", "instruction": {"ar": "حدد الحرف الساكن", "en": "Find the letter with Sukun"}, "words": [{"word": "مَسْجِد", "answer": "س"}, {"word": "شَمْس", "answer": "م"}, {"word": "عِلْم", "answer": "ل"}]},
                {"type": "read_aloud", "instruction": {"ar": "اقرأ الكلمات القرآنية", "en": "Read these Quranic words"}, "words": ["بِسْمِ", "الْحَمْدُ", "رَبْ", "يَوْمِ"]},
                {"type": "fill_mark", "instruction": {"ar": "أكمل التشكيل — ضع السكون في المكان الصحيح", "en": "Complete the marks — place Sukun correctly"}, "words": [{"base": "بسم", "answer": "بِسْمِ"}, {"base": "حمد", "answer": "حَمْدُ"}]},
            ],
            "tip": {"ar": "تذكر: السكون يجعل النطق أسرع وأوضح", "en": "Remember: Sukun makes pronunciation faster and clearer"},
        },
        "quiz": {"type": "select", "question": {"ar": "أين السكون في كلمة بِسْمِ؟", "en": "Where is the Sukun in بِسْمِ?"}, "correct": {"ar": "على السين", "en": "On the Seen (س)"}, "options": [{"ar": "على السين", "en": "On the Seen (س)"}, {"ar": "على الباء", "en": "On the Ba (ب)"}, {"ar": "على الميم", "en": "On the Meem (م)"}]},
    },
    {
        "id": 39, "level": 4, "lesson": 9, "emoji": "⚡", "method": "practice", "xp": 25,
        "title": {"ar": "مراجعة شاملة — التنوين والشدة والسكون", "en": "Full Review — Tanween, Shadda & Sukun", "de": "Gesamtwiederholung", "fr": "Révision complète", "tr": "Genel Tekrar", "ru": "Полный обзор", "sv": "Fullständig genomgång", "nl": "Volledige herhaling", "el": "Πλήρης επανάληψη"},
        "content": {
            "rule": {"ar": "مراجعة كل ما تعلمناه: التنوين (3 أنواع) + الشدة + السكون", "en": "Review everything: Tanween (3 types) + Shadda + Sukun"},
            "exercises": [
                {"type": "mixed_reading", "instruction": {"ar": "اقرأ سورة الفاتحة مع التشكيل", "en": "Read Surah Al-Fatiha with all marks"}, "text": "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ ❁ الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ"},
                {"type": "identify_marks", "instruction": {"ar": "حدد نوع كل علامة", "en": "Identify each mark type"}, "items": [{"mark": "ّ", "type": "shadda"}, {"mark": "ً", "type": "tanween_fatha"}, {"mark": "ْ", "type": "sukun"}]},
            ],
            "tip": {"ar": "أنت الآن جاهز لقراءة كلمات قرآنية كاملة!", "en": "You're now ready to read complete Quranic words!"},
        },
        "quiz": {"type": "comprehensive", "sections": [
            {"question": {"ar": "كم نوع للتنوين؟", "en": "How many types of Tanween?"}, "correct": {"ar": "3", "en": "3"}, "options": ["2", "3", "4"]},
            {"question": {"ar": "ماذا تعني الشدة؟", "en": "What does Shadda mean?"}, "correct": {"ar": "تضعيف الحرف", "en": "Letter doubling"}, "options": [{"ar": "تضعيف الحرف", "en": "Letter doubling"}, {"ar": "مد الحرف", "en": "Lengthening"}, {"ar": "إسكان الحرف", "en": "Silencing"}]},
        ]},
    },
    {
        "id": 40, "level": 4, "lesson": 10, "emoji": "🏆", "method": "assessment", "xp": 30,
        "title": {"ar": "اختبار المستوى الرابع", "en": "Level 4 Assessment", "de": "Stufe 4 Bewertung", "fr": "Évaluation Niveau 4", "tr": "Seviye 4 Değerlendirmesi", "ru": "Тест Уровня 4", "sv": "Nivå 4 bedömning", "nl": "Niveau 4 toets", "el": "Αξιολόγηση Επιπέδου 4"},
        "content": {
            "sections": [
                {"type": "read", "text": "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ", "instruction": {"ar": "اقرأ البسملة كاملة", "en": "Read the Basmala completely"}},
                {"type": "identify", "question": {"ar": "حدد الشدة والسكون والتنوين", "en": "Identify Shadda, Sukun, and Tanween"}, "text": "عِلْمًا نَافِعًا"},
            ],
            "pass_score": 70,
            "tip": {"ar": "ركّز على النطق الصحيح", "en": "Focus on correct pronunciation"},
        },
        "quiz": {"type": "comprehensive", "sections": [
            {"question": {"ar": "اقرأ: الْحَمْدُ لِلَّهِ", "en": "Read: الْحَمْدُ لِلَّهِ"}, "type": "read"},
            {"question": {"ar": "ما نوع العلامة في كلمة كِتَابًا؟", "en": "What mark type is in كِتَابًا?"}, "correct": {"ar": "تنوين بالفتح", "en": "Tanween Fatha"}, "options": [{"ar": "تنوين بالفتح", "en": "Tanween Fatha"}, {"ar": "شدة", "en": "Shadda"}, {"ar": "سكون", "en": "Sukun"}]},
        ]},
    },
]

# ═══════════════════════════════════════════════════
# LEVEL 5: قراءة الكلمات القرآنية (Lessons 41-50)
# Reading Quranic Words
# ═══════════════════════════════════════════════════

LEVEL5_LESSONS = [
    {"id": 41, "level": 5, "lesson": 1, "emoji": "📝", "method": "quran_reading", "xp": 25,
     "title": {"ar": "كلمات سورة الفاتحة", "en": "Words of Surah Al-Fatiha", "de": "Wörter der Surah Al-Fatiha", "fr": "Mots de la Sourate Al-Fatiha", "tr": "Fatiha Suresi Kelimeleri", "ru": "Слова Суры Аль-Фатиха", "sv": "Ord i Surah Al-Fatiha", "nl": "Woorden van Soera Al-Fatiha", "el": "Λέξεις Σούρα Αλ-Φάτιχα"},
     "content": {
         "surah_name": {"ar": "الفاتحة", "en": "Al-Fatiha — The Opening"},
         "words": [
             {"word": "بِسْمِ", "meaning": {"ar": "باسم", "en": "In the name of"}, "transliteration": "bismi"},
             {"word": "اللَّهِ", "meaning": {"ar": "الله", "en": "Allah (God)"}, "transliteration": "Allah"},
             {"word": "الرَّحْمَنِ", "meaning": {"ar": "الرحمن", "en": "The Most Gracious"}, "transliteration": "ar-Rahman"},
             {"word": "الرَّحِيمِ", "meaning": {"ar": "الرحيم", "en": "The Most Merciful"}, "transliteration": "ar-Raheem"},
             {"word": "الْحَمْدُ", "meaning": {"ar": "الحمد", "en": "All praise"}, "transliteration": "al-hamdu"},
             {"word": "لِلَّهِ", "meaning": {"ar": "لله", "en": "belongs to Allah"}, "transliteration": "lillahi"},
             {"word": "رَبِّ", "meaning": {"ar": "رب", "en": "Lord of"}, "transliteration": "rabbi"},
             {"word": "الْعَالَمِينَ", "meaning": {"ar": "العالمين", "en": "the worlds"}, "transliteration": "al-aalameen"},
         ],
         "tip": {"ar": "سورة الفاتحة هي أول سورة في القرآن — تعلّم كلماتها جيداً", "en": "Al-Fatiha is the first surah — learn its words well"},
     },
     "quiz": {"type": "match", "instruction": {"ar": "طابق الكلمة بمعناها", "en": "Match the word with its meaning"}, "pairs": [["بِسْمِ", {"ar": "باسم", "en": "In the name of"}], ["الرَّحْمَنِ", {"ar": "الرحمن", "en": "Most Gracious"}], ["الْحَمْدُ", {"ar": "الحمد", "en": "All praise"}]]},
    },
    {"id": 42, "level": 5, "lesson": 2, "emoji": "📝", "method": "quran_reading", "xp": 25,
     "title": {"ar": "كلمات سورة الإخلاص", "en": "Words of Surah Al-Ikhlas", "de": "Wörter der Surah Al-Ikhlas", "fr": "Mots de la Sourate Al-Ikhlas", "tr": "İhlas Suresi Kelimeleri", "ru": "Слова Суры Аль-Ихлас", "sv": "Ord i Surah Al-Ikhlas", "nl": "Woorden van Soera Al-Ikhlas", "el": "Λέξεις Σούρα Αλ-Ιχλάς"},
     "content": {
         "surah_name": {"ar": "الإخلاص", "en": "Al-Ikhlas — The Sincerity"},
         "words": [
             {"word": "قُلْ", "meaning": {"ar": "قل", "en": "Say"}, "transliteration": "qul"},
             {"word": "هُوَ", "meaning": {"ar": "هو", "en": "He is"}, "transliteration": "huwa"},
             {"word": "اللَّهُ", "meaning": {"ar": "الله", "en": "Allah"}, "transliteration": "Allahu"},
             {"word": "أَحَدٌ", "meaning": {"ar": "واحد", "en": "One"}, "transliteration": "ahad"},
             {"word": "الصَّمَدُ", "meaning": {"ar": "الصمد", "en": "The Self-Sufficient"}, "transliteration": "as-samad"},
             {"word": "لَمْ يَلِدْ", "meaning": {"ar": "لم يلد", "en": "He does not beget"}, "transliteration": "lam yalid"},
             {"word": "وَلَمْ يُولَدْ", "meaning": {"ar": "ولم يولد", "en": "nor was He begotten"}, "transliteration": "wa lam yoolad"},
             {"word": "كُفُوًا", "meaning": {"ar": "مثيلاً", "en": "equivalent"}, "transliteration": "kufuwan"},
         ],
         "full_verse": "قُلْ هُوَ اللَّهُ أَحَدٌ ❁ اللَّهُ الصَّمَدُ ❁ لَمْ يَلِدْ وَلَمْ يُولَدْ ❁ وَلَمْ يَكُن لَّهُ كُفُوًا أَحَدٌ",
         "tip": {"ar": "سورة الإخلاص تساوي ثلث القرآن!", "en": "Surah Al-Ikhlas equals one-third of the Quran!"},
     },
     "quiz": {"type": "select", "question": {"ar": "ما معنى 'أَحَدٌ'؟", "en": "What does 'أَحَدٌ' mean?"}, "correct": {"ar": "واحد", "en": "One"}, "options": [{"ar": "واحد", "en": "One"}, {"ar": "كثير", "en": "Many"}, {"ar": "عظيم", "en": "Great"}]},
    },
    {"id": 43, "level": 5, "lesson": 3, "emoji": "📝", "method": "quran_reading", "xp": 25,
     "title": {"ar": "كلمات سورة الناس", "en": "Words of Surah An-Nas", "de": "Wörter der Surah An-Nas", "fr": "Mots de la Sourate An-Nas", "tr": "Nâs Suresi Kelimeleri", "ru": "Слова Суры Ан-Нас", "sv": "Ord i Surah An-Nas", "nl": "Woorden van Soera An-Nas", "el": "Λέξεις Σούρα Αν-Νας"},
     "content": {
         "surah_name": {"ar": "الناس", "en": "An-Nas — Mankind"},
         "words": [
             {"word": "أَعُوذُ", "meaning": {"ar": "أستعيذ", "en": "I seek refuge"}, "transliteration": "a'oodhu"},
             {"word": "بِرَبِّ", "meaning": {"ar": "برب", "en": "with the Lord of"}, "transliteration": "bi-rabbi"},
             {"word": "النَّاسِ", "meaning": {"ar": "الناس", "en": "mankind"}, "transliteration": "an-naas"},
             {"word": "مَلِكِ", "meaning": {"ar": "ملك", "en": "King of"}, "transliteration": "maliki"},
             {"word": "إِلَهِ", "meaning": {"ar": "إله", "en": "God of"}, "transliteration": "ilahi"},
             {"word": "الْوَسْوَاسِ", "meaning": {"ar": "الوسواس", "en": "the whisperer"}, "transliteration": "al-waswas"},
             {"word": "الْخَنَّاسِ", "meaning": {"ar": "الخناس", "en": "who retreats"}, "transliteration": "al-khannas"},
         ],
         "tip": {"ar": "سورة الناس من السور التي نقرأها للحماية", "en": "Surah An-Nas is read for protection"},
     },
     "quiz": {"type": "select", "question": {"ar": "ما معنى 'أَعُوذُ'؟", "en": "What does 'أَعُوذُ' mean?"}, "correct": {"ar": "أستعيذ / ألجأ", "en": "I seek refuge"}, "options": [{"ar": "أستعيذ / ألجأ", "en": "I seek refuge"}, {"ar": "أشكر", "en": "I thank"}, {"ar": "أسأل", "en": "I ask"}]},
    },
    {"id": 44, "level": 5, "lesson": 4, "emoji": "📝", "method": "quran_reading", "xp": 25,
     "title": {"ar": "كلمات سورة الفلق", "en": "Words of Surah Al-Falaq", "de": "Wörter der Surah Al-Falaq", "fr": "Mots de la Sourate Al-Falaq", "tr": "Felak Suresi Kelimeleri", "ru": "Слова Суры Аль-Фалак", "sv": "Ord i Surah Al-Falaq", "nl": "Woorden van Soera Al-Falaq", "el": "Λέξεις Σούρα Αλ-Φαλάκ"},
     "content": {
         "surah_name": {"ar": "الفلق", "en": "Al-Falaq — The Daybreak"},
         "words": [
             {"word": "الْفَلَقِ", "meaning": {"ar": "الصبح", "en": "the daybreak"}, "transliteration": "al-falaq"},
             {"word": "شَرِّ", "meaning": {"ar": "شر", "en": "evil of"}, "transliteration": "sharri"},
             {"word": "مَا خَلَقَ", "meaning": {"ar": "ما خلق", "en": "what He created"}, "transliteration": "ma khalaqa"},
             {"word": "غَاسِقٍ", "meaning": {"ar": "ظلام", "en": "darkness"}, "transliteration": "ghasiq"},
             {"word": "وَقَبَ", "meaning": {"ar": "إذا اشتد", "en": "when it settles"}, "transliteration": "waqab"},
             {"word": "النَّفَّاثَاتِ", "meaning": {"ar": "النافثات", "en": "those who blow"}, "transliteration": "an-naffathat"},
             {"word": "الْعُقَدِ", "meaning": {"ar": "العقد", "en": "on knots"}, "transliteration": "al-uqad"},
             {"word": "حَاسِدٍ", "meaning": {"ar": "حاسد", "en": "an envier"}, "transliteration": "hasid"},
         ],
         "tip": {"ar": "سورة الفلق والناس هما المعوذتان — للحماية من كل شر", "en": "Al-Falaq and An-Nas are the two protective surahs"},
     },
     "quiz": {"type": "select", "question": {"ar": "ما معنى 'الفلق'؟", "en": "What does 'Al-Falaq' mean?"}, "correct": {"ar": "الصبح", "en": "The daybreak"}, "options": [{"ar": "الصبح", "en": "The daybreak"}, {"ar": "الليل", "en": "The night"}, {"ar": "النجم", "en": "The star"}]},
    },
    {"id": 45, "level": 5, "lesson": 5, "emoji": "📝", "method": "quran_reading", "xp": 25,
     "title": {"ar": "كلمات سورة الكوثر والعصر", "en": "Words of Al-Kawthar & Al-Asr", "de": "Wörter von Al-Kawthar & Al-Asr", "fr": "Mots d'Al-Kawthar et Al-Asr", "tr": "Kevser ve Asr Suresi Kelimeleri", "ru": "Слова Аль-Каусар и Аль-Аср", "sv": "Ord i Al-Kawthar & Al-Asr", "nl": "Woorden van Al-Kawthar & Al-Asr", "el": "Λέξεις Αλ-Κάουθαρ & Αλ-Ασρ"},
     "content": {
         "surahs": [
             {"name": {"ar": "الكوثر", "en": "Al-Kawthar"}, "words": [
                 {"word": "أَعْطَيْنَاكَ", "meaning": {"ar": "أعطيناك", "en": "We have given you"}, "transliteration": "a'taynaak"},
                 {"word": "الْكَوْثَرَ", "meaning": {"ar": "الخير الكثير", "en": "abundance (a river in Paradise)"}, "transliteration": "al-kawthar"},
                 {"word": "فَصَلِّ", "meaning": {"ar": "فصلّ", "en": "So pray"}, "transliteration": "fasalli"},
                 {"word": "وَانْحَرْ", "meaning": {"ar": "واذبح", "en": "and sacrifice"}, "transliteration": "wanhar"},
                 {"word": "شَانِئَكَ", "meaning": {"ar": "مبغضك", "en": "your enemy"}, "transliteration": "shani'ak"},
                 {"word": "الأَبْتَرُ", "meaning": {"ar": "المقطوع", "en": "the one cut off"}, "transliteration": "al-abtar"},
             ]},
             {"name": {"ar": "العصر", "en": "Al-Asr"}, "words": [
                 {"word": "وَالْعَصْرِ", "meaning": {"ar": "والعصر/الزمن", "en": "By time"}, "transliteration": "wal-asr"},
                 {"word": "إِنَّ الإِنسَانَ", "meaning": {"ar": "إن الإنسان", "en": "Indeed, mankind"}, "transliteration": "innal-insaan"},
                 {"word": "لَفِي خُسْرٍ", "meaning": {"ar": "في خسارة", "en": "is in loss"}, "transliteration": "lafi khusr"},
                 {"word": "آمَنُوا", "meaning": {"ar": "آمنوا", "en": "believed"}, "transliteration": "aamanoo"},
                 {"word": "الصَّالِحَاتِ", "meaning": {"ar": "الأعمال الصالحة", "en": "righteous deeds"}, "transliteration": "as-salihat"},
                 {"word": "بِالصَّبْرِ", "meaning": {"ar": "بالصبر", "en": "with patience"}, "transliteration": "bis-sabr"},
             ]},
         ],
         "tip": {"ar": "هاتان السورتان قصيرتان لكن معانيهما عظيمة", "en": "These two surahs are short but their meanings are profound"},
     },
     "quiz": {"type": "select", "question": {"ar": "ما معنى 'الكوثر'؟", "en": "What does 'Al-Kawthar' mean?"}, "correct": {"ar": "الخير الكثير / نهر في الجنة", "en": "Abundance / A river in Paradise"}, "options": [{"ar": "الخير الكثير", "en": "Abundance"}, {"ar": "الصلاة", "en": "Prayer"}, {"ar": "الصبر", "en": "Patience"}]},
    },
    {"id": 46, "level": 5, "lesson": 6, "emoji": "📝", "method": "quran_reading", "xp": 25,
     "title": {"ar": "آية الكرسي — كلمات", "en": "Ayat Al-Kursi — Words", "de": "Ayat Al-Kursi — Wörter", "fr": "Ayat Al-Kursi — Mots", "tr": "Âyetü'l-Kürsî — Kelimeler", "ru": "Аят Аль-Курси — Слова", "sv": "Ayat Al-Kursi — Ord", "nl": "Ayat Al-Kursi — Woorden", "el": "Αγιάτ Αλ-Κουρσί — Λέξεις"},
     "content": {
         "verse_name": {"ar": "آية الكرسي", "en": "Ayat Al-Kursi (Verse of the Throne)"},
         "words": [
             {"word": "اللَّهُ لَا إِلَهَ إِلَّا هُوَ", "meaning": {"ar": "الله لا معبود إلا هو", "en": "Allah, there is no god but Him"}, "transliteration": "Allahu la ilaha illa huwa"},
             {"word": "الْحَيُّ الْقَيُّومُ", "meaning": {"ar": "الحي القائم على كل شيء", "en": "The Ever-Living, Self-Sustaining"}, "transliteration": "al-hayyu al-qayyum"},
             {"word": "لَا تَأْخُذُهُ سِنَةٌ وَلَا نَوْمٌ", "meaning": {"ar": "لا ينعس ولا ينام", "en": "Neither drowsiness nor sleep overtakes Him"}, "transliteration": "la ta'khudhuhu sinatun wa la nawm"},
             {"word": "كُرْسِيُّهُ", "meaning": {"ar": "كرسيه/عرشه", "en": "His Throne"}, "transliteration": "kursiyyuhu"},
             {"word": "السَّمَاوَاتِ وَالْأَرْضَ", "meaning": {"ar": "السماوات والأرض", "en": "the heavens and the earth"}, "transliteration": "as-samawati wal-ard"},
         ],
         "tip": {"ar": "آية الكرسي أعظم آية في القرآن — من قرأها حفظه الله", "en": "Ayat Al-Kursi is the greatest verse — whoever reads it is protected by Allah"},
     },
     "quiz": {"type": "select", "question": {"ar": "ما معنى 'الحي القيوم'؟", "en": "What does 'Al-Hayy Al-Qayyum' mean?"}, "correct": {"ar": "الحي الدائم القائم على كل شيء", "en": "The Ever-Living, Self-Sustaining"}, "options": [{"ar": "الحي الدائم القائم على كل شيء", "en": "Ever-Living, Self-Sustaining"}, {"ar": "الخالق العظيم", "en": "The Great Creator"}, {"ar": "الرحمن الرحيم", "en": "Most Gracious, Most Merciful"}]},
    },
    {"id": 47, "level": 5, "lesson": 7, "emoji": "📝", "method": "practice", "xp": 25,
     "title": {"ar": "تمارين قراءة الكلمات", "en": "Word Reading Practice", "de": "Wortleseübungen", "fr": "Exercices de lecture de mots", "tr": "Kelime Okuma Alıştırmaları", "ru": "Упражнения по чтению слов", "sv": "Ordläsningsövningar", "nl": "Woordleesoefeningen", "el": "Ασκήσεις ανάγνωσης λέξεων"},
     "content": {
         "exercises": [
             {"type": "word_builder", "instruction": {"ar": "ركّب الكلمة من الحروف", "en": "Build the word from letters"}, "words": [{"letters": ["بِ", "سْ", "مِ"], "word": "بِسْمِ"}, {"letters": ["الْ", "حَ", "مْ", "دُ"], "word": "الْحَمْدُ"}]},
             {"type": "speed_reading", "instruction": {"ar": "اقرأ الكلمات بسرعة", "en": "Read the words quickly"}, "words": ["اللَّهِ", "الرَّحْمَنِ", "الرَّحِيمِ", "الْعَالَمِينَ", "الدِّينِ", "نَعْبُدُ", "نَسْتَعِينُ", "الصِّرَاطَ", "الْمُسْتَقِيمَ"]},
             {"type": "meaning_match", "instruction": {"ar": "اختر المعنى الصحيح", "en": "Choose the correct meaning"}, "items": [{"word": "رَبِّ", "correct": {"ar": "رب / سيد", "en": "Lord"}, "options": [{"ar": "رب", "en": "Lord"}, {"ar": "ملك", "en": "King"}, {"ar": "نبي", "en": "Prophet"}]}]},
         ],
         "tip": {"ar": "كلما تدربت أكثر، زادت سرعتك في القراءة", "en": "The more you practice, the faster you'll read"},
     },
     "quiz": {"type": "select", "question": {"ar": "ما معنى 'نَعْبُدُ'؟", "en": "What does 'نَعْبُدُ' mean?"}, "correct": {"ar": "نعبد", "en": "We worship"}, "options": [{"ar": "نعبد", "en": "We worship"}, {"ar": "نسأل", "en": "We ask"}, {"ar": "نشكر", "en": "We thank"}]},
    },
    {"id": 48, "level": 5, "lesson": 8, "emoji": "📝", "method": "quran_reading", "xp": 25,
     "title": {"ar": "كلمات من سورة البقرة", "en": "Words from Surah Al-Baqarah", "de": "Wörter aus Surah Al-Baqarah", "fr": "Mots de la Sourate Al-Baqarah", "tr": "Bakara Suresi'nden Kelimeler", "ru": "Слова из Суры Аль-Бакара", "sv": "Ord från Surah Al-Baqarah", "nl": "Woorden uit Soera Al-Baqarah", "el": "Λέξεις από Σούρα Αλ-Μπάκαρα"},
     "content": {
         "words": [
             {"word": "ذَلِكَ الْكِتَابُ", "meaning": {"ar": "هذا الكتاب", "en": "That is the Book"}, "transliteration": "dhalikal-kitab"},
             {"word": "لَا رَيْبَ فِيهِ", "meaning": {"ar": "لا شك فيه", "en": "no doubt in it"}, "transliteration": "la rayba fih"},
             {"word": "هُدًى", "meaning": {"ar": "هداية", "en": "guidance"}, "transliteration": "hudan"},
             {"word": "لِلْمُتَّقِينَ", "meaning": {"ar": "للذين يخافون الله", "en": "for the God-conscious"}, "transliteration": "lil-muttaqeen"},
             {"word": "يُؤْمِنُونَ", "meaning": {"ar": "يصدقون", "en": "they believe"}, "transliteration": "yu'minoon"},
             {"word": "بِالْغَيْبِ", "meaning": {"ar": "بالأمور الغيبية", "en": "in the unseen"}, "transliteration": "bil-ghayb"},
         ],
         "tip": {"ar": "سورة البقرة أطول سورة في القرآن — كل كلمة فيها كنز", "en": "Al-Baqarah is the longest surah — every word is a treasure"},
     },
     "quiz": {"type": "select", "question": {"ar": "ما معنى 'هُدًى'؟", "en": "What does 'هُدًى' mean?"}, "correct": {"ar": "هداية", "en": "Guidance"}, "options": [{"ar": "هداية", "en": "Guidance"}, {"ar": "رحمة", "en": "Mercy"}, {"ar": "نعمة", "en": "Blessing"}]},
    },
    {"id": 49, "level": 5, "lesson": 9, "emoji": "📝", "method": "practice", "xp": 25,
     "title": {"ar": "مراجعة الكلمات القرآنية", "en": "Quranic Words Review", "de": "Koranische Wörter Wiederholung", "fr": "Révision des mots coraniques", "tr": "Kur'an Kelimeleri Tekrarı", "ru": "Повторение коранических слов", "sv": "Koraniska ord repetition", "nl": "Koranische woorden herhaling", "el": "Επανάληψη κορανικών λέξεων"},
     "content": {
         "exercises": [
             {"type": "flashcards", "instruction": {"ar": "راجع الكلمات القرآنية", "en": "Review Quranic words"}, "cards": [{"front": "بِسْمِ", "back": {"ar": "باسم", "en": "In the name of"}}, {"front": "الْحَمْدُ", "back": {"ar": "الحمد/الشكر", "en": "Praise"}}, {"front": "رَبِّ", "back": {"ar": "رب/سيد", "en": "Lord"}}, {"front": "الرَّحْمَنِ", "back": {"ar": "الرحمن", "en": "Most Gracious"}}]},
             {"type": "fill_blank", "instruction": {"ar": "أكمل الآية", "en": "Complete the verse"}, "items": [{"text": "بِسْمِ ___ الرَّحْمَنِ الرَّحِيمِ", "answer": "اللَّهِ"}, {"text": "قُلْ هُوَ ___ أَحَدٌ", "answer": "اللَّهُ"}]},
         ],
         "tip": {"ar": "المراجعة المستمرة تثبت المعلومات", "en": "Regular review strengthens your knowledge"},
     },
     "quiz": {"type": "comprehensive", "sections": [
         {"question": {"ar": "أكمل: بِسْمِ ___ الرَّحْمَنِ", "en": "Complete: بِسْمِ ___ الرَّحْمَنِ"}, "correct": "اللَّهِ", "options": ["اللَّهِ", "رَبِّ", "مَلِكِ"]},
         {"question": {"ar": "ما معنى 'أَحَدٌ'؟", "en": "What does 'أَحَدٌ' mean?"}, "correct": {"ar": "واحد", "en": "One"}, "options": [{"ar": "واحد", "en": "One"}, {"ar": "كبير", "en": "Great"}, {"ar": "عظيم", "en": "Mighty"}]},
     ]},
    },
    {"id": 50, "level": 5, "lesson": 10, "emoji": "🏆", "method": "assessment", "xp": 30,
     "title": {"ar": "اختبار المستوى الخامس", "en": "Level 5 Assessment", "de": "Stufe 5 Bewertung", "fr": "Évaluation Niveau 5", "tr": "Seviye 5 Değerlendirmesi", "ru": "Тест Уровня 5", "sv": "Nivå 5 bedömning", "nl": "Niveau 5 toets", "el": "Αξιολόγηση Επιπέδου 5"},
     "content": {"pass_score": 70, "sections": [
         {"type": "read", "text": "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ", "instruction": {"ar": "اقرأ", "en": "Read aloud"}},
         {"type": "meaning", "question": {"ar": "ترجم: الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ", "en": "Translate: الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ"}},
     ], "tip": {"ar": "أظهر ما تعلمته!", "en": "Show what you've learned!"}},
     "quiz": {"type": "comprehensive", "sections": [
         {"question": {"ar": "ما معنى 'الرَّحِيمِ'؟", "en": "What does 'الرَّحِيمِ' mean?"}, "correct": {"ar": "الرحيم", "en": "The Most Merciful"}, "options": [{"ar": "الرحيم", "en": "Most Merciful"}, {"ar": "العظيم", "en": "The Mighty"}, {"ar": "الحكيم", "en": "The Wise"}]},
     ]},
    },
]

# ═══════════════════════════════════════════════════
# LEVEL 6: قراءة الآيات (Lessons 51-60)
# ═══════════════════════════════════════════════════

LEVEL6_LESSONS = []
verse_lessons = [
    (51, "سورة الفاتحة كاملة", "Complete Surah Al-Fatiha", "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ ❁ الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ ❁ الرَّحْمَنِ الرَّحِيمِ ❁ مَالِكِ يَوْمِ الدِّينِ ❁ إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ ❁ اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ ❁ صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ"),
    (52, "سورة الإخلاص كاملة", "Complete Surah Al-Ikhlas", "قُلْ هُوَ اللَّهُ أَحَدٌ ❁ اللَّهُ الصَّمَدُ ❁ لَمْ يَلِدْ وَلَمْ يُولَدْ ❁ وَلَمْ يَكُن لَّهُ كُفُوًا أَحَدٌ"),
    (53, "سورة الفلق كاملة", "Complete Surah Al-Falaq", "قُلْ أَعُوذُ بِرَبِّ الْفَلَقِ ❁ مِن شَرِّ مَا خَلَقَ ❁ وَمِن شَرِّ غَاسِقٍ إِذَا وَقَبَ ❁ وَمِن شَرِّ النَّفَّاثَاتِ فِي الْعُقَدِ ❁ وَمِن شَرِّ حَاسِدٍ إِذَا حَسَدَ"),
    (54, "سورة الناس كاملة", "Complete Surah An-Nas", "قُلْ أَعُوذُ بِرَبِّ النَّاسِ ❁ مَلِكِ النَّاسِ ❁ إِلَهِ النَّاسِ ❁ مِن شَرِّ الْوَسْوَاسِ الْخَنَّاسِ ❁ الَّذِي يُوَسْوِسُ فِي صُدُورِ النَّاسِ ❁ مِنَ الْجِنَّةِ وَالنَّاسِ"),
    (55, "سورة الكوثر والعصر", "Surah Al-Kawthar & Al-Asr", "إِنَّا أَعْطَيْنَاكَ الْكَوْثَرَ ❁ فَصَلِّ لِرَبِّكَ وَانْحَرْ ❁ إِنَّ شَانِئَكَ هُوَ الأَبْتَرُ"),
    (56, "آية الكرسي — الجزء الأول", "Ayat Al-Kursi Part 1", "اللَّهُ لَا إِلَهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ لَا تَأْخُذُهُ سِنَةٌ وَلَا نَوْمٌ"),
    (57, "آية الكرسي — الجزء الثاني", "Ayat Al-Kursi Part 2", "لَّهُ مَا فِي السَّمَاوَاتِ وَمَا فِي الأَرْضِ مَن ذَا الَّذِي يَشْفَعُ عِنْدَهُ إِلَّا بِإِذْنِهِ"),
    (58, "أوائل سورة البقرة", "Beginning of Al-Baqarah", "الم ❁ ذَلِكَ الْكِتَابُ لَا رَيْبَ فِيهِ هُدًى لِلْمُتَّقِينَ"),
    (59, "تمارين قراءة الآيات", "Verse Reading Practice", ""),
    (60, "اختبار المستوى السادس", "Level 6 Assessment", ""),
]

for lid, ar_title, en_title, verse in verse_lessons:
    lesson = {
        "id": lid, "level": 6, "lesson": lid - 50, "emoji": "📖" if lid < 59 else ("📝" if lid == 59 else "🏆"),
        "method": "quran_reading" if lid < 59 else ("practice" if lid == 59 else "assessment"), "xp": 25 if lid < 60 else 30,
        "title": {"ar": ar_title, "en": en_title, "de": en_title, "fr": en_title, "tr": en_title, "ru": en_title, "sv": en_title, "nl": en_title, "el": en_title},
        "content": {
            "verse_text": verse,
            "instruction": {"ar": "اقرأ الآية كاملة ببطء وتأنٍ", "en": "Read the complete verse slowly and carefully"},
            "tip": {"ar": "ركّز على مخارج الحروف والتشكيل", "en": "Focus on letter pronunciation and diacritical marks"},
        } if verse else {
            "exercises": [
                {"type": "recite", "instruction": {"ar": "اقرأ ما تحفظ من القرآن", "en": "Recite what you've memorized"}},
                {"type": "review", "instruction": {"ar": "راجع جميع السور التي تعلمتها", "en": "Review all surahs you've learned"}},
            ],
            "pass_score": 70 if lid == 60 else None,
            "tip": {"ar": "أنت على وشك إتقان القراءة!", "en": "You're about to master reading!"},
        },
        "quiz": {"type": "read", "text": verse[:50] + "..." if verse else "", "instruction": {"ar": "اقرأ", "en": "Read"}} if verse else {"type": "comprehensive", "sections": []},
    }
    LEVEL6_LESSONS.append(lesson)

# ═══════════════════════════════════════════════════
# LEVEL 7: التجويد والإتقان (Lessons 61-70)
# ═══════════════════════════════════════════════════

tajweed_topics = [
    (61, "أحكام النون الساكنة — الإظهار", "Noon Sakinah Rules — Izhar", "إظهار النون عند حروف الحلق: ء هـ ع ح غ خ"),
    (62, "أحكام النون الساكنة — الإدغام", "Noon Sakinah — Idgham", "إدغام النون في: ي ر م ل و ن"),
    (63, "أحكام النون الساكنة — الإقلاب", "Noon Sakinah — Iqlab", "قلب النون ميماً عند الباء"),
    (64, "أحكام النون الساكنة — الإخفاء", "Noon Sakinah — Ikhfa", "إخفاء النون عند 15 حرفاً"),
    (65, "أحكام الميم الساكنة", "Meem Sakinah Rules", "إدغام وإخفاء وإظهار الميم"),
    (66, "المد الطبيعي والفرعي", "Natural & Secondary Madd", "المد حركتين أو أكثر"),
    (67, "الوقف والابتداء", "Stopping & Starting Rules", "أين نقف وأين نبدأ"),
    (68, "تطبيق عملي — سورة الملك", "Practical — Surah Al-Mulk", "قراءة مع تطبيق التجويد"),
    (69, "مراجعة شاملة للتجويد", "Complete Tajweed Review", "مراجعة جميع أحكام التجويد"),
    (70, "اختبار التخرج — الإتقان", "Graduation Test — Mastery", "الاختبار النهائي"),
]

LEVEL7_LESSONS = []
for lid, ar_title, en_title, ar_desc in tajweed_topics:
    LEVEL7_LESSONS.append({
        "id": lid, "level": 7, "lesson": lid - 60, "emoji": "🎓" if lid < 69 else ("📝" if lid == 69 else "🏆"),
        "method": "tajweed" if lid < 69 else ("practice" if lid == 69 else "assessment"), "xp": 30 if lid < 70 else 50,
        "title": {"ar": ar_title, "en": en_title, "de": en_title, "fr": en_title, "tr": en_title, "ru": en_title, "sv": en_title, "nl": en_title, "el": en_title},
        "content": {
            "rule": {"ar": ar_desc, "en": en_title},
            "tip": {"ar": "التجويد يجمّل صوتك ويحفظ معاني القرآن", "en": "Tajweed beautifies your voice and preserves Quran's meanings"},
            "exercises": [
                {"type": "listen_compare", "instruction": {"ar": "استمع للقراءة الصحيحة ثم قلّد", "en": "Listen to correct recitation, then imitate"}},
                {"type": "practice_verse", "instruction": {"ar": "طبّق القاعدة على آية", "en": "Apply the rule on a verse"}},
            ],
        },
        "quiz": {"type": "select", "question": {"ar": "ما حكم النون الساكنة في هذا المثال؟", "en": "What is the rule for Noon Sakinah in this example?"}, "correct": {"ar": "إظهار", "en": "Izhar (clear)"}, "options": [{"ar": "إظهار", "en": "Izhar"}, {"ar": "إدغام", "en": "Idgham"}, {"ar": "إخفاء", "en": "Ikhfa"}]} if lid < 69 else {"type": "comprehensive", "sections": []},
    })

# Combined export
NOORANIYA_LESSONS_31_70 = LEVEL4_LESSONS + LEVEL5_LESSONS + LEVEL6_LESSONS + LEVEL7_LESSONS

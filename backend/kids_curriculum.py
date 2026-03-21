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
# CONTENT DATA POOLS
# ═══════════════════════════════════════════════════════════════

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
            lesson["title"] = {"ar": f"حرف {lt['name_ar']}", "en": f"Letter {lt['name_en']}"}
            lesson["sections"] = [
                {"type": "learn", "emoji": "📝", "title": _t("تعرّف على الحرف", "Meet the Letter", lang),
                 "content": {"letter": lt["letter"], "name_ar": lt["name_ar"], "name_en": lt["name_en"],
                             "sound": lt["sound"], "example_word": lt["word"], "example_en": lt["word_en"],
                             "example_emoji": lt["emoji"]}},
                {"type": "listen", "emoji": "🔊", "title": _t("استمع وردد", "Listen & Repeat", lang),
                 "content": {"text": lt["letter"], "word": lt["word"], "tip": _t("اضغط على الحرف للاستماع ثم ردد بصوت عالٍ", "Tap the letter to listen, then repeat out loud", lang)}},
                {"type": "quiz", "emoji": "❓", "title": _t("اختبر نفسك", "Test Yourself", lang),
                 "content": {"question": _t(f"أي حرف صوته {lt['sound']}؟", f"Which letter sounds like {lt['sound']}?", lang),
                             "correct": lt["letter"],
                             "options": _make_letter_options(lt["letter"], lesson_in_stage)}},
                {"type": "write", "emoji": "✍️", "title": _t("تدرب على الكتابة", "Practice Writing", lang),
                 "content": {"letter": lt["letter"], "tip": _t("اكتب الحرف 5 مرات على ورقة", "Write the letter 5 times on paper", lang)}},
            ]
        elif lesson_in_stage < 42:
            # Day 29-42: Letter forms (beginning, middle, end)
            idx = (lesson_in_stage - 28) * 2
            if idx < 28:
                lt = LETTERS_28[idx]
                lt2 = LETTERS_28[min(idx+1, 27)]
                lesson["title"] = {"ar": f"أشكال {lt['name_ar']} و{lt2['name_ar']}", "en": f"Forms of {lt['name_en']} & {lt2['name_en']}"}
                lesson["sections"] = [
                    {"type": "learn", "emoji": "📝", "title": _t("أشكال الحرف", "Letter Forms", lang),
                     "content": {"letters": [
                         {"letter": lt["letter"], "forms": lt["forms"], "name": lt["name_en"]},
                         {"letter": lt2["letter"], "forms": lt2["forms"], "name": lt2["name_en"]},
                     ]}},
                    {"type": "practice", "emoji": "🎯", "title": _t("تمرين", "Practice", lang),
                     "content": {"tip": _t("جد الحرف في أشكاله المختلفة", "Find the letter in its different forms", lang)}},
                ]
            else:
                lesson["title"] = {"ar": "مراجعة الأشكال", "en": "Review Letter Forms"}
                lesson["sections"] = [{"type": "review", "emoji": "🔄", "title": _t("مراجعة شاملة", "Full Review", lang),
                     "content": {"tip": _t("راجع جميع أشكال الحروف", "Review all letter forms", lang)}}]
        else:
            # Day 43-56: Writing and connection practice
            review_idx = (lesson_in_stage - 42) * 2
            lt = LETTERS_28[min(review_idx, 27)]
            lesson["title"] = {"ar": f"تمرين كتابة وتوصيل", "en": f"Writing & Connection Practice"}
            lesson["sections"] = [
                {"type": "connect", "emoji": "🔗", "title": _t("وصّل الحروف", "Connect Letters", lang),
                 "content": {"tip": _t("تعلم كيف تتصل الحروف ببعضها", "Learn how letters connect together", lang)}},
                {"type": "write", "emoji": "✍️", "title": _t("اكتب كلمة", "Write a Word", lang),
                 "content": {"word": lt["word"], "word_en": lt["word_en"], "tip": _t("اكتب الكلمة ببطء وحرفاً حرفاً", "Write the word slowly, letter by letter", lang)}},
            ]
    
    # ═══ STAGE 2: VOWELS (Days 57-84) ═══
    elif stage_id == "S02":
        h_idx = lesson_in_stage % len(HARAKAT)
        h = HARAKAT[h_idx]
        if lesson_in_stage < len(HARAKAT) * 3:
            lesson["title"] = {"ar": h["name_ar"], "en": h["name_en"]}
            lesson["sections"] = [
                {"type": "learn", "emoji": "🎵", "title": _t(f"تعرّف على {h['name_ar']}", f"Learn {h['name_en']}", lang),
                 "content": {"name_ar": h["name_ar"], "name_en": h["name_en"], "symbol": h["symbol"],
                             "sound": h["sound"], "example": h["example"],
                             "example_word": h["example_word"], "meaning": h["meaning"]}},
                {"type": "practice", "emoji": "🎯", "title": _t("تمرين", "Practice", lang),
                 "content": {"tip": _t(f"اقرأ الحروف مع {h['name_ar']}", f"Read letters with {h['name_en']}", lang),
                             "items": [f"{lt['letter']}{h['symbol']}" for lt in LETTERS_28[:7]]}},
                {"type": "quiz", "emoji": "❓", "title": _t("اختبر نفسك", "Test", lang),
                 "content": {"question": _t(f"ما صوت هذه الحركة: {h['symbol']}؟", f"What sound does this diacritic make: {h['symbol']}?", lang),
                             "correct": h["sound"], "options": [h["sound"], HARAKAT[(h_idx+1)%len(HARAKAT)]["sound"], HARAKAT[(h_idx+2)%len(HARAKAT)]["sound"]]}},
            ]
        else:
            lesson["title"] = {"ar": "مراجعة الحركات", "en": "Vowels Review"}
            lesson["sections"] = [{"type": "review", "emoji": "🔄", "title": _t("مراجعة", "Review", lang),
                 "content": {"items": [{"name": h["name_en"], "symbol": h["symbol"], "sound": h["sound"]} for h in HARAKAT]}}]
    
    # ═══ STAGE 3: NUMBERS (Days 85-112) ═══
    elif stage_id == "S03":
        n_idx = lesson_in_stage % len(NUMBERS_FULL)
        n = NUMBERS_FULL[n_idx]
        lesson["title"] = {"ar": f"العدد {n['ar']}", "en": f"Number {n['en']}"}
        lesson["sections"] = [
            {"type": "learn", "emoji": "🔢", "title": _t(f"تعلم العدد {n['display']}", f"Learn Number {n['num']}", lang),
             "content": {"number": n["num"], "arabic": n["ar"], "english": n["en"], "display": n["display"]}},
            {"type": "practice", "emoji": "🎯", "title": _t("عُدّ معنا", "Count With Us", lang),
             "content": {"tip": _t(f"عُدّ من ١ إلى {n['display']}", f"Count from 1 to {n['num']}", lang)}},
            {"type": "quiz", "emoji": "❓", "title": _t("اختبر", "Test", lang),
             "content": {"question": _t(f"ما هذا العدد: {n['display']}؟", f"What number is this: {n['display']}?", lang),
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
        
        cat_titles = {"colors":"Colors","animals":"Animals","family":"Family","body":"Body","food":"Food","home":"Home","nature":"Nature","school":"School","greetings":"Greetings"}
        cat_ar = {"colors":"ألوان","animals":"حيوانات","family":"عائلة","body":"جسم","food":"طعام","home":"بيت","nature":"طبيعة","school":"مدرسة","greetings":"تحيات"}
        
        lesson["title"] = {"ar": f"{cat_ar.get(cat,cat)}: {word['ar']}", "en": f"{cat_titles.get(cat,cat)}: {word['en']}"}
        lesson["sections"] = [
            {"type": "learn", "emoji": word.get("emoji","📝"), "title": _t(f"كلمة جديدة: {word['ar']}", f"New Word: {word['en']}", lang),
             "content": {"arabic": word["ar"], "english": word["en"], "emoji": word.get("emoji",""), "category": cat}},
            {"type": "listen", "emoji": "🔊", "title": _t("استمع وردد", "Listen & Repeat", lang),
             "content": {"text": word["ar"], "tip": _t("انطق الكلمة بصوت عالٍ", "Say the word out loud", lang)}},
            {"type": "quiz", "emoji": "❓", "title": _t("اختبر", "Test", lang),
             "content": {"question": _t(f"ما معنى {word['emoji']} بالعربية؟", f"What is {word['emoji']} in Arabic?", lang),
                         "correct": word["ar"],
                         "options": [word["ar"]] + [w["ar"] for w in random.sample([w2 for w2 in words if w2["ar"]!=word["ar"]], min(2, len(words)-1))]}},
        ]
    
    # ═══ STAGE 5: SIMPLE SENTENCES (Days 211-266) ═══
    elif stage_id == "S05":
        s_idx = lesson_in_stage % len(SENTENCES_BASIC)
        sent = SENTENCES_BASIC[s_idx]
        lesson["title"] = {"ar": sent["ar"], "en": sent["en"]}
        lesson["sections"] = [
            {"type": "learn", "emoji": sent["emoji"], "title": _t("جملة جديدة", "New Sentence", lang),
             "content": {"arabic": sent["ar"], "english": sent["en"], "emoji": sent["emoji"]}},
            {"type": "listen", "emoji": "🔊", "title": _t("استمع وردد", "Listen & Repeat", lang),
             "content": {"text": sent["ar"], "tip": _t("ردد الجملة كاملة", "Repeat the full sentence", lang)}},
            {"type": "practice", "emoji": "✍️", "title": _t("اكتب الجملة", "Write the Sentence", lang),
             "content": {"tip": _t("اكتب الجملة 3 مرات", "Write the sentence 3 times", lang), "sentence": sent["ar"]}},
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


def _t(ar: str, en: str, lang: str) -> str:
    """Quick translate - returns Arabic for ar, English for all others."""
    return ar if lang == "ar" else en


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
            {"type": "read", "emoji": "📖", "title": _t("اقرأ الكلمة", "Read the Word", lang),
             "content": {"arabic": w["ar"], "english": w["en"], "emoji": w.get("emoji","")}},
            {"type": "listen", "emoji": "🔊", "title": _t("استمع وردد", "Listen & Repeat", lang),
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
            {"type": "learn", "emoji": "🤲", "title": _t("تعلم", "Learn", lang),
             "content": {"arabic": tc["ar"], "english": tc["en"]}},
            {"type": "memorize", "emoji": "🧠", "title": _t("احفظ", "Memorize", lang),
             "content": {"text": tc["ar"], "tip": _t("اقرأ 3 مرات ثم ردد من الذاكرة", "Read 3 times then repeat from memory", lang)}},
        ]
    
    elif stage_id in ["S08","S14"]:  # Quran Memorization
        from kids_learning import QURAN_SURAHS_FOR_KIDS
        s_idx = lesson_idx // 7
        a_idx = lesson_idx % 7
        if s_idx < len(QURAN_SURAHS_FOR_KIDS):
            surah = QURAN_SURAHS_FOR_KIDS[s_idx]
            ayah = surah["ayahs"][a_idx % len(surah["ayahs"])]
            sections = [
                {"type": "quran", "emoji": "📖", "title": _t(f"حفظ: {surah['name_ar']}", f"Memorize: {surah['name_en']}", lang),
                 "content": {"surah": surah["name_en"], "ayah_num": ayah["num"],
                             "arabic": ayah["ar"], "translation": ayah.get(lang, ayah["en"])}},
                {"type": "listen", "emoji": "🔊", "title": _t("استمع", "Listen", lang),
                 "content": {"text": ayah["ar"]}},
                {"type": "memorize", "emoji": "🧠", "title": _t("سمّع", "Recite", lang),
                 "content": {"tip": _t("أغلق عينيك وسمّع الآية", "Close your eyes and recite the ayah", lang)}},
            ]
        else:
            sections = [{"type": "review", "emoji": "🔄", "title": _t("مراجعة", "Review", lang), "content": {}}]
    
    elif stage_id == "S09":  # Duas
        from kids_learning import KIDS_DUAS
        d = KIDS_DUAS[lesson_idx % len(KIDS_DUAS)]
        sections = [
            {"type": "dua", "emoji": d["emoji"], "title": d["title"].get(lang, d["title"]["en"]),
             "content": {"arabic": d["ar"], "transliteration": d["transliteration"], "meaning": d.get(lang, d["en"])}},
            {"type": "memorize", "emoji": "🧠", "title": _t("احفظ الدعاء", "Memorize the Dua", lang),
             "content": {"tip": _t("ردد الدعاء 5 مرات", "Repeat the dua 5 times", lang)}},
        ]
    
    elif stage_id == "S10":  # Hadiths
        from kids_learning import KIDS_HADITHS
        h = KIDS_HADITHS[lesson_idx % len(KIDS_HADITHS)]
        sections = [
            {"type": "hadith", "emoji": h["emoji"], "title": _t("حديث اليوم", "Today's Hadith", lang),
             "content": {"arabic": h["ar"], "translation": h.get(lang, h["en"]), "source": h["source"],
                         "lesson": h["lesson"].get(lang, h["lesson"]["en"])}},
            {"type": "reflect", "emoji": "💭", "title": _t("تأمل", "Reflect", lang),
             "content": {"tip": _t("فكر كيف تطبق هذا الحديث في حياتك", "Think about how to apply this hadith in your life", lang)}},
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
        t = topics[lesson_idx % len(topics)]
        sections = [
            {"type": "learn", "emoji": t["emoji"], "title": _t("تعلم", "Learn", lang),
             "content": {"arabic": t["ar"], "english": t["en"]}},
        ]
    
    elif stage_id == "S13":  # Advanced Arabic
        sections = [
            {"type": "grammar", "emoji": "📚", "title": _t("قواعد", "Grammar", lang),
             "content": {"tip": _t("تعلم قواعد جديدة", "Learn new grammar rules", lang)}},
        ]
    
    elif stage_id == "S15":  # Mastery
        sections = [
            {"type": "review", "emoji": "🎓", "title": _t("مراجعة شاملة", "Comprehensive Review", lang),
             "content": {"tip": _t("راجع كل ما تعلمته!", "Review everything you learned!", lang)}},
        ]
    
    # Ensure at least one section
    if not sections:
        sections = [{"type": "learn", "emoji": "📝", "title": _t("درس", "Lesson", lang), "content": {}}]
    
    return sections

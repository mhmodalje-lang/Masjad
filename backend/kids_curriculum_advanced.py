"""
Advanced Curriculum Content for Stages 6-15
============================================
Comprehensive educational content for Noor Academy
Each stage has deep, rich, multi-section daily lessons
"""
from localization_engine import t, get_cat_name
import random

# ═══════════════════════════════════════════════════════════════
# STAGE 6: READING PRACTICE (Days 267-308, 42 days)
# Progressive reading: words → phrases → sentences → paragraphs
# ═══════════════════════════════════════════════════════════════

READING_PASSAGES = [
    # Level 1: Short simple sentences (Days 1-14)
    {"ar": "ذَهَبَ أحمدُ إلى المسجدِ", "en": "Ahmad went to the mosque", "level": 1, "emoji": "🕌",
     "question_ar": "أين ذهب أحمد؟", "question_en": "Where did Ahmad go?",
     "answer_ar": "إلى المسجد", "answer_en": "To the mosque",
     "options_ar": ["إلى المسجد", "إلى المدرسة", "إلى البيت"]},
    {"ar": "قرأتْ فاطمةُ القرآنَ الكريمَ", "en": "Fatima read the Holy Quran", "level": 1, "emoji": "📖",
     "question_ar": "ماذا قرأت فاطمة؟", "question_en": "What did Fatima read?",
     "answer_ar": "القرآن الكريم", "answer_en": "The Holy Quran",
     "options_ar": ["القرآن الكريم", "كتاب القصص", "الجريدة"]},
    {"ar": "صلّى الأبُ صلاةَ الفجرِ في المسجدِ", "en": "The father prayed Fajr at the mosque", "level": 1, "emoji": "🌅",
     "question_ar": "أي صلاة صلاها الأب؟", "question_en": "Which prayer did the father pray?",
     "answer_ar": "صلاة الفجر", "answer_en": "Fajr prayer",
     "options_ar": ["صلاة الفجر", "صلاة الظهر", "صلاة العشاء"]},
    {"ar": "أكلَ الطفلُ التمرَ وشربَ الحليبَ", "en": "The child ate dates and drank milk", "level": 1, "emoji": "🥛",
     "question_ar": "ماذا أكل الطفل؟", "question_en": "What did the child eat?",
     "answer_ar": "التمر", "answer_en": "Dates",
     "options_ar": ["التمر", "التفاح", "الخبز"]},
    {"ar": "قالَ الولدُ: بسمِ اللهِ الرحمنِ الرحيمِ", "en": "The boy said: In the name of Allah", "level": 1, "emoji": "🤲",
     "question_ar": "ماذا قال الولد؟", "question_en": "What did the boy say?",
     "answer_ar": "بسم الله الرحمن الرحيم", "answer_en": "Bismillah",
     "options_ar": ["بسم الله الرحمن الرحيم", "الحمد لله", "سبحان الله"]},
    {"ar": "تَوَضَّأَ المسلمُ قبلَ الصلاةِ", "en": "The Muslim made wudu before prayer", "level": 1, "emoji": "💧",
     "question_ar": "ماذا فعل المسلم قبل الصلاة؟", "question_en": "What did the Muslim do before prayer?",
     "answer_ar": "توضأ", "answer_en": "Made wudu",
     "options_ar": ["توضأ", "نام", "أكل"]},
    {"ar": "ساعَدَ الولدُ أمَّهُ في البيتِ", "en": "The boy helped his mother at home", "level": 1, "emoji": "❤️",
     "question_ar": "من ساعد الولد؟", "question_en": "Who did the boy help?",
     "answer_ar": "أمه", "answer_en": "His mother",
     "options_ar": ["أمه", "صديقه", "معلمه"]},
    {"ar": "زارَ عليٌّ جدَّهُ يومَ الجمعةِ", "en": "Ali visited his grandfather on Friday", "level": 1, "emoji": "👴",
     "question_ar": "متى زار علي جده؟", "question_en": "When did Ali visit his grandfather?",
     "answer_ar": "يوم الجمعة", "answer_en": "On Friday",
     "options_ar": ["يوم الجمعة", "يوم السبت", "يوم الاثنين"]},
    {"ar": "حفظَ الطالبُ سورةَ الإخلاصِ", "en": "The student memorized Surah Al-Ikhlas", "level": 1, "emoji": "⭐",
     "question_ar": "أي سورة حفظ الطالب؟", "question_en": "Which surah did the student memorize?",
     "answer_ar": "سورة الإخلاص", "answer_en": "Surah Al-Ikhlas",
     "options_ar": ["سورة الإخلاص", "سورة الفاتحة", "سورة الناس"]},
    {"ar": "نامَ الطفلُ بعدَ قراءةِ أذكارِ النومِ", "en": "The child slept after reading sleep duas", "level": 1, "emoji": "🌙",
     "question_ar": "ماذا قرأ الطفل قبل النوم؟", "question_en": "What did the child read before sleeping?",
     "answer_ar": "أذكار النوم", "answer_en": "Sleep duas",
     "options_ar": ["أذكار النوم", "قصة", "أغنية"]},
    {"ar": "شَكَرَ أحمدُ اللهَ على نعمةِ الطعامِ", "en": "Ahmad thanked Allah for the blessing of food", "level": 1, "emoji": "🙏",
     "question_ar": "على ماذا شكر أحمد الله؟", "question_en": "What did Ahmad thank Allah for?",
     "answer_ar": "نعمة الطعام", "answer_en": "The blessing of food",
     "options_ar": ["نعمة الطعام", "نعمة اللعب", "نعمة النوم"]},
    {"ar": "تَصَدَّقَ الرجلُ على الفقراءِ", "en": "The man gave charity to the poor", "level": 1, "emoji": "💝",
     "question_ar": "ماذا فعل الرجل؟", "question_en": "What did the man do?",
     "answer_ar": "تصدق على الفقراء", "answer_en": "Gave charity to the poor",
     "options_ar": ["تصدق على الفقراء", "لعب كرة القدم", "ذهب للسوق"]},
    {"ar": "استيقظَ عمرُ مبكرًا لصلاةِ الفجرِ", "en": "Omar woke up early for Fajr prayer", "level": 1, "emoji": "🌄",
     "question_ar": "لماذا استيقظ عمر مبكرًا؟", "question_en": "Why did Omar wake up early?",
     "answer_ar": "لصلاة الفجر", "answer_en": "For Fajr prayer",
     "options_ar": ["لصلاة الفجر", "للعب", "للمدرسة"]},
    {"ar": "أحبَّتْ مريمُ القراءةَ كثيرًا", "en": "Maryam loved reading very much", "level": 1, "emoji": "📚",
     "question_ar": "ماذا أحبت مريم؟", "question_en": "What did Maryam love?",
     "answer_ar": "القراءة", "answer_en": "Reading",
     "options_ar": ["القراءة", "الرسم", "الطبخ"]},
    # Level 2: Short paragraphs (Days 15-28)
    {"ar": "في يومِ الجُمعةِ، ذَهَبَ أحمدُ مع أبيهِ إلى المسجدِ. صلّيا صلاةَ الجمعةِ واستمعا لخطبةِ الإمامِ. تعلَّمَ أحمدُ أنَّ صلاةَ الجمعةِ مِن أفضلِ الصلواتِ.", 
     "en": "On Friday, Ahmad went with his father to the mosque. They prayed Jumu'ah and listened to the imam's sermon. Ahmad learned that Friday prayer is one of the best prayers.",
     "level": 2, "emoji": "🕌",
     "question_ar": "ماذا تعلم أحمد؟", "question_en": "What did Ahmad learn?",
     "answer_ar": "أن صلاة الجمعة من أفضل الصلوات", "answer_en": "Friday prayer is one of the best",
     "options_ar": ["أن صلاة الجمعة من أفضل الصلوات", "أن المسجد كبير", "أن الإمام طويل"]},
    {"ar": "كانَ رمضانُ شهرًا مباركًا. صامَتْ العائلةُ كلُّها. أفطروا معًا على التمرِ والماءِ. ثمَّ صلّوا صلاةَ التراويحِ في المسجدِ.",
     "en": "Ramadan was a blessed month. The whole family fasted. They broke their fast together with dates and water. Then they prayed Taraweeh at the mosque.",
     "level": 2, "emoji": "🌙",
     "question_ar": "على ماذا أفطرت العائلة؟", "question_en": "What did the family break their fast with?",
     "answer_ar": "التمر والماء", "answer_en": "Dates and water",
     "options_ar": ["التمر والماء", "الأرز واللحم", "الخبز والجبن"]},
    {"ar": "حَفِظَتْ سارةُ سورةَ الفاتحةِ كاملةً. فَرِحَتْ أمُّها كثيرًا وقالَتْ لها: بارَكَ اللهُ فيكِ يا بُنيَّتي! أنتِ ذكيةٌ ومُجتهدةٌ.",
     "en": "Sara memorized the complete Surah Al-Fatiha. Her mother was very happy and said: May Allah bless you, my daughter! You are smart and hardworking.",
     "level": 2, "emoji": "📖",
     "question_ar": "كيف كانت أم سارة؟", "question_en": "How was Sara's mother?",
     "answer_ar": "فرحت كثيرًا", "answer_en": "Very happy",
     "options_ar": ["فرحت كثيرًا", "غضبت", "نامت"]},
    {"ar": "في العيدِ، لَبِسَ الأطفالُ ملابسَ جديدةً. ذَهَبوا لصلاةِ العيدِ مع آبائهم. ثمَّ زاروا الأقاربَ وأكلوا الحلوياتِ وفَرِحوا.",
     "en": "On Eid, the children wore new clothes. They went to Eid prayer with their fathers. Then they visited relatives, ate sweets and were happy.",
     "level": 2, "emoji": "🎉",
     "question_ar": "ماذا لبس الأطفال؟", "question_en": "What did the children wear?",
     "answer_ar": "ملابس جديدة", "answer_en": "New clothes",
     "options_ar": ["ملابس جديدة", "ملابس قديمة", "ملابس رياضية"]},
    {"ar": "كانَ النبيُّ محمدٌ ﷺ يُحِبُّ الأطفالَ ويَلعبُ معهم. كانَ يُسَلِّمُ عليهم ويَدعو لهم. عَلَّمَنا أنْ نكونَ لُطفاءَ مع الصِّغارِ.",
     "en": "Prophet Muhammad ﷺ loved children and played with them. He greeted them and made dua for them. He taught us to be kind with little ones.",
     "level": 2, "emoji": "🤲",
     "question_ar": "ماذا علمنا النبي ﷺ؟", "question_en": "What did the Prophet ﷺ teach us?",
     "answer_ar": "أن نكون لطفاء مع الصغار", "answer_en": "To be kind with little ones",
     "options_ar": ["أن نكون لطفاء مع الصغار", "أن نكون أقوياء", "أن نأكل كثيرًا"]},
    {"ar": "يُحِبُّ اللهُ الأطفالَ الذينَ يبِرّونَ والديهم. البِرُّ يعني أنْ تُطيعَ أمَّكَ وأباكَ، وأنْ تُساعِدَهُما، وأنْ تتكلَّمَ معهما بأدبٍ.",
     "en": "Allah loves children who are good to their parents. Being good means obeying your mother and father, helping them, and speaking to them politely.",
     "level": 2, "emoji": "❤️",
     "question_ar": "ماذا يعني البر؟", "question_en": "What does being good to parents mean?",
     "answer_ar": "طاعة الوالدين ومساعدتهما والتكلم بأدب", "answer_en": "Obeying, helping and speaking politely",
     "options_ar": ["طاعة الوالدين ومساعدتهما", "اللعب كثيرًا", "النوم مبكرًا"]},
    {"ar": "الماءُ نعمةٌ من نِعَمِ اللهِ. نشربُ الماءَ ونتوضأُ به ونسقي النباتاتِ. علَّمَنا الإسلامُ ألا نُسرِفَ في استخدامِ الماءِ.",
     "en": "Water is a blessing from Allah. We drink it, make wudu with it, and water plants. Islam taught us not to waste water.",
     "level": 2, "emoji": "💧",
     "question_ar": "ماذا علمنا الإسلام عن الماء؟", "question_en": "What did Islam teach us about water?",
     "answer_ar": "ألا نسرف في استخدامه", "answer_en": "Not to waste it",
     "options_ar": ["ألا نسرف في استخدامه", "أن نلعب به", "أن نخزنه"]},
    # Level 3: Longer paragraphs (Days 29-42)
    {"ar": "قصةُ النبيِّ إبراهيمَ عليهِ السلامُ مِن أجملِ القِصصِ. كانَ إبراهيمُ شُجاعًا جدًّا. حطَّمَ الأصنامَ التي كانَ يعبدُها قومُهُ وقالَ لهم: اعبُدوا اللهَ وَحدَهُ! غَضِبَ قومُهُ وألقَوهُ في النارِ، لكنَّ اللهَ حفظَهُ وجعلَ النارَ بردًا وسلامًا عليه.",
     "en": "The story of Prophet Ibrahim is one of the most beautiful stories. Ibrahim was very brave. He destroyed the idols his people worshipped and told them: Worship Allah alone! His people were angry and threw him in fire, but Allah protected him and made the fire cool and peaceful.",
     "level": 3, "emoji": "🕋",
     "question_ar": "كيف حمى الله إبراهيم؟", "question_en": "How did Allah protect Ibrahim?",
     "answer_ar": "جعل النار بردًا وسلامًا", "answer_en": "Made the fire cool and peaceful",
     "options_ar": ["جعل النار بردًا وسلامًا", "أطفأ النار", "أبعد النار"]},
    {"ar": "الصدقةُ مِن أحبِّ الأعمالِ إلى اللهِ. يمكنُكَ أنْ تتصدَّقَ بالمالِ أو بالطعامِ أو حتى بالابتسامةِ. قالَ النبيُّ ﷺ: تَبَسُّمُكَ في وجهِ أخيكَ صدقةٌ. فكلُّ عملٍ طيبٍ هو صدقةٌ!",
     "en": "Charity is one of Allah's most beloved deeds. You can give charity with money, food, or even a smile. The Prophet ﷺ said: Your smile to your brother is charity. Every good deed is charity!",
     "level": 3, "emoji": "💝",
     "question_ar": "ماذا قال النبي ﷺ عن الابتسامة؟", "question_en": "What did the Prophet ﷺ say about smiling?",
     "answer_ar": "تبسمك في وجه أخيك صدقة", "answer_en": "Your smile to your brother is charity",
     "options_ar": ["تبسمك في وجه أخيك صدقة", "الابتسامة جميلة", "الابتسامة مهمة"]},
    {"ar": "يجبُ على المسلمِ أنْ يكونَ صادقًا دائمًا. الصدقُ يهدي إلى البِرِّ والبِرُّ يهدي إلى الجنةِ. أمّا الكذبُ فهو مِن صفاتِ المنافقينَ. حتى لو كانَ الصِّدقُ صعبًا أحيانًا، يجبُ أنْ نقولَ الحقيقةَ دائمًا.",
     "en": "A Muslim must always be truthful. Truthfulness leads to righteousness and righteousness leads to Paradise. Lying is a trait of hypocrites. Even when truth is hard sometimes, we must always tell the truth.",
     "level": 3, "emoji": "⭐",
     "question_ar": "إلى أين يهدي الصدق؟", "question_en": "Where does truthfulness lead?",
     "answer_ar": "إلى البر ثم الجنة", "answer_en": "To righteousness then Paradise",
     "options_ar": ["إلى البر ثم الجنة", "إلى المدرسة", "إلى المسجد"]},
    {"ar": "عندما نسمعُ الأذانَ، نتوقفُ عمّا نفعلُهُ ونُردِّدُ مع المؤذِّنِ. ثمَّ نتوضأُ ونذهبُ للصلاةِ. الصلاةُ هي الصِّلةُ بيننا وبينَ اللهِ. نقفُ بينَ يديِ اللهِ خمسَ مراتٍ في اليومِ.",
     "en": "When we hear the adhan, we stop what we're doing and repeat after the muezzin. Then we make wudu and go to pray. Prayer is the connection between us and Allah. We stand before Allah five times a day.",
     "level": 3, "emoji": "🕌",
     "question_ar": "كم مرة نصلي في اليوم؟", "question_en": "How many times do we pray daily?",
     "answer_ar": "خمس مرات", "answer_en": "Five times",
     "options_ar": ["خمس مرات", "ثلاث مرات", "مرتين"]},
]

# ═══════════════════════════════════════════════════════════════
# STAGE 7: ISLAMIC FOUNDATIONS (Days 309-378, 70 days)
# Detailed Islamic knowledge lessons
# ═══════════════════════════════════════════════════════════════

ISLAMIC_FOUNDATIONS_DETAILED = [
    # Shahada - Multiple days
    {"id": "shahada_1", "emoji": "☪️", "topic": "shahada",
     "title": {"ar": "الشهادتان - الركن الأول", "en": "The Two Testimonies - First Pillar"},
     "content": {"ar": "أشهد أن لا إله إلا الله وأشهد أن محمدًا رسول الله. هذا هو الركن الأول من أركان الإسلام. معناها أننا نؤمن بأن الله واحد لا شريك له، وأن محمدًا ﷺ رسوله الكريم.",
                 "en": "I bear witness that there is no god but Allah and Muhammad is His messenger. This is the first pillar of Islam. It means we believe Allah is One with no partners, and Muhammad ﷺ is His noble messenger."},
     "memorize": {"ar": "أشهد أن لا إله إلا الله وأشهد أن محمدًا رسول الله", "en": "I bear witness that there is no god but Allah and Muhammad is His messenger"},
     "quiz_q": {"ar": "ما هو الركن الأول من أركان الإسلام؟", "en": "What is the first pillar of Islam?"},
     "quiz_a": {"ar": "الشهادتان", "en": "The Two Testimonies"},
     "quiz_opts": {"ar": ["الشهادتان", "الصلاة", "الزكاة"], "en": ["The Two Testimonies", "Prayer", "Zakat"]}},
    
    # Salah details
    {"id": "salah_1", "emoji": "🕌", "topic": "salah",
     "title": {"ar": "الصلاة - الركن الثاني", "en": "Prayer - Second Pillar"},
     "content": {"ar": "الصلاة هي الركن الثاني من أركان الإسلام. نصلي خمس صلوات في اليوم: الفجر (ركعتان)، الظهر (4 ركعات)، العصر (4 ركعات)، المغرب (3 ركعات)، العشاء (4 ركعات).",
                 "en": "Prayer is the second pillar of Islam. We pray five daily prayers: Fajr (2 rak'ahs), Dhuhr (4), Asr (4), Maghrib (3), Isha (4)."},
     "memorize": {"ar": "الصلوات الخمس: الفجر، الظهر، العصر، المغرب، العشاء", "en": "Five prayers: Fajr, Dhuhr, Asr, Maghrib, Isha"},
     "quiz_q": {"ar": "كم ركعة في صلاة المغرب؟", "en": "How many rak'ahs in Maghrib?"},
     "quiz_a": {"ar": "3 ركعات", "en": "3 rak'ahs"},
     "quiz_opts": {"ar": ["3 ركعات", "4 ركعات", "2 ركعتان"], "en": ["3 rak'ahs", "4 rak'ahs", "2 rak'ahs"]}},
    
    {"id": "salah_2", "emoji": "🧎", "topic": "salah",
     "title": {"ar": "أوقات الصلاة", "en": "Prayer Times"},
     "content": {"ar": "لكل صلاة وقت محدد: الفجر عند طلوع الفجر، الظهر عند زوال الشمس، العصر عند منتصف العصر، المغرب عند غروب الشمس، العشاء بعد غياب الشفق الأحمر.",
                 "en": "Each prayer has a specific time: Fajr at dawn, Dhuhr at noon, Asr in the afternoon, Maghrib at sunset, Isha after the red twilight disappears."},
     "memorize": {"ar": "الفجر: طلوع الفجر | الظهر: زوال الشمس | العصر: العصر | المغرب: غروب الشمس | العشاء: بعد الشفق", "en": "Fajr: dawn | Dhuhr: noon | Asr: afternoon | Maghrib: sunset | Isha: after twilight"},
     "quiz_q": {"ar": "متى وقت صلاة المغرب؟", "en": "When is Maghrib prayer time?"},
     "quiz_a": {"ar": "عند غروب الشمس", "en": "At sunset"},
     "quiz_opts": {"ar": ["عند غروب الشمس", "عند طلوع الشمس", "عند منتصف الليل"], "en": ["At sunset", "At sunrise", "At midnight"]}},
    
    # Zakat
    {"id": "zakat_1", "emoji": "💰", "topic": "zakat",
     "title": {"ar": "الزكاة - الركن الثالث", "en": "Zakat - Third Pillar"},
     "content": {"ar": "الزكاة هي إعطاء جزء من المال للفقراء والمحتاجين. هي حق الفقير في مال الغني. الزكاة تُطهِّر المال وتزيد البركة. قال الله تعالى: وأقيموا الصلاة وآتوا الزكاة.",
                 "en": "Zakat is giving a portion of wealth to the poor and needy. It is the right of the poor in the wealth of the rich. Zakat purifies wealth and increases blessings. Allah says: Establish prayer and give Zakat."},
     "memorize": {"ar": "الزكاة تطهر المال وتزيد البركة", "en": "Zakat purifies wealth and increases blessings"},
     "quiz_q": {"ar": "لمن نعطي الزكاة؟", "en": "To whom do we give Zakat?"},
     "quiz_a": {"ar": "للفقراء والمحتاجين", "en": "To the poor and needy"},
     "quiz_opts": {"ar": ["للفقراء والمحتاجين", "للأغنياء", "لأنفسنا"], "en": ["To the poor and needy", "To the rich", "To ourselves"]}},
    
    # Sawm (Fasting)
    {"id": "sawm_1", "emoji": "🌙", "topic": "sawm",
     "title": {"ar": "الصوم - الركن الرابع", "en": "Fasting - Fourth Pillar"},
     "content": {"ar": "الصوم هو الامتناع عن الطعام والشراب من الفجر إلى المغرب في شهر رمضان. الصوم يعلمنا الصبر والتقوى والإحساس بالفقراء. الأطفال يتدربون على الصيام تدريجيًا.",
                 "en": "Fasting means abstaining from food and drink from dawn to sunset in Ramadan. Fasting teaches us patience, God-consciousness and empathy for the poor. Children practice fasting gradually."},
     "memorize": {"ar": "الصوم من الفجر إلى المغرب في رمضان", "en": "Fasting from dawn to sunset in Ramadan"},
     "quiz_q": {"ar": "ماذا يعلمنا الصوم؟", "en": "What does fasting teach us?"},
     "quiz_a": {"ar": "الصبر والتقوى", "en": "Patience and God-consciousness"},
     "quiz_opts": {"ar": ["الصبر والتقوى", "الكسل", "الجوع فقط"], "en": ["Patience and piety", "Laziness", "Just hunger"]}},
    
    # Hajj
    {"id": "hajj_1", "emoji": "🕋", "topic": "hajj",
     "title": {"ar": "الحج - الركن الخامس", "en": "Hajj - Fifth Pillar"},
     "content": {"ar": "الحج هو زيارة مكة المكرمة لأداء مناسك معينة. يكون في شهر ذي الحجة. يطوف الحجاج حول الكعبة سبع مرات ويسعون بين الصفا والمروة. الحج واجب مرة واحدة في العمر لمن يستطيع.",
                 "en": "Hajj is visiting Makkah to perform specific rituals. It takes place in Dhul-Hijjah month. Pilgrims circle the Kaaba seven times and walk between Safa and Marwa. Hajj is obligatory once in a lifetime for those who can."},
     "memorize": {"ar": "الطواف حول الكعبة سبع مرات والسعي بين الصفا والمروة", "en": "Circle the Kaaba 7 times and walk between Safa and Marwa"},
     "quiz_q": {"ar": "كم مرة نطوف حول الكعبة؟", "en": "How many times do we circle the Kaaba?"},
     "quiz_a": {"ar": "سبع مرات", "en": "Seven times"},
     "quiz_opts": {"ar": ["سبع مرات", "خمس مرات", "ثلاث مرات"], "en": ["Seven times", "Five times", "Three times"]}},
    
    # Wudu details
    {"id": "wudu_detail", "emoji": "💧", "topic": "wudu",
     "title": {"ar": "الوضوء خطوة بخطوة", "en": "Wudu Step by Step"},
     "content": {"ar": "خطوات الوضوء: ١- النية وقول بسم الله ٢- غسل الكفين ثلاثًا ٣- المضمضة والاستنشاق ثلاثًا ٤- غسل الوجه ثلاثًا ٥- غسل اليدين إلى المرفقين ثلاثًا ٦- مسح الرأس ٧- غسل القدمين ثلاثًا",
                 "en": "Wudu steps: 1- Intention and say Bismillah 2- Wash hands 3 times 3- Rinse mouth and nose 3 times 4- Wash face 3 times 5- Wash arms to elbows 3 times 6- Wipe head 7- Wash feet 3 times"},
     "memorize": {"ar": "بسم الله - الكفان - المضمضة - الوجه - اليدان - الرأس - القدمان", "en": "Bismillah - Hands - Mouth - Face - Arms - Head - Feet"},
     "quiz_q": {"ar": "كم مرة نغسل الوجه في الوضوء؟", "en": "How many times do we wash the face in wudu?"},
     "quiz_a": {"ar": "ثلاث مرات", "en": "Three times"},
     "quiz_opts": {"ar": ["ثلاث مرات", "مرة واحدة", "خمس مرات"], "en": ["Three times", "Once", "Five times"]}},
    
    # Iman articles
    {"id": "iman_1", "emoji": "💎", "topic": "iman",
     "title": {"ar": "أركان الإيمان الستة", "en": "Six Pillars of Faith"},
     "content": {"ar": "أركان الإيمان الستة هي: ١- الإيمان بالله ٢- الإيمان بالملائكة ٣- الإيمان بالكتب السماوية ٤- الإيمان بالرسل ٥- الإيمان باليوم الآخر ٦- الإيمان بالقدر خيره وشره",
                 "en": "The Six Pillars of Faith: 1- Belief in Allah 2- Belief in Angels 3- Belief in Holy Books 4- Belief in Messengers 5- Belief in the Last Day 6- Belief in Divine Decree"},
     "memorize": {"ar": "الله - الملائكة - الكتب - الرسل - اليوم الآخر - القدر", "en": "Allah - Angels - Books - Messengers - Last Day - Decree"},
     "quiz_q": {"ar": "كم عدد أركان الإيمان؟", "en": "How many pillars of faith are there?"},
     "quiz_a": {"ar": "ستة", "en": "Six"},
     "quiz_opts": {"ar": ["ستة", "خمسة", "سبعة"], "en": ["Six", "Five", "Seven"]}},
    
    {"id": "iman_angels", "emoji": "👼", "topic": "iman",
     "title": {"ar": "الملائكة", "en": "The Angels"},
     "content": {"ar": "الملائكة مخلوقات من نور، لا يعصون الله أبدًا. جبريل ينزل الوحي، ميكائيل مسؤول عن المطر والنبات، إسرافيل ينفخ في الصور، وملك الموت يقبض الأرواح. والملائكة الحفظة يكتبون أعمالنا.",
                 "en": "Angels are creatures of light who never disobey Allah. Jibreel delivers revelation, Mikael manages rain and plants, Israfeel will blow the horn, and the Angel of Death takes souls. Guardian angels record our deeds."},
     "memorize": {"ar": "جبريل: الوحي | ميكائيل: المطر | إسرافيل: الصور | ملك الموت: الأرواح", "en": "Jibreel: revelation | Mikael: rain | Israfeel: the horn | Angel of Death: souls"},
     "quiz_q": {"ar": "من الملك المسؤول عن الوحي؟", "en": "Which angel delivers revelation?"},
     "quiz_a": {"ar": "جبريل", "en": "Jibreel"},
     "quiz_opts": {"ar": ["جبريل", "ميكائيل", "إسرافيل"], "en": ["Jibreel", "Mikael", "Israfeel"]}},
    
    {"id": "iman_books", "emoji": "📚", "topic": "iman",
     "title": {"ar": "الكتب السماوية", "en": "The Holy Books"},
     "content": {"ar": "أنزل الله كتبًا سماوية على أنبيائه: التوراة على موسى، الزبور على داود، الإنجيل على عيسى، والقرآن الكريم على محمد ﷺ. القرآن هو آخر الكتب وهو محفوظ إلى يوم القيامة.",
                 "en": "Allah revealed holy books to His prophets: The Torah to Musa, Zabur to Dawud, Injeel to Isa, and the Quran to Muhammad ﷺ. The Quran is the final book, preserved until the Day of Judgment."},
     "memorize": {"ar": "التوراة (موسى) - الزبور (داود) - الإنجيل (عيسى) - القرآن (محمد ﷺ)", "en": "Torah (Musa) - Zabur (Dawud) - Injeel (Isa) - Quran (Muhammad ﷺ)"},
     "quiz_q": {"ar": "على من أنزل الزبور؟", "en": "To whom was the Zabur revealed?"},
     "quiz_a": {"ar": "داود عليه السلام", "en": "Prophet Dawud"},
     "quiz_opts": {"ar": ["داود", "موسى", "عيسى"], "en": ["Dawud", "Musa", "Isa"]}},
    
    # Mosque etiquette
    {"id": "mosque_1", "emoji": "🕌", "topic": "mosque",
     "title": {"ar": "آداب المسجد", "en": "Mosque Etiquette"},
     "content": {"ar": "عند دخول المسجد: ندخل بالقدم اليمنى ونقول دعاء الدخول. نصلي تحية المسجد ركعتين. لا نرفع صوتنا. لا نأكل في المسجد. نحافظ على نظافته. نخرج بالقدم اليسرى.",
                 "en": "When entering the mosque: Enter with the right foot and say the entrance dua. Pray two rak'ahs of greeting. Don't raise our voice. Don't eat in the mosque. Keep it clean. Exit with the left foot."},
     "memorize": {"ar": "الدخول باليمنى والدعاء - تحية المسجد - الهدوء - النظافة - الخروج باليسرى", "en": "Enter right foot with dua - greet mosque - quiet - clean - exit left foot"},
     "quiz_q": {"ar": "بأي قدم ندخل المسجد؟", "en": "Which foot do we enter the mosque with?"},
     "quiz_a": {"ar": "القدم اليمنى", "en": "The right foot"},
     "quiz_opts": {"ar": ["القدم اليمنى", "القدم اليسرى", "لا فرق"], "en": ["Right foot", "Left foot", "Doesn't matter"]}},
    
    # Islamic Greetings
    {"id": "greetings_1", "emoji": "👋", "topic": "greetings",
     "title": {"ar": "التحية في الإسلام", "en": "Islamic Greetings"},
     "content": {"ar": "السلام عليكم ورحمة الله وبركاته هي أفضل تحية. عندما يسلم عليك أحد، تقول: وعليكم السلام ورحمة الله وبركاته. تحية الإسلام تنشر المحبة والسلام بين الناس.",
                 "en": "Assalamu Alaikum wa Rahmatullahi wa Barakatuh is the best greeting. When someone greets you, respond: Wa Alaikum Assalam wa Rahmatullahi wa Barakatuh. The Islamic greeting spreads love and peace among people."},
     "memorize": {"ar": "السلام عليكم ورحمة الله وبركاته", "en": "Assalamu Alaikum wa Rahmatullahi wa Barakatuh"},
     "quiz_q": {"ar": "ما أفضل تحية في الإسلام؟", "en": "What is the best greeting in Islam?"},
     "quiz_a": {"ar": "السلام عليكم ورحمة الله وبركاته", "en": "Assalamu Alaikum"},
     "quiz_opts": {"ar": ["السلام عليكم", "صباح الخير", "مرحبًا"], "en": ["Assalamu Alaikum", "Good morning", "Hello"]}},
    
    # Quran intro
    {"id": "quran_1", "emoji": "📖", "topic": "quran",
     "title": {"ar": "القرآن الكريم", "en": "The Holy Quran"},
     "content": {"ar": "القرآن الكريم هو كلام الله المنزل على نبينا محمد ﷺ بواسطة جبريل. فيه 114 سورة و30 جزءًا. أول سورة الفاتحة وآخر سورة الناس. القرآن فيه هداية وشفاء وراحة للقلوب.",
                 "en": "The Holy Quran is Allah's word revealed to Prophet Muhammad ﷺ through Jibreel. It has 114 surahs and 30 juz. First surah is Al-Fatiha and last is An-Nas. The Quran contains guidance, healing and comfort for hearts."},
     "memorize": {"ar": "القرآن: 114 سورة، 30 جزء، أوله الفاتحة وآخره الناس", "en": "Quran: 114 surahs, 30 juz, starts with Al-Fatiha ends with An-Nas"},
     "quiz_q": {"ar": "كم سورة في القرآن الكريم؟", "en": "How many surahs in the Quran?"},
     "quiz_a": {"ar": "114 سورة", "en": "114 surahs"},
     "quiz_opts": {"ar": ["114", "100", "120"], "en": ["114", "100", "120"]}},
    
    # Islamic months
    {"id": "months_1", "emoji": "📅", "topic": "months",
     "title": {"ar": "الأشهر الهجرية", "en": "Islamic Months"},
     "content": {"ar": "الأشهر الهجرية اثنا عشر شهرًا: محرّم، صفر، ربيع الأول، ربيع الثاني، جمادى الأولى، جمادى الآخرة، رجب، شعبان، رمضان، شوال، ذو القعدة، ذو الحجة. رمضان شهر الصيام وذو الحجة شهر الحج.",
                 "en": "Islamic months are twelve: Muharram, Safar, Rabi al-Awwal, Rabi ath-Thani, Jumada al-Ula, Jumada al-Akhirah, Rajab, Sha'ban, Ramadan, Shawwal, Dhul-Qi'dah, Dhul-Hijjah. Ramadan is for fasting and Dhul-Hijjah for Hajj."},
     "memorize": {"ar": "محرم - صفر - ربيع أول - ربيع ثاني - جمادى أولى - جمادى آخرة - رجب - شعبان - رمضان - شوال - ذو القعدة - ذو الحجة", "en": "Muharram - Safar - Rabi I - Rabi II - Jumada I - Jumada II - Rajab - Sha'ban - Ramadan - Shawwal - Dhul-Qi'dah - Dhul-Hijjah"},
     "quiz_q": {"ar": "ما هو شهر الصيام؟", "en": "Which is the month of fasting?"},
     "quiz_a": {"ar": "رمضان", "en": "Ramadan"},
     "quiz_opts": {"ar": ["رمضان", "شعبان", "محرم"], "en": ["Ramadan", "Sha'ban", "Muharram"]}},
    
    # Good Manners
    {"id": "akhlaq_1", "emoji": "😊", "topic": "akhlaq",
     "title": {"ar": "الأخلاق الحسنة", "en": "Good Manners"},
     "content": {"ar": "الإسلام يحثنا على الأخلاق الحسنة: الصدق، الأمانة، الإحسان إلى الجار، إكرام الضيف، احترام الكبير، العطف على الصغير، التعاون، والتسامح. قال النبي ﷺ: إنما بُعثت لأتمم مكارم الأخلاق.",
                 "en": "Islam encourages good manners: truthfulness, trustworthiness, kindness to neighbors, honoring guests, respecting elders, being gentle with children, cooperation, and forgiveness. The Prophet ﷺ said: I was sent to perfect good character."},
     "memorize": {"ar": "إنما بُعثت لأتمم مكارم الأخلاق - حديث نبوي", "en": "I was sent to perfect good character - Prophetic hadith"},
     "quiz_q": {"ar": "لماذا بُعث النبي ﷺ؟", "en": "Why was the Prophet ﷺ sent?"},
     "quiz_a": {"ar": "لإتمام مكارم الأخلاق", "en": "To perfect good character"},
     "quiz_opts": {"ar": ["لإتمام مكارم الأخلاق", "للحرب", "للسفر"], "en": ["To perfect good character", "For war", "For travel"]}},
    
    # Respecting Parents
    {"id": "birr_1", "emoji": "❤️", "topic": "parents",
     "title": {"ar": "بر الوالدين", "en": "Honoring Parents"},
     "content": {"ar": "بر الوالدين من أعظم العبادات. قال الله تعالى: وقضى ربك ألا تعبدوا إلا إياه وبالوالدين إحسانًا. نطيع والدينا، نساعدهما، لا نرفع صوتنا عليهما، وندعو لهما: رب ارحمهما كما ربياني صغيرًا.",
                 "en": "Honoring parents is one of the greatest acts of worship. Allah said: Your Lord has decreed that you worship none but Him, and be good to parents. We obey our parents, help them, don't raise our voice, and pray for them."},
     "memorize": {"ar": "رَبِّ ارْحَمْهُمَا كَمَا رَبَّيَانِي صَغِيرًا", "en": "My Lord, have mercy upon them as they brought me up when I was small"},
     "quiz_q": {"ar": "ما هو دعاء الوالدين؟", "en": "What is the dua for parents?"},
     "quiz_a": {"ar": "رب ارحمهما كما ربياني صغيرا", "en": "My Lord, have mercy upon them"},
     "quiz_opts": {"ar": ["رب ارحمهما كما ربياني صغيرا", "رب اغفر لي", "ربنا آتنا في الدنيا حسنة"], "en": ["My Lord have mercy upon them", "Lord forgive me", "Lord give us good"]}},
    
    # Kindness to animals
    {"id": "animals_1", "emoji": "🐱", "topic": "animals",
     "title": {"ar": "الرفق بالحيوان", "en": "Kindness to Animals"},
     "content": {"ar": "الإسلام يأمرنا بالرفق بالحيوانات. قال النبي ﷺ إن امرأة دخلت النار بسبب قطة حبستها ولم تطعمها. وامرأة أخرى دخلت الجنة لأنها سقت كلبًا عطشان. الرفق بالحيوان عبادة!",
                 "en": "Islam commands us to be kind to animals. The Prophet ﷺ said a woman entered Hell for imprisoning a cat without feeding it. Another woman entered Paradise for giving water to a thirsty dog. Kindness to animals is worship!"},
     "memorize": {"ar": "في كل ذات كبد رطبة أجر - حديث نبوي", "en": "There is reward for every living creature - Prophetic hadith"},
     "quiz_q": {"ar": "لماذا دخلت المرأة الجنة؟", "en": "Why did the woman enter Paradise?"},
     "quiz_a": {"ar": "لأنها سقت كلبًا عطشان", "en": "She gave water to a thirsty dog"},
     "quiz_opts": {"ar": ["سقت كلبًا عطشان", "صلت كثيرًا", "صامت كثيرًا"], "en": ["Gave water to a dog", "Prayed a lot", "Fasted a lot"]}},
    
    # Truthfulness
    {"id": "sidq_1", "emoji": "⭐", "topic": "truthfulness",
     "title": {"ar": "الصدق في الإسلام", "en": "Truthfulness in Islam"},
     "content": {"ar": "الصدق من أهم الأخلاق في الإسلام. قال النبي ﷺ: عليكم بالصدق فإن الصدق يهدي إلى البر والبر يهدي إلى الجنة. وإياكم والكذب فإن الكذب يهدي إلى الفجور والفجور يهدي إلى النار.",
                 "en": "Truthfulness is one of the most important traits in Islam. The Prophet ﷺ said: Be truthful, for truthfulness leads to righteousness and righteousness leads to Paradise. Beware of lying, for lying leads to wickedness and wickedness leads to the Fire."},
     "memorize": {"ar": "عليكم بالصدق فإن الصدق يهدي إلى البر", "en": "Be truthful, truthfulness leads to righteousness"},
     "quiz_q": {"ar": "إلى أين يهدي الصدق؟", "en": "Where does truthfulness lead?"},
     "quiz_a": {"ar": "إلى البر والجنة", "en": "To righteousness and Paradise"},
     "quiz_opts": {"ar": ["البر والجنة", "المال", "الشهرة"], "en": ["Righteousness and Paradise", "Wealth", "Fame"]}},
    
    # Cleanliness
    {"id": "tahara_1", "emoji": "🧼", "topic": "cleanliness",
     "title": {"ar": "النظافة في الإسلام", "en": "Cleanliness in Islam"},
     "content": {"ar": "النظافة من الإيمان. قال النبي ﷺ: الطهور شطر الإيمان. نغسل أيدينا قبل الأكل وبعده، ننظف أسناننا بالسواك، نقص أظافرنا، ونلبس ملابس نظيفة. الإسلام دين النظافة.",
                 "en": "Cleanliness is part of faith. The Prophet ﷺ said: Cleanliness is half of faith. We wash hands before and after eating, clean teeth with miswak, trim nails, and wear clean clothes. Islam is the religion of cleanliness."},
     "memorize": {"ar": "الطُّهورُ شَطرُ الإيمانِ - حديث نبوي", "en": "Cleanliness is half of faith - Prophetic hadith"},
     "quiz_q": {"ar": "ماذا قال النبي ﷺ عن الطهور؟", "en": "What did the Prophet ﷺ say about cleanliness?"},
     "quiz_a": {"ar": "شطر الإيمان", "en": "Half of faith"},
     "quiz_opts": {"ar": ["شطر الإيمان", "ربع الإيمان", "كل الإيمان"], "en": ["Half of faith", "Quarter of faith", "All of faith"]}},
    
    # Dhikr
    {"id": "dhikr_1", "emoji": "📿", "topic": "dhikr",
     "title": {"ar": "ذكر الله", "en": "Remembrance of Allah"},
     "content": {"ar": "ذكر الله يملأ القلب سكينة وطمأنينة. من أهم الأذكار: سبحان الله، الحمد لله، الله أكبر، لا إله إلا الله، أستغفر الله. قال الله: ألا بذكر الله تطمئن القلوب.",
                 "en": "Remembering Allah fills the heart with peace and tranquility. Important dhikr: SubhanAllah, Alhamdulillah, Allahu Akbar, La ilaha illallah, Astaghfirullah. Allah said: Surely in the remembrance of Allah hearts find peace."},
     "memorize": {"ar": "أَلَا بِذِكْرِ اللَّهِ تَطْمَئِنُّ الْقُلُوبُ", "en": "Surely in the remembrance of Allah hearts find peace"},
     "quiz_q": {"ar": "بماذا تطمئن القلوب؟", "en": "What gives hearts peace?"},
     "quiz_a": {"ar": "بذكر الله", "en": "Remembrance of Allah"},
     "quiz_opts": {"ar": ["ذكر الله", "المال", "اللعب"], "en": ["Remembrance of Allah", "Money", "Playing"]}},
    
    # Charity and helping others
    {"id": "sadaqah_1", "emoji": "🤝", "topic": "sadaqah",
     "title": {"ar": "الصدقة والإحسان", "en": "Charity and Kindness"},
     "content": {"ar": "الصدقة ليست بالمال فقط. كل عمل خير صدقة: إماطة الأذى عن الطريق صدقة، الكلمة الطيبة صدقة، والابتسامة في وجه أخيك صدقة. حتى مساعدة الآخرين صدقة.",
                 "en": "Charity is not just money. Every good deed is charity: removing harm from the road is charity, a kind word is charity, smiling at your brother is charity. Even helping others is charity."},
     "memorize": {"ar": "الكلمة الطيبة صدقة - تبسمك في وجه أخيك صدقة", "en": "A kind word is charity - Smiling at your brother is charity"},
     "quiz_q": {"ar": "ما هي الصدقة؟", "en": "What is charity?"},
     "quiz_a": {"ar": "كل عمل خير", "en": "Every good deed"},
     "quiz_opts": {"ar": ["كل عمل خير", "المال فقط", "الطعام فقط"], "en": ["Every good deed", "Only money", "Only food"]}},
]

# ═══════════════════════════════════════════════════════════════
# STAGE 12: ISLAMIC LIFE - Expanded Topics (Days 721-810)
# ═══════════════════════════════════════════════════════════════

ISLAMIC_LIFE_TOPICS = [
    {"emoji": "🌙", "title": {"ar": "رمضان - شهر الخير", "en": "Ramadan - Month of Goodness"},
     "content": {"ar": "رمضان شهر مبارك نصوم فيه ونقرأ القرآن ونتقرب إلى الله. فيه ليلة القدر التي هي خير من ألف شهر. نفطر على التمر والماء ونصلي التراويح.",
                 "en": "Ramadan is a blessed month of fasting, Quran reading and getting closer to Allah. It contains Laylatul Qadr which is better than a thousand months. We break fast with dates and water and pray Taraweeh."}},
    {"emoji": "🕋", "title": {"ar": "الحج - رحلة العمر", "en": "Hajj - Journey of a Lifetime"},
     "content": {"ar": "ملايين المسلمين يذهبون إلى مكة كل عام لأداء الحج. يلبسون الإحرام الأبيض ويطوفون حول الكعبة ويقفون بعرفة ويرمون الجمرات.",
                 "en": "Millions of Muslims go to Makkah every year for Hajj. They wear white ihram, circle the Kaaba, stand at Arafat and throw pebbles at the Jamarat."}},
    {"emoji": "🎉", "title": {"ar": "عيد الفطر - فرحة المسلمين", "en": "Eid Al-Fitr - Muslim Celebration"},
     "content": {"ar": "عيد الفطر يأتي بعد رمضان. نغتسل ونلبس أحسن الثياب. نصلي صلاة العيد ونكبر. نزور الأقارب ونتبادل التهاني ونأكل الحلويات. ونخرج زكاة الفطر قبل الصلاة.",
                 "en": "Eid Al-Fitr comes after Ramadan. We bathe and wear best clothes. We pray Eid prayer and say takbeer. We visit relatives, exchange greetings and eat sweets. We pay Zakat al-Fitr before the prayer."}},
    {"emoji": "🐑", "title": {"ar": "عيد الأضحى", "en": "Eid Al-Adha"},
     "content": {"ar": "عيد الأضحى يوم عظيم نتذكر فيه قصة إبراهيم وإسماعيل عليهما السلام. نصلي صلاة العيد ونذبح الأضحية ونوزعها: ثلث لنا وثلث للأقارب وثلث للفقراء.",
                 "en": "Eid Al-Adha is a great day when we remember the story of Ibrahim and Ismail. We pray Eid prayer, sacrifice an animal and distribute: a third for us, a third for relatives and a third for the poor."}},
    {"emoji": "🕌", "title": {"ar": "يوم الجمعة", "en": "Friday"},
     "content": {"ar": "يوم الجمعة هو سيد الأيام وأفضلها. فيه خلق آدم وفيه ساعة إجابة. نغتسل ونتطيب ونلبس أحسن الثياب. نذهب مبكرًا للمسجد ونصلي صلاة الجمعة ونسمع الخطبة.",
                 "en": "Friday is the master and best of days. Adam was created on it and there is a special hour of acceptance. We bathe, wear perfume and best clothes. We go early to the mosque for Jumu'ah prayer and listen to the sermon."}},
    {"emoji": "🌟", "title": {"ar": "ليلة القدر", "en": "Laylatul Qadr"},
     "content": {"ar": "ليلة القدر خير من ألف شهر. هي الليلة التي نزل فيها القرآن. نبحث عنها في العشر الأواخر من رمضان. نقوم الليل وندعو: اللهم إنك عفو تحب العفو فاعف عني.",
                 "en": "Laylatul Qadr is better than a thousand months. It is the night the Quran was revealed. We look for it in the last ten nights of Ramadan. We pray at night and make dua: O Allah, You are forgiving and love forgiveness, so forgive me."}},
    {"emoji": "📅", "title": {"ar": "يوم عاشوراء", "en": "Day of Ashura"},
     "content": {"ar": "يوم عاشوراء هو العاشر من محرم. في هذا اليوم نجّى الله موسى وقومه من فرعون. صامه النبي ﷺ وأمرنا بصيامه. من صامه يُكفّر عنه ذنوب سنة ماضية.",
                 "en": "Ashura is the 10th of Muharram. On this day Allah saved Musa and his people from Pharaoh. The Prophet ﷺ fasted it and told us to fast it. Fasting it expiates sins of the previous year."}},
    {"emoji": "🕋", "title": {"ar": "الكعبة المشرفة", "en": "The Holy Kaaba"},
     "content": {"ar": "الكعبة هي أول بيت وُضع للناس. بناها إبراهيم وإسماعيل عليهما السلام. فيها الحجر الأسود. نتوجه إليها في صلاتنا. هي قبلة المسلمين في كل مكان في العالم.",
                 "en": "The Kaaba is the first house built for people. Ibrahim and Ismail built it. It contains the Black Stone. We face it in our prayer. It is the qibla of Muslims everywhere in the world."}},
    {"emoji": "🕌", "title": {"ar": "المسجد الحرام", "en": "Al-Masjid Al-Haram"},
     "content": {"ar": "المسجد الحرام في مكة المكرمة هو أعظم مسجد. فيه الكعبة وبئر زمزم ومقام إبراهيم. الصلاة فيه بمئة ألف صلاة. يأتيه الحجاج والمعتمرون من كل أنحاء العالم.",
                 "en": "Al-Masjid Al-Haram in Makkah is the greatest mosque. It contains the Kaaba, Well of Zamzam and Ibrahim's station. Prayer in it equals 100,000 prayers. Pilgrims come from all over the world."}},
    {"emoji": "🟢", "title": {"ar": "المسجد النبوي", "en": "Prophet's Mosque"},
     "content": {"ar": "المسجد النبوي في المدينة المنورة بناه النبي ﷺ. فيه قبر النبي ﷺ والروضة الشريفة. الصلاة فيه بألف صلاة. المدينة المنورة هي مدينة الرسول ﷺ.",
                 "en": "The Prophet's Mosque in Madinah was built by the Prophet ﷺ. It contains the Prophet's grave and the Rawdah. Prayer in it equals 1,000 prayers. Madinah is the city of the Messenger ﷺ."}},
    {"emoji": "🟡", "title": {"ar": "المسجد الأقصى", "en": "Al-Aqsa Mosque"},
     "content": {"ar": "المسجد الأقصى في القدس هو أولى القبلتين وثالث الحرمين. أسري بالنبي ﷺ إليه ليلة المعراج. الصلاة فيه بخمسمئة صلاة. فلسطين أرض مباركة.",
                 "en": "Al-Aqsa Mosque in Jerusalem was the first qibla and third holiest mosque. The Prophet ﷺ was taken there on the Night Journey. Prayer in it equals 500 prayers. Palestine is a blessed land."}},
    {"emoji": "✨", "title": {"ar": "الإسراء والمعراج", "en": "The Night Journey & Ascension"},
     "content": {"ar": "في ليلة مباركة، أسري بالنبي ﷺ من المسجد الحرام إلى المسجد الأقصى على البراق. ثم عرج إلى السماوات السبع حيث فرضت الصلوات الخمس. التقى بالأنبياء ورأى آيات الله العظيمة.",
                 "en": "On a blessed night, the Prophet ﷺ was taken from Al-Masjid Al-Haram to Al-Aqsa on the Buraq. Then he ascended through seven heavens where the five prayers were ordained. He met the prophets and saw Allah's great signs."}},
    {"emoji": "📆", "title": {"ar": "رأس السنة الهجرية", "en": "Islamic New Year"},
     "content": {"ar": "رأس السنة الهجرية في أول محرم. التقويم الهجري يبدأ من هجرة النبي ﷺ من مكة إلى المدينة. هذه الهجرة كانت حدثًا عظيمًا غيّر تاريخ الإسلام.",
                 "en": "Islamic New Year is on the 1st of Muharram. The Hijri calendar starts from the Prophet's migration from Makkah to Madinah. This migration was a great event that changed Islamic history."}},
    {"emoji": "🕊️", "title": {"ar": "السلام في الإسلام", "en": "Peace in Islam"},
     "content": {"ar": "الإسلام دين السلام. كلمة الإسلام من السلام. تحيتنا: السلام عليكم. الجنة دار السلام. الله هو السلام. نحن نحب السلام ونعيش مع الجميع بسلام واحترام.",
                 "en": "Islam is the religion of peace. The word Islam comes from peace. Our greeting: Peace be upon you. Paradise is the abode of peace. Allah is Peace. We love peace and live with everyone in peace and respect."}},
    {"emoji": "🌳", "title": {"ar": "البيئة في الإسلام", "en": "Environment in Islam"},
     "content": {"ar": "الإسلام يأمرنا بالمحافظة على البيئة. قال النبي ﷺ: إذا قامت الساعة وفي يد أحدكم فسيلة فليغرسها. نزرع الأشجار، لا نلوث الماء، ولا نفسد الأرض. نحن خلفاء الله في الأرض.",
                 "en": "Islam commands us to protect the environment. The Prophet ﷺ said: If the Hour comes while you have a seedling, plant it. We plant trees, don't pollute water, and don't corrupt the earth. We are Allah's stewards on Earth."}},
    {"emoji": "🎓", "title": {"ar": "طلب العلم في الإسلام", "en": "Seeking Knowledge in Islam"},
     "content": {"ar": "طلب العلم فريضة على كل مسلم ومسلمة. قال النبي ﷺ: اطلبوا العلم من المهد إلى اللحد. وأول آية نزلت من القرآن: اقرأ. العلم نور يضيء حياتنا.",
                 "en": "Seeking knowledge is obligatory for every Muslim. The Prophet ﷺ said: Seek knowledge from the cradle to the grave. The first revealed Quran verse was: Read. Knowledge is a light that brightens our lives."}},
    {"emoji": "🤝", "title": {"ar": "حقوق الجار", "en": "Rights of Neighbors"},
     "content": {"ar": "للجار حقوق كثيرة في الإسلام. قال النبي ﷺ: ما زال جبريل يوصيني بالجار حتى ظننت أنه سيورثه. نحسن إلى جيراننا، لا نؤذيهم، نطعمهم إذا جاعوا، ونزورهم إذا مرضوا.",
                 "en": "Neighbors have many rights in Islam. The Prophet ﷺ said: Jibreel kept advising me about neighbors until I thought he would make them heirs. We are good to neighbors, don't harm them, feed them if hungry, visit them if sick."}},
    {"emoji": "📿", "title": {"ar": "الاستغفار", "en": "Seeking Forgiveness"},
     "content": {"ar": "الاستغفار يمحو الذنوب ويجلب الرزق والراحة. كان النبي ﷺ يستغفر الله في اليوم أكثر من سبعين مرة. ندعو: أستغفر الله العظيم الذي لا إله إلا هو الحي القيوم وأتوب إليه.",
                 "en": "Seeking forgiveness erases sins and brings provision and peace. The Prophet ﷺ used to seek forgiveness more than 70 times a day. We say: Astaghfirullah al-Adheem - I seek forgiveness from Allah the Almighty."}},
    {"emoji": "💐", "title": {"ar": "المولد النبوي الشريف", "en": "The Prophet's Birthday"},
     "content": {"ar": "وُلد النبي محمد ﷺ في ربيع الأول في مكة المكرمة. كان يتيمًا رعاه جده عبد المطلب ثم عمه أبو طالب. نشأ أمينًا صادقًا حتى لقبه قومه بالصادق الأمين.",
                 "en": "Prophet Muhammad ﷺ was born in Rabi al-Awwal in Makkah. He was an orphan raised by his grandfather Abdul-Muttalib then his uncle Abu Talib. He grew up honest and truthful, earning the title Al-Amin (The Trustworthy)."}},
]

# ═══════════════════════════════════════════════════════════════
# STAGE 13: ADVANCED ARABIC - Grammar, Verbs, Conversations
# ═══════════════════════════════════════════════════════════════

ARABIC_GRAMMAR_LESSONS = [
    # Noun types
    {"id": "g01", "emoji": "📝", "title": {"ar": "الاسم المفرد والمثنى والجمع", "en": "Singular, Dual and Plural"},
     "content": {"ar": "المفرد: كتاب (واحد) | المثنى: كتابان (اثنان) | الجمع: كتب (أكثر من اثنين). تمارين: ولد→ ولدان→ أولاد | بنت→ بنتان→ بنات | معلم→ معلمان→ معلمون",
                 "en": "Singular: kitab (one) | Dual: kitaban (two) | Plural: kutub (more than two). Practice: walad→ waladan→ awlad | bint→ bintan→ banat | mu'allim→ mu'alliman→ mu'allimun"},
     "practice": [
         {"word": "مسجد", "dual": "مسجدان", "plural": "مساجد"},
         {"word": "سورة", "dual": "سورتان", "plural": "سور"},
         {"word": "نبي", "dual": "نبيّان", "plural": "أنبياء"},
     ]},
    # Verb tenses
    {"id": "g02", "emoji": "🔤", "title": {"ar": "الفعل الماضي والمضارع والأمر", "en": "Past, Present and Command"},
     "content": {"ar": "الماضي: كَتَبَ (فعل حدث وانتهى) | المضارع: يَكتُبُ (فعل يحدث الآن) | الأمر: اُكتُبْ (طلب فعل شيء). تمارين: قرأ→ يقرأ→ اقرأ | صلّى→ يصلي→ صَلِّ | ذهب→ يذهب→ اذهب",
                 "en": "Past: kataba (happened and finished) | Present: yaktub (happening now) | Command: uktub (request to do). Practice: qara'a→ yaqra'→ iqra' | salla→ yusalli→ salli | dhahaba→ yadhhab→ idhhab"},
     "practice": [
         {"past": "أكَلَ", "present": "يَأكُلُ", "command": "كُلْ", "en": "ate/eats/eat"},
         {"past": "شَرِبَ", "present": "يَشرَبُ", "command": "اِشرَبْ", "en": "drank/drinks/drink"},
         {"past": "نَامَ", "present": "يَنامُ", "command": "نَمْ", "en": "slept/sleeps/sleep"},
     ]},
    # Pronouns
    {"id": "g03", "emoji": "👤", "title": {"ar": "الضمائر", "en": "Pronouns"},
     "content": {"ar": "أنا (متكلم) | أنتَ/أنتِ (مخاطب) | هو/هي (غائب) | نحن (جمع المتكلمين) | أنتم (جمع المخاطبين) | هم (جمع الغائبين)",
                 "en": "Ana (I) | Anta/Anti (you m/f) | Huwa/Hiya (he/she) | Nahnu (we) | Antum (you pl) | Hum (they)"},
     "practice": [
         {"pronoun": "أنا", "example": "أنا مسلم", "en": "I am a Muslim"},
         {"pronoun": "هو", "example": "هو يصلي", "en": "He is praying"},
         {"pronoun": "نحن", "example": "نحن نحب القرآن", "en": "We love the Quran"},
     ]},
    # Question words
    {"id": "g04", "emoji": "❓", "title": {"ar": "أدوات الاستفهام", "en": "Question Words"},
     "content": {"ar": "مَن؟ (للسؤال عن الشخص) | ما/ماذا؟ (للسؤال عن الشيء) | أين؟ (للمكان) | متى؟ (للزمان) | كيف؟ (للحال) | لماذا؟ (للسبب) | كم؟ (للعدد)",
                 "en": "Man? (who) | Ma/Madha? (what) | Ayna? (where) | Mata? (when) | Kayf? (how) | Limadha? (why) | Kam? (how many)"},
     "practice": [
         {"question": "مَن النبي الأخير؟", "answer": "محمد ﷺ", "en": "Who is the last prophet?"},
         {"question": "أين الكعبة؟", "answer": "في مكة المكرمة", "en": "Where is the Kaaba?"},
         {"question": "كم صلاة في اليوم؟", "answer": "خمس صلوات", "en": "How many prayers per day?"},
     ]},
    # Prepositions
    {"id": "g05", "emoji": "📍", "title": {"ar": "حروف الجر", "en": "Prepositions"},
     "content": {"ar": "في (inside) | على (on) | من (from) | إلى (to) | عن (about) | ب (with/by) | ل (for). مثال: ذهبتُ إلى المسجدِ - صليتُ في المسجدِ - رجعتُ من المسجدِ",
                 "en": "Fi (in) | Ala (on) | Min (from) | Ila (to) | An (about) | Bi (with) | Li (for). Example: I went to the mosque - I prayed in the mosque - I returned from the mosque"},
     "practice": [
         {"sentence": "الكتابُ على الطاولةِ", "en": "The book is on the table"},
         {"sentence": "ذهبنا إلى المدرسةِ", "en": "We went to school"},
         {"sentence": "خرجنا من البيتِ", "en": "We left from the house"},
     ]},
    # Conversations
    {"id": "g06", "emoji": "💬", "title": {"ar": "محادثة: في المسجد", "en": "Conversation: At the Mosque"},
     "content": {"ar": "أحمد: السلام عليكم يا عم!\nالعم: وعليكم السلام يا بُني! كيف حالك؟\nأحمد: الحمد لله بخير. هل صلاة المغرب قريبة؟\nالعم: نعم، بعد خمس دقائق إن شاء الله.\nأحمد: جزاك الله خيرًا.",
                 "en": "Ahmad: Assalamu alaikum uncle!\nUncle: Wa alaikum assalam son! How are you?\nAhmad: Alhamdulillah fine. Is Maghrib prayer soon?\nUncle: Yes, in five minutes inshaAllah.\nAhmad: JazakAllah khairan."},
     "practice": []},
    {"id": "g07", "emoji": "💬", "title": {"ar": "محادثة: في المدرسة", "en": "Conversation: At School"},
     "content": {"ar": "المعلم: صباح الخير يا طلاب!\nالطلاب: صباح النور يا أستاذ!\nالمعلم: اليوم نتعلم سورة جديدة. افتحوا المصحف.\nسارة: أي سورة يا أستاذ؟\nالمعلم: سورة الفلق. هيا نقرأ معًا.",
                 "en": "Teacher: Good morning students!\nStudents: Good morning teacher!\nTeacher: Today we learn a new surah. Open the Quran.\nSara: Which surah, teacher?\nTeacher: Surah Al-Falaq. Let's read together."},
     "practice": []},
    {"id": "g08", "emoji": "💬", "title": {"ar": "محادثة: في رمضان", "en": "Conversation: In Ramadan"},
     "content": {"ar": "الأم: هل أنت صائم اليوم يا أحمد؟\nأحمد: نعم يا أمي! أنا صائم والحمد لله.\nالأم: ما شاء الله! ماذا تريد للإفطار؟\nأحمد: تمرًا وحليبًا من فضلك.\nالأم: حاضر. بارك الله فيك يا بُني.",
                 "en": "Mom: Are you fasting today Ahmad?\nAhmad: Yes mom! I'm fasting alhamdulillah.\nMom: MashaAllah! What do you want for iftar?\nAhmad: Dates and milk please.\nMom: Of course. May Allah bless you son."},
     "practice": []},
    # Adjectives
    {"id": "g09", "emoji": "🎨", "title": {"ar": "الصفات", "en": "Adjectives"},
     "content": {"ar": "كبير↔صغير | طويل↔قصير | جميل↔قبيح | سريع↔بطيء | قوي↔ضعيف | حار↔بارد | جديد↔قديم | سعيد↔حزين. الصفة تتبع الموصوف: المسجد الكبير، البنت الجميلة.",
                 "en": "Big↔Small | Tall↔Short | Beautiful↔Ugly | Fast↔Slow | Strong↔Weak | Hot↔Cold | New↔Old | Happy↔Sad. Adjective follows the noun: the big mosque, the beautiful girl."},
     "practice": [
         {"word": "كبير", "opposite": "صغير", "example": "المسجد كبير"},
         {"word": "جميل", "opposite": "قبيح", "example": "القرآن جميل"},
         {"word": "سعيد", "opposite": "حزين", "example": "أنا سعيد"},
     ]},
    # Days of the week
    {"id": "g10", "emoji": "📅", "title": {"ar": "أيام الأسبوع", "en": "Days of the Week"},
     "content": {"ar": "السبت، الأحد، الاثنين، الثلاثاء، الأربعاء، الخميس، الجمعة. يوم الجمعة هو أفضل الأيام عند المسلمين. نصلي فيه صلاة الجمعة.",
                 "en": "Saturday, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday. Friday is the best day for Muslims. We pray Jumu'ah prayer on it."},
     "practice": [
         {"day": "السبت", "en": "Saturday"},
         {"day": "الأحد", "en": "Sunday"},
         {"day": "الجمعة", "en": "Friday"},
     ]},
]

# ═══════════════════════════════════════════════════════════════
# ADDITIONAL QURAN SURAHS FOR KIDS (Expanding the collection)
# ═══════════════════════════════════════════════════════════════

ADDITIONAL_SURAHS = [
    {
        "id": "fil", "number": 105, "name_ar": "الفيل", "name_en": "Al-Fil",
        "difficulty": 1, "total_ayahs": 5,
        "ayahs": [
            {"num": 1, "ar": "أَلَمْ تَرَ كَيْفَ فَعَلَ رَبُّكَ بِأَصْحَابِ الْفِيلِ", "en": "Have you not seen how your Lord dealt with the companions of the elephant?"},
            {"num": 2, "ar": "أَلَمْ يَجْعَلْ كَيْدَهُمْ فِي تَضْلِيلٍ", "en": "Did He not make their plan into misguidance?"},
            {"num": 3, "ar": "وَأَرْسَلَ عَلَيْهِمْ طَيْرًا أَبَابِيلَ", "en": "And He sent against them birds in flocks"},
            {"num": 4, "ar": "تَرْمِيهِمْ بِحِجَارَةٍ مِنْ سِجِّيلٍ", "en": "Striking them with stones of hard clay"},
            {"num": 5, "ar": "فَجَعَلَهُمْ كَعَصْفٍ مَأْكُولٍ", "en": "And He made them like eaten straw"},
        ],
    },
    {
        "id": "quraysh", "number": 106, "name_ar": "قريش", "name_en": "Quraysh",
        "difficulty": 1, "total_ayahs": 4,
        "ayahs": [
            {"num": 1, "ar": "لِإِيلَافِ قُرَيْشٍ", "en": "For the accustomed security of the Quraysh"},
            {"num": 2, "ar": "إِيلَافِهِمْ رِحْلَةَ الشِّتَاءِ وَالصَّيْفِ", "en": "Their accustomed security of the winter and summer journeys"},
            {"num": 3, "ar": "فَلْيَعْبُدُوا رَبَّ هَذَا الْبَيْتِ", "en": "Let them worship the Lord of this House"},
            {"num": 4, "ar": "الَّذِي أَطْعَمَهُمْ مِنْ جُوعٍ وَآمَنَهُمْ مِنْ خَوْفٍ", "en": "Who has fed them against hunger and made them safe from fear"},
        ],
    },
    {
        "id": "maun", "number": 107, "name_ar": "الماعون", "name_en": "Al-Ma'un",
        "difficulty": 2, "total_ayahs": 7,
        "ayahs": [
            {"num": 1, "ar": "أَرَأَيْتَ الَّذِي يُكَذِّبُ بِالدِّينِ", "en": "Have you seen the one who denies the religion?"},
            {"num": 2, "ar": "فَذَلِكَ الَّذِي يَدُعُّ الْيَتِيمَ", "en": "For that is the one who drives away the orphan"},
            {"num": 3, "ar": "وَلَا يَحُضُّ عَلَى طَعَامِ الْمِسْكِينِ", "en": "And does not encourage the feeding of the poor"},
            {"num": 4, "ar": "فَوَيْلٌ لِلْمُصَلِّينَ", "en": "So woe to those who pray"},
            {"num": 5, "ar": "الَّذِينَ هُمْ عَنْ صَلَاتِهِمْ سَاهُونَ", "en": "But who are heedless of their prayer"},
            {"num": 6, "ar": "الَّذِينَ هُمْ يُرَاءُونَ", "en": "Those who make show of their deeds"},
            {"num": 7, "ar": "وَيَمْنَعُونَ الْمَاعُونَ", "en": "And withhold simple assistance"},
        ],
    },
    {
        "id": "kafiroon", "number": 109, "name_ar": "الكافرون", "name_en": "Al-Kafiroon",
        "difficulty": 2, "total_ayahs": 6,
        "ayahs": [
            {"num": 1, "ar": "قُلْ يَا أَيُّهَا الْكَافِرُونَ", "en": "Say: O disbelievers"},
            {"num": 2, "ar": "لَا أَعْبُدُ مَا تَعْبُدُونَ", "en": "I do not worship what you worship"},
            {"num": 3, "ar": "وَلَا أَنْتُمْ عَابِدُونَ مَا أَعْبُدُ", "en": "Nor are you worshippers of what I worship"},
            {"num": 4, "ar": "وَلَا أَنَا عَابِدٌ مَا عَبَدْتُمْ", "en": "Nor will I be a worshipper of what you worship"},
            {"num": 5, "ar": "وَلَا أَنْتُمْ عَابِدُونَ مَا أَعْبُدُ", "en": "Nor will you be worshippers of what I worship"},
            {"num": 6, "ar": "لَكُمْ دِينُكُمْ وَلِيَ دِينِ", "en": "For you is your religion, and for me is my religion"},
        ],
    },
    {
        "id": "takathur", "number": 102, "name_ar": "التكاثر", "name_en": "At-Takathur",
        "difficulty": 2, "total_ayahs": 8,
        "ayahs": [
            {"num": 1, "ar": "أَلْهَاكُمُ التَّكَاثُرُ", "en": "Competition in worldly increase diverts you"},
            {"num": 2, "ar": "حَتَّى زُرْتُمُ الْمَقَابِرَ", "en": "Until you visit the graveyards"},
            {"num": 3, "ar": "كَلَّا سَوْفَ تَعْلَمُونَ", "en": "No! You will soon know"},
            {"num": 4, "ar": "ثُمَّ كَلَّا سَوْفَ تَعْلَمُونَ", "en": "Then no! You will soon know"},
            {"num": 5, "ar": "كَلَّا لَوْ تَعْلَمُونَ عِلْمَ الْيَقِينِ", "en": "No! If you only knew with certain knowledge"},
            {"num": 6, "ar": "لَتَرَوُنَّ الْجَحِيمَ", "en": "You will surely see the Hellfire"},
            {"num": 7, "ar": "ثُمَّ لَتَرَوُنَّهَا عَيْنَ الْيَقِينِ", "en": "Then you will surely see it with the eye of certainty"},
            {"num": 8, "ar": "ثُمَّ لَتُسْأَلُنَّ يَوْمَئِذٍ عَنِ النَّعِيمِ", "en": "Then you will surely be asked that Day about pleasure"},
        ],
    },
    {
        "id": "qariah", "number": 101, "name_ar": "القارعة", "name_en": "Al-Qariah",
        "difficulty": 2, "total_ayahs": 11,
        "ayahs": [
            {"num": 1, "ar": "الْقَارِعَةُ", "en": "The Striking Calamity"},
            {"num": 2, "ar": "مَا الْقَارِعَةُ", "en": "What is the Striking Calamity?"},
            {"num": 3, "ar": "وَمَا أَدْرَاكَ مَا الْقَارِعَةُ", "en": "And what will make you know what the Striking Calamity is?"},
            {"num": 4, "ar": "يَوْمَ يَكُونُ النَّاسُ كَالْفَرَاشِ الْمَبْثُوثِ", "en": "A Day when people will be like moths, dispersed"},
            {"num": 5, "ar": "وَتَكُونُ الْجِبَالُ كَالْعِهْنِ الْمَنْفُوشِ", "en": "And the mountains will be like carded wool"},
            {"num": 6, "ar": "فَأَمَّا مَنْ ثَقُلَتْ مَوَازِينُهُ", "en": "As for the one whose scales are heavy"},
            {"num": 7, "ar": "فَهُوَ فِي عِيشَةٍ رَاضِيَةٍ", "en": "He will be in a pleasant life"},
            {"num": 8, "ar": "وَأَمَّا مَنْ خَفَّتْ مَوَازِينُهُ", "en": "But as for the one whose scales are light"},
            {"num": 9, "ar": "فَأُمُّهُ هَاوِيَةٌ", "en": "His refuge will be the Pit"},
            {"num": 10, "ar": "وَمَا أَدْرَاكَ مَا هِيَهْ", "en": "And what will make you know what that is?"},
            {"num": 11, "ar": "نَارٌ حَامِيَةٌ", "en": "It is a blazing Fire"},
        ],
    },
    {
        "id": "zilzal", "number": 99, "name_ar": "الزلزلة", "name_en": "Az-Zilzal",
        "difficulty": 2, "total_ayahs": 8,
        "ayahs": [
            {"num": 1, "ar": "إِذَا زُلْزِلَتِ الْأَرْضُ زِلْزَالَهَا", "en": "When the earth is shaken with its final earthquake"},
            {"num": 2, "ar": "وَأَخْرَجَتِ الْأَرْضُ أَثْقَالَهَا", "en": "And the earth brings out its burdens"},
            {"num": 3, "ar": "وَقَالَ الْإِنْسَانُ مَا لَهَا", "en": "And man says: What is wrong with it?"},
            {"num": 4, "ar": "يَوْمَئِذٍ تُحَدِّثُ أَخْبَارَهَا", "en": "That Day, it will report its news"},
            {"num": 5, "ar": "بِأَنَّ رَبَّكَ أَوْحَى لَهَا", "en": "Because your Lord has commanded it"},
            {"num": 6, "ar": "يَوْمَئِذٍ يَصْدُرُ النَّاسُ أَشْتَاتًا لِيُرَوْا أَعْمَالَهُمْ", "en": "That Day, people will proceed in scattered groups to be shown their deeds"},
            {"num": 7, "ar": "فَمَنْ يَعْمَلْ مِثْقَالَ ذَرَّةٍ خَيْرًا يَرَهُ", "en": "So whoever does an atom's weight of good will see it"},
            {"num": 8, "ar": "وَمَنْ يَعْمَلْ مِثْقَالَ ذَرَّةٍ شَرًّا يَرَهُ", "en": "And whoever does an atom's weight of evil will see it"},
        ],
    },
]

# ═══════════════════════════════════════════════════════════════
# TAJWEED RULES (for Advanced Quran stage)
# ═══════════════════════════════════════════════════════════════

TAJWEED_RULES = [
    {"id": "t01", "emoji": "🔴", "title": {"ar": "الإدغام", "en": "Idgham (Merging)"},
     "content": {"ar": "الإدغام: إدخال حرف ساكن في حرف متحرك بعده. حروف الإدغام مجموعة في كلمة (يرملون). مثال: مَنْ يَعمل → مَيَّعمل",
                 "en": "Idgham: Merging a silent letter into the next voweled letter. Idgham letters are in (yarmalun). Example: man ya'mal → mayya'mal"}},
    {"id": "t02", "emoji": "🟢", "title": {"ar": "الإظهار", "en": "Izhar (Clarity)"},
     "content": {"ar": "الإظهار: نطق النون الساكنة أو التنوين بوضوح قبل حروف الحلق (ء هـ ع ح غ خ). مثال: مِنْ عِنده → مِنْ عِنده (بوضوح)",
                 "en": "Izhar: Pronouncing noon sakinah or tanween clearly before throat letters (ء هـ ع ح غ خ). Example: min 'indih → clear pronunciation"}},
    {"id": "t03", "emoji": "🔵", "title": {"ar": "الإخفاء", "en": "Ikhfa (Hiding)"},
     "content": {"ar": "الإخفاء: نطق النون الساكنة بين الإظهار والإدغام مع غنة. يكون قبل 15 حرفًا. مثال: مِنْ قبل → مِنقَبل (مع غنة خفيفة)",
                 "en": "Ikhfa: Pronouncing noon between clarity and merging with a nasal sound. It occurs before 15 letters. Example: min qablu → with a light nasal sound"}},
    {"id": "t04", "emoji": "🟡", "title": {"ar": "الإقلاب", "en": "Iqlab (Conversion)"},
     "content": {"ar": "الإقلاب: تحويل النون الساكنة أو التنوين إلى ميم مخفاة عند الباء. مثال: مِنْ بَعد → مِمبَعد. حرف واحد فقط: الباء.",
                 "en": "Iqlab: Converting noon sakinah or tanween to a hidden meem before ba. Example: min ba'd → mimba'd. Only one letter: ba."}},
    {"id": "t05", "emoji": "⭐", "title": {"ar": "المد الطبيعي", "en": "Natural Madd"},
     "content": {"ar": "المد الطبيعي: مد الحرف حركتين فقط عند وجود حرف مد (ا و ي) بدون سبب. مثال: قَالَ (الألف ممدودة حركتين)، يقُولُ (الواو ممدودة حركتين)",
                 "en": "Natural Madd: Extending the letter for exactly 2 counts when there's a madd letter (ا و ي) without cause. Example: qaala (alif extended 2 counts)"}},
]

# ═══════════════════════════════════════════════════════════════
# MASTERY REVIEW TOPICS (Stage 15)
# ═══════════════════════════════════════════════════════════════

MASTERY_REVIEWS = [
    {"id": "r01", "emoji": "🔤", "title": {"ar": "مراجعة: الحروف العربية", "en": "Review: Arabic Letters"},
     "quiz": [
         {"q": {"ar": "كم عدد الحروف العربية؟", "en": "How many Arabic letters?"}, "a": {"ar": "28", "en": "28"}, "opts": {"ar": ["28", "26", "30"], "en": ["28", "26", "30"]}},
         {"q": {"ar": "ما أول حرف في الأبجدية؟", "en": "What's the first letter?"}, "a": {"ar": "ألف", "en": "Alif"}, "opts": {"ar": ["ألف", "باء", "تاء"], "en": ["Alif", "Ba", "Ta"]}},
     ]},
    {"id": "r02", "emoji": "🔢", "title": {"ar": "مراجعة: الأرقام العربية", "en": "Review: Arabic Numbers"},
     "quiz": [
         {"q": {"ar": "ما هو الرقم ٧ بالعربية؟", "en": "What is ٧ in Arabic?"}, "a": {"ar": "سبعة", "en": "Seven"}, "opts": {"ar": ["سبعة", "ستة", "ثمانية"], "en": ["Seven", "Six", "Eight"]}},
         {"q": {"ar": "اكتب العدد: عشرون", "en": "Write the number: twenty"}, "a": {"ar": "٢٠", "en": "20"}, "opts": {"ar": ["٢٠", "١٢", "٣٠"], "en": ["20", "12", "30"]}},
     ]},
    {"id": "r03", "emoji": "🕌", "title": {"ar": "مراجعة: أركان الإسلام", "en": "Review: Pillars of Islam"},
     "quiz": [
         {"q": {"ar": "كم عدد أركان الإسلام؟", "en": "How many pillars of Islam?"}, "a": {"ar": "خمسة", "en": "Five"}, "opts": {"ar": ["خمسة", "ستة", "أربعة"], "en": ["Five", "Six", "Four"]}},
         {"q": {"ar": "ما الركن الثالث؟", "en": "What's the third pillar?"}, "a": {"ar": "الزكاة", "en": "Zakat"}, "opts": {"ar": ["الزكاة", "الصوم", "الحج"], "en": ["Zakat", "Fasting", "Hajj"]}},
     ]},
    {"id": "r04", "emoji": "📖", "title": {"ar": "مراجعة: القرآن الكريم", "en": "Review: Holy Quran"},
     "quiz": [
         {"q": {"ar": "كم سورة في القرآن؟", "en": "How many surahs?"}, "a": {"ar": "114", "en": "114"}, "opts": {"ar": ["114", "100", "120"], "en": ["114", "100", "120"]}},
         {"q": {"ar": "ما أول سورة في القرآن؟", "en": "First surah?"}, "a": {"ar": "الفاتحة", "en": "Al-Fatiha"}, "opts": {"ar": ["الفاتحة", "البقرة", "الإخلاص"], "en": ["Al-Fatiha", "Al-Baqarah", "Al-Ikhlas"]}},
     ]},
    {"id": "r05", "emoji": "📿", "title": {"ar": "مراجعة: الأنبياء", "en": "Review: Prophets"},
     "quiz": [
         {"q": {"ar": "كم نبيًا ذكر في القرآن؟", "en": "How many prophets in Quran?"}, "a": {"ar": "25", "en": "25"}, "opts": {"ar": ["25", "20", "30"], "en": ["25", "20", "30"]}},
         {"q": {"ar": "من خليل الله؟", "en": "Who is Friend of Allah?"}, "a": {"ar": "إبراهيم", "en": "Ibrahim"}, "opts": {"ar": ["إبراهيم", "موسى", "عيسى"], "en": ["Ibrahim", "Musa", "Isa"]}},
     ]},
    {"id": "r06", "emoji": "🤲", "title": {"ar": "مراجعة: الأدعية", "en": "Review: Duas"},
     "quiz": [
         {"q": {"ar": "ماذا نقول قبل الأكل؟", "en": "What do we say before eating?"}, "a": {"ar": "بسم الله", "en": "Bismillah"}, "opts": {"ar": ["بسم الله", "الحمد لله", "سبحان الله"], "en": ["Bismillah", "Alhamdulillah", "SubhanAllah"]}},
         {"q": {"ar": "ماذا نقول بعد الأكل؟", "en": "After eating?"}, "a": {"ar": "الحمد لله", "en": "Alhamdulillah"}, "opts": {"ar": ["الحمد لله", "بسم الله", "الله أكبر"], "en": ["Alhamdulillah", "Bismillah", "Allahu Akbar"]}},
     ]},
]


# ═══════════════════════════════════════════════════════════════
# MAIN BUILDER FUNCTION - Replaces the thin _build_advanced_sections
# ═══════════════════════════════════════════════════════════════

def build_rich_sections(stage_id: str, lesson_idx: int, lang: str) -> list:
    """Build comprehensive multi-section lessons for stages 6-15."""
    sections = []
    
    # ═══ STAGE 6: Reading Practice ═══
    if stage_id == "S06":
        passage = READING_PASSAGES[lesson_idx % len(READING_PASSAGES)]
        ar_text = passage["ar"]
        en_text = passage["en"]
        display_text = ar_text if lang == "ar" else en_text
        
        sections = [
            {"type": "read", "emoji": "📖", "title": t("read_word", lang),
             "content": {"arabic": ar_text, "translated": en_text if lang != "ar" else "", "emoji": passage["emoji"]}},
            {"type": "listen", "emoji": "🔊", "title": t("listen_repeat", lang),
             "content": {"text": ar_text, "tip": t("tip_repeat_sentence", lang)}},
            {"type": "quiz", "emoji": "❓", "title": t("test_yourself", lang),
             "content": {"question": passage.get(f"question_{lang}", passage["question_ar"]),
                         "correct": passage.get(f"answer_{lang}", passage["answer_ar"]),
                         "options": passage.get(f"options_{lang}", passage["options_ar"])}},
            {"type": "write", "emoji": "✍️", "title": t("practice_writing", lang),
             "content": {"sentence": ar_text, "tip": t("tip_write_sentence_3", lang)}},
        ]
    
    # ═══ STAGE 7: Islamic Foundations ═══
    elif stage_id == "S07":
        topic = ISLAMIC_FOUNDATIONS_DETAILED[lesson_idx % len(ISLAMIC_FOUNDATIONS_DETAILED)]
        title_text = topic["title"].get(lang, topic["title"]["ar"])
        content_text = topic["content"].get(lang, topic["content"]["ar"])
        memorize_text = topic["memorize"].get(lang, topic["memorize"]["ar"])
        
        sections = [
            {"type": "learn", "emoji": topic["emoji"], "title": title_text,
             "content": {"arabic": topic["content"]["ar"], "translated": content_text if lang != "ar" else ""}},
            {"type": "memorize", "emoji": "🧠", "title": t("memorize", lang),
             "content": {"text": topic["memorize"]["ar"], "tip": memorize_text if lang != "ar" else t("tip_read_3_memory", lang)}},
            {"type": "quiz", "emoji": "❓", "title": t("test_yourself", lang),
             "content": {"question": topic["quiz_q"].get(lang, topic["quiz_q"]["ar"]),
                         "correct": topic["quiz_a"].get(lang, topic["quiz_a"]["ar"]),
                         "options": topic["quiz_opts"].get(lang, topic["quiz_opts"]["ar"])}},
        ]
    
    # ═══ STAGE 8: Quran Memorization ═══
    elif stage_id == "S08":
        from kids_learning import QURAN_SURAHS_FOR_KIDS
        all_surahs = QURAN_SURAHS_FOR_KIDS + ADDITIONAL_SURAHS
        s_idx = lesson_idx // 7
        a_idx = lesson_idx % 7
        if s_idx < len(all_surahs):
            surah = all_surahs[s_idx]
            ayah = surah["ayahs"][a_idx % len(surah["ayahs"])]
            sections = [
                {"type": "quran", "emoji": "📖", "title": t("memorize_prefix", lang, name=surah.get('name_ar', surah['name_en'])),
                 "content": {"surah": surah.get("name_ar", surah["name_en"]), "ayah_num": ayah["num"],
                             "arabic": ayah["ar"], "translation": ayah.get(lang, ayah.get("en", ""))}},
                {"type": "listen", "emoji": "🔊", "title": t("listen_repeat", lang),
                 "content": {"text": ayah["ar"], "tip": t("tip_tap_letter", lang)}},
                {"type": "memorize", "emoji": "🧠", "title": t("recite", lang),
                 "content": {"text": ayah["ar"], "tip": t("tip_close_eyes_recite", lang)}},
                {"type": "write", "emoji": "✍️", "title": t("practice_writing", lang),
                 "content": {"sentence": ayah["ar"], "tip": t("tip_write_sentence_3", lang)}},
            ]
        else:
            sections = [{"type": "review", "emoji": "🔄", "title": t("review", lang), "content": {"tip": t("tip_review_all", lang)}}]
    
    # ═══ STAGE 9: Duas ═══
    elif stage_id == "S09":
        from kids_learning import KIDS_DUAS
        d = KIDS_DUAS[lesson_idx % len(KIDS_DUAS)]
        sections = [
            {"type": "dua", "emoji": d["emoji"], "title": d["title"].get(lang, d["title"]["ar"]),
             "content": {"arabic": d["ar"], "transliteration": d["transliteration"], "meaning": d.get(lang, d.get("en", ""))}},
            {"type": "listen", "emoji": "🔊", "title": t("listen_repeat", lang),
             "content": {"text": d["ar"], "tip": t("tip_repeat_sentence", lang)}},
            {"type": "memorize", "emoji": "🧠", "title": t("memorize_dua", lang),
             "content": {"text": d["ar"], "tip": t("tip_repeat_dua_5", lang)}},
            {"type": "quiz", "emoji": "❓", "title": t("test_yourself", lang),
             "content": {"question": t("quiz_complete_dua", lang) if t("quiz_complete_dua", lang) != "quiz_complete_dua" else ({"ar": "أكمل الدعاء", "en": "Complete the dua"}.get(lang, "أكمل الدعاء")),
                         "correct": d["ar"][:30],
                         "options": [d["ar"][:30], KIDS_DUAS[(lesson_idx+1) % len(KIDS_DUAS)]["ar"][:30], KIDS_DUAS[(lesson_idx+2) % len(KIDS_DUAS)]["ar"][:30]]}},
        ]
    
    # ═══ STAGE 10: Hadiths ═══
    elif stage_id == "S10":
        from kids_learning import KIDS_HADITHS
        h = KIDS_HADITHS[lesson_idx % len(KIDS_HADITHS)]
        sections = [
            {"type": "hadith", "emoji": h["emoji"], "title": t("todays_hadith", lang),
             "content": {"arabic": h["ar"], "translation": h.get(lang, h.get("en", "")), "source": h["source"],
                         "lesson": h["lesson"].get(lang, h["lesson"].get("en", ""))}},
            {"type": "memorize", "emoji": "🧠", "title": t("memorize", lang),
             "content": {"text": h["ar"], "tip": t("tip_read_3_memory", lang)}},
            {"type": "reflect", "emoji": "💭", "title": t("reflect", lang),
             "content": {"tip": h["lesson"].get(lang, h["lesson"].get("en", ""))}},
        ]
    
    # ═══ STAGE 11: Prophet Stories ═══
    elif stage_id == "S11":
        from kids_learning_extended import ALL_PROPHETS, get_prophet_field
        p = ALL_PROPHETS[lesson_idx % len(ALL_PROPHETS)]
        p_name = get_prophet_field(p, "name", lang) or p["name"].get(lang, p["name"].get("ar", ""))
        p_title = get_prophet_field(p, "title", lang) or p["title"].get(lang, p["title"].get("ar", ""))
        p_summary = get_prophet_field(p, "summary", lang)
        p_lesson = get_prophet_field(p, "lesson", lang)
        sections = [
            {"type": "story", "emoji": p["emoji"], "title": p_name,
             "content": {"name": p_name, "title": p_title, "summary": p_summary,
                         "lesson": p_lesson, "quran_ref": p["quran_ref"]}},
            {"type": "memorize", "emoji": "🧠", "title": t("memorize", lang),
             "content": {"text": p["quran_ref"], "tip": p_lesson}},
            {"type": "quiz", "emoji": "❓", "title": t("test_yourself", lang),
             "content": {"question": {"ar": f"ما لقب النبي {p['name'].get('ar', '')}؟", "en": f"What is Prophet {p['name'].get('en', '')}'s title?"}.get(lang, f"ما لقب النبي {p['name'].get('ar', '')}؟"),
                         "correct": p_title,
                         "options": [p_title, 
                                     get_prophet_field(ALL_PROPHETS[(lesson_idx+1) % len(ALL_PROPHETS)], "title", lang),
                                     get_prophet_field(ALL_PROPHETS[(lesson_idx+3) % len(ALL_PROPHETS)], "title", lang)]}},
        ]
    
    # ═══ STAGE 12: Islamic Life ═══
    elif stage_id == "S12":
        topic = ISLAMIC_LIFE_TOPICS[lesson_idx % len(ISLAMIC_LIFE_TOPICS)]
        title_text = topic["title"].get(lang, topic["title"]["ar"])
        content_text = topic["content"].get(lang, topic["content"]["ar"])
        sections = [
            {"type": "learn", "emoji": topic["emoji"], "title": title_text,
             "content": {"arabic": topic["content"]["ar"], "translated": content_text if lang != "ar" else ""}},
            {"type": "listen", "emoji": "🔊", "title": t("listen_repeat", lang),
             "content": {"text": topic["content"]["ar"][:80], "tip": t("tip_repeat_sentence", lang)}},
            {"type": "memorize", "emoji": "🧠", "title": t("memorize", lang),
             "content": {"text": topic["content"]["ar"][:80], "tip": t("tip_read_3_memory", lang)}},
        ]
    
    # ═══ STAGE 13: Advanced Arabic ═══
    elif stage_id == "S13":
        grammar = ARABIC_GRAMMAR_LESSONS[lesson_idx % len(ARABIC_GRAMMAR_LESSONS)]
        title_text = grammar["title"].get(lang, grammar["title"]["ar"])
        content_text = grammar["content"].get(lang, grammar["content"]["ar"])
        
        section_list = [
            {"type": "learn", "emoji": grammar["emoji"], "title": title_text,
             "content": {"arabic": grammar["content"]["ar"], "translated": content_text if lang != "ar" else ""}},
        ]
        
        # Add practice items if available
        if grammar.get("practice"):
            practice_items = []
            for p in grammar["practice"]:
                if "word" in p:
                    practice_items.append(p.get("word", "") + " → " + p.get("plural", p.get("opposite", "")))
                elif "past" in p:
                    practice_items.append(p["past"] + " → " + p["present"] + " → " + p["command"])
                elif "sentence" in p:
                    practice_items.append(p["sentence"])
                elif "question" in p:
                    practice_items.append(p["question"] + " — " + p["answer"])
                elif "pronoun" in p:
                    practice_items.append(p["pronoun"] + ": " + p["example"])
                elif "day" in p:
                    practice_items.append(p["day"])
            
            if practice_items:
                section_list.append(
                    {"type": "practice", "emoji": "🎯", "title": t("test", lang),
                     "content": {"items": practice_items, "tip": t("listen_repeat", lang)}}
                )
        
        section_list.append(
            {"type": "write", "emoji": "✍️", "title": t("practice_writing", lang),
             "content": {"tip": t("tip_write_sentence_3", lang)}}
        )
        sections = section_list
    
    # ═══ STAGE 14: Advanced Quran + Tajweed ═══
    elif stage_id == "S14":
        # First half: More surahs, second half: tajweed
        half = (960 - 901 + 1) // 2
        if lesson_idx < half:
            # Advanced surah memorization
            from kids_learning import QURAN_SURAHS_FOR_KIDS
            all_surahs = QURAN_SURAHS_FOR_KIDS + ADDITIONAL_SURAHS
            s_idx = lesson_idx // 5
            a_idx = lesson_idx % 5
            if s_idx < len(all_surahs):
                surah = all_surahs[s_idx % len(all_surahs)]
                ayah = surah["ayahs"][a_idx % len(surah["ayahs"])]
                sections = [
                    {"type": "quran", "emoji": "📖", "title": t("memorize_prefix", lang, name=surah.get('name_ar', surah['name_en'])),
                     "content": {"surah": surah.get("name_ar", surah["name_en"]), "ayah_num": ayah["num"],
                                 "arabic": ayah["ar"], "translation": ayah.get(lang, ayah.get("en", ""))}},
                    {"type": "listen", "emoji": "🔊", "title": t("listen_repeat", lang),
                     "content": {"text": ayah["ar"]}},
                    {"type": "memorize", "emoji": "🧠", "title": t("recite", lang),
                     "content": {"tip": t("tip_close_eyes_recite", lang)}},
                ]
            else:
                sections = [{"type": "review", "emoji": "🔄", "title": t("review", lang), "content": {"tip": t("tip_review_all", lang)}}]
        else:
            # Tajweed rules
            rule = TAJWEED_RULES[(lesson_idx - half) % len(TAJWEED_RULES)]
            sections = [
                {"type": "learn", "emoji": rule["emoji"], "title": rule["title"].get(lang, rule["title"]["ar"]),
                 "content": {"arabic": rule["content"]["ar"], "translated": rule["content"].get(lang, rule["content"]["ar"]) if lang != "ar" else ""}},
                {"type": "practice", "emoji": "🎯", "title": t("test", lang),
                 "content": {"tip": rule["content"].get(lang, rule["content"]["ar"])}},
            ]
    
    # ═══ STAGE 15: Mastery & Graduation ═══
    elif stage_id == "S15":
        review = MASTERY_REVIEWS[lesson_idx % len(MASTERY_REVIEWS)]
        quiz_items = review["quiz"]
        quiz = quiz_items[lesson_idx % len(quiz_items)] if quiz_items else None
        
        section_list = [
            {"type": "review", "emoji": review["emoji"], "title": review["title"].get(lang, review["title"]["ar"]),
             "content": {"tip": t("tip_review_all", lang)}},
        ]
        
        if quiz:
            section_list.append(
                {"type": "quiz", "emoji": "❓", "title": t("test_yourself", lang),
                 "content": {"question": quiz["q"].get(lang, quiz["q"]["ar"]),
                             "correct": quiz["a"].get(lang, quiz["a"]["ar"]),
                             "options": quiz["opts"].get(lang, quiz["opts"]["ar"])}}
            )
        
        section_list.append(
            {"type": "memorize", "emoji": "🎓", "title": t("comprehensive_review", lang),
             "content": {"tip": t("tip_review_all", lang)}}
        )
        sections = section_list
    
    if not sections:
        sections = [{"type": "learn", "emoji": "📝", "title": t("lesson", lang), "content": {"tip": t("learn", lang)}}]
    
    return sections

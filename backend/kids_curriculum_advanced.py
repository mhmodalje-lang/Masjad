"""
Advanced Curriculum Content for Stages 6-15
============================================
Comprehensive educational content for Noor Academy
Each stage has deep, rich, multi-section daily lessons
"""
from localization_engine import t

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
     "title": {"ar": "الشهادتان - الركن الأول", "en": "The Two Testimonies - First Pillar", "de": "Die zwei Glaubensbekenntnisse - Erste Säule", "fr": "Les deux attestations - Premier pilier", "tr": "İki Şehadet - Birinci Şart", "ru": "Два свидетельства - Первый столп", "sv": "De två vittnesbörden - Första pelaren", "nl": "De twee getuigenissen - Eerste zuil", "el": "Οι δύο μαρτυρίες - Πρώτος πυλώνας"},
     "content": {"ar": "أشهد أن لا إله إلا الله وأشهد أن محمدًا رسول الله. هذا هو الركن الأول من أركان الإسلام. معناها أننا نؤمن بأن الله واحد لا شريك له، وأن محمدًا ﷺ رسوله الكريم.",
                 "en": "I bear witness that there is no god but Allah and Muhammad is His messenger. This is the first pillar of Islam. It means we believe Allah is One with no partners, and Muhammad ﷺ is His noble messenger.",
                 "de": "Ich bezeuge, dass es keinen Gott gibt außer Allah und Muhammad ist Sein Gesandter. Dies ist die erste Säule des Islam. Es bedeutet, dass Allah Einer ist ohne Partner und Muhammad ﷺ Sein edler Gesandter ist.",
                 "fr": "J'atteste qu'il n'y a de dieu qu'Allah et que Muhammad est Son messager. C'est le premier pilier de l'Islam. Cela signifie que nous croyons qu'Allah est Unique sans associé et que Muhammad ﷺ est Son noble messager.",
                 "tr": "Şehadet ederim ki Allah'tan başka ilah yoktur ve Muhammed O'nun elçisidir. Bu İslam'ın birinci şartıdır. Allah'ın bir olduğuna ve Muhammed'in ﷺ O'nun peygamberi olduğuna inanırız.",
                 "ru": "Я свидетельствую, что нет бога кроме Аллаха и Мухаммад - Его посланник. Это первый столп Ислама. Это означает веру в единство Аллаха и в то, что Мухаммад ﷺ - Его благородный посланник.",
                 "sv": "Jag vittnar att det inte finns någon gud utom Allah och Muhammad är Hans sändebud. Detta är Islams första pelare. Det betyder att Allah är En utan partner och Muhammad ﷺ är Hans ädla sändebud.",
                 "nl": "Ik getuig dat er geen god is dan Allah en Muhammad is Zijn boodschapper. Dit is de eerste zuil van de Islam. Het betekent dat Allah Eén is zonder partner en Muhammad ﷺ Zijn edele boodschapper is.",
                 "el": "Μαρτυρώ ότι δεν υπάρχει θεός εκτός από τον Αλλάχ και ο Μωχάμεντ είναι ο απεσταλμένος Του. Αυτός είναι ο πρώτος πυλώνας του Ισλάμ."},
     "memorize": {"ar": "أشهد أن لا إله إلا الله وأشهد أن محمدًا رسول الله", "en": "I bear witness that there is no god but Allah and Muhammad is His messenger", "de": "Ich bezeuge, dass es keinen Gott gibt außer Allah und Muhammad ist Sein Gesandter", "fr": "J'atteste qu'il n'y a de dieu qu'Allah et que Muhammad est Son messager", "tr": "Şehadet ederim ki Allah'tan başka ilah yoktur ve Muhammed O'nun elçisidir", "ru": "Я свидетельствую, что нет бога кроме Аллаха и Мухаммад - Его посланник", "sv": "Jag vittnar att det inte finns någon gud utom Allah och Muhammad är Hans sändebud", "nl": "Ik getuig dat er geen god is dan Allah en Muhammad is Zijn boodschapper", "el": "Μαρτυρώ ότι δεν υπάρχει θεός εκτός από τον Αλλάχ και ο Μωχάμεντ είναι ο απεσταλμένος Του"},
     "quiz_q": {"ar": "ما هو الركن الأول من أركان الإسلام؟", "en": "What is the first pillar of Islam?", "de": "Was ist die erste Säule des Islam?", "fr": "Quel est le premier pilier de l'Islam?", "tr": "İslam'ın birinci şartı nedir?", "ru": "Какой первый столп Ислама?", "sv": "Vilken är Islams första pelare?", "nl": "Wat is de eerste zuil van de Islam?", "el": "Ποιος είναι ο πρώτος πυλώνας του Ισλάμ;"},
     "quiz_a": {"ar": "الشهادتان", "en": "The Two Testimonies", "de": "Die zwei Glaubensbekenntnisse", "fr": "Les deux attestations", "tr": "İki Şehadet", "ru": "Два свидетельства", "sv": "De två vittnesbörden", "nl": "De twee getuigenissen", "el": "Οι δύο μαρτυρίες"},
     "quiz_opts": {"ar": ["الشهادتان", "الصلاة", "الزكاة"], "en": ["The Two Testimonies", "Prayer", "Zakat"], "de": ["Glaubensbekenntnisse", "Gebet", "Zakat"], "fr": ["Les attestations", "La prière", "La Zakat"], "tr": ["İki Şehadet", "Namaz", "Zekât"], "ru": ["Два свидетельства", "Молитва", "Закят"], "sv": ["Vittnesbörden", "Bönen", "Zakat"], "nl": ["Getuigenissen", "Gebed", "Zakat"], "el": ["Μαρτυρίες", "Προσευχή", "Ζακάτ"]}},
    
    # Salah details
    {"id": "salah_1", "emoji": "🕌", "topic": "salah",
     "title": {"ar": "الصلاة - الركن الثاني", "en": "Prayer - Second Pillar", "de": "Gebet - Zweite Säule", "fr": "La prière - Deuxième pilier", "tr": "Namaz - İkinci Şart", "ru": "Молитва - Второй столп", "sv": "Bönen - Andra pelaren", "nl": "Gebed - Tweede zuil", "el": "Προσευχή - Δεύτερος πυλώνας"},
     "content": {"ar": "الصلاة هي الركن الثاني من أركان الإسلام. نصلي خمس صلوات في اليوم: الفجر (ركعتان)، الظهر (4 ركعات)، العصر (4 ركعات)، المغرب (3 ركعات)، العشاء (4 ركعات).",
                 "en": "Prayer is the second pillar of Islam. We pray five daily prayers: Fajr (2 rak'ahs), Dhuhr (4), Asr (4), Maghrib (3), Isha (4).",
                 "de": "Das Gebet ist die zweite Säule des Islam. Wir beten fünf tägliche Gebete: Fajr (2), Dhuhr (4), Asr (4), Maghrib (3), Isha (4).",
                 "fr": "La prière est le deuxième pilier de l'Islam. Nous prions cinq prières quotidiennes: Fajr (2 rak'ahs), Dhouhr (4), Asr (4), Maghrib (3), Isha (4).",
                 "tr": "Namaz İslam'ın ikinci şartıdır. Günde beş vakit namaz kılarız: Sabah (2), Öğle (4), İkindi (4), Akşam (3), Yatsı (4).",
                 "ru": "Молитва - второй столп Ислама. Мы совершаем пять ежедневных молитв: Фаджр (2), Зухр (4), Аср (4), Магриб (3), Иша (4).",
                 "sv": "Bönen är Islams andra pelare. Vi ber fem dagliga böner: Fajr (2), Dhuhr (4), Asr (4), Maghrib (3), Isha (4).",
                 "nl": "Het gebed is de tweede zuil van de Islam. We bidden vijf dagelijkse gebeden: Fajr (2), Dhuhr (4), Asr (4), Maghrib (3), Isha (4).",
                 "el": "Η προσευχή είναι ο δεύτερος πυλώνας του Ισλάμ. Προσευχόμαστε πέντε φορές: Φατζρ (2), Ντουχρ (4), Ασρ (4), Μαγκρίμπ (3), Ίσα (4)."},
     "memorize": {"ar": "الصلوات الخمس: الفجر، الظهر، العصر، المغرب، العشاء", "en": "Five prayers: Fajr, Dhuhr, Asr, Maghrib, Isha", "de": "Fünf Gebete: Fajr, Dhuhr, Asr, Maghrib, Isha", "fr": "Cinq prières: Fajr, Dhouhr, Asr, Maghrib, Isha", "tr": "Beş vakit namaz: Sabah, Öğle, İkindi, Akşam, Yatsı", "ru": "Пять молитв: Фаджр, Зухр, Аср, Магриб, Иша", "sv": "Fem böner: Fajr, Dhuhr, Asr, Maghrib, Isha", "nl": "Vijf gebeden: Fajr, Dhuhr, Asr, Maghrib, Isha", "el": "Πέντε προσευχές: Φατζρ, Ντουχρ, Ασρ, Μαγκρίμπ, Ίσα"},
     "quiz_q": {"ar": "كم ركعة في صلاة المغرب؟", "en": "How many rak'ahs in Maghrib?", "de": "Wie viele Gebetseinheiten hat Maghrib?", "fr": "Combien de rak'ahs à Maghrib?", "tr": "Akşam namazı kaç rekât?", "ru": "Сколько ракаатов в Магрибе?", "sv": "Hur många rak'ahs i Maghrib?", "nl": "Hoeveel rak'ahs in Maghrib?", "el": "Πόσα ρακάτ στο Μαγκρίμπ;"},
     "quiz_a": {"ar": "3 ركعات", "en": "3 rak'ahs", "de": "3 Gebetseinheiten", "fr": "3 rak'ahs", "tr": "3 rekât", "ru": "3 ракаата", "sv": "3 rak'ahs", "nl": "3 rak'ahs", "el": "3 ρακάτ"},
     "quiz_opts": {"ar": ["3 ركعات", "4 ركعات", "2 ركعتان"], "en": ["3 rak'ahs", "4 rak'ahs", "2 rak'ahs"], "de": ["3", "4", "2"], "fr": ["3 rak'ahs", "4 rak'ahs", "2 rak'ahs"], "tr": ["3 rekât", "4 rekât", "2 rekât"], "ru": ["3 ракаата", "4 ракаата", "2 ракаата"], "sv": ["3 rak'ahs", "4 rak'ahs", "2 rak'ahs"], "nl": ["3 rak'ahs", "4 rak'ahs", "2 rak'ahs"], "el": ["3 ρακάτ", "4 ρακάτ", "2 ρακάτ"]}},
    
    {"id": "salah_2", "emoji": "🧎", "topic": "salah",
     "title": {"ar": "أوقات الصلاة", "en": "Prayer Times", "de": "Gebetszeiten", "fr": "Horaires de prière", "tr": "Namaz Vakitleri", "ru": "Времена молитв", "sv": "Bönetider", "nl": "Gebedstijden", "el": "Ώρες προσευχής"},
     "content": {"ar": "لكل صلاة وقت محدد: الفجر عند طلوع الفجر، الظهر عند زوال الشمس، العصر عند منتصف العصر، المغرب عند غروب الشمس، العشاء بعد غياب الشفق الأحمر.",
                 "en": "Each prayer has a specific time: Fajr at dawn, Dhuhr at noon, Asr in the afternoon, Maghrib at sunset, Isha after the red twilight disappears.",
                 "de": "Jedes Gebet hat eine bestimmte Zeit: Fajr bei Morgendämmerung, Dhuhr am Mittag, Asr am Nachmittag, Maghrib bei Sonnenuntergang, Isha nach dem Verschwinden der Abenddämmerung.",
                 "fr": "Chaque prière a un horaire précis: Fajr à l'aube, Dhouhr à midi, Asr l'après-midi, Maghrib au coucher du soleil, Isha après la disparition du crépuscule.",
                 "tr": "Her namazın belirli bir vakti vardır: Sabah tan yerinde, Öğle güneş tepe noktasında, İkindi öğleden sonra, Akşam güneş batarken, Yatsı kırmızı şafak kaybolunca.",
                 "ru": "У каждой молитвы своё время: Фаджр на рассвете, Зухр в полдень, Аср после полудня, Магриб на закате, Иша после исчезновения сумерек.",
                 "sv": "Varje bön har en bestämd tid: Fajr vid gryningen, Dhuhr vid middagstid, Asr på eftermiddagen, Maghrib vid solnedgången, Isha efter skymningen.",
                 "nl": "Elk gebed heeft een specifieke tijd: Fajr bij dageraad, Dhuhr op het middaguur, Asr in de namiddag, Maghrib bij zonsondergang, Isha na het verdwijnen van de schemering.",
                 "el": "Κάθε προσευχή έχει συγκεκριμένη ώρα: Φατζρ στην αυγή, Ντουχρ το μεσημέρι, Ασρ το απόγευμα, Μαγκρίμπ στο ηλιοβασίλεμα, Ίσα μετά το λυκόφως."},
     "memorize": {"ar": "الفجر: طلوع الفجر | الظهر: زوال الشمس | العصر: العصر | المغرب: غروب الشمس | العشاء: بعد الشفق", "en": "Fajr: dawn | Dhuhr: noon | Asr: afternoon | Maghrib: sunset | Isha: after twilight", "de": "Fajr: Morgendämmerung | Dhuhr: Mittag | Asr: Nachmittag | Maghrib: Sonnenuntergang | Isha: Abenddämmerung", "fr": "Fajr: aube | Dhouhr: midi | Asr: après-midi | Maghrib: coucher du soleil | Isha: crépuscule", "tr": "Sabah: tan yeri | Öğle: zeval | İkindi: öğleden sonra | Akşam: güneş batışı | Yatsı: şafak", "ru": "Фаджр: рассвет | Зухр: полдень | Аср: полдень | Магриб: закат | Иша: сумерки", "sv": "Fajr: gryning | Dhuhr: middag | Asr: eftermiddag | Maghrib: solnedgång | Isha: skymning", "nl": "Fajr: dageraad | Dhuhr: middag | Asr: namiddag | Maghrib: zonsondergang | Isha: schemering", "el": "Φατζρ: αυγή | Ντουχρ: μεσημέρι | Ασρ: απόγευμα | Μαγκρίμπ: ηλιοβασίλεμα | Ίσα: λυκόφως"},
     "quiz_q": {"ar": "متى وقت صلاة المغرب؟", "en": "When is Maghrib prayer time?", "de": "Wann ist die Maghrib-Gebetszeit?", "fr": "Quand est l'heure de Maghrib?", "tr": "Akşam namazının vakti ne zaman?", "ru": "Когда время молитвы Магриб?", "sv": "När är Maghrib bönetid?", "nl": "Wanneer is Maghrib gebedstijd?", "el": "Πότε είναι η ώρα του Μαγκρίμπ;"},
     "quiz_a": {"ar": "عند غروب الشمس", "en": "At sunset", "de": "Bei Sonnenuntergang", "fr": "Au coucher du soleil", "tr": "Güneş batarken", "ru": "На закате", "sv": "Vid solnedgången", "nl": "Bij zonsondergang", "el": "Στο ηλιοβασίλεμα"},
     "quiz_opts": {"ar": ["عند غروب الشمس", "عند طلوع الشمس", "عند منتصف الليل"], "en": ["At sunset", "At sunrise", "At midnight"], "de": ["Bei Sonnenuntergang", "Bei Sonnenaufgang", "Um Mitternacht"], "fr": ["Au coucher du soleil", "Au lever du soleil", "À minuit"], "tr": ["Güneş batarken", "Güneş doğarken", "Gece yarısı"], "ru": ["На закате", "На рассвете", "В полночь"], "sv": ["Vid solnedgången", "Vid soluppgången", "Vid midnatt"], "nl": ["Bij zonsondergang", "Bij zonsopgang", "Om middernacht"], "el": ["Στο ηλιοβασίλεμα", "Στην ανατολή", "Στα μεσάνυχτα"]}},
    
    # Zakat
    {"id": "zakat_1", "emoji": "💰", "topic": "zakat",
     "title": {"ar": "الزكاة - الركن الثالث", "en": "Zakat - Third Pillar", "de": "Zakat - Dritte Säule", "fr": "La Zakat - Troisième pilier", "tr": "Zekât - Üçüncü Şart", "ru": "Закят - Третий столп", "sv": "Zakat - Tredje pelaren", "nl": "Zakat - Derde zuil", "el": "Ζακάτ - Τρίτος πυλώνας"},
     "content": {"ar": "الزكاة هي إعطاء جزء من المال للفقراء والمحتاجين. هي حق الفقير في مال الغني. الزكاة تُطهِّر المال وتزيد البركة. قال الله تعالى: وأقيموا الصلاة وآتوا الزكاة.",
                 "en": "Zakat is giving a portion of wealth to the poor and needy. It is the right of the poor in the wealth of the rich. Zakat purifies wealth and increases blessings. Allah says: Establish prayer and give Zakat.",
                 "de": "Zakat bedeutet, einen Teil des Vermögens an die Armen und Bedürftigen zu geben. Es ist das Recht der Armen am Reichtum der Reichen. Zakat reinigt das Vermögen und mehrt den Segen.",
                 "fr": "La Zakat consiste à donner une partie de ses biens aux pauvres et aux nécessiteux. C'est le droit du pauvre sur la richesse du riche. La Zakat purifie les biens et augmente les bénédictions.",
                 "tr": "Zekât, malın bir kısmını fakirlere ve muhtaçlara vermektir. Zenginin malında fakirin hakkıdır. Zekât malı temizler ve bereketi artırır.",
                 "ru": "Закят - это выделение части имущества бедным и нуждающимся. Это право бедного на богатство богатого. Закят очищает имущество и увеличивает благословения.",
                 "sv": "Zakat innebär att ge en del av sin rikedom till de fattiga och behövande. Det är de fattigas rätt i de rikas tillgångar. Zakat renar rikedomen och ökar välsignelserna.",
                 "nl": "Zakat is het geven van een deel van je bezit aan de armen en behoeftigen. Het is het recht van de arme op het bezit van de rijke. Zakat zuivert bezit en vermeerdert zegeningen.",
                 "el": "Η Ζακάτ είναι η προσφορά μέρους του πλούτου στους φτωχούς. Είναι δικαίωμα του φτωχού στον πλούτο του πλουσίου. Η Ζακάτ καθαρίζει τον πλούτο."},
     "memorize": {"ar": "الزكاة تطهر المال وتزيد البركة", "en": "Zakat purifies wealth and increases blessings", "de": "Zakat reinigt Vermögen und mehrt Segen", "fr": "La Zakat purifie les biens et augmente les bénédictions", "tr": "Zekât malı temizler ve bereketi artırır", "ru": "Закят очищает имущество и увеличивает благословения", "sv": "Zakat renar rikedom och ökar välsignelser", "nl": "Zakat zuivert bezit en vermeerdert zegeningen", "el": "Η Ζακάτ καθαρίζει τον πλούτο και αυξάνει τις ευλογίες"},
     "quiz_q": {"ar": "لمن نعطي الزكاة؟", "en": "To whom do we give Zakat?", "de": "Wem geben wir Zakat?", "fr": "À qui donnons-nous la Zakat?", "tr": "Zekâtı kime veririz?", "ru": "Кому мы даём закят?", "sv": "Till vem ger vi Zakat?", "nl": "Aan wie geven we Zakat?", "el": "Σε ποιον δίνουμε Ζακάτ;"},
     "quiz_a": {"ar": "للفقراء والمحتاجين", "en": "To the poor and needy", "de": "An die Armen und Bedürftigen", "fr": "Aux pauvres et nécessiteux", "tr": "Fakirlere ve muhtaçlara", "ru": "Бедным и нуждающимся", "sv": "Till de fattiga och behövande", "nl": "Aan de armen en behoeftigen", "el": "Στους φτωχούς και τους έχοντες ανάγκη"},
     "quiz_opts": {"ar": ["للفقراء والمحتاجين", "للأغنياء", "لأنفسنا"], "en": ["To the poor and needy", "To the rich", "To ourselves"], "de": ["Arme und Bedürftige", "Die Reichen", "Uns selbst"], "fr": ["Pauvres et nécessiteux", "Les riches", "Nous-mêmes"], "tr": ["Fakirlere", "Zenginlere", "Kendimize"], "ru": ["Бедным", "Богатым", "Себе"], "sv": ["De fattiga", "De rika", "Oss själva"], "nl": ["De armen", "De rijken", "Onszelf"], "el": ["Τους φτωχούς", "Τους πλούσιους", "Τον εαυτό μας"]}},
    
    # Sawm (Fasting)
    {"id": "sawm_1", "emoji": "🌙", "topic": "sawm",
     "title": {"ar": "الصوم - الركن الرابع", "en": "Fasting - Fourth Pillar", "de": "Fasten - Vierte Säule", "fr": "Le jeûne - Quatrième pilier", "tr": "Oruç - Dördüncü Şart", "ru": "Пост - Четвёртый столп", "sv": "Fasta - Fjärde pelaren", "nl": "Vasten - Vierde zuil", "el": "Νηστεία - Τέταρτος πυλώνας"},
     "content": {"ar": "الصوم هو الامتناع عن الطعام والشراب من الفجر إلى المغرب في شهر رمضان. الصوم يعلمنا الصبر والتقوى والإحساس بالفقراء. الأطفال يتدربون على الصيام تدريجيًا.",
                 "en": "Fasting means abstaining from food and drink from dawn to sunset in Ramadan. Fasting teaches us patience, God-consciousness and empathy for the poor. Children practice fasting gradually.",
                 "de": "Fasten bedeutet, von Morgendämmerung bis Sonnenuntergang im Ramadan auf Essen und Trinken zu verzichten. Fasten lehrt uns Geduld, Gottesfurcht und Mitgefühl für die Armen.",
                 "fr": "Le jeûne consiste à s'abstenir de manger et boire de l'aube au coucher du soleil pendant le Ramadan. Le jeûne nous enseigne la patience, la piété et la compassion envers les pauvres.",
                 "tr": "Oruç, Ramazan ayında fecirden akşama kadar yiyecek ve içecekten kaçınmaktır. Oruç bize sabır, takva ve fakirlere empati öğretir.",
                 "ru": "Пост означает воздержание от еды и питья от рассвета до заката в Рамадан. Пост учит терпению, богобоязненности и сочувствию к бедным.",
                 "sv": "Fasta innebär att avstå från mat och dryck från gryning till solnedgång under Ramadan. Fasta lär oss tålamod, gudsfruktan och medkänsla för de fattiga.",
                 "nl": "Vasten betekent zich onthouden van eten en drinken van dageraad tot zonsondergang in Ramadan. Vasten leert ons geduld, godsvrees en medeleven met de armen.",
                 "el": "Η νηστεία σημαίνει αποχή από φαγητό και ποτό από την αυγή μέχρι το ηλιοβασίλεμα στο Ραμαντάν. Η νηστεία μας διδάσκει υπομονή και συμπάθεια."},
     "memorize": {"ar": "الصوم من الفجر إلى المغرب في رمضان", "en": "Fasting from dawn to sunset in Ramadan", "de": "Fasten von Morgendämmerung bis Sonnenuntergang im Ramadan", "fr": "Jeûne de l'aube au coucher du soleil pendant le Ramadan", "tr": "Ramazan'da fecirden akşama oruç", "ru": "Пост от рассвета до заката в Рамадан", "sv": "Fasta från gryning till solnedgång i Ramadan", "nl": "Vasten van dageraad tot zonsondergang in Ramadan", "el": "Νηστεία από αυγή μέχρι ηλιοβασίλεμα στο Ραμαντάν"},
     "quiz_q": {"ar": "ماذا يعلمنا الصوم؟", "en": "What does fasting teach us?", "de": "Was lehrt uns das Fasten?", "fr": "Que nous enseigne le jeûne?", "tr": "Oruç bize ne öğretir?", "ru": "Чему учит нас пост?", "sv": "Vad lär oss fastan?", "nl": "Wat leert het vasten ons?", "el": "Τι μας διδάσκει η νηστεία;"},
     "quiz_a": {"ar": "الصبر والتقوى", "en": "Patience and God-consciousness", "de": "Geduld und Gottesfurcht", "fr": "Patience et piété", "tr": "Sabır ve takva", "ru": "Терпение и богобоязненность", "sv": "Tålamod och gudsfruktan", "nl": "Geduld en godsvrees", "el": "Υπομονή και ευσέβεια"},
     "quiz_opts": {"ar": ["الصبر والتقوى", "الكسل", "الجوع فقط"], "en": ["Patience and piety", "Laziness", "Just hunger"], "de": ["Geduld und Frömmigkeit", "Faulheit", "Nur Hunger"], "fr": ["Patience et piété", "Paresse", "Seulement la faim"], "tr": ["Sabır ve takva", "Tembellik", "Sadece açlık"], "ru": ["Терпение и благочестие", "Лень", "Только голод"], "sv": ["Tålamod och fromhet", "Lathet", "Bara hunger"], "nl": ["Geduld en vroomheid", "Luiheid", "Alleen honger"], "el": ["Υπομονή και ευσέβεια", "Τεμπελιά", "Μόνο πείνα"]}},
    
    # Hajj
    {"id": "hajj_1", "emoji": "🕋", "topic": "hajj",
     "title": {"ar": "الحج - الركن الخامس", "en": "Hajj - Fifth Pillar", "de": "Hadsch - Fünfte Säule", "fr": "Le Hajj - Cinquième pilier", "tr": "Hac - Beşinci Şart", "ru": "Хадж - Пятый столп", "sv": "Hajj - Femte pelaren", "nl": "Hadj - Vijfde zuil", "el": "Χατζ - Πέμπτος πυλώνας"},
     "content": {"ar": "الحج هو زيارة مكة المكرمة لأداء مناسك معينة. يكون في شهر ذي الحجة. يطوف الحجاج حول الكعبة سبع مرات ويسعون بين الصفا والمروة. الحج واجب مرة واحدة في العمر لمن يستطيع.",
                 "en": "Hajj is visiting Makkah to perform specific rituals. It takes place in Dhul-Hijjah month. Pilgrims circle the Kaaba seven times and walk between Safa and Marwa. Hajj is obligatory once in a lifetime for those who can."},
     "memorize": {"ar": "الطواف حول الكعبة سبع مرات والسعي بين الصفا والمروة", "en": "Circle the Kaaba 7 times and walk between Safa and Marwa"},
     "quiz_q": {"ar": "كم مرة نطوف حول الكعبة؟", "en": "How many times do we circle the Kaaba?"},
     "quiz_a": {"ar": "سبع مرات", "en": "Seven times"},
     "quiz_opts": {"ar": ["سبع مرات", "خمس مرات", "ثلاث مرات"], "en": ["Seven times", "Five times", "Three times"]}},
    
    # Wudu details
    {"id": "wudu_detail", "emoji": "💧", "topic": "wudu",
     "title": {"ar": "الوضوء خطوة بخطوة", "en": "Wudu Step by Step", "de": "Wudu Schritt für Schritt", "fr": "Les ablutions étape par étape", "tr": "Abdest Adım Adım", "ru": "Вуду шаг за шагом", "sv": "Wudu steg för steg", "nl": "Woedoe stap voor stap", "el": "Γουντού βήμα βήμα"},
     "content": {"ar": "خطوات الوضوء: ١- النية وقول بسم الله ٢- غسل الكفين ثلاثًا ٣- المضمضة والاستنشاق ثلاثًا ٤- غسل الوجه ثلاثًا ٥- غسل اليدين إلى المرفقين ثلاثًا ٦- مسح الرأس ٧- غسل القدمين ثلاثًا",
                 "en": "Wudu steps: 1- Intention and say Bismillah 2- Wash hands 3 times 3- Rinse mouth and nose 3 times 4- Wash face 3 times 5- Wash arms to elbows 3 times 6- Wipe head 7- Wash feet 3 times"},
     "memorize": {"ar": "بسم الله - الكفان - المضمضة - الوجه - اليدان - الرأس - القدمان", "en": "Bismillah - Hands - Mouth - Face - Arms - Head - Feet"},
     "quiz_q": {"ar": "كم مرة نغسل الوجه في الوضوء؟", "en": "How many times do we wash the face in wudu?"},
     "quiz_a": {"ar": "ثلاث مرات", "en": "Three times"},
     "quiz_opts": {"ar": ["ثلاث مرات", "مرة واحدة", "خمس مرات"], "en": ["Three times", "Once", "Five times"]}},
    
    # Iman articles
    {"id": "iman_1", "emoji": "💎", "topic": "iman",
     "title": {"ar": "أركان الإيمان الستة", "en": "Six Pillars of Faith", "de": "Sechs Säulen des Glaubens", "fr": "Les six piliers de la foi", "tr": "İmanın Altı Şartı", "ru": "Шесть столпов веры", "sv": "Sex trossatser", "nl": "Zes zuilen van geloof", "el": "Έξι πυλώνες πίστης"},
     "content": {"ar": "أركان الإيمان الستة هي: ١- الإيمان بالله ٢- الإيمان بالملائكة ٣- الإيمان بالكتب السماوية ٤- الإيمان بالرسل ٥- الإيمان باليوم الآخر ٦- الإيمان بالقدر خيره وشره",
                 "en": "The Six Pillars of Faith: 1- Belief in Allah 2- Belief in Angels 3- Belief in Holy Books 4- Belief in Messengers 5- Belief in the Last Day 6- Belief in Divine Decree"},
     "memorize": {"ar": "الله - الملائكة - الكتب - الرسل - اليوم الآخر - القدر", "en": "Allah - Angels - Books - Messengers - Last Day - Decree"},
     "quiz_q": {"ar": "كم عدد أركان الإيمان؟", "en": "How many pillars of faith are there?"},
     "quiz_a": {"ar": "ستة", "en": "Six"},
     "quiz_opts": {"ar": ["ستة", "خمسة", "سبعة"], "en": ["Six", "Five", "Seven"]}},
    
    {"id": "iman_angels", "emoji": "👼", "topic": "iman",
     "title": {"ar": "الملائكة", "en": "The Angels", "de": "Die Engel", "fr": "Les Anges", "tr": "Melekler", "ru": "Ангелы", "sv": "Änglarna", "nl": "De Engelen", "el": "Οι Άγγελοι"},
     "content": {"ar": "الملائكة مخلوقات من نور، لا يعصون الله أبدًا. جبريل ينزل الوحي، ميكائيل مسؤول عن المطر والنبات، إسرافيل ينفخ في الصور، وملك الموت يقبض الأرواح. والملائكة الحفظة يكتبون أعمالنا.",
                 "en": "Angels are creatures of light who never disobey Allah. Jibreel delivers revelation, Mikael manages rain and plants, Israfeel will blow the horn, and the Angel of Death takes souls. Guardian angels record our deeds."},
     "memorize": {"ar": "جبريل: الوحي | ميكائيل: المطر | إسرافيل: الصور | ملك الموت: الأرواح", "en": "Jibreel: revelation | Mikael: rain | Israfeel: the horn | Angel of Death: souls"},
     "quiz_q": {"ar": "من الملك المسؤول عن الوحي؟", "en": "Which angel delivers revelation?"},
     "quiz_a": {"ar": "جبريل", "en": "Jibreel"},
     "quiz_opts": {"ar": ["جبريل", "ميكائيل", "إسرافيل"], "en": ["Jibreel", "Mikael", "Israfeel"]}},
    
    {"id": "iman_books", "emoji": "📚", "topic": "iman",
     "title": {"ar": "الكتب السماوية", "en": "The Holy Books", "de": "Die Heiligen Bücher", "fr": "Les Livres Saints", "tr": "Kutsal Kitaplar", "ru": "Священные Книги", "sv": "De Heliga Böckerna", "nl": "De Heilige Boeken", "el": "Τα Ιερά Βιβλία"},
     "content": {"ar": "أنزل الله كتبًا سماوية على أنبيائه: التوراة على موسى، الزبور على داود، الإنجيل على عيسى، والقرآن الكريم على محمد ﷺ. القرآن هو آخر الكتب وهو محفوظ إلى يوم القيامة.",
                 "en": "Allah revealed holy books to His prophets: The Torah to Musa, Zabur to Dawud, Injeel to Isa, and the Quran to Muhammad ﷺ. The Quran is the final book, preserved until the Day of Judgment."},
     "memorize": {"ar": "التوراة (موسى) - الزبور (داود) - الإنجيل (عيسى) - القرآن (محمد ﷺ)", "en": "Torah (Musa) - Zabur (Dawud) - Injeel (Isa) - Quran (Muhammad ﷺ)"},
     "quiz_q": {"ar": "على من أنزل الزبور؟", "en": "To whom was the Zabur revealed?"},
     "quiz_a": {"ar": "داود عليه السلام", "en": "Prophet Dawud"},
     "quiz_opts": {"ar": ["داود", "موسى", "عيسى"], "en": ["Dawud", "Musa", "Isa"]}},
    
    # Mosque etiquette
    {"id": "mosque_1", "emoji": "🕌", "topic": "mosque",
     "title": {"ar": "آداب المسجد", "en": "Mosque Etiquette", "de": "Moschee-Etikette", "fr": "Étiquette de la mosquée", "tr": "Cami Adabı", "ru": "Этикет мечети", "sv": "Moskéetikett", "nl": "Moskee-etiquette", "el": "Εθιμοτυπία τεμένους"},
     "content": {"ar": "عند دخول المسجد: ندخل بالقدم اليمنى ونقول دعاء الدخول. نصلي تحية المسجد ركعتين. لا نرفع صوتنا. لا نأكل في المسجد. نحافظ على نظافته. نخرج بالقدم اليسرى.",
                 "en": "When entering the mosque: Enter with the right foot and say the entrance dua. Pray two rak'ahs of greeting. Don't raise our voice. Don't eat in the mosque. Keep it clean. Exit with the left foot."},
     "memorize": {"ar": "الدخول باليمنى والدعاء - تحية المسجد - الهدوء - النظافة - الخروج باليسرى", "en": "Enter right foot with dua - greet mosque - quiet - clean - exit left foot"},
     "quiz_q": {"ar": "بأي قدم ندخل المسجد؟", "en": "Which foot do we enter the mosque with?"},
     "quiz_a": {"ar": "القدم اليمنى", "en": "The right foot"},
     "quiz_opts": {"ar": ["القدم اليمنى", "القدم اليسرى", "لا فرق"], "en": ["Right foot", "Left foot", "Doesn't matter"]}},
    
    # Islamic Greetings
    {"id": "greetings_1", "emoji": "👋", "topic": "greetings",
     "title": {"ar": "التحية في الإسلام", "en": "Islamic Greetings", "de": "Islamische Begrüßung", "fr": "Salutations islamiques", "tr": "İslami Selamlaşma", "ru": "Исламское приветствие", "sv": "Islamiska hälsningar", "nl": "Islamitische groet", "el": "Ισλαμικοί χαιρετισμοί"},
     "content": {"ar": "السلام عليكم ورحمة الله وبركاته هي أفضل تحية. عندما يسلم عليك أحد، تقول: وعليكم السلام ورحمة الله وبركاته. تحية الإسلام تنشر المحبة والسلام بين الناس.",
                 "en": "Assalamu Alaikum wa Rahmatullahi wa Barakatuh is the best greeting. When someone greets you, respond: Wa Alaikum Assalam wa Rahmatullahi wa Barakatuh. The Islamic greeting spreads love and peace among people."},
     "memorize": {"ar": "السلام عليكم ورحمة الله وبركاته", "en": "Assalamu Alaikum wa Rahmatullahi wa Barakatuh"},
     "quiz_q": {"ar": "ما أفضل تحية في الإسلام؟", "en": "What is the best greeting in Islam?"},
     "quiz_a": {"ar": "السلام عليكم ورحمة الله وبركاته", "en": "Assalamu Alaikum"},
     "quiz_opts": {"ar": ["السلام عليكم", "صباح الخير", "مرحبًا"], "en": ["Assalamu Alaikum", "Good morning", "Hello"]}},
    
    # Quran intro
    {"id": "quran_1", "emoji": "📖", "topic": "quran",
     "title": {"ar": "القرآن الكريم", "en": "The Holy Quran", "de": "Der Heilige Quran", "fr": "Le Saint Coran", "tr": "Kur'an-ı Kerim", "ru": "Священный Коран", "sv": "Den Heliga Koranen", "nl": "De Heilige Koran", "el": "Το Ιερό Κοράνι"},
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
     "title": {"ar": "بر الوالدين", "en": "Honoring Parents", "de": "Eltern ehren", "fr": "Honorer les parents", "tr": "Anne Babaya İyilik", "ru": "Почитание родителей", "sv": "Hedra föräldrarna", "nl": "Ouders eren", "el": "Τιμή στους γονείς"},
     "content": {"ar": "بر الوالدين من أعظم العبادات. قال الله تعالى: وقضى ربك ألا تعبدوا إلا إياه وبالوالدين إحسانًا. نطيع والدينا، نساعدهما، لا نرفع صوتنا عليهما، وندعو لهما: رب ارحمهما كما ربياني صغيرًا.",
                 "en": "Honoring parents is one of the greatest acts of worship. Allah said: Your Lord has decreed that you worship none but Him, and be good to parents. We obey our parents, help them, don't raise our voice, and pray for them."},
     "memorize": {"ar": "رَبِّ ارْحَمْهُمَا كَمَا رَبَّيَانِي صَغِيرًا", "en": "My Lord, have mercy upon them as they brought me up when I was small"},
     "quiz_q": {"ar": "ما هو دعاء الوالدين؟", "en": "What is the dua for parents?"},
     "quiz_a": {"ar": "رب ارحمهما كما ربياني صغيرا", "en": "My Lord, have mercy upon them"},
     "quiz_opts": {"ar": ["رب ارحمهما كما ربياني صغيرا", "رب اغفر لي", "ربنا آتنا في الدنيا حسنة"], "en": ["My Lord have mercy upon them", "Lord forgive me", "Lord give us good"]}},
    
    # Kindness to animals
    {"id": "animals_1", "emoji": "🐱", "topic": "animals",
     "title": {"ar": "الرفق بالحيوان", "en": "Kindness to Animals", "de": "Freundlichkeit zu Tieren", "fr": "Bonté envers les animaux", "tr": "Hayvanlara İyilik", "ru": "Доброта к животным", "sv": "Vänlighet mot djur", "nl": "Vriendelijkheid voor dieren", "el": "Καλοσύνη προς τα ζώα"},
     "content": {"ar": "الإسلام يأمرنا بالرفق بالحيوانات. قال النبي ﷺ إن امرأة دخلت النار بسبب قطة حبستها ولم تطعمها. وامرأة أخرى دخلت الجنة لأنها سقت كلبًا عطشان. الرفق بالحيوان عبادة!",
                 "en": "Islam commands us to be kind to animals. The Prophet ﷺ said a woman entered Hell for imprisoning a cat without feeding it. Another woman entered Paradise for giving water to a thirsty dog. Kindness to animals is worship!"},
     "memorize": {"ar": "في كل ذات كبد رطبة أجر - حديث نبوي", "en": "There is reward for every living creature - Prophetic hadith"},
     "quiz_q": {"ar": "لماذا دخلت المرأة الجنة؟", "en": "Why did the woman enter Paradise?"},
     "quiz_a": {"ar": "لأنها سقت كلبًا عطشان", "en": "She gave water to a thirsty dog"},
     "quiz_opts": {"ar": ["سقت كلبًا عطشان", "صلت كثيرًا", "صامت كثيرًا"], "en": ["Gave water to a dog", "Prayed a lot", "Fasted a lot"]}},
    
    # Truthfulness
    {"id": "sidq_1", "emoji": "⭐", "topic": "truthfulness",
     "title": {"ar": "الصدق في الإسلام", "en": "Truthfulness in Islam", "de": "Wahrhaftigkeit im Islam", "fr": "La véracité en Islam", "tr": "İslam'da Doğruluk", "ru": "Правдивость в Исламе", "sv": "Sanningsenlighet i Islam", "nl": "Oprechtheid in de Islam", "el": "Αλήθεια στο Ισλάμ"},
     "content": {"ar": "الصدق من أهم الأخلاق في الإسلام. قال النبي ﷺ: عليكم بالصدق فإن الصدق يهدي إلى البر والبر يهدي إلى الجنة. وإياكم والكذب فإن الكذب يهدي إلى الفجور والفجور يهدي إلى النار.",
                 "en": "Truthfulness is one of the most important traits in Islam. The Prophet ﷺ said: Be truthful, for truthfulness leads to righteousness and righteousness leads to Paradise. Beware of lying, for lying leads to wickedness and wickedness leads to the Fire."},
     "memorize": {"ar": "عليكم بالصدق فإن الصدق يهدي إلى البر", "en": "Be truthful, truthfulness leads to righteousness"},
     "quiz_q": {"ar": "إلى أين يهدي الصدق؟", "en": "Where does truthfulness lead?"},
     "quiz_a": {"ar": "إلى البر والجنة", "en": "To righteousness and Paradise"},
     "quiz_opts": {"ar": ["البر والجنة", "المال", "الشهرة"], "en": ["Righteousness and Paradise", "Wealth", "Fame"]}},
    
    # Cleanliness
    {"id": "tahara_1", "emoji": "🧼", "topic": "cleanliness",
     "title": {"ar": "النظافة في الإسلام", "en": "Cleanliness in Islam", "de": "Sauberkeit im Islam", "fr": "La propreté en Islam", "tr": "İslam'da Temizlik", "ru": "Чистота в Исламе", "sv": "Renlighet i Islam", "nl": "Reinheid in de Islam", "el": "Καθαριότητα στο Ισλάμ"},
     "content": {"ar": "النظافة من الإيمان. قال النبي ﷺ: الطهور شطر الإيمان. نغسل أيدينا قبل الأكل وبعده، ننظف أسناننا بالسواك، نقص أظافرنا، ونلبس ملابس نظيفة. الإسلام دين النظافة.",
                 "en": "Cleanliness is part of faith. The Prophet ﷺ said: Cleanliness is half of faith. We wash hands before and after eating, clean teeth with miswak, trim nails, and wear clean clothes. Islam is the religion of cleanliness."},
     "memorize": {"ar": "الطُّهورُ شَطرُ الإيمانِ - حديث نبوي", "en": "Cleanliness is half of faith - Prophetic hadith"},
     "quiz_q": {"ar": "ماذا قال النبي ﷺ عن الطهور؟", "en": "What did the Prophet ﷺ say about cleanliness?"},
     "quiz_a": {"ar": "شطر الإيمان", "en": "Half of faith"},
     "quiz_opts": {"ar": ["شطر الإيمان", "ربع الإيمان", "كل الإيمان"], "en": ["Half of faith", "Quarter of faith", "All of faith"]}},
    
    # Dhikr
    {"id": "dhikr_1", "emoji": "📿", "topic": "dhikr",
     "title": {"ar": "ذكر الله", "en": "Remembrance of Allah", "de": "Gedenken Allahs", "fr": "Le rappel d'Allah", "tr": "Allah'ı Anma", "ru": "Поминание Аллаха", "sv": "Åminnelse av Allah", "nl": "Gedenken van Allah", "el": "Μνήμη του Αλλάχ"},
     "content": {"ar": "ذكر الله يملأ القلب سكينة وطمأنينة. من أهم الأذكار: سبحان الله، الحمد لله، الله أكبر، لا إله إلا الله، أستغفر الله. قال الله: ألا بذكر الله تطمئن القلوب.",
                 "en": "Remembering Allah fills the heart with peace and tranquility. Important dhikr: SubhanAllah, Alhamdulillah, Allahu Akbar, La ilaha illallah, Astaghfirullah. Allah said: Surely in the remembrance of Allah hearts find peace."},
     "memorize": {"ar": "أَلَا بِذِكْرِ اللَّهِ تَطْمَئِنُّ الْقُلُوبُ", "en": "Surely in the remembrance of Allah hearts find peace"},
     "quiz_q": {"ar": "بماذا تطمئن القلوب؟", "en": "What gives hearts peace?"},
     "quiz_a": {"ar": "بذكر الله", "en": "Remembrance of Allah"},
     "quiz_opts": {"ar": ["ذكر الله", "المال", "اللعب"], "en": ["Remembrance of Allah", "Money", "Playing"]}},
    
    # Charity and helping others
    {"id": "sadaqah_1", "emoji": "🤝", "topic": "sadaqah",
     "title": {"ar": "الصدقة والإحسان", "en": "Charity and Kindness", "de": "Wohltätigkeit und Güte", "fr": "La charité et la bonté", "tr": "Sadaka ve İyilik", "ru": "Милосердие и доброта", "sv": "Välgörenhet och vänlighet", "nl": "Liefdadigheid en goedheid", "el": "Φιλανθρωπία και καλοσύνη"},
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
    {"emoji": "🌙", "title": {"ar": "رمضان - شهر الخير", "en": "Ramadan - Month of Goodness", "de": "Ramadan - Monat des Guten", "fr": "Ramadan - Mois de bonté", "tr": "Ramazan - Hayır Ayı", "ru": "Рамадан - Месяц добра", "sv": "Ramadan - Godhetens månad", "nl": "Ramadan - Maand van goedheid", "el": "Ραμαντάν - Μήνας καλοσύνης"},
     "content": {"ar": "رمضان شهر مبارك نصوم فيه ونقرأ القرآن ونتقرب إلى الله. فيه ليلة القدر التي هي خير من ألف شهر. نفطر على التمر والماء ونصلي التراويح.",
                 "en": "Ramadan is a blessed month of fasting, Quran reading and getting closer to Allah. It contains Laylatul Qadr which is better than a thousand months. We break fast with dates and water and pray Taraweeh."}},
    {"emoji": "🕋", "title": {"ar": "الحج - رحلة العمر", "en": "Hajj - Journey of a Lifetime", "de": "Hadsch - Reise des Lebens", "fr": "Le Hajj - Voyage d'une vie", "tr": "Hac - Ömürlük Yolculuk", "ru": "Хадж - Путешествие всей жизни", "sv": "Hajj - Livets resa", "nl": "Hadj - Reis van een leven", "el": "Χατζ - Ταξίδι ζωής"},
     "content": {"ar": "ملايين المسلمين يذهبون إلى مكة كل عام لأداء الحج. يلبسون الإحرام الأبيض ويطوفون حول الكعبة ويقفون بعرفة ويرمون الجمرات.",
                 "en": "Millions of Muslims go to Makkah every year for Hajj. They wear white ihram, circle the Kaaba, stand at Arafat and throw pebbles at the Jamarat."}},
    {"emoji": "🎉", "title": {"ar": "عيد الفطر - فرحة المسلمين", "en": "Eid Al-Fitr - Muslim Celebration", "de": "Eid Al-Fitr - Muslimisches Fest", "fr": "Aïd Al-Fitr - Fête musulmane", "tr": "Ramazan Bayramı", "ru": "Ид аль-Фитр - Мусульманский праздник", "sv": "Eid Al-Fitr - Muslimsk högtid", "nl": "Eid Al-Fitr - Moslimfeest", "el": "Εΐντ Αλ-Φιτρ - Μουσουλμανική γιορτή"},
     "content": {"ar": "عيد الفطر يأتي بعد رمضان. نغتسل ونلبس أحسن الثياب. نصلي صلاة العيد ونكبر. نزور الأقارب ونتبادل التهاني ونأكل الحلويات. ونخرج زكاة الفطر قبل الصلاة.",
                 "en": "Eid Al-Fitr comes after Ramadan. We bathe and wear best clothes. We pray Eid prayer and say takbeer. We visit relatives, exchange greetings and eat sweets. We pay Zakat al-Fitr before the prayer."}},
    {"emoji": "🐑", "title": {"ar": "عيد الأضحى", "en": "Eid Al-Adha", "de": "Eid Al-Adha", "fr": "Aïd Al-Adha", "tr": "Kurban Bayramı", "ru": "Ид аль-Адха", "sv": "Eid Al-Adha", "nl": "Eid Al-Adha", "el": "Εΐντ Αλ-Άντχα"},
     "content": {"ar": "عيد الأضحى يوم عظيم نتذكر فيه قصة إبراهيم وإسماعيل عليهما السلام. نصلي صلاة العيد ونذبح الأضحية ونوزعها: ثلث لنا وثلث للأقارب وثلث للفقراء.",
                 "en": "Eid Al-Adha is a great day when we remember the story of Ibrahim and Ismail. We pray Eid prayer, sacrifice an animal and distribute: a third for us, a third for relatives and a third for the poor."}},
    {"emoji": "🕌", "title": {"ar": "يوم الجمعة", "en": "Friday", "de": "Freitag", "fr": "Le Vendredi", "tr": "Cuma Günü", "ru": "Пятница", "sv": "Fredagen", "nl": "Vrijdag", "el": "Παρασκευή"},
     "content": {"ar": "يوم الجمعة هو سيد الأيام وأفضلها. فيه خلق آدم وفيه ساعة إجابة. نغتسل ونتطيب ونلبس أحسن الثياب. نذهب مبكرًا للمسجد ونصلي صلاة الجمعة ونسمع الخطبة.",
                 "en": "Friday is the master and best of days. Adam was created on it and there is a special hour of acceptance. We bathe, wear perfume and best clothes. We go early to the mosque for Jumu'ah prayer and listen to the sermon."}},
    {"emoji": "🌟", "title": {"ar": "ليلة القدر", "en": "Laylatul Qadr", "de": "Laylatul Qadr", "fr": "La Nuit du Destin", "tr": "Kadir Gecesi", "ru": "Ляйлятуль-Кадр", "sv": "Laylatul Qadr", "nl": "Laylatul Qadr", "el": "Λάιλατουλ Κάντρ"},
     "content": {"ar": "ليلة القدر خير من ألف شهر. هي الليلة التي نزل فيها القرآن. نبحث عنها في العشر الأواخر من رمضان. نقوم الليل وندعو: اللهم إنك عفو تحب العفو فاعف عني.",
                 "en": "Laylatul Qadr is better than a thousand months. It is the night the Quran was revealed. We look for it in the last ten nights of Ramadan. We pray at night and make dua: O Allah, You are forgiving and love forgiveness, so forgive me."}},
    {"emoji": "📅", "title": {"ar": "يوم عاشوراء", "en": "Day of Ashura", "de": "Tag von Ashura", "fr": "Le jour d'Achoura", "tr": "Aşure Günü", "ru": "День Ашура", "sv": "Ashura-dagen", "nl": "Dag van Ashura", "el": "Ημέρα Ασούρα"},
     "content": {"ar": "يوم عاشوراء هو العاشر من محرم. في هذا اليوم نجّى الله موسى وقومه من فرعون. صامه النبي ﷺ وأمرنا بصيامه. من صامه يُكفّر عنه ذنوب سنة ماضية.",
                 "en": "Ashura is the 10th of Muharram. On this day Allah saved Musa and his people from Pharaoh. The Prophet ﷺ fasted it and told us to fast it. Fasting it expiates sins of the previous year."}},
    {"emoji": "🕋", "title": {"ar": "الكعبة المشرفة", "en": "The Holy Kaaba", "de": "Die Heilige Kaaba", "fr": "La Sainte Kaaba", "tr": "Kâbe-i Muazzama", "ru": "Священная Кааба", "sv": "Den Heliga Kaaba", "nl": "De Heilige Kaaba", "el": "Η Ιερή Κάαμπα"},
     "content": {"ar": "الكعبة هي أول بيت وُضع للناس. بناها إبراهيم وإسماعيل عليهما السلام. فيها الحجر الأسود. نتوجه إليها في صلاتنا. هي قبلة المسلمين في كل مكان في العالم.",
                 "en": "The Kaaba is the first house built for people. Ibrahim and Ismail built it. It contains the Black Stone. We face it in our prayer. It is the qibla of Muslims everywhere in the world."}},
    {"emoji": "🕌", "title": {"ar": "المسجد الحرام", "en": "Al-Masjid Al-Haram", "de": "Al-Masjid Al-Haram", "fr": "La Mosquée Sacrée", "tr": "Mescid-i Haram", "ru": "Аль-Масджид аль-Харам", "sv": "Al-Masjid Al-Haram", "nl": "Al-Masjid Al-Haram", "el": "Αλ-Μάσγιντ Αλ-Χαράμ"},
     "content": {"ar": "المسجد الحرام في مكة المكرمة هو أعظم مسجد. فيه الكعبة وبئر زمزم ومقام إبراهيم. الصلاة فيه بمئة ألف صلاة. يأتيه الحجاج والمعتمرون من كل أنحاء العالم.",
                 "en": "Al-Masjid Al-Haram in Makkah is the greatest mosque. It contains the Kaaba, Well of Zamzam and Ibrahim's station. Prayer in it equals 100,000 prayers. Pilgrims come from all over the world."}},
    {"emoji": "🟢", "title": {"ar": "المسجد النبوي", "en": "Prophet's Mosque", "de": "Prophetenmoschee", "fr": "La Mosquée du Prophète", "tr": "Mescid-i Nebevi", "ru": "Мечеть Пророка", "sv": "Profetens Moské", "nl": "De Moskee van de Profeet", "el": "Τέμενος του Προφήτη"},
     "content": {"ar": "المسجد النبوي في المدينة المنورة بناه النبي ﷺ. فيه قبر النبي ﷺ والروضة الشريفة. الصلاة فيه بألف صلاة. المدينة المنورة هي مدينة الرسول ﷺ.",
                 "en": "The Prophet's Mosque in Madinah was built by the Prophet ﷺ. It contains the Prophet's grave and the Rawdah. Prayer in it equals 1,000 prayers. Madinah is the city of the Messenger ﷺ."}},
    {"emoji": "🟡", "title": {"ar": "المسجد الأقصى", "en": "Al-Aqsa Mosque", "de": "Al-Aqsa-Moschee", "fr": "La Mosquée Al-Aqsa", "tr": "Mescid-i Aksa", "ru": "Мечеть Аль-Акса", "sv": "Al-Aqsa-moskén", "nl": "Al-Aqsa-moskee", "el": "Τέμενος Αλ-Άκσα"},
     "content": {"ar": "المسجد الأقصى في القدس هو أولى القبلتين وثالث الحرمين. أسري بالنبي ﷺ إليه ليلة المعراج. الصلاة فيه بخمسمئة صلاة. فلسطين أرض مباركة.",
                 "en": "Al-Aqsa Mosque in Jerusalem was the first qibla and third holiest mosque. The Prophet ﷺ was taken there on the Night Journey. Prayer in it equals 500 prayers. Palestine is a blessed land."}},
    {"emoji": "✨", "title": {"ar": "الإسراء والمعراج", "en": "The Night Journey & Ascension", "de": "Die Nachtreise und Himmelfahrt", "fr": "Le Voyage Nocturne et l'Ascension", "tr": "İsra ve Miraç", "ru": "Ночное путешествие и Вознесение", "sv": "Nattresan och Himmelsfärden", "nl": "De Nachtreis en Hemelvaart", "el": "Το Νυχτερινό Ταξίδι και η Ανάληψη"},
     "content": {"ar": "في ليلة مباركة، أسري بالنبي ﷺ من المسجد الحرام إلى المسجد الأقصى على البراق. ثم عرج إلى السماوات السبع حيث فرضت الصلوات الخمس. التقى بالأنبياء ورأى آيات الله العظيمة.",
                 "en": "On a blessed night, the Prophet ﷺ was taken from Al-Masjid Al-Haram to Al-Aqsa on the Buraq. Then he ascended through seven heavens where the five prayers were ordained. He met the prophets and saw Allah's great signs."}},
    {"emoji": "📆", "title": {"ar": "رأس السنة الهجرية", "en": "Islamic New Year", "de": "Islamisches Neujahr", "fr": "Nouvel An islamique", "tr": "Hicri Yılbaşı", "ru": "Исламский Новый год", "sv": "Islamiskt nyår", "nl": "Islamitisch Nieuwjaar", "el": "Ισλαμική Πρωτοχρονιά"},
     "content": {"ar": "رأس السنة الهجرية في أول محرم. التقويم الهجري يبدأ من هجرة النبي ﷺ من مكة إلى المدينة. هذه الهجرة كانت حدثًا عظيمًا غيّر تاريخ الإسلام.",
                 "en": "Islamic New Year is on the 1st of Muharram. The Hijri calendar starts from the Prophet's migration from Makkah to Madinah. This migration was a great event that changed Islamic history."}},
    {"emoji": "🕊️", "title": {"ar": "السلام في الإسلام", "en": "Peace in Islam", "de": "Frieden im Islam", "fr": "La paix en Islam", "tr": "İslam'da Barış", "ru": "Мир в Исламе", "sv": "Fred i Islam", "nl": "Vrede in de Islam", "el": "Ειρήνη στο Ισλάμ"},
     "content": {"ar": "الإسلام دين السلام. كلمة الإسلام من السلام. تحيتنا: السلام عليكم. الجنة دار السلام. الله هو السلام. نحن نحب السلام ونعيش مع الجميع بسلام واحترام.",
                 "en": "Islam is the religion of peace. The word Islam comes from peace. Our greeting: Peace be upon you. Paradise is the abode of peace. Allah is Peace. We love peace and live with everyone in peace and respect."}},
    {"emoji": "🌳", "title": {"ar": "البيئة في الإسلام", "en": "Environment in Islam", "de": "Umwelt im Islam", "fr": "L'environnement en Islam", "tr": "İslam'da Çevre", "ru": "Окружающая среда в Исламе", "sv": "Miljön i Islam", "nl": "Milieu in de Islam", "el": "Περιβάλλον στο Ισλάμ"},
     "content": {"ar": "الإسلام يأمرنا بالمحافظة على البيئة. قال النبي ﷺ: إذا قامت الساعة وفي يد أحدكم فسيلة فليغرسها. نزرع الأشجار، لا نلوث الماء، ولا نفسد الأرض. نحن خلفاء الله في الأرض.",
                 "en": "Islam commands us to protect the environment. The Prophet ﷺ said: If the Hour comes while you have a seedling, plant it. We plant trees, don't pollute water, and don't corrupt the earth. We are Allah's stewards on Earth."}},
    {"emoji": "🎓", "title": {"ar": "طلب العلم في الإسلام", "en": "Seeking Knowledge in Islam", "de": "Wissen suchen im Islam", "fr": "La quête du savoir en Islam", "tr": "İslam'da İlim", "ru": "Стремление к знаниям в Исламе", "sv": "Sökande av kunskap i Islam", "nl": "Kennis zoeken in de Islam", "el": "Αναζήτηση γνώσης στο Ισλάμ"},
     "content": {"ar": "طلب العلم فريضة على كل مسلم ومسلمة. قال النبي ﷺ: اطلبوا العلم من المهد إلى اللحد. وأول آية نزلت من القرآن: اقرأ. العلم نور يضيء حياتنا.",
                 "en": "Seeking knowledge is obligatory for every Muslim. The Prophet ﷺ said: Seek knowledge from the cradle to the grave. The first revealed Quran verse was: Read. Knowledge is a light that brightens our lives."}},
    {"emoji": "🤝", "title": {"ar": "حقوق الجار", "en": "Rights of Neighbors", "de": "Rechte der Nachbarn", "fr": "Les droits des voisins", "tr": "Komşu Hakları", "ru": "Права соседей", "sv": "Grannars rättigheter", "nl": "Rechten van buren", "el": "Δικαιώματα γειτόνων"},
     "content": {"ar": "للجار حقوق كثيرة في الإسلام. قال النبي ﷺ: ما زال جبريل يوصيني بالجار حتى ظننت أنه سيورثه. نحسن إلى جيراننا، لا نؤذيهم، نطعمهم إذا جاعوا، ونزورهم إذا مرضوا.",
                 "en": "Neighbors have many rights in Islam. The Prophet ﷺ said: Jibreel kept advising me about neighbors until I thought he would make them heirs. We are good to neighbors, don't harm them, feed them if hungry, visit them if sick."}},
    {"emoji": "📿", "title": {"ar": "الاستغفار", "en": "Seeking Forgiveness", "de": "Vergebung suchen", "fr": "Demander le pardon", "tr": "İstiğfar", "ru": "Покаяние", "sv": "Söka förlåtelse", "nl": "Vergeving zoeken", "el": "Αίτηση συγχώρεσης"},
     "content": {"ar": "الاستغفار يمحو الذنوب ويجلب الرزق والراحة. كان النبي ﷺ يستغفر الله في اليوم أكثر من سبعين مرة. ندعو: أستغفر الله العظيم الذي لا إله إلا هو الحي القيوم وأتوب إليه.",
                 "en": "Seeking forgiveness erases sins and brings provision and peace. The Prophet ﷺ used to seek forgiveness more than 70 times a day. We say: Astaghfirullah al-Adheem - I seek forgiveness from Allah the Almighty."}},
    {"emoji": "💐", "title": {"ar": "المولد النبوي الشريف", "en": "The Prophet's Birthday", "de": "Geburtstag des Propheten", "fr": "La naissance du Prophète", "tr": "Mevlid Kandili", "ru": "День рождения Пророка", "sv": "Profetens födelsedag", "nl": "Geboortedag van de Profeet", "el": "Γενέθλια του Προφήτη"},
     "content": {"ar": "وُلد النبي محمد ﷺ في ربيع الأول في مكة المكرمة. كان يتيمًا رعاه جده عبد المطلب ثم عمه أبو طالب. نشأ أمينًا صادقًا حتى لقبه قومه بالصادق الأمين.",
                 "en": "Prophet Muhammad ﷺ was born in Rabi al-Awwal in Makkah. He was an orphan raised by his grandfather Abdul-Muttalib then his uncle Abu Talib. He grew up honest and truthful, earning the title Al-Amin (The Trustworthy)."}},
]

# ═══════════════════════════════════════════════════════════════
# STAGE 13: ADVANCED ARABIC - Grammar, Verbs, Conversations
# ═══════════════════════════════════════════════════════════════

ARABIC_GRAMMAR_LESSONS = [
    # Noun types
    {"id": "g01", "emoji": "📝", "title": {"ar": "الاسم المفرد والمثنى والجمع", "en": "Singular, Dual and Plural", "de": "Einzahl, Zweizahl und Mehrzahl", "fr": "Singulier, duel et pluriel", "tr": "Tekil, İkil ve Çoğul", "ru": "Единственное, двойственное и множественное", "sv": "Singular, dual och plural", "nl": "Enkelvoud, tweevoud en meervoud", "el": "Ενικός, δυϊκός και πληθυντικός"},
     "content": {"ar": "المفرد: كتاب (واحد) | المثنى: كتابان (اثنان) | الجمع: كتب (أكثر من اثنين). تمارين: ولد→ ولدان→ أولاد | بنت→ بنتان→ بنات | معلم→ معلمان→ معلمون",
                 "en": "Singular: kitab (one) | Dual: kitaban (two) | Plural: kutub (more than two). Practice: walad→ waladan→ awlad | bint→ bintan→ banat | mu'allim→ mu'alliman→ mu'allimun"},
     "practice": [
         {"word": "مسجد", "dual": "مسجدان", "plural": "مساجد"},
         {"word": "سورة", "dual": "سورتان", "plural": "سور"},
         {"word": "نبي", "dual": "نبيّان", "plural": "أنبياء"},
     ]},
    # Verb tenses
    {"id": "g02", "emoji": "🔤", "title": {"ar": "الفعل الماضي والمضارع والأمر", "en": "Past, Present and Command", "de": "Vergangenheit, Gegenwart und Befehl", "fr": "Passé, présent et impératif", "tr": "Geçmiş, Şimdiki ve Emir", "ru": "Прошедшее, настоящее и повелительное", "sv": "Förflutet, nutid och imperativ", "nl": "Verleden, heden en gebiedend", "el": "Παρελθόν, παρόν και προστακτική"},
     "content": {"ar": "الماضي: كَتَبَ (فعل حدث وانتهى) | المضارع: يَكتُبُ (فعل يحدث الآن) | الأمر: اُكتُبْ (طلب فعل شيء). تمارين: قرأ→ يقرأ→ اقرأ | صلّى→ يصلي→ صَلِّ | ذهب→ يذهب→ اذهب",
                 "en": "Past: kataba (happened and finished) | Present: yaktub (happening now) | Command: uktub (request to do). Practice: qara'a→ yaqra'→ iqra' | salla→ yusalli→ salli | dhahaba→ yadhhab→ idhhab"},
     "practice": [
         {"past": "أكَلَ", "present": "يَأكُلُ", "command": "كُلْ", "en": "ate/eats/eat"},
         {"past": "شَرِبَ", "present": "يَشرَبُ", "command": "اِشرَبْ", "en": "drank/drinks/drink"},
         {"past": "نَامَ", "present": "يَنامُ", "command": "نَمْ", "en": "slept/sleeps/sleep"},
     ]},
    # Pronouns
    {"id": "g03", "emoji": "👤", "title": {"ar": "الضمائر", "en": "Pronouns", "de": "Pronomen", "fr": "Pronoms", "tr": "Zamirler", "ru": "Местоимения", "sv": "Pronomen", "nl": "Voornaamwoorden", "el": "Αντωνυμίες"},
     "content": {"ar": "أنا (متكلم) | أنتَ/أنتِ (مخاطب) | هو/هي (غائب) | نحن (جمع المتكلمين) | أنتم (جمع المخاطبين) | هم (جمع الغائبين)",
                 "en": "Ana (I) | Anta/Anti (you m/f) | Huwa/Hiya (he/she) | Nahnu (we) | Antum (you pl) | Hum (they)"},
     "practice": [
         {"pronoun": "أنا", "example": "أنا مسلم", "en": "I am a Muslim"},
         {"pronoun": "هو", "example": "هو يصلي", "en": "He is praying"},
         {"pronoun": "نحن", "example": "نحن نحب القرآن", "en": "We love the Quran"},
     ]},
    # Question words
    {"id": "g04", "emoji": "❓", "title": {"ar": "أدوات الاستفهام", "en": "Question Words", "de": "Fragewörter", "fr": "Mots interrogatifs", "tr": "Soru Kelimeleri", "ru": "Вопросительные слова", "sv": "Frågeord", "nl": "Vraagwoorden", "el": "Ερωτηματικές λέξεις"},
     "content": {"ar": "مَن؟ (للسؤال عن الشخص) | ما/ماذا؟ (للسؤال عن الشيء) | أين؟ (للمكان) | متى؟ (للزمان) | كيف؟ (للحال) | لماذا؟ (للسبب) | كم؟ (للعدد)",
                 "en": "Man? (who) | Ma/Madha? (what) | Ayna? (where) | Mata? (when) | Kayf? (how) | Limadha? (why) | Kam? (how many)"},
     "practice": [
         {"question": "مَن النبي الأخير؟", "answer": "محمد ﷺ", "en": "Who is the last prophet?"},
         {"question": "أين الكعبة؟", "answer": "في مكة المكرمة", "en": "Where is the Kaaba?"},
         {"question": "كم صلاة في اليوم؟", "answer": "خمس صلوات", "en": "How many prayers per day?"},
     ]},
    # Prepositions
    {"id": "g05", "emoji": "📍", "title": {"ar": "حروف الجر", "en": "Prepositions", "de": "Präpositionen", "fr": "Prépositions", "tr": "Edatlar", "ru": "Предлоги", "sv": "Prepositioner", "nl": "Voorzetsels", "el": "Προθέσεις"},
     "content": {"ar": "في (inside) | على (on) | من (from) | إلى (to) | عن (about) | ب (with/by) | ل (for). مثال: ذهبتُ إلى المسجدِ - صليتُ في المسجدِ - رجعتُ من المسجدِ",
                 "en": "Fi (in) | Ala (on) | Min (from) | Ila (to) | An (about) | Bi (with) | Li (for). Example: I went to the mosque - I prayed in the mosque - I returned from the mosque"},
     "practice": [
         {"sentence": "الكتابُ على الطاولةِ", "en": "The book is on the table"},
         {"sentence": "ذهبنا إلى المدرسةِ", "en": "We went to school"},
         {"sentence": "خرجنا من البيتِ", "en": "We left from the house"},
     ]},
    # Conversations
    {"id": "g06", "emoji": "💬", "title": {"ar": "محادثة: في المسجد", "en": "Conversation: At the Mosque", "de": "Gespräch: In der Moschee", "fr": "Conversation: À la mosquée", "tr": "Konuşma: Camide", "ru": "Диалог: В мечети", "sv": "Samtal: I moskén", "nl": "Gesprek: In de moskee", "el": "Συνομιλία: Στο τέμενος"},
     "content": {"ar": "أحمد: السلام عليكم يا عم!\nالعم: وعليكم السلام يا بُني! كيف حالك؟\nأحمد: الحمد لله بخير. هل صلاة المغرب قريبة؟\nالعم: نعم، بعد خمس دقائق إن شاء الله.\nأحمد: جزاك الله خيرًا.",
                 "en": "Ahmad: Assalamu alaikum uncle!\nUncle: Wa alaikum assalam son! How are you?\nAhmad: Alhamdulillah fine. Is Maghrib prayer soon?\nUncle: Yes, in five minutes inshaAllah.\nAhmad: JazakAllah khairan."},
     "practice": []},
    {"id": "g07", "emoji": "💬", "title": {"ar": "محادثة: في المدرسة", "en": "Conversation: At School", "de": "Gespräch: In der Schule", "fr": "Conversation: À l'école", "tr": "Konuşma: Okulda", "ru": "Диалог: В школе", "sv": "Samtal: I skolan", "nl": "Gesprek: Op school", "el": "Συνομιλία: Στο σχολείο"},
     "content": {"ar": "المعلم: صباح الخير يا طلاب!\nالطلاب: صباح النور يا أستاذ!\nالمعلم: اليوم نتعلم سورة جديدة. افتحوا المصحف.\nسارة: أي سورة يا أستاذ؟\nالمعلم: سورة الفلق. هيا نقرأ معًا.",
                 "en": "Teacher: Good morning students!\nStudents: Good morning teacher!\nTeacher: Today we learn a new surah. Open the Quran.\nSara: Which surah, teacher?\nTeacher: Surah Al-Falaq. Let's read together."},
     "practice": []},
    {"id": "g08", "emoji": "💬", "title": {"ar": "محادثة: في رمضان", "en": "Conversation: In Ramadan", "de": "Gespräch: Im Ramadan", "fr": "Conversation: En Ramadan", "tr": "Konuşma: Ramazan'da", "ru": "Диалог: В Рамадан", "sv": "Samtal: Under Ramadan", "nl": "Gesprek: In Ramadan", "el": "Συνομιλία: Στο Ραμαντάν"},
     "content": {"ar": "الأم: هل أنت صائم اليوم يا أحمد؟\nأحمد: نعم يا أمي! أنا صائم والحمد لله.\nالأم: ما شاء الله! ماذا تريد للإفطار؟\nأحمد: تمرًا وحليبًا من فضلك.\nالأم: حاضر. بارك الله فيك يا بُني.",
                 "en": "Mom: Are you fasting today Ahmad?\nAhmad: Yes mom! I'm fasting alhamdulillah.\nMom: MashaAllah! What do you want for iftar?\nAhmad: Dates and milk please.\nMom: Of course. May Allah bless you son."},
     "practice": []},
    # Adjectives
    {"id": "g09", "emoji": "🎨", "title": {"ar": "الصفات", "en": "Adjectives", "de": "Adjektive", "fr": "Adjectifs", "tr": "Sıfatlar", "ru": "Прилагательные", "sv": "Adjektiv", "nl": "Bijvoeglijke naamwoorden", "el": "Επίθετα"},
     "content": {"ar": "كبير↔صغير | طويل↔قصير | جميل↔قبيح | سريع↔بطيء | قوي↔ضعيف | حار↔بارد | جديد↔قديم | سعيد↔حزين. الصفة تتبع الموصوف: المسجد الكبير، البنت الجميلة.",
                 "en": "Big↔Small | Tall↔Short | Beautiful↔Ugly | Fast↔Slow | Strong↔Weak | Hot↔Cold | New↔Old | Happy↔Sad. Adjective follows the noun: the big mosque, the beautiful girl."},
     "practice": [
         {"word": "كبير", "opposite": "صغير", "example": "المسجد كبير"},
         {"word": "جميل", "opposite": "قبيح", "example": "القرآن جميل"},
         {"word": "سعيد", "opposite": "حزين", "example": "أنا سعيد"},
     ]},
    # Days of the week
    {"id": "g10", "emoji": "📅", "title": {"ar": "أيام الأسبوع", "en": "Days of the Week", "de": "Wochentage", "fr": "Les jours de la semaine", "tr": "Haftanın Günleri", "ru": "Дни недели", "sv": "Veckodagar", "nl": "Dagen van de week", "el": "Ημέρες της εβδομάδας"},
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
            {"num": 1, "ar": "أَلَمْ تَرَ كَيْفَ فَعَلَ رَبُّكَ بِأَصْحَابِ الْفِيلِ", "en": "Have you not seen how your Lord dealt with the companions of the elephant?", "de": "Hast du nicht gesehen, wie dein Herr mit den Leuten des Elefanten verfuhr?", "fr": "N'as-tu pas vu comment ton Seigneur a agi envers les gens de l'éléphant?", "tr": "Rabbinin fil sahiplerine ne yaptığını görmedin mi?", "ru": "Разве ты не видел, как поступил твой Господь с владельцами слона?", "sv": "Har du inte sett hur din Herre handlade med elefantens folk?", "nl": "Heb je niet gezien hoe jouw Heer met de mensen van de olifant heeft gehandeld?", "el": "Δεν είδες πώς ο Κύριός σου μεταχειρίστηκε τους ανθρώπους του ελέφαντα;"},
            {"num": 2, "ar": "أَلَمْ يَجْعَلْ كَيْدَهُمْ فِي تَضْلِيلٍ", "en": "Did He not make their plan into misguidance?", "de": "Hat Er nicht ihren Plan zunichte gemacht?", "fr": "N'a-t-Il pas rendu leur stratagème vain?", "tr": "Onların tuzaklarını boşa çıkarmadı mı?", "ru": "Разве Он не расстроил их козни?", "sv": "Har Han inte gjort deras plan om intet?", "nl": "Heeft Hij hun plan niet doen mislukken?", "el": "Δεν κατέστρεψε το σχέδιό τους;"},
            {"num": 3, "ar": "وَأَرْسَلَ عَلَيْهِمْ طَيْرًا أَبَابِيلَ", "en": "And He sent against them birds in flocks", "de": "Und Er sandte gegen sie Schwärme von Vögeln", "fr": "Et Il envoya contre eux des oiseaux par volées", "tr": "Üzerlerine sürü sürü kuşlar gönderdi", "ru": "И послал на них птиц стаями", "sv": "Och Han sände mot dem fåglar i svärmar", "nl": "En Hij zond tegen hen vogels in zwermen", "el": "Και έστειλε εναντίον τους σμήνη πουλιών"},
            {"num": 4, "ar": "تَرْمِيهِمْ بِحِجَارَةٍ مِنْ سِجِّيلٍ", "en": "Striking them with stones of hard clay", "de": "Die sie mit Steinen aus gebranntem Ton bewarfen", "fr": "Qui les bombardaient de pierres d'argile", "tr": "Onlara pişkin tuğladan taşlar atıyorlardı", "ru": "Которые бросали в них камни из обожжённой глины", "sv": "Som kastade stenar av bränd lera på dem", "nl": "Die hen met stenen van gebakken klei bekogelden", "el": "Που τους πετούσαν πέτρες από ψημένο πηλό"},
            {"num": 5, "ar": "فَجَعَلَهُمْ كَعَصْفٍ مَأْكُولٍ", "en": "And He made them like eaten straw", "de": "Und Er machte sie wie abgefressene Halme", "fr": "Et Il les rendit semblables à de la paille mâchée", "tr": "Böylece onları yenmiş ekin yaprağı gibi yaptı", "ru": "И превратил их в подобие изъеденных листьев", "sv": "Och Han gjorde dem som uppätna strån", "nl": "En Hij maakte hen als opgegeten stro", "el": "Και τους έκανε σαν φαγωμένα άχυρα"},
        ],
    },
    {
        "id": "quraysh", "number": 106, "name_ar": "قريش", "name_en": "Quraysh",
        "difficulty": 1, "total_ayahs": 4,
        "ayahs": [
            {"num": 1, "ar": "لِإِيلَافِ قُرَيْشٍ", "en": "For the accustomed security of the Quraysh", "de": "Wegen der Vereinbarung der Quraisch", "fr": "Pour le pacte des Qouraych", "tr": "Kureyş'in güvenliği için", "ru": "Ради единения курайшитов", "sv": "För Quraysh sedvanliga trygghet", "nl": "Voor de gewoonte van de Qoeraysh", "el": "Για τη συμφωνία των Κουράις"},
            {"num": 2, "ar": "إِيلَافِهِمْ رِحْلَةَ الشِّتَاءِ وَالصَّيْفِ", "en": "Their accustomed security of the winter and summer journeys", "de": "Ihrer Vereinbarung der Winter- und Sommerreise", "fr": "Leur pacte pour les voyages d'hiver et d'été", "tr": "Kış ve yaz yolculuklarındaki güvenlikleri için", "ru": "Единения их для зимних и летних поездок", "sv": "Deras sedvanliga trygghet under vinter- och sommarresorna", "nl": "Hun gewoonte van de winter- en zomerreizen", "el": "Τη συμφωνία τους για τα χειμερινά και θερινά ταξίδια"},
            {"num": 3, "ar": "فَلْيَعْبُدُوا رَبَّ هَذَا الْبَيْتِ", "en": "Let them worship the Lord of this House", "de": "So sollen sie dem Herrn dieses Hauses dienen", "fr": "Qu'ils adorent donc le Seigneur de cette Maison", "tr": "Bu Evin Rabbine kulluk etsinler", "ru": "Пусть же поклоняются Господу этого Дома", "sv": "Låt dem tillbe Herren av detta Hus", "nl": "Laat hen dan de Heer van dit Huis aanbidden", "el": "Ας λατρεύουν λοιπόν τον Κύριο αυτού του Οίκου"},
            {"num": 4, "ar": "الَّذِي أَطْعَمَهُمْ مِنْ جُوعٍ وَآمَنَهُمْ مِنْ خَوْفٍ", "en": "Who has fed them against hunger and made them safe from fear", "de": "Der ihnen Speise gegen Hunger gab und sie vor Furcht sicher machte", "fr": "Qui les a nourris contre la faim et rassurés de la crainte", "tr": "Ki onları açlıktan doyurmuş ve korkudan emin kılmıştır", "ru": "Который накормил их после голода и обезопасил после страха", "sv": "Som har gett dem mat mot hunger och trygghet mot fruktan", "nl": "Die hen heeft gevoed tegen honger en hen veilig heeft gesteld tegen angst", "el": "Που τους τάισε ενάντια στην πείνα και τους ασφάλισε από τον φόβο"},
        ],
    },
    {
        "id": "maun", "number": 107, "name_ar": "الماعون", "name_en": "Al-Ma'un",
        "difficulty": 2, "total_ayahs": 7,
        "ayahs": [
            {"num": 1, "ar": "أَرَأَيْتَ الَّذِي يُكَذِّبُ بِالدِّينِ", "en": "Have you seen the one who denies the religion?", "de": "Hast du den gesehen, der das Gericht leugnet?", "fr": "As-tu vu celui qui traite de mensonge la religion?", "tr": "Dini yalanlayan kimseyi gördün mü?", "ru": "Видел ли ты того, кто отрицает воздаяние?", "sv": "Har du sett den som förnekar religionen?", "nl": "Heb je degene gezien die de godsdienst loochent?", "el": "Είδες αυτόν που αρνείται τη θρησκεία;"},
            {"num": 2, "ar": "فَذَلِكَ الَّذِي يَدُعُّ الْيَتِيمَ", "en": "For that is the one who drives away the orphan", "de": "Das ist derjenige, der die Waise verstößt", "fr": "C'est bien celui qui repousse l'orphelin", "tr": "İşte yetimi itip kakan odur", "ru": "Это тот, кто гонит сироту", "sv": "Det är den som stöter bort den faderlöse", "nl": "Dat is degene die de wees wegstoot", "el": "Αυτός είναι που απωθεί το ορφανό"},
            {"num": 3, "ar": "وَلَا يَحُضُّ عَلَى طَعَامِ الْمِسْكِينِ", "en": "And does not encourage the feeding of the poor", "de": "Und nicht zur Speisung des Armen anhält", "fr": "Et n'encourage pas à nourrir le pauvre", "tr": "Yoksulu doyurmaya teşvik etmez", "ru": "И не побуждает к кормлению бедняка", "sv": "Och inte uppmuntrar till att ge den behövande mat", "nl": "En niet aanspoort tot het voeden van de arme", "el": "Και δεν ενθαρρύνει τη σίτιση του φτωχού"},
            {"num": 4, "ar": "فَوَيْلٌ لِلْمُصَلِّينَ", "en": "So woe to those who pray", "de": "Wehe also den Betenden", "fr": "Malheur donc à ceux qui prient", "tr": "Yazıklar olsun o namaz kılanlara", "ru": "Горе же молящимся", "sv": "Ve över dem som ber", "nl": "Wee dan degenen die bidden", "el": "Αλίμονο σε αυτούς που προσεύχονται"},
            {"num": 5, "ar": "الَّذِينَ هُمْ عَنْ صَلَاتِهِمْ سَاهُونَ", "en": "But who are heedless of their prayer", "de": "Die ihr Gebet vernachlässigen", "fr": "Qui sont négligents dans leur prière", "tr": "Ki onlar namazlarından gafildirler", "ru": "Которые небрежны к своей молитве", "sv": "Som är likgiltiga inför sin bön", "nl": "Die onachtzaam zijn met hun gebed", "el": "Που αμελούν την προσευχή τους"},
            {"num": 6, "ar": "الَّذِينَ هُمْ يُرَاءُونَ", "en": "Those who make show of their deeds", "de": "Die nur gesehen werden wollen", "fr": "Qui font ostentation", "tr": "Onlar gösteriş yapanlardır", "ru": "Которые показывают напоказ", "sv": "De som gör saker för syns skull", "nl": "Die opzichtig doen", "el": "Αυτοί που επιδεικνύονται"},
            {"num": 7, "ar": "وَيَمْنَعُونَ الْمَاعُونَ", "en": "And withhold simple assistance", "de": "Und die kleine Hilfeleistung verweigern", "fr": "Et refusent la petite aide", "tr": "Ve basit yardımı engellerler", "ru": "И отказывают в мелкой помощи", "sv": "Och vägrar ge enkel hjälp", "nl": "En de kleine hulp weigeren", "el": "Και αρνούνται την απλή βοήθεια"},
        ],
    },
    {
        "id": "kafiroon", "number": 109, "name_ar": "الكافرون", "name_en": "Al-Kafiroon",
        "difficulty": 2, "total_ayahs": 6,
        "ayahs": [
            {"num": 1, "ar": "قُلْ يَا أَيُّهَا الْكَافِرُونَ", "en": "Say: O disbelievers", "de": "Sprich: O ihr Ungläubigen", "fr": "Dis: Ô vous les mécréants", "tr": "De ki: Ey kâfirler", "ru": "Скажи: О неверующие", "sv": "Säg: Ni som förnekar tron", "nl": "Zeg: O ongelovigen", "el": "Πες: Ω άπιστοι"},
            {"num": 2, "ar": "لَا أَعْبُدُ مَا تَعْبُدُونَ", "en": "I do not worship what you worship", "de": "Ich diene nicht dem, dem ihr dient", "fr": "Je n'adore pas ce que vous adorez", "tr": "Ben sizin taptıklarınıza tapmam", "ru": "Я не поклоняюсь тому, чему вы поклоняетесь", "sv": "Jag tillber inte det ni tillber", "nl": "Ik aanbid niet wat jullie aanbidden", "el": "Δεν λατρεύω αυτό που λατρεύετε"},
            {"num": 3, "ar": "وَلَا أَنْتُمْ عَابِدُونَ مَا أَعْبُدُ", "en": "Nor are you worshippers of what I worship", "de": "Und ihr dient nicht dem, dem ich diene", "fr": "Et vous n'êtes pas adorateurs de ce que j'adore", "tr": "Siz de benim taptığıma tapacak değilsiniz", "ru": "И вы не поклоняетесь тому, чему я поклоняюсь", "sv": "Och ni tillber inte det jag tillber", "nl": "En jullie aanbidden niet wat ik aanbid", "el": "Ούτε εσείς λατρεύετε αυτό που λατρεύω"},
            {"num": 4, "ar": "وَلَا أَنَا عَابِدٌ مَا عَبَدْتُمْ", "en": "Nor will I be a worshipper of what you worship", "de": "Und ich werde nicht dem dienen, dem ihr gedient habt", "fr": "Et je ne suis pas adorateur de ce que vous adorez", "tr": "Ben sizin taptıklarınıza tapacak değilim", "ru": "И я не стану поклоняться тому, чему вы поклоняетесь", "sv": "Och jag kommer inte att tillbe det ni tillber", "nl": "En ik zal niet aanbidden wat jullie aanbidden", "el": "Ούτε εγώ θα λατρεύσω αυτό που λατρεύετε"},
            {"num": 5, "ar": "وَلَا أَنْتُمْ عَابِدُونَ مَا أَعْبُدُ", "en": "Nor will you be worshippers of what I worship", "de": "Und ihr werdet nicht dem dienen, dem ich diene", "fr": "Et vous n'êtes pas adorateurs de ce que j'adore", "tr": "Siz de benim taptığıma tapacak değilsiniz", "ru": "И вы не станете поклоняться тому, чему я поклоняюсь", "sv": "Och ni kommer inte att tillbe det jag tillber", "nl": "En jullie zullen niet aanbidden wat ik aanbid", "el": "Ούτε εσείς θα λατρεύσετε αυτό που λατρεύω"},
            {"num": 6, "ar": "لَكُمْ دِينُكُمْ وَلِيَ دِينِ", "en": "For you is your religion, and for me is my religion", "de": "Euch eure Religion und mir meine Religion", "fr": "A vous votre religion et à moi ma religion", "tr": "Sizin dininiz size, benim dinim bana", "ru": "Вам - ваша религия, а мне - моя", "sv": "Ni har er religion och jag har min", "nl": "Voor jullie is jullie godsdienst en voor mij is mijn godsdienst", "el": "Εσείς έχετε τη δική σας θρησκεία και εγώ τη δική μου"},
        ],
    },
    {
        "id": "takathur", "number": 102, "name_ar": "التكاثر", "name_en": "At-Takathur",
        "difficulty": 2, "total_ayahs": 8,
        "ayahs": [
            {"num": 1, "ar": "أَلْهَاكُمُ التَّكَاثُرُ", "en": "Competition in worldly increase diverts you", "de": "Das Streben nach mehr lenkt euch ab", "fr": "La course aux richesses vous distrait", "tr": "Çoğalma yarışı sizi oyaladı", "ru": "Страсть к приумножению увлекла вас", "sv": "Tävlan om att äga mer upptar er", "nl": "De wedijver om meer heeft jullie afgeleid", "el": "Ο ανταγωνισμός για περισσότερα σας αποσπά"},
            {"num": 2, "ar": "حَتَّى زُرْتُمُ الْمَقَابِرَ", "en": "Until you visit the graveyards", "de": "Bis ihr die Gräber besucht", "fr": "Jusqu'à ce que vous visitiez les tombes", "tr": "Kabirleri ziyaret edinceye kadar", "ru": "Пока вы не посетите могилы", "sv": "Tills ni besöker gravarna", "nl": "Totdat jullie de graven bezoeken", "el": "Μέχρι να επισκεφτείτε τους τάφους"},
            {"num": 3, "ar": "كَلَّا سَوْفَ تَعْلَمُونَ", "en": "No! You will soon know", "de": "Nein! Ihr werdet es noch erfahren", "fr": "Non! Vous saurez bientôt", "tr": "Hayır! Yakında bileceksiniz", "ru": "Но нет! Скоро вы узнаете", "sv": "Nej! Ni kommer snart att veta", "nl": "Nee! Jullie zullen het spoedig weten", "el": "Όχι! Σύντομα θα μάθετε"},
            {"num": 4, "ar": "ثُمَّ كَلَّا سَوْفَ تَعْلَمُونَ", "en": "Then no! You will soon know", "de": "Und abermals nein! Ihr werdet es noch erfahren", "fr": "Encore une fois, non! Vous saurez bientôt", "tr": "Yine hayır! Yakında bileceksiniz", "ru": "Ещё раз нет! Скоро вы узнаете", "sv": "Åter nej! Ni kommer snart att veta", "nl": "Nogmaals nee! Jullie zullen het spoedig weten", "el": "Και πάλι όχι! Σύντομα θα μάθετε"},
            {"num": 5, "ar": "كَلَّا لَوْ تَعْلَمُونَ عِلْمَ الْيَقِينِ", "en": "No! If you only knew with certain knowledge", "de": "Nein! Wenn ihr es mit sicherem Wissen wüsstet", "fr": "Non! Si vous saviez de science certaine", "tr": "Hayır! Kesin bilgiyle bilseydiniz", "ru": "Но нет! Если бы вы знали с несомненностью", "sv": "Nej! Om ni bara visste med säker kunskap", "nl": "Nee! Als jullie het maar wisten met zekere kennis", "el": "Όχι! Αν μόνο γνωρίζατε με βεβαιότητα"},
            {"num": 6, "ar": "لَتَرَوُنَّ الْجَحِيمَ", "en": "You will surely see the Hellfire", "de": "Ihr werdet die Hölle sehen", "fr": "Vous verrez certes la Fournaise", "tr": "Cehennemi mutlaka göreceksiniz", "ru": "Вы непременно увидите Ад", "sv": "Ni kommer förvisso att se Elden", "nl": "Jullie zullen zeker het Hellevuur zien", "el": "Σίγουρα θα δείτε την Κόλαση"},
            {"num": 7, "ar": "ثُمَّ لَتَرَوُنَّهَا عَيْنَ الْيَقِينِ", "en": "Then you will surely see it with the eye of certainty", "de": "Dann werdet ihr es mit dem Auge der Gewissheit sehen", "fr": "Puis vous le verrez avec l'œil de la certitude", "tr": "Sonra onu kesin gözle göreceksiniz", "ru": "Потом вы увидите его воочию", "sv": "Sedan kommer ni att se det med visshetens öga", "nl": "Dan zullen jullie het zien met het oog van zekerheid", "el": "Τότε θα το δείτε με το μάτι της βεβαιότητας"},
            {"num": 8, "ar": "ثُمَّ لَتُسْأَلُنَّ يَوْمَئِذٍ عَنِ النَّعِيمِ", "en": "Then you will surely be asked that Day about pleasure", "de": "Dann werdet ihr an jenem Tag nach den Wohltaten befragt werden", "fr": "Puis vous serez interrogés ce Jour-là sur les bienfaits", "tr": "Sonra o gün nimetlerden sorulacaksınız", "ru": "Потом в тот День вас спросят о благах", "sv": "Sedan kommer ni att tillfrågas den Dagen om njutningarna", "nl": "Dan zullen jullie op die Dag zeker worden gevraagd over de genietingen", "el": "Τότε θα ερωτηθείτε εκείνη την Ημέρα για τις απολαύσεις"},
        ],
    },
    {
        "id": "qariah", "number": 101, "name_ar": "القارعة", "name_en": "Al-Qariah",
        "difficulty": 2, "total_ayahs": 11,
        "ayahs": [
            {"num": 1, "ar": "الْقَارِعَةُ", "en": "The Striking Calamity", "de": "Das Pochende", "fr": "Le Fracas", "tr": "Kapıyı çalacak olan", "ru": "Великое бедствие", "sv": "Den Dånande", "nl": "De Ramp", "el": "Η Συντριπτική Καταστροφή"},
            {"num": 2, "ar": "مَا الْقَارِعَةُ", "en": "What is the Striking Calamity?", "de": "Was ist das Pochende?", "fr": "Qu'est-ce que le Fracas?", "tr": "Nedir o kapıyı çalacak olan?", "ru": "Что такое великое бедствие?", "sv": "Vad är den Dånande?", "nl": "Wat is de Ramp?", "el": "Τι είναι η Συντριπτική Καταστροφή;"},
            {"num": 3, "ar": "وَمَا أَدْرَاكَ مَا الْقَارِعَةُ", "en": "And what will make you know what the Striking Calamity is?", "de": "Und was lässt dich wissen, was das Pochende ist?", "fr": "Et qui te dira ce qu'est le Fracas?", "tr": "O kapıyı çalacak olanın ne olduğunu sen ne bileceksin?", "ru": "И что даст тебе знать, что такое великое бедствие?", "sv": "Och vad kan ge dig kunskap om vad den Dånande är?", "nl": "En wat doet jou weten wat de Ramp is?", "el": "Και τι θα σε κάνει να γνωρίσεις τι είναι;"},
            {"num": 4, "ar": "يَوْمَ يَكُونُ النَّاسُ كَالْفَرَاشِ الْمَبْثُوثِ", "en": "A Day when people will be like moths, dispersed", "de": "An dem Tag, da die Menschen wie zerstreute Motten sein werden", "fr": "Le jour où les gens seront comme des papillons éparpillés", "tr": "O gün insanlar yayılmış kelebekler gibi olacaklar", "ru": "В тот День люди будут как рассеянные мотыльки", "sv": "En Dag då människorna skall vara som spridda fjärilar", "nl": "Een Dag waarop de mensen als verspreide motten zullen zijn", "el": "Μια Ημέρα που οι άνθρωποι θα είναι σαν σκορπισμένες πεταλούδες"},
            {"num": 5, "ar": "وَتَكُونُ الْجِبَالُ كَالْعِهْنِ الْمَنْفُوشِ", "en": "And the mountains will be like carded wool", "de": "Und die Berge wie gekrämpelte Wolle sein werden", "fr": "Et les montagnes seront comme de la laine cardée", "tr": "Dağlar atılmış yün gibi olacak", "ru": "А горы будут как расчёсанная шерсть", "sv": "Och bergen skall vara som kardad ull", "nl": "En de bergen als gekarde wol zullen zijn", "el": "Και τα βουνά θα είναι σαν χτενισμένο μαλλί"},
            {"num": 6, "ar": "فَأَمَّا مَنْ ثَقُلَتْ مَوَازِينُهُ", "en": "As for the one whose scales are heavy", "de": "Was nun den betrifft, dessen Waagschalen schwer sind", "fr": "Quant à celui dont la balance sera lourde", "tr": "Tartıları ağır gelen kimseye gelince", "ru": "Тот, чьи весы окажутся тяжёлыми", "sv": "Den vars vågskålar väger tungt", "nl": "Wat betreft degene wiens weegschalen zwaar zijn", "el": "Όσο για αυτόν του οποίου οι ζυγαριές είναι βαριές"},
            {"num": 7, "ar": "فَهُوَ فِي عِيشَةٍ رَاضِيَةٍ", "en": "He will be in a pleasant life", "de": "So wird er ein zufriedenes Leben führen", "fr": "Il sera dans une vie agréable", "tr": "O hoşnut bir yaşayış içinde olacaktır", "ru": "Тот будет в приятной жизни", "sv": "Han skall leva ett behagligt liv", "nl": "Hij zal in een aangenaam leven zijn", "el": "Θα ζει μια ευχάριστη ζωή"},
            {"num": 8, "ar": "وَأَمَّا مَنْ خَفَّتْ مَوَازِينُهُ", "en": "But as for the one whose scales are light", "de": "Was aber den betrifft, dessen Waagschalen leicht sind", "fr": "Mais quant à celui dont la balance sera légère", "tr": "Tartıları hafif gelene gelince", "ru": "А тот, чьи весы окажутся лёгкими", "sv": "Men den vars vågskålar väger lätt", "nl": "Maar wat betreft degene wiens weegschalen licht zijn", "el": "Αλλά αυτός του οποίου οι ζυγαριές είναι ελαφριές"},
            {"num": 9, "ar": "فَأُمُّهُ هَاوِيَةٌ", "en": "His refuge will be the Pit", "de": "So wird der Abgrund seine Heimstatt sein", "fr": "Son refuge sera l'abîme", "tr": "Onun anası Hâviye'dir", "ru": "Его обителью будет Пропасть", "sv": "Hans hemvist skall vara Avgrunden", "nl": "Zijn toevlucht zal de Afgrond zijn", "el": "Το καταφύγιό του θα είναι η Άβυσσος"},
            {"num": 10, "ar": "وَمَا أَدْرَاكَ مَا هِيَهْ", "en": "And what will make you know what that is?", "de": "Und was lässt dich wissen, was das ist?", "fr": "Et qui te dira ce que c'est?", "tr": "Onun ne olduğunu sen ne bileceksin?", "ru": "И что даст тебе знать, что это?", "sv": "Och vad kan ge dig kunskap om vad det är?", "nl": "En wat doet jou weten wat dat is?", "el": "Και τι θα σε κάνει να γνωρίσεις τι είναι αυτό;"},
            {"num": 11, "ar": "نَارٌ حَامِيَةٌ", "en": "It is a blazing Fire", "de": "Ein loderndes Feuer", "fr": "Un Feu ardent", "tr": "Kızgın bir ateştir", "ru": "Это пылающий Огонь", "sv": "En brinnande Eld", "nl": "Een laaiend Vuur", "el": "Μια φλεγόμενη Φωτιά"},
        ],
    },
    {
        "id": "zilzal", "number": 99, "name_ar": "الزلزلة", "name_en": "Az-Zilzal",
        "difficulty": 2, "total_ayahs": 8,
        "ayahs": [
            {"num": 1, "ar": "إِذَا زُلْزِلَتِ الْأَرْضُ زِلْزَالَهَا", "en": "When the earth is shaken with its final earthquake", "de": "Wenn die Erde mit ihrem gewaltigen Beben erschüttert wird", "fr": "Quand la terre tremblera d'un violent tremblement", "tr": "Yer dehşetli bir sarsıntıyla sarsıldığında", "ru": "Когда земля сотрясётся своим сотрясением", "sv": "När jorden skakas av sin slutliga jordbävning", "nl": "Wanneer de aarde met haar zware beving wordt geschud", "el": "Όταν η γη τραντάζεται με τον τελικό σεισμό της"},
            {"num": 2, "ar": "وَأَخْرَجَتِ الْأَرْضُ أَثْقَالَهَا", "en": "And the earth brings out its burdens", "de": "Und die Erde ihre Lasten herausbringt", "fr": "Et que la terre fera sortir ses fardeaux", "tr": "Ve yer ağırlıklarını çıkardığında", "ru": "И земля извергнет свою ношу", "sv": "Och jorden kastar ut sina bördor", "nl": "En de aarde haar lasten naar buiten brengt", "el": "Και η γη βγάλει τα βάρη της"},
            {"num": 3, "ar": "وَقَالَ الْإِنْسَانُ مَا لَهَا", "en": "And man says: What is wrong with it?", "de": "Und der Mensch sagt: Was ist mit ihr?", "fr": "Et que l'homme dira: Qu'a-t-elle?", "tr": "Ve insan: Buna ne oluyor? dediğinde", "ru": "И скажет человек: Что с ней?", "sv": "Och människan säger: Vad har hänt med den?", "nl": "En de mens zegt: Wat is er met haar?", "el": "Και ο άνθρωπος λέει: Τι συμβαίνει;"},
            {"num": 4, "ar": "يَوْمَئِذٍ تُحَدِّثُ أَخْبَارَهَا", "en": "That Day, it will report its news", "de": "An jenem Tag wird sie ihre Nachrichten erzählen", "fr": "Ce jour-là, elle racontera ce qui s'est passé", "tr": "O gün yer haberlerini anlatır", "ru": "В тот День она расскажет свои вести", "sv": "Den Dagen skall den berätta sina nyheter", "nl": "Op die Dag zal zij haar nieuws vertellen", "el": "Εκείνη την Ημέρα θα αναφέρει τα νέα της"},
            {"num": 5, "ar": "بِأَنَّ رَبَّكَ أَوْحَى لَهَا", "en": "Because your Lord has commanded it", "de": "Weil dein Herr es ihr eingegeben hat", "fr": "Car ton Seigneur le lui aura commandé", "tr": "Çünkü Rabbin ona vahyetmiştir", "ru": "Ибо Господь твой повелел ей", "sv": "Ty din Herre har befallt den", "nl": "Omdat jouw Heer het haar heeft opgedragen", "el": "Επειδή ο Κύριός σου το διέταξε"},
            {"num": 6, "ar": "يَوْمَئِذٍ يَصْدُرُ النَّاسُ أَشْتَاتًا لِيُرَوْا أَعْمَالَهُمْ", "en": "That Day, people will proceed in scattered groups to be shown their deeds", "de": "An jenem Tag werden die Menschen in Gruppen herauskommen, um ihre Werke gezeigt zu bekommen", "fr": "Ce jour-là, les gens sortiront séparément pour voir leurs œuvres", "tr": "O gün insanlar amellerinin karşılığını görmek için bölük bölük çıkarlar", "ru": "В тот День люди выйдут толпами, чтобы увидеть свои деяния", "sv": "Den Dagen skall människorna komma i spridda grupper för att se sina gärningar", "nl": "Op die Dag zullen de mensen in verspreide groepen tevoorschijn komen om hun daden te zien", "el": "Εκείνη την Ημέρα οι άνθρωποι θα προχωρήσουν σε ομάδες για να δουν τα έργα τους"},
            {"num": 7, "ar": "فَمَنْ يَعْمَلْ مِثْقَالَ ذَرَّةٍ خَيْرًا يَرَهُ", "en": "So whoever does an atom's weight of good will see it", "de": "Wer Gutes im Gewicht eines Stäubchens tut, wird es sehen", "fr": "Quiconque fait un bien fût-ce du poids d'un atome le verra", "tr": "Kim zerre ağırlığınca hayır yapmışsa onu görür", "ru": "Кто сделал добро весом в пылинку, увидит его", "sv": "Den som gör gott så litet som ett stoftkorns vikt skall se det", "nl": "Wie dan ook het gewicht van een atoom aan goeds doet, zal het zien", "el": "Όποιος κάνει καλό στο βάρος ενός ατόμου θα το δει"},
            {"num": 8, "ar": "وَمَنْ يَعْمَلْ مِثْقَالَ ذَرَّةٍ شَرًّا يَرَهُ", "en": "And whoever does an atom's weight of evil will see it", "de": "Und wer Böses im Gewicht eines Stäubchens tut, wird es sehen", "fr": "Et quiconque fait un mal fût-ce du poids d'un atome le verra", "tr": "Kim de zerre ağırlığınca şer işlemişse onu görür", "ru": "И кто сделал зло весом в пылинку, увидит его", "sv": "Och den som gör ont så litet som ett stoftkorns vikt skall se det", "nl": "En wie dan ook het gewicht van een atoom aan kwaad doet, zal het zien", "el": "Και όποιος κάνει κακό στο βάρος ενός ατόμου θα το δει"},
        ],
    },
]

# ═══════════════════════════════════════════════════════════════
# TAJWEED RULES (for Advanced Quran stage)
# ═══════════════════════════════════════════════════════════════

TAJWEED_RULES = [
    {"id": "t01", "emoji": "🔴", "title": {"ar": "الإدغام", "en": "Idgham (Merging)", "de": "Idgham (Verschmelzung)", "fr": "Idgham (Fusion)", "tr": "İdğam (Birleştirme)", "ru": "Идгам (Слияние)", "sv": "Idgham (Sammansmältning)", "nl": "Idgham (Versmelting)", "el": "Ιντγάμ (Συγχώνευση)"},
     "content": {"ar": "الإدغام: إدخال حرف ساكن في حرف متحرك بعده. حروف الإدغام مجموعة في كلمة (يرملون). مثال: مَنْ يَعمل → مَيَّعمل",
                 "en": "Idgham: Merging a silent letter into the next voweled letter. Idgham letters are in (yarmalun). Example: man ya'mal → mayya'mal",
                 "de": "Idgham: Verschmelzung eines stillen Buchstabens mit dem nächsten vokalisierten. Idgham-Buchstaben sind in (yarmalun). Beispiel: man ya'mal → mayya'mal",
                 "fr": "Idgham: Fusion d'une lettre silencieuse avec la suivante vocalisée. Les lettres d'Idgham sont dans (yarmalun). Exemple: man ya'mal → mayya'mal",
                 "tr": "İdğam: Sakin bir harfin kendinden sonraki harekeli harfe katılmasıdır. İdğam harfleri (يرملون) kelimesinde toplanmıştır. Örnek: مَنْ يَعمل → مَيَّعمل",
                 "ru": "Идгам: Слияние немой буквы со следующей огласованной. Буквы идгама собраны в слове (ярмалюн). Пример: ман яъмал → маййаъмал",
                 "sv": "Idgham: Sammansmältning av en tyst bokstav med nästa vokaliserade. Idgham-bokstäverna finns i (yarmalun). Exempel: man ya'mal → mayya'mal",
                 "nl": "Idgham: Versmelting van een stille letter met de volgende gevokaliseerde. Idgham-letters zijn in (yarmalun). Voorbeeld: man ya'mal → mayya'mal",
                 "el": "Ιντγάμ: Συγχώνευση ενός σιωπηλού γράμματος με το επόμενο φωνηεντικό. Τα γράμματα Ιντγάμ είναι στο (yarmalun). Παράδειγμα: man ya'mal → mayya'mal"}},
    {"id": "t02", "emoji": "🟢", "title": {"ar": "الإظهار", "en": "Izhar (Clarity)", "de": "Izhar (Klarheit)", "fr": "Izhar (Clarté)", "tr": "İzhar (Açıklık)", "ru": "Изхар (Ясность)", "sv": "Izhar (Klarhet)", "nl": "Izhar (Duidelijkheid)", "el": "Ιζχάρ (Σαφήνεια)"},
     "content": {"ar": "الإظهار: نطق النون الساكنة أو التنوين بوضوح قبل حروف الحلق (ء هـ ع ح غ خ). مثال: مِنْ عِنده → مِنْ عِنده (بوضوح)",
                 "en": "Izhar: Pronouncing noon sakinah or tanween clearly before throat letters (ء هـ ع ح غ خ). Example: min 'indih → clear pronunciation",
                 "de": "Izhar: Klare Aussprache von Nun Sakinah oder Tanwin vor Kehlbuchstaben (ء هـ ع ح غ خ). Beispiel: min 'indih → klare Aussprache",
                 "fr": "Izhar: Prononciation claire du noun sakinah ou tanween avant les lettres gutturales (ء هـ ع ح غ خ). Exemple: min 'indih → prononciation claire",
                 "tr": "İzhar: Nun sakin veya tenvinin boğaz harflerinden önce açıkça okunmasıdır (ء هـ ع ح غ خ). Örnek: مِنْ عِنده → açık okuma",
                 "ru": "Изхар: Ясное произнесение нун сакина или танвина перед горловыми буквами (ء هـ ع ح غ خ). Пример: мин ъиндих → ясное произношение",
                 "sv": "Izhar: Tydligt uttal av nun sakinah eller tanween före halsbokstäver (ء هـ ع ح غ خ). Exempel: min 'indih → tydligt uttal",
                 "nl": "Izhar: Duidelijke uitspraak van nun sakinah of tanween voor keelletters (ء هـ ع ح غ خ). Voorbeeld: min 'indih → duidelijke uitspraak",
                 "el": "Ιζχάρ: Σαφής προφορά του νουν σακίνα ή τανουίν πριν από τα λαρυγγικά γράμματα (ء هـ ع ح غ خ). Παράδειγμα: min 'indih → σαφής προφορά"}},
    {"id": "t03", "emoji": "🔵", "title": {"ar": "الإخفاء", "en": "Ikhfa (Hiding)", "de": "Ikhfa (Verbergen)", "fr": "Ikhfa (Dissimulation)", "tr": "İhfa (Gizleme)", "ru": "Ихфа (Сокрытие)", "sv": "Ikhfa (Döljning)", "nl": "Ikhfa (Verberging)", "el": "Ιχφά (Απόκρυψη)"},
     "content": {"ar": "الإخفاء: نطق النون الساكنة بين الإظهار والإدغام مع غنة. يكون قبل 15 حرفًا. مثال: مِنْ قبل → مِنقَبل (مع غنة خفيفة)",
                 "en": "Ikhfa: Pronouncing noon between clarity and merging with a nasal sound. It occurs before 15 letters. Example: min qablu → with a light nasal sound",
                 "de": "Ikhfa: Aussprache des Nun zwischen Klarheit und Verschmelzung mit Nasallaut. Es kommt vor 15 Buchstaben vor. Beispiel: min qablu → mit leichtem Nasallaut",
                 "fr": "Ikhfa: Prononciation du noun entre clarté et fusion avec un son nasal. Il se produit avant 15 lettres. Exemple: min qablu → avec un léger son nasal",
                 "tr": "İhfa: Nun sakin harfinin izhar ile idğam arasında ğunne ile okunmasıdır. 15 harften önce yapılır. Örnek: مِنْ قبل → hafif ğunne ile",
                 "ru": "Ихфа: Произнесение нуна между ясностью и слиянием с носовым звуком. Встречается перед 15 буквами. Пример: мин каблю → с лёгким носовым звуком",
                 "sv": "Ikhfa: Uttal av nun mellan klarhet och sammansmältning med nasalt ljud. Det sker före 15 bokstäver. Exempel: min qablu → med ett lätt nasalt ljud",
                 "nl": "Ikhfa: Uitspraak van nun tussen duidelijkheid en versmelting met nasaal geluid. Het komt voor 15 letters voor. Voorbeeld: min qablu → met een licht nasaal geluid",
                 "el": "Ιχφά: Προφορά του νουν μεταξύ σαφήνειας και συγχώνευσης με ρινικό ήχο. Εμφανίζεται πριν από 15 γράμματα. Παράδειγμα: min qablu → με ελαφρύ ρινικό ήχο"}},
    {"id": "t04", "emoji": "🟡", "title": {"ar": "الإقلاب", "en": "Iqlab (Conversion)", "de": "Iqlab (Umwandlung)", "fr": "Iqlab (Conversion)", "tr": "İklab (Dönüştürme)", "ru": "Иклаб (Преобразование)", "sv": "Iqlab (Omvandling)", "nl": "Iqlab (Omzetting)", "el": "Ικλάμπ (Μετατροπή)"},
     "content": {"ar": "الإقلاب: تحويل النون الساكنة أو التنوين إلى ميم مخفاة عند الباء. مثال: مِنْ بَعد → مِمبَعد. حرف واحد فقط: الباء.",
                 "en": "Iqlab: Converting noon sakinah or tanween to a hidden meem before ba. Example: min ba'd → mimba'd. Only one letter: ba.",
                 "de": "Iqlab: Umwandlung von Nun Sakinah oder Tanwin in ein verstecktes Mim vor Ba. Beispiel: min ba'd → mimba'd. Nur ein Buchstabe: Ba.",
                 "fr": "Iqlab: Conversion du noun sakinah ou tanween en mim caché avant ba. Exemple: min ba'd → mimba'd. Une seule lettre: ba.",
                 "tr": "İklab: Nun sakin veya tenvinin ba harfinden önce gizli mim'e dönüştürülmesidir. Örnek: مِنْ بَعد → مِمبَعد. Sadece bir harf: ba.",
                 "ru": "Иклаб: Преобразование нун сакина или танвина в скрытый мим перед ба. Пример: мин баъд → мимбаъд. Только одна буква: ба.",
                 "sv": "Iqlab: Omvandling av nun sakinah eller tanween till dolt mim före ba. Exempel: min ba'd → mimba'd. Bara en bokstav: ba.",
                 "nl": "Iqlab: Omzetting van nun sakinah of tanween naar verborgen miem voor ba. Voorbeeld: min ba'd → mimba'd. Slechts één letter: ba.",
                 "el": "Ικλάμπ: Μετατροπή του νουν σακίνα ή τανουίν σε κρυφό μιμ πριν από μπα. Παράδειγμα: min ba'd → mimba'd. Μόνο ένα γράμμα: μπα."}},
    {"id": "t05", "emoji": "⭐", "title": {"ar": "المد الطبيعي", "en": "Natural Madd", "de": "Natürlicher Madd", "fr": "Madd Naturel", "tr": "Tabii Med", "ru": "Естественный Мадд", "sv": "Naturlig Madd", "nl": "Natuurlijke Madd", "el": "Φυσικό Μαντ"},
     "content": {"ar": "المد الطبيعي: مد الحرف حركتين فقط عند وجود حرف مد (ا و ي) بدون سبب. مثال: قَالَ (الألف ممدودة حركتين)، يقُولُ (الواو ممدودة حركتين)",
                 "en": "Natural Madd: Extending the letter for exactly 2 counts when there's a madd letter (ا و ي) without cause. Example: qaala (alif extended 2 counts)",
                 "de": "Natürlicher Madd: Dehnung des Buchstabens um genau 2 Takte bei einem Madd-Buchstaben (ا و ي) ohne Grund. Beispiel: qaala (Alif um 2 Takte gedehnt)",
                 "fr": "Madd Naturel: Extension de la lettre pendant exactement 2 temps lorsqu'il y a une lettre madd (ا و ي) sans cause. Exemple: qaala (alif étendu 2 temps)",
                 "tr": "Tabii Med: Med harfi (ا و ي) sebepsiz bulunduğunda harfi tam 2 vuruş uzatmaktır. Örnek: قَالَ (elif 2 vuruş uzatılır)",
                 "ru": "Естественный Мадд: Удлинение буквы ровно на 2 счёта при наличии буквы мадд (ا و ي) без причины. Пример: каала (алиф удлинён на 2 счёта)",
                 "sv": "Naturlig Madd: Förlängning av bokstaven i exakt 2 slag när det finns en madd-bokstav (ا و ي) utan orsak. Exempel: qaala (alif förlängd 2 slag)",
                 "nl": "Natuurlijke Madd: Verlenging van de letter met precies 2 tellen wanneer er een madd-letter (ا و ي) is zonder oorzaak. Voorbeeld: qaala (alif verlengd 2 tellen)",
                 "el": "Φυσικό Μαντ: Επέκταση του γράμματος για ακριβώς 2 χτύπους όταν υπάρχει γράμμα μαντ (ا و ي) χωρίς αιτία. Παράδειγμα: qaala (αλίφ επεκτεινόμενο 2 χτύπους)"}},
]

# ═══════════════════════════════════════════════════════════════
# MASTERY REVIEW TOPICS (Stage 15)
# ═══════════════════════════════════════════════════════════════

MASTERY_REVIEWS = [
    {"id": "r01", "emoji": "🔤", "title": {"ar": "مراجعة: الحروف العربية", "en": "Review: Arabic Letters", "de": "Wiederholung: Arabische Buchstaben", "fr": "Révision: Lettres arabes", "tr": "Tekrar: Arap Harfleri", "ru": "Повторение: Арабские буквы", "sv": "Repetition: Arabiska bokstäver", "nl": "Herhaling: Arabische letters", "el": "Επανάληψη: Αραβικά γράμματα"},
     "quiz": [
         {"q": {"ar": "كم عدد الحروف العربية؟", "en": "How many Arabic letters?", "de": "Wie viele arabische Buchstaben gibt es?", "fr": "Combien de lettres arabes?", "tr": "Kaç tane Arap harfi var?", "ru": "Сколько арабских букв?", "sv": "Hur många arabiska bokstäver finns det?", "nl": "Hoeveel Arabische letters zijn er?", "el": "Πόσα αραβικά γράμματα υπάρχουν;"},
          "a": {"ar": "28", "en": "28", "de": "28", "fr": "28", "tr": "28", "ru": "28", "sv": "28", "nl": "28", "el": "28"},
          "opts": {"ar": ["28", "26", "30"], "en": ["28", "26", "30"], "de": ["28", "26", "30"], "fr": ["28", "26", "30"], "tr": ["28", "26", "30"], "ru": ["28", "26", "30"], "sv": ["28", "26", "30"], "nl": ["28", "26", "30"], "el": ["28", "26", "30"]}},
         {"q": {"ar": "ما أول حرف في الأبجدية؟", "en": "What's the first letter?", "de": "Was ist der erste Buchstabe?", "fr": "Quelle est la première lettre?", "tr": "İlk harf nedir?", "ru": "Какая первая буква?", "sv": "Vilken är den första bokstaven?", "nl": "Wat is de eerste letter?", "el": "Ποιο είναι το πρώτο γράμμα;"},
          "a": {"ar": "ألف", "en": "Alif", "de": "Alif", "fr": "Alif", "tr": "Elif", "ru": "Алиф", "sv": "Alif", "nl": "Alif", "el": "Αλίφ"},
          "opts": {"ar": ["ألف", "باء", "تاء"], "en": ["Alif", "Ba", "Ta"], "de": ["Alif", "Ba", "Ta"], "fr": ["Alif", "Ba", "Ta"], "tr": ["Elif", "Ba", "Ta"], "ru": ["Алиф", "Ба", "Та"], "sv": ["Alif", "Ba", "Ta"], "nl": ["Alif", "Ba", "Ta"], "el": ["Αλίφ", "Μπα", "Τα"]}},
     ]},
    {"id": "r02", "emoji": "🔢", "title": {"ar": "مراجعة: الأرقام العربية", "en": "Review: Arabic Numbers", "de": "Wiederholung: Arabische Zahlen", "fr": "Révision: Chiffres arabes", "tr": "Tekrar: Arap Rakamları", "ru": "Повторение: Арабские цифры", "sv": "Repetition: Arabiska siffror", "nl": "Herhaling: Arabische cijfers", "el": "Επανάληψη: Αραβικοί αριθμοί"},
     "quiz": [
         {"q": {"ar": "ما هو الرقم ٧ بالعربية؟", "en": "What is ٧ in Arabic?", "de": "Was ist ٧ auf Arabisch?", "fr": "Que signifie ٧ en arabe?", "tr": "Arapçada ٧ nedir?", "ru": "Что такое ٧ по-арабски?", "sv": "Vad är ٧ på arabiska?", "nl": "Wat is ٧ in het Arabisch?", "el": "Τι είναι το ٧ στα αραβικά;"},
          "a": {"ar": "سبعة", "en": "Seven", "de": "Sieben", "fr": "Sept", "tr": "Yedi", "ru": "Семь", "sv": "Sju", "nl": "Zeven", "el": "Εφτά"},
          "opts": {"ar": ["سبعة", "ستة", "ثمانية"], "en": ["Seven", "Six", "Eight"], "de": ["Sieben", "Sechs", "Acht"], "fr": ["Sept", "Six", "Huit"], "tr": ["Yedi", "Altı", "Sekiz"], "ru": ["Семь", "Шесть", "Восемь"], "sv": ["Sju", "Sex", "Åtta"], "nl": ["Zeven", "Zes", "Acht"], "el": ["Εφτά", "Έξι", "Οχτώ"]}},
         {"q": {"ar": "اكتب العدد: عشرون", "en": "Write the number: twenty", "de": "Schreibe die Zahl: zwanzig", "fr": "Écris le nombre: vingt", "tr": "Sayıyı yaz: yirmi", "ru": "Напиши число: двадцать", "sv": "Skriv talet: tjugo", "nl": "Schrijf het getal: twintig", "el": "Γράψε τον αριθμό: είκοσι"},
          "a": {"ar": "٢٠", "en": "20", "de": "20", "fr": "20", "tr": "20", "ru": "20", "sv": "20", "nl": "20", "el": "20"},
          "opts": {"ar": ["٢٠", "١٢", "٣٠"], "en": ["20", "12", "30"], "de": ["20", "12", "30"], "fr": ["20", "12", "30"], "tr": ["20", "12", "30"], "ru": ["20", "12", "30"], "sv": ["20", "12", "30"], "nl": ["20", "12", "30"], "el": ["20", "12", "30"]}},
     ]},
    {"id": "r03", "emoji": "🕌", "title": {"ar": "مراجعة: أركان الإسلام", "en": "Review: Pillars of Islam", "de": "Wiederholung: Säulen des Islam", "fr": "Révision: Piliers de l'Islam", "tr": "Tekrar: İslam'ın Şartları", "ru": "Повторение: Столпы Ислама", "sv": "Repetition: Islams pelare", "nl": "Herhaling: Zuilen van de Islam", "el": "Επανάληψη: Πυλώνες του Ισλάμ"},
     "quiz": [
         {"q": {"ar": "كم عدد أركان الإسلام؟", "en": "How many pillars of Islam?", "de": "Wie viele Säulen hat der Islam?", "fr": "Combien de piliers a l'Islam?", "tr": "İslam'ın kaç şartı var?", "ru": "Сколько столпов Ислама?", "sv": "Hur många pelare har Islam?", "nl": "Hoeveel zuilen heeft de Islam?", "el": "Πόσοι πυλώνες έχει το Ισλάμ;"},
          "a": {"ar": "خمسة", "en": "Five", "de": "Fünf", "fr": "Cinq", "tr": "Beş", "ru": "Пять", "sv": "Fem", "nl": "Vijf", "el": "Πέντε"},
          "opts": {"ar": ["خمسة", "ستة", "أربعة"], "en": ["Five", "Six", "Four"], "de": ["Fünf", "Sechs", "Vier"], "fr": ["Cinq", "Six", "Quatre"], "tr": ["Beş", "Altı", "Dört"], "ru": ["Пять", "Шесть", "Четыре"], "sv": ["Fem", "Sex", "Fyra"], "nl": ["Vijf", "Zes", "Vier"], "el": ["Πέντε", "Έξι", "Τέσσερις"]}},
         {"q": {"ar": "ما الركن الثالث؟", "en": "What's the third pillar?", "de": "Was ist die dritte Säule?", "fr": "Quel est le troisième pilier?", "tr": "Üçüncü şart nedir?", "ru": "Какой третий столп?", "sv": "Vilken är den tredje pelaren?", "nl": "Wat is de derde zuil?", "el": "Ποιος είναι ο τρίτος πυλώνας;"},
          "a": {"ar": "الزكاة", "en": "Zakat", "de": "Zakat", "fr": "Zakat", "tr": "Zekât", "ru": "Закят", "sv": "Zakat", "nl": "Zakat", "el": "Ζακάτ"},
          "opts": {"ar": ["الزكاة", "الصوم", "الحج"], "en": ["Zakat", "Fasting", "Hajj"], "de": ["Zakat", "Fasten", "Hadsch"], "fr": ["Zakat", "Jeûne", "Hajj"], "tr": ["Zekât", "Oruç", "Hac"], "ru": ["Закят", "Пост", "Хадж"], "sv": ["Zakat", "Fasta", "Hajj"], "nl": ["Zakat", "Vasten", "Hadj"], "el": ["Ζακάτ", "Νηστεία", "Χατζ"]}},
     ]},
    {"id": "r04", "emoji": "📖", "title": {"ar": "مراجعة: القرآن الكريم", "en": "Review: Holy Quran", "de": "Wiederholung: Der Heilige Quran", "fr": "Révision: Le Saint Coran", "tr": "Tekrar: Kur'an-ı Kerim", "ru": "Повторение: Священный Коран", "sv": "Repetition: Den heliga Koranen", "nl": "Herhaling: De Heilige Koran", "el": "Επανάληψη: Το Ιερό Κοράνι"},
     "quiz": [
         {"q": {"ar": "كم سورة في القرآن؟", "en": "How many surahs?", "de": "Wie viele Suren?", "fr": "Combien de sourates?", "tr": "Kaç sure var?", "ru": "Сколько сур?", "sv": "Hur många suror?", "nl": "Hoeveel soera's?", "el": "Πόσες σούρες;"},
          "a": {"ar": "114", "en": "114", "de": "114", "fr": "114", "tr": "114", "ru": "114", "sv": "114", "nl": "114", "el": "114"},
          "opts": {"ar": ["114", "100", "120"], "en": ["114", "100", "120"], "de": ["114", "100", "120"], "fr": ["114", "100", "120"], "tr": ["114", "100", "120"], "ru": ["114", "100", "120"], "sv": ["114", "100", "120"], "nl": ["114", "100", "120"], "el": ["114", "100", "120"]}},
         {"q": {"ar": "ما أول سورة في القرآن؟", "en": "First surah?", "de": "Erste Sure?", "fr": "Première sourate?", "tr": "İlk sure?", "ru": "Первая сура?", "sv": "Första suran?", "nl": "Eerste soera?", "el": "Πρώτη σούρα;"},
          "a": {"ar": "الفاتحة", "en": "Al-Fatiha", "de": "Al-Fatiha", "fr": "Al-Fatiha", "tr": "Fatiha", "ru": "Аль-Фатиха", "sv": "Al-Fatiha", "nl": "Al-Fatiha", "el": "Αλ-Φάτιχα"},
          "opts": {"ar": ["الفاتحة", "البقرة", "الإخلاص"], "en": ["Al-Fatiha", "Al-Baqarah", "Al-Ikhlas"], "de": ["Al-Fatiha", "Al-Baqara", "Al-Ikhlas"], "fr": ["Al-Fatiha", "Al-Baqara", "Al-Ikhlas"], "tr": ["Fatiha", "Bakara", "İhlas"], "ru": ["Аль-Фатиха", "Аль-Бакара", "Аль-Ихлас"], "sv": ["Al-Fatiha", "Al-Baqarah", "Al-Ikhlas"], "nl": ["Al-Fatiha", "Al-Baqara", "Al-Ikhlas"], "el": ["Αλ-Φάτιχα", "Αλ-Μπάκαρα", "Αλ-Ιχλάς"]}},
     ]},
    {"id": "r05", "emoji": "📿", "title": {"ar": "مراجعة: الأنبياء", "en": "Review: Prophets", "de": "Wiederholung: Propheten", "fr": "Révision: Prophètes", "tr": "Tekrar: Peygamberler", "ru": "Повторение: Пророки", "sv": "Repetition: Profeter", "nl": "Herhaling: Profeten", "el": "Επανάληψη: Προφήτες"},
     "quiz": [
         {"q": {"ar": "كم نبيًا ذكر في القرآن؟", "en": "How many prophets in Quran?", "de": "Wie viele Propheten im Quran?", "fr": "Combien de prophètes dans le Coran?", "tr": "Kur'an'da kaç peygamber?", "ru": "Сколько пророков в Коране?", "sv": "Hur många profeter i Koranen?", "nl": "Hoeveel profeten in de Koran?", "el": "Πόσοι προφήτες στο Κοράνι;"},
          "a": {"ar": "25", "en": "25", "de": "25", "fr": "25", "tr": "25", "ru": "25", "sv": "25", "nl": "25", "el": "25"},
          "opts": {"ar": ["25", "20", "30"], "en": ["25", "20", "30"], "de": ["25", "20", "30"], "fr": ["25", "20", "30"], "tr": ["25", "20", "30"], "ru": ["25", "20", "30"], "sv": ["25", "20", "30"], "nl": ["25", "20", "30"], "el": ["25", "20", "30"]}},
         {"q": {"ar": "من خليل الله؟", "en": "Who is Friend of Allah?", "de": "Wer ist der Freund Allahs?", "fr": "Qui est l'ami d'Allah?", "tr": "Allah'ın dostu kimdir?", "ru": "Кто друг Аллаха?", "sv": "Vem är Allahs vän?", "nl": "Wie is de vriend van Allah?", "el": "Ποιος είναι ο φίλος του Αλλάχ;"},
          "a": {"ar": "إبراهيم", "en": "Ibrahim", "de": "Ibrahim", "fr": "Ibrahim", "tr": "İbrahim", "ru": "Ибрахим", "sv": "Ibrahim", "nl": "Ibrahim", "el": "Ιμπραχίμ"},
          "opts": {"ar": ["إبراهيم", "موسى", "عيسى"], "en": ["Ibrahim", "Musa", "Isa"], "de": ["Ibrahim", "Musa", "Isa"], "fr": ["Ibrahim", "Moussa", "Issa"], "tr": ["İbrahim", "Musa", "İsa"], "ru": ["Ибрахим", "Муса", "Иса"], "sv": ["Ibrahim", "Musa", "Isa"], "nl": ["Ibrahim", "Moesa", "Isa"], "el": ["Ιμπραχίμ", "Μούσα", "Ίσα"]}},
     ]},
    {"id": "r06", "emoji": "🤲", "title": {"ar": "مراجعة: الأدعية", "en": "Review: Duas", "de": "Wiederholung: Duas", "fr": "Révision: Invocations", "tr": "Tekrar: Dualar", "ru": "Повторение: Дуа", "sv": "Repetition: Duas", "nl": "Herhaling: Doe'as", "el": "Επανάληψη: Ντουά"},
     "quiz": [
         {"q": {"ar": "ماذا نقول قبل الأكل؟", "en": "What do we say before eating?", "de": "Was sagen wir vor dem Essen?", "fr": "Que disons-nous avant de manger?", "tr": "Yemekten önce ne deriz?", "ru": "Что мы говорим перед едой?", "sv": "Vad säger vi före maten?", "nl": "Wat zeggen we voor het eten?", "el": "Τι λέμε πριν φάμε;"},
          "a": {"ar": "بسم الله", "en": "Bismillah", "de": "Bismillah", "fr": "Bismillah", "tr": "Bismillah", "ru": "Бисмиллях", "sv": "Bismillah", "nl": "Bismillah", "el": "Μπισμιλλάχ"},
          "opts": {"ar": ["بسم الله", "الحمد لله", "سبحان الله"], "en": ["Bismillah", "Alhamdulillah", "SubhanAllah"], "de": ["Bismillah", "Alhamdulillah", "SubhanAllah"], "fr": ["Bismillah", "Alhamdoulillah", "SoubhanAllah"], "tr": ["Bismillah", "Elhamdülillah", "Sübhanallah"], "ru": ["Бисмиллях", "Альхамдулиллях", "Субханаллах"], "sv": ["Bismillah", "Alhamdulillah", "SubhanAllah"], "nl": ["Bismillah", "Alhamdulillah", "SubhanAllah"], "el": ["Μπισμιλλάχ", "Αλχαμντουλιλλάχ", "Σουμπχαναλλάχ"]}},
         {"q": {"ar": "ماذا نقول بعد الأكل؟", "en": "After eating?", "de": "Nach dem Essen?", "fr": "Après manger?", "tr": "Yemekten sonra?", "ru": "После еды?", "sv": "Efter maten?", "nl": "Na het eten?", "el": "Μετά το φαγητό;"},
          "a": {"ar": "الحمد لله", "en": "Alhamdulillah", "de": "Alhamdulillah", "fr": "Alhamdoulillah", "tr": "Elhamdülillah", "ru": "Альхамдулиллях", "sv": "Alhamdulillah", "nl": "Alhamdulillah", "el": "Αλχαμντουλιλλάχ"},
          "opts": {"ar": ["الحمد لله", "بسم الله", "الله أكبر"], "en": ["Alhamdulillah", "Bismillah", "Allahu Akbar"], "de": ["Alhamdulillah", "Bismillah", "Allahu Akbar"], "fr": ["Alhamdoulillah", "Bismillah", "Allahou Akbar"], "tr": ["Elhamdülillah", "Bismillah", "Allahu Ekber"], "ru": ["Альхамдулиллях", "Бисмиллях", "Аллаху Акбар"], "sv": ["Alhamdulillah", "Bismillah", "Allahu Akbar"], "nl": ["Alhamdulillah", "Bismillah", "Allahu Akbar"], "el": ["Αλχαμντουλιλλάχ", "Μπισμιλλάχ", "Αλλάχου Άκμπαρ"]}},
     ]},
]


# ═══════════════════════════════════════════════════════════════
# MAIN BUILDER FUNCTION - Replaces the thin _build_advanced_sections
# ═══════════════════════════════════════════════════════════════

def _build_stage_reading(lesson_idx: int, lang: str) -> list:
    """Stage 6: Reading Practice sections."""
    passage = READING_PASSAGES[lesson_idx % len(READING_PASSAGES)]
    ar_text, en_text = passage["ar"], passage["en"]
    return [
        {"type": "read", "emoji": "📖", "title": t("read_word", lang),
         "content": {"arabic": ar_text, "translated": en_text if lang != "ar" else "", "emoji": passage["emoji"]}},
        {"type": "listen", "emoji": "🔊", "title": t("listen_repeat", lang),
         "content": {"text": ar_text, "tip": t("tip_repeat_sentence", lang)}},
        {"type": "quiz", "emoji": "❓", "title": t("test_yourself", lang),
         "content": {"question": passage.get(f"question_{lang}", passage.get("question_en", passage["question_ar"])),
                     "correct": passage.get(f"answer_{lang}", passage.get("answer_en", passage["answer_ar"])),
                     "options": passage.get(f"options_{lang}", passage.get("options_en", passage["options_ar"]))}},
        {"type": "write", "emoji": "✍️", "title": t("practice_writing", lang),
         "content": {"sentence": ar_text, "tip": t("tip_write_sentence_3", lang)}},
    ]


def _build_stage_islamic(lesson_idx: int, lang: str) -> list:
    """Stage 7: Islamic Foundations sections."""
    topic = ISLAMIC_FOUNDATIONS_DETAILED[lesson_idx % len(ISLAMIC_FOUNDATIONS_DETAILED)]
    title_text = topic["title"].get(lang, topic["title"].get("en", topic["title"]["ar"]))
    content_text = topic["content"].get(lang, topic["content"].get("en", topic["content"]["ar"]))
    memorize_text = topic["memorize"].get(lang, topic["memorize"].get("en", topic["memorize"]["ar"]))
    return [
        {"type": "learn", "emoji": topic["emoji"], "title": title_text,
         "content": {"arabic": topic["content"]["ar"], "translated": content_text if lang != "ar" else ""}},
        {"type": "memorize", "emoji": "🧠", "title": t("memorize", lang),
         "content": {"text": topic["memorize"]["ar"], "tip": memorize_text if lang != "ar" else t("tip_read_3_memory", lang)}},
        {"type": "quiz", "emoji": "❓", "title": t("test_yourself", lang),
         "content": {"question": topic["quiz_q"].get(lang, topic["quiz_q"].get("en", topic["quiz_q"]["ar"])),
                     "correct": topic["quiz_a"].get(lang, topic["quiz_a"].get("en", topic["quiz_a"]["ar"])),
                     "options": topic["quiz_opts"].get(lang, topic["quiz_opts"].get("en", topic["quiz_opts"]["ar"]))}},
    ]


def _build_stage_quran(lesson_idx: int, lang: str) -> list:
    """Stage 8: Quran Memorization sections."""
    from kids_learning import QURAN_SURAHS_FOR_KIDS
    all_surahs = QURAN_SURAHS_FOR_KIDS + ADDITIONAL_SURAHS
    s_idx, a_idx = lesson_idx // 7, lesson_idx % 7
    if s_idx >= len(all_surahs):
        return [{"type": "review", "emoji": "🔄", "title": t("review", lang), "content": {"tip": t("tip_review_all", lang)}}]
    surah = all_surahs[s_idx]
    ayah = surah["ayahs"][a_idx % len(surah["ayahs"])]
    return [
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


def _build_stage_duas(lesson_idx: int, lang: str) -> list:
    """Stage 9: Duas sections."""
    from kids_learning import KIDS_DUAS
    d = KIDS_DUAS[lesson_idx % len(KIDS_DUAS)]
    quiz_q = t("quiz_complete_dua", lang)
    if quiz_q == "quiz_complete_dua":
        quiz_q = {"ar": "أكمل الدعاء", "en": "Complete the dua"}.get(lang, "أكمل الدعاء")
    return [
        {"type": "dua", "emoji": d["emoji"], "title": d["title"].get(lang, d["title"]["ar"]),
         "content": {"arabic": d["ar"], "transliteration": d["transliteration"], "meaning": d.get(lang, d.get("en", ""))}},
        {"type": "listen", "emoji": "🔊", "title": t("listen_repeat", lang),
         "content": {"text": d["ar"], "tip": t("tip_repeat_sentence", lang)}},
        {"type": "memorize", "emoji": "🧠", "title": t("memorize_dua", lang),
         "content": {"text": d["ar"], "tip": t("tip_repeat_dua_5", lang)}},
        {"type": "quiz", "emoji": "❓", "title": t("test_yourself", lang),
         "content": {"question": quiz_q, "correct": d["ar"][:30],
                     "options": [d["ar"][:30], KIDS_DUAS[(lesson_idx+1) % len(KIDS_DUAS)]["ar"][:30], KIDS_DUAS[(lesson_idx+2) % len(KIDS_DUAS)]["ar"][:30]]}},
    ]


def _build_stage_hadiths(lesson_idx: int, lang: str) -> list:
    """Stage 10: Hadiths sections."""
    from kids_learning import KIDS_HADITHS
    h = KIDS_HADITHS[lesson_idx % len(KIDS_HADITHS)]
    return [
        {"type": "hadith", "emoji": h["emoji"], "title": t("todays_hadith", lang),
         "content": {"arabic": h["ar"], "translation": h.get(lang, h.get("en", "")), "source": h["source"],
                     "lesson": h["lesson"].get(lang, h["lesson"].get("en", ""))}},
        {"type": "memorize", "emoji": "🧠", "title": t("memorize", lang),
         "content": {"text": h["ar"], "tip": t("tip_read_3_memory", lang)}},
        {"type": "reflect", "emoji": "💭", "title": t("reflect", lang),
         "content": {"tip": h["lesson"].get(lang, h["lesson"].get("en", ""))}},
    ]


def _build_stage_prophets(lesson_idx: int, lang: str) -> list:
    """Stage 11: Prophet Stories sections."""
    from kids_learning_extended import ALL_PROPHETS, get_prophet_field
    p = ALL_PROPHETS[lesson_idx % len(ALL_PROPHETS)]
    p_name = get_prophet_field(p, "name", lang) or p["name"].get(lang, p["name"].get("ar", ""))
    p_title = get_prophet_field(p, "title", lang) or p["title"].get(lang, p["title"].get("ar", ""))
    p_summary = get_prophet_field(p, "summary", lang)
    p_lesson = get_prophet_field(p, "lesson", lang)
    return [
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


def _build_stage_islamic_life(lesson_idx: int, lang: str) -> list:
    """Stage 12: Islamic Life sections."""
    topic = ISLAMIC_LIFE_TOPICS[lesson_idx % len(ISLAMIC_LIFE_TOPICS)]
    content_text = topic["content"].get(lang, topic["content"].get("en", topic["content"]["ar"]))
    return [
        {"type": "learn", "emoji": topic["emoji"], "title": topic["title"].get(lang, topic["title"].get("en", topic["title"]["ar"])),
         "content": {"arabic": topic["content"]["ar"], "translated": content_text if lang != "ar" else ""}},
        {"type": "listen", "emoji": "🔊", "title": t("listen_repeat", lang),
         "content": {"text": topic["content"]["ar"][:80], "tip": t("tip_repeat_sentence", lang)}},
        {"type": "memorize", "emoji": "🧠", "title": t("memorize", lang),
         "content": {"text": topic["content"]["ar"][:80], "tip": t("tip_read_3_memory", lang)}},
    ]


def _build_stage_grammar(lesson_idx: int, lang: str) -> list:
    """Stage 13: Advanced Arabic Grammar sections."""
    grammar = ARABIC_GRAMMAR_LESSONS[lesson_idx % len(ARABIC_GRAMMAR_LESSONS)]
    content_text = grammar["content"].get(lang, grammar["content"].get("en", grammar["content"]["ar"]))
    sections = [
        {"type": "learn", "emoji": grammar["emoji"],
         "title": grammar["title"].get(lang, grammar["title"].get("en", grammar["title"]["ar"])),
         "content": {"arabic": grammar["content"]["ar"], "translated": content_text if lang != "ar" else ""}},
    ]
    if grammar.get("practice"):
        items = _extract_practice_items(grammar["practice"])
        if items:
            sections.append({"type": "practice", "emoji": "🎯", "title": t("test", lang), "content": {"items": items, "tip": t("listen_repeat", lang)}})
    sections.append({"type": "write", "emoji": "✍️", "title": t("practice_writing", lang), "content": {"tip": t("tip_write_sentence_3", lang)}})
    return sections


def _extract_practice_items(practice_list: list) -> list:
    """Extract practice items from grammar practice data."""
    items = []
    for p in practice_list:
        if "word" in p:
            items.append(p.get("word", "") + " → " + p.get("plural", p.get("opposite", "")))
        elif "past" in p:
            items.append(p["past"] + " → " + p["present"] + " → " + p["command"])
        elif "sentence" in p:
            items.append(p["sentence"])
        elif "question" in p:
            items.append(p["question"] + " — " + p["answer"])
        elif "pronoun" in p:
            items.append(p["pronoun"] + ": " + p["example"])
        elif "day" in p:
            items.append(p["day"])
    return items


def _build_stage_advanced_quran(lesson_idx: int, lang: str) -> list:
    """Stage 14: Advanced Quran + Tajweed sections."""
    half = 30
    if lesson_idx < half:
        from kids_learning import QURAN_SURAHS_FOR_KIDS
        all_surahs = QURAN_SURAHS_FOR_KIDS + ADDITIONAL_SURAHS
        s_idx, a_idx = lesson_idx // 5, lesson_idx % 5
        if s_idx >= len(all_surahs):
            return [{"type": "review", "emoji": "🔄", "title": t("review", lang), "content": {"tip": t("tip_review_all", lang)}}]
        surah = all_surahs[s_idx % len(all_surahs)]
        ayah = surah["ayahs"][a_idx % len(surah["ayahs"])]
        return [
            {"type": "quran", "emoji": "📖", "title": t("memorize_prefix", lang, name=surah.get('name_ar', surah['name_en'])),
             "content": {"surah": surah.get("name_ar", surah["name_en"]), "ayah_num": ayah["num"],
                         "arabic": ayah["ar"], "translation": ayah.get(lang, ayah.get("en", ""))}},
            {"type": "listen", "emoji": "🔊", "title": t("listen_repeat", lang), "content": {"text": ayah["ar"]}},
            {"type": "memorize", "emoji": "🧠", "title": t("recite", lang), "content": {"tip": t("tip_close_eyes_recite", lang)}},
        ]
    rule = TAJWEED_RULES[(lesson_idx - half) % len(TAJWEED_RULES)]
    return [
        {"type": "learn", "emoji": rule["emoji"], "title": rule["title"].get(lang, rule["title"]["ar"]),
         "content": {"arabic": rule["content"]["ar"], "translated": rule["content"].get(lang, rule["content"]["ar"]) if lang != "ar" else ""}},
        {"type": "practice", "emoji": "🎯", "title": t("test", lang),
         "content": {"tip": rule["content"].get(lang, rule["content"]["ar"])}},
    ]


def _build_stage_mastery(lesson_idx: int, lang: str) -> list:
    """Stage 15: Mastery & Graduation sections."""
    review = MASTERY_REVIEWS[lesson_idx % len(MASTERY_REVIEWS)]
    sections = [
        {"type": "review", "emoji": review["emoji"], "title": review["title"].get(lang, review["title"]["ar"]),
         "content": {"tip": t("tip_review_all", lang)}},
    ]
    quiz_items = review["quiz"]
    if quiz_items:
        quiz = quiz_items[lesson_idx % len(quiz_items)]
        sections.append({"type": "quiz", "emoji": "❓", "title": t("test_yourself", lang),
             "content": {"question": quiz["q"].get(lang, quiz["q"]["ar"]),
                         "correct": quiz["a"].get(lang, quiz["a"]["ar"]),
                         "options": quiz["opts"].get(lang, quiz["opts"]["ar"])}})
    sections.append({"type": "memorize", "emoji": "🎓", "title": t("comprehensive_review", lang),
         "content": {"tip": t("tip_review_all", lang)}})
    return sections


# Stage builder dispatch table
_STAGE_BUILDERS: dict = {
    "S06": _build_stage_reading,
    "S07": _build_stage_islamic,
    "S08": _build_stage_quran,
    "S09": _build_stage_duas,
    "S10": _build_stage_hadiths,
    "S11": _build_stage_prophets,
    "S12": _build_stage_islamic_life,
    "S13": _build_stage_grammar,
    "S14": _build_stage_advanced_quran,
    "S15": _build_stage_mastery,
}


def build_rich_sections(stage_id: str, lesson_idx: int, lang: str) -> list:
    """Build comprehensive multi-section lessons for stages 6-15.
    
    Dispatches to stage-specific builder functions for maintainability.
    """
    builder = _STAGE_BUILDERS.get(stage_id)
    if builder:
        return builder(lesson_idx, lang)
    return [{"type": "learn", "emoji": "📝", "title": t("lesson", lang), "content": {"tip": t("learn", lang)}}]
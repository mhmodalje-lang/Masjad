"""
Kids Learning Extended Content - Part 2
=======================================
- All 25 Prophets
- More Surahs (Complete Juz Amma)
- Wudu & Salah Learning
- Arabic Alphabet Course
- Arabic Vocabulary (Numbers, Colors, Animals, Body, Family)
- More Duas, Hadiths
- Achievement/Badge System
"""

# ═══════════════════════════════════════════════════════════════
# ALL 25 PROPHETS MENTIONED IN QURAN
# ═══════════════════════════════════════════════════════════════

ALL_PROPHETS = [
    {"id": "adam", "number": 1, "emoji": "🌍",
     "name": {"ar": "آدم", "en": "Adam", "de": "Adam", "fr": "Adam", "tr": "Adem", "ru": "Адам"},
     "title": {"ar": "أبو البشرية", "en": "Father of Humanity", "de": "Vater der Menschheit", "fr": "Père de l'Humanité", "tr": "İnsanlığın Babası", "ru": "Отец человечества"},
     "summary": {"ar": "خلق الله آدم من طين وعلمه أسماء كل شيء. كان أول إنسان وأول نبي. سكن الجنة مع حواء ثم نزل إلى الأرض", "en": "Allah created Adam from clay and taught him the names of all things. He was the first human and first prophet. He lived in Paradise with Hawwa then came to Earth"},
     "lesson": {"ar": "التوبة والاستغفار", "en": "Repentance and seeking forgiveness"},
     "quran_ref": "البقرة 30-38"},
    {"id": "idris", "number": 2, "emoji": "📝",
     "name": {"ar": "إدريس", "en": "Idris (Enoch)", "de": "Idris (Henoch)", "fr": "Idris (Hénoch)", "tr": "İdris", "ru": "Идрис (Енох)"},
     "title": {"ar": "أول من خط بالقلم", "en": "First to Write with a Pen", "de": "Der Erste, der mit einem Stift schrieb", "fr": "Le premier à écrire avec un stylo", "tr": "Kalemle yazan ilk kişi", "ru": "Первый, кто писал пером"},
     "summary": {"ar": "كان صادقاً صبوراً ورفعه الله مكاناً علياً. كان أول من خطّ بالقلم وأول من خاط الثياب", "en": "He was truthful and patient, and Allah raised him to a high station. He was the first to write with a pen and the first to sew clothes"},
     "lesson": {"ar": "طلب العلم والصبر", "en": "Seeking knowledge and patience"},
     "quran_ref": "مريم 56-57"},
    {"id": "nuh", "number": 3, "emoji": "🚢",
     "name": {"ar": "نوح", "en": "Nuh (Noah)", "de": "Nuh (Noah)", "fr": "Nouh (Noé)", "tr": "Nuh", "ru": "Нух (Ной)"},
     "title": {"ar": "صاحب السفينة", "en": "Builder of the Ark", "de": "Erbauer der Arche", "fr": "Constructeur de l'Arche", "tr": "Geminin Sahibi", "ru": "Строитель Ковчега"},
     "summary": {"ar": "دعا قومه 950 سنة إلى عبادة الله. بنى سفينة كبيرة بأمر الله وحمل فيها من كل زوجين اثنين. جاء الطوفان وغرق الكافرون", "en": "He called his people to worship Allah for 950 years. He built a great ark by Allah's command and carried pairs of every creature. The flood came and the disbelievers drowned"},
     "lesson": {"ar": "الصبر والمثابرة", "en": "Patience and perseverance"},
     "quran_ref": "هود 25-49"},
    {"id": "hud", "number": 4, "emoji": "🏜️",
     "name": {"ar": "هود", "en": "Hud", "de": "Hud", "fr": "Houd", "tr": "Hud", "ru": "Худ"},
     "title": {"ar": "نبي قوم عاد", "en": "Prophet to the People of 'Ad", "de": "Prophet des Volkes 'Ad", "fr": "Prophète du peuple de 'Ad", "tr": "Ad Kavminin Peygamberi", "ru": "Пророк народа Ад"},
     "summary": {"ar": "أرسل إلى قوم عاد الذين كانوا أقوياء وبنوا مباني عالية. دعاهم لعبادة الله فرفضوا فأهلكهم الله بريح شديدة", "en": "Sent to the people of 'Ad who were strong and built tall buildings. He called them to worship Allah but they refused, so Allah destroyed them with a fierce wind"},
     "lesson": {"ar": "عدم التكبر", "en": "Humility, no arrogance"},
     "quran_ref": "هود 50-60"},
    {"id": "salih", "number": 5, "emoji": "🐫",
     "name": {"ar": "صالح", "en": "Salih", "de": "Salih", "fr": "Salih", "tr": "Salih", "ru": "Салих"},
     "title": {"ar": "نبي قوم ثمود", "en": "Prophet to Thamud", "de": "Prophet der Thamud", "fr": "Prophète de Thamoud", "tr": "Semud Kavminin Peygamberi", "ru": "Пророк самудян"},
     "summary": {"ar": "أرسل إلى قوم ثمود وأعطاه الله ناقة كمعجزة. حذرهم من إيذائها لكنهم عقروها فأهلكهم الله بصيحة", "en": "Sent to Thamud. Allah gave him a she-camel as a miracle. He warned them not to harm it but they killed it, so Allah destroyed them with a mighty blast"},
     "lesson": {"ar": "احترام آيات الله", "en": "Respecting Allah's signs"},
     "quran_ref": "هود 61-68"},
    {"id": "ibrahim", "number": 6, "emoji": "🕋",
     "name": {"ar": "إبراهيم", "en": "Ibrahim (Abraham)", "de": "Ibrahim (Abraham)", "fr": "Ibrahim (Abraham)", "tr": "İbrahim", "ru": "Ибрахим (Авраам)"},
     "title": {"ar": "خليل الله", "en": "Friend of Allah", "de": "Freund Allahs", "fr": "Ami d'Allah", "tr": "Allah'ın Dostu", "ru": "Друг Аллаха"},
     "summary": {"ar": "كسر الأصنام وحده ودعا إلى توحيد الله. ألقي في النار فجعلها الله برداً وسلاماً. بنى الكعبة مع ابنه إسماعيل", "en": "He broke the idols alone and called to the worship of One God. He was thrown into fire but Allah made it cool and peaceful. He built the Kaaba with his son Ismail"},
     "lesson": {"ar": "الشجاعة في الحق", "en": "Courage for truth"},
     "quran_ref": "الأنبياء 51-70"},
    {"id": "lut", "number": 7, "emoji": "🌆",
     "name": {"ar": "لوط", "en": "Lut (Lot)", "de": "Lut (Lot)", "fr": "Lout (Lot)", "tr": "Lut", "ru": "Лут (Лот)"},
     "title": {"ar": "نبي قوم سدوم", "en": "Prophet to Sodom", "de": "Prophet von Sodom", "fr": "Prophète de Sodome", "tr": "Sodom Peygamberi", "ru": "Пророк Содома"},
     "summary": {"ar": "ابن أخي إبراهيم. أرسل إلى قوم يفعلون المنكرات. دعاهم للتوبة فرفضوا فأهلكهم الله", "en": "Ibrahim's nephew. Sent to people who committed great sins. He called them to repent but they refused, so Allah destroyed them"},
     "lesson": {"ar": "الابتعاد عن المعاصي", "en": "Staying away from sin"},
     "quran_ref": "هود 77-83"},
    {"id": "ismail", "number": 8, "emoji": "🐑",
     "name": {"ar": "إسماعيل", "en": "Ismail (Ishmael)", "de": "Ismail (Ismael)", "fr": "Ismaïl (Ismaël)", "tr": "İsmail", "ru": "Исмаил (Измаил)"},
     "title": {"ar": "الذبيح", "en": "The Sacrifice", "de": "Das Opfer", "fr": "Le Sacrifice", "tr": "Kurban", "ru": "Жертва"},
     "summary": {"ar": "ابن إبراهيم. صبر عندما أمر الله أباه بذبحه ففداه الله بكبش عظيم. ساعد أباه في بناء الكعبة", "en": "Son of Ibrahim. He was patient when Allah commanded his father to sacrifice him. Allah replaced him with a great ram. He helped build the Kaaba"},
     "lesson": {"ar": "الطاعة والتسليم لله", "en": "Obedience and submission to Allah"},
     "quran_ref": "الصافات 100-111"},
    {"id": "ishaq", "number": 9, "emoji": "🌟",
     "name": {"ar": "إسحاق", "en": "Ishaq (Isaac)", "de": "Ishaq (Isaak)", "fr": "Ishaq (Isaac)", "tr": "İshak", "ru": "Исхак (Исаак)"},
     "title": {"ar": "ابن إبراهيم الثاني", "en": "Second Son of Ibrahim", "de": "Zweiter Sohn Ibrahims", "fr": "Deuxième fils d'Ibrahim", "tr": "İbrahim'in İkinci Oğlu", "ru": "Второй сын Ибрахима"},
     "summary": {"ar": "ابن إبراهيم من سارة. بشّر الله به إبراهيم وسارة وهما كبيران في السن. كان نبياً صالحاً", "en": "Son of Ibrahim and Sarah. Allah gave glad tidings of him to Ibrahim and Sarah in their old age. He was a righteous prophet"},
     "lesson": {"ar": "لا شيء مستحيل عند الله", "en": "Nothing is impossible for Allah"},
     "quran_ref": "هود 71-73"},
    {"id": "yaqub", "number": 10, "emoji": "👨‍👦‍👦",
     "name": {"ar": "يعقوب", "en": "Yaqub (Jacob)", "de": "Yaqub (Jakob)", "fr": "Yacoub (Jacob)", "tr": "Yakub", "ru": "Якуб (Иаков)"},
     "title": {"ar": "إسرائيل", "en": "Israel", "de": "Israel", "fr": "Israël", "tr": "İsrail", "ru": "Израиль"},
     "summary": {"ar": "ابن إسحاق وأبو يوسف. صبر على فراق ابنه يوسف سنوات طويلة حتى فقد بصره من كثرة البكاء ثم رد الله بصره", "en": "Son of Ishaq and father of Yusuf. He patiently bore separation from Yusuf for many years until he lost his sight from crying, then Allah restored it"},
     "lesson": {"ar": "الصبر الجميل", "en": "Beautiful patience"},
     "quran_ref": "يوسف 84-87"},
    {"id": "yusuf", "number": 11, "emoji": "⭐",
     "name": {"ar": "يوسف", "en": "Yusuf (Joseph)", "de": "Yusuf (Josef)", "fr": "Youssouf (Joseph)", "tr": "Yusuf", "ru": "Юсуф (Иосиф)"},
     "title": {"ar": "الصديق", "en": "The Truthful", "de": "Der Wahrhaftige", "fr": "Le Véridique", "tr": "Sıddık", "ru": "Правдивый"},
     "summary": {"ar": "رأى في المنام أحد عشر كوكباً تسجد له. ألقاه إخوته في البئر فأنقذه الله. صبر في السجن ثم أصبح عزيز مصر", "en": "He dreamt of eleven stars bowing to him. His brothers threw him in a well but Allah saved him. He was patient in prison then became the minister of Egypt"},
     "lesson": {"ar": "الصبر على البلاء", "en": "Patience through trials"},
     "quran_ref": "يوسف 1-111"},
    {"id": "ayyub", "number": 12, "emoji": "💪",
     "name": {"ar": "أيوب", "en": "Ayyub (Job)", "de": "Ayyub (Hiob)", "fr": "Ayyoub (Job)", "tr": "Eyyüp", "ru": "Айюб (Иов)"},
     "title": {"ar": "الصابر", "en": "The Patient One", "de": "Der Geduldige", "fr": "Le Patient", "tr": "Sabreden", "ru": "Терпеливый"},
     "summary": {"ar": "ابتلاه الله بالمرض وفقد المال والأولاد فصبر ولم يشتكِ. شفاه الله وأعاد إليه كل شيء مضاعفاً", "en": "Allah tested him with illness, loss of wealth and children. He was patient and never complained. Allah healed him and restored everything doubled"},
     "lesson": {"ar": "الصبر على الابتلاء", "en": "Patience in hardship"},
     "quran_ref": "الأنبياء 83-84"},
    {"id": "shuayb", "number": 13, "emoji": "⚖️",
     "name": {"ar": "شعيب", "en": "Shu'ayb", "de": "Schu'aib", "fr": "Chou'ayb", "tr": "Şuayb", "ru": "Шуайб"},
     "title": {"ar": "خطيب الأنبياء", "en": "Orator of the Prophets", "de": "Redner der Propheten", "fr": "Orateur des Prophètes", "tr": "Peygamberlerin Hatibi", "ru": "Оратор пророков"},
     "summary": {"ar": "أرسل إلى أهل مدين الذين كانوا يغشون في الميزان. دعاهم للعدل والأمانة فرفضوا فأهلكهم الله", "en": "Sent to the people of Madyan who cheated in trade. He called them to justice and honesty but they refused, so Allah destroyed them"},
     "lesson": {"ar": "الأمانة في التعامل", "en": "Honesty in dealings"},
     "quran_ref": "هود 84-95"},
    {"id": "musa", "number": 14, "emoji": "🌊",
     "name": {"ar": "موسى", "en": "Musa (Moses)", "de": "Musa (Moses)", "fr": "Moussa (Moïse)", "tr": "Musa", "ru": "Муса (Моисей)"},
     "title": {"ar": "كليم الله", "en": "One Who Spoke to Allah", "de": "Der zu Allah sprach", "fr": "Celui qui a parlé à Allah", "tr": "Allah'ın Kelimi", "ru": "Собеседник Аллаха"},
     "summary": {"ar": "وُلد في زمن فرعون الظالم. وضعته أمه في النهر فأنقذه الله. كلّمه الله وأعطاه تسع آيات. شقّ البحر ونجا بقومه", "en": "Born during the time of the tyrant Pharaoh. His mother placed him in the river and Allah saved him. Allah spoke to him and gave him nine signs. He split the sea and saved his people"},
     "lesson": {"ar": "التوكل على الله", "en": "Trust in Allah"},
     "quran_ref": "القصص 1-43"},
    {"id": "harun", "number": 15, "emoji": "🗣️",
     "name": {"ar": "هارون", "en": "Harun (Aaron)", "de": "Harun (Aaron)", "fr": "Haroun (Aaron)", "tr": "Harun", "ru": "Харун (Аарон)"},
     "title": {"ar": "وزير موسى", "en": "Minister of Musa", "de": "Minister von Musa", "fr": "Ministre de Moussa", "tr": "Musa'nın Veziri", "ru": "Помощник Мусы"},
     "summary": {"ar": "أخو موسى وساعده في الدعوة إلى الله. كان فصيح اللسان وطلب موسى من الله أن يكون معه في مواجهة فرعون", "en": "Brother of Musa and helped him in calling to Allah. He was eloquent and Musa asked Allah to send him as support against Pharaoh"},
     "lesson": {"ar": "التعاون على الخير", "en": "Cooperation in goodness"},
     "quran_ref": "طه 29-36"},
    {"id": "dhulkifl", "number": 16, "emoji": "🛡️",
     "name": {"ar": "ذو الكفل", "en": "Dhul-Kifl", "de": "Dhul-Kifl", "fr": "Dhoul-Kifl", "tr": "Zülkifl", "ru": "Зуль-Кифль"},
     "title": {"ar": "الصابر الشاكر", "en": "The Patient & Grateful", "de": "Der Geduldige & Dankbare", "fr": "Le Patient & Reconnaissant", "tr": "Sabreden & Şükreden", "ru": "Терпеливый и благодарный"},
     "summary": {"ar": "كان من الصابرين والأخيار. ذكره الله في القرآن مع الأنبياء وأثنى عليه", "en": "He was among the patient and the righteous. Allah mentioned him in the Quran among the prophets and praised him"},
     "lesson": {"ar": "الصبر والوفاء بالعهد", "en": "Patience and keeping promises"},
     "quran_ref": "الأنبياء 85-86"},
    {"id": "dawud", "number": 17, "emoji": "🎵",
     "name": {"ar": "داوود", "en": "Dawud (David)", "de": "Dawud (David)", "fr": "Dawoud (David)", "tr": "Davud", "ru": "Дауд (Давид)"},
     "title": {"ar": "صاحب الزبور", "en": "Given the Psalms", "de": "Empfänger der Psalmen", "fr": "Détenteur des Psaumes", "tr": "Zebur'un Sahibi", "ru": "Обладатель Забура"},
     "summary": {"ar": "كان ملكاً ونبياً. أعطاه الله صوتاً جميلاً كانت الجبال والطيور تسبح معه. علمه الله صنع الدروع وأنزل عليه الزبور", "en": "He was a king and prophet. Allah gave him a beautiful voice - mountains and birds praised Allah with him. Allah taught him to make armor and revealed the Psalms to him"},
     "lesson": {"ar": "شكر النعم", "en": "Being grateful for blessings"},
     "quran_ref": "سبأ 10-11"},
    {"id": "sulayman", "number": 18, "emoji": "👑",
     "name": {"ar": "سليمان", "en": "Sulayman (Solomon)", "de": "Sulayman (Salomo)", "fr": "Soulayman (Salomon)", "tr": "Süleyman", "ru": "Сулейман (Соломон)"},
     "title": {"ar": "ملك الجن والإنس", "en": "King of Jinn and Men", "de": "König der Dschinn und Menschen", "fr": "Roi des Djinns et des Hommes", "tr": "Cin ve İnsanların Kralı", "ru": "Царь джиннов и людей"},
     "summary": {"ar": "ابن داوود. سخر الله له الريح والجن والطير. كان يفهم لغة النمل والطيور. بنى مملكة عظيمة", "en": "Son of Dawud. Allah subjected the wind, jinn and birds to him. He understood the language of ants and birds. He built a great kingdom"},
     "lesson": {"ar": "التواضع رغم القوة", "en": "Humility despite power"},
     "quran_ref": "النمل 15-44"},
    {"id": "ilyas", "number": 19, "emoji": "⛰️",
     "name": {"ar": "إلياس", "en": "Ilyas (Elijah)", "de": "Ilyas (Elias)", "fr": "Ilyas (Élie)", "tr": "İlyas", "ru": "Ильяс (Илия)"},
     "title": {"ar": "المرسل إلى بعلبك", "en": "Sent to Baalbek", "de": "Gesandt nach Baalbek", "fr": "Envoyé à Baalbek", "tr": "Baalbek'e Gönderilen", "ru": "Посланный в Баальбек"},
     "summary": {"ar": "دعا قومه لترك عبادة صنم يسمى بعل والعودة إلى عبادة الله الواحد", "en": "He called his people to leave the worship of an idol called Ba'l and return to worshipping Allah alone"},
     "lesson": {"ar": "التمسك بالتوحيد", "en": "Holding firm to monotheism"},
     "quran_ref": "الصافات 123-132"},
    {"id": "alyasa", "number": 20, "emoji": "🌿",
     "name": {"ar": "اليسع", "en": "Al-Yasa (Elisha)", "de": "Al-Yasa (Elischa)", "fr": "Al-Yasa (Élisée)", "tr": "Elyesa", "ru": "Аль-Яса (Елисей)"},
     "title": {"ar": "من الأخيار", "en": "Among the Righteous", "de": "Unter den Rechtschaffenen", "fr": "Parmi les Justes", "tr": "İyilerden", "ru": "Среди праведных"},
     "summary": {"ar": "ذكره الله في القرآن وفضله على العالمين. كان من الأخيار والصابرين", "en": "Allah mentioned him in the Quran and favored him above all. He was among the righteous and patient"},
     "lesson": {"ar": "فضل الأخيار", "en": "Virtue of the righteous"},
     "quran_ref": "الأنعام 86"},
    {"id": "yunus", "number": 21, "emoji": "🐋",
     "name": {"ar": "يونس", "en": "Yunus (Jonah)", "de": "Yunus (Jona)", "fr": "Younous (Jonas)", "tr": "Yunus", "ru": "Юнус (Иона)"},
     "title": {"ar": "صاحب الحوت", "en": "Companion of the Whale", "de": "Gefährte des Wals", "fr": "Compagnon de la Baleine", "tr": "Balık Sahibi", "ru": "Спутник кита"},
     "summary": {"ar": "غضب من قومه وركب السفينة. ابتلعه الحوت فدعا الله في ظلمات ثلاث: لا إله إلا أنت سبحانك إني كنت من الظالمين. فأنجاه الله", "en": "He was angry with his people and boarded a ship. A whale swallowed him. He called upon Allah in three layers of darkness: There is no god but You, glory be to You, I was among the wrongdoers. Allah saved him"},
     "lesson": {"ar": "الاستغفار والتوبة", "en": "Seeking forgiveness and repentance"},
     "quran_ref": "الأنبياء 87-88"},
    {"id": "zakariya", "number": 22, "emoji": "🤲",
     "name": {"ar": "زكريا", "en": "Zakariya (Zechariah)", "de": "Zakariya (Zacharias)", "fr": "Zakaria (Zacharie)", "tr": "Zekeriya", "ru": "Закария (Захария)"},
     "title": {"ar": "كافل مريم", "en": "Guardian of Maryam", "de": "Vormund Maryams", "fr": "Tuteur de Maryam", "tr": "Meryem'in Bakıcısı", "ru": "Опекун Марьям"},
     "summary": {"ar": "كفل مريم أم عيسى. دعا الله أن يرزقه ولداً وهو كبير فاستجاب الله وبشره بيحيى", "en": "He was guardian of Maryam, mother of Isa. He prayed to Allah for a child in his old age and Allah answered, giving him glad tidings of Yahya"},
     "lesson": {"ar": "لا تيأس من رحمة الله", "en": "Never despair of Allah's mercy"},
     "quran_ref": "آل عمران 37-41"},
    {"id": "yahya", "number": 23, "emoji": "🕊️",
     "name": {"ar": "يحيى", "en": "Yahya (John)", "de": "Yahya (Johannes)", "fr": "Yahya (Jean)", "tr": "Yahya", "ru": "Яхья (Иоанн)"},
     "title": {"ar": "الحصور", "en": "The Noble & Chaste", "de": "Der Edle & Keusche", "fr": "Le Noble & Chaste", "tr": "İffetli", "ru": "Благородный и целомудренный"},
     "summary": {"ar": "ابن زكريا. كان تقياً زاهداً يحب الناس والحيوانات. سماه الله يحيى وهو أول من سُمي بهذا الاسم", "en": "Son of Zakariya. He was pious and ascetic, loved people and animals. Allah named him Yahya - the first to bear this name"},
     "lesson": {"ar": "الزهد وحب الخير", "en": "Piety and love of goodness"},
     "quran_ref": "مريم 12-15"},
    {"id": "isa", "number": 24, "emoji": "✨",
     "name": {"ar": "عيسى", "en": "Isa (Jesus)", "de": "Isa (Jesus)", "fr": "Issa (Jésus)", "tr": "İsa", "ru": "Иса (Иисус)"},
     "title": {"ar": "روح الله", "en": "Spirit of Allah", "de": "Geist Allahs", "fr": "Esprit d'Allah", "tr": "Allah'ın Ruhu", "ru": "Дух Аллаха"},
     "summary": {"ar": "ولد من مريم بدون أب بمعجزة من الله. تكلم في المهد وأحيا الموتى بإذن الله. رفعه الله إلى السماء", "en": "Born to Maryam without a father by Allah's miracle. He spoke in the cradle and revived the dead by Allah's permission. Allah raised him to the heavens"},
     "lesson": {"ar": "المعجزات بإذن الله", "en": "Miracles by Allah's permission"},
     "quran_ref": "آل عمران 45-55"},
    {"id": "muhammad", "number": 25, "emoji": "🕌",
     "name": {"ar": "محمد ﷺ", "en": "Muhammad ﷺ", "de": "Muhammad ﷺ", "fr": "Muhammad ﷺ", "tr": "Muhammed ﷺ", "ru": "Мухаммад ﷺ"},
     "title": {"ar": "خاتم الأنبياء", "en": "Seal of the Prophets", "de": "Siegel der Propheten", "fr": "Sceau des Prophètes", "tr": "Peygamberlerin Sonuncusu", "ru": "Печать пророков"},
     "summary": {"ar": "وُلد في مكة يتيماً وكان أميناً صادقاً. نزل عليه القرآن وهو في غار حراء. دعا الناس إلى الإسلام وهاجر إلى المدينة. هو قدوتنا وحبيبنا ﷺ", "en": "Born an orphan in Makkah, he was trustworthy and truthful. The Quran was revealed to him in the Cave of Hira. He called people to Islam and migrated to Madinah. He is our role model ﷺ"},
     "lesson": {"ar": "حسن الخلق والرحمة", "en": "Good character and mercy"},
     "quran_ref": "الأحزاب 21"},
]

# ═══════════════════════════════════════════════════════════════
# PROPHET TRANSLATIONS (summaries & lessons in all 9 languages)
# ═══════════════════════════════════════════════════════════════
PROPHET_TRANSLATIONS = {
    "adam": {
        "summary": {"de":"Allah erschuf Adam aus Ton und lehrte ihn die Namen aller Dinge. Er war der erste Mensch und Prophet","fr":"Allah a créé Adam d'argile et lui a enseigné les noms de toutes choses. Premier humain et premier prophète","tr":"Allah Adem'i topraktan yarattı ve ona her şeyin ismini öğretti. İlk insan ve ilk peygamberdi","ru":"Аллах создал Адама из глины и научил его именам всех вещей. Он был первым человеком и пророком","sv":"Allah skapade Adam av lera och lärde honom namnen på alla ting. Han var den första människan och profeten","nl":"Allah schiep Adam van klei en leerde hem de namen van alle dingen. Hij was de eerste mens en profeet","el":"Ο Αλλάχ δημιούργησε τον Αδάμ από πηλό και του δίδαξε τα ονόματα όλων των πραγμάτων"},
        "lesson": {"de":"Reue und Vergebung suchen","fr":"Repentir et demande de pardon","tr":"Tövbe ve istiğfar","ru":"Покаяние и просьба о прощении","sv":"Ånger och att söka förlåtelse","nl":"Berouw en vergeving zoeken","el":"Μετάνοια και αναζήτηση συγχώρεσης"},
        "name_extra": {"sv":"Adam","nl":"Adam","el":"Αδάμ"},
        "title_extra": {"sv":"Mänsklighetens fader","nl":"Vader van de mensheid","el":"Πατέρας της ανθρωπότητας"}},
    "idris": {
        "summary": {"de":"Er war wahrhaftig und geduldig, Allah erhob ihn zu einem hohen Rang. Er war der Erste, der mit einem Stift schrieb","fr":"Il était véridique et patient, Allah l'a élevé à un haut rang. Premier à écrire avec un stylo","tr":"Doğru sözlü ve sabırlıydı, Allah onu yüce bir makama yükseltti. Kalemle yazan ilk kişiydi","ru":"Он был правдивым и терпеливым, Аллах возвысил его. Первый, кто писал пером","sv":"Han var sanningsenlig och tålmodig, Allah upphöjde honom. Han var den förste att skriva med penna","nl":"Hij was waarheidsgetrouw en geduldig, Allah verhief hem. Hij was de eerste die met een pen schreef","el":"Ήταν αληθινός και υπομονετικός, ο Αλλάχ τον ύψωσε. Ήταν ο πρώτος που έγραψε με στυλό"},
        "lesson": {"de":"Wissen suchen und Geduld","fr":"Recherche du savoir et patience","tr":"İlim öğrenmek ve sabır","ru":"Поиск знаний и терпение","sv":"Sök kunskap och tålamod","nl":"Kennis zoeken en geduld","el":"Αναζήτηση γνώσης και υπομονή"},
        "title_extra": {"sv":"Sanningsenlig och tålmodig","nl":"Waarheidsgetrouw en geduldig","el":"Αληθινός και υπομονετικός"}},
    "nuh": {
        "summary": {"de":"Er rief sein Volk 950 Jahre lang zur Anbetung Allahs auf. Er baute eine große Arche und die Sintflut kam","fr":"Il a appelé son peuple à adorer Allah pendant 950 ans. Il a construit une grande arche et le déluge est venu","tr":"Kavmini 950 yıl Allah'a ibadete çağırdı. Büyük bir gemi inşa etti ve tufan geldi","ru":"Он призывал свой народ к поклонению Аллаху 950 лет. Построил великий ковчег и пришёл потоп","sv":"Han kallade sitt folk att tillbe Allah i 950 år. Han byggde en stor ark och översvämningen kom","nl":"Hij riep zijn volk 950 jaar op om Allah te aanbidden. Hij bouwde een grote ark en de vloed kwam","el":"Κάλεσε τον λαό του να λατρεύσει τον Αλλάχ για 950 χρόνια. Έχτισε μεγάλη κιβωτό και ήρθε ο κατακλυσμός"},
        "lesson": {"de":"Geduld und Ausdauer","fr":"Patience et persévérance","tr":"Sabır ve azim","ru":"Терпение и настойчивость","sv":"Tålamod och uthållighet","nl":"Geduld en doorzettingsvermogen","el":"Υπομονή και επιμονή"},
        "title_extra": {"sv":"Den förste store sändebudet","nl":"De eerste grote boodschapper","el":"Ο πρώτος μεγάλος απεσταλμένος"}},
    "hud": {
        "summary": {"de":"Gesandt zum Volk 'Ad, das stark war und hohe Gebäude baute. Er rief sie zur Anbetung Allahs auf, aber sie weigerten sich","fr":"Envoyé au peuple de 'Ad qui était fort et construisait de hauts bâtiments. Il les a appelés à adorer Allah mais ils ont refusé","tr":"Güçlü olan ve yüksek binalar yapan Ad kavmine gönderildi. Onları Allah'a ibadete çağırdı ama reddettiler","ru":"Послан к народу Ад, который был сильным и строил высокие здания. Призвал их к поклонению Аллаху, но они отказались","sv":"Sänd till Ads folk som var starka och byggde höga byggnader. Han kallade dem att tillbe Allah men de vägrade","nl":"Gezonden naar het volk van Ad dat sterk was en hoge gebouwen bouwde. Hij riep hen op Allah te aanbidden maar zij weigerden","el":"Στάλθηκε στον λαό του Αντ που ήταν ισχυρός και έχτιζε ψηλά κτίρια. Τους κάλεσε να λατρεύσουν τον Αλλάχ αλλά αρνήθηκαν"},
        "lesson": {"de":"Demut, kein Hochmut","fr":"Humilité, pas d'arrogance","tr":"Kibirlenmemek","ru":"Смирение, без высокомерия","sv":"Ödmjukhet, ingen arrogans","nl":"Nederigheid, geen arrogantie","el":"Ταπεινότητα, χωρίς αλαζονεία"},
        "title_extra": {"sv":"Sänd till Ads folk","nl":"Gezonden naar het volk van Ad","el":"Σταλμένος στον λαό του Αντ"}},
    "salih": {
        "summary": {"de":"Gesandt nach Thamud. Allah gab ihm eine Kamelstute als Wunder. Sie töteten sie, also vernichtete Allah sie","fr":"Envoyé à Thamoud. Allah lui a donné une chamelle comme miracle. Ils l'ont tuée, alors Allah les a détruits","tr":"Semud kavmine gönderildi. Allah ona mucize olarak bir deve verdi. Onu öldürdüler, Allah onları helak etti","ru":"Послан к самудянам. Аллах дал ему верблюдицу как чудо. Они убили её, и Аллах уничтожил их","sv":"Sänd till Thamud. Allah gav honom en kamelsto som mirakel. De dödade den, så Allah förstörde dem","nl":"Gezonden naar Thamud. Allah gaf hem een kameelmerrie als wonder. Ze doodden haar, dus Allah vernietigde hen","el":"Στάλθηκε στους Θαμούντ. Ο Αλλάχ του έδωσε μια καμήλα ως θαύμα. Τη σκότωσαν και ο Αλλάχ τους κατέστρεψε"},
        "lesson": {"de":"Allahs Zeichen respektieren","fr":"Respecter les signes d'Allah","tr":"Allah'ın ayetlerine saygı","ru":"Уважение знамений Аллаха","sv":"Respektera Allahs tecken","nl":"Allahs tekenen respecteren","el":"Σεβασμός στα σημεία του Αλλάχ"},
        "title_extra": {"sv":"Sänd till Thamud","nl":"Gezonden naar Thamud","el":"Σταλμένος στους Θαμούντ"}},
    "ibrahim": {
        "summary": {"de":"Er zerbrach die Götzen allein und rief zur Anbetung des Einen Gottes auf. Er wurde ins Feuer geworfen, aber Allah machte es kühl. Er baute die Kaaba mit seinem Sohn Ismail","fr":"Il a brisé les idoles seul et a appelé à l'adoration d'un Dieu unique. Jeté au feu, Allah l'a rendu frais. Il a construit la Kaaba avec son fils Ismaïl","tr":"Putları tek başına kırdı ve tek Allah'a ibadete çağırdı. Ateşe atıldı ama Allah ateşi serin kıldı. Oğlu İsmail ile Kabe'yi inşa etti","ru":"Он разбил идолов и призвал к поклонению Единому Богу. Был брошен в огонь, но Аллах сделал его прохладным. Построил Каабу с сыном Исмаилом","sv":"Han krossade avgudarna ensam och kallade till dyrkan av den Ende Guden. Han kastades i elden men Allah gjorde den sval. Han byggde Kaba med sin son Ismail","nl":"Hij brak de afgoden alleen en riep op tot aanbidding van de Ene God. Hij werd in het vuur geworpen maar Allah maakte het koel. Hij bouwde de Kaaba met zijn zoon Ismail","el":"Έσπασε τα είδωλα μόνος και κάλεσε στη λατρεία του Ενός Θεού. Ρίχτηκε στη φωτιά αλλά ο Αλλάχ την έκανε δροσερή. Έχτισε την Κάαμπα με τον γιο του Ισμαήλ"},
        "lesson": {"de":"Mut für die Wahrheit","fr":"Courage pour la vérité","tr":"Hak için cesaret","ru":"Мужество ради истины","sv":"Mod för sanningen","nl":"Moed voor de waarheid","el":"Θάρρος για την αλήθεια"},
        "title_extra": {"sv":"Allahs vän","nl":"Vriend van Allah","el":"Φίλος του Αλλάχ"}},
    "lut": {
        "summary": {"de":"Ibrahims Neffe. Gesandt zu einem Volk, das große Sünden beging. Er rief sie zur Umkehr, aber sie weigerten sich","fr":"Neveu d'Ibrahim. Envoyé à un peuple qui commettait de grands péchés. Il les a appelés au repentir mais ils ont refusé","tr":"İbrahim'in yeğeni. Büyük günahlar işleyen bir kavme gönderildi. Tövbeye çağırdı ama reddettiler","ru":"Племянник Ибрахима. Послан к людям, совершавшим великие грехи. Призвал их к покаянию, но они отказались","sv":"Ibrahims brorson. Sänd till folk som begick stora synder. Han kallade dem till ånger men de vägrade","nl":"Neef van Ibrahim. Gezonden naar mensen die grote zonden begingen. Hij riep hen op tot berouw maar zij weigerden","el":"Ανιψιός του Ιμπραχίμ. Στάλθηκε σε λαό που διέπραττε μεγάλες αμαρτίες. Τους κάλεσε σε μετάνοια αλλά αρνήθηκαν"},
        "lesson": {"de":"Sich von Sünden fernhalten","fr":"S'éloigner du péché","tr":"Günahlardan uzak durmak","ru":"Держаться подальше от грехов","sv":"Hålla sig borta från synd","nl":"Wegblijven van zonde","el":"Αποφυγή αμαρτίας"},
        "title_extra": {"sv":"Ibrahims brorson","nl":"Neef van Ibrahim","el":"Ανιψιός του Ιμπραχίμ"}},
    "ismail": {
        "summary": {"de":"Sohn Ibrahims. Er war geduldig, als Allah seinen Vater befahl, ihn zu opfern. Allah ersetzte ihn durch einen Widder","fr":"Fils d'Ibrahim. Patient quand Allah ordonna à son père de le sacrifier. Allah le remplaça par un bélier","tr":"İbrahim'in oğlu. Allah babasına onu kurban etmesini emrettiğinde sabretti. Allah onu büyük bir koçla değiştirdi","ru":"Сын Ибрахима. Был терпелив, когда Аллах повелел его отцу принести его в жертву. Аллах заменил его бараном","sv":"Ibrahims son. Han var tålmodig när Allah befallde hans far att offra honom. Allah ersatte honom med en bagge","nl":"Zoon van Ibrahim. Hij was geduldig toen Allah zijn vader beval hem te offeren. Allah verving hem door een ram","el":"Γιος του Ιμπραχίμ. Υπέμεινε όταν ο Αλλάχ διέταξε τον πατέρα του να τον θυσιάσει. Ο Αλλάχ τον αντικατέστησε με κριάρι"},
        "lesson": {"de":"Gehorsam und Hingabe an Allah","fr":"Obéissance et soumission à Allah","tr":"Allah'a itaat ve teslimiyet","ru":"Покорность и подчинение Аллаху","sv":"Lydnad och underkastelse till Allah","nl":"Gehoorzaamheid en overgave aan Allah","el":"Υπακοή και υποταγή στον Αλλάχ"},
        "title_extra": {"sv":"Offrets son","nl":"Zoon van het offer","el":"Ο γιος της θυσίας"}},
    "ishaq": {
        "summary": {"de":"Sohn Ibrahims und Sarahs. Allah verkündete ihnen die frohe Botschaft in ihrem hohen Alter","fr":"Fils d'Ibrahim et Sarah. Allah leur a annoncé la bonne nouvelle dans leur vieillesse","tr":"İbrahim ve Sara'nın oğlu. Allah onlara yaşlılıklarında müjde verdi","ru":"Сын Ибрахима и Сары. Аллах обрадовал их этой вестью в старости","sv":"Son till Ibrahim och Sarah. Allah gav dem glada nyheter i deras ålderdom","nl":"Zoon van Ibrahim en Sarah. Allah gaf hen het goede nieuws op hun oude dag","el":"Γιος του Ιμπραχίμ και της Σάρα. Ο Αλλάχ τους ευαγγελίστηκε στα γεράματά τους"},
        "lesson": {"de":"Nichts ist unmöglich bei Allah","fr":"Rien n'est impossible pour Allah","tr":"Allah'ın yapamayacağı hiçbir şey yoktur","ru":"Для Аллаха нет ничего невозможного","sv":"Inget är omöjligt för Allah","nl":"Niets is onmogelijk voor Allah","el":"Τίποτα δεν είναι αδύνατο για τον Αλλάχ"},
        "title_extra": {"sv":"Son till Ibrahim och Sarah","nl":"Zoon van Ibrahim en Sarah","el":"Γιος Ιμπραχίμ και Σάρα"}},
    "yaqub": {
        "summary": {"de":"Sohn Ishaqs und Vater Yusufs. Er ertrug geduldig die Trennung von Yusuf, bis er sein Augenlicht verlor","fr":"Fils d'Ishaq et père de Youssouf. Il supporta patiemment la séparation de Youssouf jusqu'à perdre la vue","tr":"İshak'ın oğlu ve Yusuf'un babası. Yusuf'tan ayrılığa sabırla katlandı, gözlerini kaybedene kadar","ru":"Сын Исхака и отец Юсуфа. Терпеливо переносил разлуку с Юсуфом, пока не ослеп от слёз","sv":"Son till Ishaq och far till Yusuf. Han bar tålmodigt separationen från Yusuf tills han förlorade synen","nl":"Zoon van Ishaq en vader van Yusuf. Hij doorstond geduldig de scheiding van Yusuf tot hij zijn zicht verloor","el":"Γιος του Ισχάκ και πατέρας του Γιούσουφ. Υπέμεινε με υπομονή τον χωρισμό μέχρι που έχασε την όρασή του"},
        "lesson": {"de":"Schöne Geduld","fr":"Belle patience","tr":"Güzel sabır","ru":"Прекрасное терпение","sv":"Vacker tålamod","nl":"Mooi geduld","el":"Όμορφη υπομονή"},
        "title_extra": {"sv":"Fader till tolv stammar","nl":"Vader van twaalf stammen","el":"Πατέρας δώδεκα φυλών"}},
    "yusuf": {
        "summary": {"de":"Er träumte von elf Sternen, die sich vor ihm verneigten. Seine Brüder warfen ihn in einen Brunnen. Er war geduldig im Gefängnis und wurde dann Minister von Ägypten","fr":"Il rêva de onze étoiles s'inclinant devant lui. Ses frères le jetèrent dans un puits. Patient en prison, il devint ministre d'Égypte","tr":"On bir yıldızın kendisine secde ettiğini rüyasında gördü. Kardeşleri onu kuyuya attı. Hapiste sabretti ve Mısır'ın azizi oldu","ru":"Он увидел во сне одиннадцать звёзд, поклоняющихся ему. Братья бросили его в колодец. Терпеливо переносил тюрьму, затем стал правителем Египта","sv":"Han drömde om elva stjärnor som bugade sig för honom. Hans bröder kastade honom i en brunn. Han var tålmodig i fängelse och blev sedan Egyptens minister","nl":"Hij droomde van elf sterren die voor hem bogen. Zijn broers gooiden hem in een put. Geduldig in de gevangenis werd hij minister van Egypte","el":"Ονειρεύτηκε ένδεκα αστέρια που υποκλίνονταν. Τα αδέλφια του τον πέταξαν σε πηγάδι. Υπέμεινε στη φυλακή και έγινε υπουργός της Αιγύπτου"},
        "lesson": {"de":"Geduld bei Prüfungen","fr":"Patience face aux épreuves","tr":"Sıkıntılarda sabır","ru":"Терпение в испытаниях","sv":"Tålamod genom prövningar","nl":"Geduld bij beproevingen","el":"Υπομονή στις δοκιμασίες"},
        "title_extra": {"sv":"Den vackre och tålmodige","nl":"De mooie en geduldige","el":"Ο ωραίος και υπομονετικός"}},
    "ayyub": {
        "summary": {"de":"Allah prüfte ihn mit Krankheit und Verlust. Er war geduldig und beschwerte sich nie. Allah heilte ihn und gab alles doppelt zurück","fr":"Allah l'a éprouvé par la maladie et la perte. Patient, il ne s'est jamais plaint. Allah l'a guéri et tout restitué en double","tr":"Allah onu hastalık ve kayıpla imtihan etti. Sabretti ve şikayet etmedi. Allah onu iyileştirdi ve her şeyi iki katına çıkardı","ru":"Аллах испытал его болезнью и потерями. Он терпел и не жаловался. Аллах исцелил его и вернул всё вдвойне","sv":"Allah prövade honom med sjukdom och förlust. Han var tålmodig och klagade aldrig. Allah botade honom och gav tillbaka allt dubbelt","nl":"Allah beproefde hem met ziekte en verlies. Hij was geduldig en klaagde nooit. Allah genas hem en gaf alles dubbel terug","el":"Ο Αλλάχ τον δοκίμασε με ασθένεια και απώλειες. Υπέμεινε χωρίς παράπονα. Ο Αλλάχ τον θεράπευσε και επέστρεψε τα πάντα διπλά"},
        "lesson": {"de":"Geduld bei Leid","fr":"Patience dans l'épreuve","tr":"Belaya sabır","ru":"Терпение в трудностях","sv":"Tålamod i prövningar","nl":"Geduld bij tegenspoed","el":"Υπομονή στις δυσκολίες"},
        "title_extra": {"sv":"Den tålmodige","nl":"De geduldige","el":"Ο υπομονετικός"}},
    "shuayb": {
        "summary": {"de":"Gesandt zum Volk von Madyan, das im Handel betrog. Er rief sie zur Gerechtigkeit auf, aber sie weigerten sich","fr":"Envoyé au peuple de Madyan qui trichait dans le commerce. Il les a appelés à la justice mais ils ont refusé","tr":"Ticarette hile yapan Medyen halkına gönderildi. Onları adalete çağırdı ama reddettiler","ru":"Послан к жителям Мадьяна, обманывавшим в торговле. Призвал их к справедливости, но они отказались","sv":"Sänd till Madyans folk som fuskade i handel. Han kallade dem till rättvisa men de vägrade","nl":"Gezonden naar het volk van Madyan dat in handel bedrog. Hij riep hen op tot rechtvaardigheid maar zij weigerden","el":"Στάλθηκε στον λαό του Μαντιάν που εξαπατούσε στο εμπόριο. Τους κάλεσε στη δικαιοσύνη αλλά αρνήθηκαν"},
        "lesson": {"de":"Ehrlichkeit im Umgang","fr":"Honnêteté dans les relations","tr":"Muamelelerde dürüstlük","ru":"Честность в делах","sv":"Ärlighet i handel","nl":"Eerlijkheid in omgang","el":"Τιμιότητα στις συναλλαγές"},
        "title_extra": {"sv":"Profeternas talare","nl":"Redenaar van de profeten","el":"Ο ρήτορας των προφητών"}},
    "musa": {
        "summary": {"de":"Geboren zur Zeit des Tyrannen Pharao. Seine Mutter legte ihn in den Fluss. Allah sprach zu ihm und gab ihm neun Zeichen. Er teilte das Meer und rettete sein Volk","fr":"Né à l'époque du tyran Pharaon. Sa mère le plaça dans le fleuve. Allah lui parla et lui donna neuf signes. Il fendit la mer et sauva son peuple","tr":"Zalim Firavun döneminde doğdu. Annesi onu nehre bıraktı. Allah onunla konuştu ve dokuz mucize verdi. Denizi yardı ve kavmini kurtardı","ru":"Родился во времена тирана фараона. Мать положила его в реку. Аллах говорил с ним и дал девять знамений. Он рассёк море и спас свой народ","sv":"Född under tyrannen Faraos tid. Hans mor lade honom i floden. Allah talade till honom och gav honom nio tecken. Han delade havet och räddade sitt folk","nl":"Geboren ten tijde van de tiran Farao. Zijn moeder legde hem in de rivier. Allah sprak tot hem en gaf hem negen tekenen. Hij splitste de zee en redde zijn volk","el":"Γεννήθηκε στην εποχή του τυράννου Φαραώ. Η μητέρα του τον έβαλε στον ποταμό. Ο Αλλάχ μίλησε μαζί του και του έδωσε εννέα σημεία. Χώρισε τη θάλασσα και έσωσε τον λαό του"},
        "lesson": {"de":"Vertrauen auf Allah","fr":"Confiance en Allah","tr":"Allah'a tevekkül","ru":"Упование на Аллаха","sv":"Tillit till Allah","nl":"Vertrouwen op Allah","el":"Εμπιστοσύνη στον Αλλάχ"},
        "title_extra": {"sv":"Den som talade med Allah","nl":"Spreker tot Allah","el":"Αυτός που μίλησε με τον Αλλάχ"}},
    "harun": {
        "summary": {"de":"Bruder von Musa und sein Helfer bei der Einladung zu Allah. Er war redegewandt","fr":"Frère de Moussa et son aide dans l'appel à Allah. Il était éloquent","tr":"Musa'nın kardeşi ve Allah'a davette yardımcısı. Güzel konuşan biriydi","ru":"Брат Мусы и его помощник в призыве к Аллаху. Был красноречив","sv":"Musas bror och hjälpare i kallelsen till Allah. Han var vältalig","nl":"Broer van Musa en zijn helper in de oproep tot Allah. Hij was welsprekend","el":"Αδελφός του Μούσα και βοηθός του στο κάλεσμα στον Αλλάχ. Ήταν εύγλωττος"},
        "lesson": {"de":"Zusammenarbeit im Guten","fr":"Coopération dans le bien","tr":"Hayırda yardımlaşma","ru":"Сотрудничество в добре","sv":"Samarbete i godhet","nl":"Samenwerking in het goede","el":"Συνεργασία στο καλό"},
        "title_extra": {"sv":"Musas bror","nl":"Broer van Musa","el":"Αδελφός του Μούσα"}},
    "dhulkifl": {
        "summary": {"de":"Er war unter den Geduldigen und Rechtschaffenen. Allah erwähnte ihn im Koran und lobte ihn","fr":"Il était parmi les patients et les justes. Allah l'a mentionné dans le Coran et l'a loué","tr":"Sabredenlerden ve iyilerden biriydi. Allah onu Kur'an'da peygamberlerle birlikte andı","ru":"Был среди терпеливых и праведных. Аллах упомянул его в Коране среди пророков","sv":"Han var bland de tålmodiga och rättfärdiga. Allah nämnde honom i Koranen och prisade honom","nl":"Hij was onder de geduldigen en rechtschapenen. Allah noemde hem in de Koran en prees hem","el":"Ήταν μεταξύ των υπομονετικών και δικαίων. Ο Αλλάχ τον ανέφερε στο Κοράνι και τον εγκωμίασε"},
        "lesson": {"de":"Geduld und Versprechen halten","fr":"Patience et tenir ses promesses","tr":"Sabır ve sözünde durmak","ru":"Терпение и верность обещаниям","sv":"Tålamod och att hålla löften","nl":"Geduld en beloften nakomen","el":"Υπομονή και τήρηση υποσχέσεων"},
        "title_extra": {"sv":"Den ståndaktige","nl":"De standvastige","el":"Ο σταθερός"}},
    "dawud": {
        "summary": {"de":"König und Prophet. Allah gab ihm eine schöne Stimme, Berge und Vögel priesen Allah mit ihm. Allah offenbarte ihm die Psalmen","fr":"Roi et prophète. Allah lui donna une belle voix, montagnes et oiseaux glorifiaient Allah avec lui. Les Psaumes lui furent révélés","tr":"Hem kral hem peygamberdi. Allah ona güzel bir ses verdi, dağlar ve kuşlar onunla birlikte tesbih ederdi. Zebur ona indirildi","ru":"Царь и пророк. Аллах дал ему прекрасный голос, горы и птицы славили Аллаха вместе с ним. Ему был ниспослан Забур","sv":"Kung och profet. Allah gav honom en vacker röst, berg och fåglar prisade Allah med honom. Psaltaren uppenbarades för honom","nl":"Koning en profeet. Allah gaf hem een mooie stem, bergen en vogels prezen Allah met hem. De Psalmen werden aan hem geopenbaard","el":"Βασιλιάς και προφήτης. Ο Αλλάχ του έδωσε όμορφη φωνή, βουνά και πουλιά δόξαζαν τον Αλλάχ μαζί του. Οι Ψαλμοί αποκαλύφθηκαν σε αυτόν"},
        "lesson": {"de":"Dankbar für Segen sein","fr":"Être reconnaissant pour les bienfaits","tr":"Nimetlere şükretmek","ru":"Благодарность за дары","sv":"Vara tacksam för välsignelser","nl":"Dankbaar zijn voor zegeningen","el":"Ευγνωμοσύνη για τις ευλογίες"},
        "title_extra": {"sv":"Profet-konung","nl":"Profeet-koning","el":"Προφήτης-βασιλιάς"}},
    "sulayman": {
        "summary": {"de":"Sohn von Dawud. Allah unterwarf ihm Wind, Dschinn und Vögel. Er verstand die Sprache der Ameisen und Vögel","fr":"Fils de Dawoud. Allah lui soumit le vent, les djinns et les oiseaux. Il comprenait le langage des fourmis et des oiseaux","tr":"Davud'un oğlu. Allah ona rüzgarı, cinleri ve kuşları boyun eğdirdi. Karınca ve kuş dilini anlardı","ru":"Сын Дауда. Аллах подчинил ему ветер, джиннов и птиц. Он понимал язык муравьёв и птиц","sv":"Son till Dawud. Allah underkastade vinden, djinner och fåglar åt honom. Han förstod myrornas och fåglarnas språk","nl":"Zoon van Dawud. Allah onderwierp wind, djinn en vogels aan hem. Hij begreep de taal van mieren en vogels","el":"Γιος του Ντάουντ. Ο Αλλάχ υπέταξε τον άνεμο, τα τζιν και τα πουλιά σε αυτόν. Καταλάβαινε τη γλώσσα μυρμηγκιών και πουλιών"},
        "lesson": {"de":"Demut trotz Macht","fr":"Humilité malgré le pouvoir","tr":"Güce rağmen tevazu","ru":"Смирение несмотря на силу","sv":"Ödmjukhet trots makt","nl":"Nederigheid ondanks macht","el":"Ταπεινότητα παρά τη δύναμη"},
        "title_extra": {"sv":"Vis kung","nl":"Wijze koning","el":"Σοφός βασιλιάς"}},
    "ilyas": {
        "summary": {"de":"Er rief sein Volk auf, die Anbetung eines Götzen namens Baal aufzugeben und Allah allein anzubeten","fr":"Il a appelé son peuple à abandonner l'idole Ba'l et à revenir à l'adoration d'Allah seul","tr":"Kavmini Baal adlı putu bırakıp yalnız Allah'a ibadete çağırdı","ru":"Призвал свой народ оставить поклонение идолу Баалу и вернуться к поклонению одному Аллаху","sv":"Han kallade sitt folk att överge avguden Baal och återvända till att tillbe Allah ensam","nl":"Hij riep zijn volk op het afgod Baäl te verlaten en terug te keren naar de aanbidding van Allah alleen","el":"Κάλεσε τον λαό του να εγκαταλείψει τη λατρεία του ειδώλου Μπάαλ και να επιστρέψει στη λατρεία του Αλλάχ"},
        "lesson": {"de":"Am Monotheismus festhalten","fr":"S'accrocher au monothéisme","tr":"Tevhide bağlı kalmak","ru":"Твёрдость в единобожии","sv":"Hålla fast vid monoteism","nl":"Vasthouden aan monotheïsme","el":"Κράτημα στον μονοθεϊσμό"},
        "title_extra": {"sv":"Den ivrige","nl":"De ijverige","el":"Ο ζηλωτής"}},
    "alyasa": {
        "summary": {"de":"Allah erwähnte ihn im Koran und bevorzugte ihn. Er war unter den Rechtschaffenen und Geduldigen","fr":"Allah l'a mentionné dans le Coran et l'a favorisé. Il était parmi les justes et les patients","tr":"Allah onu Kur'an'da andı ve üstün kıldı. İyilerden ve sabredenlerden biriydi","ru":"Аллах упомянул его в Коране и возвысил. Был среди праведных и терпеливых","sv":"Allah nämnde honom i Koranen och gynnade honom. Han var bland de rättfärdiga och tålmodiga","nl":"Allah noemde hem in de Koran en bevoordeelde hem. Hij was onder de rechtschapenen en geduldigen","el":"Ο Αλλάχ τον ανέφερε στο Κοράνι και τον ευνόησε. Ήταν μεταξύ των δικαίων και υπομονετικών"},
        "lesson": {"de":"Tugend der Rechtschaffenen","fr":"Vertu des justes","tr":"İyilerin fazileti","ru":"Добродетель праведных","sv":"De rättfärdigas dygd","nl":"Deugd van de rechtschapenen","el":"Αρετή των δικαίων"},
        "title_extra": {"sv":"Den rättfärdige","nl":"De rechtschapene","el":"Ο δίκαιος"}},
    "yunus": {
        "summary": {"de":"Er war wütend auf sein Volk und bestieg ein Schiff. Ein Wal verschluckte ihn. Er rief Allah an und wurde gerettet","fr":"Fâché contre son peuple, il monta sur un navire. Une baleine l'avala. Il invoqua Allah et fut sauvé","tr":"Kavmine kızdı ve gemiye bindi. Balık onu yuttu. Karanlıklarda Allah'a dua etti ve kurtarıldı","ru":"Разгневался на свой народ и сел на корабль. Кит проглотил его. Он воззвал к Аллаху и был спасён","sv":"Han var arg på sitt folk och gick ombord på ett skepp. En val svalde honom. Han åkallade Allah och räddades","nl":"Hij was boos op zijn volk en ging aan boord van een schip. Een walvis slikte hem in. Hij riep Allah aan en werd gered","el":"Θύμωσε με τον λαό του και μπήκε σε πλοίο. Μια φάλαινα τον κατάπιε. Επικαλέστηκε τον Αλλάχ και σώθηκε"},
        "lesson": {"de":"Vergebung suchen und bereuen","fr":"Demander pardon et se repentir","tr":"İstiğfar ve tövbe","ru":"Просить прощения и каяться","sv":"Söka förlåtelse och ångra sig","nl":"Vergeving zoeken en berouw tonen","el":"Αναζήτηση συγχώρεσης και μετάνοια"},
        "title_extra": {"sv":"Valens följeslagare","nl":"Metgezel van de walvis","el":"Σύντροφος της φάλαινας"}},
    "zakariya": {
        "summary": {"de":"Vormund Maryams. Er betete im Alter zu Allah um ein Kind und Allah schenkte ihm Yahya","fr":"Tuteur de Maryam. Il pria Allah pour un enfant dans sa vieillesse et Allah lui donna Yahya","tr":"Meryem'in bakıcısıydı. Yaşlılığında Allah'a çocuk için dua etti ve Allah ona Yahya'yı müjdeledi","ru":"Опекун Марьям. В старости молил Аллаха о ребёнке, и Аллах обрадовал его вестью о Яхье","sv":"Maryams förmyndare. Han bad Allah om ett barn i sin ålderdom och Allah gav honom Yahya","nl":"Voogd van Maryam. Hij bad Allah om een kind op zijn oude dag en Allah gaf hem Yahya","el":"Κηδεμόνας της Μαριάμ. Προσευχήθηκε στον Αλλάχ για παιδί σε μεγάλη ηλικία και ο Αλλάχ του χάρισε τον Γιαχιά"},
        "lesson": {"de":"Nie an Allahs Barmherzigkeit verzweifeln","fr":"Ne jamais désespérer de la miséricorde d'Allah","tr":"Allah'ın rahmetinden ümit kesmemek","ru":"Никогда не отчаивайся в милости Аллаха","sv":"Misströsta aldrig om Allahs barmhärtighet","nl":"Wanhoop nooit aan Allahs genade","el":"Ποτέ μην απελπίζεσαι από το έλεος του Αλλάχ"},
        "title_extra": {"sv":"Maryams förmyndare","nl":"Voogd van Maryam","el":"Κηδεμόνας της Μαριάμ"}},
    "yahya": {
        "summary": {"de":"Sohn Zakariyas. Fromm und bescheiden, liebte Menschen und Tiere. Allah nannte ihn Yahya - der Erste mit diesem Namen","fr":"Fils de Zakaria. Pieux et ascétique, aimait les gens et les animaux. Allah l'a nommé Yahya - le premier à porter ce nom","tr":"Zekeriya'nın oğlu. Takva sahibi ve zahitti, insanları ve hayvanları severdi. Bu isimle ilk anılan kişiydi","ru":"Сын Закарии. Был набожным и скромным, любил людей и животных. Аллах назвал его Яхья — первый с этим именем","sv":"Zakariyas son. From och asketisk, älskade människor och djur. Allah namngav honom Yahya - den förste med detta namn","nl":"Zoon van Zakariya. Vroom en ascetisch, hield van mensen en dieren. Allah noemde hem Yahya - de eerste met deze naam","el":"Γιος του Ζακαρία. Ευσεβής και ασκητικός, αγαπούσε ανθρώπους και ζώα. Ο Αλλάχ τον ονόμασε Γιαχιά - ο πρώτος με αυτό το όνομα"},
        "lesson": {"de":"Frömmigkeit und Liebe zum Guten","fr":"Piété et amour du bien","tr":"Takva ve hayırseverlik","ru":"Благочестие и любовь к добру","sv":"Fromhet och kärlek till godhet","nl":"Vroomheid en liefde voor het goede","el":"Ευσέβεια και αγάπη για το καλό"},
        "title_extra": {"sv":"Den fromme unge","nl":"De vrome jongeling","el":"Ο ευσεβής νέος"}},
    "isa": {
        "summary": {"de":"Von Maryam ohne Vater durch Allahs Wunder geboren. Er sprach in der Wiege und erweckte Tote mit Allahs Erlaubnis. Allah erhob ihn in den Himmel","fr":"Né de Maryam sans père par miracle d'Allah. Il parla au berceau et ressuscita les morts avec la permission d'Allah. Allah l'éleva aux cieux","tr":"Allah'ın mucizesiyle babasız olarak Meryem'den doğdu. Beşikte konuştu ve Allah'ın izniyle ölüleri diriltti. Allah onu göğe yükseltti","ru":"Родился от Марьям без отца чудом Аллаха. Говорил в колыбели и воскрешал мёртвых с позволения Аллаха. Аллах вознёс его на небеса","sv":"Född av Maryam utan far genom Allahs mirakel. Han talade i vaggan och väckte döda med Allahs tillåtelse. Allah upphöjde honom till himlarna","nl":"Geboren uit Maryam zonder vader door Allahs wonder. Hij sprak in de wieg en wekte doden op met Allahs toestemming. Allah verhief hem naar de hemelen","el":"Γεννήθηκε από τη Μαριάμ χωρίς πατέρα με θαύμα του Αλλάχ. Μίλησε στην κούνια και ανέστησε νεκρούς με την άδεια του Αλλάχ. Ο Αλλάχ τον ύψωσε στους ουρανούς"},
        "lesson": {"de":"Wunder geschehen mit Allahs Erlaubnis","fr":"Les miracles se produisent avec la permission d'Allah","tr":"Mucizeler Allah'ın izniyle olur","ru":"Чудеса происходят с позволения Аллаха","sv":"Mirakel sker med Allahs tillåtelse","nl":"Wonderen gebeuren met Allahs toestemming","el":"Τα θαύματα γίνονται με την άδεια του Αλλάχ"},
        "title_extra": {"sv":"Ande från Allah","nl":"Geest van Allah","el":"Πνεύμα από τον Αλλάχ"}},
    "muhammad": {
        "summary": {"de":"Als Waise in Mekka geboren, war er vertrauenswürdig und wahrhaftig. Der Koran wurde ihm in der Höhle Hira offenbart. Er rief zum Islam auf und wanderte nach Medina aus. Er ist unser Vorbild ﷺ","fr":"Né orphelin à La Mecque, il était digne de confiance et véridique. Le Coran lui fut révélé dans la grotte de Hira. Il appela à l'Islam et émigra à Médine. Il est notre modèle ﷺ","tr":"Mekke'de yetim olarak doğdu, güvenilir ve doğru sözlüydü. Kur'an ona Hira mağarasında indirildi. İslam'a davet etti ve Medine'ye hicret etti. Bizim örneğimizdir ﷺ","ru":"Родился сиротой в Мекке, был надёжным и правдивым. Коран был ниспослан ему в пещере Хира. Призвал к Исламу и переселился в Медину. Он наш образец ﷺ","sv":"Född som föräldralös i Mecka, var han pålitlig och sanningsenlig. Koranen uppenbarades för honom i Hira-grottan. Han kallade till Islam och utvandrade till Medina. Han är vår förebild ﷺ","nl":"Geboren als wees in Mekka, was hij betrouwbaar en waarheidsgetrouw. De Koran werd aan hem geopenbaard in de grot van Hira. Hij riep op tot de Islam en emigreerde naar Medina. Hij is ons voorbeeld ﷺ","el":"Γεννήθηκε ορφανός στη Μέκκα, ήταν αξιόπιστος και αληθινός. Το Κοράνι αποκαλύφθηκε σε αυτόν στη σπηλιά Χίρα. Κάλεσε στο Ισλάμ και μετανάστευσε στη Μεδίνα. Είναι το πρότυπό μας ﷺ"},
        "lesson": {"de":"Guter Charakter und Barmherzigkeit","fr":"Bon caractère et miséricorde","tr":"Güzel ahlak ve merhamet","ru":"Хороший нрав и милосердие","sv":"God karaktär och barmhärtighet","nl":"Goed karakter en barmhartigheid","el":"Καλός χαρακτήρας και έλεος"},
        "title_extra": {"sv":"Profeternas sigill ﷺ","nl":"Zegel der profeten ﷺ","el":"Σφραγίδα των προφητών ﷺ"}},
}

def get_prophet_field(prophet, field, lang):
    """Get a translated field for a prophet, checking PROPHET_TRANSLATIONS first."""
    pid = prophet["id"]
    trans = PROPHET_TRANSLATIONS.get(pid, {})
    # Check name_extra / title_extra for name/title fields
    extra_key = f"{field}_extra"
    if extra_key in trans and lang in trans[extra_key]:
        return trans[extra_key][lang]
    # Check summary/lesson translations
    if field in trans and lang in trans[field]:
        return trans[field][lang]
    # Fallback to prophet's own data
    if field in prophet and isinstance(prophet[field], dict):
        data = prophet[field]
        if lang in data:
            return data[lang]
        # For names/titles, prefer English (romanized) over Arabic
        if field in ("name", "title"):
            return data.get("en", data.get("ar", ""))
        # For content fields, prefer Arabic (the language being taught)
        return data.get("ar", data.get("en", ""))
    return ""


# ═══════════════════════════════════════════════════════════════
# WUDU (ABLUTION) STEPS FOR KIDS
# ═══════════════════════════════════════════════════════════════

WUDU_STEPS = [
    {"step": 1, "emoji": "🤲", "ar": "النية والتسمية", "en": "Intention & Bismillah", "desc_ar": "انوِ في قلبك الوضوء لله تعالى، ثم قل: بِسْمِ اللَّه", "desc_en": "Make intention in your heart, then say: Bismillah"},
    {"step": 2, "emoji": "🫧", "ar": "غسل الكفين", "en": "Wash Palms", "desc_ar": "اغسل كفيك (يديك) ثلاث مرات، ابدأ باليمنى", "desc_en": "Wash both palms three times, start with the right"},
    {"step": 3, "emoji": "💧", "ar": "المضمضة", "en": "Rinse Mouth", "desc_ar": "أدخل الماء في فمك وتمضمض ثلاث مرات", "desc_en": "Put water in your mouth and rinse three times"},
    {"step": 4, "emoji": "💧", "ar": "الاستنشاق والاستنثار", "en": "Sniff & Blow Nose", "desc_ar": "استنشق الماء بأنفك ثم انثره ثلاث مرات", "desc_en": "Sniff water into your nose then blow it out, three times"},
    {"step": 5, "emoji": "💦", "ar": "غسل الوجه", "en": "Wash Face", "desc_ar": "اغسل وجهك ثلاث مرات من منبت الشعر إلى الذقن، ومن الأذن إلى الأذن", "desc_en": "Wash your face three times from hairline to chin, ear to ear"},
    {"step": 6, "emoji": "💧", "ar": "غسل اليد اليمنى", "en": "Wash Right Arm", "desc_ar": "اغسل يدك اليمنى من أطراف الأصابع إلى المرفق ثلاث مرات", "desc_en": "Wash your right arm from fingertips to elbow three times"},
    {"step": 7, "emoji": "💧", "ar": "غسل اليد اليسرى", "en": "Wash Left Arm", "desc_ar": "اغسل يدك اليسرى من أطراف الأصابع إلى المرفق ثلاث مرات", "desc_en": "Wash your left arm from fingertips to elbow three times"},
    {"step": 8, "emoji": "💦", "ar": "مسح الرأس", "en": "Wipe Head", "desc_ar": "بلّل يديك وامسح رأسك من المقدمة إلى المؤخرة ثم ارجع، مرة واحدة", "desc_en": "Wet your hands and wipe your head from front to back then return, once"},
    {"step": 9, "emoji": "💦", "ar": "مسح الأذنين", "en": "Wipe Ears", "desc_ar": "أدخل سبابتيك في أذنيك وامسح ظاهرهما بإبهاميك", "desc_en": "Insert index fingers in ears and wipe outer ears with thumbs"},
    {"step": 10, "emoji": "💧", "ar": "غسل القدم اليمنى", "en": "Wash Right Foot", "desc_ar": "اغسل قدمك اليمنى مع الكعبين ثلاث مرات، وخلّل بين الأصابع", "desc_en": "Wash right foot including ankles three times, between toes too"},
    {"step": 11, "emoji": "💧", "ar": "غسل القدم اليسرى", "en": "Wash Left Foot", "desc_ar": "اغسل قدمك اليسرى مع الكعبين ثلاث مرات، وخلّل بين الأصابع", "desc_en": "Wash left foot including ankles three times, between toes too"},
    {"step": 12, "emoji": "🤲", "ar": "دعاء بعد الوضوء", "en": "Dua After Wudu", "desc_ar": "أَشْهَدُ أَنْ لَا إِلَهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ، وَأَشْهَدُ أَنَّ مُحَمَّدًا عَبْدُهُ وَرَسُولُهُ، اللَّهُمَّ اجْعَلْنِي مِنَ التَّوَّابِينَ وَاجْعَلْنِي مِنَ الْمُتَطَهِّرِينَ", "desc_en": "I bear witness that none has the right to be worshipped except Allah alone, and Muhammad is His slave and Messenger. O Allah, make me of those who repent and purify themselves"},
]

# ═══════════════════════════════════════════════════════════════
# SALAH (PRAYER) STEPS FOR KIDS
# ═══════════════════════════════════════════════════════════════
# Source: Based on authentic Islamic jurisprudence (fiqh) references
# Images: 4K 3D renders generated with OpenAI gpt-image-1 (Pixar/UE5 style)
# ═══════════════════════════════════════════════════════════════

# Image path mapping (10 generated images mapped to 11 steps)
SALAH_IMAGE_MAP = {
    "qiyam_niyyah": "/assets/kids_zone/prayer_v2/prayer_step_1.webp",
    "takbir": "/assets/kids_zone/prayer_v2/prayer_step_2.webp",
    "qiyam_qiraa": "/assets/kids_zone/prayer_v2/prayer_step_3.webp",
    "qiyam_fatiha": "/assets/kids_zone/prayer_v2/prayer_step_3.webp",   # Same standing position
    "ruku": "/assets/kids_zone/prayer_v2/prayer_step_4.webp",
    "itidal": "/assets/kids_zone/prayer_v2/prayer_step_5.webp",
    "sujud_1": "/assets/kids_zone/prayer_v2/prayer_step_6.webp",
    "juloos": "/assets/kids_zone/prayer_v2/prayer_step_7.webp",
    "sujud_2": "/assets/kids_zone/prayer_v2/prayer_step_8.webp",
    "tashahhud": "/assets/kids_zone/prayer_v2/prayer_step_9.webp",
    "tasleem": "/assets/kids_zone/prayer_v2/prayer_step_10.webp",
}

SALAH_STEPS = [
    {
        "step": 1,
        "position": "qiyam_niyyah",
        "image_url": SALAH_IMAGE_MAP["qiyam_niyyah"],
        "ar": "النية والقيام",
        "en": "Intention & Standing (Niyyah & Qiyam)",
        "desc_ar": "قف مستقيماً باتجاه القبلة، واجعل بينك وبين موضع سجودك مسافة ذراع. انوِ في قلبك الصلاة التي تريد أداءها (مثلاً: نويت أن أصلي فرض الظهر أربع ركعات لله تعالى). النية محلها القلب ولا يُشترط التلفظ بها.",
        "desc_en": "Stand upright facing the Qibla, about an arm's length from where you will prostrate. Make the intention in your heart for the prayer you want to perform (e.g., I intend to pray the obligatory Dhuhr prayer, four rak'ahs, for Allah). The intention is in the heart and does not need to be spoken.",
        "dhikr_ar": "",
        "dhikr_transliteration": "",
        "body_position_ar": "الوقوف مستقيماً، النظر إلى موضع السجود",
        "body_position_en": "Standing straight, eyes looking at the place of prostration"
    },
    {
        "step": 2,
        "position": "takbir",
        "image_url": SALAH_IMAGE_MAP["takbir"],
        "ar": "تكبيرة الإحرام",
        "en": "Opening Takbir (Takbiratul Ihram)",
        "desc_ar": "ارفع يديك حذو أذنيك (أو حذو منكبيك) مع فرد الأصابع وتوجيه الكفين نحو القبلة، وقل: «اللّهُ أَكْبَر». هذه التكبيرة تبدأ بها الصلاة ويَحرُم بعدها الكلام والحركة.",
        "desc_en": "Raise both hands up to your ears (or shoulders) with fingers spread and palms facing the Qibla, and say: 'Allahu Akbar' (Allah is the Greatest). This opening Takbir begins the prayer, after which talking and unnecessary movements are forbidden.",
        "dhikr_ar": "اللّهُ أَكْبَر",
        "dhikr_transliteration": "Allahu Akbar",
        "body_position_ar": "رفع اليدين حذو الأذنين أو المنكبين",
        "body_position_en": "Hands raised to ears or shoulders level"
    },
    {
        "step": 3,
        "position": "qiyam_qiraa",
        "image_url": SALAH_IMAGE_MAP["qiyam_qiraa"],
        "ar": "وضع اليدين وقراءة دعاء الاستفتاح",
        "en": "Hands on Chest & Opening Supplication",
        "desc_ar": "ضع يدك اليمنى فوق اليسرى على صدرك. ثم اقرأ دعاء الاستفتاح: «سُبْحَانَكَ اللَّهُمَّ وَبِحَمْدِكَ، وَتَبَارَكَ اسْمُكَ، وَتَعَالَى جَدُّكَ، وَلَا إِلَهَ غَيْرُكَ». ثم قل: «أَعُوذُ بِاللَّهِ مِنَ الشَّيْطَانِ الرَّجِيمِ» و«بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ».",
        "desc_en": "Place your right hand over your left hand on your chest. Then recite the opening supplication: 'Subhanaka Allahumma wa bihamdika, wa tabaraka ismuka, wa ta'ala jadduka, wa la ilaha ghairuk.' Then say: 'A'udhu billahi minash-shaytanir-rajim' and 'Bismillahir-Rahmanir-Rahim.'",
        "dhikr_ar": "سُبْحَانَكَ اللَّهُمَّ وَبِحَمْدِكَ، وَتَبَارَكَ اسْمُكَ، وَتَعَالَى جَدُّكَ، وَلَا إِلَهَ غَيْرُكَ",
        "dhikr_transliteration": "Subhanaka Allahumma wa bihamdika, wa tabaraka ismuka, wa ta'ala jadduka, wa la ilaha ghairuk",
        "body_position_ar": "اليد اليمنى فوق اليسرى على الصدر",
        "body_position_en": "Right hand over left hand on the chest"
    },
    {
        "step": 4,
        "position": "qiyam_fatiha",
        "image_url": SALAH_IMAGE_MAP["qiyam_fatiha"],
        "ar": "قراءة سورة الفاتحة",
        "en": "Reciting Surah Al-Fatiha",
        "desc_ar": "اقرأ سورة الفاتحة كاملة وهي ركن من أركان الصلاة: «الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ ❊ الرَّحْمَنِ الرَّحِيمِ ❊ مَالِكِ يَوْمِ الدِّينِ ❊ إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ ❊ اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ ❊ صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ». ثم قل: «آمين». ثم اقرأ ما تيسر من القرآن (سورة قصيرة).",
        "desc_en": "Recite Surah Al-Fatiha completely - it is an essential pillar of prayer: 'Alhamdulillahi Rabbil 'Aalameen, Ar-Rahmanir-Raheem, Maliki Yawmid-Deen, Iyyaka na'budu wa iyyaka nasta'een, Ihdinas-Siratal-Mustaqeem, Siratal-ladhina an'amta 'alayhim ghayril-maghdubi 'alayhim walad-daalleen.' Then say 'Ameen.' Then recite what you can from the Quran (a short surah).",
        "dhikr_ar": "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ ❊ الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ...",
        "dhikr_transliteration": "Bismillahir-Rahmanir-Rahim. Alhamdulillahi Rabbil 'Aalameen...",
        "body_position_ar": "القيام مع وضع اليدين على الصدر والنظر لموضع السجود",
        "body_position_en": "Standing with hands on chest, eyes on prostration spot"
    },
    {
        "step": 5,
        "position": "ruku",
        "image_url": SALAH_IMAGE_MAP["ruku"],
        "ar": "الركوع",
        "en": "Bowing (Ruku')",
        "desc_ar": "كبّر «اللّهُ أَكْبَر» وانحنِ حتى يستوي ظهرك مع رأسك (كأنه طاولة مستوية). ضع كفيك على ركبتيك مع تفريق الأصابع. قل: «سُبْحَانَ رَبِّيَ الْعَظِيم» ثلاث مرات على الأقل.",
        "desc_en": "Say 'Allahu Akbar' and bow until your back is straight and level (like a flat table). Place your palms on your knees with fingers spread. Say: 'Subhana Rabbiyal-Adheem' (Glory be to my Lord, the Almighty) at least three times.",
        "dhikr_ar": "سُبْحَانَ رَبِّيَ الْعَظِيم (٣ مرات)",
        "dhikr_transliteration": "Subhana Rabbiyal-Adheem (3 times)",
        "body_position_ar": "الانحناء مع استواء الظهر، الكفان على الركبتين",
        "body_position_en": "Bowing with back straight and level, palms on knees"
    },
    {
        "step": 6,
        "position": "itidal",
        "image_url": SALAH_IMAGE_MAP["itidal"],
        "ar": "الاعتدال من الركوع",
        "en": "Rising from Bowing (I'tidal)",
        "desc_ar": "ارفع من الركوع قائلاً: «سَمِعَ اللّهُ لِمَنْ حَمِدَه». ثم قف مستقيماً تماماً وقل: «رَبَّنَا وَلَكَ الْحَمْد، حَمْداً كَثِيراً طَيِّباً مُبَارَكاً فِيه».",
        "desc_en": "Rise from bowing saying: 'Sami'Allahu liman hamidah' (Allah hears whoever praises Him). Then stand completely upright and say: 'Rabbana wa lakal-hamd, hamdan katheeran tayyiban mubarakan fih.'",
        "dhikr_ar": "سَمِعَ اللّهُ لِمَنْ حَمِدَه، رَبَّنَا وَلَكَ الْحَمْد",
        "dhikr_transliteration": "Sami'Allahu liman hamidah, Rabbana wa lakal-hamd",
        "body_position_ar": "الوقوف مستقيماً بعد الركوع",
        "body_position_en": "Standing straight after bowing"
    },
    {
        "step": 7,
        "position": "sujud_1",
        "image_url": SALAH_IMAGE_MAP["sujud_1"],
        "ar": "السجدة الأولى",
        "en": "First Prostration (Sujud)",
        "desc_ar": "كبّر «اللّهُ أَكْبَر» وانزل للسجود. يجب أن تسجد على سبعة أعضاء: الجبهة مع الأنف، الكفين، الركبتين، وأطراف أصابع القدمين. ارفع ذراعيك عن الأرض ولا تفرشهما. قل: «سُبْحَانَ رَبِّيَ الأَعْلَى» ثلاث مرات على الأقل. السجود أقرب ما يكون العبد من ربه.",
        "desc_en": "Say 'Allahu Akbar' and go down to prostrate. You must prostrate on seven body parts: forehead with nose, both palms, both knees, and toes of both feet. Keep your arms raised off the ground, don't spread them flat. Say: 'Subhana Rabbiyal-A'la' (Glory be to my Lord, the Most High) at least three times. Prostration is when a servant is closest to their Lord.",
        "dhikr_ar": "سُبْحَانَ رَبِّيَ الأَعْلَى (٣ مرات)",
        "dhikr_transliteration": "Subhana Rabbiyal-A'la (3 times)",
        "body_position_ar": "السجود على ٧ أعضاء: الجبهة والأنف، الكفين، الركبتين، أطراف القدمين",
        "body_position_en": "Prostrating on 7 body parts: forehead+nose, palms, knees, toes"
    },
    {
        "step": 8,
        "position": "juloos",
        "image_url": SALAH_IMAGE_MAP["juloos"],
        "ar": "الجلسة بين السجدتين",
        "en": "Sitting Between Two Prostrations",
        "desc_ar": "كبّر «اللّهُ أَكْبَر» وارفع من السجود واجلس على رجلك اليسرى مفترشاً إياها، وانصب رجلك اليمنى. ضع يديك على فخذيك. قل: «رَبِّ اغْفِرْ لِي، رَبِّ اغْفِرْ لِي» (مرتين أو أكثر).",
        "desc_en": "Say 'Allahu Akbar' and rise from prostration to sit on your left foot (spread beneath you) with your right foot upright. Place your hands on your thighs. Say: 'Rabbighfir li, Rabbighfir li' (My Lord, forgive me) twice or more.",
        "dhikr_ar": "رَبِّ اغْفِرْ لِي، رَبِّ اغْفِرْ لِي",
        "dhikr_transliteration": "Rabbighfir li, Rabbighfir li",
        "body_position_ar": "الجلوس مفترشاً الرجل اليسرى وناصباً اليمنى",
        "body_position_en": "Sitting on left foot, right foot upright"
    },
    {
        "step": 9,
        "position": "sujud_2",
        "image_url": SALAH_IMAGE_MAP["sujud_2"],
        "ar": "السجدة الثانية",
        "en": "Second Prostration (Sujud)",
        "desc_ar": "كبّر «اللّهُ أَكْبَر» واسجد مرة ثانية كالسجدة الأولى تماماً على الأعضاء السبعة. قل: «سُبْحَانَ رَبِّيَ الأَعْلَى» ثلاث مرات على الأقل. وبهذا تكتمل الركعة الأولى.",
        "desc_en": "Say 'Allahu Akbar' and prostrate again exactly like the first prostration on the seven body parts. Say: 'Subhana Rabbiyal-A'la' (Glory be to my Lord, the Most High) at least three times. This completes the first rak'ah (unit of prayer).",
        "dhikr_ar": "سُبْحَانَ رَبِّيَ الأَعْلَى (٣ مرات)",
        "dhikr_transliteration": "Subhana Rabbiyal-A'la (3 times)",
        "body_position_ar": "نفس السجدة الأولى على الأعضاء السبعة",
        "body_position_en": "Same as first prostration on seven body parts"
    },
    {
        "step": 10,
        "position": "tashahhud",
        "image_url": SALAH_IMAGE_MAP["tashahhud"],
        "ar": "التشهد (التحيات)",
        "en": "Tashahhud (Testimony of Faith)",
        "desc_ar": "بعد السجدة الثانية من الركعة الأخيرة، اجلس للتشهد. اجلس مفترشاً (في التشهد الأول) أو متوركاً (في التشهد الأخير). ضع يديك على فخذيك وأشر بسبابة يدك اليمنى عند قول «لا إله إلا الله». اقرأ التحيات: «التَّحِيَّاتُ لِلَّهِ وَالصَّلَوَاتُ وَالطَّيِّبَاتُ، السَّلَامُ عَلَيْكَ أَيُّهَا النَّبِيُّ وَرَحْمَةُ اللَّهِ وَبَرَكَاتُهُ، السَّلَامُ عَلَيْنَا وَعَلَى عِبَادِ اللَّهِ الصَّالِحِينَ، أَشْهَدُ أَنْ لَا إِلَهَ إِلَّا اللَّهُ وَأَشْهَدُ أَنَّ مُحَمَّدًا عَبْدُهُ وَرَسُولُهُ». ثم الصلاة الإبراهيمية.",
        "desc_en": "After the second prostration of the last rak'ah, sit for Tashahhud. Sit with left foot spread beneath you (first tashahhud) or in tawarruk position (final tashahhud). Place hands on thighs and point with right index finger when saying 'La ilaha illallah'. Recite At-Tahiyyat: 'At-tahiyyatu lillahi was-salawatu wat-tayyibat, as-salamu 'alayka ayyuhan-nabiyyu wa rahmatullahi wa barakatuh, as-salamu 'alayna wa 'ala 'ibadillahis-saliheen, ash-hadu an la ilaha illallah wa ash-hadu anna Muhammadan 'abduhu wa rasuluh.' Then recite the Ibrahimic prayer.",
        "dhikr_ar": "التَّحِيَّاتُ لِلَّهِ وَالصَّلَوَاتُ وَالطَّيِّبَاتُ...",
        "dhikr_transliteration": "At-tahiyyatu lillahi was-salawatu wat-tayyibat...",
        "body_position_ar": "الجلوس مع الإشارة بالسبابة",
        "body_position_en": "Sitting with index finger pointing"
    },
    {
        "step": 11,
        "position": "tasleem",
        "image_url": SALAH_IMAGE_MAP["tasleem"],
        "ar": "التسليم",
        "en": "Ending the Prayer (Tasleem)",
        "desc_ar": "التفت برأسك إلى اليمين وقل: «السَّلَامُ عَلَيْكُمْ وَرَحْمَةُ اللَّه»، ثم التفت إلى اليسار وقل: «السَّلَامُ عَلَيْكُمْ وَرَحْمَةُ اللَّه». وبهذا تنتهي الصلاة. بارك الله فيك!",
        "desc_en": "Turn your head to the right and say: 'Assalamu Alaikum wa Rahmatullah' (Peace and mercy of Allah be upon you), then turn to the left and say: 'Assalamu Alaikum wa Rahmatullah.' This completes the prayer. May Allah bless you!",
        "dhikr_ar": "السَّلَامُ عَلَيْكُمْ وَرَحْمَةُ اللَّه",
        "dhikr_transliteration": "Assalamu Alaikum wa Rahmatullah",
        "body_position_ar": "الالتفات يميناً ثم يساراً",
        "body_position_en": "Turning head right then left"
    },
]

# ═══════════════════════════════════════════════════════════════
# ARABIC ALPHABET FULL COURSE
# ═══════════════════════════════════════════════════════════════

ARABIC_ALPHABET = [
    {"letter": "أ", "name_ar": "ألف", "name_en": "Alif", "sound": "/a/", "word_ar": "أسد", "word_en": "Lion", "emoji": "🦁"},
    {"letter": "ب", "name_ar": "باء", "name_en": "Ba", "sound": "/b/", "word_ar": "بطة", "word_en": "Duck", "emoji": "🦆"},
    {"letter": "ت", "name_ar": "تاء", "name_en": "Ta", "sound": "/t/", "word_ar": "تفاحة", "word_en": "Apple", "emoji": "🍎"},
    {"letter": "ث", "name_ar": "ثاء", "name_en": "Tha", "sound": "/th/", "word_ar": "ثعلب", "word_en": "Fox", "emoji": "🦊"},
    {"letter": "ج", "name_ar": "جيم", "name_en": "Jim", "sound": "/j/", "word_ar": "جمل", "word_en": "Camel", "emoji": "🐫"},
    {"letter": "ح", "name_ar": "حاء", "name_en": "Ha", "sound": "/ḥ/", "word_ar": "حصان", "word_en": "Horse", "emoji": "🐴"},
    {"letter": "خ", "name_ar": "خاء", "name_en": "Kha", "sound": "/kh/", "word_ar": "خروف", "word_en": "Sheep", "emoji": "🐑"},
    {"letter": "د", "name_ar": "دال", "name_en": "Dal", "sound": "/d/", "word_ar": "دجاجة", "word_en": "Chicken", "emoji": "🐔"},
    {"letter": "ذ", "name_ar": "ذال", "name_en": "Dhal", "sound": "/dh/", "word_ar": "ذرة", "word_en": "Corn", "emoji": "🌽"},
    {"letter": "ر", "name_ar": "راء", "name_en": "Ra", "sound": "/r/", "word_ar": "رمان", "word_en": "Pomegranate", "emoji": "🍎"},
    {"letter": "ز", "name_ar": "زاي", "name_en": "Zay", "sound": "/z/", "word_ar": "زرافة", "word_en": "Giraffe", "emoji": "🦒"},
    {"letter": "س", "name_ar": "سين", "name_en": "Sin", "sound": "/s/", "word_ar": "سمكة", "word_en": "Fish", "emoji": "🐟"},
    {"letter": "ش", "name_ar": "شين", "name_en": "Shin", "sound": "/sh/", "word_ar": "شمس", "word_en": "Sun", "emoji": "☀️"},
    {"letter": "ص", "name_ar": "صاد", "name_en": "Sad", "sound": "/ṣ/", "word_ar": "صقر", "word_en": "Falcon", "emoji": "🦅"},
    {"letter": "ض", "name_ar": "ضاد", "name_en": "Dad", "sound": "/ḍ/", "word_ar": "ضفدع", "word_en": "Frog", "emoji": "🐸"},
    {"letter": "ط", "name_ar": "طاء", "name_en": "Taa", "sound": "/ṭ/", "word_ar": "طائر", "word_en": "Bird", "emoji": "🐦"},
    {"letter": "ظ", "name_ar": "ظاء", "name_en": "Dhaa", "sound": "/ẓ/", "word_ar": "ظرف", "word_en": "Envelope", "emoji": "✉️"},
    {"letter": "ع", "name_ar": "عين", "name_en": "Ayn", "sound": "/ʿ/", "word_ar": "عنب", "word_en": "Grapes", "emoji": "🍇"},
    {"letter": "غ", "name_ar": "غين", "name_en": "Ghayn", "sound": "/gh/", "word_ar": "غزال", "word_en": "Gazelle", "emoji": "🦌"},
    {"letter": "ف", "name_ar": "فاء", "name_en": "Fa", "sound": "/f/", "word_ar": "فراشة", "word_en": "Butterfly", "emoji": "🦋"},
    {"letter": "ق", "name_ar": "قاف", "name_en": "Qaf", "sound": "/q/", "word_ar": "قمر", "word_en": "Moon", "emoji": "🌙"},
    {"letter": "ك", "name_ar": "كاف", "name_en": "Kaf", "sound": "/k/", "word_ar": "كتاب", "word_en": "Book", "emoji": "📖"},
    {"letter": "ل", "name_ar": "لام", "name_en": "Lam", "sound": "/l/", "word_ar": "ليمون", "word_en": "Lemon", "emoji": "🍋"},
    {"letter": "م", "name_ar": "ميم", "name_en": "Mim", "sound": "/m/", "word_ar": "مسجد", "word_en": "Mosque", "emoji": "🕌"},
    {"letter": "ن", "name_ar": "نون", "name_en": "Nun", "sound": "/n/", "word_ar": "نجمة", "word_en": "Star", "emoji": "⭐"},
    {"letter": "هـ", "name_ar": "هاء", "name_en": "Ha", "sound": "/h/", "word_ar": "هلال", "word_en": "Crescent", "emoji": "🌙"},
    {"letter": "و", "name_ar": "واو", "name_en": "Waw", "sound": "/w/", "word_ar": "وردة", "word_en": "Rose", "emoji": "🌹"},
    {"letter": "ي", "name_ar": "ياء", "name_en": "Ya", "sound": "/y/", "word_ar": "يد", "word_en": "Hand", "emoji": "✋"},
]

# ═══════════════════════════════════════════════════════════════
# ARABIC VOCABULARY - NUMBERS, COLORS, ANIMALS, BODY, FAMILY
# ═══════════════════════════════════════════════════════════════

ARABIC_NUMBERS = [
    {"num": 0, "ar": "صفر", "en": "Zero", "display": "٠"}, {"num": 1, "ar": "واحد", "en": "One", "display": "١"},
    {"num": 2, "ar": "اثنان", "en": "Two", "display": "٢"}, {"num": 3, "ar": "ثلاثة", "en": "Three", "display": "٣"},
    {"num": 4, "ar": "أربعة", "en": "Four", "display": "٤"}, {"num": 5, "ar": "خمسة", "en": "Five", "display": "٥"},
    {"num": 6, "ar": "ستة", "en": "Six", "display": "٦"}, {"num": 7, "ar": "سبعة", "en": "Seven", "display": "٧"},
    {"num": 8, "ar": "ثمانية", "en": "Eight", "display": "٨"}, {"num": 9, "ar": "تسعة", "en": "Nine", "display": "٩"},
    {"num": 10, "ar": "عشرة", "en": "Ten", "display": "١٠"},
]

ARABIC_COLORS = [
    {"ar": "أحمر", "en": "Red", "emoji": "🔴", "hex": "#EF4444"},
    {"ar": "أزرق", "en": "Blue", "emoji": "🔵", "hex": "#3B82F6"},
    {"ar": "أخضر", "en": "Green", "emoji": "🟢", "hex": "#22C55E"},
    {"ar": "أصفر", "en": "Yellow", "emoji": "🟡", "hex": "#EAB308"},
    {"ar": "برتقالي", "en": "Orange", "emoji": "🟠", "hex": "#F97316"},
    {"ar": "بنفسجي", "en": "Purple", "emoji": "🟣", "hex": "#A855F7"},
    {"ar": "أبيض", "en": "White", "emoji": "⚪", "hex": "#FFFFFF"},
    {"ar": "أسود", "en": "Black", "emoji": "⚫", "hex": "#000000"},
    {"ar": "وردي", "en": "Pink", "emoji": "🩷", "hex": "#EC4899"},
    {"ar": "بني", "en": "Brown", "emoji": "🟤", "hex": "#92400E"},
]

ARABIC_ANIMALS = [
    {"ar": "أسد", "en": "Lion", "emoji": "🦁"}, {"ar": "قط", "en": "Cat", "emoji": "🐱"},
    {"ar": "كلب", "en": "Dog", "emoji": "🐶"}, {"ar": "حصان", "en": "Horse", "emoji": "🐴"},
    {"ar": "جمل", "en": "Camel", "emoji": "🐫"}, {"ar": "فيل", "en": "Elephant", "emoji": "🐘"},
    {"ar": "دجاجة", "en": "Chicken", "emoji": "🐔"}, {"ar": "سمكة", "en": "Fish", "emoji": "🐟"},
    {"ar": "فراشة", "en": "Butterfly", "emoji": "🦋"}, {"ar": "نحلة", "en": "Bee", "emoji": "🐝"},
    {"ar": "نملة", "en": "Ant", "emoji": "🐜"}, {"ar": "أرنب", "en": "Rabbit", "emoji": "🐰"},
    {"ar": "بقرة", "en": "Cow", "emoji": "🐄"}, {"ar": "خروف", "en": "Sheep", "emoji": "🐑"},
    {"ar": "طائر", "en": "Bird", "emoji": "🐦"}, {"ar": "سلحفاة", "en": "Turtle", "emoji": "🐢"},
]

ARABIC_BODY = [
    {"ar": "رأس", "en": "Head", "emoji": "🗣️"}, {"ar": "عين", "en": "Eye", "emoji": "👁️"},
    {"ar": "أنف", "en": "Nose", "emoji": "👃"}, {"ar": "فم", "en": "Mouth", "emoji": "👄"},
    {"ar": "أذن", "en": "Ear", "emoji": "👂"}, {"ar": "يد", "en": "Hand", "emoji": "✋"},
    {"ar": "قدم", "en": "Foot", "emoji": "🦶"}, {"ar": "قلب", "en": "Heart", "emoji": "❤️"},
    {"ar": "إصبع", "en": "Finger", "emoji": "☝️"}, {"ar": "شعر", "en": "Hair", "emoji": "💇"},
]

ARABIC_FAMILY = [
    {"ar": "أب / بابا", "en": "Father", "emoji": "👨"}, {"ar": "أم / ماما", "en": "Mother", "emoji": "👩"},
    {"ar": "أخ", "en": "Brother", "emoji": "👦"}, {"ar": "أخت", "en": "Sister", "emoji": "👧"},
    {"ar": "جد", "en": "Grandfather", "emoji": "👴"}, {"ar": "جدة", "en": "Grandmother", "emoji": "👵"},
    {"ar": "عم", "en": "Uncle (paternal)", "emoji": "👨"}, {"ar": "خال", "en": "Uncle (maternal)", "emoji": "👨"},
    {"ar": "عمة", "en": "Aunt (paternal)", "emoji": "👩"}, {"ar": "خالة", "en": "Aunt (maternal)", "emoji": "👩"},
    {"ar": "ابن", "en": "Son", "emoji": "👦"}, {"ar": "بنت", "en": "Daughter", "emoji": "👧"},
]

# ═══════════════════════════════════════════════════════════════
# ACHIEVEMENT BADGES
# ═══════════════════════════════════════════════════════════════

ACHIEVEMENT_BADGES = [
    {"id": "first_lesson", "emoji": "🌟", "title_ar": "الدرس الأول", "title_en": "First Lesson", "title_de": "Erste Lektion", "title_fr": "Première leçon", "title_tr": "İlk Ders", "title_ru": "Первый урок", "title_sv": "Första lektionen", "title_nl": "Eerste les", "title_el": "Πρώτο μάθημα", "desc_ar": "أكملت أول درس", "desc_en": "Completed first lesson", "condition": "total_lessons >= 1"},
    {"id": "week_streak", "emoji": "🔥", "title_ar": "أسبوع متواصل", "title_en": "Week Streak", "title_de": "Wochenserie", "title_fr": "Série hebdomadaire", "title_tr": "Haftalık Seri", "title_ru": "Неделя подряд", "title_sv": "Veckosvit", "title_nl": "Weekreeks", "title_el": "Εβδομαδιαίο σερί", "desc_ar": "7 أيام متتالية", "desc_en": "7 consecutive days", "condition": "streak >= 7"},
    {"id": "month_streak", "emoji": "💎", "title_ar": "شهر متواصل", "title_en": "Month Streak", "title_de": "Monatsserie", "title_fr": "Série mensuelle", "title_tr": "Aylık Seri", "title_ru": "Месяц подряд", "title_sv": "Månadssvit", "title_nl": "Maandreeks", "title_el": "Μηνιαίο σερί", "desc_ar": "30 يوماً متتالياً", "desc_en": "30 consecutive days", "condition": "streak >= 30"},
    {"id": "quran_starter", "emoji": "📖", "title_ar": "حافظ مبتدئ", "title_en": "Quran Starter", "title_de": "Koran-Anfänger", "title_fr": "Débutant Coran", "title_tr": "Kur'an Başlangıç", "title_ru": "Начинающий хафиз", "title_sv": "Koranbörjare", "title_nl": "Koranstarter", "title_el": "Αρχάριος Κορανίου", "desc_ar": "حفظت 10 آيات", "desc_en": "Memorized 10 ayahs", "condition": "memorized_ayahs >= 10"},
    {"id": "quran_master", "emoji": "🏆", "title_ar": "حافظ متقدم", "title_en": "Quran Master", "title_de": "Koran-Meister", "title_fr": "Maître du Coran", "title_tr": "Kur'an Ustası", "title_ru": "Мастер Корана", "title_sv": "Koranmästare", "title_nl": "Koranmeester", "title_el": "Μάστορας Κορανίου", "desc_ar": "حفظت 50 آية", "desc_en": "Memorized 50 ayahs", "condition": "memorized_ayahs >= 50"},
    {"id": "dua_collector", "emoji": "🤲", "title_ar": "جامع الأدعية", "title_en": "Dua Collector", "title_de": "Dua-Sammler", "title_fr": "Collecteur de Duas", "title_tr": "Dua Koleksiyoncusu", "title_ru": "Собиратель дуа", "title_sv": "Duasamlare", "title_nl": "Duaverzamelaar", "title_el": "Συλλέκτης ντουά", "desc_ar": "تعلمت 10 أدعية", "desc_en": "Learned 10 duas", "condition": "learned_duas >= 10"},
    {"id": "hadith_scholar", "emoji": "📜", "title_ar": "عالم الأحاديث", "title_en": "Hadith Scholar", "title_de": "Hadith-Gelehrter", "title_fr": "Savant du Hadith", "title_tr": "Hadis Alimi", "title_ru": "Знаток хадисов", "title_sv": "Hadithlärd", "title_nl": "Hadithgeleerde", "title_el": "Μελετητής Χαντίθ", "desc_ar": "تعلمت 10 أحاديث", "desc_en": "Learned 10 hadiths", "condition": "learned_hadiths >= 10"},
    {"id": "explorer", "emoji": "🗺️", "title_ar": "المستكشف", "title_en": "Explorer", "title_de": "Entdecker", "title_fr": "Explorateur", "title_tr": "Kaşif", "title_ru": "Исследователь", "title_sv": "Utforskare", "title_nl": "Ontdekker", "title_el": "Εξερευνητής", "desc_ar": "أكملت 10 دروس", "desc_en": "Completed 10 lessons", "condition": "total_lessons >= 10"},
    {"id": "scholar", "emoji": "🎓", "title_ar": "العالم الصغير", "title_en": "Little Scholar", "title_de": "Kleiner Gelehrter", "title_fr": "Petit Savant", "title_tr": "Küçük Alim", "title_ru": "Юный учёный", "title_sv": "Liten lärd", "title_nl": "Kleine geleerde", "title_el": "Μικρός μελετητής", "desc_ar": "أكملت 50 درساً", "desc_en": "Completed 50 lessons", "condition": "total_lessons >= 50"},
    {"id": "xp_100", "emoji": "⚡", "title_ar": "نجم صاعد", "title_en": "Rising Star", "title_de": "Aufgehender Stern", "title_fr": "Étoile montante", "title_tr": "Yükselen Yıldız", "title_ru": "Восходящая звезда", "title_sv": "Stigande stjärna", "title_nl": "Rijzende ster", "title_el": "Ανερχόμενο αστέρι", "desc_ar": "جمعت 100 نقطة", "desc_en": "Earned 100 XP", "condition": "xp >= 100"},
    {"id": "xp_500", "emoji": "🌟", "title_ar": "نجم لامع", "title_en": "Shining Star", "title_de": "Leuchtender Stern", "title_fr": "Étoile brillante", "title_tr": "Parlayan Yıldız", "title_ru": "Сияющая звезда", "title_sv": "Lysande stjärna", "title_nl": "Stralende ster", "title_el": "Λαμπρό αστέρι", "desc_ar": "جمعت 500 نقطة", "desc_en": "Earned 500 XP", "condition": "xp >= 500"},
    {"id": "xp_1000", "emoji": "👑", "title_ar": "النجم الذهبي", "title_en": "Golden Star", "title_de": "Goldener Stern", "title_fr": "Étoile d'or", "title_tr": "Altın Yıldız", "title_ru": "Золотая звезда", "title_sv": "Gyllene stjärna", "title_nl": "Gouden ster", "title_el": "Χρυσό αστέρι", "desc_ar": "جمعت 1000 نقطة", "desc_en": "Earned 1000 XP", "condition": "xp >= 1000"},
]

# ═══════════════════════════════════════════════════════════════
# MORE LIBRARY CONTENT
# ═══════════════════════════════════════════════════════════════

EXTENDED_LIBRARY = [
    {"id": "qs_two_sons", "category": "quran_stories", "emoji": "👦", "difficulty": 1, "age_range": "5-10",
     "title": {"ar": "قصة ابني آدم", "en": "The Two Sons of Adam"},
     "content": {"ar": "قابيل وهابيل ابنا آدم. قدما قرباناً لله فتقبل الله من هابيل ولم يتقبل من قابيل. حسد قابيل أخاه فقتله. تعلمنا أن الحسد يؤدي إلى الشر", "en": "Cain and Abel, sons of Adam. They offered a sacrifice to Allah. Allah accepted from Abel but not from Cain. Cain envied his brother and killed him. This teaches us envy leads to evil"}},
    {"id": "qs_sulayman_ant", "category": "quran_stories", "emoji": "🐜", "difficulty": 1, "age_range": "4-8",
     "title": {"ar": "سليمان والنملة", "en": "Sulayman and the Ant"},
     "content": {"ar": "كان النبي سليمان يمشي مع جيشه فسمع نملة تقول لقومها: ادخلوا مساكنكم لا يحطمنكم سليمان وجنوده. فتبسم سليمان وشكر الله", "en": "Prophet Sulayman was walking with his army when he heard an ant telling its colony: Enter your homes so Sulayman and his soldiers don't crush you. Sulayman smiled and thanked Allah"}},
    {"id": "qs_yunus_whale", "category": "quran_stories", "emoji": "🐋", "difficulty": 1, "age_range": "4-8",
     "title": {"ar": "يونس والحوت", "en": "Yunus and the Whale"},
     "content": {"ar": "التقم الحوت يونس فنادى في الظلمات: لا إله إلا أنت سبحانك إني كنت من الظالمين. فاستجاب الله له وأنقذه", "en": "The whale swallowed Yunus. He called out in the darkness: There is no god but You, glory be to You, I was wrong. Allah answered him and saved him"}},
    {"id": "ms_sharing", "category": "moral_stories", "emoji": "🤝", "difficulty": 1, "age_range": "3-7",
     "title": {"ar": "قصة المشاركة", "en": "The Sharing Story"},
     "content": {"ar": "كان سامي يملك تفاحتين كبيرتين. رأى صديقه حسن بدون طعام. قسم التفاحة وأعطاه نصفها. فرح حسن وشكره. المشاركة تجلب السعادة", "en": "Sami had two big apples. He saw his friend Hassan without food. He shared his apple and gave him half. Hassan was happy and thanked him. Sharing brings happiness"}},
    {"id": "ms_forgiveness", "category": "moral_stories", "emoji": "💝", "difficulty": 1, "age_range": "4-8",
     "title": {"ar": "العفو والتسامح", "en": "Forgiveness"},
     "content": {"ar": "كسر زيد لعبة أخته نورة بالخطأ وبكى. نورة غضبت لكنها تذكرت أن الله يحب المتسامحين فسامحته وقالت: لا بأس، سنصلحها معاً", "en": "Zaid accidentally broke his sister Noura's toy and cried. Noura was angry but remembered Allah loves those who forgive. She forgave him and said: It's okay, we'll fix it together"}},
    {"id": "sc_planets", "category": "science", "emoji": "🪐", "difficulty": 2, "age_range": "6-10",
     "title": {"ar": "الكواكب", "en": "The Planets"},
     "content": {"ar": "خلق الله الكون العظيم فيه الشمس والكواكب. عطارد أقرب كوكب للشمس، والمشتري أكبرها، والأرض كوكبنا الجميل. قال الله: أفلم ينظروا إلى السماء فوقهم كيف بنيناها", "en": "Allah created the great universe with the Sun and planets. Mercury is closest to the Sun, Jupiter is the largest, and Earth is our beautiful planet. Allah says: Have they not looked at the sky above them, how We built it?"}},
    {"id": "sc_body", "category": "science", "emoji": "🫀", "difficulty": 1, "age_range": "5-9",
     "title": {"ar": "جسم الإنسان", "en": "The Human Body"},
     "content": {"ar": "خلق الله الإنسان في أحسن تقويم. القلب يضخ الدم، والرئتان تتنفسان، والعينان تبصران، والأذنان تسمعان. سبحان الله الخالق!", "en": "Allah created humans in the best form. The heart pumps blood, lungs breathe, eyes see, and ears hear. Glory be to Allah the Creator!"}},
    {"id": "im_respect_parents", "category": "islamic_manners", "emoji": "👨‍👩‍👧", "difficulty": 1, "age_range": "3-8",
     "title": {"ar": "بر الوالدين", "en": "Respecting Parents"},
     "content": {"ar": "أمر الله ببر الوالدين وحسن معاملتهما. لا تقل لهما أف ولا تنهرهما. ساعدهما واحترمهما واطلب لهما الرحمة: رب ارحمهما كما ربياني صغيراً", "en": "Allah commands us to respect and be kind to our parents. Don't say 'uff' to them. Help them, respect them, and pray for them: My Lord, have mercy upon them as they raised me when I was small"}},
    {"id": "im_mosque_etiquette", "category": "islamic_manners", "emoji": "🕌", "difficulty": 1, "age_range": "4-8",
     "title": {"ar": "آداب المسجد", "en": "Mosque Etiquette"},
     "content": {"ar": "ادخل المسجد بالقدم اليمنى وقل: اللهم افتح لي أبواب رحمتك. كن هادئاً ولا تزعج المصلين. اجلس بأدب واستمع للخطبة. اخرج بالقدم اليسرى", "en": "Enter the mosque with your right foot and say: O Allah, open for me the doors of Your mercy. Be quiet and don't disturb those praying. Sit politely and listen to the sermon. Exit with your left foot"}},
    {"id": "nat_seasons", "category": "nature", "emoji": "🍂", "difficulty": 1, "age_range": "3-7",
     "title": {"ar": "الفصول الأربعة", "en": "The Four Seasons"},
     "content": {"ar": "خلق الله أربعة فصول: الربيع تتفتح الأزهار 🌸، الصيف حار ☀️، الخريف تتساقط الأوراق 🍂، الشتاء يهطل المطر 🌧️. كل فصل نعمة من الله", "en": "Allah created four seasons: Spring when flowers bloom 🌸, Summer is hot ☀️, Autumn leaves fall 🍂, Winter brings rain 🌧️. Each season is a blessing from Allah"}},
    {"id": "nat_trees", "category": "nature", "emoji": "🌳", "difficulty": 1, "age_range": "3-7",
     "title": {"ar": "الأشجار", "en": "Trees"},
     "content": {"ar": "الأشجار نعمة عظيمة. تعطينا الظل والأكسجين والثمار. قال الرسول ﷺ: ما من مسلم يغرس غرساً فيأكل منه إنسان أو حيوان إلا كان له صدقة", "en": "Trees are a great blessing. They give us shade, oxygen, and fruits. The Prophet ﷺ said: No Muslim plants a tree from which a person or animal eats but it is charity for him"}},
    {"id": "math_shapes", "category": "math", "emoji": "🔺", "difficulty": 1, "age_range": "3-6",
     "title": {"ar": "الأشكال الهندسية", "en": "Geometric Shapes"},
     "content": {"ar": "دائرة ⭕ ليس لها زوايا، مثلث 🔺 له ثلاث زوايا، مربع ⬛ له أربع زوايا متساوية، مستطيل له زاويتان طويلتان وزاويتان قصيرتان", "en": "Circle ⭕ has no corners, Triangle 🔺 has three corners, Square ⬛ has four equal corners, Rectangle has two long sides and two short sides"}},
    {"id": "math_counting", "category": "math", "emoji": "🔢", "difficulty": 1, "age_range": "3-5",
     "title": {"ar": "العد من 1 إلى 10", "en": "Counting 1 to 10"},
     "content": {"ar": "واحد ١ ☝️ اثنان ٢ ✌️ ثلاثة ٣ ☘️ أربعة ٤ 🍀 خمسة ٥ 🖐️ ستة ٦ 🎲 سبعة ٧ 🌈 ثمانية ٨ 🐙 تسعة ٩ ⭐ عشرة ١٠ 🔟", "en": "One 1 ☝️ Two 2 ✌️ Three 3 ☘️ Four 4 🍀 Five 5 🖐️ Six 6 🎲 Seven 7 🌈 Eight 8 🐙 Nine 9 ⭐ Ten 10 🔟"}},
]


# ═══════════════════════════════════════════════════════════════
# ADDITIONAL DUAS
# ═══════════════════════════════════════════════════════════════

EXTENDED_DUAS = [
    {"id": "sick", "category": "health", "emoji": "🤒",
     "ar": "أذهب البأس رب الناس، اشف أنت الشافي، لا شفاء إلا شفاؤك، شفاءً لا يغادر سقماً",
     "transliteration": "Adh-hibil-ba'sa Rabban-nas, ishfi antash-shafi, la shifa'a illa shifa'uka, shifa'an la yughadiru saqama",
     "en": "Remove the illness, O Lord of mankind, heal, for You are the Healer, there is no healing except Your healing, a healing that leaves no sickness",
     "title": {"ar": "للمريض", "en": "For the Sick"}},
    {"id": "fear", "category": "emotions", "emoji": "😰",
     "ar": "أعوذ بكلمات الله التامات من شر ما خلق",
     "transliteration": "A'udhu bikalimatillahit-tammati min sharri ma khalaq",
     "en": "I seek refuge in the perfect words of Allah from the evil of what He has created",
     "title": {"ar": "عند الخوف", "en": "When Afraid"}},
    {"id": "mirror", "category": "daily", "emoji": "🪞",
     "ar": "اللهم أنت حسنت خَلقي فحسن خُلقي",
     "transliteration": "Allahumma anta hassanta khalqi fahassin khuluqi",
     "en": "O Allah, You made my form beautiful, so make my character beautiful",
     "title": {"ar": "عند النظر للمرآة", "en": "Looking in the Mirror"}},
    {"id": "new_clothes", "category": "daily", "emoji": "👕",
     "ar": "الحمد لله الذي كساني هذا ورزقنيه من غير حول مني ولا قوة",
     "transliteration": "Alhamdulillahil-ladhi kasani hadha wa razaqanihi min ghayri hawlin minni wa la quwwah",
     "en": "Praise be to Allah who clothed me with this and provided it for me without any power or strength from me",
     "title": {"ar": "عند لبس ثوب جديد", "en": "Wearing New Clothes"}},
    {"id": "thunder", "category": "nature", "emoji": "⛈️",
     "ar": "سبحان الذي يسبح الرعد بحمده والملائكة من خيفته",
     "transliteration": "Subhanal-ladhi yusabbihur-ra'du bihamdihi wal-mala'ikatu min khifatih",
     "en": "Glory be to Him whom thunder and angels glorify due to His awe",
     "title": {"ar": "عند سماع الرعد", "en": "Hearing Thunder"}},
]

# ═══════════════════════════════════════════════════════════════
# ADDITIONAL HADITHS
# ═══════════════════════════════════════════════════════════════

EXTENDED_HADITHS = [
    {"id": 11, "category": "respect", "emoji": "🧓",
     "ar": "ليس منا من لم يرحم صغيرنا ويوقر كبيرنا",
     "en": "He is not one of us who does not show mercy to our young and respect to our elders",
     "source": "الترمذي", "narrator": "عبد الله بن عمرو",
     "lesson": {"ar": "احترم الكبير وارحم الصغير", "en": "Respect elders and be kind to children"}},
    {"id": 12, "category": "strength", "emoji": "💪",
     "ar": "المؤمن القوي خير وأحب إلى الله من المؤمن الضعيف",
     "en": "The strong believer is better and more beloved to Allah than the weak believer",
     "source": "مسلم", "narrator": "أبو هريرة",
     "lesson": {"ar": "كن قوياً في إيمانك وجسمك", "en": "Be strong in faith and body"}},
    {"id": 13, "category": "gratitude", "emoji": "🙏",
     "ar": "من لا يشكر الناس لا يشكر الله",
     "en": "Whoever does not thank people has not thanked Allah",
     "source": "الترمذي", "narrator": "أبو هريرة",
     "lesson": {"ar": "اشكر الناس واشكر الله", "en": "Thank people and thank Allah"}},
    {"id": 14, "category": "brotherhood", "emoji": "🤝",
     "ar": "المسلم أخو المسلم لا يظلمه ولا يخذله",
     "en": "A Muslim is a brother to another Muslim. He does not wrong him nor forsake him",
     "source": "مسلم", "narrator": "أبو هريرة",
     "lesson": {"ar": "ساعد أخاك المسلم", "en": "Help your Muslim brother"}},
    {"id": 15, "category": "character", "emoji": "🌹",
     "ar": "إن من أحبكم إلي وأقربكم مني مجلساً يوم القيامة أحاسنكم أخلاقاً",
     "en": "The most beloved and nearest to me on the Day of Judgment will be those with the best character",
     "source": "الترمذي", "narrator": "جابر بن عبد الله",
     "lesson": {"ar": "حسّن أخلاقك", "en": "Improve your character"}},
]


def get_wudu_steps(locale="ar"):
    lang = "ar" if locale == "ar" else "en"
    return [{"step": s["step"], "emoji": s["emoji"], "title": s[lang], "description": s[f"desc_{lang}"]} for s in WUDU_STEPS]

def get_salah_steps(locale="ar"):
    lang = "ar" if locale == "ar" else "en"
    result = []
    for s in SALAH_STEPS:
        step_data = {
            "step": s["step"],
            "position": s.get("position", ""),
            "image_url": s.get("image_url", ""),
            "title": s[lang],
            "description": s[f"desc_{lang}"],
            "dhikr_ar": s.get("dhikr_ar", ""),
            "dhikr_transliteration": s.get("dhikr_transliteration", ""),
            "body_position": s.get(f"body_position_{lang}", ""),
        }
        result.append(step_data)
    return result

def get_alphabet():
    return ARABIC_ALPHABET

def get_vocabulary(category="numbers"):
    if category == "numbers": return ARABIC_NUMBERS
    if category == "colors": return ARABIC_COLORS
    if category == "animals": return ARABIC_ANIMALS
    if category == "body": return ARABIC_BODY
    if category == "family": return ARABIC_FAMILY
    return []

def get_achievements(progress):
    """Check which badges user has earned."""
    earned = []
    for badge in ACHIEVEMENT_BADGES:
        cond = badge["condition"]
        key, op, val = cond.split(" ")
        val = int(val)
        user_val = progress.get(key, 0)
        if isinstance(user_val, list):
            user_val = len(user_val)
        if op == ">=" and user_val >= val:
            earned.append(badge)
    return earned

def get_all_prophets(locale="ar"):
    lang = locale if locale in ["ar", "en", "de", "fr", "tr", "ru"] else "en"
    return [{
        "id": p["id"], "number": p["number"], "emoji": p["emoji"],
        "name": p["name"].get(lang, p["name"]["en"]),
        "title": p["title"].get(lang, p["title"]["en"]),
        "summary": p["summary"].get(lang, p["summary"]["en"]),
        "lesson": p["lesson"].get(lang, p["lesson"]["en"]),
        "quran_ref": p["quran_ref"],
    } for p in ALL_PROPHETS]

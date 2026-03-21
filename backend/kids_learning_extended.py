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
    {"id": "zakariya", "number": 22, "emoji": "🙏",
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
# WUDU (ABLUTION) STEPS FOR KIDS
# ═══════════════════════════════════════════════════════════════

WUDU_STEPS = [
    {"step": 1, "emoji": "🤲", "ar": "النية", "en": "Intention (Niyyah)", "desc_ar": "انوِ في قلبك أنك تتوضأ لله", "desc_en": "Make intention in your heart to perform wudu for Allah"},
    {"step": 2, "emoji": "🙌", "ar": "غسل اليدين", "en": "Wash Hands", "desc_ar": "اغسل يديك ثلاث مرات", "desc_en": "Wash your hands three times"},
    {"step": 3, "emoji": "💧", "ar": "المضمضة", "en": "Rinse Mouth", "desc_ar": "تمضمض ثلاث مرات", "desc_en": "Rinse your mouth three times"},
    {"step": 4, "emoji": "👃", "ar": "الاستنشاق", "en": "Sniff Water", "desc_ar": "استنشق الماء ثلاث مرات", "desc_en": "Sniff water into your nose three times"},
    {"step": 5, "emoji": "😊", "ar": "غسل الوجه", "en": "Wash Face", "desc_ar": "اغسل وجهك ثلاث مرات من الأذن إلى الأذن ومن الجبهة إلى الذقن", "desc_en": "Wash your face three times from ear to ear and forehead to chin"},
    {"step": 6, "emoji": "💪", "ar": "غسل اليد اليمنى", "en": "Wash Right Arm", "desc_ar": "اغسل يدك اليمنى إلى المرفق ثلاث مرات", "desc_en": "Wash your right arm up to the elbow three times"},
    {"step": 7, "emoji": "💪", "ar": "غسل اليد اليسرى", "en": "Wash Left Arm", "desc_ar": "اغسل يدك اليسرى إلى المرفق ثلاث مرات", "desc_en": "Wash your left arm up to the elbow three times"},
    {"step": 8, "emoji": "🧕", "ar": "مسح الرأس", "en": "Wipe Head", "desc_ar": "امسح رأسك بيديك المبللتين مرة واحدة", "desc_en": "Wipe your head with wet hands once"},
    {"step": 9, "emoji": "👂", "ar": "مسح الأذنين", "en": "Wipe Ears", "desc_ar": "امسح أذنيك بإصبعيك", "desc_en": "Wipe your ears with your fingers"},
    {"step": 10, "emoji": "🦶", "ar": "غسل القدم اليمنى", "en": "Wash Right Foot", "desc_ar": "اغسل قدمك اليمنى مع الكعبين ثلاث مرات", "desc_en": "Wash your right foot including ankles three times"},
    {"step": 11, "emoji": "🦶", "ar": "غسل القدم اليسرى", "en": "Wash Left Foot", "desc_ar": "اغسل قدمك اليسرى مع الكعبين ثلاث مرات", "desc_en": "Wash your left foot including ankles three times"},
    {"step": 12, "emoji": "🤲", "ar": "الدعاء بعد الوضوء", "en": "Dua After Wudu", "desc_ar": "أشهد أن لا إله إلا الله وأشهد أن محمداً عبده ورسوله", "desc_en": "I bear witness that there is no god but Allah and Muhammad is His servant and messenger"},
]

# ═══════════════════════════════════════════════════════════════
# SALAH (PRAYER) STEPS FOR KIDS
# ═══════════════════════════════════════════════════════════════

SALAH_STEPS = [
    {"step": 1, "emoji": "🧍", "ar": "القيام والنية", "en": "Standing & Intention", "desc_ar": "قف باتجاه القبلة وانوِ الصلاة", "desc_en": "Stand facing the Qibla and make intention"},
    {"step": 2, "emoji": "🙌", "ar": "تكبيرة الإحرام", "en": "Takbiratul Ihram", "desc_ar": "ارفع يديك وقل: الله أكبر", "desc_en": "Raise your hands and say: Allahu Akbar"},
    {"step": 3, "emoji": "📖", "ar": "قراءة الفاتحة", "en": "Recite Al-Fatiha", "desc_ar": "اقرأ سورة الفاتحة", "desc_en": "Recite Surah Al-Fatiha"},
    {"step": 4, "emoji": "📖", "ar": "قراءة سورة قصيرة", "en": "Recite a Short Surah", "desc_ar": "اقرأ سورة قصيرة مثل الإخلاص", "desc_en": "Recite a short surah like Al-Ikhlas"},
    {"step": 5, "emoji": "🙇", "ar": "الركوع", "en": "Ruku (Bowing)", "desc_ar": "انحنِ وقل: سبحان ربي العظيم ثلاث مرات", "desc_en": "Bow and say: Subhana Rabbiyal Adheem three times"},
    {"step": 6, "emoji": "🧍", "ar": "الرفع من الركوع", "en": "Rising from Ruku", "desc_ar": "قم وقل: سمع الله لمن حمده، ربنا ولك الحمد", "desc_en": "Rise and say: Sami'Allahu liman hamidah, Rabbana wa lakal hamd"},
    {"step": 7, "emoji": "🧎", "ar": "السجدة الأولى", "en": "First Sujud", "desc_ar": "اسجد وقل: سبحان ربي الأعلى ثلاث مرات", "desc_en": "Prostrate and say: Subhana Rabbiyal A'la three times"},
    {"step": 8, "emoji": "🧘", "ar": "الجلسة بين السجدتين", "en": "Sitting Between Sujud", "desc_ar": "اجلس وقل: رب اغفر لي", "desc_en": "Sit and say: Rabbi ighfir li"},
    {"step": 9, "emoji": "🧎", "ar": "السجدة الثانية", "en": "Second Sujud", "desc_ar": "اسجد مرة أخرى وقل: سبحان ربي الأعلى ثلاث مرات", "desc_en": "Prostrate again and say: Subhana Rabbiyal A'la three times"},
    {"step": 10, "emoji": "🧘", "ar": "التشهد", "en": "Tashahhud", "desc_ar": "اجلس واقرأ التحيات", "desc_en": "Sit and recite At-Tahiyyat"},
    {"step": 11, "emoji": "👋", "ar": "التسليم", "en": "Tasleem", "desc_ar": "التفت يميناً وقل: السلام عليكم ورحمة الله، ثم يساراً", "desc_en": "Turn right and say: Assalamu Alaikum wa Rahmatullah, then turn left"},
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
    {"id": "first_lesson", "emoji": "🌟", "title_ar": "الدرس الأول", "title_en": "First Lesson", "desc_ar": "أكملت أول درس", "desc_en": "Completed first lesson", "condition": "total_lessons >= 1"},
    {"id": "week_streak", "emoji": "🔥", "title_ar": "أسبوع متواصل", "title_en": "Week Streak", "desc_ar": "7 أيام متتالية", "desc_en": "7 consecutive days", "condition": "streak >= 7"},
    {"id": "month_streak", "emoji": "💎", "title_ar": "شهر متواصل", "title_en": "Month Streak", "desc_ar": "30 يوماً متتالياً", "desc_en": "30 consecutive days", "condition": "streak >= 30"},
    {"id": "quran_starter", "emoji": "📖", "title_ar": "حافظ مبتدئ", "title_en": "Quran Starter", "desc_ar": "حفظت 10 آيات", "desc_en": "Memorized 10 ayahs", "condition": "memorized_ayahs >= 10"},
    {"id": "quran_master", "emoji": "🏆", "title_ar": "حافظ متقدم", "title_en": "Quran Master", "desc_ar": "حفظت 50 آية", "desc_en": "Memorized 50 ayahs", "condition": "memorized_ayahs >= 50"},
    {"id": "dua_collector", "emoji": "🤲", "title_ar": "جامع الأدعية", "title_en": "Dua Collector", "desc_ar": "تعلمت 10 أدعية", "desc_en": "Learned 10 duas", "condition": "learned_duas >= 10"},
    {"id": "hadith_scholar", "emoji": "📜", "title_ar": "عالم الأحاديث", "title_en": "Hadith Scholar", "desc_ar": "تعلمت 10 أحاديث", "desc_en": "Learned 10 hadiths", "condition": "learned_hadiths >= 10"},
    {"id": "explorer", "emoji": "🗺️", "title_ar": "المستكشف", "title_en": "Explorer", "desc_ar": "أكملت 10 دروس", "desc_en": "Completed 10 lessons", "condition": "total_lessons >= 10"},
    {"id": "scholar", "emoji": "🎓", "title_ar": "العالم الصغير", "title_en": "Little Scholar", "desc_ar": "أكملت 50 درساً", "desc_en": "Completed 50 lessons", "condition": "total_lessons >= 50"},
    {"id": "xp_100", "emoji": "⚡", "title_ar": "نجم صاعد", "title_en": "Rising Star", "desc_ar": "جمعت 100 نقطة", "desc_en": "Earned 100 XP", "condition": "xp >= 100"},
    {"id": "xp_500", "emoji": "🌟", "title_ar": "نجم لامع", "title_en": "Shining Star", "desc_ar": "جمعت 500 نقطة", "desc_en": "Earned 500 XP", "condition": "xp >= 500"},
    {"id": "xp_1000", "emoji": "👑", "title_ar": "النجم الذهبي", "title_en": "Golden Star", "desc_ar": "جمعت 1000 نقطة", "desc_en": "Earned 1000 XP", "condition": "xp >= 1000"},
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
    return [{"step": s["step"], "emoji": s["emoji"], "title": s[lang], "description": s[f"desc_{lang}"]} for s in SALAH_STEPS]

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

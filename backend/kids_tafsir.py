"""
Kids Tafsir Module - Simplified Quran Explanations for Children
==============================================================
Based on Tafsir Al-Muyassar (simplified) from King Fahd Complex
Adapted for children's understanding in 9 languages.
Source: مجمع الملك فهد لطباعة المصحف الشريف
"""

# Simplified tafsir for each ayah of kids surahs
# Keys: surah_id -> ayah_num -> {lang: explanation}
KIDS_TAFSIR = {
    "fatiha": {
        1: {
            "ar": "نبدأ بذكر اسم الله تعالى الرحمن الرحيم، ونستعين به في كل أمورنا",
            "en": "We begin by mentioning Allah's name. He is the Most Kind and Merciful. We ask for His help in everything we do",
            "de": "Wir beginnen mit dem Namen Allahs. Er ist der Gütigste und Barmherzigste. Wir bitten Ihn um Hilfe bei allem",
            "fr": "Nous commençons par le nom d'Allah. Il est le Plus Gentil et le Plus Miséricordieux. Nous demandons Son aide en tout",
            "tr": "Allah'ın adıyla başlıyoruz. O en merhametli ve şefkatlidir. Her işimizde O'ndan yardım isteriz",
            "ru": "Мы начинаем с имени Аллаха. Он самый Добрый и Милосердный. Мы просим Его помощи во всём",
            "sv": "Vi börjar med Allahs namn. Han är den Vänligaste och den Barmhärtigaste. Vi ber om Hans hjälp i allt",
            "nl": "We beginnen met de naam van Allah. Hij is de Vriendelijkste en Barmhartigste. We vragen Zijn hulp bij alles",
            "el": "Ξεκινάμε με το όνομα του Θεού. Είναι ο πιο Ευσπλαχνικός. Ζητάμε τη βοήθειά Του σε ό,τι κάνουμε"
        },
        2: {
            "ar": "نحمد الله ونشكره على كل شيء، فهو الذي خلق كل العالمين ويرعاهم",
            "en": "We praise and thank Allah for everything. He created all the worlds and takes care of everyone",
            "de": "Wir loben und danken Allah für alles. Er hat alle Welten erschaffen und kümmert sich um alle",
            "fr": "Nous louons et remercions Allah pour tout. Il a créé tous les mondes et prend soin de tout le monde",
            "tr": "Allah'a her şey için hamd ve şükür ederiz. O bütün alemleri yarattı ve herkese bakıyor",
            "ru": "Мы восхваляем и благодарим Аллаха за всё. Он создал все миры и заботится обо всех",
            "sv": "Vi prisar och tackar Allah för allt. Han skapade alla världar och tar hand om alla",
            "nl": "We prijzen en danken Allah voor alles. Hij heeft alle werelden geschapen en zorgt voor iedereen",
            "el": "Δοξάζουμε και ευχαριστούμε τον Θεό για τα πάντα. Δημιούργησε όλους τους κόσμους και φροντίζει τους πάντες"
        },
        3: {
            "ar": "الله هو الرحمن الذي يرحم جميع المخلوقات، والرحيم الذي يرحم المؤمنين رحمة خاصة",
            "en": "Allah is very kind to all His creation, and He has special mercy for those who believe in Him",
            "de": "Allah ist sehr gütig zu allen Geschöpfen und hat besondere Barmherzigkeit für die Gläubigen",
            "fr": "Allah est très bon envers toute Sa création et a une miséricorde spéciale pour les croyants",
            "tr": "Allah bütün yarattıklarına çok merhametlidir ve iman edenlere özel merhameti vardır",
            "ru": "Аллах очень добр ко всем Своим созданиям и имеет особую милость к верующим",
            "sv": "Allah är mycket vänlig mot alla sina skapelser och har särskild barmhärtighet för de troende",
            "nl": "Allah is zeer vriendelijk voor al Zijn schepping en heeft speciale barmhartigheid voor de gelovigen",
            "el": "Ο Θεός είναι πολύ καλός με όλη τη δημιουργία Του και έχει ειδικό έλεος για τους πιστούς"
        },
        4: {
            "ar": "الله هو المالك الحقيقي ليوم القيامة، يوم يحاسب الناس على أعمالهم",
            "en": "Allah is the Owner of the Day of Judgment, when everyone will be asked about their good and bad deeds",
            "de": "Allah ist der Herrscher über den Tag des Gerichts, an dem jeder über seine Taten befragt wird",
            "fr": "Allah est le Maître du Jour du Jugement, quand chacun sera interrogé sur ses bonnes et mauvaises actions",
            "tr": "Allah, herkesin iyi ve kötü amellerinden sorgulanacağı Kıyamet Gününün sahibidir",
            "ru": "Аллах — Владыка Дня Суда, когда каждого спросят о его хороших и плохих делах",
            "sv": "Allah är Härskaren över Domens dag, då alla kommer att tillfrågas om sina goda och dåliga gärningar",
            "nl": "Allah is de Meester van de Dag des Oordeels, wanneer iedereen gevraagd wordt over zijn daden",
            "el": "Ο Θεός είναι ο Κυρίαρχος της Ημέρας της Κρίσης, όταν ο καθένας θα ρωτηθεί για τις πράξεις του"
        },
        5: {
            "ar": "نحن نعبد الله وحده ولا نعبد أحداً غيره، ونطلب المساعدة منه وحده",
            "en": "We worship only Allah and ask only Him for help. No one else deserves our worship",
            "de": "Wir beten nur zu Allah und bitten nur Ihn um Hilfe. Niemand sonst verdient unsere Anbetung",
            "fr": "Nous n'adorons qu'Allah et ne demandons de l'aide qu'à Lui. Personne d'autre ne mérite notre adoration",
            "tr": "Sadece Allah'a ibadet ederiz ve sadece O'ndan yardım isteriz. Başka hiç kimse ibadete layık değildir",
            "ru": "Мы поклоняемся только Аллаху и просим помощи только у Него. Никто другой не заслуживает поклонения",
            "sv": "Vi tillber bara Allah och ber bara Honom om hjälp. Ingen annan förtjänar vår tillbedjan",
            "nl": "We aanbidden alleen Allah en vragen alleen Hem om hulp. Niemand anders verdient onze aanbidding",
            "el": "Λατρεύουμε μόνο τον Θεό και ζητάμε βοήθεια μόνο από Αυτόν. Κανείς άλλος δεν αξίζει τη λατρεία μας"
        },
        6: {
            "ar": "ندعو الله أن يهدينا إلى الطريق الصحيح، طريق الإسلام والإيمان",
            "en": "We ask Allah to guide us to the right path — the path of Islam and true faith",
            "de": "Wir bitten Allah, uns auf den richtigen Weg zu führen — den Weg des Islam und des wahren Glaubens",
            "fr": "Nous demandons à Allah de nous guider vers le droit chemin — le chemin de l'Islam et de la vraie foi",
            "tr": "Allah'tan bizi doğru yola — İslam ve gerçek iman yoluna — iletmesini isteriz",
            "ru": "Мы просим Аллаха направить нас на правильный путь — путь Ислама и истинной веры",
            "sv": "Vi ber Allah att leda oss på den rätta vägen — Islams och den sanna trons väg",
            "nl": "We vragen Allah om ons naar het rechte pad te leiden — het pad van de Islam en het ware geloof",
            "el": "Ζητάμε από τον Θεό να μας οδηγήσει στο σωστό δρόμο — τον δρόμο του Ισλάμ και της αληθινής πίστης"
        },
        7: {
            "ar": "طريق الذين أنعم الله عليهم من الأنبياء والصالحين، وليس طريق الذين غضب الله عليهم أو ضلوا",
            "en": "The path of the prophets and good people whom Allah blessed, not the path of those who went wrong",
            "de": "Der Weg der Propheten und guten Menschen, die Allah gesegnet hat, nicht der Weg derer, die falsch gingen",
            "fr": "Le chemin des prophètes et des bonnes personnes qu'Allah a bénis, pas le chemin de ceux qui se sont égarés",
            "tr": "Allah'ın nimetlendirdiği peygamberlerin ve iyi insanların yolu, yanlış yola sapanların yolu değil",
            "ru": "Путь пророков и праведных людей, которых благословил Аллах, а не путь тех, кто пошёл неправильно",
            "sv": "Profeternas och de goda människornas väg som Allah välsignade, inte de som gick fel väg",
            "nl": "Het pad van de profeten en goede mensen die Allah heeft gezegend, niet het pad van degenen die verkeerd gingen",
            "el": "Ο δρόμος των προφητών και των καλών ανθρώπων που ο Θεός ευλόγησε, όχι αυτών που πήγαν λάθος"
        },
    },
    "ikhlas": {
        1: {
            "ar": "قل يا محمد: الله واحد لا شريك له",
            "en": "Say: Allah is One. There is only one God and no one is like Him",
            "de": "Sag: Allah ist Einer. Es gibt nur einen Gott und niemand ist wie Er",
            "fr": "Dis: Allah est Unique. Il n'y a qu'un seul Dieu et personne ne Lui ressemble",
            "tr": "De ki: Allah birdir. Tek bir İlah vardır ve O'na benzer hiçbir şey yoktur",
            "ru": "Скажи: Аллах Один. Есть только один Бог и никто не подобен Ему",
            "sv": "Säg: Allah är En. Det finns bara en Gud och ingen är som Han",
            "nl": "Zeg: Allah is Eén. Er is maar één God en niemand is zoals Hij",
            "el": "Πες: Ο Θεός είναι Ένας. Υπάρχει μόνο ένας Θεός και κανείς δεν είναι σαν Αυτόν"
        },
        2: {
            "ar": "الله الصمد هو الذي يلجأ إليه جميع المخلوقات في حاجاتهم",
            "en": "Allah is the One everyone turns to when they need help. He needs nothing from anyone",
            "de": "Allah ist Derjenige, an den sich alle wenden, wenn sie Hilfe brauchen. Er braucht nichts von niemandem",
            "fr": "Allah est Celui vers qui tout le monde se tourne quand on a besoin d'aide. Il n'a besoin de rien",
            "tr": "Allah, herkesin yardıma ihtiyaç duyduğunda yöneldiği Zattır. O hiç kimseye muhtaç değildir",
            "ru": "Аллах — Тот, к Кому все обращаются за помощью. Он ни в ком не нуждается",
            "sv": "Allah är Den som alla vänder sig till när de behöver hjälp. Han behöver inget från någon",
            "nl": "Allah is Degene tot wie iedereen zich wendt als ze hulp nodig hebben. Hij heeft niets van iemand nodig",
            "el": "Ο Θεός είναι Αυτός στον Οποίο στρέφονται όλοι όταν χρειάζονται βοήθεια. Δεν χρειάζεται τίποτα"
        },
        3: {
            "ar": "الله لم يلد ولداً ولم يولد من أب أو أم، فهو الأول والآخر",
            "en": "Allah was not born and does not have children. He has always existed and will always exist",
            "de": "Allah wurde nicht geboren und hat keine Kinder. Er hat immer existiert und wird immer existieren",
            "fr": "Allah n'est pas né et n'a pas d'enfants. Il a toujours existé et existera toujours",
            "tr": "Allah doğmamıştır ve çocuğu yoktur. O her zaman var olmuştur ve her zaman var olacaktır",
            "ru": "Аллах не родился и не имеет детей. Он существовал всегда и будет существовать вечно",
            "sv": "Allah föddes inte och har inga barn. Han har alltid funnits och kommer alltid att finnas",
            "nl": "Allah is niet geboren en heeft geen kinderen. Hij heeft altijd bestaan en zal altijd bestaan",
            "el": "Ο Θεός δεν γεννήθηκε και δεν έχει παιδιά. Υπήρχε πάντα και θα υπάρχει πάντα"
        },
        4: {
            "ar": "لا يوجد أحد يشبه الله أو يساويه، فهو فريد ولا مثيل له",
            "en": "No one is equal to Allah or like Him. He is unique and nothing compares to Him",
            "de": "Niemand ist gleich wie Allah. Er ist einzigartig und nichts kann mit Ihm verglichen werden",
            "fr": "Personne n'est égal à Allah. Il est unique et rien ne Lui est comparable",
            "tr": "Hiç kimse Allah'a eşit veya O'na benzer değildir. O eşsizdir ve hiçbir şey O'nunla kıyaslanamaz",
            "ru": "Никто не равен Аллаху. Он уникален и ничто не сравнится с Ним",
            "sv": "Ingen är lika med Allah. Han är unik och inget kan jämföras med Honom",
            "nl": "Niemand is gelijk aan Allah. Hij is uniek en niets is vergelijkbaar met Hem",
            "el": "Κανείς δεν είναι ίσος με τον Θεό. Είναι μοναδικός και τίποτα δεν συγκρίνεται μαζί Του"
        },
    },
    "falaq": {
        1: {
            "ar": "قل يا محمد: أعوذ بالله الذي خلق الصبح والنور من كل شر",
            "en": "Say: I ask Allah, who creates the morning light, to protect me from all evil",
            "de": "Sag: Ich bitte Allah, der das Morgenlicht erschafft, mich vor allem Bösen zu schützen",
            "fr": "Dis: Je demande à Allah, qui crée la lumière du matin, de me protéger de tout mal",
            "tr": "De ki: Sabah aydınlığını yaratan Allah'a sığınırım, her kötülükten",
            "ru": "Скажи: Я прошу защиты у Аллаха, Который создаёт утренний свет, от всякого зла",
            "sv": "Säg: Jag ber Allah, som skapar morgonljuset, att skydda mig från allt ont",
            "nl": "Zeg: Ik vraag Allah, die het ochtendlicht schept, om mij te beschermen tegen alle kwaad",
            "el": "Πες: Ζητώ από τον Θεό, που δημιουργεί το πρωινό φως, να με προστατεύσει από κάθε κακό"
        },
        2: {
            "ar": "من شر كل المخلوقات التي قد تؤذينا",
            "en": "Protect me from the harm of anything that could hurt me",
            "de": "Schütze mich vor dem Schaden von allem, was mir schaden könnte",
            "fr": "Protège-moi du mal de tout ce qui pourrait me nuire",
            "tr": "Bana zarar verebilecek her şeyin kötülüğünden koru beni",
            "ru": "Защити меня от вреда всего, что может навредить мне",
            "sv": "Skydda mig från skada av allt som kan skada mig",
            "nl": "Bescherm mij tegen het kwaad van alles dat mij kan schaden",
            "el": "Προστάτεψέ με από το κακό οτιδήποτε μπορεί να μου βλάψει"
        },
        3: {
            "ar": "ومن شر الليل المظلم وما قد يحدث فيه",
            "en": "And protect me from the darkness of night and what may happen in it",
            "de": "Und schütze mich vor der Dunkelheit der Nacht und was darin geschehen kann",
            "fr": "Et protège-moi de l'obscurité de la nuit et de ce qui peut s'y passer",
            "tr": "Ve gecenin karanlığından ve içinde olabilecek kötülüklerden koru beni",
            "ru": "И защити меня от тьмы ночи и того, что может в ней произойти",
            "sv": "Och skydda mig från nattens mörker och vad som kan hända i det",
            "nl": "En bescherm mij tegen de duisternis van de nacht en wat erin kan gebeuren",
            "el": "Και προστάτεψέ με από το σκοτάδι της νύχτας και ό,τι μπορεί να συμβεί σε αυτό"
        },
        4: {
            "ar": "ومن شر السحرة الذين يؤذون الناس بسحرهم",
            "en": "And protect me from those who do magic and try to harm people with it",
            "de": "Und schütze mich vor denen, die Magie benutzen und versuchen, Menschen zu schaden",
            "fr": "Et protège-moi de ceux qui font de la magie et essaient de nuire aux gens",
            "tr": "Ve sihir yapan ve insanlara zarar vermeye çalışanların kötülüğünden koru beni",
            "ru": "И защити меня от тех, кто занимается колдовством и пытается навредить людям",
            "sv": "Och skydda mig från dem som gör magi och försöker skada människor",
            "nl": "En bescherm mij tegen degenen die magie gebruiken en proberen mensen te schaden",
            "el": "Και προστάτεψέ με από αυτούς που κάνουν μαγεία και προσπαθούν να βλάψουν τους ανθρώπους"
        },
        5: {
            "ar": "ومن شر الحاسد الذي يتمنى زوال نعمة غيره",
            "en": "And protect me from jealous people who wish bad things for others",
            "de": "Und schütze mich vor neidischen Menschen, die anderen Schlechtes wünschen",
            "fr": "Et protège-moi des personnes jalouses qui souhaitent du mal aux autres",
            "tr": "Ve başkalarına kötülük dileyen kıskanç insanların şerrinden koru beni",
            "ru": "И защити меня от завистливых людей, которые желают зла другим",
            "sv": "Och skydda mig från avundsjuka människor som önskar andra ont",
            "nl": "En bescherm mij tegen jaloerse mensen die anderen kwaad toewensen",
            "el": "Και προστάτεψέ με από τους ζηλόφθονους ανθρώπους που εύχονται κακό στους άλλους"
        },
    },
    "nas": {
        1: {
            "ar": "قل يا محمد: أستعيذ وألجأ إلى رب الناس وخالقهم",
            "en": "Say: I seek protection from the Lord of all people, who created everyone",
            "de": "Sag: Ich suche Schutz beim Herrn aller Menschen, der alle erschaffen hat",
            "fr": "Dis: Je cherche protection auprès du Seigneur de tous les gens, qui a créé tout le monde",
            "tr": "De ki: Herkesi yaratan insanların Rabbine sığınırım",
            "ru": "Скажи: Я прибегаю к защите Господа всех людей, Который создал всех",
            "sv": "Säg: Jag söker skydd hos alla människors Herre, som skapade alla",
            "nl": "Zeg: Ik zoek bescherming bij de Heer van alle mensen, die iedereen heeft geschapen",
            "el": "Πες: Ζητώ προστασία από τον Κύριο όλων των ανθρώπων, που δημιούργησε τους πάντες"
        },
        2: {
            "ar": "ملك الناس الذي يملك كل شيء ويحكم بالعدل",
            "en": "The King of all people who owns everything and judges fairly",
            "de": "Der König aller Menschen, dem alles gehört und der gerecht richtet",
            "fr": "Le Roi de tous les gens qui possède tout et juge avec justice",
            "tr": "Her şeye sahip olan ve adaletle hükmeden insanların Kralı",
            "ru": "Царь всех людей, Которому принадлежит всё и Который судит справедливо",
            "sv": "Alla människors Konung som äger allt och dömer rättvist",
            "nl": "De Koning van alle mensen die alles bezit en rechtvaardig oordeelt",
            "el": "Ο Βασιλιάς όλων των ανθρώπων που κατέχει τα πάντα και κρίνει δίκαια"
        },
        3: {
            "ar": "إله الناس الذي يستحق العبادة وحده",
            "en": "The God of all people who alone deserves to be worshipped",
            "de": "Der Gott aller Menschen, der allein angebetet werden sollte",
            "fr": "Le Dieu de tous les gens qui seul mérite d'être adoré",
            "tr": "Tek başına ibadete layık olan insanların İlahı",
            "ru": "Бог всех людей, Которому Одному подобает поклонение",
            "sv": "Alla människors Gud som ensam förtjänar att tillbes",
            "nl": "De God van alle mensen die alleen het waard is om aanbeden te worden",
            "el": "Ο Θεός όλων των ανθρώπων που μόνο Αυτός αξίζει να λατρεύεται"
        },
        4: {
            "ar": "من شر الشيطان الذي يوسوس ثم يختفي عندما نذكر الله",
            "en": "Protect me from the devil who whispers bad thoughts but runs away when we remember Allah",
            "de": "Schütze mich vor dem Teufel, der böse Gedanken flüstert, aber wegläuft wenn wir Allahs gedenken",
            "fr": "Protège-moi du diable qui chuchote de mauvaises pensées mais s'enfuit quand on se souvient d'Allah",
            "tr": "Allah'ı andığımızda kaçan ama kötü düşünceler fısıldayan şeytanın şerrinden koru beni",
            "ru": "Защити меня от шайтана, который нашёптывает плохие мысли, но убегает, когда мы вспоминаем Аллаха",
            "sv": "Skydda mig från djävulen som viskar onda tankar men flyr när vi minns Allah",
            "nl": "Bescherm mij tegen de duivel die slechte gedachten influistert maar vlucht als we Allah gedenken",
            "el": "Προστάτεψέ με από τον διάβολο που ψιθυρίζει κακές σκέψεις αλλά φεύγει όταν θυμόμαστε τον Θεό"
        },
        5: {
            "ar": "الذي يوسوس في قلوب الناس بالأفكار السيئة",
            "en": "The one who puts bad ideas into people's hearts and minds",
            "de": "Der böse Ideen in die Herzen und Gedanken der Menschen bringt",
            "fr": "Celui qui met de mauvaises idées dans les cœurs et les esprits des gens",
            "tr": "İnsanların kalplerine ve zihinlerine kötü fikirler sokan",
            "ru": "Который вкладывает плохие мысли в сердца и умы людей",
            "sv": "Den som lägger dåliga idéer i människors hjärtan och sinnen",
            "nl": "Degene die slechte ideeën in de harten en gedachten van mensen plaatst",
            "el": "Αυτός που βάζει κακές ιδέες στις καρδιές και τα μυαλά των ανθρώπων"
        },
        6: {
            "ar": "سواء كان من الجن أو من الناس الذين يوسوسون بالشر",
            "en": "Whether it is from the jinn or from bad people who encourage wrong things",
            "de": "Ob es von den Dschinn oder von schlechten Menschen kommt, die zu Falschem verleiten",
            "fr": "Que ce soit des djinns ou des mauvaises personnes qui encouragent le mal",
            "tr": "İster cinlerden olsun ister kötülük teşvik eden kötü insanlardan",
            "ru": "Будь то от джиннов или от плохих людей, которые подталкивают ко злу",
            "sv": "Vare sig det är från djinner eller dåliga människor som uppmuntrar till fel",
            "nl": "Of het nu van de djinn is of van slechte mensen die tot kwaad aanmoedigen",
            "el": "Είτε είναι από τα τζιν είτε από κακούς ανθρώπους που ενθαρρύνουν το κακό"
        },
    },
    "kawthar": {
        1: {
            "ar": "لقد أعطينا النبي محمد ﷺ الكوثر وهو نهر في الجنة وخيراً كثيراً",
            "en": "Allah gave Prophet Muhammad ﷺ Al-Kawthar — a river in Paradise and many blessings",
            "de": "Allah gab dem Propheten Muhammad ﷺ Al-Kauthar — einen Fluss im Paradies und viele Segnungen",
            "fr": "Allah a donné au Prophète Muhammad ﷺ Al-Kawthar — une rivière au Paradis et beaucoup de bénédictions",
            "tr": "Allah, Hz. Muhammed'e ﷺ Kevser'i — Cennette bir nehir ve birçok nimetler — verdi",
            "ru": "Аллах дал Пророку Мухаммаду ﷺ аль-Каусар — реку в Раю и множество благ",
            "sv": "Allah gav Profeten Muhammad ﷺ Al-Kawthar — en flod i Paradiset och många välsignelser",
            "nl": "Allah gaf Profeet Muhammad ﷺ Al-Kawthar — een rivier in het Paradijs en vele zegeningen",
            "el": "Ο Θεός έδωσε στον Προφήτη Μωχάμεντ ﷺ το Καουθάρ — ένα ποτάμι στον Παράδεισο και πολλές ευλογίες"
        },
        2: {
            "ar": "فصلِّ لربك شكراً له على نعمه وقدم القربان لوجهه",
            "en": "So pray to your Lord to thank Him and make sacrifice for His sake",
            "de": "So bete zu deinem Herrn um Ihm zu danken und opfere für Ihn",
            "fr": "Alors prie ton Seigneur pour Le remercier et sacrifie pour Lui",
            "tr": "O'na şükretmek için Rabbine namaz kıl ve O'nun için kurban kes",
            "ru": "Так молись своему Господу в благодарность и приноси жертву ради Него",
            "sv": "Så be till din Herre för att tacka Honom och offra för Hans skull",
            "nl": "Bid daarom tot je Heer om Hem te danken en offer voor Hem",
            "el": "Προσεύξου στον Κύριό σου για να Τον ευχαριστήσεις και θυσίασε για χάρη Του"
        },
        3: {
            "ar": "إن الذي يكرهك ويعاديك هو المقطوع من كل خير",
            "en": "The one who hates you is the one who will lose everything and be forgotten",
            "de": "Derjenige, der dich hasst, ist derjenige, der alles verlieren und vergessen werden wird",
            "fr": "Celui qui te hait est celui qui perdra tout et sera oublié",
            "tr": "Sana kin besleyen, her şeyi kaybedecek ve unutulacak olandır",
            "ru": "Тот, кто ненавидит тебя — это тот, кто потеряет всё и будет забыт",
            "sv": "Den som hatar dig är den som kommer att förlora allt och glömmas bort",
            "nl": "Degene die jou haat is degene die alles zal verliezen en vergeten zal worden",
            "el": "Αυτός που σε μισεί είναι αυτός που θα χάσει τα πάντα και θα ξεχαστεί"
        },
    },
    "asr": {
        1: {
            "ar": "أقسم الله بالعصر (الوقت) لأهميته الكبيرة في حياة الإنسان",
            "en": "Allah swears by Time, because time is very important and precious in our lives",
            "de": "Allah schwört bei der Zeit, weil die Zeit sehr wichtig und kostbar in unserem Leben ist",
            "fr": "Allah jure par le Temps, car le temps est très important et précieux dans nos vies",
            "tr": "Allah zamana yemin eder, çünkü zaman hayatımızda çok önemli ve değerlidir",
            "ru": "Аллах клянётся Временем, потому что время очень важно и ценно в нашей жизни",
            "sv": "Allah svär vid Tiden, eftersom tiden är mycket viktig och värdefull i våra liv",
            "nl": "Allah zweert bij de Tijd, omdat tijd zeer belangrijk en kostbaar is in ons leven",
            "el": "Ο Θεός ορκίζεται στον Χρόνο, γιατί ο χρόνος είναι πολύ σημαντικός στη ζωή μας"
        },
        2: {
            "ar": "إن جميع الناس في خسارة كبيرة إلا من يعمل الأعمال الصالحة",
            "en": "All people are in loss, except those who do good deeds and believe in Allah",
            "de": "Alle Menschen sind im Verlust, außer denen, die gute Taten tun und an Allah glauben",
            "fr": "Tous les gens sont en perte, sauf ceux qui font de bonnes actions et croient en Allah",
            "tr": "Bütün insanlar hüsrandadır, ancak iyi işler yapanlar ve Allah'a inananlar hariç",
            "ru": "Все люди в убытке, кроме тех, кто совершает добрые дела и верит в Аллаха",
            "sv": "Alla människor är i förlust, utom de som gör goda gärningar och tror på Allah",
            "nl": "Alle mensen zijn in verlies, behalve degenen die goede daden doen en in Allah geloven",
            "el": "Όλοι οι άνθρωποι χάνουν, εκτός από αυτούς που κάνουν καλές πράξεις και πιστεύουν στον Θεό"
        },
        3: {
            "ar": "إلا الذين آمنوا بالله وعملوا الأعمال الصالحة وتواصوا بالحق والصبر",
            "en": "Except those who believe, do good deeds, remind each other of truth and patience",
            "de": "Außer denen, die glauben, Gutes tun und sich gegenseitig zu Wahrheit und Geduld ermahnen",
            "fr": "Sauf ceux qui croient, font le bien et se rappellent mutuellement la vérité et la patience",
            "tr": "Ancak iman eden, iyi işler yapan, birbirlerine hakkı ve sabrı tavsiye edenler hariç",
            "ru": "Кроме тех, кто уверовал, совершает праведные дела и завещает друг другу истину и терпение",
            "sv": "Utom de som tror, gör gott och påminner varandra om sanning och tålamod",
            "nl": "Behalve degenen die geloven, goed doen en elkaar aansporen tot waarheid en geduld",
            "el": "Εκτός από αυτούς που πιστεύουν, κάνουν καλό και υπενθυμίζουν ο ένας στον άλλο την αλήθεια"
        },
    },
}


def get_kids_tafsir(surah_id: str, ayah_num: int, language: str = "ar") -> str:
    """Get simplified kids tafsir for a specific ayah."""
    surah_tafsir = KIDS_TAFSIR.get(surah_id, {})
    ayah_tafsir = surah_tafsir.get(ayah_num, {})
    return ayah_tafsir.get(language, ayah_tafsir.get("en", ""))


def get_surah_kids_tafsir(surah_id: str, language: str = "ar") -> dict:
    """Get all kids tafsir for a surah."""
    surah_tafsir = KIDS_TAFSIR.get(surah_id, {})
    result = {}
    for ayah_num, translations in surah_tafsir.items():
        result[ayah_num] = translations.get(language, translations.get("en", ""))
    return result

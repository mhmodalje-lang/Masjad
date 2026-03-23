"""
Kids Learning Module - Comprehensive Educational System
========================================================
- Daily Lessons (365 days, school-like curriculum)
- Quran Memorization (Juz Amma - short surahs)
- Duas for Kids (daily duas with meanings)
- Hadiths for Kids (simplified hadiths)
- Prophet Stories (25 prophets)  
- Islamic Knowledge (pillars, values, morals)
- Children's Library (categorized educational content)
- All content supports 9 languages
"""
import uuid
import random
from datetime import datetime, date
from typing import Optional

# ═══════════════════════════════════════════════════════════════
# QURAN MEMORIZATION - JUZ AMMA SHORT SURAHS
# ═══════════════════════════════════════════════════════════════

QURAN_SURAHS_FOR_KIDS = [
    {
        "id": "fatiha", "number": 1, "name_ar": "الفاتحة", "name_en": "Al-Fatiha",
        "difficulty": 1, "total_ayahs": 7,
        "ayahs": [
            {"num": 1, "ar": "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ", "en": "In the name of Allah, the Most Gracious, the Most Merciful", "de": "Im Namen Allahs, des Allerbarmers, des Barmherzigen", "fr": "Au nom d'Allah, le Tout Miséricordieux, le Très Miséricordieux", "tr": "Rahman ve Rahim olan Allah'ın adıyla", "ru": "Во имя Аллаха, Милостивого, Милосердного", "sv": "I Guds, den Nåderikes, den Barmhärtiges namn", "nl": "In de naam van Allah, de Erbarmer, de Meest Barmhartige", "el": "Στο όνομα του Θεού, του Ελεήμονος, του Οικτίρμονος"},
            {"num": 2, "ar": "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ", "en": "All praise is due to Allah, Lord of all the worlds", "de": "Alles Lob gebührt Allah, dem Herrn der Welten", "fr": "Louange à Allah, Seigneur des mondes", "tr": "Hamd, alemlerin Rabbi Allah'a mahsustur", "ru": "Хвала Аллаху, Господу миров", "sv": "Lov och pris tillkommer Gud, världarnas Herre", "nl": "Alle lof zij Allah, de Heer der werelden", "el": "Δοξασμένος ο Θεός, ο Κύριος των κόσμων"},
            {"num": 3, "ar": "الرَّحْمَنِ الرَّحِيمِ", "en": "The Most Gracious, the Most Merciful", "de": "Dem Allerbarmer, dem Barmherzigen", "fr": "Le Tout Miséricordieux, le Très Miséricordieux", "tr": "Rahman'dır, Rahim'dir", "ru": "Милостивому, Милосердному", "sv": "Den Nåderike, den Barmhärtige", "nl": "De Erbarmer, de Meest Barmhartige", "el": "Ο Ελεήμων, ο Οικτίρμων"},
            {"num": 4, "ar": "مَالِكِ يَوْمِ الدِّينِ", "en": "Master of the Day of Judgment", "de": "Dem Herrscher am Tag des Gerichts", "fr": "Maître du Jour du Jugement", "tr": "Din gününün sahibidir", "ru": "Властелину Дня воздаяния", "sv": "Härskaren över Domens dag", "nl": "Meester van de Dag des Oordeels", "el": "Κυρίαρχος της Ημέρας της Κρίσης"},
            {"num": 5, "ar": "إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ", "en": "You alone we worship, and You alone we ask for help", "de": "Dir allein dienen wir, und Dich allein bitten wir um Hilfe", "fr": "C'est Toi seul que nous adorons, et c'est Toi seul dont nous implorons secours", "tr": "Ancak Sana ibadet eder ve ancak Senden yardım dileriz", "ru": "Тебе одному мы поклоняемся и Тебя одного молим о помощи", "sv": "Dig tillber vi; Dig anropar vi om hjälp", "nl": "U alleen aanbidden wij en U alleen vragen wij om hulp", "el": "Εσένα μόνο λατρεύουμε και Εσένα μόνο ζητάμε βοήθεια"},
            {"num": 6, "ar": "اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ", "en": "Guide us to the straight path", "de": "Führe uns den geraden Weg", "fr": "Guide-nous vers le droit chemin", "tr": "Bizi doğru yola ilet", "ru": "Веди нас прямым путём", "sv": "Led oss på den raka vägen", "nl": "Leid ons op het rechte pad", "el": "Οδήγησέ μας στον ευθύ δρόμο"},
            {"num": 7, "ar": "صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ", "en": "The path of those You have blessed, not of those who earned anger, nor of those who went astray", "de": "Den Weg derer, denen Du Gnade erwiesen hast, nicht derer, die Deinen Zorn erregt haben, und nicht der Irregehenden", "fr": "Le chemin de ceux que Tu as comblés de faveurs, non pas de ceux qui ont encouru Ta colère, ni des égarés", "tr": "Kendilerine nimet verdiklerinin yoluna; gazaba uğrayanların ve sapıtanların yoluna değil", "ru": "Путём тех, кого Ты облагодетельствовал, не тех, на кого пал гнев, и не заблудших", "sv": "Den väg de vandrat som Du har välsignat, inte de som har drabbats av Din vrede och inte de som har gått vilse", "nl": "Het pad van degenen die U begunstigd hebt, niet van degenen die de toorn verdienden, noch van de dwalenden", "el": "Τον δρόμο εκείνων που ευλόγησες, όχι αυτών που προκάλεσαν την οργή Σου, ούτε αυτών που πλανήθηκαν"},
        ],
    },
    {
        "id": "ikhlas", "number": 112, "name_ar": "الإخلاص", "name_en": "Al-Ikhlas",
        "difficulty": 1, "total_ayahs": 4,
        "ayahs": [
            {"num": 1, "ar": "قُلْ هُوَ اللَّهُ أَحَدٌ", "en": "Say: He is Allah, the One", "de": "Sprich: Er ist Allah, der Einzige", "fr": "Dis: Il est Allah, Unique", "tr": "De ki: O Allah'tır, Bir'dir", "ru": "Скажи: Он - Аллах Единый", "sv": "Säg: Han är Gud, den Ende", "nl": "Zeg: Hij is Allah, de Enige", "el": "Πες: Αυτός είναι ο Θεός, ο Ένας"},
            {"num": 2, "ar": "اللَّهُ الصَّمَدُ", "en": "Allah, the Eternal Refuge", "de": "Allah, der Absolute", "fr": "Allah, Le Seul à être imploré", "tr": "Allah Samed'dir", "ru": "Аллах Вечный", "sv": "Gud, den Evige", "nl": "Allah, de Eeuwige", "el": "Ο Θεός, ο Αιώνιος"},
            {"num": 3, "ar": "لَمْ يَلِدْ وَلَمْ يُولَدْ", "en": "He neither begets nor was He begotten", "de": "Er hat nicht gezeugt und wurde nicht gezeugt", "fr": "Il n'a pas engendré, et n'a pas été engendré", "tr": "Doğurmamış ve doğmamıştır", "ru": "Он не родил и не был рождён", "sv": "Han har inte fött och inte blivit född", "nl": "Hij verwekt niet, noch is Hij verwekt", "el": "Δεν γέννησε ούτε γεννήθηκε"},
            {"num": 4, "ar": "وَلَمْ يَكُنْ لَهُ كُفُوًا أَحَدٌ", "en": "Nor is there to Him any equal", "de": "Und keiner ist Ihm gleich", "fr": "Et nul n'est égal à Lui", "tr": "Hiçbir şey O'nun dengi değildir", "ru": "И нет никого, подобного Ему", "sv": "Och ingen är Hans like", "nl": "En er is niemand gelijk aan Hem", "el": "Και κανείς δεν είναι ίσος Του"},
        ],
    },
    {
        "id": "falaq", "number": 113, "name_ar": "الفلق", "name_en": "Al-Falaq",
        "difficulty": 1, "total_ayahs": 5,
        "ayahs": [
            {"num": 1, "ar": "قُلْ أَعُوذُ بِرَبِّ الْفَلَقِ", "en": "Say: I seek refuge in the Lord of daybreak", "de": "Sprich: Ich nehme Zuflucht beim Herrn der Morgendämmerung", "fr": "Dis: Je cherche protection auprès du Seigneur de l'aube naissante", "tr": "De ki: Sabahın Rabbine sığınırım", "ru": "Скажи: Прибегаю к защите Господа рассвета", "sv": "Säg: Jag söker skydd hos gryningens Herre", "nl": "Zeg: Ik zoek toevlucht bij de Heer van de dageraad", "el": "Πες: Ζητώ καταφύγιο στον Κύριο της αυγής"},
            {"num": 2, "ar": "مِنْ شَرِّ مَا خَلَقَ", "en": "From the evil of that which He created", "de": "Vor dem Übel dessen, was Er erschaffen hat", "fr": "Contre le mal de ce qu'Il a créé", "tr": "Yarattığı şeylerin şerrinden", "ru": "От зла того, что Он сотворил", "sv": "Från det onda i det Han har skapat", "nl": "Tegen het kwaad van wat Hij heeft geschapen", "el": "Από το κακό αυτού που δημιούργησε"},
            {"num": 3, "ar": "وَمِنْ شَرِّ غَاسِقٍ إِذَا وَقَبَ", "en": "And from the evil of darkness when it settles", "de": "Und vor dem Übel der Dunkelheit, wenn sie hereinbricht", "fr": "Contre le mal de l'obscurité quand elle s'approfondit", "tr": "Karanlığı çöktüğü zaman gecenin şerrinden", "ru": "От зла мрака, когда он наступает", "sv": "Från det onda i mörkret när det lägger sig", "nl": "En tegen het kwaad van de duisternis wanneer het valt", "el": "Και από το κακό του σκότους όταν πέφτει"},
            {"num": 4, "ar": "وَمِنْ شَرِّ النَّفَّاثَاتِ فِي الْعُقَدِ", "en": "And from the evil of the blowers in knots", "de": "Und vor dem Übel der Knotenanbläserinnen", "fr": "Contre le mal de celles qui soufflent sur les nœuds", "tr": "Düğümlere üfleyenlerin şerrinden", "ru": "От зла дующих на узлы", "sv": "Från det onda hos dem som blåser på knutar", "nl": "En tegen het kwaad van de blazers op knopen", "el": "Και από το κακό αυτών που φυσούν στους κόμπους"},
            {"num": 5, "ar": "وَمِنْ شَرِّ حَاسِدٍ إِذَا حَسَدَ", "en": "And from the evil of an envier when they envy", "de": "Und vor dem Übel eines Neiders, wenn er neidet", "fr": "Et contre le mal de l'envieux quand il envie", "tr": "Haset ettiği zaman hasetçinin şerrinden", "ru": "От зла завистника, когда он завидует", "sv": "Från det onda hos den avundsjuke", "nl": "En tegen het kwaad van de jaloerse wanneer hij jaloers is", "el": "Και από το κακό του φθονερού όταν φθονεί"},
        ],
    },
    {
        "id": "nas", "number": 114, "name_ar": "الناس", "name_en": "An-Nas",
        "difficulty": 1, "total_ayahs": 6,
        "ayahs": [
            {"num": 1, "ar": "قُلْ أَعُوذُ بِرَبِّ النَّاسِ", "en": "Say: I seek refuge in the Lord of mankind", "de": "Sprich: Ich nehme Zuflucht beim Herrn der Menschen", "fr": "Dis: Je cherche protection auprès du Seigneur des hommes", "tr": "De ki: İnsanların Rabbine sığınırım", "ru": "Скажи: Прибегаю к защите Господа людей", "sv": "Säg: Jag söker skydd hos människornas Herre", "nl": "Zeg: Ik zoek toevlucht bij de Heer der mensen", "el": "Πες: Ζητώ καταφύγιο στον Κύριο των ανθρώπων"},
            {"num": 2, "ar": "مَلِكِ النَّاسِ", "en": "The King of mankind", "de": "Dem König der Menschen", "fr": "Le Souverain des hommes", "tr": "İnsanların Melikine", "ru": "Царю людей", "sv": "Människornas Konung", "nl": "De Koning der mensen", "el": "Ο Βασιλιάς των ανθρώπων"},
            {"num": 3, "ar": "إِلَهِ النَّاسِ", "en": "The God of mankind", "de": "Dem Gott der Menschen", "fr": "Le Dieu des hommes", "tr": "İnsanların İlahına", "ru": "Богу людей", "sv": "Människornas Gud", "nl": "De God der mensen", "el": "Ο Θεός των ανθρώπων"},
            {"num": 4, "ar": "مِنْ شَرِّ الْوَسْوَاسِ الْخَنَّاسِ", "en": "From the evil of the whisperer who withdraws", "de": "Vor dem Übel des sich zurückziehenden Einflüsterers", "fr": "Contre le mal du chuchoteur furtif", "tr": "Sinsi vesvesecinin şerrinden", "ru": "От зла искусителя отступающего", "sv": "Från det onda i den lismande frestaren", "nl": "Tegen het kwaad van de terugwijkende fluisteraar", "el": "Από το κακό του ψιθυριστή που υποχωρεί"},
            {"num": 5, "ar": "الَّذِي يُوَسْوِسُ فِي صُدُورِ النَّاسِ", "en": "Who whispers in the chests of mankind", "de": "Der in die Herzen der Menschen einflüstert", "fr": "Celui qui chuchote dans les poitrines des gens", "tr": "O ki insanların göğüslerine vesvese verir", "ru": "Который нашёптывает в груди людей", "sv": "Som viskar i människornas bröst", "nl": "Die fluistert in de harten van de mensen", "el": "Αυτός που ψιθυρίζει στις καρδιές των ανθρώπων"},
            {"num": 6, "ar": "مِنَ الْجِنَّةِ وَالنَّاسِ", "en": "From among the jinn and mankind", "de": "Sei er von den Dschinn oder den Menschen", "fr": "Qu'il soit parmi les djinns ou les hommes", "tr": "Cinlerden ve insanlardan", "ru": "Из числа джиннов и людей", "sv": "Vare sig de hör till de osynliga väsendena eller människorna", "nl": "Van de djinn en de mensen", "el": "Από τους τζιν και τους ανθρώπους"},
        ],
    },
    {
        "id": "kawthar", "number": 108, "name_ar": "الكوثر", "name_en": "Al-Kawthar",
        "difficulty": 1, "total_ayahs": 3,
        "ayahs": [
            {"num": 1, "ar": "إِنَّا أَعْطَيْنَاكَ الْكَوْثَرَ", "en": "Indeed, We have granted you Al-Kawthar", "de": "Wir haben dir wahrlich die Fülle gegeben", "fr": "Nous t'avons certes accordé l'Abondance", "tr": "Şüphesiz biz sana Kevser'i verdik", "ru": "Мы даровали тебе Кавсар", "sv": "Vi har sannerligen givit dig Överflöd", "nl": "Voorwaar, Wij hebben jou Al-Kawthar gegeven", "el": "Σου δώσαμε το Καουθάρ"},
            {"num": 2, "ar": "فَصَلِّ لِرَبِّكَ وَانْحَرْ", "en": "So pray to your Lord and sacrifice", "de": "So bete zu deinem Herrn und opfere", "fr": "Accomplis la Salat pour ton Seigneur et sacrifie", "tr": "Sen de Rabbine namaz kıl ve kurban kes", "ru": "Посему совершай молитву ради Господа и закалывай", "sv": "Bed därför till din Herre och offra", "nl": "Bid daarom tot jouw Heer en offer", "el": "Προσεύχου λοιπόν στον Κύριό σου και θυσίασε"},
            {"num": 3, "ar": "إِنَّ شَانِئَكَ هُوَ الْأَبْتَرُ", "en": "Indeed, your enemy is the one cut off", "de": "Wahrlich, dein Hasser ist der Abgeschnittene", "fr": "Celui qui te hait sera lui-même privé de postérité", "tr": "Şüphesiz sana buğzeden, soyu kesik olanın ta kendisidir", "ru": "Поистине, ненавистник твой - он бесплоден", "sv": "Den som hatar dig - det är han som är den avskurne", "nl": "Voorwaar, degene die jou haat, hij is degene die afgesneden is", "el": "Αυτός που σε μισεί είναι ο αποκομμένος"},
        ],
    },
    {
        "id": "asr", "number": 103, "name_ar": "العصر", "name_en": "Al-Asr",
        "difficulty": 1, "total_ayahs": 3,
        "ayahs": [
            {"num": 1, "ar": "وَالْعَصْرِ", "en": "By time", "de": "Bei der Zeit", "fr": "Par le Temps", "tr": "Asra yemin olsun", "ru": "Клянусь временем", "sv": "Vid Tiden", "nl": "Bij de tijd", "el": "Μα τον χρόνο"},
            {"num": 2, "ar": "إِنَّ الْإِنْسَانَ لَفِي خُسْرٍ", "en": "Indeed, mankind is in loss", "de": "Der Mensch befindet sich wahrlich in Verlust", "fr": "L'homme est certes en perdition", "tr": "İnsan gerçekten ziyan içindedir", "ru": "Поистине, человек в убытке", "sv": "Människan förlorar sannerligen", "nl": "Voorwaar, de mens is in verlies", "el": "Ο άνθρωπος είναι σε απώλεια"},
            {"num": 3, "ar": "إِلَّا الَّذِينَ آمَنُوا وَعَمِلُوا الصَّالِحَاتِ وَتَوَاصَوْا بِالْحَقِّ وَتَوَاصَوْا بِالصَّبْرِ", "en": "Except those who believe, do good, urge truth, and urge patience", "de": "Außer denjenigen, die glauben und rechtschaffen handeln und einander zur Wahrheit und zur Geduld ermahnen", "fr": "Sauf ceux qui croient, font de bonnes œuvres, s'enjoignent la vérité et s'enjoignent la patience", "tr": "Ancak iman edip salih ameller işleyenler, birbirlerine hakkı ve sabrı tavsiye edenler müstesna", "ru": "Кроме тех, которые уверовали, совершали благие дела, призывали к истине и призывали к терпению", "sv": "Utom de som tror och lever rättskaffens, manar varandra till sanning och manar varandra till tålamod", "nl": "Behalve degenen die geloven en goede werken verrichten en elkaar aansporen tot de waarheid en tot geduld", "el": "Εκτός από αυτούς που πιστεύουν, κάνουν καλό, προτρέπουν στην αλήθεια και στην υπομονή"},
        ],
    },
    {
        "id": "nasr", "number": 110, "name_ar": "النصر", "name_en": "An-Nasr",
        "difficulty": 2, "total_ayahs": 3,
        "ayahs": [
            {"num": 1, "ar": "إِذَا جَاءَ نَصْرُ اللَّهِ وَالْفَتْحُ", "en": "When the victory of Allah has come and the conquest", "de": "Wenn Allahs Hilfe kommt und der Sieg", "fr": "Lorsque vient le secours d'Allah et la victoire", "tr": "Allah'ın yardımı ve fetih geldiğinde", "ru": "Когда придёт помощь Аллаха и победа", "sv": "När Guds hjälp och seger kommer", "nl": "Wanneer de hulp van Allah en de overwinning komen", "el": "Όταν έρθει η βοήθεια του Θεού και η νίκη"},
            {"num": 2, "ar": "وَرَأَيْتَ النَّاسَ يَدْخُلُونَ فِي دِينِ اللَّهِ أَفْوَاجًا", "en": "And you see people entering the religion of Allah in multitudes", "de": "Und du die Menschen in Scharen in Allahs Religion eintreten siehst", "fr": "Et que tu vois les gens entrer en foule dans la religion d'Allah", "tr": "İnsanların bölük bölük Allah'ın dinine girdiklerini gördüğünde", "ru": "И увидишь людей, вступающих в религию Аллаха толпами", "sv": "Och du ser människorna inträda i Guds religion i skaror", "nl": "En je de mensen in menigten de religie van Allah ziet binnentreden", "el": "Και βλέπεις τους ανθρώπους να μπαίνουν στη θρησκεία του Θεού σε πλήθη"},
            {"num": 3, "ar": "فَسَبِّحْ بِحَمْدِ رَبِّكَ وَاسْتَغْفِرْهُ إِنَّهُ كَانَ تَوَّابًا", "en": "Then exalt with praise of your Lord and ask forgiveness; indeed He is ever accepting of repentance", "de": "Dann lobpreise deinen Herrn und bitte Ihn um Vergebung; Er ist wahrlich der Reue-Annehmende", "fr": "Alors glorifie ton Seigneur et implore Son pardon; Il est certes le Grand Accueillant au repentir", "tr": "Rabbini hamd ile tesbih et ve O'ndan mağfiret dile; çünkü O tövbeleri çok kabul edendir", "ru": "Восславь хвалой Господа и проси у Него прощения; поистине, Он - Принимающий покаяние", "sv": "Lova då din Herres ära och be om Hans förlåtelse; Han tar ständigt emot ånger", "nl": "Prijs dan de lof van jouw Heer en vraag Hem om vergeving; Hij is zeker de Aanvaarder van berouw", "el": "Δόξασε τον Κύριό σου και ζήτα συγχώρεση; Είναι πάντα δεκτικός μετάνοιας"},
        ],
    },
    {
        "id": "masad", "number": 111, "name_ar": "المسد", "name_en": "Al-Masad",
        "difficulty": 2, "total_ayahs": 5,
        "ayahs": [
            {"num": 1, "ar": "تَبَّتْ يَدَا أَبِي لَهَبٍ وَتَبَّ", "en": "May the hands of Abu Lahab be ruined, and ruined is he", "de": "Zugrunde gehen sollen die Hände Abu Lahabs, und zugrunde gehen soll er", "fr": "Que périssent les deux mains d'Abu Lahab et que lui-même périsse", "tr": "Ebu Leheb'in elleri kurusun, kurudu da", "ru": "Да пропадут руки Абу Лахаба, и сам он пропадёт", "sv": "Abu Lahabs händer skall förgås och han själv skall förgås", "nl": "Mogen de handen van Abu Lahab vergaan, en moge hij vergaan", "el": "Ας χαθούν τα χέρια του Αμπού Λαχάμπ"},
            {"num": 2, "ar": "مَا أَغْنَى عَنْهُ مَالُهُ وَمَا كَسَبَ", "en": "His wealth and gains will not avail him", "de": "Sein Besitz und das, was er erworben hat, nützen ihm nichts", "fr": "Ses biens ne lui serviront à rien, ni ce qu'il a acquis", "tr": "Malı ve kazandıkları ona fayda vermedi", "ru": "Не помогло ему его богатство и то, что он приобрёл", "sv": "Hans rikedom och allt hans förvärvande skall inte gagna honom", "nl": "Zijn bezit en wat hij verworven heeft zullen hem niet baten", "el": "Δεν θα τον ωφελήσει ο πλούτος του"},
            {"num": 3, "ar": "سَيَصْلَى نَارًا ذَاتَ لَهَبٍ", "en": "He will be burned in a Fire of blazing flame", "de": "Er wird einem Feuer ausgesetzt sein, das lodert", "fr": "Il sera exposé à un Feu plein de flammes", "tr": "Alevli bir ateşe girecektir", "ru": "Он будет гореть в пламенном огне", "sv": "Han skall stötas i en flammande Eld", "nl": "Hij zal branden in een laaiend Vuur", "el": "Θα καεί σε φλεγόμενη Φωτιά"},
            {"num": 4, "ar": "وَامْرَأَتُهُ حَمَّالَةَ الْحَطَبِ", "en": "And his wife, the carrier of firewood", "de": "Und seine Frau, die Trägerin des Brennholzes", "fr": "De même sa femme, la porteuse de bois", "tr": "Karısı da odun taşıyıcısı olarak", "ru": "И жена его — носительница дров", "sv": "Och hans hustru, vedslitaren", "nl": "En zijn vrouw, de draagster van brandhout", "el": "Και η γυναίκα του, η μεταφορέας ξύλων"},
            {"num": 5, "ar": "فِي جِيدِهَا حَبْلٌ مِنْ مَسَدٍ", "en": "Around her neck is a rope of palm fiber", "de": "An ihrem Hals hängt ein Strick aus Palmfaser", "fr": "A son cou une corde de fibres", "tr": "Boynunda bükülmüş hurma lifinden bir ip olduğu halde", "ru": "На шее у неё верёвка из пальмовых волокон", "sv": "Om hennes hals ett rep av palmfiber", "nl": "Om haar nek een touw van palmvezel", "el": "Στον λαιμό της ένα σχοινί από ίνες φοίνικα"},
        ],
    },
]

# ═══════════════════════════════════════════════════════════════
# KIDS DUAS (Daily Duas with Multilingual Meanings)
# ═══════════════════════════════════════════════════════════════

KIDS_DUAS = [
    {"id": "wake_up", "category": "daily", "emoji": "🌅",
     "ar": "الحَمْدُ لِلَّهِ الَّذِي أَحْيَانَا بَعْدَ مَا أَمَاتَنَا وَإِلَيْهِ النُّشُورُ",
     "transliteration": "Alhamdu lillahil-lathee ahyana ba'da ma amatana wa ilayhin-nushoor",
     "en": "Praise be to Allah who gave us life after death and unto Him is the return",
     "de": "Lob sei Allah, Der uns Leben gab nach dem Tod und zu Ihm ist die Rückkehr",
     "fr": "Louange à Allah qui nous a donné la vie après la mort et vers Lui est le retour",
     "tr": "Bizi öldürdükten sonra dirilten ve dönüş kendisine olan Allah'a hamd olsun",
     "ru": "Хвала Аллаху, Который оживил нас после того, как умертвил, и к Нему воскрешение",
     "sv": "Lov och pris tillkommer Allah som gav oss liv efter döden och till Honom är återkomsten",
     "nl": "Alle lof zij Allah die ons leven gaf na de dood en tot Hem is de terugkeer",
     "el": "Δόξα στον Αλλάχ που μας έδωσε ζωή μετά τον θάνατο και σε Αυτόν είναι η επιστροφή",
     "title": {"ar": "دعاء الاستيقاظ", "en": "Waking Up", "de": "Beim Aufwachen", "fr": "Au réveil", "tr": "Uyanınca", "ru": "При пробуждении", "sv": "Vid uppvaknande", "nl": "Bij het wakker worden", "el": "Κατά το ξύπνημα"}},
    {"id": "sleep", "category": "daily", "emoji": "🌙",
     "ar": "بِاسْمِكَ اللَّهُمَّ أَمُوتُ وَأَحْيَا",
     "transliteration": "Bismika Allahumma amootu wa ahya",
     "en": "In Your name, O Allah, I die and I live",
     "de": "In Deinem Namen, o Allah, sterbe ich und lebe ich",
     "fr": "En Ton nom, ô Allah, je meurs et je vis",
     "tr": "Senin adınla, ey Allah'ım, ölür ve yaşarım",
     "ru": "С именем Твоим, о Аллах, я умираю и живу",
     "sv": "I Ditt namn, o Allah, dör jag och lever jag",
     "nl": "In Uw naam, o Allah, sterf ik en leef ik",
     "el": "Στο όνομά Σου, ω Αλλάχ, πεθαίνω και ζω",
     "title": {"ar": "دعاء النوم", "en": "Before Sleep", "de": "Vor dem Schlafen", "fr": "Avant de dormir", "tr": "Uyumadan önce", "ru": "Перед сном", "sv": "Före sömn", "nl": "Voor het slapen", "el": "Πριν τον ύπνο"}},
    {"id": "eat_before", "category": "food", "emoji": "🍽️",
     "ar": "بِسْمِ اللَّهِ",
     "transliteration": "Bismillah",
     "en": "In the name of Allah",
     "de": "Im Namen Allahs",
     "fr": "Au nom d'Allah",
     "tr": "Allah'ın adıyla",
     "ru": "Во имя Аллаха",
     "sv": "I Allahs namn",
     "nl": "In de naam van Allah",
     "el": "Στο όνομα του Αλλάχ",
     "title": {"ar": "قبل الأكل", "en": "Before Eating", "de": "Vor dem Essen", "fr": "Avant de manger", "tr": "Yemekten önce", "ru": "Перед едой", "sv": "Före maten", "nl": "Voor het eten", "el": "Πριν το φαγητό"}},
    {"id": "eat_after", "category": "food", "emoji": "😋",
     "ar": "الحَمْدُ لِلَّهِ الَّذِي أَطْعَمَنَا وَسَقَانَا وَجَعَلَنَا مُسْلِمِينَ",
     "transliteration": "Alhamdu lillahil-lathee at'amana wa saqana wa ja'alana muslimeen",
     "en": "Praise be to Allah Who fed us and gave us drink and made us Muslims",
     "de": "Lob sei Allah, Der uns gespeist und getränkt und uns zu Muslimen gemacht hat",
     "fr": "Louange à Allah qui nous a nourris, abreuvés et faits musulmans",
     "tr": "Bizi yediren, içiren ve Müslüman kılan Allah'a hamd olsun",
     "ru": "Хвала Аллаху, Который накормил нас, напоил и сделал мусульманами",
     "sv": "Lov och pris tillkommer Allah som gav oss mat och dryck och gjorde oss till muslimer",
     "nl": "Alle lof zij Allah die ons voedde, te drinken gaf en ons moslims maakte",
     "el": "Δόξα στον Αλλάχ που μας τάισε, μας πότισε και μας έκανε μουσουλμάνους",
     "title": {"ar": "بعد الأكل", "en": "After Eating", "de": "Nach dem Essen", "fr": "Après manger", "tr": "Yemekten sonra", "ru": "После еды", "sv": "Efter maten", "nl": "Na het eten", "el": "Μετά το φαγητό"}},
    {"id": "enter_home", "category": "daily", "emoji": "🏠",
     "ar": "بِسْمِ اللَّهِ وَلَجْنَا، وَبِسْمِ اللَّهِ خَرَجْنَا، وَعَلَى اللَّهِ رَبِّنَا تَوَكَّلْنَا",
     "transliteration": "Bismillahi walajna, wa bismillahi kharajna, wa 'ala Allahi Rabbina tawakkalna",
     "en": "In the name of Allah we enter, in the name of Allah we leave, and upon Allah our Lord we rely",
     "de": "Im Namen Allahs treten wir ein, im Namen Allahs gehen wir hinaus, und auf Allah, unseren Herrn, vertrauen wir",
     "fr": "Au nom d'Allah nous entrons, au nom d'Allah nous sortons, et sur Allah notre Seigneur nous comptons",
     "tr": "Allah'ın adıyla girdik, Allah'ın adıyla çıktık ve Rabbimiz Allah'a tevekkül ettik",
     "ru": "Именем Аллаха мы входим, именем Аллаха выходим и на Аллаха, нашего Господа, уповаем",
     "sv": "I Allahs namn träder vi in, i Allahs namn går vi ut, och på Allah, vår Herre, förlitar vi oss",
     "nl": "In de naam van Allah treden wij binnen, in de naam van Allah gaan wij naar buiten, en op Allah, onze Heer, vertrouwen wij",
     "el": "Στο όνομα του Αλλάχ μπαίνουμε, στο όνομα του Αλλάχ βγαίνουμε, και στον Αλλάχ τον Κύριό μας στηριζόμαστε",
     "title": {"ar": "دخول المنزل", "en": "Entering Home", "de": "Beim Heimkommen", "fr": "En entrant à la maison", "tr": "Eve girerken", "ru": "При входе в дом", "sv": "Hemkomst", "nl": "Bij thuiskomst", "el": "Εισερχόμενοι στο σπίτι"}},
    {"id": "leave_home", "category": "daily", "emoji": "🚪",
     "ar": "بِسْمِ اللَّهِ تَوَكَّلْتُ عَلَى اللَّهِ وَلَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ",
     "transliteration": "Bismillahi tawakkaltu 'ala Allah, wa la hawla wa la quwwata illa billah",
     "en": "In the name of Allah, I rely on Allah. There is no power nor might except with Allah",
     "de": "Im Namen Allahs, ich vertraue auf Allah. Es gibt keine Macht und keine Kraft außer bei Allah",
     "fr": "Au nom d'Allah, je m'en remets à Allah. Il n'y a de force ni de puissance qu'en Allah",
     "tr": "Allah'ın adıyla, Allah'a tevekkül ettim. Güç ve kuvvet ancak Allah'tandır",
     "ru": "Именем Аллаха, я уповаю на Аллаха. Нет силы и мощи, кроме как у Аллаха",
     "sv": "I Allahs namn, jag förlitar mig på Allah. Det finns ingen makt eller styrka utom hos Allah",
     "nl": "In de naam van Allah, ik vertrouw op Allah. Er is geen macht of kracht behalve bij Allah",
     "el": "Στο όνομα του Αλλάχ, στηρίζομαι στον Αλλάχ. Δεν υπάρχει δύναμη ούτε ισχύς παρά μόνο από τον Αλλάχ",
     "title": {"ar": "الخروج من المنزل", "en": "Leaving Home", "de": "Beim Verlassen des Hauses", "fr": "En sortant de la maison", "tr": "Evden çıkarken", "ru": "При выходе из дома", "sv": "Att lämna hemmet", "nl": "Het huis verlaten", "el": "Φεύγοντας από το σπίτι"}},
    {"id": "enter_mosque", "category": "prayer", "emoji": "🕌",
     "ar": "اللَّهُمَّ افْتَحْ لِي أَبْوَابَ رَحْمَتِكَ",
     "transliteration": "Allahumma iftah li abwaba rahmatik",
     "en": "O Allah, open for me the doors of Your mercy",
     "de": "O Allah, öffne mir die Tore Deiner Barmherzigkeit",
     "fr": "Ô Allah, ouvre-moi les portes de Ta miséricorde",
     "tr": "Allah'ım, bana rahmet kapılarını aç",
     "ru": "О Аллах, открой для меня врата Твоей милости",
     "sv": "O Allah, öppna för mig dörrarna till Din barmhärtighet",
     "nl": "O Allah, open voor mij de deuren van Uw genade",
     "el": "Ω Αλλάχ, άνοιξε για μένα τις πύλες του ελέους Σου",
     "title": {"ar": "دخول المسجد", "en": "Entering Mosque", "de": "Beim Betreten der Moschee", "fr": "En entrant à la mosquée", "tr": "Camiye girerken", "ru": "При входе в мечеть", "sv": "Att gå in i moskén", "nl": "Bij het betreden van de moskee", "el": "Εισερχόμενοι στο τζαμί"}},
    {"id": "enter_bathroom", "category": "daily", "emoji": "🚿",
     "ar": "بِسْمِ اللَّهِ، اللَّهُمَّ إِنِّي أَعُوذُ بِكَ مِنَ الْخُبُثِ وَالْخَبَائِثِ",
     "transliteration": "Bismillah, Allahumma inni a'udhu bika minal-khubthi wal-khaba'ith",
     "en": "In the name of Allah. O Allah, I seek refuge in You from evil",
     "de": "Im Namen Allahs. O Allah, ich suche Zuflucht bei Dir vor dem Bösen",
     "fr": "Au nom d'Allah. Ô Allah, je cherche refuge auprès de Toi contre le mal",
     "tr": "Allah'ın adıyla. Allah'ım, kötülükten Sana sığınırım",
     "ru": "Именем Аллаха. О Аллах, я прибегаю к Тебе от зла",
     "sv": "I Allahs namn. O Allah, jag söker skydd hos Dig från det onda",
     "nl": "In de naam van Allah. O Allah, ik zoek toevlucht bij U tegen het kwaad",
     "el": "Στο όνομα του Αλλάχ. Ω Αλλάχ, ζητώ καταφύγιο σε Εσένα από το κακό",
     "title": {"ar": "دخول الحمام", "en": "Entering Bathroom", "de": "Beim Betreten des Badezimmers", "fr": "En entrant aux toilettes", "tr": "Tuvalete girerken", "ru": "При входе в туалет", "sv": "Att gå in på toaletten", "nl": "Bij het betreden van de badkamer", "el": "Εισερχόμενοι στην τουαλέτα"}},
    {"id": "travel", "category": "daily", "emoji": "✈️",
     "ar": "سُبْحَانَ الَّذِي سَخَّرَ لَنَا هَذَا وَمَا كُنَّا لَهُ مُقْرِنِينَ وَإِنَّا إِلَى رَبِّنَا لَمُنْقَلِبُونَ",
     "transliteration": "Subhana-llathee sakh-khara lana hatha wa ma kunna lahu muqrineen, wa inna ila Rabbina lamunqaliboon",
     "en": "Glory to Him who has subjected this to us, we could never have accomplished this ourselves. To our Lord we shall surely return",
     "de": "Gepriesen sei Der, Der uns dies dienstbar gemacht hat, wir hätten es selbst nicht vermocht. Zu unserem Herrn kehren wir gewiss zurück",
     "fr": "Gloire à Celui qui a mis ceci à notre service, nous n'aurions pu le faire. Vers notre Seigneur nous retournerons",
     "tr": "Bunu bizim hizmetimize veren Allah münezzehtir, yoksa biz buna güç yetiremezdik. Şüphesiz biz Rabbimize döneceğiz",
     "ru": "Пречист Тот, Кто подчинил нам это, ведь мы сами не смогли бы этого. К нашему Господу мы вернёмся",
     "sv": "Ära till Den som underkastade detta åt oss, vi hade aldrig klarat det själva. Till vår Herre ska vi återvända",
     "nl": "Glorie aan Hem die dit aan ons onderdanig heeft gemaakt, wij hadden dit zelf nooit gekund. Tot onze Heer zullen wij terugkeren",
     "el": "Δόξα σε Αυτόν που υπέταξε αυτό σε εμάς, δεν θα μπορούσαμε μόνοι μας. Στον Κύριό μας θα επιστρέψουμε",
     "title": {"ar": "دعاء السفر", "en": "Travel Prayer", "de": "Reisegebet", "fr": "Prière du voyage", "tr": "Yolculuk duası", "ru": "Молитва путешественника", "sv": "Resebön", "nl": "Reisgebed", "el": "Προσευχή ταξιδιού"}},
    {"id": "rain", "category": "nature", "emoji": "🌧️",
     "ar": "اللَّهُمَّ صَيِّبًا نَافِعًا",
     "transliteration": "Allahumma sayyiban nafi'an",
     "en": "O Allah, let it be beneficial rain",
     "de": "O Allah, lass es nützlichen Regen sein",
     "fr": "Ô Allah, fais qu'il soit une pluie bénéfique",
     "tr": "Allah'ım, faydalı yağmur yağdır",
     "ru": "О Аллах, пусть будет полезный дождь",
     "sv": "O Allah, låt det vara nyttigt regn",
     "nl": "O Allah, laat het nuttige regen zijn",
     "el": "Ω Αλλάχ, ας είναι ωφέλιμη βροχή",
     "title": {"ar": "عند المطر", "en": "When It Rains", "de": "Bei Regen", "fr": "Quand il pleut", "tr": "Yağmur yağınca", "ru": "Во время дождя", "sv": "När det regnar", "nl": "Wanneer het regent", "el": "Όταν βρέχει"}},
    {"id": "parents", "category": "family", "emoji": "👨‍👩‍👧‍👦",
     "ar": "رَبِّ ارْحَمْهُمَا كَمَا رَبَّيَانِي صَغِيرًا",
     "transliteration": "Rabbi irhamhuma kama rabbayanee sagheera",
     "en": "My Lord, have mercy upon them as they brought me up when I was small",
     "de": "Mein Herr, erbarme Dich ihrer, wie sie mich aufzogen, als ich klein war",
     "fr": "Mon Seigneur, fais-leur miséricorde comme ils m'ont élevé quand j'étais petit",
     "tr": "Rabbim, onlara merhamet et, tıpkı beni küçükken büyüttükleri gibi",
     "ru": "Господи, помилуй их, как они воспитывали меня, когда я был маленьким",
     "sv": "Min Herre, förbarma Dig över dem som de fostrade mig när jag var liten",
     "nl": "Mijn Heer, ontferm U over hen zoals zij mij opvoedden toen ik klein was",
     "el": "Κύριέ μου, ελέησέ τους όπως με μεγάλωσαν όταν ήμουν μικρός",
     "title": {"ar": "دعاء للوالدين", "en": "For Parents", "de": "Für die Eltern", "fr": "Pour les parents", "tr": "Anne baba için", "ru": "За родителей", "sv": "För föräldrarna", "nl": "Voor ouders", "el": "Για τους γονείς"}},
    {"id": "knowledge", "category": "learning", "emoji": "📚",
     "ar": "رَبِّ زِدْنِي عِلْمًا",
     "transliteration": "Rabbi zidni 'ilma",
     "en": "My Lord, increase me in knowledge",
     "de": "Mein Herr, vermehre mein Wissen",
     "fr": "Mon Seigneur, augmente-moi en science",
     "tr": "Rabbim, ilmimi artır",
     "ru": "Господи, приумножь моё знание",
     "sv": "Min Herre, öka min kunskap",
     "nl": "Mijn Heer, vermeerder mijn kennis",
     "el": "Κύριέ μου, αύξησε τη γνώση μου",
     "title": {"ar": "طلب العلم", "en": "Seeking Knowledge", "de": "Wissen suchen", "fr": "Recherche du savoir", "tr": "İlim öğrenirken", "ru": "Поиск знаний", "sv": "Kunskapssökning", "nl": "Kennis zoeken", "el": "Αναζήτηση γνώσης"}},
    {"id": "distress", "category": "emotions", "emoji": "😔",
     "ar": "لَا إِلَهَ إِلَّا أَنْتَ سُبْحَانَكَ إِنِّي كُنْتُ مِنَ الظَّالِمِينَ",
     "transliteration": "La ilaha illa anta subhanaka inni kuntu minaz-zalimeen",
     "en": "There is no god but You, glory be to You, indeed I was among the wrongdoers",
     "de": "Es gibt keinen Gott außer Dir, gepriesen seist Du, ich war wahrlich unter den Ungerechten",
     "fr": "Il n'y a pas de divinité sauf Toi, gloire à Toi, j'étais certes parmi les injustes",
     "tr": "Senden başka ilah yoktur, Seni tenzih ederim, gerçekten ben zalimlerden oldum",
     "ru": "Нет бога, кроме Тебя, пречист Ты, поистине, я был из числа несправедливых",
     "sv": "Det finns ingen gud utom Du, ära vare Dig, jag var sannerligen bland de orättfärdiga",
     "nl": "Er is geen god dan U, verheerlijkt zijt Gij, ik was waarlijk onder de onrechtvaardigen",
     "el": "Δεν υπάρχει θεός εκτός από Εσένα, δόξα Σοι, ήμουν από τους αδίκους",
     "title": {"ar": "عند الضيق", "en": "In Distress", "de": "In Not", "fr": "Dans la détresse", "tr": "Sıkıntıda", "ru": "В беде", "sv": "I nöd", "nl": "In nood", "el": "Σε δυσκολία"}},
    {"id": "morning", "category": "daily", "emoji": "☀️",
     "ar": "أَصْبَحْنَا وَأَصْبَحَ الْمُلْكُ لِلَّهِ وَالْحَمْدُ لِلَّهِ",
     "transliteration": "Asbahna wa asbahal-mulku lillah, walhamdu lillah",
     "en": "We have entered the morning and all dominion belongs to Allah, and praise be to Allah",
     "de": "Wir sind in den Morgen eingetreten und alle Herrschaft gehört Allah, und Lob sei Allah",
     "fr": "Nous avons atteint le matin et toute la royauté appartient à Allah, et louange à Allah",
     "tr": "Sabaha erdik, mülk de Allah'ın oldu, hamd Allah'adır",
     "ru": "Мы вступили в утро, и вся власть принадлежит Аллаху, и хвала Аллаху",
     "sv": "Vi har nått morgonen och all herravälde tillhör Allah, och lov och pris tillkommer Allah",
     "nl": "Wij zijn de ochtend ingegaan en alle heerschappij behoort Allah toe, en alle lof zij Allah",
     "el": "Μπήκαμε στο πρωί και όλη η εξουσία ανήκει στον Αλλάχ, και δόξα στον Αλλάχ",
     "title": {"ar": "أذكار الصباح", "en": "Morning Dhikr", "de": "Morgengedenken", "fr": "Dhikr du matin", "tr": "Sabah zikri", "ru": "Утренний зикр", "sv": "Morgonåminnelse", "nl": "Ochtend dhikr", "el": "Πρωινό ζικρ"}},
    {"id": "evening", "category": "daily", "emoji": "🌆",
     "ar": "أَمْسَيْنَا وَأَمْسَى الْمُلْكُ لِلَّهِ وَالْحَمْدُ لِلَّهِ",
     "transliteration": "Amsayna wa amsal-mulku lillah, walhamdu lillah",
     "en": "We have entered the evening and all dominion belongs to Allah, and praise be to Allah",
     "de": "Wir sind in den Abend eingetreten und alle Herrschaft gehört Allah, und Lob sei Allah",
     "fr": "Nous avons atteint le soir et toute la royauté appartient à Allah, et louange à Allah",
     "tr": "Akşama erdik, mülk de Allah'ın oldu, hamd Allah'adır",
     "ru": "Мы вступили в вечер, и вся власть принадлежит Аллаху, и хвала Аллаху",
     "sv": "Vi har nått kvällen och all herravälde tillhör Allah, och lov och pris tillkommer Allah",
     "nl": "Wij zijn de avond ingegaan en alle heerschappij behoort Allah toe, en alle lof zij Allah",
     "el": "Μπήκαμε στο βράδυ και όλη η εξουσία ανήκει στον Αλλάχ, και δόξα στον Αλλάχ",
     "title": {"ar": "أذكار المساء", "en": "Evening Dhikr", "de": "Abendgedenken", "fr": "Dhikr du soir", "tr": "Akşam zikri", "ru": "Вечерний зикр", "sv": "Kvällsåminnelse", "nl": "Avond dhikr", "el": "Βραδινό ζικρ"}},
]

# ═══════════════════════════════════════════════════════════════
# KIDS HADITHS (Simplified Hadiths with Multilingual Translations)
# ═══════════════════════════════════════════════════════════════

KIDS_HADITHS = [
    {"id": 1, "category": "kindness", "emoji": "💖",
     "ar": "مَنْ لا يَرْحَمُ النَّاسَ لا يَرْحَمْهُ اللهُ",
     "en": "Whoever does not show mercy to people, Allah will not show mercy to him",
     "de": "Wer den Menschen keine Barmherzigkeit zeigt, dem zeigt Allah keine Barmherzigkeit",
     "fr": "Celui qui ne fait pas preuve de miséricorde envers les gens, Allah ne lui fera pas miséricorde",
     "tr": "İnsanlara merhamet etmeyene Allah merhamet etmez",
     "ru": "Кто не проявляет милосердия к людям, Аллах не проявит к нему милосердия",
     "sv": "Den som inte visar barmhärtighet mot människor, Allah visar inte barmhärtighet mot honom",
     "nl": "Wie geen genade toont aan de mensen, Allah toont geen genade aan hem",
     "el": "Όποιος δεν δείχνει έλεος στους ανθρώπους, ο Αλλάχ δεν θα δείξει έλεος σε αυτόν",
     "source": "البخاري ومسلم", "narrator": "جرير بن عبد الله",
     "lesson": {"ar": "كن رحيماً مع الناس والحيوانات", "en": "Be kind to people and animals", "de": "Sei freundlich zu Menschen und Tieren", "fr": "Sois gentil avec les gens et les animaux", "tr": "İnsanlara ve hayvanlara karşı merhametli ol", "ru": "Будь добр к людям и животным", "sv": "Var snäll mot människor och djur", "nl": "Wees vriendelijk voor mensen en dieren", "el": "Να είσαι καλός με ανθρώπους και ζώα"}},
    {"id": 2, "category": "honesty", "emoji": "✅",
     "ar": "عليكم بالصدق فإن الصدق يهدي إلى البر وإن البر يهدي إلى الجنة",
     "en": "You must be truthful, for truthfulness leads to righteousness and righteousness leads to Paradise",
     "de": "Ihr müsst wahrhaftig sein, denn Wahrhaftigkeit führt zur Rechtschaffenheit und Rechtschaffenheit führt zum Paradies",
     "fr": "Soyez véridiques, car la véracité mène à la droiture et la droiture mène au Paradis",
     "tr": "Doğru sözlü olun, çünkü doğruluk iyiliğe götürür ve iyilik cennete götürür",
     "ru": "Будьте правдивы, ибо правдивость ведёт к праведности, а праведность ведёт в Рай",
     "sv": "Var sanningsenliga, ty sanningen leder till rättfärdighet och rättfärdighet leder till Paradiset",
     "nl": "Wees waarheidsgetrouw, want waarheidsgetrouwheid leidt tot rechtschapenheid en rechtschapenheid leidt tot het Paradijs",
     "el": "Να είστε αληθινοί, γιατί η αλήθεια οδηγεί στη δικαιοσύνη και η δικαιοσύνη οδηγεί στον Παράδεισο",
     "source": "البخاري ومسلم", "narrator": "عبد الله بن مسعود",
     "lesson": {"ar": "قل الصدق دائماً", "en": "Always tell the truth", "de": "Sage immer die Wahrheit", "fr": "Dis toujours la vérité", "tr": "Her zaman doğruyu söyle", "ru": "Всегда говори правду", "sv": "Säg alltid sanningen", "nl": "Spreek altijd de waarheid", "el": "Πάντα λέγε την αλήθεια"}},
    {"id": 3, "category": "smile", "emoji": "😊",
     "ar": "لا تَحْقِرَنَّ مِنَ المَعْرُوفِ شَيْئًا وَلَوْ أَنْ تَلْقَى أَخَاكَ بِوَجْهٍ طَلْقٍ",
     "en": "Do not belittle any good deed, even meeting your brother with a cheerful face",
     "de": "Verachte keine gute Tat, selbst wenn du deinem Bruder mit einem fröhlichen Gesicht begegnest",
     "fr": "Ne dédaigne aucune bonne action, même rencontrer ton frère avec un visage joyeux",
     "tr": "Hiçbir iyiliği küçük görme, kardeşini güler yüzle karşılasan bile",
     "ru": "Не пренебрегай никаким добрым делом, даже встречая брата с весёлым лицом",
     "sv": "Förakta ingen god gärning, även att möta din broder med ett glatt ansikte",
     "nl": "Kijk niet neer op enig goed werk, zelfs niet het ontmoeten van je broeder met een vrolijk gezicht",
     "el": "Μην υποτιμάς καμία καλή πράξη, ακόμα και να συναντάς τον αδελφό σου με χαρούμενο πρόσωπο",
     "source": "مسلم", "narrator": "أبو ذر",
     "lesson": {"ar": "ابتسم دائماً", "en": "Always smile", "de": "Lächle immer", "fr": "Souris toujours", "tr": "Her zaman gülümse", "ru": "Всегда улыбайся", "sv": "Le alltid", "nl": "Lach altijd", "el": "Χαμογέλα πάντα"}},
    {"id": 4, "category": "manners", "emoji": "🤝",
     "ar": "من كان يؤمن بالله واليوم الآخر فليقل خيراً أو ليصمت",
     "en": "Whoever believes in Allah and the Last Day should speak good or keep silent",
     "de": "Wer an Allah und den Jüngsten Tag glaubt, soll Gutes sprechen oder schweigen",
     "fr": "Quiconque croit en Allah et au Jour dernier, qu'il dise du bien ou qu'il se taise",
     "tr": "Allah'a ve ahiret gününe iman eden, ya hayır söylesin ya da sussun",
     "ru": "Кто верует в Аллаха и Последний день, пусть говорит благое или молчит",
     "sv": "Den som tror på Allah och den Yttersta dagen ska tala gott eller tiga",
     "nl": "Wie in Allah en de Laatste Dag gelooft, laat hem goed spreken of zwijgen",
     "el": "Όποιος πιστεύει στον Αλλάχ και στην Τελευταία Ημέρα, ας μιλά καλά ή ας σιωπά",
     "source": "البخاري ومسلم", "narrator": "أبو هريرة",
     "lesson": {"ar": "تكلم بالخير أو اسكت", "en": "Speak good or stay silent", "de": "Sprich Gutes oder schweige", "fr": "Dis du bien ou tais-toi", "tr": "Ya hayır söyle ya sus", "ru": "Говори доброе или молчи", "sv": "Tala gott eller tig", "nl": "Spreek goed of zwijg", "el": "Μίλα καλά ή σιώπα"}},
    {"id": 5, "category": "cleanliness", "emoji": "🧼",
     "ar": "الطهور شطر الإيمان",
     "en": "Cleanliness is half of faith",
     "de": "Sauberkeit ist die Hälfte des Glaubens",
     "fr": "La propreté est la moitié de la foi",
     "tr": "Temizlik imanın yarısıdır",
     "ru": "Чистота — половина веры",
     "sv": "Renlighet är halva tron",
     "nl": "Reinheid is de helft van het geloof",
     "el": "Η καθαριότητα είναι η μισή πίστη",
     "source": "مسلم", "narrator": "أبو مالك الأشعري",
     "lesson": {"ar": "حافظ على نظافتك", "en": "Keep yourself clean", "de": "Halte dich sauber", "fr": "Reste propre", "tr": "Temizliğine dikkat et", "ru": "Содержи себя в чистоте", "sv": "Håll dig ren", "nl": "Houd jezelf schoon", "el": "Κράτα τον εαυτό σου καθαρό"}},
    {"id": 6, "category": "neighbors", "emoji": "🏘️",
     "ar": "ما زال جبريل يوصيني بالجار حتى ظننت أنه سيورثه",
     "en": "Jibreel kept advising me about the neighbor until I thought he would make him an heir",
     "de": "Jibril empfahl mir den Nachbarn so oft, dass ich dachte, er würde ihn zum Erben machen",
     "fr": "Jibreel n'a cessé de me recommander le voisin au point que j'ai pensé qu'il en ferait un héritier",
     "tr": "Cebrail bana komşu hakkında o kadar tavsiyede bulundu ki komşuyu mirasçı yapacak sandım",
     "ru": "Джибриль так часто наставлял меня о соседе, что я подумал, он сделает его наследником",
     "sv": "Jibril påminde mig så ofta om grannen att jag trodde han skulle göra honom till arvinge",
     "nl": "Jibriel bleef mij zo over de buurman adviseren dat ik dacht dat hij hem erfgenaam zou maken",
     "el": "Ο Τζιμπρίλ συνέχιζε να με συμβουλεύει για τον γείτονα ώσπου νόμισα ότι θα τον κάνει κληρονόμο",
     "source": "البخاري ومسلم", "narrator": "عائشة",
     "lesson": {"ar": "أحسن إلى جيرانك", "en": "Be good to your neighbors", "de": "Sei gut zu deinen Nachbarn", "fr": "Sois bon envers tes voisins", "tr": "Komşularına iyi davran", "ru": "Будь добр к соседям", "sv": "Var god mot dina grannar", "nl": "Wees goed voor je buren", "el": "Να είσαι καλός με τους γείτονές σου"}},
    {"id": 7, "category": "knowledge", "emoji": "📖",
     "ar": "مَنْ يُرِدِ اللهُ بِهِ خَيْرًا يُفَقِّهْهُ فِي الدِّينِ",
     "en": "When Allah wants good for someone, He grants him understanding of the religion",
     "de": "Wenn Allah jemandem Gutes will, gewährt Er ihm Verständnis der Religion",
     "fr": "Quand Allah veut du bien pour quelqu'un, Il lui accorde la compréhension de la religion",
     "tr": "Allah bir kişiye hayır dilerse, onu dinde fakih kılar",
     "ru": "Когда Аллах желает блага кому-то, Он дарует ему понимание религии",
     "sv": "När Allah vill gott för någon, skänker Han honom förståelse av religionen",
     "nl": "Wanneer Allah goed wil voor iemand, schenkt Hij hem begrip van de religie",
     "el": "Όταν ο Αλλάχ θέλει καλό για κάποιον, του χαρίζει κατανόηση της θρησκείας",
     "source": "البخاري", "narrator": "معاوية بن أبي سفيان",
     "lesson": {"ar": "تعلم كل يوم شيئاً جديداً", "en": "Learn something new every day", "de": "Lerne jeden Tag etwas Neues", "fr": "Apprends quelque chose de nouveau chaque jour", "tr": "Her gün yeni bir şey öğren", "ru": "Учись чему-то новому каждый день", "sv": "Lär dig något nytt varje dag", "nl": "Leer elke dag iets nieuws", "el": "Μάθε κάτι νέο κάθε μέρα"}},
    {"id": 8, "category": "nature", "emoji": "🌱",
     "ar": "ما من مسلم يغرس غرساً فيأكل منه طير أو إنسان أو بهيمة إلا كان له به صدقة",
     "en": "No Muslim plants a tree from which a bird, a human, or an animal eats but that it is charity for him",
     "de": "Kein Muslim pflanzt einen Baum, von dem ein Vogel, ein Mensch oder ein Tier isst, ohne dass es für ihn eine Wohltätigkeit ist",
     "fr": "Aucun musulman ne plante un arbre dont mange un oiseau, un humain ou un animal sans que cela soit une aumône pour lui",
     "tr": "Bir Müslüman bir ağaç diker de ondan kuş, insan veya hayvan yerse, bu onun için sadakadır",
     "ru": "Не посадит мусульманин дерево, от которого поест птица, человек или животное, без того, чтобы это не было для него милостыней",
     "sv": "Ingen muslim planterar ett träd som en fågel, en människa eller ett djur äter av utan att det räknas som välgörenhet",
     "nl": "Geen moslim plant een boom waarvan een vogel, mens of dier eet, of het wordt als liefdadigheid beschouwd",
     "el": "Κανένας μουσουλμάνος δεν φυτεύει δέντρο από το οποίο τρώει πουλί, άνθρωπος ή ζώο χωρίς να είναι ελεημοσύνη",
     "source": "البخاري ومسلم", "narrator": "أنس بن مالك",
     "lesson": {"ar": "ازرع واعتنِ بالبيئة", "en": "Plant trees and care for the environment", "de": "Pflanze Bäume und kümmere dich um die Umwelt", "fr": "Plante des arbres et prends soin de l'environnement", "tr": "Ağaç dik ve çevreye özen göster", "ru": "Сажай деревья и заботься об окружающей среде", "sv": "Plantera träd och ta hand om miljön", "nl": "Plant bomen en zorg voor het milieu", "el": "Φύτεψε δέντρα και φρόντισε το περιβάλλον"}},
    {"id": 9, "category": "patience", "emoji": "🌟",
     "ar": "عجباً لأمر المؤمن إن أمره كله خير",
     "en": "How amazing is the affair of the believer, for all of his affairs are good",
     "de": "Wie wunderbar ist die Angelegenheit des Gläubigen, denn all seine Angelegenheiten sind gut",
     "fr": "Comme l'affaire du croyant est étonnante, car toutes ses affaires sont bonnes",
     "tr": "Müminin durumu ne güzeldir! Onun her hali hayırdır",
     "ru": "Удивительно положение верующего — все его дела благие",
     "sv": "Hur underbar är den troendes situation, allt i hans liv är gott",
     "nl": "Hoe wonderlijk is de zaak van de gelovige, al zijn zaken zijn goed",
     "el": "Πόσο θαυμαστή είναι η υπόθεση του πιστού, όλες οι υποθέσεις του είναι καλές",
     "source": "مسلم", "narrator": "صهيب الرومي",
     "lesson": {"ar": "كن إيجابياً دائماً", "en": "Always be positive", "de": "Sei immer positiv", "fr": "Sois toujours positif", "tr": "Her zaman olumlu ol", "ru": "Всегда будь позитивным", "sv": "Var alltid positiv", "nl": "Wees altijd positief", "el": "Να είσαι πάντα θετικός"}},
    {"id": 10, "category": "food", "emoji": "🥘",
     "ar": "كلوا واشربوا ولا تسرفوا",
     "en": "Eat and drink, but do not waste",
     "de": "Esst und trinkt, aber verschwendet nicht",
     "fr": "Mangez et buvez, mais ne gaspillez pas",
     "tr": "Yiyin, için fakat israf etmeyin",
     "ru": "Ешьте и пейте, но не расточительствуйте",
     "sv": "Ät och drick, men slösa inte",
     "nl": "Eet en drink, maar verspil niet",
     "el": "Φάτε και πιείτε, αλλά μη σπαταλάτε",
     "source": "القرآن - الأعراف 31", "narrator": "",
     "lesson": {"ar": "لا تبذر في الطعام", "en": "Don't waste food", "de": "Verschwende kein Essen", "fr": "Ne gaspille pas la nourriture", "tr": "Yiyeceği israf etme", "ru": "Не трать еду впустую", "sv": "Slösa inte mat", "nl": "Verspil geen eten", "el": "Μη σπαταλάς φαγητό"}},
]

# ═══════════════════════════════════════════════════════════════
# PROPHET STORIES FOR KIDS
# ═══════════════════════════════════════════════════════════════

PROPHET_STORIES = [
    {"id": "adam", "number": 1, "emoji": "🌍",
     "name": {"ar": "آدم", "en": "Adam", "de": "Adam", "fr": "Adam", "tr": "Adem", "ru": "Адам", "sv": "Adam", "nl": "Adam", "el": "Αδάμ"},
     "title": {"ar": "أبو البشرية", "en": "Father of Humanity", "de": "Vater der Menschheit", "fr": "Père de l'Humanité", "tr": "İnsanlığın Babası", "ru": "Отец человечества", "sv": "Mänsklighetens fader", "nl": "Vader van de mensheid", "el": "Πατέρας της Ανθρωπότητας"},
     "summary": {
         "ar": "خلق الله آدم من طين وعلمه أسماء كل شيء. كان أول إنسان وأول نبي. سكن الجنة مع حواء ثم نزل إلى الأرض",
         "en": "Allah created Adam from clay and taught him the names of all things. He was the first human and first prophet. He lived in Paradise with Hawwa then came to Earth",
         "de": "Allah erschuf Adam aus Ton und lehrte ihn die Namen aller Dinge. Er war der erste Mensch und der erste Prophet",
         "fr": "Allah a créé Adam d'argile et lui a enseigné les noms de toutes choses. Il était le premier humain et le premier prophète",
         "tr": "Allah, Adem'i çamurdan yarattı ve ona her şeyin ismini öğretti. İlk insan ve ilk peygamberdi",
         "ru": "Аллах создал Адама из глины и научил его именам всех вещей. Он был первым человеком и первым пророком",
     },
     "lesson": {"ar": "التوبة والاستغفار", "en": "Repentance and seeking forgiveness", "de": "Reue und um Vergebung bitten", "fr": "Le repentir et demander pardon", "tr": "Tövbe etmek ve af dilemek", "ru": "Покаяние и просьба о прощении"},
     "quran_ref": "البقرة 30-38"},
    {"id": "nuh", "number": 2, "emoji": "🚢",
     "name": {"ar": "نوح", "en": "Nuh (Noah)", "de": "Nuh (Noah)", "fr": "Nouh (Noé)", "tr": "Nuh", "ru": "Нух (Ной)", "sv": "Nuh (Noa)", "nl": "Nuh (Noach)", "el": "Νουχ (Νώε)"},
     "title": {"ar": "صاحب السفينة", "en": "Builder of the Ark", "de": "Erbauer der Arche", "fr": "Constructeur de l'Arche", "tr": "Geminin Sahibi", "ru": "Строитель Ковчега", "sv": "Arkens byggare", "nl": "Bouwer van de Ark", "el": "Κατασκευαστής της Κιβωτού"},
     "summary": {
         "ar": "دعا قومه 950 سنة إلى عبادة الله. بنى سفينة كبيرة بأمر الله وحمل فيها من كل زوجين اثنين. جاء الطوفان وغرق الكافرون",
         "en": "He called his people to worship Allah for 950 years. He built a great ark by Allah's command and carried pairs of every creature. The flood came and the disbelievers drowned",
         "de": "Er rief sein Volk 950 Jahre lang zur Anbetung Allahs. Er baute eine große Arche auf Allahs Befehl",
         "fr": "Il a appelé son peuple à adorer Allah pendant 950 ans. Il a construit une grande arche sur l'ordre d'Allah",
         "tr": "Kavmini 950 yıl boyunca Allah'a ibadete çağırdı. Allah'ın emriyle büyük bir gemi inşa etti",
         "ru": "Он призывал свой народ к поклонению Аллаху 950 лет. Построил великий ковчег по велению Аллаха",
     },
     "lesson": {"ar": "الصبر والمثابرة", "en": "Patience and perseverance", "de": "Geduld und Ausdauer", "fr": "La patience et la persévérance", "tr": "Sabır ve azim", "ru": "Терпение и настойчивость"},
     "quran_ref": "هود 25-49"},
    {"id": "ibrahim", "number": 3, "emoji": "🕋",
     "name": {"ar": "إبراهيم", "en": "Ibrahim (Abraham)", "de": "Ibrahim (Abraham)", "fr": "Ibrahim (Abraham)", "tr": "İbrahim", "ru": "Ибрахим (Авраам)", "sv": "Ibrahim (Abraham)", "nl": "Ibrahim (Abraham)", "el": "Ιμπραχίμ (Αβραάμ)"},
     "title": {"ar": "خليل الله", "en": "Friend of Allah", "de": "Freund Allahs", "fr": "Ami d'Allah", "tr": "Allah'ın Dostu", "ru": "Друг Аллаха", "sv": "Guds vän", "nl": "Vriend van Allah", "el": "Φίλος του Θεού"},
     "summary": {
         "ar": "كسر الأصنام وحده ودعا إلى توحيد الله. ألقي في النار فجعلها الله برداً وسلاماً. بنى الكعبة مع ابنه إسماعيل",
         "en": "He broke the idols alone and called to the worship of One God. He was thrown into fire but Allah made it cool and peaceful. He built the Kaaba with his son Ismail",
         "de": "Er zerbrach allein die Götzen und rief zur Anbetung des einen Gottes. Er wurde ins Feuer geworfen, aber Allah machte es kühl und friedlich",
         "fr": "Il a brisé les idoles seul et appelé à l'adoration d'un seul Dieu. Il a été jeté dans le feu mais Allah l'a rendu frais et paisible",
         "tr": "Putları tek başına kırdı ve tek Allah'a ibadete çağırdı. Ateşe atıldı ama Allah ateşi serin ve selamet kıldı",
         "ru": "Он один разбил идолов и призвал к поклонению Единому Богу. Был брошен в огонь, но Аллах сделал его прохладным и мирным",
     },
     "lesson": {"ar": "الشجاعة في الحق", "en": "Courage for truth", "de": "Mut für die Wahrheit", "fr": "Le courage pour la vérité", "tr": "Hak için cesaret", "ru": "Мужество ради истины"},
     "quran_ref": "الأنبياء 51-70"},
    {"id": "yusuf", "number": 4, "emoji": "⭐",
     "name": {"ar": "يوسف", "en": "Yusuf (Joseph)", "de": "Yusuf (Josef)", "fr": "Youssouf (Joseph)", "tr": "Yusuf", "ru": "Юсуф (Иосиф)", "sv": "Yusuf (Josef)", "nl": "Yusuf (Jozef)", "el": "Γιουσούφ (Ιωσήφ)"},
     "title": {"ar": "الصديق", "en": "The Truthful", "de": "Der Wahrhaftige", "fr": "Le Véridique", "tr": "Sıddık", "ru": "Правдивый", "sv": "Den Sanningsenlige", "nl": "De Waarachtige", "el": "Ο Αληθινός"},
     "summary": {
         "ar": "رأى في المنام أحد عشر كوكباً تسجد له. ألقاه إخوته في البئر فأنقذه الله. صبر في السجن ثم أصبح عزيز مصر",
         "en": "He dreamt of eleven stars bowing to him. His brothers threw him in a well but Allah saved him. He was patient in prison then became the minister of Egypt",
         "de": "Er träumte von elf Sternen, die sich vor ihm verneigten. Seine Brüder warfen ihn in einen Brunnen, aber Allah rettete ihn",
         "fr": "Il a rêvé de onze étoiles se prosternant devant lui. Ses frères l'ont jeté dans un puits mais Allah l'a sauvé",
         "tr": "Rüyasında on bir yıldızın ona secde ettiğini gördü. Kardeşleri onu kuyuya attı ama Allah onu kurtardı",
         "ru": "Ему приснились одиннадцать звёзд, поклонившихся ему. Братья бросили его в колодец, но Аллах спас его",
     },
     "lesson": {"ar": "الصبر على البلاء", "en": "Patience through trials", "de": "Geduld in Prüfungen", "fr": "La patience à travers les épreuves", "tr": "Sınavlarda sabır", "ru": "Терпение в испытаниях"},
     "quran_ref": "يوسف 1-111"},
    {"id": "musa", "number": 5, "emoji": "🌊",
     "name": {"ar": "موسى", "en": "Musa (Moses)", "de": "Musa (Moses)", "fr": "Moussa (Moïse)", "tr": "Musa", "ru": "Муса (Моисей)", "sv": "Musa (Moses)", "nl": "Musa (Mozes)", "el": "Μούσα (Μωυσής)"},
     "title": {"ar": "كليم الله", "en": "One Who Spoke to Allah", "de": "Einer der zu Allah sprach", "fr": "Celui qui a parlé à Allah", "tr": "Allah'ın Kelimi", "ru": "Собеседник Аллаха", "sv": "Den som talade med Gud", "nl": "Degene die met Allah sprak", "el": "Αυτός που μίλησε στον Θεό"},
     "summary": {
         "ar": "وُلد في زمن فرعون الظالم. وضعته أمه في النهر فأنقذه الله. كلّمه الله وأعطاه تسع آيات. شقّ البحر ونجا بقومه",
         "en": "Born during the time of the tyrant Pharaoh. His mother placed him in the river and Allah saved him. Allah spoke to him and gave him nine signs. He split the sea and saved his people",
         "de": "Geboren zur Zeit des Tyrannen Pharao. Seine Mutter legte ihn in den Fluss und Allah rettete ihn",
         "fr": "Né au temps du tyran Pharaon. Sa mère l'a mis dans le fleuve et Allah l'a sauvé",
         "tr": "Zalim Firavun döneminde doğdu. Annesi onu nehre bıraktı ve Allah onu kurtardı",
         "ru": "Родился во времена тирана Фараона. Мать опустила его в реку, и Аллах спас его",
     },
     "lesson": {"ar": "التوكل على الله", "en": "Trust in Allah", "de": "Vertrauen in Allah", "fr": "Confiance en Allah", "tr": "Allah'a tevekkül", "ru": "Упование на Аллаха"},
     "quran_ref": "القصص 1-43"},
    {"id": "muhammad", "number": 6, "emoji": "🕌",
     "name": {"ar": "محمد ﷺ", "en": "Muhammad ﷺ", "de": "Muhammad ﷺ", "fr": "Muhammad ﷺ", "tr": "Muhammed ﷺ", "ru": "Мухаммад ﷺ", "sv": "Muhammad ﷺ", "nl": "Muhammad ﷺ", "el": "Μουχάμαντ ﷺ"},
     "title": {"ar": "خاتم الأنبياء", "en": "Seal of the Prophets", "de": "Siegel der Propheten", "fr": "Sceau des Prophètes", "tr": "Peygamberlerin Sonuncusu", "ru": "Печать пророков", "sv": "Profeternas insegel", "nl": "Zegel der Profeten", "el": "Σφραγίδα των Προφητών"},
     "summary": {
         "ar": "وُلد في مكة يتيماً وكان أميناً صادقاً. نزل عليه القرآن وهو في غار حراء. دعا الناس إلى الإسلام وهاجر إلى المدينة. هو قدوتنا وحبيبنا ﷺ",
         "en": "Born an orphan in Makkah, he was trustworthy and truthful. The Quran was revealed to him in the Cave of Hira. He called people to Islam and migrated to Madinah. He is our role model ﷺ",
         "de": "Als Waise in Mekka geboren, war er vertrauenswürdig und wahrhaftig. Der Quran wurde ihm in der Höhle von Hira offenbart",
         "fr": "Né orphelin à La Mecque, il était digne de confiance et véridique. Le Coran lui a été révélé dans la grotte de Hira",
         "tr": "Mekke'de yetim olarak doğdu, güvenilir ve doğru sözlüydü. Kur'an ona Hira mağarasında indirildi",
         "ru": "Родился сиротой в Мекке, был надёжным и правдивым. Коран был ниспослан ему в пещере Хира",
     },
     "lesson": {"ar": "حسن الخلق والرحمة", "en": "Good character and mercy", "de": "Guter Charakter und Barmherzigkeit", "fr": "Bon caractère et miséricorde", "tr": "Güzel ahlak ve merhamet", "ru": "Благой нрав и милосердие"},
     "quran_ref": "الأحزاب 21"},
]

# ═══════════════════════════════════════════════════════════════
# ISLAMIC KNOWLEDGE FOR KIDS (Pillars, Values, Morals)
# ═══════════════════════════════════════════════════════════════

ISLAMIC_PILLARS = [
    {"id": "shahada", "number": 1, "emoji": "☝️",
     "title": {"ar": "الشهادة", "en": "Shahada", "de": "Shahada", "fr": "Shahada", "tr": "Şehadet", "ru": "Шахада"},
     "desc": {"ar": "أشهد أن لا إله إلا الله وأن محمداً رسول الله", "en": "Testifying there is no god but Allah and Muhammad is His messenger", "de": "Bezeugen, dass es keinen Gott außer Allah gibt und Muhammad Sein Gesandter ist", "fr": "Témoigner qu'il n'y a de dieu qu'Allah et que Muhammad est Son messager", "tr": "Allah'tan başka ilah olmadığına ve Muhammed'in O'nun elçisi olduğuna şehadet etmek", "ru": "Свидетельство, что нет бога кроме Аллаха и Мухаммад — Его посланник"}},
    {"id": "salah", "number": 2, "emoji": "🕌",
     "title": {"ar": "الصلاة", "en": "Salah (Prayer)", "de": "Salah (Gebet)", "fr": "Salat (Prière)", "tr": "Namaz", "ru": "Салят (Молитва)"},
     "desc": {"ar": "خمس صلوات في اليوم: الفجر، الظهر، العصر، المغرب، العشاء", "en": "Five daily prayers: Fajr, Dhuhr, Asr, Maghrib, Isha", "de": "Fünf tägliche Gebete: Fajr, Dhuhr, Asr, Maghrib, Isha", "fr": "Cinq prières quotidiennes: Fajr, Dhouhr, Asr, Maghrib, Isha", "tr": "Beş vakit namaz: Sabah, Öğle, İkindi, Akşam, Yatsı", "ru": "Пять ежедневных молитв: Фаджр, Зухр, Аср, Магриб, Иша"}},
    {"id": "zakat", "number": 3, "emoji": "💰",
     "title": {"ar": "الزكاة", "en": "Zakat (Charity)", "de": "Zakat (Almosen)", "fr": "Zakat (Aumône)", "tr": "Zekat", "ru": "Закят (Милостыня)"},
     "desc": {"ar": "إعطاء جزء من المال للفقراء والمحتاجين", "en": "Giving a portion of wealth to the poor and needy", "de": "Einen Teil des Vermögens den Armen und Bedürftigen geben", "fr": "Donner une partie de ses richesses aux pauvres et nécessiteux", "tr": "Malın bir kısmını fakir ve muhtaçlara vermek", "ru": "Отдавать часть имущества бедным и нуждающимся"}},
    {"id": "sawm", "number": 4, "emoji": "🌙",
     "title": {"ar": "الصوم", "en": "Sawm (Fasting)", "de": "Sawm (Fasten)", "fr": "Sawm (Jeûne)", "tr": "Oruç", "ru": "Саум (Пост)"},
     "desc": {"ar": "الصيام في شهر رمضان من الفجر إلى المغرب", "en": "Fasting in Ramadan from dawn to sunset", "de": "Fasten im Ramadan von der Morgendämmerung bis zum Sonnenuntergang", "fr": "Jeûner pendant le Ramadan de l'aube au coucher du soleil", "tr": "Ramazan ayında fecirden akşama kadar oruç tutmak", "ru": "Пост в Рамадан от рассвета до заката"}},
    {"id": "hajj", "number": 5, "emoji": "🕋",
     "title": {"ar": "الحج", "en": "Hajj (Pilgrimage)", "de": "Hajj (Pilgerfahrt)", "fr": "Hajj (Pèlerinage)", "tr": "Hac", "ru": "Хадж (Паломничество)"},
     "desc": {"ar": "زيارة بيت الله الحرام في مكة مرة في العمر لمن استطاع", "en": "Visiting the Holy House in Makkah once in a lifetime for those who can", "de": "Besuch des Heiligen Hauses in Mekka einmal im Leben für jene, die können", "fr": "Visiter la Maison Sacrée à La Mecque une fois dans sa vie pour ceux qui le peuvent", "tr": "Gücü yeten için ömürde bir kez Mekke'deki Kutsal Evi ziyaret etmek", "ru": "Посещение Священного Дома в Мекке раз в жизни для тех, кто может"}},
]

# ═══════════════════════════════════════════════════════════════
# CHILDREN'S LEARNING LIBRARY (Comprehensive Multilingual)
# ═══════════════════════════════════════════════════════════════

KIDS_LIBRARY_CATEGORIES = [
    {"id": "quran_stories", "emoji": "📖", "color": "#10B981",
     "title": {"ar": "قصص القرآن", "en": "Quran Stories", "de": "Koran-Geschichten", "fr": "Histoires du Coran", "tr": "Kur'an Kıssaları", "ru": "Истории Корана", "sv": "Koranens berättelser", "nl": "Koraan Verhalen", "el": "Ιστορίες του Κορανίου"},
     "count": 20},
    {"id": "prophet_stories", "emoji": "🕌", "color": "#3B82F6",
     "title": {"ar": "قصص الأنبياء", "en": "Prophet Stories", "de": "Prophetengeschichten", "fr": "Histoires des Prophètes", "tr": "Peygamber Kıssaları", "ru": "Истории пророков", "sv": "Profetberättelser", "nl": "Profetensverhalen", "el": "Ιστορίες Προφητών"},
     "count": 25},
    {"id": "moral_stories", "emoji": "⭐", "color": "#F59E0B",
     "title": {"ar": "قصص أخلاقية", "en": "Moral Stories", "de": "Moralische Geschichten", "fr": "Histoires morales", "tr": "Ahlaki Hikayeler", "ru": "Нравственные истории", "sv": "Moraliska berättelser", "nl": "Morele Verhalen", "el": "Ηθικές Ιστορίες"},
     "count": 30},
    {"id": "science", "emoji": "🔬", "color": "#8B5CF6",
     "title": {"ar": "العلوم المرحة", "en": "Fun Science", "de": "Spaß mit Wissenschaft", "fr": "Sciences amusantes", "tr": "Eğlenceli Bilim", "ru": "Весёлая наука", "sv": "Rolig vetenskap", "nl": "Leuke Wetenschap", "el": "Διασκεδαστική Επιστήμη"},
     "count": 20},
    {"id": "arabic_language", "emoji": "🔤", "color": "#EF4444",
     "title": {"ar": "اللغة العربية", "en": "Arabic Language", "de": "Arabische Sprache", "fr": "Langue Arabe", "tr": "Arapça", "ru": "Арабский язык", "sv": "Arabiska", "nl": "Arabische Taal", "el": "Αραβική Γλώσσα"},
     "count": 50},
    {"id": "math", "emoji": "🔢", "color": "#06B6D4",
     "title": {"ar": "الرياضيات", "en": "Mathematics", "de": "Mathematik", "fr": "Mathématiques", "tr": "Matematik", "ru": "Математика", "sv": "Matematik", "nl": "Wiskunde", "el": "Μαθηματικά"},
     "count": 30},
    {"id": "islamic_manners", "emoji": "🤲", "color": "#059669",
     "title": {"ar": "الآداب الإسلامية", "en": "Islamic Manners", "de": "Islamische Umgangsformen", "fr": "Bonnes manières islamiques", "tr": "İslami Adab", "ru": "Исламские манеры", "sv": "Islamiska seder", "nl": "Islamitische Manieren", "el": "Ισλαμικοί τρόποι"},
     "count": 20},
    {"id": "nature", "emoji": "🌿", "color": "#84CC16",
     "title": {"ar": "الطبيعة والبيئة", "en": "Nature & Environment", "de": "Natur & Umwelt", "fr": "Nature & Environnement", "tr": "Doğa ve Çevre", "ru": "Природа и окружающая среда", "sv": "Natur & Miljö", "nl": "Natuur & Milieu", "el": "Φύση & Περιβάλλον"},
     "count": 15},
]

KIDS_LIBRARY_ITEMS = [
    # Quran Stories
    {"id": "qs_elephant", "category": "quran_stories", "emoji": "🐘", "difficulty": 1, "age_range": "3-7",
     "title": {"ar": "قصة أصحاب الفيل", "en": "The People of the Elephant", "de": "Die Leute des Elefanten", "fr": "Les gens de l'éléphant", "tr": "Fil Sahipleri", "ru": "Люди слона"},
     "content": {"ar": "جاء أبرهة بجيش كبير وفيل ضخم ليهدم الكعبة. لكن الله حمى بيته وأرسل طيوراً أبابيل ترميهم بحجارة من سجيل. فجعلهم كعصف مأكول. هذه القصة تعلمنا أن الله يحمي بيته دائماً", "en": "Abraha came with a huge army and a big elephant to destroy the Kaaba. But Allah protected His House and sent birds (Ababil) that threw stones at them. This story teaches us that Allah always protects His House", "de": "Abraha kam mit einer großen Armee und einem riesigen Elefanten, um die Kaaba zu zerstören. Aber Allah schützte Sein Haus", "fr": "Abraha est venu avec une grande armée et un énorme éléphant pour détruire la Kaaba. Mais Allah a protégé Sa Maison", "tr": "Ebrehe, Kabe'yi yıkmak için büyük bir ordu ve devasa bir fille geldi. Ama Allah evini korudu", "ru": "Абраха пришёл с огромной армией и большим слоном, чтобы разрушить Каабу. Но Аллах защитил Свой Дом"},
     "quran_ref": "سورة الفيل"},
    {"id": "qs_cave", "category": "quran_stories", "emoji": "🕳️", "difficulty": 1, "age_range": "5-10",
     "title": {"ar": "أصحاب الكهف", "en": "The People of the Cave", "de": "Die Leute der Höhle", "fr": "Les gens de la caverne", "tr": "Ashab-ı Kehf", "ru": "Обитатели пещеры"},
     "content": {"ar": "شباب آمنوا بالله فهربوا من الملك الظالم واختبأوا في كهف. أنامهم الله 309 سنوات ثم أيقظهم. هذه القصة تعلمنا أن الله يحمي من يؤمن به", "en": "Young believers fled from a tyrant king and hid in a cave. Allah made them sleep for 309 years then woke them. This teaches us that Allah protects those who believe in Him", "de": "Junge Gläubige flohen vor einem tyrannischen König und versteckten sich in einer Höhle. Allah ließ sie 309 Jahre schlafen", "fr": "De jeunes croyants ont fui un roi tyran et se sont cachés dans une caverne. Allah les a fait dormir 309 ans", "tr": "Genç müminler zalim kraldan kaçıp bir mağaraya sığındılar. Allah onları 309 yıl uyuttu", "ru": "Молодые верующие бежали от тирана и спрятались в пещере. Аллах усыпил их на 309 лет"},
     "quran_ref": "سورة الكهف"},
    # Moral Stories
    {"id": "ms_ant", "category": "moral_stories", "emoji": "🐜", "difficulty": 1, "age_range": "3-7",
     "title": {"ar": "النملة المجتهدة", "en": "The Hardworking Ant", "de": "Die fleißige Ameise", "fr": "La fourmi travailleuse", "tr": "Çalışkan Karınca", "ru": "Трудолюбивый муравей"},
     "content": {"ar": "نملة صغيرة عملت طوال الصيف لتخزن الطعام للشتاء. النملة تعلمنا أن العمل الجاد والتخطيط المبكر يحمينا من الصعوبات", "en": "A tiny ant worked all summer to store food for winter. The ant teaches us that hard work and early planning protect us from difficulties", "de": "Eine kleine Ameise arbeitete den ganzen Sommer, um Essen für den Winter zu lagern", "fr": "Une petite fourmi a travaillé tout l'été pour stocker de la nourriture pour l'hiver", "tr": "Küçük bir karınca, kış için yiyecek depolamak üzere bütün yaz çalıştı", "ru": "Маленький муравей работал всё лето, чтобы запасти еду на зиму"},
     "lesson": {"ar": "الاجتهاد والعمل", "en": "Hard work and diligence", "de": "Fleiß und Arbeit", "fr": "Travail et diligence", "tr": "Çalışkanlık", "ru": "Трудолюбие"}},
    {"id": "ms_honesty", "category": "moral_stories", "emoji": "✨", "difficulty": 1, "age_range": "4-8",
     "title": {"ar": "الصدق ينجي", "en": "Honesty Saves", "de": "Ehrlichkeit rettet", "fr": "L'honnêteté sauve", "tr": "Dürüstlük Kurtarır", "ru": "Честность спасает"},
     "content": {"ar": "كان هناك ولد اسمه أحمد. كسر المزهرية في البيت وخاف. لكنه تذكر أن الرسول ﷺ أمرنا بالصدق. فاعترف لأمه التي سامحته وفرحت بصدقه", "en": "A boy named Ahmad broke a vase at home and was scared. But he remembered the Prophet ﷺ told us to be truthful. He told his mother who forgave him and was happy with his honesty", "de": "Ein Junge namens Ahmad zerbrach eine Vase und hatte Angst. Er erinnerte sich an den Propheten und sagte die Wahrheit", "fr": "Un garçon nommé Ahmad a cassé un vase et avait peur. Il s'est souvenu du Prophète et a dit la vérité", "tr": "Ahmed adında bir çocuk vazoyu kırdı ve korktu. Peygamber'in doğruluk emrini hatırladı ve annesine söyledi", "ru": "Мальчик по имени Ахмад разбил вазу и испугался. Он вспомнил, что Пророк велел быть правдивым"},
     "lesson": {"ar": "قل الصدق دائماً", "en": "Always tell the truth", "de": "Sage immer die Wahrheit", "fr": "Dis toujours la vérité", "tr": "Her zaman doğruyu söyle", "ru": "Всегда говори правду"}},
    # Science
    {"id": "sc_water", "category": "science", "emoji": "💧", "difficulty": 1, "age_range": "4-8",
     "title": {"ar": "دورة الماء", "en": "The Water Cycle", "de": "Der Wasserkreislauf", "fr": "Le cycle de l'eau", "tr": "Su Döngüsü", "ru": "Круговорот воды"},
     "content": {"ar": "الماء ينزل من السماء مطراً فيملأ الأنهار والبحار. ثم تسخنه الشمس فيتبخر ويصعد للسماء ويصبح غيوماً. قال الله تعالى: وأنزلنا من السماء ماءً طهوراً", "en": "Water falls from the sky as rain filling rivers and seas. Then the sun heats it, it evaporates and rises to become clouds. Allah says: And We sent down from the sky pure water", "de": "Wasser fällt als Regen vom Himmel und füllt Flüsse und Meere. Die Sonne erwärmt es und es verdampft", "fr": "L'eau tombe du ciel sous forme de pluie et remplit les rivières et les mers", "tr": "Su gökyüzünden yağmur olarak düşer, nehirleri ve denizleri doldurur", "ru": "Вода падает с неба дождём, наполняя реки и моря"},
     "quran_ref": "الفرقان 48"},
    # Islamic Manners
    {"id": "im_salam", "category": "islamic_manners", "emoji": "👋", "difficulty": 1, "age_range": "3-7",
     "title": {"ar": "إلقاء السلام", "en": "Giving Salam", "de": "Salam geben", "fr": "Donner le Salam", "tr": "Selam Vermek", "ru": "Приветствие Салам"},
     "content": {"ar": "عندما نلتقي بأحد نقول: السلام عليكم ورحمة الله وبركاته. ويرد: وعليكم السلام ورحمة الله وبركاته. السلام ينشر المحبة بين الناس", "en": "When we meet someone we say: Assalamu Alaikum wa Rahmatullahi wa Barakatuh. They reply: Wa Alaikum Assalam wa Rahmatullahi wa Barakatuh. Salam spreads love among people", "de": "Wenn wir jemanden treffen, sagen wir: Assalamu Alaikum wa Rahmatullahi wa Barakatuh", "fr": "Quand nous rencontrons quelqu'un, nous disons: Assalamou Aleykoum wa Rahmatullahi wa Barakatouh", "tr": "Birisiyle karşılaştığımızda: Esselamu aleyküm ve rahmetullahi ve berekatüh deriz", "ru": "Когда мы встречаем кого-то, мы говорим: Ассаламу алейкум ва рахматуллахи ва баракатух"},
     "lesson": {"ar": "ألقِ السلام على الجميع", "en": "Greet everyone with Salam", "de": "Grüße alle mit Salam", "fr": "Salue tout le monde avec Salam", "tr": "Herkese selam ver", "ru": "Приветствуй всех салямом"}},
]

# ═══════════════════════════════════════════════════════════════
# DAILY COMPREHENSIVE LESSONS (School-like structure)
# ═══════════════════════════════════════════════════════════════

def build_daily_lesson(day_number: int, locale: str = "ar") -> dict:
    """Build a comprehensive daily lesson for kids - like a school day."""
    
    # Cycle through content based on day number
    surah_idx = (day_number - 1) % len(QURAN_SURAHS_FOR_KIDS)
    dua_idx = (day_number - 1) % len(KIDS_DUAS)
    hadith_idx = (day_number - 1) % len(KIDS_HADITHS)
    story_idx = (day_number - 1) % len(PROPHET_STORIES)
    pillar_idx = (day_number - 1) % len(ISLAMIC_PILLARS)
    library_idx = (day_number - 1) % len(KIDS_LIBRARY_ITEMS)
    
    surah = QURAN_SURAHS_FOR_KIDS[surah_idx]
    dua = KIDS_DUAS[dua_idx]
    hadith = KIDS_HADITHS[hadith_idx]
    prophet = PROPHET_STORIES[story_idx]
    pillar = ISLAMIC_PILLARS[pillar_idx]
    library_item = KIDS_LIBRARY_ITEMS[library_idx]
    
    # Pick specific ayah for memorization (cycle through ayahs)
    total_ayahs = len(surah["ayahs"])
    ayah_idx = (day_number - 1) % total_ayahs
    today_ayah = surah["ayahs"][ayah_idx]
    
    lang = locale if locale in ["ar", "en", "de", "fr", "tr", "ru", "sv", "nl", "el"] else "en"
    
    lesson = {
        "day": day_number,
        "date": str(date.today()),
        "greeting": _get_greeting(lang),
        
        # Section 1: Quran Memorization
        "quran": {
            "section_title": _ml("حفظ القرآن", "Quran Memorization", lang),
            "section_emoji": "📖",
            "surah_name": surah[f"name_{lang}"] if f"name_{lang}" in surah else surah["name_en"],
            "surah_number": surah["number"],
            "ayah": {
                "number": today_ayah["num"],
                "arabic": today_ayah["ar"],
                "translation": today_ayah.get(lang, today_ayah["en"]),
                "transliteration": "",  # Can be added
            },
            "full_surah_ayahs": len(surah["ayahs"]),
            "tip": _ml("اقرأ الآية 3 مرات ثم أغلق عينيك وحاول تسميعها", "Read the ayah 3 times then close your eyes and try to recite it", lang),
        },
        
        # Section 2: Daily Dua
        "dua": {
            "section_title": _ml("دعاء اليوم", "Today's Dua", lang),
            "section_emoji": dua["emoji"],
            "title": dua["title"].get(lang, dua["title"]["en"]),
            "arabic": dua["ar"],
            "transliteration": dua["transliteration"],
            "meaning": dua.get(lang, dua["en"]) if lang != "ar" else "",
        },
        
        # Section 3: Hadith of the Day
        "hadith": {
            "section_title": _ml("حديث اليوم", "Today's Hadith", lang),
            "section_emoji": hadith["emoji"],
            "arabic": hadith["ar"],
            "translation": hadith.get(lang, hadith["en"]),
            "source": hadith["source"],
            "lesson": hadith["lesson"].get(lang, hadith["lesson"]["en"]),
        },
        
        # Section 4: Prophet Story
        "story": {
            "section_title": _ml("قصة نبي", "Prophet Story", lang),
            "section_emoji": prophet["emoji"],
            "prophet_name": prophet["name"].get(lang, prophet["name"]["en"]),
            "title": prophet["title"].get(lang, prophet["title"]["en"]),
            "summary": prophet["summary"].get(lang, prophet["summary"]["en"]),
            "lesson": prophet["lesson"].get(lang, prophet["lesson"]["en"]),
            "quran_ref": prophet["quran_ref"],
        },
        
        # Section 5: Islamic Knowledge
        "islamic_knowledge": {
            "section_title": _ml("معلومة إسلامية", "Islamic Knowledge", lang),
            "section_emoji": pillar["emoji"],
            "topic": pillar["title"].get(lang, pillar["title"]["en"]),
            "description": pillar["desc"].get(lang, pillar["desc"]["en"]),
        },
        
        # Section 6: Library Pick of the Day
        "library_pick": {
            "section_title": _ml("من المكتبة", "From the Library", lang),
            "section_emoji": library_item["emoji"],
            "title": library_item["title"].get(lang, library_item["title"]["en"]),
            "content": library_item["content"].get(lang, library_item["content"]["en"]),
            "category": library_item["category"],
            "age_range": library_item.get("age_range", "3-10"),
        },
        
        # Section 7: Activity / Exercise
        "activity": _build_daily_activity(day_number, lang),
    }
    
    return lesson


def _ml(ar: str, en: str, lang: str) -> str:
    """Simple multilingual helper."""
    if lang == "ar":
        return ar
    translations = {
        "de": {"حفظ القرآن": "Koran-Memorierung", "دعاء اليوم": "Heutiges Dua", "حديث اليوم": "Heutiger Hadith", "قصة نبي": "Prophetengeschichte", "معلومة إسلامية": "Islamisches Wissen", "من المكتبة": "Aus der Bibliothek"},
        "fr": {"حفظ القرآن": "Mémorisation du Coran", "دعاء اليوم": "Dua du jour", "حديث اليوم": "Hadith du jour", "قصة نبي": "Histoire d'un prophète", "معلومة إسلامية": "Savoir islamique", "من المكتبة": "De la bibliothèque"},
        "tr": {"حفظ القرآن": "Kur'an Ezberleme", "دعاء اليوم": "Günün Duası", "حديث اليوم": "Günün Hadisi", "قصة نبي": "Peygamber Kıssası", "معلومة إسلامية": "İslami Bilgi", "من المكتبة": "Kütüphaneden"},
        "ru": {"حفظ القرآن": "Заучивание Корана", "دعاء اليوم": "Дуа дня", "حديث اليوم": "Хадис дня", "قصة نبي": "История пророка", "معلومة إسلامية": "Исламские знания", "من المكتبة": "Из библиотеки"},
        "sv": {"حفظ القرآن": "Koran-memorering", "دعاء اليوم": "Dagens Dua", "حديث اليوم": "Dagens Hadith", "قصة نبي": "Profetberättelse", "معلومة إسلامية": "Islamisk kunskap", "من المكتبة": "Från biblioteket"},
        "nl": {"حفظ القرآن": "Koran Memorisatie", "دعاء اليوم": "Dua van vandaag", "حديث اليوم": "Hadith van vandaag", "قصة نبي": "Profetensverhaal", "معلومة إسلامية": "Islamitische kennis", "من المكتبة": "Uit de bibliotheek"},
        "el": {"حفظ القرآن": "Απομνημόνευση Κορανίου", "دعاء اليوم": "Ντουά της ημέρας", "حديث اليوم": "Χαντίθ της ημέρας", "قصة نبي": "Ιστορία Προφήτη", "معلومة إسلامية": "Ισλαμική γνώση", "من المكتبة": "Από τη βιβλιοθήκη"},
    }
    if lang in translations and ar in translations[lang]:
        return translations[lang][ar]
    return en


def _get_greeting(lang: str) -> str:
    """Get time-appropriate greeting."""
    greetings = {
        "ar": "السلام عليكم! مرحباً بدرس اليوم 🌟",
        "en": "Assalamu Alaikum! Welcome to today's lesson 🌟",
        "de": "Assalamu Alaikum! Willkommen zur heutigen Lektion 🌟",
        "fr": "Assalamou Aleykoum ! Bienvenue au cours d'aujourd'hui 🌟",
        "tr": "Esselamu Aleyküm! Bugünkü derse hoş geldiniz 🌟",
        "ru": "Ассаляму алейкум! Добро пожаловать на сегодняшний урок 🌟",
        "sv": "Assalamu Alaikum! Välkommen till dagens lektion 🌟",
        "nl": "Assalamu Alaikum! Welkom bij de les van vandaag 🌟",
        "el": "Ασσαλάμου Αλέικουμ! Καλώς ήρθατε στο σημερινό μάθημα 🌟",
    }
    return greetings.get(lang, greetings["en"])


def _build_daily_activity(day: int, lang: str) -> dict:
    """Build a daily activity/exercise."""
    activities = [
        {"type": "memorize", "emoji": "🧠",
         "title": {"ar": "تحدي الحفظ", "en": "Memory Challenge", "de": "Gedächtnis-Challenge", "fr": "Défi mémoire", "tr": "Hafıza Yarışması", "ru": "Испытание памяти"},
         "desc": {"ar": "احفظ الآية التي تعلمتها اليوم وسمّعها لوالديك", "en": "Memorize today's ayah and recite it to your parents", "de": "Lerne den heutigen Vers auswendig und trage ihn deinen Eltern vor", "fr": "Mémorise le verset d'aujourd'hui et récite-le à tes parents", "tr": "Bugünkü ayeti ezberle ve ailene oku", "ru": "Выучи сегодняшний аят и прочитай его родителям"}},
        {"type": "draw", "emoji": "🎨",
         "title": {"ar": "ارسم وتعلم", "en": "Draw & Learn", "de": "Malen & Lernen", "fr": "Dessine & Apprends", "tr": "Çiz & Öğren", "ru": "Рисуй и учись"},
         "desc": {"ar": "ارسم صورة عن قصة النبي التي قرأتها اليوم", "en": "Draw a picture about today's prophet story", "de": "Male ein Bild zur heutigen Prophetengeschichte", "fr": "Dessine une image de l'histoire du prophète d'aujourd'hui", "tr": "Bugünkü peygamber hikayesi hakkında bir resim çiz", "ru": "Нарисуй картинку об истории пророка"}},
        {"type": "practice", "emoji": "✍️",
         "title": {"ar": "تمرين الكتابة", "en": "Writing Practice", "de": "Schreibübung", "fr": "Exercice d'écriture", "tr": "Yazı Alıştırması", "ru": "Практика письма"},
         "desc": {"ar": "اكتب الدعاء الذي تعلمته 3 مرات", "en": "Write today's dua 3 times", "de": "Schreibe das heutige Dua 3 mal", "fr": "Écris le dua d'aujourd'hui 3 fois", "tr": "Bugünkü duayı 3 kere yaz", "ru": "Напиши сегодняшнее дуа 3 раза"}},
        {"type": "quiz", "emoji": "❓",
         "title": {"ar": "اختبر نفسك", "en": "Test Yourself", "de": "Teste dich", "fr": "Teste-toi", "tr": "Kendini Test Et", "ru": "Проверь себя"},
         "desc": {"ar": "أجب على أسئلة عن درس اليوم", "en": "Answer questions about today's lesson", "de": "Beantworte Fragen zur heutigen Lektion", "fr": "Réponds aux questions sur la leçon d'aujourd'hui", "tr": "Bugünkü ders hakkındaki soruları cevapla", "ru": "Ответь на вопросы о сегодняшнем уроке"}},
        {"type": "share", "emoji": "🗣️",
         "title": {"ar": "شارك ما تعلمته", "en": "Share What You Learned", "de": "Teile was du gelernt hast", "fr": "Partage ce que tu as appris", "tr": "Öğrendiklerini Paylaş", "ru": "Поделись тем, что узнал"},
         "desc": {"ar": "أخبر عائلتك بالحديث الذي تعلمته اليوم", "en": "Tell your family about today's hadith", "de": "Erzähle deiner Familie vom heutigen Hadith", "fr": "Raconte à ta famille le hadith d'aujourd'hui", "tr": "Ailene bugünkü hadisi anlat", "ru": "Расскажи семье о сегодняшнем хадисе"}},
    ]
    
    activity = activities[(day - 1) % len(activities)]
    return {
        "type": activity["type"],
        "emoji": activity["emoji"],
        "title": activity["title"].get(lang, activity["title"]["en"]),
        "description": activity["desc"].get(lang, activity["desc"]["en"]),
    }


def get_quran_memorization_plan(locale: str = "ar") -> list:
    """Get the full Quran memorization plan for kids."""
    lang = locale if locale in ["ar", "en", "de", "fr", "tr", "ru", "sv", "nl", "el"] else "en"
    plan = []
    for surah in QURAN_SURAHS_FOR_KIDS:
        plan.append({
            "id": surah["id"],
            "number": surah["number"],
            "name_ar": surah["name_ar"],
            "name_en": surah["name_en"],
            "difficulty": surah["difficulty"],
            "total_ayahs": surah["total_ayahs"],
            "ayahs": [{
                "number": a["num"],
                "arabic": a["ar"],
                "translation": a.get(lang, a["en"]),
            } for a in surah["ayahs"]],
        })
    return plan


def get_all_duas(locale: str = "ar") -> list:
    """Get all kids duas with translations."""
    lang = locale if locale in ["ar", "en", "de", "fr", "tr", "ru", "sv", "nl", "el"] else "en"
    result = []
    for dua in KIDS_DUAS:
        result.append({
            "id": dua["id"],
            "category": dua["category"],
            "emoji": dua["emoji"],
            "title": dua["title"].get(lang, dua["title"]["en"]),
            "arabic": dua["ar"],
            "transliteration": dua["transliteration"],
            "meaning": dua.get(lang, dua["en"]) if lang != "ar" else "",
        })
    return result


def get_all_hadiths(locale: str = "ar") -> list:
    """Get all kids hadiths with translations."""
    lang = locale if locale in ["ar", "en", "de", "fr", "tr", "ru", "sv", "nl", "el"] else "en"
    result = []
    for h in KIDS_HADITHS:
        result.append({
            "id": h["id"],
            "category": h["category"],
            "emoji": h["emoji"],
            "arabic": h["ar"],
            "translation": h.get(lang, h["en"]),
            "source": h["source"],
            "narrator": h["narrator"],
            "lesson": h["lesson"].get(lang, h["lesson"]["en"]),
        })
    return result


def get_prophet_stories(locale: str = "ar") -> list:
    """Get all prophet stories with translations."""
    lang = locale if locale in ["ar", "en", "de", "fr", "tr", "ru", "sv", "nl", "el"] else "en"
    result = []
    for p in PROPHET_STORIES:
        result.append({
            "id": p["id"],
            "number": p["number"],
            "emoji": p["emoji"],
            "name": p["name"].get(lang, p["name"]["en"]),
            "title": p["title"].get(lang, p["title"]["en"]),
            "summary": p["summary"].get(lang, p["summary"]["en"]),
            "lesson": p["lesson"].get(lang, p["lesson"]["en"]),
            "quran_ref": p["quran_ref"],
        })
    return result


def get_islamic_pillars(locale: str = "ar") -> list:
    """Get 5 pillars of Islam with translations."""
    lang = locale if locale in ["ar", "en", "de", "fr", "tr", "ru", "sv", "nl", "el"] else "en"
    result = []
    for p in ISLAMIC_PILLARS:
        result.append({
            "id": p["id"],
            "number": p["number"],
            "emoji": p["emoji"],
            "title": p["title"].get(lang, p["title"]["en"]),
            "description": p["desc"].get(lang, p["desc"]["en"]),
        })
    return result


def get_library_categories(locale: str = "ar") -> list:
    """Get library categories with accurate counts."""
    from kids_library_content import EXPANDED_LIBRARY_ITEMS
    lang = locale if locale in ["ar", "en", "de", "fr", "tr", "ru", "sv", "nl", "el"] else "en"
    # Merge items, expanded takes priority (has better translations)
    seen_ids = set()
    all_items = []
    for item in EXPANDED_LIBRARY_ITEMS:
        if item["id"] not in seen_ids:
            all_items.append(item)
            seen_ids.add(item["id"])
    for item in KIDS_LIBRARY_ITEMS:
        if item["id"] not in seen_ids:
            all_items.append(item)
            seen_ids.add(item["id"])
    result = []
    for c in KIDS_LIBRARY_CATEGORIES:
        real_count = len([i for i in all_items if i["category"] == c["id"]])
        result.append({
            "id": c["id"],
            "emoji": c["emoji"],
            "color": c["color"],
            "title": c["title"].get(lang, c["title"]["en"]),
            "count": real_count,
        })
    return result


def get_library_items(category: str = "all", locale: str = "ar") -> list:
    """Get library items, optionally filtered by category."""
    from kids_library_content import EXPANDED_LIBRARY_ITEMS
    lang = locale if locale in ["ar", "en", "de", "fr", "tr", "ru", "sv", "nl", "el"] else "en"
    # Merge items, expanded takes priority
    seen_ids = set()
    all_items = []
    for item in EXPANDED_LIBRARY_ITEMS:
        if item["id"] not in seen_ids:
            all_items.append(item)
            seen_ids.add(item["id"])
    for item in KIDS_LIBRARY_ITEMS:
        if item["id"] not in seen_ids:
            all_items.append(item)
            seen_ids.add(item["id"])
    items = all_items if category == "all" else [i for i in all_items if i["category"] == category]
    result = []
    for item in items:
        result.append({
            "id": item["id"],
            "category": item["category"],
            "emoji": item["emoji"],
            "difficulty": item.get("difficulty", 1),
            "age_range": item.get("age_range", "3-10"),
            "title": item["title"].get(lang, item["title"]["en"]),
            "content": item["content"].get(lang, item["content"]["en"]),
            "lesson": item.get("lesson", {}).get(lang, item.get("lesson", {}).get("en", "")) if "lesson" in item else "",
            "quran_ref": item.get("quran_ref", ""),
        })
    return result

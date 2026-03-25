"""
Multilingual Content Data
=========================
Translated store items, gifts, packages, categories, and error messages.
All 10 locales: ar, en, de, de-AT, fr, tr, ru, sv, nl, el
"""

SUPPORTED_LOCALES = ["ar", "en", "de", "de-AT", "fr", "tr", "ru", "sv", "nl", "el"]


def _t(translations: dict, locale: str) -> str:
    """Get translation for locale with fallback chain: locale -> base_lang -> ar"""
    lang = locale
    if lang == "de-AT":
        lang = "de"
    return translations.get(lang, translations.get("ar", ""))


# ==================== STORE ITEMS ====================
STORE_ITEMS_TRANSLATED = [
    {
        "category": "frame", "price_gold": 50, "price_usd": 0.99, "image_url": None, "active": True,
        "name": {"ar": "إطار ذهبي", "en": "Golden Frame", "de": "Goldener Rahmen", "fr": "Cadre doré", "tr": "Altın Çerçeve", "ru": "Золотая рамка", "sv": "Gyllene ram", "nl": "Gouden kader", "el": "Χρυσό πλαίσιο"},
        "description": {"ar": "إطار ذهبي مميز لصورتك الشخصية", "en": "A premium golden frame for your profile picture", "de": "Ein hochwertiger goldener Rahmen für Ihr Profilbild", "fr": "Un cadre doré premium pour votre photo de profil", "tr": "Profil resminiz için özel altın çerçeve", "ru": "Премиальная золотая рамка для фото профиля", "sv": "En gyllene premiumram för din profilbild", "nl": "Een premium gouden kader voor je profielfoto", "el": "Ένα χρυσό πλαίσιο premium για τη φωτογραφία προφίλ σας"},
    },
    {
        "category": "theme", "price_gold": 30, "price_usd": 0.49, "image_url": None, "active": True,
        "name": {"ar": "خلفية رمضانية", "en": "Ramadan Theme", "de": "Ramadan-Thema", "fr": "Thème Ramadan", "tr": "Ramazan Teması", "ru": "Тема Рамадан", "sv": "Ramadan-tema", "nl": "Ramadan-thema", "el": "Θέμα Ραμαντάν"},
        "description": {"ar": "خلفية خاصة بشهر رمضان المبارك", "en": "A special theme for the blessed month of Ramadan", "de": "Ein besonderes Thema für den gesegneten Monat Ramadan", "fr": "Un thème spécial pour le mois béni du Ramadan", "tr": "Mübarek Ramazan ayına özel tema", "ru": "Особая тема для благословенного месяца Рамадан", "sv": "Ett speciellt tema för den välsignade månaden Ramadan", "nl": "Een speciaal thema voor de gezegende maand Ramadan", "el": "Ένα ειδικό θέμα για τον ευλογημένο μήνα Ραμαντάν"},
    },
    {
        "category": "badge", "price_gold": 100, "price_usd": 1.99, "image_url": None, "active": True,
        "name": {"ar": "شارة حافظ", "en": "Hafiz Badge", "de": "Hafiz-Abzeichen", "fr": "Badge Hafiz", "tr": "Hafız Rozeti", "ru": "Значок Хафиз", "sv": "Hafiz-märke", "nl": "Hafiz-badge", "el": "Σήμα Χαφίζ"},
        "description": {"ar": "شارة مميزة تظهر بجانب اسمك", "en": "A distinctive badge that appears next to your name", "de": "Ein besonderes Abzeichen neben Ihrem Namen", "fr": "Un badge distinctif qui apparaît à côté de votre nom", "tr": "Adınızın yanında görünen özel rozet", "ru": "Отличительный значок рядом с вашим именем", "sv": "Ett distinkt märke som visas bredvid ditt namn", "nl": "Een onderscheidend badge naast je naam", "el": "Ένα ξεχωριστό σήμα δίπλα στο όνομά σας"},
    },
    {
        "category": "effect", "price_gold": 75, "price_usd": 1.49, "image_url": None, "active": True,
        "name": {"ar": "تأثير نجوم", "en": "Stars Effect", "de": "Sterneneffekt", "fr": "Effet étoiles", "tr": "Yıldız Efekti", "ru": "Эффект звёзд", "sv": "Stjärneffekt", "nl": "Sterreneffect", "el": "Εφέ αστεριών"},
        "description": {"ar": "تأثير نجوم متحركة على منشوراتك", "en": "Animated star effects on your posts", "de": "Animierte Sterneneffekte auf Ihren Beiträgen", "fr": "Effets d'étoiles animées sur vos publications", "tr": "Gönderilerinizde hareketli yıldız efekti", "ru": "Анимированные звёздные эффекты на ваших публикациях", "sv": "Animerade stjärneffekter på dina inlägg", "nl": "Geanimeerde sterreneffecten op je berichten", "el": "Κινούμενα εφέ αστεριών στις δημοσιεύσεις σας"},
    },
    {
        "category": "membership", "price_gold": 500, "price_usd": 4.99, "image_url": None, "active": True,
        "name": {"ar": "عضوية مميزة (شهر)", "en": "Premium Membership (Month)", "de": "Premium-Mitgliedschaft (Monat)", "fr": "Abonnement Premium (Mois)", "tr": "Premium Üyelik (Ay)", "ru": "Премиум-членство (Месяц)", "sv": "Premiummedlemskap (Månad)", "nl": "Premium-lidmaatschap (Maand)", "el": "Premium Συνδρομή (Μήνας)"},
        "description": {"ar": "وصول لميزات حصرية لمدة شهر", "en": "Access to exclusive features for one month", "de": "Zugang zu exklusiven Funktionen für einen Monat", "fr": "Accès aux fonctionnalités exclusives pendant un mois", "tr": "Bir ay süreyle özel özelliklere erişim", "ru": "Доступ к эксклюзивным функциям на один месяц", "sv": "Tillgång till exklusiva funktioner i en månad", "nl": "Toegang tot exclusieve functies voor één maand", "el": "Πρόσβαση σε αποκλειστικές λειτουργίες για ένα μήνα"},
    },
    {
        "category": "charity", "price_gold": 10, "price_usd": 0, "image_url": None, "active": True,
        "name": {"ar": "صدقة جارية", "en": "Ongoing Charity", "de": "Fortlaufende Wohltätigkeit", "fr": "Charité continue", "tr": "Sadaka-i Cariye", "ru": "Непрерывная милостыня", "sv": "Pågående välgörenhet", "nl": "Doorlopende liefdadigheid", "el": "Συνεχής φιλανθρωπία"},
        "description": {"ar": "تبرع بالذهب لمشاريع خيرية", "en": "Donate gold to charitable projects", "de": "Gold für wohltätige Projekte spenden", "fr": "Faites don d'or à des projets caritatifs", "tr": "Hayır projelerine altın bağışlayın", "ru": "Пожертвуйте золото на благотворительные проекты", "sv": "Donera guld till välgörenhetsprojekt", "nl": "Doneer goud aan liefdadigheidsprojecten", "el": "Δωρίστε χρυσό σε φιλανθρωπικά έργα"},
    },
]


# ==================== STORE PACKAGES ====================
STORE_PACKAGES_TRANSLATED = {
    "frame": {"name": {"ar": "إطار ذهبي", "en": "Golden Frame", "de": "Goldener Rahmen", "fr": "Cadre doré", "tr": "Altın Çerçeve", "ru": "Золотая рамка", "sv": "Gyllene ram", "nl": "Gouden kader", "el": "Χρυσό πλαίσιο"}, "price": 0.99},
    "theme": {"name": {"ar": "خلفية رمضانية", "en": "Ramadan Theme", "de": "Ramadan-Thema", "fr": "Thème Ramadan", "tr": "Ramazan Teması", "ru": "Тема Рамадан", "sv": "Ramadan-tema", "nl": "Ramadan-thema", "el": "Θέμα Ραμαντάν"}, "price": 0.49},
    "badge": {"name": {"ar": "شارة حافظ", "en": "Hafiz Badge", "de": "Hafiz-Abzeichen", "fr": "Badge Hafiz", "tr": "Hafız Rozeti", "ru": "Значок Хафиз", "sv": "Hafiz-märke", "nl": "Hafiz-badge", "el": "Σήμα Χαφίζ"}, "price": 1.99},
    "effect": {"name": {"ar": "تأثير نجوم", "en": "Stars Effect", "de": "Sterneneffekt", "fr": "Effet étoiles", "tr": "Yıldız Efekti", "ru": "Эффект звёзд", "sv": "Stjärneffekt", "nl": "Sterreneffect", "el": "Εφέ αστεριών"}, "price": 1.49},
    "membership_monthly": {"name": {"ar": "عضوية مميزة (شهر)", "en": "Premium Membership (Month)", "de": "Premium-Mitgliedschaft (Monat)", "fr": "Abonnement Premium (Mois)", "tr": "Premium Üyelik (Ay)", "ru": "Премиум-членство (Месяц)", "sv": "Premiummedlemskap (Månad)", "nl": "Premium-lidmaatschap (Maand)", "el": "Premium Συνδρομή (Μήνας)"}, "price": 4.99},
    "gold_100": {"name": {"ar": "100 ذهب", "en": "100 Gold", "de": "100 Gold", "fr": "100 Or", "tr": "100 Altın", "ru": "100 золотых", "sv": "100 Guld", "nl": "100 Goud", "el": "100 Χρυσός"}, "price": 0.99},
    "gold_500": {"name": {"ar": "500 ذهب", "en": "500 Gold", "de": "500 Gold", "fr": "500 Or", "tr": "500 Altın", "ru": "500 золотых", "sv": "500 Guld", "nl": "500 Goud", "el": "500 Χρυσός"}, "price": 3.99},
    "gold_1000": {"name": {"ar": "1000 ذهب", "en": "1000 Gold", "de": "1000 Gold", "fr": "1000 Or", "tr": "1000 Altın", "ru": "1000 золотых", "sv": "1000 Guld", "nl": "1000 Goud", "el": "1000 Χρυσός"}, "price": 6.99},
}


# ==================== GOLD PACKAGES (for /payments/packages) ====================
GOLD_PACKAGES_TRANSLATED = [
    {"id": "gold_100", "name": {"ar": "100 ذهب", "en": "100 Gold", "de": "100 Gold", "fr": "100 Or", "tr": "100 Altın", "ru": "100 золотых", "sv": "100 Guld", "nl": "100 Goud", "el": "100 Χρυσός"}, "price": 0.99, "type": "gold", "amount": 100},
    {"id": "gold_500", "name": {"ar": "500 ذهب", "en": "500 Gold", "de": "500 Gold", "fr": "500 Or", "tr": "500 Altın", "ru": "500 золотых", "sv": "500 Guld", "nl": "500 Goud", "el": "500 Χρυσός"}, "price": 3.99, "type": "gold", "amount": 500},
    {"id": "gold_1000", "name": {"ar": "1000 ذهب", "en": "1000 Gold", "de": "1000 Gold", "fr": "1000 Or", "tr": "1000 Altın", "ru": "1000 золотых", "sv": "1000 Guld", "nl": "1000 Goud", "el": "1000 Χρυσός"}, "price": 6.99, "type": "gold", "amount": 1000},
    {"id": "membership_monthly", "name": {"ar": "عضوية مميزة (شهر)", "en": "Premium Membership (Month)", "de": "Premium-Mitgliedschaft (Monat)", "fr": "Abonnement Premium (Mois)", "tr": "Premium Üyelik (Ay)", "ru": "Премиум-членство (Месяц)", "sv": "Premiummedlemskap (Månad)", "nl": "Premium-lidmaatschap (Maand)", "el": "Premium Συνδρομή (Μήνας)"}, "price": 4.99, "type": "membership"},
]


# ==================== CREDIT PACKAGES ====================
CREDIT_PACKAGES_TRANSLATED = [
    {"id": "credits_5", "credits": 65, "price_eur": 0.05, "label": {"ar": "65 نقطة", "en": "65 Points", "de": "65 Punkte", "fr": "65 Points", "tr": "65 Puan", "ru": "65 очков", "sv": "65 Poäng", "nl": "65 Punten", "el": "65 Πόντοι"}, "popular": False},
    {"id": "credits_50", "credits": 650, "price_eur": 0.50, "label": {"ar": "650 نقطة", "en": "650 Points", "de": "650 Punkte", "fr": "650 Points", "tr": "650 Puan", "ru": "650 очков", "sv": "650 Poäng", "nl": "650 Punten", "el": "650 Πόντοι"}, "popular": False},
    {"id": "credits_100", "credits": 1300, "price_eur": 1.0, "label": {"ar": "1,300 نقطة", "en": "1,300 Points", "de": "1.300 Punkte", "fr": "1 300 Points", "tr": "1.300 Puan", "ru": "1 300 очков", "sv": "1 300 Poäng", "nl": "1.300 Punten", "el": "1.300 Πόντοι"}, "popular": True},
    {"id": "credits_500", "credits": 6800, "price_eur": 5.0, "label": {"ar": "6,800 نقطة", "en": "6,800 Points", "de": "6.800 Punkte", "fr": "6 800 Points", "tr": "6.800 Puan", "ru": "6 800 очков", "sv": "6 800 Poäng", "nl": "6.800 Punten", "el": "6.800 Πόντοι"}, "popular": False},
    {"id": "credits_1000", "credits": 14000, "price_eur": 10.0, "label": {"ar": "14,000 نقطة", "en": "14,000 Points", "de": "14.000 Punkte", "fr": "14 000 Points", "tr": "14.000 Puan", "ru": "14 000 очков", "sv": "14 000 Poäng", "nl": "14.000 Punten", "el": "14.000 Πόντοι"}, "popular": False},
    {"id": "credits_5000", "credits": 75000, "price_eur": 50.0, "label": {"ar": "75,000 نقطة", "en": "75,000 Points", "de": "75.000 Punkte", "fr": "75 000 Points", "tr": "75.000 Puan", "ru": "75 000 очков", "sv": "75 000 Poäng", "nl": "75.000 Punten", "el": "75.000 Πόντοι"}, "popular": False},
    {"id": "credits_10000", "credits": 160000, "price_eur": 100.0, "label": {"ar": "160,000 نقطة", "en": "160,000 Points", "de": "160.000 Punkte", "fr": "160 000 Points", "tr": "160.000 Puan", "ru": "160 000 очков", "sv": "160 000 Poäng", "nl": "160.000 Punten", "el": "160.000 Πόντοι"}, "popular": False},
    {"id": "credits_100000", "credits": 1700000, "price_eur": 1000.0, "label": {"ar": "1,700,000 نقطة", "en": "1,700,000 Points", "de": "1.700.000 Punkte", "fr": "1 700 000 Points", "tr": "1.700.000 Puan", "ru": "1 700 000 очков", "sv": "1 700 000 Poäng", "nl": "1.700.000 Punten", "el": "1.700.000 Πόντοι"}, "popular": False},
]


# ==================== ISLAMIC GIFTS ====================
ISLAMIC_GIFTS_TRANSLATED = [
    {"id": "gift_lion", "emoji": "🦁", "price_credits": 50,
     "name": {"ar": "الأسد", "en": "The Lion", "de": "Der Löwe", "fr": "Le Lion", "tr": "Aslan", "ru": "Лев", "sv": "Lejonet", "nl": "De Leeuw", "el": "Το Λιοντάρι"},
     "description": {"ar": "أسد الإسلام - هدية القوة", "en": "Lion of Islam - Gift of Strength", "de": "Löwe des Islam - Geschenk der Stärke", "fr": "Lion de l'Islam - Cadeau de force", "tr": "İslam'ın Aslanı - Güç hediyesi", "ru": "Лев Ислама - Дар силы", "sv": "Islams lejon - Styrkans gåva", "nl": "Leeuw van de Islam - Geschenk van kracht", "el": "Λιοντάρι του Ισλάμ - Δώρο δύναμης"}},
    {"id": "gift_crescent", "emoji": "🌙", "price_credits": 100,
     "name": {"ar": "الهلال الذهبي", "en": "Golden Crescent", "de": "Goldener Halbmond", "fr": "Croissant doré", "tr": "Altın Hilal", "ru": "Золотой полумесяц", "sv": "Gyllene halvmåne", "nl": "Gouden halve maan", "el": "Χρυσή ημισέληνος"},
     "description": {"ar": "رمز الإسلام المتألق", "en": "The shining symbol of Islam", "de": "Das leuchtende Symbol des Islam", "fr": "Le symbole éclatant de l'Islam", "tr": "İslam'ın parlayan sembolü", "ru": "Сияющий символ Ислама", "sv": "Islams lysande symbol", "nl": "Het stralende symbool van de Islam", "el": "Το λαμπερό σύμβολο του Ισλάμ"}},
    {"id": "gift_kaaba", "emoji": "🕋", "price_credits": 500,
     "name": {"ar": "الكعبة المشرفة", "en": "The Holy Kaaba", "de": "Die Heilige Kaaba", "fr": "La Sainte Kaaba", "tr": "Kâbe-i Muazzama", "ru": "Священная Кааба", "sv": "Den Heliga Kaba", "nl": "De Heilige Kaaba", "el": "Η Ιερή Κάαμπα"},
     "description": {"ar": "هدية مميزة بيت الله الحرام", "en": "A special gift - The Sacred House of Allah", "de": "Ein besonderes Geschenk - Das Heilige Haus Allahs", "fr": "Un cadeau spécial - La Maison Sacrée d'Allah", "tr": "Özel hediye - Allah'ın Kutsal Evi", "ru": "Особый подарок - Священный Дом Аллаха", "sv": "En speciell gåva - Allahs Heliga Hus", "nl": "Een speciaal cadeau - Het Heilige Huis van Allah", "el": "Ένα ξεχωριστό δώρο - Ο Ιερός Οίκος του Αλλάχ"}},
    {"id": "gift_star", "emoji": "⭐", "price_credits": 30,
     "name": {"ar": "النجمة", "en": "The Star", "de": "Der Stern", "fr": "L'Étoile", "tr": "Yıldız", "ru": "Звезда", "sv": "Stjärnan", "nl": "De Ster", "el": "Το Αστέρι"},
     "description": {"ar": "نجمة الإبداع", "en": "Star of Creativity", "de": "Stern der Kreativität", "fr": "Étoile de la créativité", "tr": "Yaratıcılık Yıldızı", "ru": "Звезда творчества", "sv": "Kreativitetens stjärna", "nl": "Ster van creativiteit", "el": "Αστέρι δημιουργικότητας"}},
    {"id": "gift_rose", "emoji": "🌹", "price_credits": 20,
     "name": {"ar": "الوردة", "en": "The Rose", "de": "Die Rose", "fr": "La Rose", "tr": "Gül", "ru": "Роза", "sv": "Rosen", "nl": "De Roos", "el": "Το Τριαντάφυλλο"},
     "description": {"ar": "وردة التقدير", "en": "Rose of Appreciation", "de": "Rose der Wertschätzung", "fr": "Rose de l'appréciation", "tr": "Takdir Gülü", "ru": "Роза признательности", "sv": "Uppskattningens ros", "nl": "Roos van waardering", "el": "Τριαντάφυλλο εκτίμησης"}},
    {"id": "gift_book", "emoji": "📖", "price_credits": 200,
     "name": {"ar": "القرآن", "en": "The Quran", "de": "Der Koran", "fr": "Le Coran", "tr": "Kur'an", "ru": "Коран", "sv": "Koranen", "nl": "De Koran", "el": "Το Κοράνι"},
     "description": {"ar": "نور المعرفة والهداية", "en": "Light of Knowledge and Guidance", "de": "Licht des Wissens und der Rechtleitung", "fr": "Lumière de la connaissance et de la guidance", "tr": "Bilgi ve hidayet nuru", "ru": "Свет знания и руководства", "sv": "Kunskapens och vägledningens ljus", "nl": "Licht van kennis en leiding", "el": "Φως γνώσης και καθοδήγησης"}},
    {"id": "gift_mosque", "emoji": "🕌", "price_credits": 300,
     "name": {"ar": "المسجد", "en": "The Mosque", "de": "Die Moschee", "fr": "La Mosquée", "tr": "Cami", "ru": "Мечеть", "sv": "Moskén", "nl": "De Moskee", "el": "Το Τζαμί"},
     "description": {"ar": "بيت من بيوت الله", "en": "A House of Allah", "de": "Ein Haus Allahs", "fr": "Une Maison d'Allah", "tr": "Allah'ın evlerinden bir ev", "ru": "Один из домов Аллаха", "sv": "Ett av Allahs hus", "nl": "Een Huis van Allah", "el": "Ένα Σπίτι του Αλλάχ"}},
    {"id": "gift_prayer", "emoji": "🧎", "price_credits": 150,
     "name": {"ar": "سجادة الصلاة", "en": "Prayer Mat", "de": "Gebetsteppich", "fr": "Tapis de prière", "tr": "Seccade", "ru": "Молитвенный коврик", "sv": "Bönematta", "nl": "Gebedsmat", "el": "Χαλί προσευχής"},
     "description": {"ar": "للعابدين المخلصين", "en": "For the devoted worshippers", "de": "Für die hingebungsvollen Anbeter", "fr": "Pour les adorateurs dévoués", "tr": "İhlaslı kullara", "ru": "Для преданных поклоняющихся", "sv": "För de hängivna tillbedjarna", "nl": "Voor de toegewijde aanbidders", "el": "Για τους αφοσιωμένους λάτρεις"}},
    {"id": "gift_crown", "emoji": "👑", "price_credits": 1000,
     "name": {"ar": "التاج الذهبي", "en": "Golden Crown", "de": "Goldene Krone", "fr": "Couronne dorée", "tr": "Altın Taç", "ru": "Золотая корона", "sv": "Gyllene krona", "nl": "Gouden kroon", "el": "Χρυσό στέμμα"},
     "description": {"ar": "تاج الملوك - أغلى هدية", "en": "Crown of Kings - The most precious gift", "de": "Krone der Könige - Das wertvollste Geschenk", "fr": "Couronne des rois - Le cadeau le plus précieux", "tr": "Kralların tacı - En değerli hediye", "ru": "Корона королей - Самый ценный подарок", "sv": "Kungarnas krona - Den dyrbaraste gåvan", "nl": "Kroon der koningen - Het kostbaarste cadeau", "el": "Στέμμα βασιλέων - Το πιο πολύτιμο δώρο"}},
    {"id": "gift_diamond", "emoji": "💎", "price_credits": 2000,
     "name": {"ar": "الماسة", "en": "The Diamond", "de": "Der Diamant", "fr": "Le Diamant", "tr": "Elmas", "ru": "Бриллиант", "sv": "Diamanten", "nl": "De Diamant", "el": "Το Διαμάντι"},
     "description": {"ar": "ألماسة نادرة للمميزين", "en": "A rare diamond for the distinguished", "de": "Ein seltener Diamant für die Besonderen", "fr": "Un diamant rare pour les distingués", "tr": "Seçkinler için nadir bir elmas", "ru": "Редкий бриллиант для избранных", "sv": "En sällsynt diamant för de utmärkta", "nl": "Een zeldzame diamant voor de bijzondere", "el": "Ένα σπάνιο διαμάντι για τους ξεχωριστούς"}},
    {"id": "gift_dove", "emoji": "🕊️", "price_credits": 75,
     "name": {"ar": "حمامة السلام", "en": "Dove of Peace", "de": "Friedenstaube", "fr": "Colombe de paix", "tr": "Barış Güvercini", "ru": "Голубь мира", "sv": "Fredsduva", "nl": "Vredesduif", "el": "Περιστέρι ειρήνης"},
     "description": {"ar": "رسالة سلام ومحبة", "en": "A message of peace and love", "de": "Eine Botschaft des Friedens und der Liebe", "fr": "Un message de paix et d'amour", "tr": "Barış ve sevgi mesajı", "ru": "Послание мира и любви", "sv": "Ett budskap om fred och kärlek", "nl": "Een boodschap van vrede en liefde", "el": "Ένα μήνυμα ειρήνης και αγάπης"}},
    {"id": "gift_palm", "emoji": "🌴", "price_credits": 40,
     "name": {"ar": "النخلة", "en": "The Palm Tree", "de": "Die Palme", "fr": "Le Palmier", "tr": "Hurma Ağacı", "ru": "Пальма", "sv": "Palmträdet", "nl": "De Palmboom", "el": "Ο Φοίνικας"},
     "description": {"ar": "نخلة البركة", "en": "Palm of Blessing", "de": "Palme des Segens", "fr": "Palmier de la bénédiction", "tr": "Bereket Hurması", "ru": "Пальма благословения", "sv": "Välsignelsens palm", "nl": "Palm van zegen", "el": "Φοίνικας ευλογίας"}},
]


# ==================== ERROR MESSAGES ====================
ERROR_MESSAGES = {
    "login_required": {
        "ar": "يجب تسجيل الدخول", "en": "Login required", "de": "Anmeldung erforderlich",
        "fr": "Connexion requise", "tr": "Giriş yapmanız gerekiyor", "ru": "Необходимо войти",
        "sv": "Inloggning krävs", "nl": "Inloggen vereist", "el": "Απαιτείται σύνδεση"
    },
    "product_not_found": {
        "ar": "المنتج غير موجود", "en": "Product not found", "de": "Produkt nicht gefunden",
        "fr": "Produit introuvable", "tr": "Ürün bulunamadı", "ru": "Товар не найден",
        "sv": "Produkten hittades inte", "nl": "Product niet gevonden", "el": "Το προϊόν δεν βρέθηκε"
    },
    "insufficient_gold": {
        "ar": "رصيد الذهب غير كافٍ", "en": "Insufficient gold balance", "de": "Unzureichendes Goldguthaben",
        "fr": "Solde d'or insuffisant", "tr": "Yetersiz altın bakiyesi", "ru": "Недостаточно золота",
        "sv": "Otillräckligt guldsaldo", "nl": "Onvoldoende goudsaldo", "el": "Ανεπαρκές υπόλοιπο χρυσού"
    },
    "invalid_reward_type": {
        "ar": "نوع المكافأة غير صالح", "en": "Invalid reward type", "de": "Ungültiger Belohnungstyp",
        "fr": "Type de récompense invalide", "tr": "Geçersiz ödül türü", "ru": "Недопустимый тип награды",
        "sv": "Ogiltig belöningstyp", "nl": "Ongeldig beloningstype", "el": "Μη έγκυρος τύπος ανταμοιβής"
    },
    "reward_already_claimed": {
        "ar": "تم استلام مكافأة اليوم مسبقاً", "en": "Today's reward already claimed", "de": "Heutige Belohnung bereits abgeholt",
        "fr": "Récompense du jour déjà réclamée", "tr": "Bugünkü ödül zaten alındı", "ru": "Сегодняшняя награда уже получена",
        "sv": "Dagens belöning redan hämtad", "nl": "Beloning van vandaag al opgehaald", "el": "Η σημερινή ανταμοιβή ήδη αξιώθηκε"
    },
    "origin_url_required": {
        "ar": "origin_url مطلوب", "en": "origin_url required", "de": "origin_url erforderlich",
        "fr": "origin_url requis", "tr": "origin_url gerekli", "ru": "Требуется origin_url",
        "sv": "origin_url krävs", "nl": "origin_url vereist", "el": "Απαιτείται origin_url"
    },
    "product_free_or_unavailable": {
        "ar": "هذا المنتج مجاني أو غير متاح للشراء بالمال", "en": "This product is free or not available for purchase",
        "de": "Dieses Produkt ist kostenlos oder nicht käuflich", "fr": "Ce produit est gratuit ou indisponible à l'achat",
        "tr": "Bu ürün ücretsiz veya satın alınamaz", "ru": "Этот товар бесплатный или недоступен для покупки",
        "sv": "Denna produkt är gratis eller inte tillgänglig för köp", "nl": "Dit product is gratis of niet beschikbaar voor aankoop",
        "el": "Αυτό το προϊόν είναι δωρεάν ή μη διαθέσιμο για αγορά"
    },
    "must_select_product": {
        "ar": "يجب تحديد المنتج", "en": "Must select a product", "de": "Produkt muss ausgewählt werden",
        "fr": "Vous devez sélectionner un produit", "tr": "Ürün seçilmeli", "ru": "Необходимо выбрать товар",
        "sv": "Måste välja en produkt", "nl": "Moet een product selecteren", "el": "Πρέπει να επιλέξετε ένα προϊόν"
    },
    "transaction_not_found": {
        "ar": "المعاملة غير موجودة", "en": "Transaction not found", "de": "Transaktion nicht gefunden",
        "fr": "Transaction introuvable", "tr": "İşlem bulunamadı", "ru": "Транзакция не найдена",
        "sv": "Transaktionen hittades inte", "nl": "Transactie niet gevonden", "el": "Η συναλλαγή δεν βρέθηκε"
    },
    "invalid_package": {
        "ar": "الباقة غير صالحة", "en": "Invalid package", "de": "Ungültiges Paket",
        "fr": "Forfait invalide", "tr": "Geçersiz paket", "ru": "Недействительный пакет",
        "sv": "Ogiltigt paket", "nl": "Ongeldig pakket", "el": "Μη έγκυρο πακέτο"
    },
    "invalid_gift": {
        "ar": "الهدية غير صالحة", "en": "Invalid gift", "de": "Ungültiges Geschenk",
        "fr": "Cadeau invalide", "tr": "Geçersiz hediye", "ru": "Недействительный подарок",
        "sv": "Ogiltig gåva", "nl": "Ongeldig cadeau", "el": "Μη έγκυρο δώρο"
    },
    "must_select_recipient": {
        "ar": "يجب تحديد المستلم", "en": "Must select a recipient", "de": "Empfänger muss ausgewählt werden",
        "fr": "Vous devez sélectionner un destinataire", "tr": "Alıcı seçilmeli", "ru": "Необходимо выбрать получателя",
        "sv": "Måste välja en mottagare", "nl": "Moet een ontvanger selecteren", "el": "Πρέπει να επιλέξετε παραλήπτη"
    },
    "cannot_gift_self": {
        "ar": "لا يمكنك إهداء نفسك", "en": "You cannot gift yourself", "de": "Sie können sich nicht selbst beschenken",
        "fr": "Vous ne pouvez pas vous offrir un cadeau", "tr": "Kendinize hediye gönderemezsiniz", "ru": "Нельзя дарить подарок себе",
        "sv": "Du kan inte ge gåvor till dig själv", "nl": "Je kunt geen cadeau aan jezelf geven", "el": "Δεν μπορείτε να κάνετε δώρο στον εαυτό σας"
    },
    "insufficient_credits": {
        "ar": "رصيد النقاط غير كافٍ", "en": "Insufficient credit balance", "de": "Unzureichendes Guthaben",
        "fr": "Solde de crédits insuffisant", "tr": "Yetersiz puan bakiyesi", "ru": "Недостаточно очков",
        "sv": "Otillräckligt poängsaldo", "nl": "Onvoldoende puntsaldo", "el": "Ανεπαρκές υπόλοιπο πόντων"
    },
    "email_already_registered": {
        "ar": "البريد الإلكتروني مسجل مسبقاً", "en": "Email already registered", "de": "E-Mail bereits registriert",
        "fr": "Adresse e-mail déjà enregistrée", "tr": "E-posta zaten kayıtlı", "ru": "Email уже зарегистрирован",
        "sv": "E-post redan registrerad", "nl": "E-mail al geregistreerd", "el": "Το email είναι ήδη εγγεγραμμένο"
    },
    "user_deleted": {
        "ar": "تم حذف المستخدم", "en": "User deleted", "de": "Benutzer gelöscht",
        "fr": "Utilisateur supprimé", "tr": "Kullanıcı silindi", "ru": "Пользователь удалён",
        "sv": "Användare borttagen", "nl": "Gebruiker verwijderd", "el": "Ο χρήστης διαγράφηκε"
    },
    "notification_sent": {
        "ar": "تم إرسال الإشعار", "en": "Notification sent", "de": "Benachrichtigung gesendet",
        "fr": "Notification envoyée", "tr": "Bildirim gönderildi", "ru": "Уведомление отправлено",
        "sv": "Avisering skickad", "nl": "Melding verzonden", "el": "Η ειδοποίηση στάλθηκε"
    },
}


def get_error(key: str, locale: str = "ar") -> str:
    """Get localized error message."""
    msg = ERROR_MESSAGES.get(key, {})
    return _t(msg, locale) if msg else key


# ==================== SOHBA CATEGORIES ====================
SOHBA_CATEGORIES_TRANSLATED = [
    {"key": "general", "labelKey": "sohbaCatGeneral", "icon": "globe",
     "label": {"ar": "عام", "en": "General", "de": "Allgemein", "fr": "Général", "tr": "Genel", "ru": "Общее", "sv": "Allmänt", "nl": "Algemeen", "el": "Γενικά"}},
    {"key": "quran", "labelKey": "sohbaCatQuran", "icon": "book",
     "label": {"ar": "القرآن الكريم", "en": "The Noble Quran", "de": "Der Edle Koran", "fr": "Le Noble Coran", "tr": "Kur'ân-ı Kerîm", "ru": "Благородный Коран", "sv": "Den Ädla Koranen", "nl": "De Edele Koran", "el": "Το Ευγενές Κοράνι"}},
    {"key": "hadith", "labelKey": "sohbaCatHadith", "icon": "scroll",
     "label": {"ar": "الحديث الشريف", "en": "Noble Hadith", "de": "Edle Hadithe", "fr": "Noble Hadith", "tr": "Hadis-i Şerif", "ru": "Благородный Хадис", "sv": "Ädla Hadith", "nl": "Edele Hadith", "el": "Ευγενές Χαντίθ"}},
    {"key": "ramadan", "labelKey": "sohbaCatRamadan", "icon": "moon",
     "label": {"ar": "رمضان", "en": "Ramadan", "de": "Ramadan", "fr": "Ramadan", "tr": "Ramazan", "ru": "Рамадан", "sv": "Ramadan", "nl": "Ramadan", "el": "Ραμαντάν"}},
    {"key": "dua", "labelKey": "sohbaCatDua", "icon": "hands",
     "label": {"ar": "الدعاء والأذكار", "en": "Duas & Dhikr", "de": "Bittgebete & Dhikr", "fr": "Invocations & Dhikr", "tr": "Dua ve Zikirler", "ru": "Дуа и Зикр", "sv": "Böner & Dhikr", "nl": "Smeekbeden & Dhikr", "el": "Ντουά & Ζικρ"}},
    {"key": "stories", "labelKey": "sohbaCatStories", "icon": "feather",
     "label": {"ar": "قصص وعبر", "en": "Stories & Lessons", "de": "Geschichten & Lehren", "fr": "Histoires & Leçons", "tr": "Kıssalar ve İbretler", "ru": "Истории и уроки", "sv": "Berättelser & Lärdomar", "nl": "Verhalen & Lessen", "el": "Ιστορίες & Μαθήματα"}},
    {"key": "hajj", "labelKey": "sohbaCatHajj", "icon": "kaaba",
     "label": {"ar": "الحج والعمرة", "en": "Hajj & Umrah", "de": "Hajj & Umra", "fr": "Hajj & Omra", "tr": "Hac ve Umre", "ru": "Хадж и Умра", "sv": "Hajj & Umrah", "nl": "Hadj & Umrah", "el": "Χατζ & Ούμρα"}},
    {"key": "halal", "labelKey": "sohbaCatHalal", "icon": "plane",
     "label": {"ar": "السفر الحلال", "en": "Halal Travel", "de": "Halal-Reisen", "fr": "Voyage Halal", "tr": "Helal Seyahat", "ru": "Халяль-путешествия", "sv": "Halal-resor", "nl": "Halal-reizen", "el": "Χαλάλ Ταξίδια"}},
    {"key": "family", "labelKey": "sohbaCatFamily", "icon": "heart",
     "label": {"ar": "الأسرة المسلمة", "en": "Muslim Family", "de": "Muslimische Familie", "fr": "Famille musulmane", "tr": "Müslüman Aile", "ru": "Мусульманская семья", "sv": "Muslimsk familj", "nl": "Moslimfamilie", "el": "Μουσουλμανική οικογένεια"}},
    {"key": "youth", "labelKey": "sohbaCatYouth", "icon": "users",
     "label": {"ar": "الشباب", "en": "Youth", "de": "Jugend", "fr": "Jeunesse", "tr": "Gençlik", "ru": "Молодёжь", "sv": "Ungdom", "nl": "Jeugd", "el": "Νεολαία"}},
]


# ==================== STORY CATEGORIES ====================
STORY_CATEGORIES_TRANSLATED = [
    {"key": "general", "labelKey": "storyCatGeneral", "emoji": "📝", "icon": "file-text", "color": "#64748b",
     "label": {"ar": "عام", "en": "General", "de": "Allgemein", "fr": "Général", "tr": "Genel", "ru": "Общее", "sv": "Allmänt", "nl": "Algemeen", "el": "Γενικά"}},
    {"key": "istighfar", "labelKey": "storyCatIstighfar", "emoji": "🤲", "icon": "sparkles", "color": "#10b981",
     "label": {"ar": "قصص الاستغفار", "en": "Stories of Repentance", "de": "Geschichten der Reue", "fr": "Histoires de repentir", "tr": "İstiğfar Kıssaları", "ru": "Истории покаяния", "sv": "Berättelser om ånger", "nl": "Verhalen van berouw", "el": "Ιστορίες μετάνοιας"}},
    {"key": "sahaba", "labelKey": "storyCatSahaba", "emoji": "📖", "icon": "book", "color": "#f59e0b",
     "label": {"ar": "قصص الصحابة", "en": "Stories of the Companions", "de": "Geschichten der Gefährten", "fr": "Histoires des Compagnons", "tr": "Sahabe Kıssaları", "ru": "Истории сподвижников", "sv": "Följeslagarnas berättelser", "nl": "Verhalen van de metgezellen", "el": "Ιστορίες των Σαχάμπα"}},
    {"key": "quran", "labelKey": "storyCatQuran", "emoji": "📗", "icon": "book-open", "color": "#059669",
     "label": {"ar": "قصص القرآن", "en": "Stories of the Quran", "de": "Geschichten des Koran", "fr": "Histoires du Coran", "tr": "Kur'an Kıssaları", "ru": "Истории Корана", "sv": "Koranens berättelser", "nl": "Verhalen van de Koran", "el": "Ιστορίες του Κορανίου"}},
    {"key": "prophets", "labelKey": "storyCatProphets", "emoji": "🌟", "icon": "star", "color": "#8b5cf6",
     "label": {"ar": "قصص الأنبياء", "en": "Stories of the Prophets", "de": "Geschichten der Propheten", "fr": "Histoires des Prophètes", "tr": "Peygamber Kıssaları", "ru": "Истории пророков", "sv": "Profeternas berättelser", "nl": "Verhalen van de profeten", "el": "Ιστορίες των Προφητών"}},
    {"key": "ruqyah", "labelKey": "storyCatRuqyah", "emoji": "🛡️", "icon": "shield", "color": "#3b82f6",
     "label": {"ar": "قصص الرقية", "en": "Ruqyah Stories", "de": "Ruqya-Geschichten", "fr": "Histoires de Roqya", "tr": "Rukye Kıssaları", "ru": "Истории рукъя", "sv": "Ruqyah-berättelser", "nl": "Ruqyah-verhalen", "el": "Ιστορίες Ρουκιά"}},
    {"key": "rizq", "labelKey": "storyCatRizq", "emoji": "✨", "icon": "coins", "color": "#eab308",
     "label": {"ar": "قصص الرزق", "en": "Stories of Provision", "de": "Geschichten der Versorgung", "fr": "Histoires de subsistance", "tr": "Rızık Kıssaları", "ru": "Истории о пропитании", "sv": "Berättelser om försörjning", "nl": "Verhalen van voorziening", "el": "Ιστορίες πρόνοιας"}},
    {"key": "tawba", "labelKey": "storyCatTawba", "emoji": "💚", "icon": "heart", "color": "#22c55e",
     "label": {"ar": "قصص التوبة", "en": "Stories of Repentance", "de": "Geschichten der Umkehr", "fr": "Histoires de repentance", "tr": "Tövbe Kıssaları", "ru": "Истории покаяния", "sv": "Berättelser om omvändelse", "nl": "Verhalen van berouw", "el": "Ιστορίες μετάνοιας"}},
    {"key": "miracles", "labelKey": "storyCatMiracles", "emoji": "🌙", "icon": "moon", "color": "#6366f1",
     "label": {"ar": "معجزات وعبر", "en": "Miracles & Lessons", "de": "Wunder & Lehren", "fr": "Miracles & Leçons", "tr": "Mucizeler ve İbretler", "ru": "Чудеса и уроки", "sv": "Mirakel & Lärdomar", "nl": "Wonderen & Lessen", "el": "Θαύματα & Μαθήματα"}},
    {"key": "embed", "labelKey": "storyCatEmbed", "emoji": "🎬", "icon": "film", "color": "#ef4444",
     "label": {"ar": "فيديوهات", "en": "Videos", "de": "Videos", "fr": "Vidéos", "tr": "Videolar", "ru": "Видео", "sv": "Videor", "nl": "Video's", "el": "Βίντεο"}},
]


# ==================== UI STRINGS (BACKEND) ====================
# Completing missing languages (sv, nl, el) for the /localization/strings/{lang} endpoint
UI_STRINGS_ALL = {
    "ar": {
        "home": "الرئيسية", "prayer_times": "مواقيت الصلاة", "quran": "القرآن الكريم",
        "qibla": "اتجاه القبلة", "tasbeeh": "التسبيح", "duas": "الأدعية",
        "stories": "حكاياتي", "messages": "الرسائل", "more": "المزيد",
        "login": "تسجيل الدخول", "register": "إنشاء حساب", "profile": "الملف الشخصي",
        "follow": "متابعة", "following": "متابَع", "followers": "متابعين",
        "likes": "الإعجابات", "comments": "التعليقات", "share": "مشاركة",
        "create_post": "إنشاء منشور", "trending": "الترندات", "video": "فيديو",
        "search": "بحث", "settings": "الإعدادات", "logout": "خروج",
    },
    "en": {
        "home": "Home", "prayer_times": "Prayer Times", "quran": "Quran",
        "qibla": "Qibla", "tasbeeh": "Tasbeeh", "duas": "Duas",
        "stories": "Hikayati", "messages": "Messages", "more": "More",
        "login": "Login", "register": "Register", "profile": "Profile",
        "follow": "Follow", "following": "Following", "followers": "Followers",
        "likes": "Likes", "comments": "Comments", "share": "Share",
        "create_post": "Create Post", "trending": "Trending", "video": "Video",
        "search": "Search", "settings": "Settings", "logout": "Logout",
    },
    "de": {
        "home": "Startseite", "prayer_times": "Gebetszeiten", "quran": "Koran",
        "qibla": "Qibla", "tasbeeh": "Tasbih", "duas": "Bittgebete",
        "stories": "Hikayati", "messages": "Nachrichten", "more": "Mehr",
        "login": "Anmelden", "register": "Registrieren", "profile": "Profil",
        "follow": "Folgen", "following": "Gefolgt", "followers": "Follower",
        "likes": "Gefällt mir", "comments": "Kommentare", "share": "Teilen",
        "create_post": "Beitrag erstellen", "trending": "Trends", "video": "Video",
        "search": "Suche", "settings": "Einstellungen", "logout": "Abmelden",
    },
    "fr": {
        "home": "Accueil", "prayer_times": "Heures de prière", "quran": "Coran",
        "qibla": "Qibla", "tasbeeh": "Tasbih", "duas": "Invocations",
        "stories": "Hikayati", "messages": "Messages", "more": "Plus",
        "login": "Connexion", "register": "Inscription", "profile": "Profil",
        "follow": "Suivre", "following": "Abonné", "followers": "Abonnés",
        "likes": "J'aime", "comments": "Commentaires", "share": "Partager",
        "create_post": "Créer une publication", "trending": "Tendances", "video": "Vidéo",
        "search": "Recherche", "settings": "Paramètres", "logout": "Déconnexion",
    },
    "tr": {
        "home": "Ana Sayfa", "prayer_times": "Namaz Vakitleri", "quran": "Kur'an",
        "qibla": "Kıble", "tasbeeh": "Tesbih", "duas": "Dualar",
        "stories": "Hikayelerim", "messages": "Mesajlar", "more": "Daha Fazla",
        "login": "Giriş", "register": "Kayıt Ol", "profile": "Profil",
        "follow": "Takip Et", "following": "Takip Ediliyor", "followers": "Takipçiler",
        "likes": "Beğeniler", "comments": "Yorumlar", "share": "Paylaş",
        "create_post": "Gönderi Oluştur", "trending": "Trendler", "video": "Video",
        "search": "Ara", "settings": "Ayarlar", "logout": "Çıkış",
    },
    "ru": {
        "home": "Главная", "prayer_times": "Время молитв", "quran": "Коран",
        "qibla": "Кибла", "tasbeeh": "Тасбих", "duas": "Дуа",
        "stories": "Хикаяти", "messages": "Сообщения", "more": "Ещё",
        "login": "Войти", "register": "Регистрация", "profile": "Профиль",
        "follow": "Подписаться", "following": "Подписан", "followers": "Подписчики",
        "likes": "Нравится", "comments": "Комментарии", "share": "Поделиться",
        "create_post": "Создать пост", "trending": "В тренде", "video": "Видео",
        "search": "Поиск", "settings": "Настройки", "logout": "Выход",
    },
    "sv": {
        "home": "Hem", "prayer_times": "Bönetider", "quran": "Koranen",
        "qibla": "Qibla", "tasbeeh": "Tasbih", "duas": "Böner",
        "stories": "Hikayati", "messages": "Meddelanden", "more": "Mer",
        "login": "Logga in", "register": "Registrera", "profile": "Profil",
        "follow": "Följ", "following": "Följer", "followers": "Följare",
        "likes": "Gillar", "comments": "Kommentarer", "share": "Dela",
        "create_post": "Skapa inlägg", "trending": "Trendande", "video": "Video",
        "search": "Sök", "settings": "Inställningar", "logout": "Logga ut",
    },
    "nl": {
        "home": "Home", "prayer_times": "Gebedstijden", "quran": "Koran",
        "qibla": "Qibla", "tasbeeh": "Tasbih", "duas": "Smeekbeden",
        "stories": "Hikayati", "messages": "Berichten", "more": "Meer",
        "login": "Inloggen", "register": "Registreren", "profile": "Profiel",
        "follow": "Volgen", "following": "Volgend", "followers": "Volgers",
        "likes": "Likes", "comments": "Reacties", "share": "Delen",
        "create_post": "Bericht maken", "trending": "Trending", "video": "Video",
        "search": "Zoeken", "settings": "Instellingen", "logout": "Uitloggen",
    },
    "el": {
        "home": "Αρχική", "prayer_times": "Ώρες Προσευχής", "quran": "Κοράνι",
        "qibla": "Κίμπλα", "tasbeeh": "Τασμπίχ", "duas": "Ντουά",
        "stories": "Χικαγιάτι", "messages": "Μηνύματα", "more": "Περισσότερα",
        "login": "Σύνδεση", "register": "Εγγραφή", "profile": "Προφίλ",
        "follow": "Ακολούθηση", "following": "Ακολουθείτε", "followers": "Ακόλουθοι",
        "likes": "Μου αρέσει", "comments": "Σχόλια", "share": "Κοινοποίηση",
        "create_post": "Δημιουργία ανάρτησης", "trending": "Τάσεις", "video": "Βίντεο",
        "search": "Αναζήτηση", "settings": "Ρυθμίσεις", "logout": "Αποσύνδεση",
    },
}

# ==================== STORE LISTING (App Stores) ====================
STORE_LISTING_TRANSLATED = {
    "ar": {"title": "أذان وحكاية - مواقيت الصلاة والقرآن", "short": "مواقيت الصلاة، القرآن، الأذكار"},
    "en": {"title": "Azan & Hikaya - Prayer Times & Quran", "short": "Prayer Times, Quran, Azkar"},
    "de": {"title": "Azan & Hikaya - Gebetszeiten & Koran", "short": "Gebetszeiten, Koran, Dhikr"},
    "fr": {"title": "Azan & Hikaya - Heures de prière & Coran", "short": "Heures de prière, Coran, Dhikr"},
    "tr": {"title": "Ezan ve Hikaye - Namaz Vakitleri ve Kur'an", "short": "Namaz Vakitleri, Kur'an, Zikirler"},
    "ru": {"title": "Азан и Хикая - Время молитв и Коран", "short": "Время молитв, Коран, Азкар"},
    "sv": {"title": "Azan & Hikaya - Bönetider & Koranen", "short": "Bönetider, Koranen, Dhikr"},
    "nl": {"title": "Azan & Hikaya - Gebedstijden & Koran", "short": "Gebedstijden, Koran, Dhikr"},
    "el": {"title": "Αζάν & Χικάγια - Ώρες Προσευχής & Κοράνι", "short": "Ώρες Προσευχής, Κοράνι, Αζκάρ"},
}

# ==================== SEO KEYWORDS ====================
SEO_KEYWORDS_TRANSLATED = {
    "ar": ["مواقيت الصلاة", "القرآن الكريم", "أذكار", "أدعية", "حكاياتي", "منصة إسلامية"],
    "en": ["prayer times", "quran", "islamic app", "muslim", "azkar", "duas"],
    "de": ["gebetszeiten", "koran", "islamische app", "muslim", "dhikr", "dua"],
    "fr": ["heures de prière", "coran", "application islamique", "musulman", "dhikr", "invocations"],
    "tr": ["namaz vakitleri", "kuran", "islam uygulaması", "müslüman", "dua", "zikir"],
    "ru": ["время молитв", "коран", "исламское приложение", "мусульманин", "намаз", "дуа"],
    "sv": ["bönetider", "koranen", "islamisk app", "muslim", "dhikr", "böner"],
    "nl": ["gebedstijden", "koran", "islamitische app", "moslim", "dhikr", "smeekbeden"],
    "el": ["ώρες προσευχής", "κοράνι", "ισλαμική εφαρμογή", "μουσουλμάνος", "ζικρ", "ντουά"],
}

# ==================== SUPPORTED LANGUAGES (full list) ====================
SUPPORTED_LANGUAGES_FULL = [
    {"code": "ar", "label": "العربية", "flag": "🇸🇦", "dir": "rtl", "complete": True},
    {"code": "en", "label": "English", "flag": "🇬🇧", "dir": "ltr", "complete": True},
    {"code": "de", "label": "Deutsch", "flag": "🇩🇪", "dir": "ltr", "complete": True},
    {"code": "de-AT", "label": "Deutsch (Österreich)", "flag": "🇦🇹", "dir": "ltr", "complete": True},
    {"code": "fr", "label": "Français", "flag": "🇫🇷", "dir": "ltr", "complete": True},
    {"code": "tr", "label": "Türkçe", "flag": "🇹🇷", "dir": "ltr", "complete": True},
    {"code": "ru", "label": "Русский", "flag": "🇷🇺", "dir": "ltr", "complete": True},
    {"code": "sv", "label": "Svenska", "flag": "🇸🇪", "dir": "ltr", "complete": True},
    {"code": "nl", "label": "Nederlands", "flag": "🇳🇱", "dir": "ltr", "complete": True},
    {"code": "el", "label": "Ελληνικά", "flag": "🇬🇷", "dir": "ltr", "complete": True},
]

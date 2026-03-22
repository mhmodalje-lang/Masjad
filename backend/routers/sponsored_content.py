"""
Islamic Sponsored Content System
=================================
Self-hosted halal ad system - no 3rd party ad networks
Each ad is Islamic-themed sponsored content (books, courses, charities, etc.)
Connected to Baraka Market reward system
"""
from fastapi import APIRouter
from deps import db
from datetime import datetime
import uuid
import random

router = APIRouter(tags=["Sponsored Content"])

# ═══ ISLAMIC SPONSORED CONTENT DATABASE ═══
# Real Islamic content - NO policy violations, NO 3rd party ad networks

SPONSORED_CONTENT = [
    # ═══ ISLAMIC BOOKS ═══
    {"id": "sp_quran_tafsir", "category": "books", "emoji": "📖",
     "title": {"ar": "تفسير ابن كثير الميسر", "en": "Ibn Kathir Tafsir Simplified", "de": "Ibn Kathir Tafsir vereinfacht", "fr": "Tafsir Ibn Kathir simplifié", "tr": "İbn Kesir Tefsiri", "ru": "Тафсир Ибн Касира", "sv": "Ibn Kathir Tafsir", "nl": "Ibn Kathir Tafsir", "el": "Ταφσίρ Ιμπν Καθίρ"},
     "desc": {"ar": "فهم القرآن بأسلوب سهل ومبسط", "en": "Understand the Quran in a simple way", "de": "Den Quran einfach verstehen", "fr": "Comprendre le Coran facilement", "tr": "Kur'an'ı kolay anlayın", "ru": "Понимание Корана простым языком", "sv": "Förstå Koranen enkelt", "nl": "Begrijp de Koran eenvoudig", "el": "Κατανόηση του Κορανίου"},
     "cta": {"ar": "اقرأ مجاناً", "en": "Read Free", "de": "Kostenlos lesen", "fr": "Lire gratuitement", "tr": "Ücretsiz oku", "ru": "Читать бесплатно", "sv": "Läs gratis", "nl": "Gratis lezen", "el": "Διάβασε δωρεάν"},
     "color": "#10B981", "icon": "📖", "coins_reward": 5, "placement": ["main", "quran", "stories"],
     "target_route": "/tafsir"},

    {"id": "sp_riyad_saliheen", "category": "books", "emoji": "📚",
     "title": {"ar": "رياض الصالحين", "en": "Riyad As-Salihin", "de": "Riyad As-Salihin", "fr": "Riyad As-Salihin", "tr": "Riyâzü's-Sâlihîn", "ru": "Сады праведных", "sv": "Riyad As-Salihin", "nl": "Riyad As-Salihin", "el": "Ριγιάντ Ας-Σαλιχίν"},
     "desc": {"ar": "أحاديث نبوية مختارة في الأخلاق والعبادات", "en": "Selected hadiths on morals and worship", "de": "Ausgewählte Hadithe über Moral", "fr": "Hadiths sélectionnés sur la morale", "tr": "Ahlak ve ibadet üzerine hadisler", "ru": "Избранные хадисы о нравственности", "sv": "Utvalda hadither om moral", "nl": "Geselecteerde hadith over moraal", "el": "Επιλεγμένα χαντίθ"},
     "cta": {"ar": "تصفح الأحاديث", "en": "Browse Hadiths", "de": "Hadithe durchsuchen", "fr": "Parcourir les hadiths", "tr": "Hadisleri gözat", "ru": "Просмотреть хадисы", "sv": "Bläddra hadither", "nl": "Bekijk hadith", "el": "Δες χαντίθ"},
     "color": "#8B5CF6", "icon": "📚", "coins_reward": 5, "placement": ["main", "duas", "stories"],
     "target_route": "/stories"},

    {"id": "sp_40_nawawi", "category": "books", "emoji": "📕",
     "title": {"ar": "الأربعون النووية", "en": "40 Nawawi Hadiths", "de": "40 Nawawi Hadithe", "fr": "40 Hadiths Nawawi", "tr": "Kırk Hadis", "ru": "40 хадисов ан-Навави", "sv": "40 Nawawi hadither", "nl": "40 Nawawi hadith", "el": "40 Χαντίθ Ναουαουί"},
     "desc": {"ar": "أربعون حديثاً جامعاً لأصول الدين", "en": "40 comprehensive hadiths on Islam's foundations", "de": "40 umfassende Hadithe über die Grundlagen", "fr": "40 hadiths sur les fondements de l'Islam", "tr": "İslam'ın temelleri üzerine 40 hadis", "ru": "40 хадисов об основах Ислама", "sv": "40 hadither om Islams grunder", "nl": "40 hadith over de basis van de Islam", "el": "40 χαντίθ για τα θεμέλια"},
     "cta": {"ar": "ابدأ الحفظ", "en": "Start Memorizing", "de": "Auswendig lernen", "fr": "Commence à mémoriser", "tr": "Ezberlemeye başla", "ru": "Начать заучивать", "sv": "Börja memorera", "nl": "Begin met memoriseren", "el": "Ξεκίνα απομνημόνευση"},
     "color": "#EF4444", "icon": "📕", "coins_reward": 5, "placement": ["main", "duas"],
     "target_route": "/forty-nawawi"},

    # ═══ ISLAMIC COURSES ═══
    {"id": "sp_tajweed_course", "category": "courses", "emoji": "🎓",
     "title": {"ar": "دورة التجويد المتقدمة", "en": "Advanced Tajweed Course", "de": "Fortgeschrittener Tajweed-Kurs", "fr": "Cours avancé de Tajweed", "tr": "İleri Tecvid Kursu", "ru": "Курс таджвида", "sv": "Avancerad Tajweed-kurs", "nl": "Gevorderde Tajweed-cursus", "el": "Προχωρημένο μάθημα Ταζουίντ"},
     "desc": {"ar": "تعلم أحكام التجويد مع شيخ متخصص", "en": "Learn tajweed rules with a specialist", "de": "Lerne Tajweed-Regeln mit einem Spezialisten", "fr": "Apprenez le tajweed avec un spécialiste", "tr": "Uzman hocayla tecvid kurallarını öğrenin", "ru": "Изучите правила таджвида со специалистом", "sv": "Lär dig tajweed med en specialist", "nl": "Leer tajweed met een specialist", "el": "Μάθε ταζουίντ με ειδικό"},
     "cta": {"ar": "سجل مجاناً", "en": "Enroll Free", "de": "Kostenlos anmelden", "fr": "Inscris-toi gratuitement", "tr": "Ücretsiz kaydol", "ru": "Записаться бесплатно", "sv": "Registrera gratis", "nl": "Gratis inschrijven", "el": "Εγγράψου δωρεάν"},
     "color": "#F59E0B", "icon": "🎓", "coins_reward": 5, "placement": ["quran", "main"],
     "target_route": "/quran"},

    {"id": "sp_arabic_course", "category": "courses", "emoji": "🔤",
     "title": {"ar": "دورة اللغة العربية للمبتدئين", "en": "Arabic Language for Beginners", "de": "Arabisch für Anfänger", "fr": "L'arabe pour débutants", "tr": "Yeni Başlayanlar İçin Arapça", "ru": "Арабский для начинающих", "sv": "Arabiska för nybörjare", "nl": "Arabisch voor beginners", "el": "Αραβικά για αρχάριους"},
     "desc": {"ar": "تعلم القراءة والكتابة العربية في 30 يوماً", "en": "Learn to read & write Arabic in 30 days", "de": "Lerne Arabisch lesen & schreiben in 30 Tagen", "fr": "Apprenez à lire l'arabe en 30 jours", "tr": "30 günde Arapça okumayı öğrenin", "ru": "Научитесь читать по-арабски за 30 дней", "sv": "Lär dig arabiska på 30 dagar", "nl": "Leer Arabisch in 30 dagen", "el": "Μάθε αραβικά σε 30 μέρες"},
     "cta": {"ar": "ابدأ التعلم", "en": "Start Learning", "de": "Lerne jetzt", "fr": "Commence à apprendre", "tr": "Öğrenmeye başla", "ru": "Начать обучение", "sv": "Börja lära dig", "nl": "Begin met leren", "el": "Ξεκίνα να μαθαίνεις"},
     "color": "#3B82F6", "icon": "🔤", "coins_reward": 5, "placement": ["main", "stories"],
     "target_route": "/kids-zone"},

    # ═══ ISLAMIC CHARITY ═══
    {"id": "sp_orphan_sponsor", "category": "charity", "emoji": "🤲",
     "title": {"ar": "اكفل يتيماً", "en": "Sponsor an Orphan", "de": "Waise unterstützen", "fr": "Parrainez un orphelin", "tr": "Yetim Sponsor Ol", "ru": "Спонсируй сироту", "sv": "Sponsra en föräldralös", "nl": "Sponsor een wees", "el": "Υποστήριξε ένα ορφανό"},
     "desc": {"ar": "أنا وكافل اليتيم في الجنة كهاتين — حديث نبوي", "en": "I and the caretaker of an orphan will be in Paradise — Hadith", "de": "Ich und der Betreuer einer Waise werden im Paradies sein", "fr": "Moi et le tuteur de l'orphelin serons au Paradis", "tr": "Ben ve yetimin bakıcısı cennette böyle olacağız", "ru": "Я и опекун сироты будем в Раю", "sv": "Jag och den föräldralöses vårdare i Paradiset", "nl": "Ik en de verzorger van een wees in het Paradijs", "el": "Εγώ και ο κηδεμόνας ορφανού στον Παράδεισο"},
     "cta": {"ar": "تبرع الآن", "en": "Donate Now", "de": "Jetzt spenden", "fr": "Faire un don", "tr": "Şimdi bağış yap", "ru": "Пожертвовать", "sv": "Donera nu", "nl": "Doneer nu", "el": "Δώρισε τώρα"},
     "color": "#EC4899", "icon": "🤲", "coins_reward": 10, "placement": ["main", "duas", "stories"],
     "target_route": "/donations"},

    {"id": "sp_water_well", "category": "charity", "emoji": "💧",
     "title": {"ar": "ساهم في حفر بئر ماء", "en": "Help Build a Water Well", "de": "Helfe beim Brunnenbau", "fr": "Aidez à construire un puits", "tr": "Su kuyusu açılmasına yardım et", "ru": "Помоги построить колодец", "sv": "Hjälp bygga en brunn", "nl": "Help een waterput bouwen", "el": "Βοήθα να χτιστεί πηγάδι"},
     "desc": {"ar": "صدقة جارية تنفع الناس وتستمر بعد الموت", "en": "Ongoing charity that benefits people forever", "de": "Fortlaufende Wohltätigkeit die ewig hilft", "fr": "Charité continue qui aide pour toujours", "tr": "İnsanlara sonsuza dek fayda sağlayan sadaka", "ru": "Непрерывная благотворительность", "sv": "Välgörenhet som hjälper för alltid", "nl": "Doorlopende liefdadigheid", "el": "Συνεχής φιλανθρωπία"},
     "cta": {"ar": "ساهم الآن", "en": "Contribute Now", "de": "Jetzt beitragen", "fr": "Contribuer maintenant", "tr": "Şimdi katkıda bulun", "ru": "Внести вклад", "sv": "Bidra nu", "nl": "Draag nu bij", "el": "Συνεισφέρε τώρα"},
     "color": "#06B6D4", "icon": "💧", "coins_reward": 10, "placement": ["main", "duas"],
     "target_route": "/donations"},

    {"id": "sp_mosque_build", "category": "charity", "emoji": "🕌",
     "title": {"ar": "ساهم في بناء مسجد", "en": "Help Build a Mosque", "de": "Helfe beim Moscheebau", "fr": "Aidez à construire une mosquée", "tr": "Cami yapımına katkı sağla", "ru": "Помоги построить мечеть", "sv": "Hjälp bygga en moské", "nl": "Help een moskee bouwen", "el": "Βοήθα να χτιστεί τζαμί"},
     "desc": {"ar": "من بنى لله مسجدًا بنى الله له بيتًا في الجنة", "en": "Whoever builds a mosque, Allah builds a house in Paradise for them", "de": "Wer eine Moschee baut, dem baut Allah ein Haus im Paradies", "fr": "Qui construit une mosquée, Allah lui construit une maison au Paradis", "tr": "Kim bir mescid yaparsa Allah ona cennette bir ev yapar", "ru": "Кто построит мечеть, Аллах построит ему дом в Раю", "sv": "Den som bygger en moské, bygger Allah ett hus i Paradiset", "nl": "Wie een moskee bouwt, Allah bouwt een huis in het Paradijs", "el": "Όποιος χτίσει τζαμί, ο Αλλάχ χτίζει σπίτι στον Παράδεισο"},
     "cta": {"ar": "ساهم في البناء", "en": "Help Build", "de": "Helfe beim Bau", "fr": "Aidez à construire", "tr": "İnşaata katkıda bulun", "ru": "Помоги построить", "sv": "Hjälp att bygga", "nl": "Help bouwen", "el": "Βοήθα στην κατασκευή"},
     "color": "#059669", "icon": "🕌", "coins_reward": 10, "placement": ["main", "duas", "stories"],
     "target_route": "/donations"},

    # ═══ ISLAMIC PRODUCTS ═══
    {"id": "sp_prayer_mat", "category": "products", "emoji": "🧎",
     "title": {"ar": "سجادة صلاة ذكية", "en": "Smart Prayer Mat", "de": "Smarte Gebetsmatte", "fr": "Tapis de prière intelligent", "tr": "Akıllı Seccade", "ru": "Умный молитвенный коврик", "sv": "Smart bönematta", "nl": "Slim gebedsmatje", "el": "Έξυπνο χαλί προσευχής"},
     "desc": {"ar": "سجادة صلاة تساعدك في تعلم الصلاة الصحيحة", "en": "A prayer mat that helps you learn proper prayer", "de": "Eine Gebetsmatte die beim Gebet hilft", "fr": "Un tapis qui aide à apprendre la prière", "tr": "Doğru namaz kılmayı öğreten seccade", "ru": "Коврик, который помогает учиться молиться", "sv": "En bönematta som hjälper dig be", "nl": "Een gebedsmat die helpt bij het gebed", "el": "Χαλί που βοηθά στην προσευχή"},
     "cta": {"ar": "اطلب الآن", "en": "Order Now", "de": "Jetzt bestellen", "fr": "Commandez maintenant", "tr": "Şimdi sipariş ver", "ru": "Заказать", "sv": "Beställ nu", "nl": "Bestel nu", "el": "Παράγγειλε τώρα"},
     "color": "#D97706", "icon": "🧎", "coins_reward": 5, "placement": ["main"],
     "target_route": "/baraka-market"},

    {"id": "sp_quran_pen", "category": "products", "emoji": "🖊️",
     "title": {"ar": "القلم القارئ للقرآن", "en": "Quran Reading Pen", "de": "Koran-Lesestift", "fr": "Stylo lecteur du Coran", "tr": "Kur'an Okuma Kalemi", "ru": "Ручка для чтения Корана", "sv": "Koranen läspenna", "nl": "Koran-leespen", "el": "Στυλό ανάγνωσης Κορανίου"},
     "desc": {"ar": "قلم ذكي يقرأ لك القرآن بصوت أشهر القراء", "en": "A smart pen that reads Quran for you", "de": "Ein smarter Stift der den Koran liest", "fr": "Un stylo intelligent qui lit le Coran", "tr": "Kur'an'ı sizin için okuyan akıllı kalem", "ru": "Умная ручка, читающая Коран", "sv": "En smart penna som läser Koranen", "nl": "Een slimme pen die de Koran leest", "el": "Ένα έξυπνο στυλό που διαβάζει το Κοράνι"},
     "cta": {"ar": "اشترِ الآن", "en": "Buy Now", "de": "Jetzt kaufen", "fr": "Acheter maintenant", "tr": "Şimdi satın al", "ru": "Купить", "sv": "Köp nu", "nl": "Nu kopen", "el": "Αγόρασε τώρα"},
     "color": "#7C3AED", "icon": "🖊️", "coins_reward": 5, "placement": ["quran", "main"],
     "target_route": "/quran"},

    # ═══ DAILY REMINDERS ═══
    {"id": "sp_dhikr_reminder", "category": "reminder", "emoji": "📿",
     "title": {"ar": "لا تنسَ ذكر الله", "en": "Don't Forget to Remember Allah", "de": "Vergiss das Gedenken Allahs nicht", "fr": "N'oublie pas le dhikr", "tr": "Allah'ı Zikretmeyi Unutma", "ru": "Не забывай поминать Аллаха", "sv": "Glöm inte att minnas Allah", "nl": "Vergeet niet Allah te gedenken", "el": "Μη ξεχνάς τον Αλλάχ"},
     "desc": {"ar": "ألا بذكر الله تطمئن القلوب — الرعد ٢٨", "en": "Surely in the remembrance of Allah hearts find peace — 13:28", "de": "Im Gedenken Allahs finden Herzen Ruhe — 13:28", "fr": "C'est par le rappel d'Allah que les cœurs se tranquillisent — 13:28", "tr": "Kalpler ancak Allah'ın zikriyle huzur bulur — 13:28", "ru": "Поистине, в поминании Аллаха сердца находят покой — 13:28", "sv": "I Allahs åminnelse finner hjärtan frid — 13:28", "nl": "In het gedenken van Allah vinden harten vrede — 13:28", "el": "Στη μνήμη του Αλλάχ βρίσκουν ειρήνη οι καρδιές — 13:28"},
     "cta": {"ar": "ابدأ الذكر", "en": "Start Dhikr", "de": "Dhikr starten", "fr": "Commencer le dhikr", "tr": "Zikre başla", "ru": "Начать зикр", "sv": "Börja dhikr", "nl": "Begin dhikr", "el": "Ξεκίνα ζικρ"},
     "color": "#14B8A6", "icon": "📿", "coins_reward": 3, "placement": ["main", "duas", "stories"],
     "target_route": "/tasbeeh"},

    {"id": "sp_sadaqah_daily", "category": "reminder", "emoji": "💝",
     "title": {"ar": "صدقتك اليومية", "en": "Your Daily Sadaqah", "de": "Deine tägliche Sadaqa", "fr": "Ton Sadaqah quotidien", "tr": "Günlük Sadakan", "ru": "Твоя ежедневная садака", "sv": "Din dagliga Sadaqah", "nl": "Je dagelijkse Sadaqah", "el": "Η ημερήσια Σαντάκα σου"},
     "desc": {"ar": "تبسمك في وجه أخيك صدقة — حديث نبوي", "en": "Your smile to your brother is charity — Hadith", "de": "Dein Lächeln zu deinem Bruder ist Sadaqa", "fr": "Ton sourire à ton frère est une aumône", "tr": "Kardeşine gülümsemen sadakadır — Hadis", "ru": "Твоя улыбка брату — садака — Хадис", "sv": "Ditt leende till din broder är välgörenhet", "nl": "Je glimlach naar je broeder is liefdadigheid", "el": "Το χαμόγελό σου είναι φιλανθρωπία"},
     "cta": {"ar": "تصدق اليوم", "en": "Give Today", "de": "Heute spenden", "fr": "Donne aujourd'hui", "tr": "Bugün sadaka ver", "ru": "Пожертвуй сегодня", "sv": "Ge idag", "nl": "Geef vandaag", "el": "Δώσε σήμερα"},
     "color": "#F43F5E", "icon": "💝", "coins_reward": 3, "placement": ["main", "stories"],
     "target_route": "/donations"},
]


# ═══ API ENDPOINTS ═══

@router.get("/ads/content")
async def get_sponsored_content(placement: str = "main", locale: str = "ar", limit: int = 3):
    """Get sponsored content for a specific page placement."""
    lang = locale if locale in ["ar", "en", "de", "de-AT", "fr", "tr", "ru", "sv", "nl", "el"] else "en"
    if lang == "de-AT":
        lang = "de"

    # Filter by placement
    available = [c for c in SPONSORED_CONTENT if placement in c["placement"]]
    if not available:
        available = SPONSORED_CONTENT

    # Randomize and limit
    selected = random.sample(available, min(limit, len(available)))

    result = []
    for item in selected:
        result.append({
            "id": item["id"],
            "category": item["category"],
            "emoji": item["emoji"],
            "icon": item["icon"],
            "title": item["title"].get(lang, item["title"]["en"]),
            "description": item["desc"].get(lang, item["desc"]["en"]),
            "cta": item["cta"].get(lang, item["cta"]["en"]),
            "color": item["color"],
            "coins_reward": item["coins_reward"],
            "target_route": item.get("target_route", ""),
        })

    return {"success": True, "ads": result, "total": len(result)}


@router.post("/ads/click/{ad_id}")
async def track_ad_click(ad_id: str, user_id: str = "guest"):
    """Track when a user clicks/interacts with sponsored content. Awards coins."""
    ad = next((c for c in SPONSORED_CONTENT if c["id"] == ad_id), None)
    coins = ad["coins_reward"] if ad else 3

    # Award coins to user wallet
    wallet = await db.baraka_wallets.find_one({"user_id": user_id})
    if wallet:
        await db.baraka_wallets.update_one(
            {"user_id": user_id},
            {"$inc": {"blessing_coins": coins, "total_earned_coins": coins}}
        )

    # Log the click
    await db.ad_clicks.insert_one({
        "_id": str(uuid.uuid4()),
        "ad_id": ad_id,
        "user_id": user_id,
        "coins_awarded": coins,
        "created_at": datetime.utcnow().isoformat(),
    })

    return {"success": True, "coins_awarded": coins, "ad_id": ad_id}


@router.get("/ads/stats")
async def get_ad_stats():
    """Get ad performance statistics."""
    total_clicks = await db.ad_clicks.count_documents({})
    total_coins = 0
    async for doc in db.ad_clicks.find({}, {"coins_awarded": 1}):
        total_coins += doc.get("coins_awarded", 0)

    return {
        "success": True,
        "total_clicks": total_clicks,
        "total_coins_awarded": total_coins,
        "total_ads_available": len(SPONSORED_CONTENT),
    }

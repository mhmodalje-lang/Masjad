#!/usr/bin/env python3
"""
Comprehensive translation key update script.
Adds all missing translation keys for complete i18n coverage.
"""
import json
import os

LOCALES_DIR = "/app/frontend/src/locales"

# New keys to add for COMPLETE translation coverage
NEW_KEYS = {
    # ============== RUQYAH PAGE ==============
    "ruqyahPageTitle": {
        "ar": "العلاج بالرقية الشرعية",
        "en": "Ruqyah Shariah Treatment",
        "de": "Ruqyah Scharia Behandlung",
        "fr": "Traitement par la Roqya Légale",
        "ru": "Лечение Рукъей по Шариату",
        "tr": "Rukye Tedavisi"
    },
    "ruqyahPageSubtitle": {
        "ar": "رقية شرعية من القرآن والسنة",
        "en": "Ruqyah from the Quran and Sunnah",
        "de": "Ruqyah aus Quran und Sunnah",
        "fr": "Roqya du Coran et de la Sunna",
        "ru": "Рукъя из Корана и Сунны",
        "tr": "Kur'an ve Sünnetten Rukye"
    },
    "ruqyahCatAll": {
        "ar": "الكل", "en": "All", "de": "Alle", "fr": "Tout", "ru": "Все", "tr": "Tümü"
    },
    "ruqyahCatGeneral": {
        "ar": "عام", "en": "General", "de": "Allgemein", "fr": "Général", "ru": "Общее", "tr": "Genel"
    },
    "ruqyahCatEye": {
        "ar": "عين", "en": "Evil Eye", "de": "Böser Blick", "fr": "Mauvais œil", "ru": "Сглаз", "tr": "Nazar"
    },
    "ruqyahCatEnvy": {
        "ar": "حسد", "en": "Envy", "de": "Neid", "fr": "Envie", "ru": "Зависть", "tr": "Haset"
    },
    "ruqyahCatMagic": {
        "ar": "سحر", "en": "Magic", "de": "Magie", "fr": "Sorcellerie", "ru": "Колдовство", "tr": "Büyü"
    },
    "ruqyahCatTouch": {
        "ar": "مس", "en": "Jinn Touch", "de": "Dschinn-Berührung", "fr": "Toucher des Djinns", "ru": "Джинны", "tr": "Cin Dokunması"
    },
    "ruqyahCatInsomnia": {
        "ar": "أرق", "en": "Insomnia", "de": "Schlaflosigkeit", "fr": "Insomnie", "ru": "Бессонница", "tr": "Uykusuzluk"
    },
    "ruqyahCatWhispers": {
        "ar": "وسواس", "en": "Whispers", "de": "Einflüsterungen", "fr": "Chuchotements", "ru": "Наваждения", "tr": "Vesvese"
    },
    "ruqyahCatProtection": {
        "ar": "حماية", "en": "Protection", "de": "Schutz", "fr": "Protection", "ru": "Защита", "tr": "Koruma"
    },
    "ruqyahAyatKursiTitle": {
        "ar": "آية الكرسي", "en": "Ayat al-Kursi", "de": "Ayat al-Kursi", "fr": "Ayat al-Kursi", "ru": "Аят аль-Курси", "tr": "Ayetel Kürsi"
    },
    "ruqyahAyatKursiSubtitle": {
        "ar": "للحفظ والحماية", "en": "For preservation and protection", "de": "Zum Schutz und Bewahrung", "fr": "Pour la préservation et la protection", "ru": "Для сохранения и защиты", "tr": "Koruma ve muhafaza için"
    },
    "ruqyahFalaqTitle": {
        "ar": "سورة الفلق", "en": "Surah Al-Falaq", "de": "Sure Al-Falaq", "fr": "Sourate Al-Falaq", "ru": "Сура Аль-Фаляк", "tr": "Felak Suresi"
    },
    "ruqyahFalaqSubtitle": {
        "ar": "من شر ما خلق", "en": "From the evil of what He created", "de": "Vor dem Übel seiner Schöpfung", "fr": "Du mal de ce qu'Il a créé", "ru": "От зла того, что Он сотворил", "tr": "Yarattığı şeylerin şerrinden"
    },
    "ruqyahNasTitle": {
        "ar": "سورة الناس", "en": "Surah An-Nas", "de": "Sure An-Nas", "fr": "Sourate An-Nas", "ru": "Сура Ан-Нас", "tr": "Nas Suresi"
    },
    "ruqyahNasSubtitle": {
        "ar": "من شر الوسواس", "en": "From the evil of the whisperer", "de": "Vor dem Übel des Einflüsterers", "fr": "Du mal du chuchoteur", "ru": "От зла наущающего", "tr": "Vesvesecinin şerrinden"
    },
    "ruqyahIkhlasTitle": {
        "ar": "سورة الإخلاص", "en": "Surah Al-Ikhlas", "de": "Sure Al-Ikhlas", "fr": "Sourate Al-Ikhlas", "ru": "Сура Аль-Ихляс", "tr": "İhlas Suresi"
    },
    "ruqyahIkhlasSubtitle": {
        "ar": "تعدل ثلث القرآن", "en": "Equals one-third of the Quran", "de": "Entspricht einem Drittel des Quran", "fr": "Équivaut à un tiers du Coran", "ru": "Равна трети Корана", "tr": "Kur'an'ın üçte birine denk"
    },
    "ruqyahHomeProtTitle": {
        "ar": "حماية المنزل", "en": "Home Protection", "de": "Schutz des Hauses", "fr": "Protection de la maison", "ru": "Защита дома", "tr": "Ev Koruması"
    },
    "ruqyahHomeProtSubtitle": {
        "ar": "من الجن والشياطين", "en": "From jinn and devils", "de": "Vor Dschinn und Teufel", "fr": "Des djinns et des diables", "ru": "От джиннов и шайтанов", "tr": "Cin ve şeytanlardan"
    },
    "ruqyahRefBaqara255": {
        "ar": "البقرة: 255", "en": "Al-Baqarah: 255", "de": "Al-Baqara: 255", "fr": "Al-Baqara: 255", "ru": "Аль-Бакара: 255", "tr": "Bakara: 255"
    },
    "ruqyahRefFalaq": {
        "ar": "الفلق: 1-5", "en": "Al-Falaq: 1-5", "de": "Al-Falaq: 1-5", "fr": "Al-Falaq: 1-5", "ru": "Аль-Фаляк: 1-5", "tr": "Felak: 1-5"
    },
    "ruqyahRefNas": {
        "ar": "الناس: 1-6", "en": "An-Nas: 1-6", "de": "An-Nas: 1-6", "fr": "An-Nas: 1-6", "ru": "Ан-Нас: 1-6", "tr": "Nas: 1-6"
    },
    "ruqyahRefIkhlas": {
        "ar": "الإخلاص: 1-4", "en": "Al-Ikhlas: 1-4", "de": "Al-Ikhlas: 1-4", "fr": "Al-Ikhlas: 1-4", "ru": "Аль-Ихляс: 1-4", "tr": "İhlas: 1-4"
    },
    "ruqyahRefSahihHadith": {
        "ar": "حديث صحيح", "en": "Authentic Hadith", "de": "Sahih-Hadith", "fr": "Hadith authentique", "ru": "Достоверный хадис", "tr": "Sahih Hadis"
    },
    "ruqyahReadThrice": {
        "ar": "(تُقرأ ثلاث مرات صباحاً ومساءً)", "en": "(Read three times in the morning and evening)", "de": "(Morgens und abends dreimal lesen)", "fr": "(À lire trois fois matin et soir)", "ru": "(Читать три раза утром и вечером)", "tr": "(Sabah ve akşam üç kez okunur)"
    },
    "closeBtn": {
        "ar": "اغلاق", "en": "Close", "de": "Schließen", "fr": "Fermer", "ru": "Закрыть", "tr": "Kapat"
    },
    "noRuqyahInCategory": {
        "ar": "لا توجد رقية في هذا التصنيف", "en": "No ruqyah in this category", "de": "Keine Ruqyah in dieser Kategorie", "fr": "Pas de roqya dans cette catégorie", "ru": "Нет рукъи в этой категории", "tr": "Bu kategoride rukye yok"
    },

    # ============== DAILY DUAS PAGE ==============
    "morningAdhkarTitle": {
        "ar": "أذكار الصباح والخروج", "en": "Morning & Going Out Adhkar", "de": "Morgen- & Ausgangsgebete", "fr": "Adhkar du matin et de sortie", "ru": "Утренние азкары", "tr": "Sabah ve Dışarı Çıkma Zikirleri"
    },
    "morningAdhkarSubtitle": {
        "ar": "ابدأ يومك بذكر الله", "en": "Start your day remembering Allah", "de": "Beginne deinen Tag mit dem Gedenken Allahs", "fr": "Commencez votre journée en invoquant Allah", "ru": "Начните день с поминания Аллаха", "tr": "Gününüze Allah'ı anarak başlayın"
    },
    "middayDuasTitle": {
        "ar": "أدعية ومناجاة", "en": "Duas & Supplications", "de": "Bittgebete & Anrufungen", "fr": "Duas et supplications", "ru": "Дуа и мольбы", "tr": "Dualar ve Yakarışlar"
    },
    "middayDuasSubtitle": {
        "ar": "دعاء للوالدين والتسبيح والاستغفار", "en": "Dua for parents, glorification, and forgiveness", "de": "Bittgebet für Eltern, Lobpreisung und Vergebung", "fr": "Dua pour les parents, glorification et pardon", "ru": "Дуа за родителей, тасбих и истигфар", "tr": "Anne-baba duası, tesbih ve istiğfar"
    },
    "eveningQuranTitle": {
        "ar": "وقت القرآن", "en": "Quran Time", "de": "Quran-Zeit", "fr": "Temps du Coran", "ru": "Время Корана", "tr": "Kur'an Zamanı"
    },
    "eveningQuranSubtitle": {
        "ar": "تعال نقرأ القرآن ونتدبر", "en": "Come read and reflect on the Quran", "de": "Komm, lass uns den Quran lesen und nachdenken", "fr": "Venez lire et méditer le Coran", "ru": "Давайте читать и размышлять над Кораном", "tr": "Gel Kur'an okuyalım ve düşünelim"
    },
    "bedtimeAdhkarTitle": {
        "ar": "أذكار قبل النوم", "en": "Bedtime Adhkar", "de": "Schlafenszeit-Gebete", "fr": "Adhkar avant le coucher", "ru": "Азкары перед сном", "tr": "Uyku Öncesi Zikirleri"
    },
    "bedtimeAdhkarSubtitle": {
        "ar": "حصّن نفسك قبل النوم", "en": "Fortify yourself before sleep", "de": "Schütze dich vor dem Schlafen", "fr": "Fortifiez-vous avant de dormir", "ru": "Защитите себя перед сном", "tr": "Uyumadan önce kendinizi koruyun"
    },
    "favorites": {
        "ar": "المفضلة", "en": "Favorites", "de": "Favoriten", "fr": "Favoris", "ru": "Избранное", "tr": "Favoriler"
    },
    "yourSavedDuas": {
        "ar": "أدعيتك المحفوظة", "en": "Your saved duas", "de": "Deine gespeicherten Bittgebete", "fr": "Vos duas sauvegardées", "ru": "Ваши сохранённые дуа", "tr": "Kaydedilen dualarınız"
    },
    "aiSelectedDuas": {
        "ar": "أدعية مُختارة لك اليوم بالذكاء الاصطناعي ✨", "en": "AI-selected duas for you today ✨", "de": "KI-ausgewählte Bittgebete für dich heute ✨", "fr": "Duas sélectionnées par IA pour vous aujourd'hui ✨", "ru": "Дуа, выбранные ИИ для вас сегодня ✨", "tr": "Bugün sizin için yapay zeka tarafından seçilen dualar ✨"
    },
    "youHaveSavedDuas": {
        "ar": "لديك {count} دعاء محفوظ", "en": "You have {count} saved duas", "de": "Du hast {count} gespeicherte Bittgebete", "fr": "Vous avez {count} duas sauvegardées", "ru": "У вас {count} сохранённых дуа", "tr": "{count} kayıtlı duanız var"
    },
    "noSavedDuasYet": {
        "ar": "لم تحفظ أي دعاء بعد", "en": "You haven't saved any duas yet", "de": "Du hast noch keine Bittgebete gespeichert", "fr": "Vous n'avez pas encore sauvegardé de duas", "ru": "Вы ещё не сохранили дуа", "tr": "Henüz dua kaydetmediniz"
    },
    "loadingAdhkar": {
        "ar": "جارٍ تحضير أذكارك...", "en": "Preparing your adhkar...", "de": "Deine Adhkar werden vorbereitet...", "fr": "Préparation de vos adhkar...", "ru": "Подготовка ваших азкаров...", "tr": "Zikirlerin hazırlanıyor..."
    },
    "tapToSaveFavorites": {
        "ar": "اضغط على ❤️ لحفظ أدعيتك المفضلة", "en": "Tap ❤️ to save your favorite duas", "de": "Tippe auf ❤️ um deine Lieblings-Bittgebete zu speichern", "fr": "Appuyez sur ❤️ pour sauvegarder vos duas préférées", "ru": "Нажмите ❤️ чтобы сохранить избранные дуа", "tr": "Favori dualarınızı kaydetmek için ❤️'e dokunun"
    },
    "backToAdhkar": {
        "ar": "العودة للأذكار", "en": "Back to Adhkar", "de": "Zurück zu den Adhkar", "fr": "Retour aux Adhkar", "ru": "Назад к азкарам", "tr": "Zikirlere Dön"
    },
    "newDuas": {
        "ar": "أدعية جديدة", "en": "New Duas", "de": "Neue Bittgebete", "fr": "Nouvelles Duas", "ru": "Новые дуа", "tr": "Yeni Dualar"
    },
    "openQuran": {
        "ar": "افتح القرآن الكريم", "en": "Open the Holy Quran", "de": "Öffne den Heiligen Quran", "fr": "Ouvrir le Saint Coran", "ru": "Открыть Священный Коран", "tr": "Kur'an-ı Kerim'i Aç"
    },

    # ============== PRAYER TRACKER ==============
    "trackYourDailyPrayers": {
        "ar": "تابع صلواتك اليومية", "en": "Track your daily prayers", "de": "Verfolge deine täglichen Gebete", "fr": "Suivez vos prières quotidiennes", "ru": "Отслеживайте ваши ежедневные молитвы", "tr": "Günlük namazlarınızı takip edin"
    },
    "todayProgress": {
        "ar": "تقدم اليوم", "en": "Today's Progress", "de": "Fortschritt heute", "fr": "Progrès d'aujourd'hui", "ru": "Прогресс за сегодня", "tr": "Bugünün İlerlemesi"
    },
    "todayPrayers": {
        "ar": "صلوات اليوم", "en": "Today's Prayers", "de": "Heutige Gebete", "fr": "Prières d'aujourd'hui", "ru": "Молитвы сегодня", "tr": "Bugünün Namazları"
    },

    # ============== QURAN GOAL ==============
    "setQuranGoalTitle": {
        "ar": "حدّد هدف القرآن", "en": "Set Quran Goal", "de": "Quran-Ziel setzen", "fr": "Définir l'objectif du Coran", "ru": "Установить цель Корана", "tr": "Kur'an Hedefi Belirle"
    },
    "howMuchQuranDaily": {
        "ar": "كم من الوقت تريد قراءة القرآن يومياً؟", "en": "How much time do you want to read Quran daily?", "de": "Wie viel Zeit möchtest du täglich den Quran lesen?", "fr": "Combien de temps voulez-vous lire le Coran quotidiennement?", "ru": "Сколько времени вы хотите читать Коран ежедневно?", "tr": "Günde ne kadar Kur'an okumak istiyorsunuz?"
    },
    "5minutes": {
        "ar": "5 دقائق", "en": "5 minutes", "de": "5 Minuten", "fr": "5 minutes", "ru": "5 минут", "tr": "5 dakika"
    },
    "10minutes": {
        "ar": "10 دقائق", "en": "10 minutes", "de": "10 Minuten", "fr": "10 minutes", "ru": "10 минут", "tr": "10 dakika"
    },
    "20minutes": {
        "ar": "20 دقيقة", "en": "20 minutes", "de": "20 Minuten", "fr": "20 minutes", "ru": "20 минут", "tr": "20 dakika"
    },
    "30minutes": {
        "ar": "30 دقيقة", "en": "30 minutes", "de": "30 Minuten", "fr": "30 minutes", "ru": "30 минут", "tr": "30 dakika"
    },
    "1hour": {
        "ar": "ساعة", "en": "1 hour", "de": "1 Stunde", "fr": "1 heure", "ru": "1 час", "tr": "1 saat"
    },
    "dailyReminder": {
        "ar": "تذكير يومي", "en": "Daily Reminder", "de": "Tägliche Erinnerung", "fr": "Rappel quotidien", "ru": "Ежедневное напоминание", "tr": "Günlük Hatırlatma"
    },
    "createGoal": {
        "ar": "أنشئ هدفاً", "en": "Create Goal", "de": "Ziel erstellen", "fr": "Créer un objectif", "ru": "Создать цель", "tr": "Hedef Oluştur"
    },
    "quranGoalSaved": {
        "ar": "تم حفظ هدف القرآن ✅", "en": "Quran goal saved ✅", "de": "Quran-Ziel gespeichert ✅", "fr": "Objectif du Coran sauvegardé ✅", "ru": "Цель Корана сохранена ✅", "tr": "Kur'an hedefi kaydedildi ✅"
    },
    "minutesDaily": {
        "ar": "{count} دقيقة يومياً", "en": "{count} minutes daily", "de": "{count} Minuten täglich", "fr": "{count} minutes par jour", "ru": "{count} минут ежедневно", "tr": "Günlük {count} dakika"
    },

    # ============== DHIKR SETTINGS ==============
    "setDailyAdhkar": {
        "ar": "حدد الأذكار اليومية", "en": "Set Daily Adhkar", "de": "Tägliche Adhkar einstellen", "fr": "Définir les Adhkar quotidiens", "ru": "Установить ежедневные азкары", "tr": "Günlük Zikirleri Belirle"
    },
    "adhkarSettingsSaved": {
        "ar": "تم حفظ إعدادات الأذكار ✅", "en": "Adhkar settings saved ✅", "de": "Adhkar-Einstellungen gespeichert ✅", "fr": "Paramètres Adhkar sauvegardés ✅", "ru": "Настройки азкаров сохранены ✅", "tr": "Zikir ayarları kaydedildi ✅"
    },
    "saveSettings": {
        "ar": "حفظ الإعدادات", "en": "Save Settings", "de": "Einstellungen speichern", "fr": "Sauvegarder les paramètres", "ru": "Сохранить настройки", "tr": "Ayarları Kaydet"
    },

    # ============== REWARDS PAGE ==============
    "rewardsTitle": {
        "ar": "المكافآت", "en": "Rewards", "de": "Belohnungen", "fr": "Récompenses", "ru": "Награды", "tr": "Ödüller"
    },
    "dailyLogin": {
        "ar": "تسجيل يومي", "en": "Daily Login", "de": "Tägliche Anmeldung", "fr": "Connexion quotidienne", "ru": "Ежедневный вход", "tr": "Günlük Giriş"
    },
    "dailyLoginDesc": {
        "ar": "سجّل دخولك يومياً واحصل على مكافأة", "en": "Log in daily and earn a reward", "de": "Melde dich täglich an und verdiene eine Belohnung", "fr": "Connectez-vous quotidiennement et gagnez une récompense", "ru": "Входите ежедневно и получайте награду", "tr": "Her gün giriş yapın ve ödül kazanın"
    },
    "tasbeeh100": {
        "ar": "تسبيح 100", "en": "Tasbeeh 100", "de": "Tasbih 100", "fr": "Tasbih 100", "ru": "Тасбих 100", "tr": "Tesbih 100"
    },
    "tasbeeh100Desc": {
        "ar": "أكمل 100 تسبيحة", "en": "Complete 100 tasbeehs", "de": "100 Tasbih vervollständigen", "fr": "Complétez 100 tasbihs", "ru": "Выполните 100 тасбихов", "tr": "100 tesbih tamamlayın"
    },
    "quranPageReward": {
        "ar": "صفحة قرآن", "en": "Quran Page", "de": "Quran-Seite", "fr": "Page du Coran", "ru": "Страница Корана", "tr": "Kur'an Sayfası"
    },
    "quranPageRewardDesc": {
        "ar": "اقرأ صفحة من القرآن", "en": "Read a page from the Quran", "de": "Lies eine Seite des Quran", "fr": "Lisez une page du Coran", "ru": "Прочитайте страницу Корана", "tr": "Kur'an'dan bir sayfa okuyun"
    },
    "mustLogin": {
        "ar": "يجب تسجيل الدخول", "en": "You must log in", "de": "Du musst dich anmelden", "fr": "Vous devez vous connecter", "ru": "Необходимо войти", "tr": "Giriş yapmalısınız"
    },
    "errorOccurred": {
        "ar": "حدث خطأ", "en": "An error occurred", "de": "Ein Fehler ist aufgetreten", "fr": "Une erreur est survenue", "ru": "Произошла ошибка", "tr": "Bir hata oluştu"
    },
    "loginToCollect": {
        "ar": "سجّل دخولك لجمع الذهب", "en": "Log in to collect gold", "de": "Melde dich an, um Gold zu sammeln", "fr": "Connectez-vous pour collecter de l'or", "ru": "Войдите, чтобы собирать золото", "tr": "Altın toplamak için giriş yapın"
    },
    "loginBtn": {
        "ar": "تسجيل الدخول", "en": "Log In", "de": "Anmelden", "fr": "Se connecter", "ru": "Войти", "tr": "Giriş Yap"
    },
    "yourBalance": {
        "ar": "رصيدك", "en": "Your Balance", "de": "Dein Guthaben", "fr": "Votre solde", "ru": "Ваш баланс", "tr": "Bakiyeniz"
    },
    "streakDays": {
        "ar": "سلسلة أيام", "en": "Day Streak", "de": "Tagesserie", "fr": "Jours consécutifs", "ru": "Серия дней", "tr": "Gün Serisi"
    },
    "totalEarned": {
        "ar": "إجمالي", "en": "Total", "de": "Gesamt", "fr": "Total", "ru": "Всего", "tr": "Toplam"
    },
    "collectRewards": {
        "ar": "اجمع المكافآت", "en": "Collect Rewards", "de": "Belohnungen sammeln", "fr": "Collecter les récompenses", "ru": "Собрать награды", "tr": "Ödülleri Topla"
    },
    "claimBtn": {
        "ar": "استلم", "en": "Claim", "de": "Abholen", "fr": "Réclamer", "ru": "Получить", "tr": "Al"
    },
    "storeBtn": {
        "ar": "المتجر", "en": "Store", "de": "Laden", "fr": "Boutique", "ru": "Магазин", "tr": "Mağaza"
    },
    "buyWithGold": {
        "ar": "اشترِ عناصر مميزة بالذهب", "en": "Buy premium items with gold", "de": "Kaufe Premium-Artikel mit Gold", "fr": "Achetez des articles premium avec de l'or", "ru": "Купите премиум предметы за золото", "tr": "Altınla premium öğeler satın alın"
    },
    "logTitle": {
        "ar": "السجل", "en": "Log", "de": "Protokoll", "fr": "Journal", "ru": "Журнал", "tr": "Kayıt"
    },
    "noTransactionsYet": {
        "ar": "لا توجد معاملات بعد", "en": "No transactions yet", "de": "Noch keine Transaktionen", "fr": "Pas encore de transactions", "ru": "Пока нет транзакций", "tr": "Henüz işlem yok"
    },

    # ============== STORE PAGE ==============
    "storeTitle": {
        "ar": "المتجر", "en": "Store", "de": "Laden", "fr": "Boutique", "ru": "Магазин", "tr": "Mağaza"
    },
    "storePremiumItems": {
        "ar": "اقتنِ عناصر مميزة بالذهب", "en": "Get premium items with gold", "de": "Erhalte Premium-Artikel mit Gold", "fr": "Obtenez des articles premium avec de l'or", "ru": "Получите премиум предметы за золото", "tr": "Altınla premium öğeler edinin"
    },
    "storeCatAll": {
        "ar": "الكل", "en": "All", "de": "Alle", "fr": "Tout", "ru": "Все", "tr": "Tümü"
    },
    "storeCatFrame": {
        "ar": "إطارات", "en": "Frames", "de": "Rahmen", "fr": "Cadres", "ru": "Рамки", "tr": "Çerçeveler"
    },
    "storeCatTheme": {
        "ar": "خلفيات", "en": "Themes", "de": "Hintergründe", "fr": "Thèmes", "ru": "Темы", "tr": "Temalar"
    },
    "storeCatBadge": {
        "ar": "شارات", "en": "Badges", "de": "Abzeichen", "fr": "Badges", "ru": "Значки", "tr": "Rozetler"
    },
    "storeCatEffect": {
        "ar": "تأثيرات", "en": "Effects", "de": "Effekte", "fr": "Effets", "ru": "Эффекты", "tr": "Efektler"
    },
    "storeCatMembership": {
        "ar": "عضويات", "en": "Memberships", "de": "Mitgliedschaften", "fr": "Adhésions", "ru": "Подписки", "tr": "Üyelikler"
    },
    "storeCatCharity": {
        "ar": "صدقات", "en": "Charity", "de": "Wohltätigkeit", "fr": "Charité", "ru": "Благотворительность", "tr": "Sadaka"
    },
    "goldLabel": {
        "ar": "ذهب", "en": "Gold", "de": "Gold", "fr": "Or", "ru": "Золото", "tr": "Altın"
    },
    "ownedLabel": {
        "ar": "مملوك", "en": "Owned", "de": "Im Besitz", "fr": "Possédé", "ru": "Куплено", "tr": "Sahip"
    },
    "insufficientGold": {
        "ar": "غير كافٍ", "en": "Insufficient", "de": "Unzureichend", "fr": "Insuffisant", "ru": "Недостаточно", "tr": "Yetersiz"
    },
    "buyBtn": {
        "ar": "شراء", "en": "Buy", "de": "Kaufen", "fr": "Acheter", "ru": "Купить", "tr": "Satın Al"
    },
    "insufficientGoldMsg": {
        "ar": "رصيد الذهب غير كافٍ", "en": "Insufficient gold balance", "de": "Nicht genügend Gold", "fr": "Solde d'or insuffisant", "ru": "Недостаточно золота", "tr": "Yetersiz altın bakiyesi"
    },
    "purchaseFailed": {
        "ar": "فشل الشراء", "en": "Purchase failed", "de": "Kauf fehlgeschlagen", "fr": "Achat échoué", "ru": "Покупка не удалась", "tr": "Satın alma başarısız"
    },

    # ============== DONATIONS PAGE ==============
    "donationsTitle": {
        "ar": "التبرعات", "en": "Donations", "de": "Spenden", "fr": "Dons", "ru": "Пожертвования", "tr": "Bağışlar"
    },
    "requestHelp": {
        "ar": "طلب مساعدة", "en": "Request Help", "de": "Hilfe anfordern", "fr": "Demander de l'aide", "ru": "Запросить помощь", "tr": "Yardım İste"
    },
    "importantNotice": {
        "ar": "تنبيه مهم", "en": "Important Notice", "de": "Wichtiger Hinweis", "fr": "Avis important", "ru": "Важное уведомление", "tr": "Önemli Uyarı"
    },
    "donationsDisclaimer": {
        "ar": "نحن فقط وسيلة لإيصالكم لبعض. لا نتحمل أي مسؤولية عن المعاملات بين الأطراف. فقط ادعو لوالدَيّ بالرحمة والمغفرة.", 
        "en": "We are only a platform to connect people. We bear no responsibility for transactions between parties. Please pray for our parents' mercy and forgiveness.",
        "de": "Wir sind nur eine Plattform, um Menschen zu verbinden. Wir übernehmen keine Verantwortung für Transaktionen zwischen den Parteien.",
        "fr": "Nous ne sommes qu'une plateforme pour connecter les gens. Nous n'assumons aucune responsabilité pour les transactions entre les parties.",
        "ru": "Мы лишь платформа для связи людей. Мы не несём ответственности за сделки между сторонами.",
        "tr": "Biz sadece insanları birbirine bağlayan bir platformuz. Taraflar arasındaki işlemlerden sorumlu değiliz."
    },
    "noRequestsNow": {
        "ar": "لا توجد طلبات حالياً", "en": "No requests at the moment", "de": "Derzeit keine Anfragen", "fr": "Aucune demande pour le moment", "ru": "Нет запросов в данный момент", "tr": "Şu anda istek yok"
    },
    "beFirstToPost": {
        "ar": "كن أول من ينشر طلب مساعدة", "en": "Be the first to post a help request", "de": "Sei der Erste, der eine Hilfeanfrage postet", "fr": "Soyez le premier à poster une demande d'aide", "ru": "Будьте первым, кто опубликует запрос о помощи", "tr": "İlk yardım isteğini paylaşan siz olun"
    },
    "anonymous": {
        "ar": "مجهول", "en": "Anonymous", "de": "Anonym", "fr": "Anonyme", "ru": "Аноним", "tr": "Anonim"
    },
    "amountNeeded": {
        "ar": "المبلغ المطلوب", "en": "Amount needed", "de": "Benötigter Betrag", "fr": "Montant nécessaire", "ru": "Необходимая сумма", "tr": "Gereken miktar"
    },
    "contactInfo": {
        "ar": "تواصل", "en": "Contact", "de": "Kontakt", "fr": "Contact", "ru": "Контакт", "tr": "İletişim"
    },
    "fillAllFields": {
        "ar": "يرجى ملء جميع الحقول", "en": "Please fill all fields", "de": "Bitte fülle alle Felder aus", "fr": "Veuillez remplir tous les champs", "ru": "Пожалуйста, заполните все поля", "tr": "Lütfen tüm alanları doldurun"
    },
    "requestPublished": {
        "ar": "تم نشر طلبك", "en": "Your request has been published", "de": "Deine Anfrage wurde veröffentlicht", "fr": "Votre demande a été publiée", "ru": "Ваш запрос опубликован", "tr": "İsteğiniz yayınlandı"
    },
    "cancelBtn": {
        "ar": "إلغاء", "en": "Cancel", "de": "Abbrechen", "fr": "Annuler", "ru": "Отмена", "tr": "İptal"
    },
    "publishBtn": {
        "ar": "نشر", "en": "Publish", "de": "Veröffentlichen", "fr": "Publier", "ru": "Опубликовать", "tr": "Yayınla"
    },
    "requestTitlePlaceholder": {
        "ar": "عنوان الطلب *", "en": "Request title *", "de": "Anfragetitel *", "fr": "Titre de la demande *", "ru": "Заголовок запроса *", "tr": "İstek başlığı *"
    },
    "requestDescPlaceholder": {
        "ar": "وصف الحالة *", "en": "Describe the case *", "de": "Beschreibe den Fall *", "fr": "Décrivez le cas *", "ru": "Опишите ситуацию *", "tr": "Durumu açıklayın *"
    },
    "contactInfoPlaceholder": {
        "ar": "معلومات التواصل (بريد أو رقم) *", "en": "Contact info (email or phone) *", "de": "Kontaktinfo (E-Mail oder Telefon) *", "fr": "Coordonnées (email ou téléphone) *", "ru": "Контакты (email или телефон) *", "tr": "İletişim bilgisi (e-posta veya telefon) *"
    },
    "amountPlaceholder": {
        "ar": "المبلغ المطلوب (اختياري)", "en": "Amount needed (optional)", "de": "Benötigter Betrag (optional)", "fr": "Montant nécessaire (optionnel)", "ru": "Необходимая сумма (необязательно)", "tr": "Gereken miktar (isteğe bağlı)"
    },

    # ============== AI ASSISTANT ==============
    "aiAssistantTitle": {
        "ar": "المساعد الإسلامي", "en": "Islamic Assistant", "de": "Islamischer Assistent", "fr": "Assistant Islamique", "ru": "Исламский помощник", "tr": "İslami Asistan"
    },
    "aiAssistantDesc": {
        "ar": "مساعد ذكي مدعوم بـ GPT-5.2 متخصص في الأسئلة الإسلامية", "en": "AI assistant powered by GPT-5.2 specialized in Islamic questions", "de": "KI-Assistent mit GPT-5.2 für islamische Fragen", "fr": "Assistant IA alimenté par GPT-5.2 spécialisé dans les questions islamiques", "ru": "ИИ-помощник на GPT-5.2, специализирующийся на исламских вопросах", "tr": "İslami sorularda uzmanlaşmış GPT-5.2 destekli yapay zeka asistanı"
    },
    "poweredByGPT": {
        "ar": "مدعوم بـ GPT-5.2", "en": "Powered by GPT-5.2", "de": "Betrieben von GPT-5.2", "fr": "Propulsé par GPT-5.2", "ru": "Работает на GPT-5.2", "tr": "GPT-5.2 ile desteklenmektedir"
    },
    "freeRemaining": {
        "ar": "{count} مجاني", "en": "{count} free", "de": "{count} kostenlos", "fr": "{count} gratuit", "ru": "{count} бесплатно", "tr": "{count} ücretsiz"
    },
    "perQuestion": {
        "ar": "5/سؤال", "en": "5/question", "de": "5/Frage", "fr": "5/question", "ru": "5/вопрос", "tr": "5/soru"
    },
    "remainingLabel": {
        "ar": "متبقي", "en": "remaining", "de": "verbleibend", "fr": "restant", "ru": "осталось", "tr": "kalan"
    },
    "bismillah": {
        "ar": "بسم الله الرحمن الرحيم", "en": "In the Name of Allah, the Most Gracious, the Most Merciful", "de": "Im Namen Allahs, des Allerbarmers, des Barmherzigen", "fr": "Au Nom d'Allah, le Tout Miséricordieux, le Très Miséricordieux", "ru": "Во имя Аллаха, Милостивого, Милосердного", "tr": "Rahman ve Rahim olan Allah'ın adıyla"
    },
    "askMeAnything": {
        "ar": "اسألني أي سؤال إسلامي", "en": "Ask me any Islamic question", "de": "Stelle mir eine islamische Frage", "fr": "Posez-moi une question islamique", "ru": "Задайте мне любой исламский вопрос", "tr": "Bana herhangi bir İslami soru sorun"
    },
    "loginFirstMsg": {
        "ar": "سجّل دخولك أولاً", "en": "Please log in first", "de": "Bitte melde dich zuerst an", "fr": "Veuillez d'abord vous connecter", "ru": "Пожалуйста, сначала войдите", "tr": "Lütfen önce giriş yapın"
    },
    "connectionError": {
        "ar": "حدث خطأ في الاتصال", "en": "Connection error occurred", "de": "Verbindungsfehler aufgetreten", "fr": "Erreur de connexion", "ru": "Ошибка подключения", "tr": "Bağlantı hatası oluştu"
    },
    "writeYourQuestion": {
        "ar": "اكتب سؤالك الإسلامي...", "en": "Write your Islamic question...", "de": "Schreibe deine islamische Frage...", "fr": "Écrivez votre question islamique...", "ru": "Напишите ваш исламский вопрос...", "tr": "İslami sorunuzu yazın..."
    },
    "watchVideosForPoints": {
        "ar": "شاهد فيديوهات لكسب نقاط مجانية", "en": "Watch videos to earn free points", "de": "Schau Videos, um kostenlose Punkte zu verdienen", "fr": "Regardez des vidéos pour gagner des points gratuits", "ru": "Смотрите видео, чтобы заработать бесплатные очки", "tr": "Ücretsiz puan kazanmak için video izleyin"
    },
    "sampleQ1": {
        "ar": "ما حكم صلاة التراويح؟", "en": "What is the ruling on Taraweeh prayer?", "de": "Was ist das Urteil über das Tarawih-Gebet?", "fr": "Quel est le jugement sur la prière de Tarawih?", "ru": "Каково постановление о молитве Таравих?", "tr": "Teravih namazının hükmü nedir?"
    },
    "sampleQ2": {
        "ar": "كيف أحسب زكاة المال؟", "en": "How to calculate Zakat on wealth?", "de": "Wie berechne ich die Zakat auf Vermögen?", "fr": "Comment calculer la Zakat sur la richesse?", "ru": "Как рассчитать закят на имущество?", "tr": "Mal zekatı nasıl hesaplanır?"
    },
    "sampleQ3": {
        "ar": "ما هي أركان الإسلام؟", "en": "What are the pillars of Islam?", "de": "Was sind die Säulen des Islam?", "fr": "Quels sont les piliers de l'Islam?", "ru": "Каковы столпы Ислама?", "tr": "İslam'ın şartları nelerdir?"
    },
    "sampleQ4": {
        "ar": "دعاء دخول المسجد", "en": "Dua for entering the mosque", "de": "Bittgebet beim Betreten der Moschee", "fr": "Dua pour entrer dans la mosquée", "ru": "Дуа при входе в мечеть", "tr": "Camiye giriş duası"
    },

    # ============== CONTACT US ==============
    "contactUsTitle": {
        "ar": "تواصل معنا", "en": "Contact Us", "de": "Kontaktieren Sie uns", "fr": "Contactez-nous", "ru": "Свяжитесь с нами", "tr": "Bize Ulaşın"
    },
    "emailLabel": {
        "ar": "البريد الإلكتروني", "en": "Email", "de": "E-Mail", "fr": "E-mail", "ru": "Электронная почта", "tr": "E-posta"
    },
    "phoneWhatsapp": {
        "ar": "الهاتف / واتساب", "en": "Phone / WhatsApp", "de": "Telefon / WhatsApp", "fr": "Téléphone / WhatsApp", "ru": "Телефон / WhatsApp", "tr": "Telefon / WhatsApp"
    },
    "directWhatsapp": {
        "ar": "واتساب مباشر", "en": "Direct WhatsApp", "de": "Direkt WhatsApp", "fr": "WhatsApp direct", "ru": "Прямой WhatsApp", "tr": "Doğrudan WhatsApp"
    },
    "instantChat": {
        "ar": "تواصل فوري", "en": "Instant Chat", "de": "Sofortiger Chat", "fr": "Chat instantané", "ru": "Мгновенный чат", "tr": "Anlık Sohbet"
    },
    "sendMessage": {
        "ar": "أرسل رسالة", "en": "Send a Message", "de": "Nachricht senden", "fr": "Envoyer un message", "ru": "Отправить сообщение", "tr": "Mesaj Gönderin"
    },
    "namePlaceholder": {
        "ar": "الاسم *", "en": "Name *", "de": "Name *", "fr": "Nom *", "ru": "Имя *", "tr": "İsim *"
    },
    "emailPlaceholder": {
        "ar": "البريد الإلكتروني", "en": "Email", "de": "E-Mail", "fr": "E-mail", "ru": "Электронная почта", "tr": "E-posta"
    },
    "messagePlaceholder": {
        "ar": "رسالتك *", "en": "Your message *", "de": "Ihre Nachricht *", "fr": "Votre message *", "ru": "Ваше сообщение *", "tr": "Mesajınız *"
    },
    "sendBtn": {
        "ar": "إرسال", "en": "Send", "de": "Senden", "fr": "Envoyer", "ru": "Отправить", "tr": "Gönder"
    },
    "sending": {
        "ar": "جاري الإرسال...", "en": "Sending...", "de": "Wird gesendet...", "fr": "Envoi en cours...", "ru": "Отправка...", "tr": "Gönderiliyor..."
    },
    "messageSentSuccess": {
        "ar": "تم إرسال رسالتك بنجاح! سنرد عليك قريباً", "en": "Your message was sent successfully! We'll reply soon.", "de": "Ihre Nachricht wurde erfolgreich gesendet! Wir antworten bald.", "fr": "Votre message a été envoyé avec succès! Nous vous répondrons bientôt.", "ru": "Ваше сообщение успешно отправлено! Мы скоро ответим.", "tr": "Mesajınız başarıyla gönderildi! En kısa sürede yanıt vereceğiz."
    },
    "sendError": {
        "ar": "خطأ في الإرسال", "en": "Error sending message", "de": "Fehler beim Senden", "fr": "Erreur d'envoi", "ru": "Ошибка отправки", "tr": "Gönderme hatası"
    },
    "fillRequiredFields": {
        "ar": "يرجى ملء الحقول المطلوبة", "en": "Please fill required fields", "de": "Bitte fülle die Pflichtfelder aus", "fr": "Veuillez remplir les champs requis", "ru": "Пожалуйста, заполните обязательные поля", "tr": "Lütfen gerekli alanları doldurun"
    },
    "ownerDeveloper": {
        "ar": "المالك والمطور: محمد الرجب", "en": "Owner & Developer: Muhammad Al-Rajab", "de": "Eigentümer & Entwickler: Muhammad Al-Rajab", "fr": "Propriétaire & Développeur: Muhammad Al-Rajab", "ru": "Владелец и разработчик: Мухаммад Аль-Раджаб", "tr": "Sahibi ve Geliştirici: Muhammed El-Receb"
    },

    # ============== MARKETPLACE ==============
    "marketplaceTitle": {
        "ar": "السوق الإسلامي", "en": "Islamic Marketplace", "de": "Islamischer Marktplatz", "fr": "Marché Islamique", "ru": "Исламский маркетплейс", "tr": "İslami Pazar Yeri"
    },
    "marketplaceSubtitle": {
        "ar": "منتجات إسلامية من حولك", "en": "Islamic products around you", "de": "Islamische Produkte in deiner Nähe", "fr": "Produits islamiques autour de vous", "ru": "Исламские товары рядом с вами", "tr": "Çevrenizdeki İslami ürünler"
    },
    "marketCatAll": {
        "ar": "الكل", "en": "All", "de": "Alle", "fr": "Tout", "ru": "Все", "tr": "Tümü"
    },
    "marketCatClothing": {
        "ar": "ملابس", "en": "Clothing", "de": "Kleidung", "fr": "Vêtements", "ru": "Одежда", "tr": "Giyim"
    },
    "marketCatBooks": {
        "ar": "كتب", "en": "Books", "de": "Bücher", "fr": "Livres", "ru": "Книги", "tr": "Kitaplar"
    },
    "marketCatAccessories": {
        "ar": "إكسسوارات", "en": "Accessories", "de": "Zubehör", "fr": "Accessoires", "ru": "Аксессуары", "tr": "Aksesuarlar"
    },
    "marketCatFood": {
        "ar": "طعام", "en": "Food", "de": "Essen", "fr": "Nourriture", "ru": "Еда", "tr": "Yiyecek"
    },
    "marketCatPerfume": {
        "ar": "عطور", "en": "Perfume", "de": "Parfüm", "fr": "Parfum", "ru": "Парфюмерия", "tr": "Parfüm"
    },
    "marketCatGeneral": {
        "ar": "عام", "en": "General", "de": "Allgemein", "fr": "Général", "ru": "Общее", "tr": "Genel"
    },
    "registerAsVendor": {
        "ar": "تسجيل كبائع", "en": "Register as Vendor", "de": "Als Verkäufer registrieren", "fr": "S'inscrire en tant que vendeur", "ru": "Зарегистрироваться как продавец", "tr": "Satıcı Olarak Kaydol"
    },
    "wantToSell": {
        "ar": "هل تريد بيع منتجاتك؟", "en": "Want to sell your products?", "de": "Möchtest du deine Produkte verkaufen?", "fr": "Vous voulez vendre vos produits?", "ru": "Хотите продавать свои товары?", "tr": "Ürünlerinizi satmak ister misiniz?"
    },
    "registerAndPublish": {
        "ar": "سجّل كبائع وابدأ النشر بعد موافقة الإدارة", "en": "Register as vendor and start publishing after admin approval", "de": "Registriere dich als Verkäufer und veröffentliche nach Admin-Genehmigung", "fr": "Inscrivez-vous comme vendeur et publiez après approbation de l'admin", "ru": "Зарегистрируйтесь как продавец и публикуйте после одобрения администратора", "tr": "Satıcı olarak kaydolun ve yönetici onayından sonra yayınlamaya başlayın"
    },
    "requestUnderReview": {
        "ar": "طلبك قيد المراجعة", "en": "Your request is under review", "de": "Deine Anfrage wird geprüft", "fr": "Votre demande est en cours d'examen", "ru": "Ваш запрос на рассмотрении", "tr": "İsteğiniz inceleniyor"
    },
    "willNotifyApproval": {
        "ar": "سيتم إشعارك عند الموافقة", "en": "You'll be notified upon approval", "de": "Du wirst bei Genehmigung benachrichtigt", "fr": "Vous serez notifié lors de l'approbation", "ru": "Вы будете уведомлены при одобрении", "tr": "Onaylandığında bilgilendirileceksiniz"
    },
    "enterShopName": {
        "ar": "أدخل اسم المتجر", "en": "Enter shop name", "de": "Shopname eingeben", "fr": "Entrez le nom du magasin", "ru": "Введите название магазина", "tr": "Mağaza adını girin"
    },
    "requestSent": {
        "ar": "تم إرسال الطلب", "en": "Request sent", "de": "Anfrage gesendet", "fr": "Demande envoyée", "ru": "Запрос отправлен", "tr": "İstek gönderildi"
    },
    "fillNameAndPrice": {
        "ar": "يجب ملء الاسم والسعر", "en": "Name and price are required", "de": "Name und Preis sind erforderlich", "fr": "Le nom et le prix sont requis", "ru": "Название и цена обязательны", "tr": "İsim ve fiyat gereklidir"
    },
    "productAdded": {
        "ar": "تم إضافة المنتج", "en": "Product added", "de": "Produkt hinzugefügt", "fr": "Produit ajouté", "ru": "Товар добавлен", "tr": "Ürün eklendi"
    },

    # ============== ABOUT US ==============
    "aboutUsTitle": {
        "ar": "من نحن", "en": "About Us", "de": "Über uns", "fr": "À propos", "ru": "О нас", "tr": "Hakkımızda"
    },

    # ============== HADITH MULTILINGUAL (backend keys) ==============
    "hadithNarrator": {
        "ar": "الراوي", "en": "Narrator", "de": "Erzähler", "fr": "Narrateur", "ru": "Рассказчик", "tr": "Ravî"
    },
}

def update_locale(lang_code, new_keys):
    filepath = os.path.join(LOCALES_DIR, f"{lang_code}.json")
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    added = 0
    for key, translations in new_keys.items():
        if key not in data:
            data[key] = translations.get(lang_code, translations.get("en", key))
            added += 1
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return added, len(data)

if __name__ == "__main__":
    languages = ["ar", "en", "de", "fr", "ru", "tr"]
    for lang in languages:
        added, total = update_locale(lang, NEW_KEYS)
        print(f"{lang}: Added {added} keys, Total: {total}")
    print(f"\nTotal new keys defined: {len(NEW_KEYS)}")

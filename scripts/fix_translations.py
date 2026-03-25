#!/usr/bin/env python3
"""
Comprehensive translation fix script for Azan & Hikaya app.
Fixes:
1. 41 missing keys in ar, en, tr, el, ru
2. Arabic text leak in de-AT.json
3. Untranslated values across all language files
4. Ensures all files have identical key sets
"""
import json
import os
import copy

LOCALES_DIR = '/app/frontend/src/locales'

# ============================================================
# PART 1: 41 Missing keys - translations for ar, en, tr, el, ru
# ============================================================
MISSING_KEYS_TRANSLATIONS = {
    "adhanNotification": {
        "ar": "إشعار الأذان",
        "en": "Adhan Notification",
        "tr": "Ezan Bildirimi",
        "el": "Ειδοποίηση Αζάν",
        "ru": "Уведомление об Азане",
        "de": "Adhan-Benachrichtigung",
        "de-AT": "Adhan-Benachrichtigung",
        "fr": "Notification de l'adhan",
        "nl": "Adhan-melding",
        "sv": "Adhan-notifikation"
    },
    "badges": {
        "ar": "الشارات",
        "en": "Badges",
        "tr": "Rozetler",
        "el": "Σήματα",
        "ru": "Значки",
        "de": "Abzeichen",
        "de-AT": "Abzeichen",
        "fr": "Badges",
        "nl": "Badges",
        "sv": "Märken"
    },
    "bestScore": {
        "ar": "أفضل نتيجة",
        "en": "Best Score",
        "tr": "En İyi Skor",
        "el": "Καλύτερη Βαθμολογία",
        "ru": "Лучший результат",
        "de": "Beste Punktzahl",
        "de-AT": "Beste Punktzahl",
        "fr": "Meilleur score",
        "nl": "Beste score",
        "sv": "Bästa poäng"
    },
    "chapterCount": {
        "ar": "الأجزاء",
        "en": "Chapters",
        "tr": "Bölümler",
        "el": "Κεφάλαια",
        "ru": "Главы",
        "de": "Kapitel",
        "de-AT": "Kapitel",
        "fr": "Chapitres",
        "nl": "Hoofdstukken",
        "sv": "Kapitel"
    },
    "chapterIntro": {
        "ar": "مقدمة الفصل",
        "en": "Chapter Introduction",
        "tr": "Bölüm Tanıtımı",
        "el": "Εισαγωγή Κεφαλαίου",
        "ru": "Введение в главу",
        "de": "Kapiteleinführung",
        "de-AT": "Kapiteleinführung",
        "fr": "Introduction du chapitre",
        "nl": "Hoofdstukintroductie",
        "sv": "Kapitelintroduktion"
    },
    "completedLessons": {
        "ar": "الدروس المكتملة",
        "en": "Completed Lessons",
        "tr": "Tamamlanan Dersler",
        "el": "Ολοκληρωμένα Μαθήματα",
        "ru": "Завершённые уроки",
        "de": "Abgeschlossene Lektionen",
        "de-AT": "Abgeschlossene Lektionen",
        "fr": "Leçons terminées",
        "nl": "Voltooide lessen",
        "sv": "Avklarade lektioner"
    },
    "consentHistory": {
        "ar": "سجل الموافقات",
        "en": "Consent History",
        "tr": "Onay Geçmişi",
        "el": "Ιστορικό Συναίνεσης",
        "ru": "История согласий",
        "de": "Einwilligungsverlauf",
        "de-AT": "Einwilligungsverlauf",
        "fr": "Historique de consentement",
        "nl": "Toestemmingsgeschiedenis",
        "sv": "Samtyckeshistorik"
    },
    "continue": {
        "ar": "متابعة",
        "en": "Continue",
        "tr": "Devam Et",
        "el": "Συνέχεια",
        "ru": "Продолжить",
        "de": "Fortfahren",
        "de-AT": "Fortfahren",
        "fr": "Continuer",
        "nl": "Doorgaan",
        "sv": "Fortsätt"
    },
    "continueLesson": {
        "ar": "متابعة الدرس",
        "en": "Continue Lesson",
        "tr": "Derse Devam Et",
        "el": "Συνέχεια Μαθήματος",
        "ru": "Продолжить урок",
        "de": "Lektion fortsetzen",
        "de-AT": "Lektion fortsetzen",
        "fr": "Continuer la leçon",
        "nl": "Les voortzetten",
        "sv": "Fortsätt lektion"
    },
    "correctAnswers": {
        "ar": "الإجابات الصحيحة",
        "en": "Correct Answers",
        "tr": "Doğru Cevaplar",
        "el": "Σωστές Απαντήσεις",
        "ru": "Правильные ответы",
        "de": "Richtige Antworten",
        "de-AT": "Richtige Antworten",
        "fr": "Bonnes réponses",
        "nl": "Juiste antwoorden",
        "sv": "Rätta svar"
    },
    "createPost": {
        "ar": "إنشاء منشور",
        "en": "Create Post",
        "tr": "Gönderi Oluştur",
        "el": "Δημιουργία Δημοσίευσης",
        "ru": "Создать публикацию",
        "de": "Beitrag erstellen",
        "de-AT": "Beitrag erstellen",
        "fr": "Créer une publication",
        "nl": "Bericht aanmaken",
        "sv": "Skapa inlägg"
    },
    "dailyStreak": {
        "ar": "السلسلة اليومية",
        "en": "Daily Streak",
        "tr": "Günlük Seri",
        "el": "Ημερήσιο Σερί",
        "ru": "Ежедневная серия",
        "de": "Tägliche Serie",
        "de-AT": "Tägliche Serie",
        "fr": "Série quotidienne",
        "nl": "Dagelijkse reeks",
        "sv": "Daglig svit"
    },
    "dataRetention": {
        "ar": "الاحتفاظ بالبيانات",
        "en": "Data Retention",
        "tr": "Veri Saklama",
        "el": "Διατήρηση Δεδομένων",
        "ru": "Хранение данных",
        "de": "Datenaufbewahrung",
        "de-AT": "Datenaufbewahrung",
        "fr": "Conservation des données",
        "nl": "Gegevensbewaring",
        "sv": "Datalagring"
    },
    "dataRetentionDesc": {
        "ar": "سيتم حذف بياناتك خلال 30 يومًا.",
        "en": "Your data will be deleted within 30 days.",
        "tr": "Verileriniz 30 gün içinde silinecektir.",
        "el": "Τα δεδομένα σας θα διαγραφούν εντός 30 ημερών.",
        "ru": "Ваши данные будут удалены в течение 30 дней.",
        "de": "Ihre Daten werden innerhalb von 30 Tagen gelöscht.",
        "de-AT": "Ihre Daten werden innerhalb von 30 Tagen gelöscht.",
        "fr": "Vos données seront supprimées dans les 30 jours.",
        "nl": "Uw gegevens worden binnen 30 dagen verwijderd.",
        "sv": "Dina uppgifter raderas inom 30 dagar."
    },
    "done": {
        "ar": "تم",
        "en": "Done",
        "tr": "Tamam",
        "el": "Ολοκληρώθηκε",
        "ru": "Готово",
        "de": "Fertig",
        "de-AT": "Fertig",
        "fr": "Terminé",
        "nl": "Klaar",
        "sv": "Klar"
    },
    "exportData": {
        "ar": "تصدير البيانات",
        "en": "Export Data",
        "tr": "Verileri Dışa Aktar",
        "el": "Εξαγωγή Δεδομένων",
        "ru": "Экспорт данных",
        "de": "Daten exportieren",
        "de-AT": "Daten exportieren",
        "fr": "Exporter les données",
        "nl": "Gegevens exporteren",
        "sv": "Exportera data"
    },
    "feedback": {
        "ar": "ملاحظات",
        "en": "Feedback",
        "tr": "Geri Bildirim",
        "el": "Σχόλια",
        "ru": "Обратная связь",
        "de": "Feedback",
        "de-AT": "Feedback",
        "fr": "Commentaires",
        "nl": "Feedback",
        "sv": "Feedback"
    },
    "hadithCount": {
        "ar": "الأحاديث",
        "en": "Hadiths",
        "tr": "Hadisler",
        "el": "Χαντίθ",
        "ru": "Хадисы",
        "de": "Hadithe",
        "de-AT": "Hadithe",
        "fr": "Hadiths",
        "nl": "Hadiths",
        "sv": "Hadither"
    },
    "leaderboard": {
        "ar": "لوحة المتصدرين",
        "en": "Leaderboard",
        "tr": "Sıralama Tablosu",
        "el": "Πίνακας Κατάταξης",
        "ru": "Таблица лидеров",
        "de": "Bestenliste",
        "de-AT": "Bestenliste",
        "fr": "Classement",
        "nl": "Scorebord",
        "sv": "Topplista"
    },
    "letterMatch": {
        "ar": "مطابقة الحروف",
        "en": "Letter Match",
        "tr": "Harf Eşleştirme",
        "el": "Αντιστοίχιση Γραμμάτων",
        "ru": "Сопоставление букв",
        "de": "Buchstaben zuordnen",
        "de-AT": "Buchstaben zuordnen",
        "fr": "Associer les lettres",
        "nl": "Letters koppelen",
        "sv": "Matcha bokstäver"
    },
    "memoryGame": {
        "ar": "لعبة الذاكرة",
        "en": "Memory Game",
        "tr": "Hafıza Oyunu",
        "el": "Παιχνίδι Μνήμης",
        "ru": "Игра на память",
        "de": "Gedächtnisspiel",
        "de-AT": "Gedächtnisspiel",
        "fr": "Jeu de mémoire",
        "nl": "Geheugenspel",
        "sv": "Memoryspel"
    },
    "monthlyProgress": {
        "ar": "التقدم الشهري",
        "en": "Monthly Progress",
        "tr": "Aylık İlerleme",
        "el": "Μηνιαία Πρόοδος",
        "ru": "Ежемесячный прогресс",
        "de": "Monatlicher Fortschritt",
        "de-AT": "Monatlicher Fortschritt",
        "fr": "Progrès mensuel",
        "nl": "Maandelijkse voortgang",
        "sv": "Månadsframsteg"
    },
    "noPosts": {
        "ar": "لا توجد منشورات",
        "en": "No posts available",
        "tr": "Gönderi bulunmuyor",
        "el": "Δεν υπάρχουν δημοσιεύσεις",
        "ru": "Нет публикаций",
        "de": "Keine Beiträge vorhanden",
        "de-AT": "Keine Beiträge vorhanden",
        "fr": "Aucune publication",
        "nl": "Geen berichten beschikbaar",
        "sv": "Inga inlägg tillgängliga"
    },
    "pageCount": {
        "ar": "الصفحات",
        "en": "Pages",
        "tr": "Sayfalar",
        "el": "Σελίδες",
        "ru": "Страницы",
        "de": "Seiten",
        "de-AT": "Seiten",
        "fr": "Pages",
        "nl": "Pagina's",
        "sv": "Sidor"
    },
    "postContent": {
        "ar": "محتوى المنشور",
        "en": "Post Content",
        "tr": "Gönderi İçeriği",
        "el": "Περιεχόμενο Δημοσίευσης",
        "ru": "Содержание публикации",
        "de": "Beitragsinhalt",
        "de-AT": "Beitragsinhalt",
        "fr": "Contenu de la publication",
        "nl": "Berichtinhoud",
        "sv": "Inläggsinnehåll"
    },
    "prayerNotification": {
        "ar": "إشعار الصلاة",
        "en": "Prayer Notification",
        "tr": "Namaz Bildirimi",
        "el": "Ειδοποίηση Προσευχής",
        "ru": "Уведомление о молитве",
        "de": "Gebetsbenachrichtigung",
        "de-AT": "Gebetsbenachrichtigung",
        "fr": "Notification de prière",
        "nl": "Gebeds­melding",
        "sv": "Bönenotifikation"
    },
    "privacyRights": {
        "ar": "حقوقك في الخصوصية",
        "en": "Your Privacy Rights",
        "tr": "Gizlilik Haklarınız",
        "el": "Τα Δικαιώματα Απορρήτου σας",
        "ru": "Ваши права на конфиденциальность",
        "de": "Ihre Datenschutzrechte",
        "de-AT": "Ihre Datenschutzrechte",
        "fr": "Vos droits de confidentialité",
        "nl": "Uw privacyrechten",
        "sv": "Dina integritetsrättigheter"
    },
    "quizGame": {
        "ar": "لعبة الأسئلة",
        "en": "Quiz Game",
        "tr": "Bilgi Yarışması",
        "el": "Κουίζ",
        "ru": "Викторина",
        "de": "Quiz-Spiel",
        "de-AT": "Quiz-Spiel",
        "fr": "Quiz",
        "nl": "Quizspel",
        "sv": "Frågesport"
    },
    "reminderNotification": {
        "ar": "إشعار التذكير",
        "en": "Reminder Notification",
        "tr": "Hatırlatma Bildirimi",
        "el": "Ειδοποίηση Υπενθύμισης",
        "ru": "Уведомление-напоминание",
        "de": "Erinnerungsbenachrichtigung",
        "de-AT": "Erinnerungsbenachrichtigung",
        "fr": "Notification de rappel",
        "nl": "Herinneringsmelding",
        "sv": "Påminnelsenotifikation"
    },
    "report": {
        "ar": "إبلاغ",
        "en": "Report",
        "tr": "Bildir",
        "el": "Αναφορά",
        "ru": "Пожаловаться",
        "de": "Melden",
        "de-AT": "Melden",
        "fr": "Signaler",
        "nl": "Melden",
        "sv": "Rapportera"
    },
    "skip": {
        "ar": "تخطي",
        "en": "Skip",
        "tr": "Atla",
        "el": "Παράλειψη",
        "ru": "Пропустить",
        "de": "Überspringen",
        "de-AT": "Überspringen",
        "fr": "Passer",
        "nl": "Overslaan",
        "sv": "Hoppa över"
    },
    "startLesson": {
        "ar": "بدء الدرس",
        "en": "Start Lesson",
        "tr": "Derse Başla",
        "el": "Έναρξη Μαθήματος",
        "ru": "Начать урок",
        "de": "Lektion starten",
        "de-AT": "Lektion starten",
        "fr": "Commencer la leçon",
        "nl": "Les starten",
        "sv": "Starta lektion"
    },
    "todayGames": {
        "ar": "ألعاب اليوم",
        "en": "Today's Games",
        "tr": "Bugünün Oyunları",
        "el": "Σημερινά Παιχνίδια",
        "ru": "Игры на сегодня",
        "de": "Heutige Spiele",
        "de-AT": "Heutige Spiele",
        "fr": "Jeux du jour",
        "nl": "Spellen van vandaag",
        "sv": "Dagens spel"
    },
    "totalGames": {
        "ar": "إجمالي الألعاب",
        "en": "Total Games",
        "tr": "Toplam Oyun",
        "el": "Σύνολο Παιχνιδιών",
        "ru": "Всего игр",
        "de": "Gesamtspiele",
        "de-AT": "Gesamtspiele",
        "fr": "Total des jeux",
        "nl": "Totaal spellen",
        "sv": "Totalt antal spel"
    },
    "totalLessons": {
        "ar": "إجمالي الدروس",
        "en": "Total Lessons",
        "tr": "Toplam Ders",
        "el": "Σύνολο Μαθημάτων",
        "ru": "Всего уроков",
        "de": "Gesamtlektionen",
        "de-AT": "Gesamtlektionen",
        "fr": "Total des leçons",
        "nl": "Totaal lessen",
        "sv": "Totalt antal lektioner"
    },
    "verseCount": {
        "ar": "الآيات",
        "en": "Verses",
        "tr": "Ayetler",
        "el": "Στίχοι",
        "ru": "Аяты",
        "de": "Verse",
        "de-AT": "Verse",
        "fr": "Versets",
        "nl": "Verzen",
        "sv": "Verser"
    },
    "version": {
        "ar": "الإصدار",
        "en": "Version",
        "tr": "Sürüm",
        "el": "Έκδοση",
        "ru": "Версия",
        "de": "Version",
        "de-AT": "Version",
        "fr": "Version",
        "nl": "Versie",
        "sv": "Version"
    },
    "weeklyProgress": {
        "ar": "التقدم الأسبوعي",
        "en": "Weekly Progress",
        "tr": "Haftalık İlerleme",
        "el": "Εβδομαδιαία Πρόοδος",
        "ru": "Еженедельный прогресс",
        "de": "Wöchentlicher Fortschritt",
        "de-AT": "Wöchentlicher Fortschritt",
        "fr": "Progrès hebdomadaire",
        "nl": "Wekelijkse voortgang",
        "sv": "Veckans framsteg"
    },
    "withdrawConsent": {
        "ar": "سحب الموافقة",
        "en": "Withdraw Consent",
        "tr": "Onayı Geri Çek",
        "el": "Ανάκληση Συναίνεσης",
        "ru": "Отозвать согласие",
        "de": "Einwilligung widerrufen",
        "de-AT": "Einwilligung widerrufen",
        "fr": "Retirer le consentement",
        "nl": "Toestemming intrekken",
        "sv": "Återkalla samtycke"
    },
    "wordBuilder": {
        "ar": "بناء الكلمات",
        "en": "Word Builder",
        "tr": "Kelime Oluşturucu",
        "el": "Δημιουργός Λέξεων",
        "ru": "Составление слов",
        "de": "Wortbauer",
        "de-AT": "Wortbauer",
        "fr": "Constructeur de mots",
        "nl": "Woordbouwer",
        "sv": "Ordbyggare"
    },
    "wrongAnswers": {
        "ar": "الإجابات الخاطئة",
        "en": "Wrong Answers",
        "tr": "Yanlış Cevaplar",
        "el": "Λάθος Απαντήσεις",
        "ru": "Неправильные ответы",
        "de": "Falsche Antworten",
        "de-AT": "Falsche Antworten",
        "fr": "Mauvaises réponses",
        "nl": "Foute antwoorden",
        "sv": "Felaktiga svar"
    },
}

# ============================================================
# PART 2: Fix untranslated values (English left in non-English files)
# These are genuinely translatable values that were missed
# ============================================================
TRANSLATION_FIXES = {
    "de": {
        "gold": "Gold",
        "goldLabel": "Gold",
        "status": "Status",
        "name": "Name",
        "nameLabel": "Name",
        "namePlaceholder": "Name *",
        "linkLabel": "Link",
        "pauseBtn": "Pause",
        "transliteration": "Transliteration",
        "system": "System",
        "deepfakes": "Deepfakes",
        "live247": "Live 24/7",
        "liveLabel": "Live",
        "mediaAudio": "Audio",
        "mediaText": "Text",
        "mediaVideo": "Video",
        "video": "Video",
        "videoLabel": "Video",
        "videos": "Videos",
        "videosCategory": "Videos 🎬",
        "videosLabel": "Videos",
        "videosTab": "Videos",
        "trendsTab": "Trends",
        "textType": "Text",
        "wuduTab": "Wudu",
        "wuduTitle": "Wudu",
        "nisab": "Nisab",
        "nisabIn": "Nisab in",
        "quiz": "Quiz",
    },
    "de-AT": {
        "taraweehRuling": "Was ist das Urteil (Hukm) zum Tarawih-Gebet?",
    },
    "fr": {
        "actions": "Actions",
        "adDescription": "Description",
        "addImage": "Image",
        "assistant": "Assistant",
        "contactInfo": "Contact",
        "conversationsTitle": "Conversations",
        "date": "Date",
        "deepfakes": "Deepfakes",
        "embedDescription": "Description",
        "europeanMosques": "Europe",
        "gratitudeCategory": "Gratitude ❤️",
        "imageOption": "Image",
        "imageType": "Image",
        "images": "Images",
        "mediaAudio": "Audio",
        "messages": "Messages",
        "messagesTab": "Messages",
        "messagesTitle": "Messages",
        "miracles": "Miracles",
        "navMessages": "Messages",
        "notes": "Notes",
        "notifications": "Notifications",
        "notificationsTab": "Notifications",
        "pagesManagement": "Pages",
        "pauseBtn": "Pause",
        "permNotifTitle": "Notifications",
        "points": "Points",
        "protectionLabel": "Protection",
        "question": "question",
        "questionCategory": "Question ❓",
        "score": "Score",
        "section": "Section",
        "sectionsLabel": "Sections",
        "source": "Source",
        "stageMinaret": "Minaret",
        "storeBadges": "Badges",
        "storeCatBadge": "Badges",
        "subCategories": "sections",
        "tabGuide": "Guide",
        "tafsirSource": "Source",
        "termsIntroTitle": "Introduction",
        "total": "Total",
        "type": "Type",
        "reportReasonViolence": "Violence",
        "rizqCategory": "Rizq 🤲",
        "rarityRare": "Rare",
        "dailyLessonPointsFormat": "points",
        "10minutes": "10 minutes",
        "20minutes": "20 minutes",
        "30minutes": "30 minutes",
        "5minutes": "5 minutes",
    },
    "nl": {
        "arabicLetters": "Letters",
        "contactInfo": "Contact",
        "correct": "Correct!",
        "correctAnswer": "🎉 Correct! +{xp} XP",
        "deepfakes": "Deepfakes",
        "directWhatsapp": "Direct WhatsApp",
        "home": "Home",
        "kidsStop": "Stop",
        "letter": "Letter",
        "linkLabel": "Link",
        "linkOption": "Link",
        "live247": "Live 24/7",
        "liveLabel": "Live",
        "mediaAudio": "Audio",
        "mediaVideo": "Video",
        "nisab": "Nisab",
        "nisabIn": "Nisab in",
        "permLaterBtn": "Later",
        "privacy": "Privacy",
        "recent": "Recent",
        "reset": "Reset",
        "score": "Score",
        "start": "Start",
        "status": "Status",
        "storeBadges": "Badges",
        "storeCatBadge": "Badges",
        "stageMinaret": "Minaret",
        "surahName": "Soera",
        "termsDisclaimerTitle": "Disclaimer",
        "trending": "Trending 🔥",
        "trendsTab": "Trends",
        "type": "Type",
        "video": "Video",
        "videoLabel": "Video",
        "gram": "gram",
    },
    "sv": {
        "deepfakes": "Deepfakes",
        "dhikrLabel": "Dhikr / Recitation",
        "final": "Final",
        "gram": "gram",
        "initial": "Initial",
        "level5Skill3": "Recitation",
        "live247": "Live 24/7",
        "liveLabel": "Live",
        "mediaText": "Text",
        "mediaVideo": "Video",
        "silver": "Silver",
        "status": "Status",
        "system": "System",
        "tabGuide": "Guide",
        "textType": "Text",
        "video": "Video",
        "videoLabel": "Video",
    },
}

# ============================================================
# PART 3: Additional translation improvements
# Fix values that should be translated but were left in English
# ============================================================
DEEP_FIXES = {
    "nl": {
        # Dutch translations for values still in English
        "correctAnswer": "🎉 Goed zo! +{xp} XP",
        "correct": "Goed zo!",
        "home": "Startpagina",
        "arabicLetters": "Arabische letters",
        "contactInfo": "Contactgegevens",
        "kidsStop": "Stoppen",
        "letter": "Brief",
        "permLaterBtn": "Later",
        "privacy": "Privacy",
        "recent": "Recent",
        "reset": "Opnieuw instellen",
        "score": "Score",
        "start": "Starten",
        "status": "Status",
        "storeBadges": "Badges",
        "storeCatBadge": "Badges",
        "surahName": "Soera",
        "termsDisclaimerTitle": "Disclaimer",
        "trending": "Populair 🔥",
        "type": "Type",
        "zakatNisabTitle": "Zakat Nisab in {{currency}}",
    },
    "sv": {
        # Swedish translations for values still in English  
        "final": "Sista",
        "initial": "Inledande",
        "level5Skill3": "Recitation",
        "silver": "Silver",
        "status": "Status",
        "system": "System",
        "tabGuide": "Guide",
    },
    "fr": {
        # French translations for values still in English
        "actions": "Actions",
        "adDescription": "Description",
        "addImage": "Image",
        "assistant": "Assistant",
        "contactInfo": "Contact",
        "conversationsTitle": "Conversations",
        "date": "Date",
        "embedDescription": "Description",
        "europeanMosques": "Europe",
        "gratitudeCategory": "Gratitude ❤️",
        "imageOption": "Image",
        "imageType": "Image",
        "images": "Images",
        "messages": "Messages",
        "messagesTab": "Messages",
        "messagesTitle": "Messages",
        "miracles": "Miracles",
        "navMessages": "Messages",
        "notes": "Notes",
        "notifications": "Notifications",
        "notificationsTab": "Notifications",
        "pagesManagement": "Pages",
        "pauseBtn": "Pause",
        "permNotifTitle": "Notifications",
        "points": "Points",
        "protectionLabel": "Protection",
        "question": "question",
        "questionCategory": "Question ❓",
        "score": "Score",
        "section": "Section",
        "sectionsLabel": "Sections",
        "source": "Source",
        "stageMinaret": "Minaret",
        "subCategories": "sections",
        "tabGuide": "Guide",
        "tafsirSource": "Source",
        "termsIntroTitle": "Introduction",
        "total": "Total",
        "type": "Type",
        "reportReasonViolence": "Violence",
        "rarityRare": "Rare",
    },
}


def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')


def get_all_keys_flat(d, prefix=''):
    keys = set()
    for k, v in d.items():
        full_key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            keys.update(get_all_keys_flat(v, full_key))
        else:
            keys.add(full_key)
    return keys


def main():
    lang_files = {
        'ar': 'ar.json',
        'en': 'en.json',
        'de': 'de.json',
        'de-AT': 'de-AT.json',
        'fr': 'fr.json',
        'nl': 'nl.json',
        'sv': 'sv.json',
        'tr': 'tr.json',
        'el': 'el.json',
        'ru': 'ru.json',
    }
    
    # Load all files
    data = {}
    for lang, fname in lang_files.items():
        filepath = os.path.join(LOCALES_DIR, fname)
        data[lang] = load_json(filepath)
        print(f"Loaded {fname}: {len(get_all_keys_flat(data[lang]))} keys")
    
    changes_made = {lang: 0 for lang in lang_files}
    
    # ==========================================
    # STEP 1: Add 41 missing keys to all files
    # ==========================================
    print("\n=== STEP 1: Adding missing keys ===")
    for key, translations in MISSING_KEYS_TRANSLATIONS.items():
        for lang in lang_files:
            if key not in data[lang]:
                if lang in translations:
                    data[lang][key] = translations[lang]
                    changes_made[lang] += 1
                    print(f"  Added '{key}' to {lang}: {translations[lang][:50]}")
    
    # ==========================================
    # STEP 2: Fix Arabic text leak in de-AT
    # ==========================================
    print("\n=== STEP 2: Fixing Arabic text leaks ===")
    if "taraweehRuling" in data["de-AT"]:
        old_val = data["de-AT"]["taraweehRuling"]
        new_val = "Was ist das Urteil (Hukm) zum Tarawih-Gebet?"
        if old_val != new_val:
            data["de-AT"]["taraweehRuling"] = new_val
            changes_made["de-AT"] += 1
            print(f"  Fixed de-AT taraweehRuling: {old_val[:50]} -> {new_val[:50]}")
    
    # ==========================================
    # STEP 3: Apply translation fixes
    # ==========================================
    print("\n=== STEP 3: Applying deep translation fixes ===")
    for lang, fixes in DEEP_FIXES.items():
        for key, value in fixes.items():
            if key in data[lang]:
                old_val = data[lang][key]
                if old_val != value:
                    data[lang][key] = value
                    changes_made[lang] += 1
                    print(f"  Fixed {lang} '{key}': '{old_val[:40]}' -> '{value[:40]}'")
    
    # ==========================================
    # STEP 4: Ensure all files have same keys
    # ==========================================
    print("\n=== STEP 4: Syncing keys across all files ===")
    
    # Get union of ALL keys across all files
    all_keys = set()
    for lang in lang_files:
        all_keys.update(data[lang].keys())
    
    # For each file, check if any keys are missing
    for lang in lang_files:
        missing = all_keys - set(data[lang].keys())
        if missing:
            print(f"\n  {lang} is missing {len(missing)} keys:")
            for key in sorted(missing):
                # Find the value from another language and translate
                # Priority: use English as source
                source_val = None
                for src_lang in ['en', 'ar', 'de', 'fr']:
                    if key in data[src_lang]:
                        source_val = data[src_lang][key]
                        break
                
                if source_val is not None:
                    # Use the key translations if we have them
                    if key in MISSING_KEYS_TRANSLATIONS and lang in MISSING_KEYS_TRANSLATIONS[key]:
                        data[lang][key] = MISSING_KEYS_TRANSLATIONS[key][lang]
                    else:
                        # Fallback: use English value (better than missing)
                        data[lang][key] = source_val
                    changes_made[lang] += 1
                    print(f"    Added '{key}' = '{str(data[lang][key])[:50]}'")
    
    # ==========================================
    # STEP 5: Save all files
    # ==========================================
    print("\n=== STEP 5: Saving files ===")
    for lang, fname in lang_files.items():
        filepath = os.path.join(LOCALES_DIR, fname)
        save_json(filepath, data[lang])
        final_keys = len(get_all_keys_flat(data[lang]))
        print(f"  Saved {fname}: {final_keys} keys ({changes_made[lang]} changes)")
    
    # ==========================================
    # STEP 6: Final verification
    # ==========================================
    print("\n=== FINAL VERIFICATION ===")
    key_counts = {}
    for lang, fname in lang_files.items():
        filepath = os.path.join(LOCALES_DIR, fname)
        check_data = load_json(filepath)
        key_counts[lang] = len(get_all_keys_flat(check_data))
        print(f"  {fname}: {key_counts[lang]} keys")
    
    # Check all counts are the same
    counts = set(key_counts.values())
    if len(counts) == 1:
        print(f"\n✅ SUCCESS: All files have exactly {counts.pop()} keys!")
    else:
        print(f"\n⚠️ WARNING: Key counts differ: {key_counts}")
        # Show differences
        max_keys = max(key_counts.values())
        for lang, count in key_counts.items():
            if count < max_keys:
                print(f"  {lang} is missing {max_keys - count} keys")
    
    total_changes = sum(changes_made.values())
    print(f"\n📊 Total changes made: {total_changes}")
    for lang, count in changes_made.items():
        if count > 0:
            print(f"  {lang}: {count} changes")


if __name__ == '__main__':
    main()

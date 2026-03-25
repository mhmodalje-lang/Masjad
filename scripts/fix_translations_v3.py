#!/usr/bin/env python3
"""
Fix remaining hardcoded Arabic text in user-facing components - Phase 3
"""
import json
import os

LOCALES_DIR = '/app/frontend/src/locales'

NEW_KEYS = {
    # Profile.tsx
    "themeLabel": {
        "ar": "المظهر", "en": "Theme", "de": "Design", "de-AT": "Design",
        "fr": "Thème", "nl": "Thema", "sv": "Tema", "tr": "Tema",
        "el": "Θέμα", "ru": "Тема"
    },
    "notificationsLabel": {
        "ar": "الإشعارات", "en": "Notifications", "de": "Benachrichtigungen", "de-AT": "Benachrichtigungen",
        "fr": "Notifications", "nl": "Meldingen", "sv": "Aviseringar", "tr": "Bildirimler",
        "el": "Ειδοποιήσεις", "ru": "Уведомления"
    },
    "privacyLabel": {
        "ar": "الخصوصية", "en": "Privacy", "de": "Datenschutz", "de-AT": "Datenschutz",
        "fr": "Confidentialité", "nl": "Privacy", "sv": "Integritet", "tr": "Gizlilik",
        "el": "Απόρρητο", "ru": "Конфиденциальность"
    },
    # Install.tsx
    "installFeature1": {
        "ar": "يعمل بدون إنترنت", "en": "Works offline", "de": "Funktioniert offline", "de-AT": "Funktioniert offline",
        "fr": "Fonctionne hors ligne", "nl": "Werkt offline", "sv": "Fungerar offline", "tr": "Çevrimdışı çalışır",
        "el": "Λειτουργεί εκτός σύνδεσης", "ru": "Работает офлайн"
    },
    "installFeature2": {
        "ar": "تنبيهات مواقيت الصلاة", "en": "Prayer time alerts", "de": "Gebetszeit-Benachrichtigungen", "de-AT": "Gebetszeit-Benachrichtigungen",
        "fr": "Alertes heures de prière", "nl": "Gebetstijd meldingen", "sv": "Bönetidsaviseringar", "tr": "Namaz vakti bildirimleri",
        "el": "Ειδοποιήσεις ωρών προσευχής", "ru": "Уведомления о времени молитвы"
    },
    "installFeature3": {
        "ar": "تخزين البيانات محلياً", "en": "Local data storage", "de": "Lokale Datenspeicherung", "de-AT": "Lokale Datenspeicherung",
        "fr": "Stockage de données local", "nl": "Lokale gegevensopslag", "sv": "Lokal datalagring", "tr": "Yerel veri depolama",
        "el": "Τοπική αποθήκευση δεδομένων", "ru": "Локальное хранение данных"
    },
    # usePushNotifications.tsx
    "notifAllowRequired": {
        "ar": "يجب السماح بالإشعارات", "en": "Notifications must be allowed", "de": "Benachrichtigungen müssen erlaubt sein",
        "de-AT": "Benachrichtigungen müssen erlaubt sein",
        "fr": "Les notifications doivent être autorisées", "nl": "Meldingen moeten worden toegestaan",
        "sv": "Aviseringar måste tillåtas", "tr": "Bildirimlere izin verilmeli",
        "el": "Πρέπει να επιτρέπονται οι ειδοποιήσεις", "ru": "Необходимо разрешить уведомления"
    },
    "notifEnabled": {
        "ar": "تم تفعيل الإشعارات بنجاح 🔔", "en": "Notifications enabled successfully 🔔",
        "de": "Benachrichtigungen erfolgreich aktiviert 🔔", "de-AT": "Benachrichtigungen erfolgreich aktiviert 🔔",
        "fr": "Notifications activées avec succès 🔔", "nl": "Meldingen succesvol ingeschakeld 🔔",
        "sv": "Aviseringar aktiverade 🔔", "tr": "Bildirimler başarıyla etkinleştirildi 🔔",
        "el": "Ειδοποιήσεις ενεργοποιήθηκαν 🔔", "ru": "Уведомления успешно включены 🔔"
    },
    "notifEnableFailed": {
        "ar": "فشل تفعيل الإشعارات", "en": "Failed to enable notifications",
        "de": "Benachrichtigungen konnten nicht aktiviert werden", "de-AT": "Benachrichtigungen konnten nicht aktiviert werden",
        "fr": "Échec de l'activation des notifications", "nl": "Meldingen inschakelen mislukt",
        "sv": "Misslyckades med att aktivera aviseringar", "tr": "Bildirimler etkinleştirilemedi",
        "el": "Αποτυχία ενεργοποίησης ειδοποιήσεων", "ru": "Не удалось включить уведомления"
    },
    "notifDisabled": {
        "ar": "تم إيقاف الإشعارات", "en": "Notifications disabled",
        "de": "Benachrichtigungen deaktiviert", "de-AT": "Benachrichtigungen deaktiviert",
        "fr": "Notifications désactivées", "nl": "Meldingen uitgeschakeld",
        "sv": "Aviseringar inaktiverade", "tr": "Bildirimler devre dışı bırakıldı",
        "el": "Ειδοποιήσεις απενεργοποιήθηκαν", "ru": "Уведомления отключены"
    },
    "notifNotSubscribed": {
        "ar": "غير مشترك في الإشعارات", "en": "Not subscribed to notifications",
        "de": "Nicht für Benachrichtigungen abonniert", "de-AT": "Nicht für Benachrichtigungen abonniert",
        "fr": "Non abonné aux notifications", "nl": "Niet geabonneerd op meldingen",
        "sv": "Inte prenumererad på aviseringar", "tr": "Bildirimlere abone değil",
        "el": "Δεν είστε εγγεγραμμένοι σε ειδοποιήσεις", "ru": "Не подписаны на уведомления"
    },
    "notifTestFailed": {
        "ar": "فشل إرسال إشعار تجريبي", "en": "Failed to send test notification",
        "de": "Testbenachrichtigung konnte nicht gesendet werden", "de-AT": "Testbenachrichtigung konnte nicht gesendet werden",
        "fr": "Échec de l'envoi de la notification test", "nl": "Test melding verzenden mislukt",
        "sv": "Misslyckades med att skicka testavisering", "tr": "Test bildirimi gönderilemedi",
        "el": "Αποτυχία αποστολής δοκιμαστικής ειδοποίησης", "ru": "Не удалось отправить тестовое уведомление"
    },
    "notifTestSent": {
        "ar": "تم إرسال إشعار تجريبي", "en": "Test notification sent",
        "de": "Testbenachrichtigung gesendet", "de-AT": "Testbenachrichtigung gesendet",
        "fr": "Notification test envoyée", "nl": "Testmelding verzonden",
        "sv": "Testavisering skickad", "tr": "Test bildirimi gönderildi",
        "el": "Δοκιμαστική ειδοποίηση στάλθηκε", "ru": "Тестовое уведомление отправлено"
    },
    # useFavoriteDuas.tsx
    "duaRemovedFav": {
        "ar": "تم إزالة الدعاء من المفضلة", "en": "Dua removed from favorites",
        "de": "Dua aus Favoriten entfernt", "de-AT": "Dua aus Favoriten entfernt",
        "fr": "Dua retiré des favoris", "nl": "Dua verwijderd uit favorieten",
        "sv": "Dua borttagen från favoriter", "tr": "Dua favorilerden kaldırıldı",
        "el": "Η ντουά αφαιρέθηκε από τα αγαπημένα", "ru": "Дуа удалена из избранного"
    },
    "duaSavedFav": {
        "ar": "تم حفظ الدعاء في المفضلة ❤️", "en": "Dua saved to favorites ❤️",
        "de": "Dua zu Favoriten hinzugefügt ❤️", "de-AT": "Dua zu Favoriten hinzugefügt ❤️",
        "fr": "Dua ajouté aux favoris ❤️", "nl": "Dua opgeslagen in favorieten ❤️",
        "sv": "Dua sparad i favoriter ❤️", "tr": "Dua favorilere kaydedildi ❤️",
        "el": "Η ντουά αποθηκεύτηκε στα αγαπημένα ❤️", "ru": "Дуа сохранена в избранное ❤️"
    },
    # RamadanCalendar.tsx
    "ramadanCalendarTitle": {
        "ar": "تقويم رمضان ١٤٤٧", "en": "Ramadan Calendar 1447",
        "de": "Ramadan-Kalender 1447", "de-AT": "Ramadan-Kalender 1447",
        "fr": "Calendrier du Ramadan 1447", "nl": "Ramadan kalender 1447",
        "sv": "Ramadan-kalender 1447", "tr": "Ramazan Takvimi 1447",
        "el": "Ημερολόγιο Ραμαδάν 1447", "ru": "Календарь Рамадана 1447"
    },
    "ramadanDayOf30": {
        "ar": "من 30", "en": "of 30", "de": "von 30", "de-AT": "von 30",
        "fr": "sur 30", "nl": "van 30", "sv": "av 30", "tr": "/ 30",
        "el": "από 30", "ru": "из 30"
    },
    "duasTab": {
        "ar": "🤲 الأدعية", "en": "🤲 Duas", "de": "🤲 Duas", "de-AT": "🤲 Duas",
        "fr": "🤲 Duas", "nl": "🤲 Duas", "sv": "🤲 Duas", "tr": "🤲 Dualar",
        "el": "🤲 Ντουάς", "ru": "🤲 Дуа"
    },
    "calendarTab": {
        "ar": "📅 التقويم", "en": "📅 Calendar", "de": "📅 Kalender", "de-AT": "📅 Kalender",
        "fr": "📅 Calendrier", "nl": "📅 Kalender", "sv": "📅 Kalender", "tr": "📅 Takvim",
        "el": "📅 Ημερολόγιο", "ru": "📅 Календарь"
    },
    "deedsTab": {
        "ar": "✨ الأعمال", "en": "✨ Deeds", "de": "✨ Taten", "de-AT": "✨ Taten",
        "fr": "✨ Actions", "nl": "✨ Daden", "sv": "✨ Handlingar", "tr": "✨ Ameller",
        "el": "✨ Πράξεις", "ru": "✨ Деяния"
    },
    "ramadanDaySelected": {
        "ar": "من رمضان", "en": "of Ramadan", "de": "von Ramadan", "de-AT": "von Ramadan",
        "fr": "du Ramadan", "nl": "van Ramadan", "sv": "av Ramadan", "tr": "Ramazan",
        "el": "Ραμαδάν", "ru": "Рамадана"
    },
    "deedCompleted": {
        "ar": "أكملت هذا العمل", "en": "Completed this deed",
        "de": "Diese Tat abgeschlossen", "de-AT": "Diese Tat abgeschlossen",
        "fr": "Action accomplie", "nl": "Deze daad voltooid",
        "sv": "Utfört denna handling", "tr": "Bu ameli tamamladım",
        "el": "Ολοκλήρωσα αυτή την πράξη", "ru": "Выполнил это деяние"
    },
    # RamadanBook.tsx
    "ramadanBookTitle": {
        "ar": "كتاب رمضان", "en": "Ramadan Book",
        "de": "Ramadan-Buch", "de-AT": "Ramadan-Buch",
        "fr": "Livre du Ramadan", "nl": "Ramadan boek",
        "sv": "Ramadan-bok", "tr": "Ramazan Kitabı",
        "el": "Βιβλίο Ραμαδάν", "ru": "Книга Рамадана"
    },
    "fastingRulesTitle": {
        "ar": "أحكام الصيام", "en": "Fasting Rules",
        "de": "Fastenregeln", "de-AT": "Fastenregeln",
        "fr": "Règles du jeûne", "nl": "Vastenregels",
        "sv": "Fasteregler", "tr": "Oruç Hükümleri",
        "el": "Κανόνες Νηστείας", "ru": "Правила поста"
    },
    "fastingDefTitle": {
        "ar": "تعريف الصيام", "en": "Definition of Fasting",
        "de": "Definition des Fastens", "de-AT": "Definition des Fastens",
        "fr": "Définition du jeûne", "nl": "Definitie van vasten",
        "sv": "Definition av fasta", "tr": "Orucun Tanımı",
        "el": "Ορισμός Νηστείας", "ru": "Определение поста"
    },
    "fastingDefContent": {
        "ar": "الصيام هو الإمساك عن الطعام والشراب وسائر المفطرات من طلوع الفجر إلى غروب الشمس بنية التقرب إلى الله تعالى",
        "en": "Fasting is abstaining from food, drink, and all things that break the fast from dawn to sunset with the intention of drawing closer to Allah the Almighty",
        "de": "Fasten bedeutet, sich von Essen, Trinken und allem, was das Fasten bricht, von der Morgendämmerung bis zum Sonnenuntergang zu enthalten, mit der Absicht, Allah näher zu kommen",
        "de-AT": "Fasten bedeutet, sich von Essen, Trinken und allem, was das Fasten bricht, von der Morgendämmerung bis zum Sonnenuntergang zu enthalten, mit der Absicht, Allah näher zu kommen",
        "fr": "Le jeûne consiste à s'abstenir de nourriture, de boisson et de tout ce qui rompt le jeûne, de l'aube au coucher du soleil, avec l'intention de se rapprocher d'Allah le Tout-Puissant",
        "nl": "Vasten is zich onthouden van eten, drinken en alles wat het vasten verbreekt, van dageraad tot zonsondergang, met de intentie dichter bij Allah de Almachtige te komen",
        "sv": "Fasta innebär att avstå från mat, dryck och allt som bryter fastan från gryning till solnedgång med avsikten att komma närmare Allah den Allsmäktige",
        "tr": "Oruç, Allah'a yaklaşma niyetiyle fecirden güneş batışına kadar yeme, içme ve orucu bozan tüm şeylerden uzak durmaktır",
        "el": "Η νηστεία σημαίνει αποχή από φαγητό, ποτό και όλα όσα σπάνε τη νηστεία από την αυγή μέχρι τη δύση του ηλίου, με σκοπό την προσέγγιση στον Αλλάχ τον Παντοδύναμο",
        "ru": "Пост — это воздержание от еды, питья и всего, что нарушает пост, с рассвета до заката с намерением приблизиться к Аллаху Всевышнему"
    },
    "fastingConditionsTitle": {
        "ar": "شروط وجوب الصيام", "en": "Conditions of Fasting",
        "de": "Bedingungen des Fastens", "de-AT": "Bedingungen des Fastens",
        "fr": "Conditions du jeûne", "nl": "Voorwaarden van vasten",
        "sv": "Villkor för fasta", "tr": "Orucun Şartları",
        "el": "Προϋποθέσεις Νηστείας", "ru": "Условия обязательности поста"
    },
    "fastingConditionsContent": {
        "ar": "الإسلام، البلوغ، العقل، القدرة على الصوم، الإقامة (المسافر يجوز له الفطر)",
        "en": "Islam, maturity, sanity, ability to fast, residence (travelers may break the fast)",
        "de": "Islam, Reife, Verstand, Fähigkeit zu fasten, Ansässigkeit (Reisende dürfen das Fasten brechen)",
        "de-AT": "Islam, Reife, Verstand, Fähigkeit zu fasten, Ansässigkeit (Reisende dürfen das Fasten brechen)",
        "fr": "L'islam, la puberté, la raison, la capacité de jeûner, la résidence (le voyageur peut rompre le jeûne)",
        "nl": "Islam, volwassenheid, verstand, vermogen om te vasten, verblijf (reizigers mogen het vasten verbreken)",
        "sv": "Islam, mognad, förstånd, förmåga att fasta, bosättning (resenärer får bryta fastan)",
        "tr": "İslam, ergenlik, akıl, oruç tutma gücü, ikamet (yolcu iftar edebilir)",
        "el": "Ισλάμ, ωριμότητα, λογική, ικανότητα νηστείας, κατοικία (οι ταξιδιώτες μπορούν να σπάσουν τη νηστεία)",
        "ru": "Ислам, совершеннолетие, разум, способность поститься, проживание (путешественник может разговеться)"
    },
    "fastingPillarsTitle": {
        "ar": "أركان الصيام", "en": "Pillars of Fasting",
        "de": "Säulen des Fastens", "de-AT": "Säulen des Fastens",
        "fr": "Piliers du jeûne", "nl": "Pilaren van vasten",
        "sv": "Fastans pelare", "tr": "Orucun Rükünleri",
        "el": "Πυλώνες Νηστείας", "ru": "Столпы поста"
    },
    "fastingPillarsContent": {
        "ar": "النية: ويجب تبييتها من الليل في صوم الفريضة. الإمساك عن المفطرات من الفجر إلى المغرب",
        "en": "Intention: must be made the night before for obligatory fasting. Abstaining from things that break the fast from Fajr to Maghrib",
        "de": "Absicht: muss am Vorabend für das Pflichtfasten gefasst werden. Enthaltung von fastenbrechenden Dingen von Fajr bis Maghrib",
        "de-AT": "Absicht: muss am Vorabend für das Pflichtfasten gefasst werden. Enthaltung von fastenbrechenden Dingen von Fajr bis Maghrib",
        "fr": "L'intention : doit être formulée la veille pour le jeûne obligatoire. S'abstenir de ce qui rompt le jeûne de Fajr à Maghrib",
        "nl": "Intentie: moet de avond ervoor worden gemaakt voor verplicht vasten. Onthouden van vastenverbrekende zaken van Fajr tot Maghrib",
        "sv": "Avsikt: måste göras kvällen innan för obligatorisk fasta. Avstå från saker som bryter fastan från Fajr till Maghrib",
        "tr": "Niyet: Farz oruç için geceden yapılmalıdır. Fecirden akşama kadar orucu bozan şeylerden uzak durma",
        "el": "Πρόθεση: πρέπει να γίνει το προηγούμενο βράδυ για υποχρεωτική νηστεία. Αποχή από πράγματα που σπάνε τη νηστεία από Φατζρ έως Μαγκρίμπ",
        "ru": "Намерение: должно быть сделано накануне для обязательного поста. Воздержание от нарушающих пост вещей от Фаджра до Магриба"
    },
    "fastingBreakersTitle": {
        "ar": "مبطلات الصيام", "en": "Things That Break the Fast",
        "de": "Was das Fasten bricht", "de-AT": "Was das Fasten bricht",
        "fr": "Ce qui annule le jeûne", "nl": "Wat het vasten verbreekt",
        "sv": "Saker som bryter fastan", "tr": "Orucu Bozan Şeyler",
        "el": "Πράγματα που σπάνε τη νηστεία", "ru": "Что нарушает пост"
    },
    "fastingBreakersContent": {
        "ar": "الأكل والشرب عمداً، التقيؤ عمداً، الحيض والنفاس، الجماع في نهار رمضان",
        "en": "Eating or drinking intentionally, deliberate vomiting, menstruation and postpartum bleeding, sexual relations during Ramadan daytime",
        "de": "Absichtliches Essen oder Trinken, absichtliches Erbrechen, Menstruation und Wochenbettblutung, Geschlechtsverkehr tagsüber im Ramadan",
        "de-AT": "Absichtliches Essen oder Trinken, absichtliches Erbrechen, Menstruation und Wochenbettblutung, Geschlechtsverkehr tagsüber im Ramadan",
        "fr": "Manger ou boire intentionnellement, vomir volontairement, menstruation et lochies, rapports sexuels pendant la journée du Ramadan",
        "nl": "Opzettelijk eten of drinken, opzettelijk braken, menstruatie en postpartumbloeding, seksuele gemeenschap overdag tijdens Ramadan",
        "sv": "Äta eller dricka avsiktligt, avsiktlig kräkning, menstruation och efterblödning, sexuellt umgänge under Ramadans dagtid",
        "tr": "Kasten yemek ve içmek, kasten kusma, hayız ve nifas, Ramazan gündüzünde cinsel ilişki",
        "el": "Εσκεμμένο φαγητό ή ποτό, σκόπιμος εμετός, εμμηνόρροια και λοχεία, σεξουαλικές σχέσεις κατά τη διάρκεια της ημέρας του Ραμαδάν",
        "ru": "Намеренное употребление пищи или питья, намеренная рвота, менструация и послеродовое кровотечение, половые отношения в дневное время Рамадана"
    },
    # prayerNotifications.ts
    "prayerNotifTest": {
        "ar": "🕌 اختبار - أذان وحكاية", "en": "🕌 Test - Azan & Hikaya",
        "de": "🕌 Test - Azan & Hikaya", "de-AT": "🕌 Test - Azan & Hikaya",
        "fr": "🕌 Test - Azan & Hikaya", "nl": "🕌 Test - Azan & Hikaya",
        "sv": "🕌 Test - Azan & Hikaya", "tr": "🕌 Test - Azan & Hikaya",
        "el": "🕌 Δοκιμή - Azan & Hikaya", "ru": "🕌 Тест - Azan & Hikaya"
    },
    "prayerNotifTestBody": {
        "ar": "الإشعارات تعمل بنجاح!", "en": "Notifications are working!",
        "de": "Benachrichtigungen funktionieren!", "de-AT": "Benachrichtigungen funktionieren!",
        "fr": "Les notifications fonctionnent !", "nl": "Meldingen werken!",
        "sv": "Aviseringar fungerar!", "tr": "Bildirimler çalışıyor!",
        "el": "Οι ειδοποιήσεις λειτουργούν!", "ru": "Уведомления работают!"
    },
    # useSEO.tsx
    "seoHomeTitle": {
        "ar": "أذان وحكاية - مواقيت الصلاة | القرآن الكريم | أذكار وأدعية",
        "en": "Azan & Hikaya - Prayer Times | Holy Quran | Adhkar & Duas",
        "de": "Azan & Hikaya - Gebetszeiten | Heiliger Quran | Adhkar & Duas",
        "de-AT": "Azan & Hikaya - Gebetszeiten | Heiliger Quran | Adhkar & Duas",
        "fr": "Azan & Hikaya - Horaires de prière | Saint Coran | Adhkar & Duas",
        "nl": "Azan & Hikaya - Gebetstijden | Heilige Koran | Adhkar & Duas",
        "sv": "Azan & Hikaya - Bönetider | Heliga Koranen | Adhkar & Duas",
        "tr": "Azan & Hikaya - Namaz Vakitleri | Kuran-ı Kerim | Zikirler & Dualar",
        "el": "Azan & Hikaya - Ώρες Προσευχής | Ιερό Κοράνι | Αζκάρ & Ντουά",
        "ru": "Азан и Хикая - Время молитвы | Священный Коран | Азкар и Дуа"
    },
    "seoHomeDesc": {
        "ar": "تطبيق إسلامي شامل: مواقيت الصلاة، القرآن الكريم، الأذكار، حاسبة الزكاة، تعلم العربية، وأكثر",
        "en": "Comprehensive Islamic app: prayer times, Holy Quran, Adhkar, Zakat calculator, learn Arabic, and more",
        "de": "Umfassende islamische App: Gebetszeiten, Heiliger Quran, Adhkar, Zakat-Rechner, Arabisch lernen und mehr",
        "de-AT": "Umfassende islamische App: Gebetszeiten, Heiliger Quran, Adhkar, Zakat-Rechner, Arabisch lernen und mehr",
        "fr": "Application islamique complète : horaires de prière, Saint Coran, Adhkar, calculateur de Zakat, apprendre l'arabe et plus",
        "nl": "Uitgebreide islamitische app: gebetstijden, Heilige Koran, Adhkar, Zakat-calculator, Arabisch leren en meer",
        "sv": "Heltäckande islamisk app: bönetider, Heliga Koranen, Adhkar, Zakat-kalkylator, lär dig arabiska och mer",
        "tr": "Kapsamlı İslami uygulama: namaz vakitleri, Kuran-ı Kerim, zikirler, zekat hesaplayıcı, Arapça öğren ve daha fazlası",
        "el": "Ολοκληρωμένη ισλαμική εφαρμογή: ώρες προσευχής, Ιερό Κοράνι, Αζκάρ, υπολογιστής Ζακάτ, μάθε Αραβικά και πολλά ακόμα",
        "ru": "Полноценное исламское приложение: время молитвы, Священный Коран, Азкар, калькулятор Закята, изучение арабского и многое другое"
    },
    # AdminDashboard.tsx
    "appSettings": {
        "ar": "إعدادات التطبيق", "en": "App Settings",
        "de": "App-Einstellungen", "de-AT": "App-Einstellungen",
        "fr": "Paramètres de l'application", "nl": "App-instellingen",
        "sv": "Appinställningar", "tr": "Uygulama Ayarları",
        "el": "Ρυθμίσεις Εφαρμογής", "ru": "Настройки приложения"
    },
    "generalAnnouncement": {
        "ar": "إعلان عام", "en": "General Announcement",
        "de": "Allgemeine Ankündigung", "de-AT": "Allgemeine Ankündigung",
        "fr": "Annonce générale", "nl": "Algemene aankondiging",
        "sv": "Allmänt meddelande", "tr": "Genel Duyuru",
        "el": "Γενική Ανακοίνωση", "ru": "Общее объявление"
    },
    "saveSettings": {
        "ar": "حفظ الإعدادات", "en": "Save Settings",
        "de": "Einstellungen speichern", "de-AT": "Einstellungen speichern",
        "fr": "Enregistrer les paramètres", "nl": "Instellingen opslaan",
        "sv": "Spara inställningar", "tr": "Ayarları Kaydet",
        "el": "Αποθήκευση Ρυθμίσεων", "ru": "Сохранить настройки"
    },
    "dangerZone": {
        "ar": "منطقة الخطر", "en": "Danger Zone",
        "de": "Gefahrenzone", "de-AT": "Gefahrenzone",
        "fr": "Zone de danger", "nl": "Gevarenzone",
        "sv": "Farzon", "tr": "Tehlikeli Alan",
        "el": "Ζώνη Κινδύνου", "ru": "Опасная зона"
    },
    "noDataYet": {
        "ar": "لا توجد بيانات بعد", "en": "No data yet",
        "de": "Noch keine Daten", "de-AT": "Noch keine Daten",
        "fr": "Pas encore de données", "nl": "Nog geen gegevens",
        "sv": "Ingen data ännu", "tr": "Henüz veri yok",
        "el": "Δεν υπάρχουν δεδομένα ακόμα", "ru": "Данных пока нет"
    },
}


def main():
    lang_files = {
        'ar': 'ar.json', 'en': 'en.json', 'de': 'de.json', 'de-AT': 'de-AT.json',
        'fr': 'fr.json', 'nl': 'nl.json', 'sv': 'sv.json', 'tr': 'tr.json',
        'el': 'el.json', 'ru': 'ru.json',
    }

    data = {}
    for lang, fname in lang_files.items():
        with open(os.path.join(LOCALES_DIR, fname), 'r', encoding='utf-8') as f:
            data[lang] = json.load(f)

    changes = {l: 0 for l in lang_files}
    for key, translations in NEW_KEYS.items():
        for lang in lang_files:
            if lang in translations:
                if key not in data[lang] or data[lang][key] != translations[lang]:
                    data[lang][key] = translations[lang]
                    changes[lang] += 1

    for lang, fname in lang_files.items():
        with open(os.path.join(LOCALES_DIR, fname), 'w', encoding='utf-8') as f:
            json.dump(data[lang], f, ensure_ascii=False, indent=2)
            f.write('\n')
        print(f"  {fname}: {changes[lang]} keys added/updated")

    print(f"\nTotal: {sum(changes.values())}")


if __name__ == '__main__':
    main()

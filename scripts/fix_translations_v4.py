#!/usr/bin/env python3
"""Fix AdminDashboard and remaining Arabic text - Phase 4"""
import json
import os

LOCALES_DIR = '/app/frontend/src/locales'

ADMIN_KEYS = {
    "appSettingsTitle": {
        "ar": "إعدادات التطبيق", "en": "App Settings", "de": "App-Einstellungen", "de-AT": "App-Einstellungen",
        "fr": "Paramètres", "nl": "App-instellingen", "sv": "Appinställningar", "tr": "Uygulama Ayarları",
        "el": "Ρυθμίσεις", "ru": "Настройки"
    },
    "tempPause": {
        "ar": "إيقاف مؤقت", "en": "Temporary Pause", "de": "Vorübergehend pausiert",
        "de-AT": "Vorübergehend pausiert", "fr": "Pause temporaire", "nl": "Tijdelijk gepauzeerd",
        "sv": "Tillfälligt pausad", "tr": "Geçici Duraklatma", "el": "Προσωρινή παύση", "ru": "Временная пауза"
    },
    "generalAnnouncementLabel": {
        "ar": "إعلان عام", "en": "General Announcement", "de": "Allgemeine Ankündigung",
        "de-AT": "Allgemeine Ankündigung", "fr": "Annonce générale", "nl": "Algemene aankondiging",
        "sv": "Allmänt meddelande", "tr": "Genel Duyuru", "el": "Γενική Ανακοίνωση", "ru": "Общее объявление"
    },
    "msgForAll": {
        "ar": "رسالة للجميع...", "en": "Message for everyone...", "de": "Nachricht für alle...",
        "de-AT": "Nachricht für alle...", "fr": "Message pour tous...", "nl": "Bericht voor iedereen...",
        "sv": "Meddelande till alla...", "tr": "Herkese mesaj...", "el": "Μήνυμα για όλους...", "ru": "Сообщение для всех..."
    },
    "bankAccountTitle": {
        "ar": "الحساب البنكي (لاستقبال الأرباح)", "en": "Bank Account (for receiving earnings)",
        "de": "Bankkonto (für Einnahmen)", "de-AT": "Bankkonto (für Einnahmen)",
        "fr": "Compte bancaire (pour les gains)", "nl": "Bankrekening (voor inkomsten)",
        "sv": "Bankkonto (för intäkter)", "tr": "Banka Hesabı (kazanç almak için)",
        "el": "Τραπεζικός λογαριασμός (για κέρδη)", "ru": "Банковский счёт (для получения доходов)"
    },
    "bankNameLabel": {
        "ar": "اسم البنك", "en": "Bank Name", "de": "Bankname", "de-AT": "Bankname",
        "fr": "Nom de la banque", "nl": "Banknaam", "sv": "Banknamn", "tr": "Banka Adı",
        "el": "Όνομα τράπεζας", "ru": "Название банка"
    },
    "saveBankBtn": {
        "ar": "حفظ الحساب البنكي", "en": "Save Bank Account", "de": "Bankkonto speichern",
        "de-AT": "Bankkonto speichern", "fr": "Enregistrer le compte", "nl": "Bankrekening opslaan",
        "sv": "Spara bankkonto", "tr": "Banka Hesabını Kaydet", "el": "Αποθήκευση λογαριασμού",
        "ru": "Сохранить банковский счёт"
    },
    "marketCommission": {
        "ar": "عمولة السوق", "en": "Market Commission", "de": "Marktprovision", "de-AT": "Marktprovision",
        "fr": "Commission du marché", "nl": "Marktcommissie", "sv": "Marknadsprovision",
        "tr": "Pazar Komisyonu", "el": "Προμήθεια αγοράς", "ru": "Комиссия маркетплейса"
    },
    "adSettingsTitle": {
        "ar": "إعدادات الإعلانات", "en": "Ad Settings", "de": "Werbeeinstellungen", "de-AT": "Werbeeinstellungen",
        "fr": "Paramètres de publicité", "nl": "Advertentie-instellingen", "sv": "Annonsinställningar",
        "tr": "Reklam Ayarları", "el": "Ρυθμίσεις διαφημίσεων", "ru": "Настройки рекламы"
    },
    "enableAds": {
        "ar": "تفعيل الإعلانات", "en": "Enable Ads", "de": "Werbung aktivieren", "de-AT": "Werbung aktivieren",
        "fr": "Activer les publicités", "nl": "Advertenties inschakelen", "sv": "Aktivera annonser",
        "tr": "Reklamları Etkinleştir", "el": "Ενεργοποίηση διαφημίσεων", "ru": "Включить рекламу"
    },
    "showAdsInApp": {
        "ar": "عرض الإعلانات في التطبيق", "en": "Show ads in app", "de": "Werbung in der App anzeigen",
        "de-AT": "Werbung in der App anzeigen", "fr": "Afficher les pubs dans l'app",
        "nl": "Advertenties tonen in app", "sv": "Visa annonser i appen",
        "tr": "Uygulamada reklamları göster", "el": "Εμφάνιση διαφημίσεων στην εφαρμογή",
        "ru": "Показывать рекламу в приложении"
    },
    "muteVideo": {
        "ar": "كتم صوت الفيديو", "en": "Mute Video", "de": "Video stumm schalten", "de-AT": "Video stumm schalten",
        "fr": "Couper le son de la vidéo", "nl": "Video dempen", "sv": "Stäng av videoljud",
        "tr": "Video Sesini Kapat", "el": "Σίγαση βίντεο", "ru": "Отключить звук видео"
    },
    "gdprConsent": {
        "ar": "موافقة GDPR", "en": "GDPR Consent", "de": "GDPR-Einwilligung", "de-AT": "DSGVO-Einwilligung",
        "fr": "Consentement RGPD", "nl": "AVG-toestemming", "sv": "GDPR-samtycke",
        "tr": "GDPR Onayı", "el": "Συναίνεση GDPR", "ru": "Согласие GDPR"
    },
    "askConsentBeforeAds": {
        "ar": "طلب الموافقة قبل عرض الإعلانات", "en": "Ask consent before showing ads",
        "de": "Einwilligung vor Werbung einholen", "de-AT": "Einwilligung vor Werbung einholen",
        "fr": "Demander le consentement avant les pubs", "nl": "Toestemming vragen voor advertenties",
        "sv": "Fråga om samtycke före annonser", "tr": "Reklamlardan önce onay iste",
        "el": "Ζήτηση συναίνεσης πριν τις διαφημίσεις", "ru": "Запрашивать согласие перед рекламой"
    },
    "adTypes": {
        "ar": "أنواع الإعلانات:", "en": "Ad Types:", "de": "Werbearten:", "de-AT": "Werbearten:",
        "fr": "Types de publicité :", "nl": "Advertentietypen:", "sv": "Annonstyper:",
        "tr": "Reklam Türleri:", "el": "Τύποι διαφημίσεων:", "ru": "Типы рекламы:"
    },
    "bannerAds": {
        "ar": "إعلانات البانر", "en": "Banner Ads", "de": "Banner-Werbung", "de-AT": "Banner-Werbung",
        "fr": "Bannières publicitaires", "nl": "Banneradvertenties", "sv": "Bannerannonser",
        "tr": "Banner Reklamlar", "el": "Διαφημίσεις banner", "ru": "Баннерная реклама"
    },
    "interstitialAds": {
        "ar": "إعلانات بين الصفحات", "en": "Interstitial Ads", "de": "Interstitial-Werbung",
        "de-AT": "Interstitial-Werbung", "fr": "Publicités interstitielles", "nl": "Interstitial-advertenties",
        "sv": "Mellansidesannonser", "tr": "Geçiş Reklamları", "el": "Ενδιάμεσες διαφημίσεις",
        "ru": "Межстраничная реклама"
    },
    "rewardedAds": {
        "ar": "إعلانات المكافآت", "en": "Rewarded Ads", "de": "Belohnungswerbung", "de-AT": "Belohnungswerbung",
        "fr": "Publicités récompensées", "nl": "Beloningsadvertenties", "sv": "Belöningsannonser",
        "tr": "Ödüllü Reklamlar", "el": "Διαφημίσεις ανταμοιβής", "ru": "Реклама с вознаграждением"
    },
    "saveAdSettings": {
        "ar": "حفظ إعدادات الإعلانات", "en": "Save Ad Settings", "de": "Werbeeinstellungen speichern",
        "de-AT": "Werbeeinstellungen speichern", "fr": "Enregistrer les paramètres pub",
        "nl": "Advertentie-instellingen opslaan", "sv": "Spara annonsinställningar",
        "tr": "Reklam Ayarlarını Kaydet", "el": "Αποθήκευση ρυθμίσεων", "ru": "Сохранить настройки рекламы"
    },
    "analyticsTitle": {
        "ar": "التحليلات (آخر 7 أيام)", "en": "Analytics (last 7 days)", "de": "Analysen (letzte 7 Tage)",
        "de-AT": "Analysen (letzte 7 Tage)", "fr": "Analyses (7 derniers jours)",
        "nl": "Analyses (laatste 7 dagen)", "sv": "Analyser (senaste 7 dagarna)",
        "tr": "Analizler (son 7 gün)", "el": "Αναλυτικά (τελευταίες 7 ημέρες)", "ru": "Аналитика (последние 7 дней)"
    },
    "refreshAnalytics": {
        "ar": "تحديث التحليلات", "en": "Refresh Analytics", "de": "Analysen aktualisieren",
        "de-AT": "Analysen aktualisieren", "fr": "Actualiser les analyses", "nl": "Analyses vernieuwen",
        "sv": "Uppdatera analyser", "tr": "Analizleri Yenile", "el": "Ανανέωση αναλυτικών", "ru": "Обновить аналитику"
    },
    "totalEvents": {
        "ar": "إجمالي الأحداث", "en": "Total Events", "de": "Gesamtereignisse", "de-AT": "Gesamtereignisse",
        "fr": "Total des événements", "nl": "Totaal gebeurtenissen", "sv": "Totalt antal händelser",
        "tr": "Toplam Olaylar", "el": "Συνολικά γεγονότα", "ru": "Всего событий"
    },
    "uniqueUsers": {
        "ar": "مستخدمون فريدون", "en": "Unique Users", "de": "Eindeutige Benutzer", "de-AT": "Eindeutige Benutzer",
        "fr": "Utilisateurs uniques", "nl": "Unieke gebruikers", "sv": "Unika användare",
        "tr": "Benzersiz Kullanıcılar", "el": "Μοναδικοί χρήστες", "ru": "Уникальные пользователи"
    },
    "mostVisitedPages": {
        "ar": "أكثر الصفحات زيارة:", "en": "Most Visited Pages:", "de": "Meistbesuchte Seiten:",
        "de-AT": "Meistbesuchte Seiten:", "fr": "Pages les plus visitées :", "nl": "Meest bezochte pagina's:",
        "sv": "Mest besökta sidor:", "tr": "En Çok Ziyaret Edilen Sayfalar:", "el": "Πιο δημοφιλείς σελίδες:",
        "ru": "Самые посещаемые страницы:"
    },
    "noEmbedYet": {
        "ar": "لا توجد بيانات مضمنة بعد", "en": "No embedded data yet", "de": "Noch keine eingebetteten Daten",
        "de-AT": "Noch keine eingebetteten Daten", "fr": "Aucune donnée intégrée", "nl": "Nog geen ingebedde gegevens",
        "sv": "Ingen inbäddad data ännu", "tr": "Henüz gömülü veri yok", "el": "Δεν υπάρχουν ενσωματωμένα δεδομένα",
        "ru": "Встроенных данных пока нет"
    },
    "channelAds": {
        "ar": "إعلانات القنوات", "en": "Channel Ads", "de": "Kanalwerbung", "de-AT": "Kanalwerbung",
        "fr": "Publicités de chaînes", "nl": "Kanaaladvertenties", "sv": "Kanalannonser",
        "tr": "Kanal Reklamları", "el": "Διαφημίσεις καναλιών", "ru": "Реклама каналов"
    },
    "channelAdsDesc": {
        "ar": "الإعلانات المقدمة من أصحاب القنوات للمراجعة والموافقة",
        "en": "Ads submitted by channel owners for review and approval",
        "de": "Von Kanalbesitzern eingereichte Werbung zur Prüfung", "de-AT": "Von Kanalbesitzern eingereichte Werbung zur Prüfung",
        "fr": "Publicités soumises par les propriétaires de chaînes", "nl": "Advertenties ingediend door kanaaleigenaren",
        "sv": "Annonser inskickade av kanalägare", "tr": "Kanal sahiplerinden gelen reklamlar",
        "el": "Διαφημίσεις από ιδιοκτήτες καναλιών", "ru": "Реклама от владельцев каналов"
    },
    "noAdsYet": {
        "ar": "لا توجد إعلانات بعد", "en": "No ads yet", "de": "Noch keine Werbung", "de-AT": "Noch keine Werbung",
        "fr": "Aucune publicité", "nl": "Nog geen advertenties", "sv": "Inga annonser ännu",
        "tr": "Henüz reklam yok", "el": "Δεν υπάρχουν διαφημίσεις", "ru": "Рекламы пока нет"
    },
    "pendingStatus": {
        "ar": "في الانتظار", "en": "Pending", "de": "Ausstehend", "de-AT": "Ausstehend",
        "fr": "En attente", "nl": "In afwachting", "sv": "Väntande", "tr": "Beklemede",
        "el": "Σε αναμονή", "ru": "Ожидание"
    },
    "viewsLabel": {
        "ar": "المشاهدات:", "en": "Views:", "de": "Aufrufe:", "de-AT": "Aufrufe:",
        "fr": "Vues :", "nl": "Weergaven:", "sv": "Visningar:", "tr": "Görüntülemeler:",
        "el": "Προβολές:", "ru": "Просмотры:"
    },
    "priceLabel": {
        "ar": "السعر:", "en": "Price:", "de": "Preis:", "de-AT": "Preis:",
        "fr": "Prix :", "nl": "Prijs:", "sv": "Pris:", "tr": "Fiyat:",
        "el": "Τιμή:", "ru": "Цена:"
    },
    "pointsUnit": {
        "ar": "نقطة", "en": "points", "de": "Punkte", "de-AT": "Punkte",
        "fr": "points", "nl": "punten", "sv": "poäng", "tr": "puan",
        "el": "πόντοι", "ru": "баллов"
    },
    "vendorRequests": {
        "ar": "طلبات البائعين", "en": "Vendor Requests", "de": "Händleranfragen", "de-AT": "Händleranfragen",
        "fr": "Demandes vendeurs", "nl": "Verkopersverzoeken", "sv": "Säljarförfrågningar",
        "tr": "Satıcı İstekleri", "el": "Αιτήσεις πωλητών", "ru": "Запросы продавцов"
    },
    "vendorNoPublish": {
        "ar": "لا يُنشر أي منتج إلا بعد موافقتك على البائع",
        "en": "No product is published without your approval of the vendor",
        "de": "Kein Produkt wird ohne Ihre Genehmigung veröffentlicht",
        "de-AT": "Kein Produkt wird ohne Ihre Genehmigung veröffentlicht",
        "fr": "Aucun produit n'est publié sans votre approbation",
        "nl": "Geen product wordt gepubliceerd zonder uw goedkeuring",
        "sv": "Ingen produkt publiceras utan ditt godkännande",
        "tr": "Hiçbir ürün satıcı onayınız olmadan yayınlanmaz",
        "el": "Κανένα προϊόν δεν δημοσιεύεται χωρίς την έγκρισή σας",
        "ru": "Ни один товар не публикуется без вашего одобрения продавца"
    },
    "noVendorRequests": {
        "ar": "لا توجد طلبات", "en": "No requests", "de": "Keine Anfragen", "de-AT": "Keine Anfragen",
        "fr": "Aucune demande", "nl": "Geen verzoeken", "sv": "Inga förfrågningar",
        "tr": "İstek yok", "el": "Δεν υπάρχουν αιτήσεις", "ru": "Нет запросов"
    },
    "revenueTitle": {
        "ar": "الإيرادات", "en": "Revenue", "de": "Einnahmen", "de-AT": "Einnahmen",
        "fr": "Revenus", "nl": "Inkomsten", "sv": "Intäkter", "tr": "Gelirler",
        "el": "Έσοδα", "ru": "Доходы"
    },
    "giftPointsRevenue": {
        "ar": "نقاط من الهدايا (50%)", "en": "Points from gifts (50%)", "de": "Punkte aus Geschenken (50%)",
        "de-AT": "Punkte aus Geschenken (50%)", "fr": "Points des cadeaux (50%)",
        "nl": "Punten van geschenken (50%)", "sv": "Poäng från gåvor (50%)",
        "tr": "Hediyelerden puanlar (%50)", "el": "Πόντοι από δώρα (50%)", "ru": "Баллы от подарков (50%)"
    },
    "electronicPayment": {
        "ar": "الدفع الإلكتروني", "en": "Electronic Payment", "de": "Elektronische Zahlung",
        "de-AT": "Elektronische Zahlung", "fr": "Paiement électronique", "nl": "Elektronische betaling",
        "sv": "Elektronisk betalning", "tr": "Elektronik Ödeme", "el": "Ηλεκτρονική πληρωμή",
        "ru": "Электронная оплата"
    },
    "infoLabel": {
        "ar": "معلومات", "en": "Info", "de": "Info", "de-AT": "Info",
        "fr": "Infos", "nl": "Info", "sv": "Info", "tr": "Bilgi",
        "el": "Πληροφορίες", "ru": "Информация"
    },
    "responsibleLabel": {
        "ar": "المسؤول:", "en": "Manager:", "de": "Verantwortlich:", "de-AT": "Verantwortlich:",
        "fr": "Responsable :", "nl": "Verantwoordelijke:", "sv": "Ansvarig:",
        "tr": "Sorumlu:", "el": "Υπεύθυνος:", "ru": "Ответственный:"
    },
    "aiLabel": {
        "ar": "الذكاء الاصطناعي:", "en": "AI:", "de": "KI:", "de-AT": "KI:",
        "fr": "IA :", "nl": "AI:", "sv": "AI:", "tr": "Yapay Zeka:",
        "el": "Τεχνητή νοημοσύνη:", "ru": "ИИ:"
    },
    "originalArabicText": {
        "ar": "النص العربي الأصلي...", "en": "Original Arabic text...", "de": "Originaltext auf Arabisch...",
        "de-AT": "Originaltext auf Arabisch...", "fr": "Texte arabe original...", "nl": "Originele Arabische tekst...",
        "sv": "Ursprunglig arabisk text...", "tr": "Orijinal Arapça metin...",
        "el": "Αρχικό αραβικό κείμενο...", "ru": "Оригинальный арабский текст..."
    },
    # Ruqyah category labels
    "ruqyahCatEye": {
        "ar": "عين", "en": "Evil Eye", "de": "Böser Blick", "de-AT": "Böser Blick",
        "fr": "Mauvais œil", "nl": "Boze oog", "sv": "Onda ögat", "tr": "Nazar",
        "el": "Κακό μάτι", "ru": "Сглаз"
    },
    "ruqyahCatEnvy": {
        "ar": "حسد", "en": "Envy", "de": "Neid", "de-AT": "Neid",
        "fr": "Envie", "nl": "Jaloezie", "sv": "Avundsjuka", "tr": "Haset",
        "el": "Φθόνος", "ru": "Зависть"
    },
    "ruqyahCatMagic": {
        "ar": "سحر", "en": "Magic/Sorcery", "de": "Magie/Zauberei", "de-AT": "Magie/Zauberei",
        "fr": "Magie/Sorcellerie", "nl": "Magie/Toverij", "sv": "Magi/Trolldom", "tr": "Büyü/Sihir",
        "el": "Μαγεία", "ru": "Колдовство"
    },
    "revenueHowItWorks": {
        "ar": "كيف يعمل نظام الإيرادات:", "en": "How the revenue system works:",
        "de": "So funktioniert das Einnahmensystem:", "de-AT": "So funktioniert das Einnahmensystem:",
        "fr": "Comment fonctionne le système de revenus :", "nl": "Hoe het inkomstensysteem werkt:",
        "sv": "Så fungerar intäktssystemet:", "tr": "Gelir sistemi nasıl çalışır:",
        "el": "Πώς λειτουργεί το σύστημα εσόδων:", "ru": "Как работает система доходов:"
    },
    "revenueRule1": {
        "ar": "عند إرسال هدية: 50% للإدارة و 50% لصانع المحتوى",
        "en": "When sending a gift: 50% for admin and 50% for content creator",
        "de": "Bei Geschenkversand: 50% für Admin und 50% für Inhaltsersteller",
        "de-AT": "Bei Geschenkversand: 50% für Admin und 50% für Inhaltsersteller",
        "fr": "Lors de l'envoi d'un cadeau : 50% pour l'admin et 50% pour le créateur",
        "nl": "Bij het sturen van een geschenk: 50% voor admin en 50% voor maker",
        "sv": "Vid gåva: 50% för admin och 50% för innehållsskapare",
        "tr": "Hediye gönderildiğinde: %50 yöneticiye ve %50 içerik üreticisine",
        "el": "Κατά την αποστολή δώρου: 50% στον διαχειριστή και 50% στον δημιουργό",
        "ru": "При отправке подарка: 50% администратору и 50% создателю контента"
    },
    "revenueRule2": {
        "ar": "المستخدمون يكسبون النقاط من الإعلانات والأنشطة",
        "en": "Users earn points from ads and activities",
        "de": "Benutzer verdienen Punkte durch Werbung und Aktivitäten",
        "de-AT": "Benutzer verdienen Punkte durch Werbung und Aktivitäten",
        "fr": "Les utilisateurs gagnent des points grâce aux publicités et activités",
        "nl": "Gebruikers verdienen punten via advertenties en activiteiten",
        "sv": "Användare tjänar poäng genom annonser och aktiviteter",
        "tr": "Kullanıcılar reklamlardan ve etkinliklerden puan kazanır",
        "el": "Οι χρήστες κερδίζουν πόντους από διαφημίσεις και δραστηριότητες",
        "ru": "Пользователи зарабатывают баллы от рекламы и активностей"
    },
    "revenueRule3": {
        "ar": "أصحاب القنوات يرفعون إعلانات وتحدد الإدارة السعر",
        "en": "Channel owners upload ads and admin sets the price",
        "de": "Kanalbesitzer laden Werbung hoch, Admin legt den Preis fest",
        "de-AT": "Kanalbesitzer laden Werbung hoch, Admin legt den Preis fest",
        "fr": "Les propriétaires de chaînes soumettent des publicités, l'admin fixe le prix",
        "nl": "Kanaaleigenaren uploaden advertenties, admin bepaalt de prijs",
        "sv": "Kanalägare laddar upp annonser, admin sätter priset",
        "tr": "Kanal sahipleri reklam yükler, yönetici fiyatı belirler",
        "el": "Οι ιδιοκτήτες καναλιών ανεβάζουν διαφημίσεις, ο admin ορίζει την τιμή",
        "ru": "Владельцы каналов загружают рекламу, администратор устанавливает цену"
    },
    "revenueRule4": {
        "ar": "عمولة السوق تُخصم تلقائياً من كل عملية بيع",
        "en": "Market commission is automatically deducted from each sale",
        "de": "Marktprovision wird automatisch von jedem Verkauf abgezogen",
        "de-AT": "Marktprovision wird automatisch von jedem Verkauf abgezogen",
        "fr": "La commission est automatiquement déduite de chaque vente",
        "nl": "Marktcommissie wordt automatisch afgetrokken van elke verkoop",
        "sv": "Marknadsprovision dras automatiskt från varje försäljning",
        "tr": "Pazar komisyonu her satıştan otomatik olarak düşülür",
        "el": "Η προμήθεια αφαιρείται αυτόματα από κάθε πώληση",
        "ru": "Комиссия автоматически вычитается из каждой продажи"
    },
}


def main():
    lang_files = {
        'ar': 'ar.json', 'en': 'en.json', 'de': 'de.json', 'de-AT': 'de-AT.json',
        'fr': 'fr.json', 'nl': 'nl.json', 'sv': 'sv.json', 'tr': 'tr.json',
        'el': 'el.json', 'ru': 'ru.json',
    }

    changes = {l: 0 for l in lang_files}
    for lang, fname in lang_files.items():
        with open(os.path.join(LOCALES_DIR, fname), 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for key, translations in ADMIN_KEYS.items():
            if lang in translations:
                if key not in data or data[key] != translations[lang]:
                    data[key] = translations[lang]
                    changes[lang] += 1
        
        with open(os.path.join(LOCALES_DIR, fname), 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write('\n')
        print(f"  {fname}: {changes[lang]} keys")

    print(f"\nTotal: {sum(changes.values())}")


if __name__ == '__main__':
    main()

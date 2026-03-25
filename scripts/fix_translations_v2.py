#!/usr/bin/env python3
"""
COMPREHENSIVE fix for all hardcoded Arabic text in components.
Adds translation keys and values for all 10 languages.
"""
import json
import os

LOCALES_DIR = '/app/frontend/src/locales'

# All new translation keys needed across all components
NEW_KEYS = {
    # ZakatCalculator
    "zakatBelowNisabDesc": {
        "ar": "أموالك ({total}) أقل من النصاب ({nisab})",
        "en": "Your wealth ({total}) is below the Nisab ({nisab})",
        "de": "Ihr Vermögen ({total}) liegt unter dem Nisab ({nisab})",
        "de-AT": "Ihr Vermögen ({total}) liegt unter dem Nisab ({nisab})",
        "fr": "Votre richesse ({total}) est inférieure au Nisab ({nisab})",
        "nl": "Uw vermogen ({total}) ligt onder de Nisab ({nisab})",
        "sv": "Din förmögenhet ({total}) är under Nisab ({nisab})",
        "tr": "Servetiniz ({total}) Nisab'ın ({nisab}) altında",
        "el": "Ο πλούτος σας ({total}) είναι κάτω από το Νισάμπ ({nisab})",
        "ru": "Ваше имущество ({total}) ниже нисаба ({nisab})"
    },

    # CreatePost
    "createPostTitle": {
        "ar": "إنشاء منشور",
        "en": "Create Post",
        "de": "Beitrag erstellen",
        "de-AT": "Beitrag erstellen",
        "fr": "Créer une publication",
        "nl": "Bericht aanmaken",
        "sv": "Skapa inlägg",
        "tr": "Gönderi Oluştur",
        "el": "Δημιουργία Δημοσίευσης",
        "ru": "Создать публикацию"
    },
    "publishBtn": {
        "ar": "نشر",
        "en": "Publish",
        "de": "Veröffentlichen",
        "de-AT": "Veröffentlichen",
        "fr": "Publier",
        "nl": "Publiceren",
        "sv": "Publicera",
        "tr": "Yayınla",
        "el": "Δημοσίευση",
        "ru": "Опубликовать"
    },
    "sharePlaceholder": {
        "ar": "شارك فكرتك مع المجتمع...",
        "en": "Share your thought with the community...",
        "de": "Teile deine Idee mit der Gemeinschaft...",
        "de-AT": "Teile deine Idee mit der Gemeinschaft...",
        "fr": "Partagez votre idée avec la communauté...",
        "nl": "Deel je gedachte met de gemeenschap...",
        "sv": "Dela din tanke med gemenskapen...",
        "tr": "Düşünceni toplulukla paylaş...",
        "el": "Μοιράσου τη σκέψη σου με την κοινότητα...",
        "ru": "Поделитесь своей мыслью с сообществом..."
    },
    "addMediaBtn": {
        "ar": "إضافة صورة أو فيديو",
        "en": "Add photo or video",
        "de": "Foto oder Video hinzufügen",
        "de-AT": "Foto oder Video hinzufügen",
        "fr": "Ajouter une photo ou vidéo",
        "nl": "Foto of video toevoegen",
        "sv": "Lägg till foto eller video",
        "tr": "Fotoğraf veya video ekle",
        "el": "Προσθήκη φωτογραφίας ή βίντεο",
        "ru": "Добавить фото или видео"
    },
    "uploadError": {
        "ar": "فشل في رفع الملف",
        "en": "File upload failed",
        "de": "Datei-Upload fehlgeschlagen",
        "de-AT": "Datei-Upload fehlgeschlagen",
        "fr": "Échec du téléchargement du fichier",
        "nl": "Bestandsupload mislukt",
        "sv": "Filuppladdning misslyckades",
        "tr": "Dosya yükleme başarısız",
        "el": "Αποτυχία μεταφόρτωσης αρχείου",
        "ru": "Ошибка загрузки файла"
    },
    "writeFirst": {
        "ar": "اكتب شيئاً أولاً",
        "en": "Write something first",
        "de": "Schreibe zuerst etwas",
        "de-AT": "Schreibe zuerst etwas",
        "fr": "Écrivez quelque chose d'abord",
        "nl": "Schrijf eerst iets",
        "sv": "Skriv något först",
        "tr": "Önce bir şey yazın",
        "el": "Γράψε κάτι πρώτα",
        "ru": "Сначала напишите что-нибудь"
    },
    "publishError": {
        "ar": "حدث خطأ أثناء النشر",
        "en": "An error occurred while publishing",
        "de": "Beim Veröffentlichen ist ein Fehler aufgetreten",
        "de-AT": "Beim Veröffentlichen ist ein Fehler aufgetreten",
        "fr": "Une erreur s'est produite lors de la publication",
        "nl": "Er is een fout opgetreden bij het publiceren",
        "sv": "Ett fel uppstod vid publicering",
        "tr": "Yayınlarken bir hata oluştu",
        "el": "Σφάλμα κατά τη δημοσίευση",
        "ru": "Произошла ошибка при публикации"
    },
    "publishSuccess": {
        "ar": "تم النشر بنجاح! ✨",
        "en": "Published successfully! ✨",
        "de": "Erfolgreich veröffentlicht! ✨",
        "de-AT": "Erfolgreich veröffentlicht! ✨",
        "fr": "Publié avec succès ! ✨",
        "nl": "Succesvol gepubliceerd! ✨",
        "sv": "Publicerat! ✨",
        "tr": "Başarıyla yayınlandı! ✨",
        "el": "Δημοσιεύτηκε επιτυχώς! ✨",
        "ru": "Успешно опубликовано! ✨"
    },
    "publishFailed": {
        "ar": "فشل في النشر",
        "en": "Publishing failed",
        "de": "Veröffentlichung fehlgeschlagen",
        "de-AT": "Veröffentlichung fehlgeschlagen",
        "fr": "Échec de la publication",
        "nl": "Publicatie mislukt",
        "sv": "Publicering misslyckades",
        "tr": "Yayınlama başarısız",
        "el": "Αποτυχία δημοσίευσης",
        "ru": "Ошибка публикации"
    },
    "textOption": {
        "ar": "نص",
        "en": "Text",
        "de": "Text",
        "de-AT": "Text",
        "fr": "Texte",
        "nl": "Tekst",
        "sv": "Text",
        "tr": "Metin",
        "el": "Κείμενο",
        "ru": "Текст"
    },
    "reelsOption": {
        "ar": "ريلز",
        "en": "Reels",
        "de": "Reels",
        "de-AT": "Reels",
        "fr": "Reels",
        "nl": "Reels",
        "sv": "Reels",
        "tr": "Reels",
        "el": "Reels",
        "ru": "Reels"
    },
    # SocialProfile
    "giftsLabel": {
        "ar": "الهدايا",
        "en": "Gifts",
        "de": "Geschenke",
        "de-AT": "Geschenke",
        "fr": "Cadeaux",
        "nl": "Geschenken",
        "sv": "Gåvor",
        "tr": "Hediyeler",
        "el": "Δώρα",
        "ru": "Подарки"
    },
    "editProfile": {
        "ar": "تعديل الملف الشخصي",
        "en": "Edit Profile",
        "de": "Profil bearbeiten",
        "de-AT": "Profil bearbeiten",
        "fr": "Modifier le profil",
        "nl": "Profiel bewerken",
        "sv": "Redigera profil",
        "tr": "Profili Düzenle",
        "el": "Επεξεργασία Προφίλ",
        "ru": "Редактировать профиль"
    },
    "followingLabel": {
        "ar": "متابَع ✓",
        "en": "Following ✓",
        "de": "Folge ich ✓",
        "de-AT": "Folge ich ✓",
        "fr": "Abonné ✓",
        "nl": "Volgend ✓",
        "sv": "Följer ✓",
        "tr": "Takip Ediliyor ✓",
        "el": "Ακολουθώ ✓",
        "ru": "Подписан ✓"
    },
    "chatLabel": {
        "ar": "المحادثة",
        "en": "Chat",
        "de": "Chat",
        "de-AT": "Chat",
        "fr": "Discussion",
        "nl": "Chat",
        "sv": "Chatt",
        "tr": "Mesaj",
        "el": "Συνομιλία",
        "ru": "Чат"
    },
    "postsTab": {
        "ar": "المنشورات",
        "en": "Posts",
        "de": "Beiträge",
        "de-AT": "Beiträge",
        "fr": "Publications",
        "nl": "Berichten",
        "sv": "Inlägg",
        "tr": "Gönderiler",
        "el": "Δημοσιεύσεις",
        "ru": "Публикации"
    },
    "infoTab": {
        "ar": "المعلومات",
        "en": "Info",
        "de": "Info",
        "de-AT": "Info",
        "fr": "Infos",
        "nl": "Info",
        "sv": "Info",
        "tr": "Bilgi",
        "el": "Πληροφορίες",
        "ru": "Информация"
    },
    "noPostsYet": {
        "ar": "لا توجد منشورات حتى الآن",
        "en": "No posts yet",
        "de": "Noch keine Beiträge",
        "de-AT": "Noch keine Beiträge",
        "fr": "Aucune publication pour le moment",
        "nl": "Nog geen berichten",
        "sv": "Inga inlägg ännu",
        "tr": "Henüz gönderi yok",
        "el": "Δεν υπάρχουν δημοσιεύσεις ακόμα",
        "ru": "Публикаций пока нет"
    },
    # MosquePrayerTimes keys
    "mosquePrayerFajr": {
        "ar": "الفجر", "en": "Fajr", "de": "Fajr", "de-AT": "Fajr",
        "fr": "Fajr", "nl": "Fajr", "sv": "Fajr", "tr": "Fecir",
        "el": "Φατζρ", "ru": "Фаджр"
    },
    "mosquePrayerSunrise": {
        "ar": "الشروق", "en": "Sunrise", "de": "Sonnenaufgang", "de-AT": "Sonnenaufgang",
        "fr": "Lever du soleil", "nl": "Zonsopgang", "sv": "Soluppgång", "tr": "Güneş",
        "el": "Ανατολή", "ru": "Восход"
    },
    "mosquePrayerDhuhr": {
        "ar": "الظهر", "en": "Dhuhr", "de": "Dhuhr", "de-AT": "Dhuhr",
        "fr": "Dhuhr", "nl": "Dhuhr", "sv": "Dhuhr", "tr": "Öğle",
        "el": "Ντουχρ", "ru": "Зухр"
    },
    "mosquePrayerAsr": {
        "ar": "العصر", "en": "Asr", "de": "Asr", "de-AT": "Asr",
        "fr": "Asr", "nl": "Asr", "sv": "Asr", "tr": "İkindi",
        "el": "Ασρ", "ru": "Аср"
    },
    "mosquePrayerMaghrib": {
        "ar": "المغرب", "en": "Maghrib", "de": "Maghrib", "de-AT": "Maghrib",
        "fr": "Maghrib", "nl": "Maghrib", "sv": "Maghrib", "tr": "Akşam",
        "el": "Μαγκρίμπ", "ru": "Магриб"
    },
    "mosquePrayerIsha": {
        "ar": "العشاء", "en": "Isha", "de": "Isha", "de-AT": "Isha",
        "fr": "Isha", "nl": "Isha", "sv": "Isha", "tr": "Yatsı",
        "el": "Ίσα", "ru": "Иша"
    },
    "mosquePrayerJumuah": {
        "ar": "الجمعة", "en": "Jumuah", "de": "Jumu'a", "de-AT": "Jumu'a",
        "fr": "Jumu'a", "nl": "Jumu'a", "sv": "Jumu'a", "tr": "Cuma",
        "el": "Τζουμούα", "ru": "Джума"
    },
    "locatingPosition": {
        "ar": "جارٍ تحديد الموقع...",
        "en": "Locating...",
        "de": "Standort wird ermittelt...",
        "de-AT": "Standort wird ermittelt...",
        "fr": "Localisation en cours...",
        "nl": "Locatie bepalen...",
        "sv": "Lokaliserar...",
        "tr": "Konum belirleniyor...",
        "el": "Εντοπισμός θέσης...",
        "ru": "Определение местоположения..."
    },
    "adjustMinutes": {
        "ar": "ضبط فرق الدقائق",
        "en": "Adjust minute differences",
        "de": "Minutenunterschiede anpassen",
        "de-AT": "Minutenunterschiede anpassen",
        "fr": "Ajuster les différences de minutes",
        "nl": "Minutenverschillen aanpassen",
        "sv": "Justera minutskillnader",
        "tr": "Dakika farklarını ayarla",
        "el": "Ρύθμιση διαφορών λεπτών",
        "ru": "Настроить разницу минут"
    },
    "shareTimes": {
        "ar": "مشاركة الأوقات",
        "en": "Share prayer times",
        "de": "Gebetszeiten teilen",
        "de-AT": "Gebetszeiten teilen",
        "fr": "Partager les horaires de prière",
        "nl": "Gebetstijden delen",
        "sv": "Dela bönetider",
        "tr": "Namaz vakitlerini paylaş",
        "el": "Κοινοποίηση ωρών προσευχής",
        "ru": "Поделиться временем молитвы"
    },
    "telegram": {
        "ar": "تيليجرام", "en": "Telegram", "de": "Telegram", "de-AT": "Telegram",
        "fr": "Telegram", "nl": "Telegram", "sv": "Telegram", "tr": "Telegram",
        "el": "Telegram", "ru": "Telegram"
    },
    "messenger": {
        "ar": "ماسنجر", "en": "Messenger", "de": "Messenger", "de-AT": "Messenger",
        "fr": "Messenger", "nl": "Messenger", "sv": "Messenger", "tr": "Messenger",
        "el": "Messenger", "ru": "Messenger"
    },
    "otherShare": {
        "ar": "مشاركة أخرى...",
        "en": "Other share...",
        "de": "Andere Freigabe...",
        "de-AT": "Andere Freigabe...",
        "fr": "Autre partage...",
        "nl": "Ander delen...",
        "sv": "Annat delning...",
        "tr": "Diğer paylaşım...",
        "el": "Άλλη κοινοποίηση...",
        "ru": "Другой способ..."
    },
    "copyText": {
        "ar": "نسخ النص",
        "en": "Copy text",
        "de": "Text kopieren",
        "de-AT": "Text kopieren",
        "fr": "Copier le texte",
        "nl": "Tekst kopiëren",
        "sv": "Kopiera text",
        "tr": "Metni kopyala",
        "el": "Αντιγραφή κειμένου",
        "ru": "Скопировать текст"
    },
    "saveBtn": {
        "ar": "حفظ",
        "en": "Save",
        "de": "Speichern",
        "de-AT": "Speichern",
        "fr": "Enregistrer",
        "nl": "Opslaan",
        "sv": "Spara",
        "tr": "Kaydet",
        "el": "Αποθήκευση",
        "ru": "Сохранить"
    },
    "manualTimesStored": {
        "ar": "أوقات يدوية محفوظة",
        "en": "Manual times saved",
        "de": "Manuelle Zeiten gespeichert",
        "de-AT": "Manuelle Zeiten gespeichert",
        "fr": "Horaires manuels enregistrés",
        "nl": "Handmatige tijden opgeslagen",
        "sv": "Manuella tider sparade",
        "tr": "Manuel vakitler kaydedildi",
        "el": "Χειροκίνητοι χρόνοι αποθηκεύτηκαν",
        "ru": "Ручные значения сохранены"
    },
    "liveFromMawaqit": {
        "ar": "⚡ أوقات مباشرة من Mawaqit",
        "en": "⚡ Live times from Mawaqit",
        "de": "⚡ Live-Zeiten von Mawaqit",
        "de-AT": "⚡ Live-Zeiten von Mawaqit",
        "fr": "⚡ Horaires en direct de Mawaqit",
        "nl": "⚡ Live tijden van Mawaqit",
        "sv": "⚡ Live-tider från Mawaqit",
        "tr": "⚡ Mawaqit'ten canlı vakitler",
        "el": "⚡ Ζωντανοί χρόνοι από Mawaqit",
        "ru": "⚡ Онлайн-время от Mawaqit"
    },
    "timesFromWebsite": {
        "ar": "🌐 أوقات من موقع المسجد",
        "en": "🌐 Times from mosque website",
        "de": "🌐 Zeiten von der Moschee-Website",
        "de-AT": "🌐 Zeiten von der Moschee-Website",
        "fr": "🌐 Horaires du site de la mosquée",
        "nl": "🌐 Tijden van de moskee-website",
        "sv": "🌐 Tider från moskéns webbplats",
        "tr": "🌐 Cami web sitesinden vakitler",
        "el": "🌐 Ωράρια από τον ιστότοπο τζαμιού",
        "ru": "🌐 Время с сайта мечети"
    },
    "calculatedTimes": {
        "ar": "⏳ أوقات حسابية — يمكنك تعديلها يدوياً",
        "en": "⏳ Calculated times — you can adjust manually",
        "de": "⏳ Berechnete Zeiten — manuell anpassbar",
        "de-AT": "⏳ Berechnete Zeiten — manuell anpassbar",
        "fr": "⏳ Horaires calculés — ajustables manuellement",
        "nl": "⏳ Berekende tijden — handmatig aanpasbaar",
        "sv": "⏳ Beräknade tider — kan justeras manuellt",
        "tr": "⏳ Hesaplanan vakitler — manuel olarak düzenleyebilirsiniz",
        "el": "⏳ Υπολογισμένοι χρόνοι — μπορείτε να τους ρυθμίσετε",
        "ru": "⏳ Расчётное время — можно настроить вручную"
    },
    "adjustedTimes": {
        "ar": "⏱️ أوقات معدلة (تحديث يومي تلقائي)",
        "en": "⏱️ Adjusted times (automatic daily update)",
        "de": "⏱️ Angepasste Zeiten (automatische tägliche Aktualisierung)",
        "de-AT": "⏱️ Angepasste Zeiten (automatische tägliche Aktualisierung)",
        "fr": "⏱️ Horaires ajustés (mise à jour quotidienne automatique)",
        "nl": "⏱️ Aangepaste tijden (automatische dagelijkse update)",
        "sv": "⏱️ Justerade tider (automatisk daglig uppdatering)",
        "tr": "⏱️ Düzeltilmiş vakitler (otomatik günlük güncelleme)",
        "el": "⏱️ Προσαρμοσμένοι χρόνοι (αυτόματη ημερήσια ενημέρωση)",
        "ru": "⏱️ Скорректированное время (автоматическое ежедневное обновление)"
    },
    "resetToAuto": {
        "ar": "إعادة للتلقائي",
        "en": "Reset to auto",
        "de": "Zurücksetzen auf automatisch",
        "de-AT": "Zurücksetzen auf automatisch",
        "fr": "Réinitialiser en automatique",
        "nl": "Terug naar automatisch",
        "sv": "Återställ till automatisk",
        "tr": "Otomatiğe sıfırla",
        "el": "Επαναφορά σε αυτόματο",
        "ru": "Сбросить на автоматическое"
    },
    "nextPrayerIn": {
        "ar": "بعد",
        "en": "in",
        "de": "in",
        "de-AT": "in",
        "fr": "dans",
        "nl": "over",
        "sv": "om",
        "tr": "sonra",
        "el": "σε",
        "ru": "через"
    },
    "editModeManual": {
        "ar": "📝 وضع التعديل: أدخل أوقات الصلاة يدوياً",
        "en": "📝 Edit mode: Enter prayer times manually",
        "de": "📝 Bearbeitungsmodus: Gebetszeiten manuell eingeben",
        "de-AT": "📝 Bearbeitungsmodus: Gebetszeiten manuell eingeben",
        "fr": "📝 Mode édition : Saisir les horaires manuellement",
        "nl": "📝 Bewerkingsmodus: Gebetstijden handmatig invoeren",
        "sv": "📝 Redigeringsläge: Ange bönetider manuellt",
        "tr": "📝 Düzenleme modu: Namaz vakitlerini manuel girin",
        "el": "📝 Λειτουργία επεξεργασίας: Εισάγετε ώρες προσευχής χειροκίνητα",
        "ru": "📝 Режим редактирования: Введите время молитв вручную"
    },
    "editModeDiffs": {
        "ar": "⏱️ وضع فرق الدقائق: حدد كم دقيقة يتقدم (+) أو يتأخر (-) كل وقت عن التوقيت الفلكي",
        "en": "⏱️ Minute offset mode: Set how many minutes each prayer time is ahead (+) or behind (-) the astronomical time",
        "de": "⏱️ Minuten-Offset-Modus: Legen Sie fest, wie viele Minuten jede Gebetszeit vor (+) oder nach (-) der astronomischen Zeit liegt",
        "de-AT": "⏱️ Minuten-Offset-Modus: Legen Sie fest, wie viele Minuten jede Gebetszeit vor (+) oder nach (-) der astronomischen Zeit liegt",
        "fr": "⏱️ Mode décalage minutes : Définissez combien de minutes chaque horaire est en avance (+) ou en retard (-)",
        "nl": "⏱️ Minuten-offsetmodus: Stel in hoeveel minuten elk gebetstijd voor (+) of achter (-) loopt",
        "sv": "⏱️ Minutavvikelseläge: Ange hur många minuter varje bönetid är före (+) eller efter (-)",
        "tr": "⏱️ Dakika farkı modu: Her namaz vaktinin astronomik saatten kaç dakika önce (+) veya sonra (-) olduğunu belirleyin",
        "el": "⏱️ Λειτουργία αντιστάθμισης λεπτών: Ορίστε πόσα λεπτά κάθε ώρα προσευχής είναι μπροστά (+) ή πίσω (-)",
        "ru": "⏱️ Режим смещения минут: Укажите на сколько минут каждое время молитвы опережает (+) или отстаёт (-)"
    },
    "filterAuto": {
        "ar": "⚡ تلقائي",
        "en": "⚡ Auto",
        "de": "⚡ Automatisch",
        "de-AT": "⚡ Automatisch",
        "fr": "⚡ Auto",
        "nl": "⚡ Automatisch",
        "sv": "⚡ Auto",
        "tr": "⚡ Otomatik",
        "el": "⚡ Αυτόματο",
        "ru": "⚡ Авто"
    },
    "filterManual": {
        "ar": "✏️ يدوي",
        "en": "✏️ Manual",
        "de": "✏️ Manuell",
        "de-AT": "✏️ Manuell",
        "fr": "✏️ Manuel",
        "nl": "✏️ Handmatig",
        "sv": "✏️ Manuell",
        "tr": "✏️ Manuel",
        "el": "✏️ Χειροκίνητο",
        "ru": "✏️ Вручную"
    },
    "nearbyMosques": {
        "ar": "المساجد المحيطة بك",
        "en": "Nearby mosques",
        "de": "Moscheen in der Nähe",
        "de-AT": "Moscheen in der Nähe",
        "fr": "Mosquées à proximité",
        "nl": "Moskeeën in de buurt",
        "sv": "Närliggande moskéer",
        "tr": "Yakındaki camiler",
        "el": "Κοντινά τζαμιά",
        "ru": "Ближайшие мечети"
    },
    "checkingLabel": {
        "ar": "جاري الفحص...",
        "en": "Checking...",
        "de": "Wird geprüft...",
        "de-AT": "Wird geprüft...",
        "fr": "Vérification...",
        "nl": "Controleren...",
        "sv": "Kontrollerar...",
        "tr": "Kontrol ediliyor...",
        "el": "Έλεγχος...",
        "ru": "Проверка..."
    },
    "autoTimesAvailable": {
        "ar": "⚡ أوقات تلقائية متوفرة",
        "en": "⚡ Auto times available",
        "de": "⚡ Automatische Zeiten verfügbar",
        "de-AT": "⚡ Automatische Zeiten verfügbar",
        "fr": "⚡ Horaires automatiques disponibles",
        "nl": "⚡ Automatische tijden beschikbaar",
        "sv": "⚡ Automatiska tider tillgängliga",
        "tr": "⚡ Otomatik vakitler mevcut",
        "el": "⚡ Αυτόματοι χρόνοι διαθέσιμοι",
        "ru": "⚡ Автоматическое время доступно"
    },
    "manualOnly": {
        "ar": "يدوي فقط",
        "en": "Manual only",
        "de": "Nur manuell",
        "de-AT": "Nur manuell",
        "fr": "Manuel uniquement",
        "nl": "Alleen handmatig",
        "sv": "Endast manuell",
        "tr": "Sadece manuel",
        "el": "Μόνο χειροκίνητα",
        "ru": "Только вручную"
    },
    "checkBtn": {
        "ar": "فحص",
        "en": "Check",
        "de": "Prüfen",
        "de-AT": "Prüfen",
        "fr": "Vérifier",
        "nl": "Controleren",
        "sv": "Kontrollera",
        "tr": "Kontrol et",
        "el": "Έλεγχος",
        "ru": "Проверить"
    },
    "trySearchExpand": {
        "ar": "جرّب البحث بالاسم أو توسيع نطاق البحث",
        "en": "Try searching by name or expanding the search area",
        "de": "Versuchen Sie, nach Name zu suchen oder den Suchbereich zu erweitern",
        "de-AT": "Versuchen Sie, nach Name zu suchen oder den Suchbereich zu erweitern",
        "fr": "Essayez de rechercher par nom ou d'élargir la zone de recherche",
        "nl": "Probeer op naam te zoeken of het zoekgebied uit te breiden",
        "sv": "Försök söka efter namn eller utöka sökområdet",
        "tr": "İsimle aramayı veya arama alanını genişletmeyi deneyin",
        "el": "Δοκιμάστε αναζήτηση με όνομα ή επεκτείνετε την περιοχή αναζήτησης",
        "ru": "Попробуйте поиск по названию или расширьте область поиска"
    },
    "mosqueNoOnlineTimes": {
        "ar": "بعض المساجد لا تتوفر أوقاتها على الإنترنت. يمكنك:",
        "en": "Some mosques don't have online prayer times. You can:",
        "de": "Einige Moscheen haben keine Online-Gebetszeiten. Sie können:",
        "de-AT": "Einige Moscheen haben keine Online-Gebetszeiten. Sie können:",
        "fr": "Certaines mosquées n'ont pas d'horaires en ligne. Vous pouvez :",
        "nl": "Sommige moskeeën hebben geen online gebetstijden. U kunt:",
        "sv": "Vissa moskéer har inte bönetider online. Du kan:",
        "tr": "Bazı camilerin çevrimiçi namaz vakitleri yok. Şunları yapabilirsiniz:",
        "el": "Κάποια τζαμιά δεν έχουν ωράρια online. Μπορείτε:",
        "ru": "У некоторых мечетей нет онлайн-времени. Вы можете:"
    },
    "enterTimesManually": {
        "ar": "إدخال الأوقات يدوياً مرة واحدة",
        "en": "Enter times manually once",
        "de": "Zeiten einmalig manuell eingeben",
        "de-AT": "Zeiten einmalig manuell eingeben",
        "fr": "Saisir les horaires manuellement une fois",
        "nl": "Tijden eenmalig handmatig invoeren",
        "sv": "Ange tider manuellt en gång",
        "tr": "Vakitleri bir kez manuel olarak girin",
        "el": "Εισάγετε χρόνους χειροκίνητα μία φορά",
        "ru": "Ввести время вручную один раз"
    },
    "setMinuteOffset": {
        "ar": "أو ضبط فرق الدقائق عن التوقيت الفلكي (مثال: +5 للفجر)",
        "en": "Or set the minute offset from astronomical time (e.g., +5 for Fajr)",
        "de": "Oder den Minutenversatz zur astronomischen Zeit einstellen (z.B. +5 für Fajr)",
        "de-AT": "Oder den Minutenversatz zur astronomischen Zeit einstellen (z.B. +5 für Fajr)",
        "fr": "Ou définir le décalage en minutes par rapport à l'heure astronomique (ex: +5 pour Fajr)",
        "nl": "Of stel de minutenafwijking in ten opzichte van de astronomische tijd (bijv. +5 voor Fajr)",
        "sv": "Eller ställ in minutavvikelsen från astronomisk tid (t.ex. +5 för Fajr)",
        "tr": "Veya astronomik saatten dakika farkını ayarlayın (örn: Fecir için +5)",
        "el": "Ή ορίστε την αντιστάθμιση λεπτών από τον αστρονομικό χρόνο (π.χ., +5 για Φατζρ)",
        "ru": "Или установите смещение минут от астрономического времени (напр., +5 для Фаджр)"
    },
    "autoUpdateDaily": {
        "ar": "سيتم التحديث تلقائياً يومياً بناءً على إعداداتك",
        "en": "Will update automatically daily based on your settings",
        "de": "Wird täglich automatisch basierend auf Ihren Einstellungen aktualisiert",
        "de-AT": "Wird täglich automatisch basierend auf Ihren Einstellungen aktualisiert",
        "fr": "Mise à jour automatique quotidienne selon vos paramètres",
        "nl": "Wordt dagelijks automatisch bijgewerkt op basis van uw instellingen",
        "sv": "Uppdateras automatiskt dagligen baserat på dina inställningar",
        "tr": "Ayarlarınıza göre günlük otomatik güncellenecektir",
        "el": "Θα ενημερώνεται αυτόματα καθημερινά σύμφωνα με τις ρυθμίσεις σας",
        "ru": "Будет обновляться ежедневно автоматически на основе ваших настроек"
    },
    "mawaqitSuccess": {
        "ar": "تم سحب الأوقات من Mawaqit ✅",
        "en": "Times fetched from Mawaqit ✅",
        "de": "Zeiten von Mawaqit abgerufen ✅",
        "de-AT": "Zeiten von Mawaqit abgerufen ✅",
        "fr": "Horaires récupérés de Mawaqit ✅",
        "nl": "Tijden opgehaald van Mawaqit ✅",
        "sv": "Tider hämtade från Mawaqit ✅",
        "tr": "Mawaqit'ten vakitler alındı ✅",
        "el": "Χρόνοι ανακτήθηκαν από Mawaqit ✅",
        "ru": "Время получено из Mawaqit ✅"
    },
    # RamadanChallenge
    "ramadanChallengeTitle": {
        "ar": "تحدي رمضان",
        "en": "Ramadan Challenge",
        "de": "Ramadan-Herausforderung",
        "de-AT": "Ramadan-Herausforderung",
        "fr": "Défi du Ramadan",
        "nl": "Ramadan-uitdaging",
        "sv": "Ramadan-utmaning",
        "tr": "Ramazan Mücadelesi",
        "el": "Πρόκληση Ραμαδάν",
        "ru": "Испытание Рамадана"
    },
    "dayLabel": {
        "ar": "يوم",
        "en": "Day",
        "de": "Tag",
        "de-AT": "Tag",
        "fr": "Jour",
        "nl": "Dag",
        "sv": "Dag",
        "tr": "Gün",
        "el": "Ημέρα",
        "ru": "День"
    },
}


def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')


def main():
    lang_files = {
        'ar': 'ar.json', 'en': 'en.json', 'de': 'de.json', 'de-AT': 'de-AT.json',
        'fr': 'fr.json', 'nl': 'nl.json', 'sv': 'sv.json', 'tr': 'tr.json',
        'el': 'el.json', 'ru': 'ru.json',
    }

    data = {}
    for lang, fname in lang_files.items():
        data[lang] = load_json(os.path.join(LOCALES_DIR, fname))

    changes = {l: 0 for l in lang_files}

    # Add all new keys
    for key, translations in NEW_KEYS.items():
        for lang in lang_files:
            if lang in translations:
                if key not in data[lang] or data[lang][key] != translations[lang]:
                    data[lang][key] = translations[lang]
                    changes[lang] += 1

    # Save
    for lang, fname in lang_files.items():
        save_json(os.path.join(LOCALES_DIR, fname), data[lang])
        print(f"  {fname}: {changes[lang]} keys added/updated")

    print(f"\nTotal new keys added: {sum(changes.values())}")


if __name__ == '__main__':
    main()

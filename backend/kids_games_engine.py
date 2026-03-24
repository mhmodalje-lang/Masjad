"""
Kids Game Engine — Generates interactive game data from curriculum content.
Supports: Quiz, Memory, DragDrop, BubblePop, Scenario games.
All content localized in 9 languages.
"""
import random
import json
import os
from datetime import datetime

# ═══════ GAME CONTENT DATABASE ═══════

WUDU_STEPS = {
    "ar": ["النية", "غسل اليدين", "المضمضة", "الاستنشاق", "غسل الوجه", "غسل اليدين إلى المرفقين", "مسح الرأس", "غسل القدمين"],
    "en": ["Intention (Niyyah)", "Wash Hands (3x)", "Rinse Mouth (3x)", "Sniff Water in Nose (3x)", "Wash Face (3x)", "Wash Arms to Elbows (3x)", "Wipe Head", "Wash Feet (3x)"],
    "fr": ["Intention (Niyyah)", "Laver les mains (3x)", "Rincer la bouche (3x)", "Aspirer l'eau par le nez (3x)", "Laver le visage (3x)", "Laver les bras jusqu'aux coudes (3x)", "Essuyer la tête", "Laver les pieds (3x)"],
    "de": ["Absicht (Niyyah)", "Hände waschen (3x)", "Mund ausspülen (3x)", "Wasser in die Nase ziehen (3x)", "Gesicht waschen (3x)", "Arme bis Ellbogen waschen (3x)", "Kopf wischen", "Füße waschen (3x)"],
    "tr": ["Niyet", "Elleri yıkamak (3x)", "Ağzı çalkalamak (3x)", "Burna su çekmek (3x)", "Yüzü yıkamak (3x)", "Kolları dirseklere kadar yıkamak (3x)", "Başı meshetmek", "Ayakları yıkamak (3x)"],
    "ru": ["Намерение (Ният)", "Мытьё рук (3x)", "Полоскание рта (3x)", "Промывание носа (3x)", "Мытьё лица (3x)", "Мытьё рук до локтей (3x)", "Протирание головы", "Мытьё ног (3x)"],
    "sv": ["Avsikt (Niyyah)", "Tvätta händerna (3x)", "Skölj munnen (3x)", "Sniffa vatten i näsan (3x)", "Tvätta ansiktet (3x)", "Tvätta armarna till armbågarna (3x)", "Torka huvudet", "Tvätta fötterna (3x)"],
    "nl": ["Intentie (Niyyah)", "Handen wassen (3x)", "Mond spoelen (3x)", "Water in neus snuiven (3x)", "Gezicht wassen (3x)", "Armen tot ellebogen wassen (3x)", "Hoofd afvegen", "Voeten wassen (3x)"],
    "el": ["Πρόθεση (Νιγιάχ)", "Πλύσιμο χεριών (3x)", "Ξέπλυμα στόματος (3x)", "Εισπνοή νερού στη μύτη (3x)", "Πλύσιμο προσώπου (3x)", "Πλύσιμο χεριών ως αγκώνες (3x)", "Σκούπισμα κεφαλιού", "Πλύσιμο ποδιών (3x)"],
}

SALAH_STEPS = {
    "ar": ["تكبيرة الإحرام", "قراءة الفاتحة", "الركوع", "الرفع من الركوع", "السجود", "الجلوس بين السجدتين", "السجود الثاني", "التشهد والسلام"],
    "en": ["Takbir (Allahu Akbar)", "Recite Al-Fatiha", "Bow (Ruku)", "Rise from Bowing", "Prostrate (Sujud)", "Sit between Prostrations", "Second Prostration", "Tashahhud & Salam"],
    "fr": ["Takbir (Allahu Akbar)", "Réciter Al-Fatiha", "Inclination (Ruku)", "Se relever de l'inclination", "Prosternation (Sujud)", "S'asseoir entre les prosternations", "Deuxième prosternation", "Tashahhud et Salam"],
    "de": ["Takbir (Allahu Akbar)", "Al-Fatiha rezitieren", "Verbeugung (Ruku)", "Aufstehen von der Verbeugung", "Niederwerfung (Sujud)", "Sitzen zwischen den Niederwerfungen", "Zweite Niederwerfung", "Tashahhud und Salam"],
    "tr": ["Tekbir (Allahu Ekber)", "Fatiha Okumak", "Rükû", "Rükûdan Kalkmak", "Secde", "İki Secde Arası Oturuş", "İkinci Secde", "Tahiyyat ve Selam"],
    "ru": ["Такбир (Аллаху Акбар)", "Чтение Аль-Фатихи", "Поклон (Руку)", "Подъём от поклона", "Земной поклон (Суджуд)", "Сидение между поклонами", "Второй земной поклон", "Ташаххуд и Салам"],
    "sv": ["Takbir (Allahu Akbar)", "Recitera Al-Fatiha", "Buga (Ruku)", "Resa sig från bugning", "Prostration (Sujud)", "Sitta mellan prostrationerna", "Andra prostrationen", "Tashahhud och Salam"],
    "nl": ["Takbir (Allahu Akbar)", "Al-Fatiha reciteren", "Buigen (Ruku)", "Opstaan van buiging", "Prosternatie (Sujud)", "Zitten tussen prosternaties", "Tweede prosternatie", "Tashahhud en Salam"],
    "el": ["Τακμπίρ (Αλλάχου Άκμπαρ)", "Απαγγελία Αλ-Φάτιχα", "Υπόκλιση (Ρουκού)", "Ανύψωση από υπόκλιση", "Προσκύνηση (Σουτζούντ)", "Κάθισμα μεταξύ προσκυνήσεων", "Δεύτερη προσκύνηση", "Τασαχχούντ και Σαλάμ"],
}

PILLARS_OF_ISLAM = {
    "ar": ["الشهادة", "الصلاة", "الزكاة", "الصيام", "الحج"],
    "en": ["Shahada (Declaration of Faith)", "Salah (Prayer)", "Zakat (Charity)", "Sawm (Fasting)", "Hajj (Pilgrimage)"],
    "fr": ["Chahada (Déclaration de foi)", "Salat (Prière)", "Zakat (Aumône)", "Sawm (Jeûne)", "Hajj (Pèlerinage)"],
    "de": ["Shahada (Glaubensbekenntnis)", "Salah (Gebet)", "Zakat (Almosen)", "Sawm (Fasten)", "Hajj (Pilgerfahrt)"],
    "tr": ["Şehadet", "Namaz", "Zekât", "Oruç", "Hac"],
    "ru": ["Шахада (Свидетельство)", "Салят (Молитва)", "Закят (Милостыня)", "Саум (Пост)", "Хадж (Паломничество)"],
    "sv": ["Shahada (Trosbekännelse)", "Salah (Bön)", "Zakat (Allmosor)", "Sawm (Fasta)", "Hajj (Pilgrimsfärd)"],
    "nl": ["Shahada (Geloofsbelijdenis)", "Salah (Gebed)", "Zakat (Aalmoezen)", "Sawm (Vasten)", "Hajj (Bedevaart)"],
    "el": ["Σαχάντα (Δήλωση Πίστης)", "Σαλάχ (Προσευχή)", "Ζακάτ (Ελεημοσύνη)", "Σαούμ (Νηστεία)", "Χατζ (Προσκύνημα)"],
}

# Quiz question banks per category
QUIZ_BANKS = {
    "pillars": {
        "questions": [
            {
                "q": {"ar":"كم عدد أركان الإسلام؟","en":"How many pillars of Islam are there?","fr":"Combien de piliers de l'Islam y a-t-il ?","de":"Wie viele Säulen des Islam gibt es?","tr":"İslam'ın kaç şartı vardır?","ru":"Сколько столпов Ислама?","sv":"Hur många pelare har Islam?","nl":"Hoeveel zuilen heeft de Islam?","el":"Πόσοι πυλώνες του Ισλάμ υπάρχουν;"},
                "options": {"ar":["3","5","7","4"],"en":["3","5","7","4"],"fr":["3","5","7","4"],"de":["3","5","7","4"],"tr":["3","5","7","4"],"ru":["3","5","7","4"],"sv":["3","5","7","4"],"nl":["3","5","7","4"],"el":["3","5","7","4"]},
                "answer": 1
            },
            {
                "q": {"ar":"ما هو الركن الأول في الإسلام؟","en":"What is the first pillar of Islam?","fr":"Quel est le premier pilier de l'Islam ?","de":"Was ist die erste Säule des Islam?","tr":"İslam'ın ilk şartı nedir?","ru":"Какой первый столп Ислама?","sv":"Vad är Islams första pelare?","nl":"Wat is de eerste zuil van de Islam?","el":"Ποιος είναι ο πρώτος πυλώνας του Ισλάμ;"},
                "options": {"ar":["الصلاة","الشهادة","الزكاة","الحج"],"en":["Salah (Prayer)","Shahada (Declaration of Faith)","Zakat (Charity)","Hajj (Pilgrimage)"],"fr":["Salat","Chahada","Zakat","Hajj"],"de":["Salah","Shahada","Zakat","Hajj"],"tr":["Namaz","Şehadet","Zekât","Hac"],"ru":["Салят","Шахада","Закят","Хадж"],"sv":["Salah","Shahada","Zakat","Hajj"],"nl":["Salah","Shahada","Zakat","Hajj"],"el":["Σαλάχ","Σαχάντα","Ζακάτ","Χατζ"]},
                "answer": 1
            },
            {
                "q": {"ar":"في أي شهر يصوم المسلمون؟","en":"In which month do Muslims fast?","fr":"Pendant quel mois les musulmans jeûnent-ils ?","de":"In welchem Monat fasten Muslime?","tr":"Müslümanlar hangi ayda oruç tutar?","ru":"В каком месяце мусульмане постятся?","sv":"Under vilken månad fastar muslimer?","nl":"In welke maand vasten moslims?","el":"Σε ποιον μήνα νηστεύουν οι μουσουλμάνοι;"},
                "options": {"ar":["شعبان","رمضان","محرم","ذو الحجة"],"en":["Shaban","Ramadan","Muharram","Dhul Hijjah"],"fr":["Chaban","Ramadan","Muharram","Dhoul Hijja"],"de":["Schaban","Ramadan","Muharram","Dhul Hijjah"],"tr":["Şaban","Ramazan","Muharrem","Zilhicce"],"ru":["Шабан","Рамадан","Мухаррам","Зуль-Хиджа"],"sv":["Shaban","Ramadan","Muharram","Dhul Hijjah"],"nl":["Shaban","Ramadan","Muharram","Dhul Hijjah"],"el":["Σαμπάν","Ραμαντάν","Μουχαρράμ","Ζουλ Χίτζα"]},
                "answer": 1
            },
        ]
    },
    "quran": {
        "questions": [
            {
                "q": {"ar":"كم عدد سور القرآن الكريم؟","en":"How many surahs are in the Quran?","fr":"Combien de sourates dans le Coran ?","de":"Wie viele Suren hat der Koran?","tr":"Kur'an'da kaç sure vardır?","ru":"Сколько сур в Коране?","sv":"Hur många suror finns i Koranen?","nl":"Hoeveel soera's heeft de Koran?","el":"Πόσες σούρες έχει το Κοράνι;"},
                "options": {"ar":["100","114","120","99"],"en":["100","114","120","99"],"fr":["100","114","120","99"],"de":["100","114","120","99"],"tr":["100","114","120","99"],"ru":["100","114","120","99"],"sv":["100","114","120","99"],"nl":["100","114","120","99"],"el":["100","114","120","99"]},
                "answer": 1
            },
            {
                "q": {"ar":"ما أول سورة في القرآن؟","en":"What is the first surah of the Quran?","fr":"Quelle est la première sourate du Coran ?","de":"Was ist die erste Sure des Koran?","tr":"Kur'an'ın ilk suresi hangisidir?","ru":"Какая первая сура Корана?","sv":"Vad är Koranens första sura?","nl":"Wat is de eerste soera van de Koran?","el":"Ποια είναι η πρώτη σούρα του Κορανιού;"},
                "options": {"ar":["البقرة","الفاتحة","الناس","الإخلاص"],"en":["Al-Baqara","Al-Fatiha","An-Nas","Al-Ikhlas"],"fr":["Al-Baqara","Al-Fatiha","An-Nas","Al-Ikhlas"],"de":["Al-Baqara","Al-Fatiha","An-Nas","Al-Ikhlas"],"tr":["Bakara","Fatiha","Nas","İhlas"],"ru":["Аль-Бакара","Аль-Фатиха","Ан-Нас","Аль-Ихлас"],"sv":["Al-Baqara","Al-Fatiha","An-Nas","Al-Ikhlas"],"nl":["Al-Baqara","Al-Fatiha","An-Nas","Al-Ikhlas"],"el":["Αλ-Μπάκαρα","Αλ-Φάτιχα","Αν-Νας","Αλ-Ιχλάς"]},
                "answer": 1
            },
            {
                "q": {"ar":"ما أقصر سورة في القرآن؟","en":"What is the shortest surah in the Quran?","fr":"Quelle est la sourate la plus courte du Coran ?","de":"Was ist die kürzeste Sure des Koran?","tr":"Kur'an'ın en kısa suresi hangisidir?","ru":"Какая самая короткая сура Корана?","sv":"Vilken är Koranens kortaste sura?","nl":"Wat is de kortste soera van de Koran?","el":"Ποια είναι η πιο σύντομη σούρα;"},
                "options": {"ar":["الفلق","الإخلاص","الكوثر","الناس"],"en":["Al-Falaq","Al-Ikhlas","Al-Kawthar","An-Nas"],"fr":["Al-Falaq","Al-Ikhlas","Al-Kawthar","An-Nas"],"de":["Al-Falaq","Al-Ikhlas","Al-Kawthar","An-Nas"],"tr":["Felak","İhlas","Kevser","Nas"],"ru":["Аль-Фалак","Аль-Ихлас","Аль-Каусар","Ан-Нас"],"sv":["Al-Falaq","Al-Ikhlas","Al-Kawthar","An-Nas"],"nl":["Al-Falaq","Al-Ikhlas","Al-Kawthar","An-Nas"],"el":["Αλ-Φαλάκ","Αλ-Ιχλάς","Αλ-Κάουθαρ","Αν-Νας"]},
                "answer": 2
            },
        ]
    },
    "prayer": {
        "questions": [
            {
                "q": {"ar":"كم مرة يصلي المسلم في اليوم؟","en":"How many times a day does a Muslim pray?","fr":"Combien de fois par jour un musulman prie-t-il ?","de":"Wie oft am Tag betet ein Muslim?","tr":"Bir Müslüman günde kaç vakit namaz kılar?","ru":"Сколько раз в день молится мусульманин?","sv":"Hur många gånger om dagen ber en muslim?","nl":"Hoe vaak per dag bidt een moslim?","el":"Πόσες φορές την ημέρα προσεύχεται ένας μουσουλμάνος;"},
                "options": {"ar":["3","5","7","2"],"en":["3","5","7","2"],"fr":["3","5","7","2"],"de":["3","5","7","2"],"tr":["3","5","7","2"],"ru":["3","5","7","2"],"sv":["3","5","7","2"],"nl":["3","5","7","2"],"el":["3","5","7","2"]},
                "answer": 1
            },
            {
                "q": {"ar":"ما أول صلاة في اليوم؟","en":"What is the first prayer of the day?","fr":"Quelle est la première prière du jour ?","de":"Was ist das erste Gebet des Tages?","tr":"Günün ilk namazı hangisidir?","ru":"Какая первая молитва дня?","sv":"Vilken är dagens första bön?","nl":"Wat is het eerste gebed van de dag?","el":"Ποια είναι η πρώτη προσευχή της ημέρας;"},
                "options": {"ar":["الظهر","الفجر","المغرب","العشاء"],"en":["Dhuhr","Fajr","Maghrib","Isha"],"fr":["Dhouhr","Fajr","Maghrib","Icha"],"de":["Dhuhr","Fajr","Maghrib","Isha"],"tr":["Öğle","Sabah","Akşam","Yatsı"],"ru":["Зухр","Фаджр","Магриб","Иша"],"sv":["Dhuhr","Fajr","Maghrib","Isha"],"nl":["Dhuhr","Fajr","Maghrib","Isha"],"el":["Ζουχρ","Φάτζρ","Μαγκρίμπ","Ίσα"]},
                "answer": 1
            },
        ]
    },
}

# Memory game pairs
MEMORY_PAIRS = {
    "islamic_symbols": {
        "ar": [("🕌","مسجد"),("🕋","الكعبة"),("📖","القرآن"),("🤲","الدعاء"),("☪️","الهلال"),("⭐","النجمة")],
        "en": [("🕌","Mosque"),("🕋","Kaaba"),("📖","Quran"),("🤲","Dua"),("☪️","Crescent"),("⭐","Star")],
        "fr": [("🕌","Mosquée"),("🕋","Kaaba"),("📖","Coran"),("🤲","Doua"),("☪️","Croissant"),("⭐","Étoile")],
        "de": [("🕌","Moschee"),("🕋","Kaaba"),("📖","Koran"),("🤲","Dua"),("☪️","Halbmond"),("⭐","Stern")],
        "tr": [("🕌","Cami"),("🕋","Kâbe"),("📖","Kur'an"),("🤲","Dua"),("☪️","Hilal"),("⭐","Yıldız")],
        "ru": [("🕌","Мечеть"),("🕋","Кааба"),("📖","Коран"),("🤲","Дуа"),("☪️","Полумесяц"),("⭐","Звезда")],
        "sv": [("🕌","Moské"),("🕋","Kaaba"),("📖","Koranen"),("🤲","Dua"),("☪️","Halvmåne"),("⭐","Stjärna")],
        "nl": [("🕌","Moskee"),("🕋","Kaaba"),("📖","Koran"),("🤲","Doea"),("☪️","Halve maan"),("⭐","Ster")],
        "el": [("🕌","Τζαμί"),("🕋","Κάαμπα"),("📖","Κοράνι"),("🤲","Ντουά"),("☪️","Ημισέληνος"),("⭐","Αστέρι")],
    },
}

# Digital Shield scenario questions
SHIELD_SCENARIOS = {
    "en": [
        {"scenario": "A stranger online asks you to share your home address. What do you do?", "options": ["Share it — they seem nice", "Block and tell a parent", "Ignore the message", "Ask them why"], "correct": 1, "explanation": "Always block strangers who ask for personal info and tell your parents immediately!"},
        {"scenario": "You see a video of a famous person saying something shocking. What should you do?", "options": ["Share it immediately", "Check if it's a deepfake first", "Believe it because it looks real", "Comment your opinion"], "correct": 1, "explanation": "Always verify before sharing! Deepfakes can make anyone appear to say anything."},
        {"scenario": "An AI chatbot asks for your photo to 'make you look pretty'. What do you do?", "options": ["Send your photo", "Block and report it", "Send a fake photo", "Ask your friend to send theirs"], "correct": 1, "explanation": "Never send photos to AI bots or strangers online. Your privacy is sacred!"},
        {"scenario": "Someone is being bullied in a group chat. What should you do?", "options": ["Join the bullying", "Stay silent — not my problem", "Defend them and report the bully", "Leave the group quietly"], "correct": 2, "explanation": "The Prophet ﷺ said to help your brother. Standing up against bullying is the right thing to do!"},
        {"scenario": "You found free Wi-Fi at a cafe. Should you log into your bank account?", "options": ["Yes, it's convenient", "No, use mobile data instead", "Only if you're quick", "Ask the cafe staff first"], "correct": 1, "explanation": "Public Wi-Fi is not secure. Never access important accounts on it!"},
    ],
    "fr": [
        {"scenario": "Un inconnu en ligne vous demande de partager votre adresse. Que faites-vous ?", "options": ["La partager — il semble gentil", "Bloquer et prévenir un parent", "Ignorer le message", "Demander pourquoi"], "correct": 1, "explanation": "Bloquez toujours les inconnus qui demandent des infos personnelles !"},
        {"scenario": "Vous voyez une vidéo choquante d'une célébrité. Que devriez-vous faire ?", "options": ["La partager immédiatement", "Vérifier si c'est un deepfake d'abord", "Y croire car ça semble réel", "Commenter votre opinion"], "correct": 1, "explanation": "Vérifiez toujours avant de partager !"},
        {"scenario": "Un chatbot IA demande votre photo. Que faites-vous ?", "options": ["Envoyer votre photo", "Bloquer et signaler", "Envoyer une fausse photo", "Demander à un ami"], "correct": 1, "explanation": "N'envoyez jamais de photos à des bots IA !"},
        {"scenario": "Quelqu'un est harcelé dans un chat de groupe. Que devriez-vous faire ?", "options": ["Participer", "Rester silencieux", "Le défendre et signaler", "Quitter le groupe"], "correct": 2, "explanation": "Le Prophète ﷺ a dit d'aider votre frère."},
        {"scenario": "Vous trouvez du Wi-Fi gratuit. Devriez-vous accéder à votre compte bancaire ?", "options": ["Oui, c'est pratique", "Non, utilisez les données mobiles", "Seulement si c'est rapide", "Demander au personnel"], "correct": 1, "explanation": "Le Wi-Fi public n'est pas sécurisé !"},
    ],
    "de": [
        {"scenario": "Ein Fremder online bittet um deine Adresse. Was tust du?", "options": ["Teilen — scheint nett", "Blockieren und Eltern informieren", "Nachricht ignorieren", "Fragen warum"], "correct": 1, "explanation": "Blockiere immer Fremde, die nach persönlichen Infos fragen!"},
        {"scenario": "Du siehst ein schockierendes Video einer berühmten Person. Was tust du?", "options": ["Sofort teilen", "Erst prüfen ob Deepfake", "Glauben weil es echt aussieht", "Kommentieren"], "correct": 1, "explanation": "Immer erst überprüfen!"},
        {"scenario": "Ein KI-Chatbot bittet um dein Foto. Was tust du?", "options": ["Foto senden", "Blockieren und melden", "Falsches Foto senden", "Freund fragen"], "correct": 1, "explanation": "Sende niemals Fotos an KI-Bots!"},
        {"scenario": "Jemand wird im Gruppenchat gemobbt. Was solltest du tun?", "options": ["Mitmachen", "Schweigen", "Verteidigen und melden", "Gruppe verlassen"], "correct": 2, "explanation": "Der Prophet ﷺ sagte, helft eurem Bruder."},
        {"scenario": "Du findest kostenloses WLAN. Solltest du dein Bankkonto öffnen?", "options": ["Ja, ist bequem", "Nein, mobile Daten nutzen", "Nur wenn schnell", "Personal fragen"], "correct": 1, "explanation": "Öffentliches WLAN ist nicht sicher!"},
    ],
    "tr": [
        {"scenario": "Çevrimiçi bir yabancı ev adresinizi istiyor. Ne yaparsınız?", "options": ["Paylaşırım — iyi görünüyor", "Engelle ve ebeveyne söyle", "Mesajı görmezden gel", "Nedenini sor"], "correct": 1, "explanation": "Kişisel bilgi isteyen yabancıları her zaman engelleyin!"},
        {"scenario": "Ünlü birinin şok edici videosunu gördünüz. Ne yapmalısınız?", "options": ["Hemen paylaş", "Önce deepfake mi kontrol et", "Gerçek görünüyor inan", "Yorumunu yaz"], "correct": 1, "explanation": "Paylaşmadan önce her zaman doğrulayın!"},
        {"scenario": "Bir yapay zeka botu fotoğrafınızı istiyor. Ne yaparsınız?", "options": ["Fotoğraf gönder", "Engelle ve bildir", "Sahte fotoğraf gönder", "Arkadaşına sor"], "correct": 1, "explanation": "Yapay zeka botlarına asla fotoğraf göndermeyin!"},
        {"scenario": "Grup sohbetinde biri zorbalığa uğruyor. Ne yapmalısınız?", "options": ["Katıl", "Sessiz kal", "Savun ve bildir", "Gruptan ayrıl"], "correct": 2, "explanation": "Hz. Peygamber ﷺ kardeşinize yardım edin buyurmuştur."},
        {"scenario": "Kafede ücretsiz Wi-Fi buldunuz. Banka hesabınıza girmeli misiniz?", "options": ["Evet, rahat", "Hayır, mobil veri kullan", "Hızlı olursa evet", "Personele sor"], "correct": 1, "explanation": "Halka açık Wi-Fi güvenli değildir!"},
    ],
    "ru": [
        {"scenario": "Незнакомец онлайн просит ваш домашний адрес. Что делать?", "options": ["Поделиться — кажется хорошим", "Заблокировать и сказать родителям", "Игнорировать сообщение", "Спросить зачем"], "correct": 1, "explanation": "Всегда блокируйте незнакомцев, запрашивающих личные данные!"},
        {"scenario": "Вы видите шокирующее видео знаменитости. Что делать?", "options": ["Сразу поделиться", "Сначала проверить на дипфейк", "Поверить — выглядит реально", "Прокомментировать"], "correct": 1, "explanation": "Всегда проверяйте перед тем, как делиться!"},
        {"scenario": "ИИ-бот просит ваше фото. Что делать?", "options": ["Отправить фото", "Заблокировать и пожаловаться", "Отправить фейковое фото", "Спросить друга"], "correct": 1, "explanation": "Никогда не отправляйте фото ИИ-ботам!"},
        {"scenario": "Кого-то травят в групповом чате. Что делать?", "options": ["Присоединиться", "Молчать", "Защитить и сообщить", "Выйти из группы"], "correct": 2, "explanation": "Пророк ﷺ сказал: помогайте вашему брату."},
        {"scenario": "Нашли бесплатный Wi-Fi. Заходить в банк?", "options": ["Да, удобно", "Нет, использовать мобильный интернет", "Только быстро", "Спросить персонал"], "correct": 1, "explanation": "Публичный Wi-Fi небезопасен!"},
    ],
    "sv": [
        {"scenario": "En främling online ber om din hemadress. Vad gör du?", "options": ["Dela — verkar trevlig", "Blockera och berätta för förälder", "Ignorera meddelandet", "Fråga varför"], "correct": 1, "explanation": "Blockera alltid främlingar som ber om personlig info!"},
        {"scenario": "Du ser en chockerande video av en kändis. Vad bör du göra?", "options": ["Dela direkt", "Kontrollera om det är deepfake först", "Tro på det — ser äkta ut", "Kommentera"], "correct": 1, "explanation": "Verifiera alltid innan du delar!"},
        {"scenario": "En AI-bot ber om ditt foto. Vad gör du?", "options": ["Skicka foto", "Blockera och rapportera", "Skicka falskt foto", "Fråga en vän"], "correct": 1, "explanation": "Skicka aldrig foton till AI-botar!"},
        {"scenario": "Någon mobbas i en gruppchatt. Vad bör du göra?", "options": ["Delta", "Vara tyst", "Försvara och rapportera", "Lämna gruppen"], "correct": 2, "explanation": "Profeten ﷺ sade: hjälp er broder."},
        {"scenario": "Du hittar gratis Wi-Fi. Ska du logga in på banken?", "options": ["Ja, bekvämt", "Nej, använd mobildata", "Bara om det är snabbt", "Fråga personalen"], "correct": 1, "explanation": "Offentligt Wi-Fi är inte säkert!"},
    ],
    "nl": [
        {"scenario": "Een vreemde online vraagt je thuisadres. Wat doe je?", "options": ["Delen — lijkt aardig", "Blokkeren en ouder vertellen", "Bericht negeren", "Vragen waarom"], "correct": 1, "explanation": "Blokkeer altijd vreemden die om persoonlijke info vragen!"},
        {"scenario": "Je ziet een schokkende video van een beroemdheid. Wat doe je?", "options": ["Direct delen", "Eerst controleren op deepfake", "Geloven — ziet er echt uit", "Reageren"], "correct": 1, "explanation": "Verifieer altijd voor het delen!"},
        {"scenario": "Een AI-bot vraagt om je foto. Wat doe je?", "options": ["Foto sturen", "Blokkeren en melden", "Nep foto sturen", "Vriend vragen"], "correct": 1, "explanation": "Stuur nooit foto's naar AI-bots!"},
        {"scenario": "Iemand wordt gepest in een groepschat. Wat doe je?", "options": ["Meedoen", "Stil zijn", "Verdedigen en melden", "Groep verlaten"], "correct": 2, "explanation": "De Profeet ﷺ zei: help je broeder."},
        {"scenario": "Je vindt gratis Wi-Fi. Inloggen bij de bank?", "options": ["Ja, handig", "Nee, mobiele data gebruiken", "Alleen snel", "Personeel vragen"], "correct": 1, "explanation": "Openbaar Wi-Fi is niet veilig!"},
    ],
    "el": [
        {"scenario": "Ένας άγνωστος online ζητά τη διεύθυνσή σου. Τι κάνεις;", "options": ["Μοιράζομαι — φαίνεται καλός", "Μπλοκάρω και λέω στον γονέα", "Αγνοώ το μήνυμα", "Ρωτάω γιατί"], "correct": 1, "explanation": "Πάντα μπλοκάρετε αγνώστους που ζητούν προσωπικές πληροφορίες!"},
        {"scenario": "Βλέπεις ένα σοκαριστικό βίντεο διασημότητας. Τι κάνεις;", "options": ["Μοιράζομαι αμέσως", "Ελέγχω αν είναι deepfake", "Πιστεύω — φαίνεται αληθινό", "Σχολιάζω"], "correct": 1, "explanation": "Πάντα επαληθεύστε πριν μοιραστείτε!"},
        {"scenario": "Ένα AI bot ζητά τη φωτογραφία σου. Τι κάνεις;", "options": ["Στέλνω φωτό", "Μπλοκάρω και αναφέρω", "Στέλνω ψεύτικη φωτό", "Ρωτάω φίλο"], "correct": 1, "explanation": "Μην στέλνετε ποτέ φωτογραφίες σε AI bots!"},
        {"scenario": "Κάποιος εκφοβίζεται σε ομαδική συνομιλία. Τι κάνεις;", "options": ["Συμμετέχω", "Σιωπώ", "Υπερασπίζομαι και αναφέρω", "Φεύγω"], "correct": 2, "explanation": "Ο Προφήτης ﷺ είπε: βοηθήστε τον αδελφό σας."},
        {"scenario": "Βρίσκεις δωρεάν Wi-Fi. Να μπεις στην τράπεζα;", "options": ["Ναι, βολικό", "Όχι, χρήση δεδομένων κινητού", "Μόνο γρήγορα", "Ρωτάω προσωπικό"], "correct": 1, "explanation": "Το δημόσιο Wi-Fi δεν είναι ασφαλές!"},
    ],
    "ar": [
        {"scenario": "شخص غريب على الإنترنت يطلب عنوان منزلك. ماذا تفعل؟", "options": ["أشاركه — يبدو لطيفاً", "أحظره وأخبر والديّ", "أتجاهل الرسالة", "أسأله لماذا"], "correct": 1, "explanation": "احظر دائماً الغرباء الذين يطلبون معلوماتك الشخصية!"},
        {"scenario": "رأيت فيديو صادم لشخص مشهور. ماذا تفعل؟", "options": ["أشاركه فوراً", "أتحقق إذا كان تزييفاً عميقاً", "أصدقه لأنه يبدو حقيقياً", "أعلق برأيي"], "correct": 1, "explanation": "تحقق دائماً قبل المشاركة!"},
        {"scenario": "روبوت ذكاء اصطناعي يطلب صورتك. ماذا تفعل؟", "options": ["أرسل صورتي", "أحظره وأبلغ عنه", "أرسل صورة مزيفة", "أسأل صديقي"], "correct": 1, "explanation": "لا ترسل صوراً أبداً لروبوتات الذكاء الاصطناعي!"},
        {"scenario": "شخص يتعرض للتنمر في مجموعة. ماذا تفعل؟", "options": ["أشارك في التنمر", "أبقى صامتاً", "أدافع عنه وأبلغ", "أغادر المجموعة"], "correct": 2, "explanation": "قال النبي ﷺ: انصر أخاك."},
        {"scenario": "وجدت واي فاي مجاني. هل تفتح حسابك البنكي؟", "options": ["نعم، مريح", "لا، استخدم بيانات الهاتف", "فقط إذا كنت سريعاً", "اسأل الموظفين"], "correct": 1, "explanation": "الواي فاي العام غير آمن!"},
    ],
}


def generate_daily_games(day: int, locale: str = "en") -> dict:
    """Generate a set of games for a given day, localized."""
    lang = locale if locale in WUDU_STEPS else "en"
    random.seed(day)  # Deterministic per day
    
    games = []
    
    # Game 1: Quiz (rotating categories)
    categories = list(QUIZ_BANKS.keys())
    cat = categories[day % len(categories)]
    bank = QUIZ_BANKS[cat]
    q = bank["questions"][day % len(bank["questions"])]
    games.append({
        "type": "quiz",
        "id": f"quiz_{day}",
        "title": _get_game_title("quiz", lang),
        "question": q["q"].get(lang, q["q"]["en"]),
        "options": q["options"].get(lang, q["options"]["en"]),
        "correct_index": q["answer"],
        "xp": 10,
        "emoji": "🧠",
    })
    
    # Game 2: Memory Match (rotating themes)
    theme = "islamic_symbols"
    pairs = MEMORY_PAIRS[theme].get(lang, MEMORY_PAIRS[theme]["en"])
    selected_pairs = random.sample(pairs, min(4, len(pairs)))
    cards = []
    for i, (emoji, text) in enumerate(selected_pairs):
        cards.append({"id": f"e{i}", "content": emoji, "pair_id": f"p{i}", "type": "emoji"})
        cards.append({"id": f"t{i}", "content": text, "pair_id": f"p{i}", "type": "text"})
    random.shuffle(cards)
    games.append({
        "type": "memory",
        "id": f"memory_{day}",
        "title": _get_game_title("memory", lang),
        "cards": cards,
        "total_pairs": len(selected_pairs),
        "xp": 15,
        "emoji": "🎴",
    })
    
    # Game 3: Drag & Drop (alternate between wudu and salah)
    if day % 2 == 0:
        steps = WUDU_STEPS.get(lang, WUDU_STEPS["en"])
        drag_title = _get_game_title("wudu_order", lang)
    else:
        steps = SALAH_STEPS.get(lang, SALAH_STEPS["en"])
        drag_title = _get_game_title("salah_order", lang)
    
    # Show 4-5 steps to order
    num_steps = min(5, len(steps))
    start = (day * 2) % max(1, len(steps) - num_steps)
    subset = steps[start:start + num_steps]
    correct_order = list(range(len(subset)))
    shuffled_items = list(enumerate(subset))
    random.shuffle(shuffled_items)
    games.append({
        "type": "drag_drop",
        "id": f"drag_{day}",
        "title": drag_title,
        "items": [{"id": idx, "text": text} for idx, text in shuffled_items],
        "correct_order": [idx for idx, _ in enumerate(subset)],
        "xp": 20,
        "emoji": "🔀",
    })
    
    # Game 4: Digital Shield Scenario
    scenarios = SHIELD_SCENARIOS.get(lang, SHIELD_SCENARIOS["en"])
    scenario = scenarios[day % len(scenarios)]
    games.append({
        "type": "scenario",
        "id": f"scenario_{day}",
        "title": _get_game_title("scenario", lang),
        "scenario": scenario["scenario"],
        "options": scenario["options"],
        "correct_index": scenario["correct"],
        "explanation": scenario["explanation"],
        "xp": 15,
        "emoji": "🛡️",
    })
    
    return {
        "day": day,
        "total_xp": sum(g["xp"] for g in games),
        "games": games,
        "games_count": len(games),
    }


def _get_game_title(game_type: str, lang: str) -> str:
    titles = {
        "quiz": {"ar":"تحدي المعرفة","en":"Knowledge Challenge","fr":"Défi des connaissances","de":"Wissens-Challenge","tr":"Bilgi Yarışması","ru":"Вызов знаний","sv":"Kunskapsutmaning","nl":"Kennisuitdaging","el":"Πρόκληση γνώσης"},
        "memory": {"ar":"تحدي الذاكرة","en":"Memory Challenge","fr":"Défi mémoire","de":"Gedächtnis-Challenge","tr":"Hafıza Oyunu","ru":"Испытание памяти","sv":"Minnesutmaning","nl":"Geheugenuitdaging","el":"Πρόκληση μνήμης"},
        "wudu_order": {"ar":"رتّب خطوات الوضوء","en":"Order the Wudu Steps","fr":"Ordonnez les étapes du Wudu","de":"Ordne die Wudu-Schritte","tr":"Abdest Adımlarını Sırala","ru":"Расположи шаги Вуду","sv":"Ordna Wudu-stegen","nl":"Rangschik de Wudu-stappen","el":"Τακτοποίησε τα βήματα Wudu"},
        "salah_order": {"ar":"رتّب خطوات الصلاة","en":"Order the Salah Steps","fr":"Ordonnez les étapes de la Salat","de":"Ordne die Salah-Schritte","tr":"Namaz Adımlarını Sırala","ru":"Расположи шаги Салят","sv":"Ordna Salah-stegen","nl":"Rangschik de Salah-stappen","el":"Τακτοποίησε τα βήματα Σαλάχ"},
        "scenario": {"ar":"سيناريو الدرع الرقمي","en":"Digital Shield Scenario","fr":"Scénario Bouclier Numérique","de":"Digitaler Schutzschild Szenario","tr":"Dijital Kalkan Senaryosu","ru":"Сценарий Цифрового Щита","sv":"Digitalt Skydd Scenario","nl":"Digitaal Schild Scenario","el":"Σενάριο Ψηφιακής Ασπίδας"},
    }
    return titles.get(game_type, {}).get(lang, titles.get(game_type, {}).get("en", game_type))

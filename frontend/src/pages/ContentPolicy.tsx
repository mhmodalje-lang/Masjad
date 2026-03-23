import { Link } from 'react-router-dom';
import { ArrowRight, ArrowLeft, Shield, AlertTriangle, Ban, Eye, Flag, Users } from 'lucide-react';
import { useLocale } from '@/hooks/useLocale';

const CONTENT_POLICY: Record<string, Record<string, string>> = {
  ar: {
    title: 'سياسة المحتوى والإشراف',
    lastUpdated: 'آخر تحديث: يوليو 2025',
    introTitle: 'مقدمة',
    introText: 'تطبيق "أذان وحكاية" يتيح للمستخدمين نشر محتوى (نصوص، صور، فيديوهات). نلتزم بالحفاظ على بيئة آمنة ومحترمة لجميع المستخدمين من خلال سياسة إشراف صارمة.',
    prohibitedTitle: 'المحتوى المحظور',
    prohibited1: 'المحتوى المسيء أو التحرش أو التنمر',
    prohibited2: 'خطاب الكراهية أو التمييز العنصري أو الديني',
    prohibited3: 'المحتوى الإباحي أو الجنسي',
    prohibited4: 'المحتوى العنيف أو الذي يروج للعنف',
    prohibited5: 'الاحتيال والنصب والمعلومات المضللة',
    prohibited6: 'انتهاك حقوق الملكية الفكرية',
    prohibited7: 'البريد العشوائي (Spam) أو الإعلانات غير المصرح بها',
    prohibited8: 'المحتوى الذي يستغل الأطفال أو يعرضهم للخطر',
    reportTitle: 'الإبلاغ عن المحتوى',
    reportText: 'يمكنك الإبلاغ عن أي محتوى مخالف من خلال:',
    report1: 'الضغط على زر الإبلاغ (🚩) الموجود بجانب كل منشور',
    report2: 'اختيار سبب الإبلاغ من القائمة',
    report3: 'إضافة تفاصيل إضافية إن أمكن',
    report4: 'فريقنا يراجع جميع البلاغات خلال 24 ساعة',
    blockTitle: 'حظر المستخدمين',
    blockText: 'يمكنك حظر أي مستخدم لمنعه من رؤية محتواك أو التفاعل معك. المستخدم المحظور لن يعلم بحظره.',
    moderationTitle: 'إجراءات الإشراف',
    moderation1: 'مراجعة البلاغات خلال 24 ساعة',
    moderation2: 'إزالة المحتوى المخالف فوراً',
    moderation3: 'تحذير المستخدم المخالف',
    moderation4: 'إيقاف الحساب مؤقتاً أو دائماً في حالة التكرار',
    moderation5: 'إبلاغ الجهات المختصة في حالات الجرائم',
    appealTitle: 'الطعن والاستئناف',
    appealText: 'إذا تم إزالة محتواك أو تقييد حسابك، يمكنك تقديم طعن عبر البريد الإلكتروني خلال 14 يوماً. سيتم مراجعة طعنك خلال 7 أيام عمل.',
    childrenTitle: 'حماية الأطفال',
    childrenText: 'نتخذ إجراءات صارمة لحماية القاصرين. أي محتوى يستغل الأطفال يتم إزالته فوراً والإبلاغ عنه للجهات المختصة.',
    contactTitle: 'تواصل معنا',
    contactText: 'للإبلاغ عن مشكلات عاجلة أو استفسارات حول سياسة المحتوى:',
  },
  en: {
    title: 'Content & Moderation Policy',
    lastUpdated: 'Last updated: July 2025',
    introTitle: 'Introduction',
    introText: '"Azan & Hikaya" allows users to publish content (text, images, videos). We are committed to maintaining a safe and respectful environment for all users through strict moderation policies.',
    prohibitedTitle: 'Prohibited Content',
    prohibited1: 'Harassment, bullying, or abusive content',
    prohibited2: 'Hate speech, racial or religious discrimination',
    prohibited3: 'Pornographic or sexual content',
    prohibited4: 'Violent content or content promoting violence',
    prohibited5: 'Fraud, scams, and misinformation',
    prohibited6: 'Intellectual property infringement',
    prohibited7: 'Spam or unauthorized advertisements',
    prohibited8: 'Content that exploits or endangers children',
    reportTitle: 'Reporting Content',
    reportText: 'You can report any violating content by:',
    report1: 'Tapping the Report button (🚩) next to any post',
    report2: 'Selecting the reason for reporting from the list',
    report3: 'Adding additional details if possible',
    report4: 'Our team reviews all reports within 24 hours',
    blockTitle: 'Blocking Users',
    blockText: 'You can block any user to prevent them from seeing your content or interacting with you. The blocked user will not be notified.',
    moderationTitle: 'Moderation Actions',
    moderation1: 'Review reports within 24 hours',
    moderation2: 'Immediately remove violating content',
    moderation3: 'Warn the violating user',
    moderation4: 'Temporarily or permanently suspend accounts for repeat offenses',
    moderation5: 'Report criminal activity to relevant authorities',
    appealTitle: 'Appeals',
    appealText: 'If your content was removed or your account restricted, you can submit an appeal via email within 14 days. Your appeal will be reviewed within 7 business days.',
    childrenTitle: 'Child Safety',
    childrenText: 'We take strict measures to protect minors. Any content exploiting children is immediately removed and reported to relevant authorities.',
    contactTitle: 'Contact Us',
    contactText: 'For urgent issues or content policy inquiries:',
  },
  de: {
    title: 'Inhalts- & Moderationsrichtlinie',
    lastUpdated: 'Letzte Aktualisierung: Juli 2025',
    introTitle: 'Einleitung',
    introText: '"Azan & Hikaya" erlaubt Nutzern das Veröffentlichen von Inhalten (Texte, Bilder, Videos). Wir verpflichten uns, eine sichere und respektvolle Umgebung durch strenge Moderationsrichtlinien aufrechtzuerhalten.',
    prohibitedTitle: 'Verbotene Inhalte',
    prohibited1: 'Belästigung, Mobbing oder missbräuchliche Inhalte',
    prohibited2: 'Hassrede, rassistische oder religiöse Diskriminierung',
    prohibited3: 'Pornografische oder sexuelle Inhalte',
    prohibited4: 'Gewalttätige Inhalte oder Gewaltverherrlichung',
    prohibited5: 'Betrug und Fehlinformationen',
    prohibited6: 'Verletzung geistigen Eigentums',
    prohibited7: 'Spam oder unautorisierte Werbung',
    prohibited8: 'Inhalte, die Kinder ausbeuten oder gefährden',
    reportTitle: 'Inhalte melden',
    reportText: 'Sie können jeden Verstoß melden durch:',
    report1: 'Tippen auf die Melden-Schaltfläche (🚩) neben jedem Beitrag',
    report2: 'Auswahl des Meldegruunds aus der Liste',
    report3: 'Zusätzliche Details hinzufügen',
    report4: 'Unser Team prüft alle Meldungen innerhalb von 24 Stunden',
    blockTitle: 'Nutzer blockieren',
    blockText: 'Sie können jeden Nutzer blockieren, um zu verhindern, dass er Ihre Inhalte sieht oder mit Ihnen interagiert.',
    moderationTitle: 'Moderationsmaßnahmen',
    moderation1: 'Prüfung von Meldungen innerhalb von 24 Stunden',
    moderation2: 'Sofortige Entfernung von Verstößen',
    moderation3: 'Warnung des verstoßenden Nutzers',
    moderation4: 'Vorübergehende oder dauerhafte Kontosperrung',
    moderation5: 'Meldung krimineller Aktivitäten an Behörden',
    appealTitle: 'Einspruch',
    appealText: 'Wenn Ihr Inhalt entfernt oder Ihr Konto eingeschränkt wurde, können Sie innerhalb von 14 Tagen per E-Mail Einspruch einlegen.',
    childrenTitle: 'Kinderschutz',
    childrenText: 'Wir ergreifen strenge Maßnahmen zum Schutz von Minderjährigen.',
    contactTitle: 'Kontakt',
    contactText: 'Für dringende Probleme oder Fragen zur Inhaltsrichtlinie:',
  },
  fr: {
    title: 'Politique de contenu et modération',
    lastUpdated: 'Dernière mise à jour : Juillet 2025',
    introTitle: 'Introduction',
    introText: '"Azan & Hikaya" permet aux utilisateurs de publier du contenu. Nous nous engageons à maintenir un environnement sûr et respectueux.',
    prohibitedTitle: 'Contenu interdit',
    prohibited1: 'Harcèlement, intimidation ou contenu abusif',
    prohibited2: 'Discours de haine ou discrimination',
    prohibited3: 'Contenu pornographique ou sexuel',
    prohibited4: 'Contenu violent ou promouvant la violence',
    prohibited5: 'Fraude et désinformation',
    prohibited6: 'Violation de la propriété intellectuelle',
    prohibited7: 'Spam ou publicités non autorisées',
    prohibited8: 'Contenu exploitant ou mettant en danger les enfants',
    reportTitle: 'Signaler du contenu',
    reportText: 'Vous pouvez signaler tout contenu en violation :',
    report1: 'Appuyez sur le bouton Signaler (🚩)',
    report2: 'Sélectionnez la raison du signalement',
    report3: 'Ajoutez des détails supplémentaires',
    report4: 'Notre équipe examine tous les signalements sous 24 heures',
    blockTitle: 'Bloquer des utilisateurs',
    blockText: 'Vous pouvez bloquer tout utilisateur pour l\'empêcher de voir votre contenu.',
    moderationTitle: 'Actions de modération',
    moderation1: 'Examen des signalements sous 24 heures',
    moderation2: 'Suppression immédiate du contenu en violation',
    moderation3: 'Avertissement de l\'utilisateur',
    moderation4: 'Suspension temporaire ou permanente du compte',
    moderation5: 'Signalement aux autorités en cas d\'infraction pénale',
    appealTitle: 'Appel',
    appealText: 'Si votre contenu a été supprimé, vous pouvez faire appel par e-mail dans les 14 jours.',
    childrenTitle: 'Protection des enfants',
    childrenText: 'Nous prenons des mesures strictes pour protéger les mineurs.',
    contactTitle: 'Contactez-nous',
    contactText: 'Pour les problèmes urgents ou questions sur la politique de contenu :',
  },
  ru: {
    title: 'Политика контента и модерации',
    lastUpdated: 'Последнее обновление: июль 2025',
    introTitle: 'Введение',
    introText: '"Азан и Хикая" позволяет пользователям публиковать контент. Мы стремимся поддерживать безопасную и уважительную среду.',
    prohibitedTitle: 'Запрещённый контент',
    prohibited1: 'Преследование, травля или оскорбительный контент',
    prohibited2: 'Ненавистнические высказывания или дискриминация',
    prohibited3: 'Порнографический или сексуальный контент',
    prohibited4: 'Насильственный контент',
    prohibited5: 'Мошенничество и дезинформация',
    prohibited6: 'Нарушение интеллектуальной собственности',
    prohibited7: 'Спам или несанкционированная реклама',
    prohibited8: 'Контент, эксплуатирующий детей',
    reportTitle: 'Жалобы на контент',
    reportText: 'Вы можете пожаловаться на нарушающий контент:',
    report1: 'Нажмите кнопку жалобы (🚩) рядом с публикацией',
    report2: 'Выберите причину жалобы',
    report3: 'Добавьте дополнительные подробности',
    report4: 'Наша команда рассматривает все жалобы в течение 24 часов',
    blockTitle: 'Блокировка пользователей',
    blockText: 'Вы можете заблокировать любого пользователя.',
    moderationTitle: 'Действия модерации',
    moderation1: 'Рассмотрение жалоб в течение 24 часов',
    moderation2: 'Немедленное удаление нарушающего контента',
    moderation3: 'Предупреждение нарушителя',
    moderation4: 'Временная или постоянная блокировка аккаунта',
    moderation5: 'Сообщение в правоохранительные органы',
    appealTitle: 'Обжалование',
    appealText: 'Если ваш контент был удалён, вы можете подать апелляцию по электронной почте в течение 14 дней.',
    childrenTitle: 'Защита детей',
    childrenText: 'Мы принимаем строгие меры для защиты несовершеннолетних.',
    contactTitle: 'Свяжитесь с нами',
    contactText: 'По срочным вопросам или вопросам о политике контента:',
  },
  tr: {
    title: 'İçerik ve Moderasyon Politikası',
    lastUpdated: 'Son güncelleme: Temmuz 2025',
    introTitle: 'Giriş',
    introText: '"Ezan ve Hikaye" kullanıcıların içerik yayınlamasına izin verir. Güvenli ve saygılı bir ortam sağlamaya kararlıyız.',
    prohibitedTitle: 'Yasak İçerik',
    prohibited1: 'Taciz, zorbalık veya kötüye kullanım',
    prohibited2: 'Nefret söylemi veya ayrımcılık',
    prohibited3: 'Pornografik veya cinsel içerik',
    prohibited4: 'Şiddeti teşvik eden içerik',
    prohibited5: 'Dolandırıcılık ve yanlış bilgi',
    prohibited6: 'Fikri mülkiyet ihlali',
    prohibited7: 'Spam veya yetkisiz reklamlar',
    prohibited8: 'Çocukları istismar eden içerik',
    reportTitle: 'İçerik Bildirme',
    reportText: 'İhlal eden içeriği bildirebilirsiniz:',
    report1: 'Gönderinin yanındaki Bildir (🚩) düğmesine dokunun',
    report2: 'Bildirim nedenini seçin',
    report3: 'Ek ayrıntılar ekleyin',
    report4: 'Ekibimiz tüm bildirimleri 24 saat içinde inceler',
    blockTitle: 'Kullanıcı Engelleme',
    blockText: 'Herhangi bir kullanıcıyı engelleyebilirsiniz.',
    moderationTitle: 'Moderasyon Eylemleri',
    moderation1: 'Bildirimlerin 24 saat içinde incelenmesi',
    moderation2: 'İhlal eden içeriğin derhal kaldırılması',
    moderation3: 'İhlal eden kullanıcının uyarılması',
    moderation4: 'Geçici veya kalıcı hesap askıya alma',
    moderation5: 'Suç faaliyetlerinin yetkililere bildirilmesi',
    appealTitle: 'İtiraz',
    appealText: 'İçeriğiniz kaldırıldıysa 14 gün içinde e-posta ile itiraz edebilirsiniz.',
    childrenTitle: 'Çocuk Güvenliği',
    childrenText: 'Küçükleri korumak için sıkı önlemler alıyoruz.',
    contactTitle: 'İletişim',
    contactText: 'Acil sorunlar veya içerik politikası soruları için:',
  },
  sv: {
    title: 'Innehålls- och modereringspolicy',
    lastUpdated: 'Senast uppdaterad: Juli 2025',
    introTitle: 'Introduktion',
    introText: '"Azan & Hikaya" låter användare publicera innehåll. Vi strävar efter att upprätthålla en säker och respektfull miljö.',
    prohibitedTitle: 'Förbjudet innehåll',
    prohibited1: 'Trakasserier, mobbning eller missbruk',
    prohibited2: 'Hatretorik eller diskriminering',
    prohibited3: 'Pornografiskt eller sexuellt innehåll',
    prohibited4: 'Våldsamt innehåll',
    prohibited5: 'Bedrägeri och desinformation',
    prohibited6: 'Intrång i immateriella rättigheter',
    prohibited7: 'Spam eller obehörig reklam',
    prohibited8: 'Innehåll som utnyttjar barn',
    reportTitle: 'Rapportera innehåll',
    reportText: 'Du kan rapportera överträdande innehåll:',
    report1: 'Tryck på Rapportera-knappen (🚩)',
    report2: 'Välj rapporteringsorsak',
    report3: 'Lägg till ytterligare detaljer',
    report4: 'Vårt team granskar alla rapporter inom 24 timmar',
    blockTitle: 'Blockera användare',
    blockText: 'Du kan blockera vilken användare som helst.',
    moderationTitle: 'Modereringsåtgärder',
    moderation1: 'Granskning av rapporter inom 24 timmar',
    moderation2: 'Omedelbar borttagning av överträdande innehåll',
    moderation3: 'Varning till överträdande användare',
    moderation4: 'Tillfällig eller permanent avstängning',
    moderation5: 'Rapportering till myndigheter vid brottslighet',
    appealTitle: 'Överklagande',
    appealText: 'Om ditt innehåll togs bort kan du överklaga via e-post inom 14 dagar.',
    childrenTitle: 'Barnsäkerhet',
    childrenText: 'Vi vidtar strikta åtgärder för att skydda minderåriga.',
    contactTitle: 'Kontakta oss',
    contactText: 'För brådskande frågor eller innehållspolicyfrågor:',
  },
  nl: {
    title: 'Inhouds- en moderatiebeleid',
    lastUpdated: 'Laatst bijgewerkt: Juli 2025',
    introTitle: 'Introductie',
    introText: '"Azan & Hikaya" staat gebruikers toe inhoud te publiceren. We streven naar een veilige en respectvolle omgeving.',
    prohibitedTitle: 'Verboden inhoud',
    prohibited1: 'Intimidatie, pesterij of misbruik',
    prohibited2: 'Haatspraak of discriminatie',
    prohibited3: 'Pornografische of seksuele inhoud',
    prohibited4: 'Gewelddadige inhoud',
    prohibited5: 'Fraude en desinformatie',
    prohibited6: 'Schending van intellectueel eigendom',
    prohibited7: 'Spam of ongeautoriseerde reclame',
    prohibited8: 'Inhoud die kinderen exploiteert',
    reportTitle: 'Inhoud melden',
    reportText: 'U kunt overtredende inhoud melden:',
    report1: 'Tik op de Melden-knop (🚩)',
    report2: 'Selecteer de meldreden',
    report3: 'Voeg aanvullende details toe',
    report4: 'Ons team beoordeelt alle meldingen binnen 24 uur',
    blockTitle: 'Gebruikers blokkeren',
    blockText: 'U kunt elke gebruiker blokkeren.',
    moderationTitle: 'Moderatieacties',
    moderation1: 'Beoordeling van meldingen binnen 24 uur',
    moderation2: 'Onmiddellijke verwijdering van overtredende inhoud',
    moderation3: 'Waarschuwing aan overtredende gebruiker',
    moderation4: 'Tijdelijke of permanente schorsing',
    moderation5: 'Melding aan autoriteiten bij criminaliteit',
    appealTitle: 'Beroep',
    appealText: 'Als uw inhoud is verwijderd kunt u binnen 14 dagen per e-mail beroep aantekenen.',
    childrenTitle: 'Kinderveiligheid',
    childrenText: 'We nemen strikte maatregelen om minderjarigen te beschermen.',
    contactTitle: 'Neem contact op',
    contactText: 'Voor urgente problemen of vragen over inhoudsbeleid:',
  },
  el: {
    title: 'Πολιτική Περιεχομένου και Εποπτείας',
    lastUpdated: 'Τελευταία ενημέρωση: Ιούλιος 2025',
    introTitle: 'Εισαγωγή',
    introText: 'Το "Azan & Hikaya" επιτρέπει στους χρήστες να δημοσιεύουν περιεχόμενο. Δεσμευόμαστε να διατηρούμε ένα ασφαλές περιβάλλον.',
    prohibitedTitle: 'Απαγορευμένο Περιεχόμενο',
    prohibited1: 'Παρενόχληση ή εκφοβισμός',
    prohibited2: 'Ρητορική μίσους ή διακρίσεις',
    prohibited3: 'Πορνογραφικό ή σεξουαλικό περιεχόμενο',
    prohibited4: 'Βίαιο περιεχόμενο',
    prohibited5: 'Απάτη και παραπληροφόρηση',
    prohibited6: 'Παραβίαση πνευματικής ιδιοκτησίας',
    prohibited7: 'Spam ή μη εξουσιοδοτημένες διαφημίσεις',
    prohibited8: 'Περιεχόμενο που εκμεταλλεύεται παιδιά',
    reportTitle: 'Αναφορά Περιεχομένου',
    reportText: 'Μπορείτε να αναφέρετε παραβατικό περιεχόμενο:',
    report1: 'Πατήστε το κουμπί Αναφοράς (🚩)',
    report2: 'Επιλέξτε τον λόγο αναφοράς',
    report3: 'Προσθέστε επιπλέον λεπτομέρειες',
    report4: 'Η ομάδα μας εξετάζει όλες τις αναφορές εντός 24 ωρών',
    blockTitle: 'Αποκλεισμός Χρηστών',
    blockText: 'Μπορείτε να αποκλείσετε οποιονδήποτε χρήστη.',
    moderationTitle: 'Ενέργειες Εποπτείας',
    moderation1: 'Εξέταση αναφορών εντός 24 ωρών',
    moderation2: 'Άμεση αφαίρεση παραβατικού περιεχομένου',
    moderation3: 'Προειδοποίηση του παραβάτη',
    moderation4: 'Προσωρινή ή μόνιμη αναστολή λογαριασμού',
    moderation5: 'Αναφορά στις αρχές σε περίπτωση εγκλήματος',
    appealTitle: 'Ένσταση',
    appealText: 'Αν αφαιρέθηκε το περιεχόμενό σας, μπορείτε να υποβάλετε ένσταση μέσω email εντός 14 ημερών.',
    childrenTitle: 'Ασφάλεια Παιδιών',
    childrenText: 'Λαμβάνουμε αυστηρά μέτρα για την προστασία ανηλίκων.',
    contactTitle: 'Επικοινωνία',
    contactText: 'Για επείγοντα ζητήματα ή ερωτήσεις σχετικά με την πολιτική περιεχομένου:',
  },
};

function getContent(locale: string): Record<string, string> {
  return CONTENT_POLICY[locale] || CONTENT_POLICY['en'];
}

export default function ContentPolicy() {
  const { t, dir, isRTL, locale } = useLocale();
  const BackArrow = isRTL ? ArrowRight : ArrowLeft;
  const c = getContent(locale);

  return (
    <div className="min-h-screen pb-24 bg-background" dir={dir} data-testid="content-policy-page">
      <div className="sticky top-0 z-50 glass-nav bg-background/80 border-b border-border/10 px-4 h-14 flex items-center gap-3">
        <Link to="/more" className="p-2 rounded-xl bg-muted/50 active:scale-95"><BackArrow className="h-5 w-5 text-foreground" /></Link>
        <h1 className="text-lg font-bold text-foreground">{c.title}</h1>
      </div>
      <div className="px-5 py-6 space-y-5 max-w-3xl mx-auto">
        <p className="text-xs text-muted-foreground text-center">{c.lastUpdated}</p>

        <div className="rounded-2xl neu-card p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2">
            <Shield className="h-4 w-4 text-primary" />{c.introTitle}
          </h3>
          <p className="text-sm text-muted-foreground leading-relaxed">{c.introText}</p>
        </div>

        <div className="rounded-2xl bg-red-500/5 border border-red-500/20 p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2">
            <Ban className="h-4 w-4 text-red-500" />{c.prohibitedTitle}
          </h3>
          <ul className="space-y-2 text-sm text-muted-foreground">
            <li>• {c.prohibited1}</li><li>• {c.prohibited2}</li>
            <li>• {c.prohibited3}</li><li>• {c.prohibited4}</li>
            <li>• {c.prohibited5}</li><li>• {c.prohibited6}</li>
            <li>• {c.prohibited7}</li><li>• {c.prohibited8}</li>
          </ul>
        </div>

        <div className="rounded-2xl neu-card p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2">
            <Flag className="h-4 w-4 text-amber-500" />{c.reportTitle}
          </h3>
          <p className="text-sm text-muted-foreground mb-2">{c.reportText}</p>
          <ul className="space-y-2 text-sm text-muted-foreground">
            <li>1. {c.report1}</li><li>2. {c.report2}</li>
            <li>3. {c.report3}</li><li>4. {c.report4}</li>
          </ul>
        </div>

        <div className="rounded-2xl neu-card p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2">
            <Users className="h-4 w-4 text-blue-500" />{c.blockTitle}
          </h3>
          <p className="text-sm text-muted-foreground leading-relaxed">{c.blockText}</p>
        </div>

        <div className="rounded-2xl neu-card p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2">
            <Eye className="h-4 w-4 text-purple-500" />{c.moderationTitle}
          </h3>
          <ul className="space-y-2 text-sm text-muted-foreground">
            <li>• {c.moderation1}</li><li>• {c.moderation2}</li>
            <li>• {c.moderation3}</li><li>• {c.moderation4}</li>
            <li>• {c.moderation5}</li>
          </ul>
        </div>

        <div className="rounded-2xl neu-card p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2">
            <AlertTriangle className="h-4 w-4 text-amber-500" />{c.appealTitle}
          </h3>
          <p className="text-sm text-muted-foreground leading-relaxed">{c.appealText}</p>
        </div>

        <div className="rounded-2xl bg-primary/5 border border-primary/20 p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2">
            <Shield className="h-4 w-4 text-primary" />{c.childrenTitle}
          </h3>
          <p className="text-sm text-muted-foreground leading-relaxed">{c.childrenText}</p>
        </div>

        <div className="rounded-2xl neu-card p-5">
          <h3 className="text-base font-bold text-foreground mb-3">{c.contactTitle}</h3>
          <p className="text-sm text-muted-foreground mb-2">{c.contactText}</p>
          <p className="text-sm text-primary"><a href="mailto:mohammedalrejab@gmail.com">mohammedalrejab@gmail.com</a></p>
        </div>
      </div>
    </div>
  );
}

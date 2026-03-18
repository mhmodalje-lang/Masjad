import { Link } from 'react-router-dom';
import { ArrowRight, ArrowLeft, Shield, Eye, Database, Lock, UserCheck, Globe, Trash2, Mail } from 'lucide-react';
import { useLocale } from '@/hooks/useLocale';

// All privacy policy content by language
const PRIVACY_CONTENT: Record<string, Record<string, string>> = {
  ar: {
    lastUpdated: 'آخر تحديث: يوليو 2025',
    intro_title: 'مقدمة',
    intro_text: 'نحن في تطبيق "أذان وحكاية" نلتزم بحماية خصوصيتك وبياناتك الشخصية وفقاً للائحة العامة لحماية البيانات (GDPR) الصادرة عن الاتحاد الأوروبي والقوانين الدولية لحماية البيانات. توضح هذه السياسة كيفية جمع واستخدام وحماية وتخزين بياناتك.',
    dataController_title: 'المسؤول عن البيانات',
    dataController_text: 'المسؤول عن معالجة بياناتك الشخصية:',
    dataCollect_title: 'البيانات التي نجمعها',
    account_title: '1. بيانات الحساب',
    account_1: 'الاسم والبريد الإلكتروني (عند إنشاء حساب)',
    account_2: 'كلمة المرور (مشفرة ومحمية)',
    location_title: '2. بيانات الموقع',
    location_1: 'الموقع الجغرافي (فقط بإذنك) لتحديد مواقيت الصلاة واتجاه القبلة',
    location_2: 'لا نخزن سجل مواقعك',
    usage_title: '3. بيانات الاستخدام',
    usage_1: 'المحتوى المنشور (القصص والتعليقات)',
    usage_2: 'تفضيلات التطبيق (اللغة، المظهر، الإشعارات)',
    technical_title: '4. بيانات تقنية',
    technical_1: 'نوع المتصفح ونظام التشغيل',
    technical_2: 'عنوان IP (مجهول الهوية)',
    legal_title: 'الأساس القانوني للمعالجة (المادة 6 GDPR)',
    legal_consent: 'الموافقة:',
    legal_consent_t: 'عند تسجيل الحساب أو تفعيل الإشعارات أو الموقع',
    legal_contract: 'تنفيذ العقد:',
    legal_contract_t: 'لتقديم خدمات التطبيق الأساسية',
    legal_interest: 'المصالح المشروعة:',
    legal_interest_t: 'تحسين التطبيق وتأمين الخدمة',
    howUse_title: 'كيف نستخدم بياناتك',
    howUse_1: 'تقديم مواقيت الصلاة الدقيقة بناءً على موقعك',
    howUse_2: 'تخصيص تجربة المستخدم واللغة',
    howUse_3: 'إرسال إشعارات الأذان والتذكيرات (بموافقتك)',
    howUse_4: 'عرض المحتوى الإسلامي والقصص',
    howUse_5: 'تحسين خدماتنا وميزاتنا',
    thirdParty_title: 'محتوى مضمّن من أطراف ثالثة',
    thirdParty_text: 'قد يحتوي التطبيق على محتوى مضمّن (فيديوهات) من منصات مثل YouTube وVimeo وDailymotion. هذه المنصات قد تجمع بياناتك وفقاً لسياسات الخصوصية الخاصة بها.',
    ads_title: 'الإعلانات',
    ads_text: 'نستخدم خدمات إعلانية (مثل Google AdMob/AdSense) لعرض الإعلانات. هذه الخدمات قد تجمع معرّفات إعلانية ومعلومات الجهاز لتقديم إعلانات مخصصة. يمكنك إلغاء الإعلانات المخصصة من إعدادات جهازك.',
    cookies_title: 'ملفات تعريف الارتباط (Cookies)',
    cookies_text: 'نستخدم ملفات تعريف الارتباط الضرورية فقط لعمل التطبيق.',
    cookies_necessary: 'ضرورية:',
    cookies_necessary_t: 'تفضيلات اللغة، المظهر، حالة تسجيل الدخول',
    cookies_embed: 'محتوى مضمّن:',
    cookies_embed_t: 'قد تضع المنصات المضمّنة ملفاتها الخاصة',
    retention_title: 'مدة الاحتفاظ بالبيانات',
    retention_1: 'بيانات الحساب: حتى تطلب حذف حسابك',
    retention_2: 'المحتوى المنشور: حتى تحذفه أو يتم حذف الحساب',
    retention_3: 'بيانات الموقع: لا يتم تخزينها بشكل دائم',
    rights_title: 'حقوقك بموجب GDPR',
    rights_access: 'حق الوصول:',
    rights_access_t: 'طلب نسخة من بياناتك الشخصية',
    rights_rectify: 'حق التصحيح:',
    rights_rectify_t: 'تعديل بياناتك غير الدقيقة',
    rights_erase: 'حق الحذف:',
    rights_erase_t: 'طلب حذف جميع بياناتك ("الحق في النسيان")',
    rights_restrict: 'حق التقييد:',
    rights_restrict_t: 'تقييد معالجة بياناتك',
    rights_port: 'حق نقل البيانات:',
    rights_port_t: 'الحصول على بياناتك بتنسيق قابل للنقل',
    rights_object: 'حق الاعتراض:',
    rights_object_t: 'الاعتراض على معالجة بياناتك',
    rights_withdraw: 'سحب الموافقة:',
    rights_withdraw_t: 'سحب موافقتك في أي وقت',
    rights_contact: 'لممارسة أي من هذه الحقوق، تواصل معنا عبر:',
    security_title: 'حماية البيانات',
    security_1: 'تشفير البيانات أثناء النقل (HTTPS/TLS)',
    security_2: 'تشفير كلمات المرور بخوارزميات bcrypt',
    security_3: 'لن نبيع أو نشارك بياناتك مع أطراف ثالثة لأغراض تجارية',
    children_title: 'حماية الأطفال',
    children_text: 'التطبيق مناسب لجميع الأعمار. لا نجمع بيانات شخصية من الأطفال دون سن 16 عاماً بدون موافقة ولي الأمر.',
    authority_title: 'هيئة الرقابة',
    authority_text: 'لديك الحق في تقديم شكوى إلى هيئة حماية البيانات المختصة في بلدك أو في ألمانيا (BfDI).',
    contact_title: 'تواصل معنا',
    contact_text: 'لأي استفسارات حول سياسة الخصوصية أو لممارسة حقوقك:',
    version: 'آخر تحديث: يوليو 2025 | الإصدار 2.0',
  },
  en: {
    lastUpdated: 'Last updated: July 2025',
    intro_title: 'Introduction',
    intro_text: 'At "Azan & Hikaya", we are committed to protecting your privacy and personal data in accordance with the EU General Data Protection Regulation (GDPR) and international data protection laws. This policy explains how we collect, use, protect, and store your data.',
    dataController_title: 'Data Controller',
    dataController_text: 'The controller responsible for processing your personal data:',
    dataCollect_title: 'Data We Collect',
    account_title: '1. Account Data',
    account_1: 'Name and email (when creating an account)',
    account_2: 'Password (encrypted and protected)',
    location_title: '2. Location Data',
    location_1: 'Geographic location (only with your permission) for prayer times and Qibla direction',
    location_2: 'We do not store your location history',
    usage_title: '3. Usage Data',
    usage_1: 'Published content (stories and comments)',
    usage_2: 'App preferences (language, theme, notifications)',
    technical_title: '4. Technical Data',
    technical_1: 'Browser type and operating system',
    technical_2: 'IP address (anonymized)',
    legal_title: 'Legal Basis for Processing (GDPR Article 6)',
    legal_consent: 'Consent:',
    legal_consent_t: 'When registering an account, enabling notifications, or location',
    legal_contract: 'Contract Performance:',
    legal_contract_t: 'To provide core app services',
    legal_interest: 'Legitimate Interests:',
    legal_interest_t: 'Improving the app and securing the service',
    howUse_title: 'How We Use Your Data',
    howUse_1: 'Providing accurate prayer times based on your location',
    howUse_2: 'Personalizing user experience and language',
    howUse_3: 'Sending Azan notifications and reminders (with your consent)',
    howUse_4: 'Displaying Islamic content and stories',
    howUse_5: 'Improving our services and features',
    thirdParty_title: 'Third-Party Embedded Content',
    thirdParty_text: 'The app may contain embedded content (videos) from platforms such as YouTube, Vimeo, and Dailymotion. These platforms may collect your data according to their own privacy policies.',
    ads_title: 'Advertisements',
    ads_text: 'We use advertising services (such as Google AdMob/AdSense) to display ads. These services may collect advertising identifiers and device information to serve personalized ads. You can opt out of personalized ads in your device settings.',
    cookies_title: 'Cookies',
    cookies_text: 'We only use strictly necessary cookies for the app to function.',
    cookies_necessary: 'Necessary:',
    cookies_necessary_t: 'Language preferences, theme, login state',
    cookies_embed: 'Embedded content:',
    cookies_embed_t: 'Embedded platforms may set their own cookies',
    retention_title: 'Data Retention',
    retention_1: 'Account data: Until you request account deletion',
    retention_2: 'Published content: Until you delete it or account is deleted',
    retention_3: 'Location data: Not permanently stored',
    rights_title: 'Your Rights Under GDPR',
    rights_access: 'Right of Access:',
    rights_access_t: 'Request a copy of your personal data',
    rights_rectify: 'Right to Rectification:',
    rights_rectify_t: 'Correct inaccurate data',
    rights_erase: 'Right to Erasure:',
    rights_erase_t: 'Request deletion of all your data ("Right to be Forgotten")',
    rights_restrict: 'Right to Restriction:',
    rights_restrict_t: 'Restrict processing of your data',
    rights_port: 'Right to Data Portability:',
    rights_port_t: 'Receive your data in a portable format',
    rights_object: 'Right to Object:',
    rights_object_t: 'Object to processing of your data',
    rights_withdraw: 'Withdraw Consent:',
    rights_withdraw_t: 'Withdraw your consent at any time',
    rights_contact: 'To exercise any of these rights, contact us at:',
    security_title: 'Data Security',
    security_1: 'Data encryption in transit (HTTPS/TLS)',
    security_2: 'Password hashing with bcrypt algorithms',
    security_3: 'We will never sell or share your data with third parties for commercial purposes',
    children_title: "Children's Privacy",
    children_text: 'The app is suitable for all ages. We do not collect personal data from children under 16 without parental consent.',
    authority_title: 'Supervisory Authority',
    authority_text: 'You have the right to lodge a complaint with the competent data protection authority in your country or in Germany (BfDI).',
    contact_title: 'Contact Us',
    contact_text: 'For any privacy inquiries or to exercise your rights:',
    version: 'Last updated: July 2025 | Version 2.0',
  },
  ru: {
    lastUpdated: 'Последнее обновление: июль 2025',
    intro_title: 'Введение',
    intro_text: 'Мы в приложении «Азан и Хикая» обязуемся защищать вашу конфиденциальность и персональные данные в соответствии с Общим регламентом ЕС по защите данных (GDPR) и международным законодательством о защите данных.',
    dataController_title: 'Контролёр данных',
    dataController_text: 'Лицо, ответственное за обработку ваших персональных данных:',
    dataCollect_title: 'Данные, которые мы собираем',
    account_title: '1. Данные аккаунта',
    account_1: 'Имя и электронная почта (при создании аккаунта)',
    account_2: 'Пароль (зашифрован и защищён)',
    location_title: '2. Данные о местоположении',
    location_1: 'Геолокация (только с вашего разрешения) для расчёта времени намаза и направления Киблы',
    location_2: 'Мы не храним историю вашего местоположения',
    usage_title: '3. Данные об использовании',
    usage_1: 'Опубликованный контент (истории и комментарии)',
    usage_2: 'Настройки приложения (язык, тема, уведомления)',
    technical_title: '4. Технические данные',
    technical_1: 'Тип браузера и операционная система',
    technical_2: 'IP-адрес (анонимизирован)',
    legal_title: 'Правовое основание обработки (Статья 6 GDPR)',
    legal_consent: 'Согласие:',
    legal_consent_t: 'При регистрации аккаунта, включении уведомлений или геолокации',
    legal_contract: 'Исполнение договора:',
    legal_contract_t: 'Для предоставления основных услуг приложения',
    legal_interest: 'Законные интересы:',
    legal_interest_t: 'Улучшение приложения и обеспечение безопасности',
    howUse_title: 'Как мы используем ваши данные',
    howUse_1: 'Предоставление точного времени намаза на основе вашего местоположения',
    howUse_2: 'Персонализация пользовательского опыта и языка',
    howUse_3: 'Отправка уведомлений об Азане (с вашего согласия)',
    howUse_4: 'Отображение исламского контента и историй',
    howUse_5: 'Улучшение наших услуг и функций',
    thirdParty_title: 'Встроенный контент третьих сторон',
    thirdParty_text: 'Приложение может содержать встроенный контент (видео) с платформ YouTube, Vimeo и Dailymotion.',
    ads_title: 'Реклама',
    ads_text: 'Мы используем рекламные сервисы (Google AdMob/AdSense) для показа рекламы. Эти сервисы могут собирать рекламные идентификаторы и информацию об устройстве.',
    cookies_title: 'Файлы cookie',
    cookies_text: 'Мы используем только необходимые файлы cookie для работы приложения.',
    cookies_necessary: 'Необходимые:',
    cookies_necessary_t: 'Языковые настройки, тема, состояние входа',
    cookies_embed: 'Встроенный контент:',
    cookies_embed_t: 'Встроенные платформы могут устанавливать свои cookie',
    retention_title: 'Срок хранения данных',
    retention_1: 'Данные аккаунта: до запроса на удаление',
    retention_2: 'Опубликованный контент: до удаления вами или удаления аккаунта',
    retention_3: 'Данные о местоположении: не хранятся постоянно',
    rights_title: 'Ваши права по GDPR',
    rights_access: 'Право на доступ:',
    rights_access_t: 'Запрос копии ваших персональных данных',
    rights_rectify: 'Право на исправление:',
    rights_rectify_t: 'Исправление неточных данных',
    rights_erase: 'Право на удаление:',
    rights_erase_t: 'Запрос на удаление всех ваших данных',
    rights_restrict: 'Право на ограничение:',
    rights_restrict_t: 'Ограничение обработки ваших данных',
    rights_port: 'Право на переносимость:',
    rights_port_t: 'Получение ваших данных в переносимом формате',
    rights_object: 'Право на возражение:',
    rights_object_t: 'Возражение против обработки ваших данных',
    rights_withdraw: 'Отзыв согласия:',
    rights_withdraw_t: 'Отзыв вашего согласия в любое время',
    rights_contact: 'Для реализации любых прав свяжитесь с нами:',
    security_title: 'Безопасность данных',
    security_1: 'Шифрование данных при передаче (HTTPS/TLS)',
    security_2: 'Хеширование паролей алгоритмами bcrypt',
    security_3: 'Мы никогда не продадим ваши данные третьим лицам',
    children_title: 'Конфиденциальность детей',
    children_text: 'Приложение подходит для всех возрастов. Мы не собираем данные детей до 16 лет без согласия родителей.',
    authority_title: 'Надзорный орган',
    authority_text: 'Вы можете подать жалобу в уполномоченный орган по защите данных.',
    contact_title: 'Свяжитесь с нами',
    contact_text: 'По любым вопросам о конфиденциальности:',
    version: 'Последнее обновление: июль 2025 | Версия 2.0',
  },
  tr: {
    lastUpdated: 'Son güncelleme: Temmuz 2025',
    intro_title: 'Giriş',
    intro_text: '"Ezan ve Hikaye" uygulamasında, AB Genel Veri Koruma Yönetmeliği (GDPR) ve uluslararası veri koruma yasalarına uygun olarak gizliliğinizi ve kişisel verilerinizi korumayı taahhüt ediyoruz.',
    dataController_title: 'Veri Sorumlusu',
    dataController_text: 'Kişisel verilerinizin işlenmesinden sorumlu kişi:',
    dataCollect_title: 'Topladığımız Veriler',
    account_title: '1. Hesap Verileri',
    account_1: 'Ad ve e-posta (hesap oluştururken)',
    account_2: 'Şifre (şifrelenmiş ve korunmuş)',
    location_title: '2. Konum Verileri',
    location_1: 'Coğrafi konum (yalnızca izninizle) namaz vakitleri ve Kıble yönü için',
    location_2: 'Konum geçmişinizi saklamıyoruz',
    usage_title: '3. Kullanım Verileri',
    usage_1: 'Yayınlanan içerik (hikayeler ve yorumlar)',
    usage_2: 'Uygulama tercihleri (dil, tema, bildirimler)',
    technical_title: '4. Teknik Veriler',
    technical_1: 'Tarayıcı türü ve işletim sistemi',
    technical_2: 'IP adresi (anonimleştirilmiş)',
    legal_title: 'İşlemenin Yasal Dayanağı (GDPR Madde 6)',
    legal_consent: 'Onay:',
    legal_consent_t: 'Hesap kaydı, bildirimlerin veya konumun etkinleştirilmesi',
    legal_contract: 'Sözleşme İfası:',
    legal_contract_t: 'Temel uygulama hizmetlerinin sunulması',
    legal_interest: 'Meşru Menfaatler:',
    legal_interest_t: 'Uygulamanın iyileştirilmesi ve hizmetin güvenliği',
    howUse_title: 'Verilerinizi Nasıl Kullanıyoruz',
    howUse_1: 'Konumunuza göre doğru namaz vakitleri sağlama',
    howUse_2: 'Kullanıcı deneyimini ve dili kişiselleştirme',
    howUse_3: 'Ezan bildirimleri gönderme (onayınızla)',
    howUse_4: 'İslami içerik ve hikayeleri görüntüleme',
    howUse_5: 'Hizmetlerimizi ve özelliklerimizi geliştirme',
    thirdParty_title: 'Üçüncü Taraf Gömülü İçerik',
    thirdParty_text: 'Uygulama, YouTube, Vimeo ve Dailymotion gibi platformlardan gömülü içerik (videolar) içerebilir.',
    ads_title: 'Reklamlar',
    ads_text: 'Reklam göstermek için reklam hizmetleri (Google AdMob/AdSense) kullanıyoruz. Bu hizmetler reklam tanımlayıcıları ve cihaz bilgileri toplayabilir.',
    cookies_title: 'Çerezler',
    cookies_text: 'Yalnızca uygulamanın çalışması için gerekli çerezleri kullanıyoruz.',
    cookies_necessary: 'Gerekli:',
    cookies_necessary_t: 'Dil tercihleri, tema, oturum durumu',
    cookies_embed: 'Gömülü içerik:',
    cookies_embed_t: 'Gömülü platformlar kendi çerezlerini ayarlayabilir',
    retention_title: 'Veri Saklama',
    retention_1: 'Hesap verileri: Hesap silme talebine kadar',
    retention_2: 'Yayınlanan içerik: Silene veya hesap silinene kadar',
    retention_3: 'Konum verileri: Kalıcı olarak saklanmaz',
    rights_title: 'GDPR Kapsamındaki Haklarınız',
    rights_access: 'Erişim Hakkı:',
    rights_access_t: 'Kişisel verilerinizin bir kopyasını talep etme',
    rights_rectify: 'Düzeltme Hakkı:',
    rights_rectify_t: 'Yanlış verileri düzeltme',
    rights_erase: 'Silme Hakkı:',
    rights_erase_t: 'Tüm verilerinizin silinmesini talep etme',
    rights_restrict: 'Kısıtlama Hakkı:',
    rights_restrict_t: 'Verilerinizin işlenmesini kısıtlama',
    rights_port: 'Taşınabilirlik Hakkı:',
    rights_port_t: 'Verilerinizi taşınabilir formatta alma',
    rights_object: 'İtiraz Hakkı:',
    rights_object_t: 'Verilerinizin işlenmesine itiraz etme',
    rights_withdraw: 'Onayı Geri Çekme:',
    rights_withdraw_t: 'Onayınızı istediğiniz zaman geri çekme',
    rights_contact: 'Haklarınızı kullanmak için bize ulaşın:',
    security_title: 'Veri Güvenliği',
    security_1: 'Aktarım sırasında veri şifreleme (HTTPS/TLS)',
    security_2: 'bcrypt algoritmaları ile şifre karma',
    security_3: 'Verilerinizi ticari amaçlarla üçüncü taraflarla paylaşmayız',
    children_title: 'Çocuk Gizliliği',
    children_text: 'Uygulama tüm yaşlar için uygundur. Ebeveyn onayı olmadan 16 yaş altı çocuklardan veri toplamıyoruz.',
    authority_title: 'Denetim Makamı',
    authority_text: 'Ülkenizdeki yetkili veri koruma makamına şikayette bulunma hakkınız vardır.',
    contact_title: 'Bize Ulaşın',
    contact_text: 'Gizlilik soruları veya haklarınızı kullanmak için:',
    version: 'Son güncelleme: Temmuz 2025 | Sürüm 2.0',
  },
};

// Fallback to English for unsupported languages
function getContent(locale: string): Record<string, string> {
  return PRIVACY_CONTENT[locale] || PRIVACY_CONTENT['en'];
}

export default function PrivacyPolicy() {
  const { t, dir, isRTL, locale } = useLocale();
  const BackArrow = isRTL ? ArrowRight : ArrowLeft;
  const c = getContent(locale);

  return (
    <div className="min-h-screen pb-24 bg-background" dir={dir} data-testid="privacy-page">
      <div className="sticky top-0 z-50 bg-background/95 backdrop-blur-xl border-b border-border/20 px-4 h-14 flex items-center gap-3">
        <Link to="/more" className="p-2 rounded-xl bg-muted/50 active:scale-95"><BackArrow className="h-5 w-5 text-foreground" /></Link>
        <h1 className="text-lg font-bold text-foreground">{t('privacyPolicy')}</h1>
      </div>
      <div className="px-5 py-6 space-y-5 max-w-3xl mx-auto">
        <p className="text-xs text-muted-foreground text-center">{c.lastUpdated}</p>

        {/* Introduction */}
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2">
            <Shield className="h-4 w-4 text-primary" />{c.intro_title}
          </h3>
          <p className="text-sm text-muted-foreground leading-relaxed">{c.intro_text}</p>
        </div>

        {/* Data Controller */}
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2">
            <UserCheck className="h-4 w-4 text-blue-400" />{c.dataController_title}
          </h3>
          <p className="text-sm text-muted-foreground leading-relaxed">{c.dataController_text}</p>
          <div className="mt-2 bg-muted/30 rounded-xl p-3 text-sm text-foreground/80">
            <p className="font-semibold">Mohammed Al-Rejab</p>
            <p>Email: <a href="mailto:mohammedalrejab@gmail.com" className="text-primary">mohammedalrejab@gmail.com</a></p>
            <p dir="ltr">Phone: <a href="tel:+4917684034961" className="text-primary">+49 176 84034961</a></p>
          </div>
        </div>

        {/* Data We Collect */}
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2">
            <Database className="h-4 w-4 text-green-400" />{c.dataCollect_title}
          </h3>
          <div className="space-y-3">
            <div>
              <p className="text-sm font-semibold text-foreground mb-1">{c.account_title}</p>
              <ul className="space-y-1 text-sm text-muted-foreground">
                <li>• {c.account_1}</li><li>• {c.account_2}</li>
              </ul>
            </div>
            <div>
              <p className="text-sm font-semibold text-foreground mb-1">{c.location_title}</p>
              <ul className="space-y-1 text-sm text-muted-foreground">
                <li>• {c.location_1}</li><li>• {c.location_2}</li>
              </ul>
            </div>
            <div>
              <p className="text-sm font-semibold text-foreground mb-1">{c.usage_title}</p>
              <ul className="space-y-1 text-sm text-muted-foreground">
                <li>• {c.usage_1}</li><li>• {c.usage_2}</li>
              </ul>
            </div>
            <div>
              <p className="text-sm font-semibold text-foreground mb-1">{c.technical_title}</p>
              <ul className="space-y-1 text-sm text-muted-foreground">
                <li>• {c.technical_1}</li><li>• {c.technical_2}</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Legal Basis */}
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2">
            <Lock className="h-4 w-4 text-yellow-500" />{c.legal_title}
          </h3>
          <ul className="space-y-2 text-sm text-muted-foreground">
            <li>• <strong>{c.legal_consent}</strong> {c.legal_consent_t}</li>
            <li>• <strong>{c.legal_contract}</strong> {c.legal_contract_t}</li>
            <li>• <strong>{c.legal_interest}</strong> {c.legal_interest_t}</li>
          </ul>
        </div>

        {/* How We Use Data */}
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2">
            <Eye className="h-4 w-4 text-purple-400" />{c.howUse_title}
          </h3>
          <ul className="space-y-2 text-sm text-muted-foreground">
            <li>• {c.howUse_1}</li><li>• {c.howUse_2}</li><li>• {c.howUse_3}</li>
            <li>• {c.howUse_4}</li><li>• {c.howUse_5}</li>
          </ul>
        </div>

        {/* Third Party */}
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2">
            <Globe className="h-4 w-4 text-teal-400" />{c.thirdParty_title}
          </h3>
          <p className="text-sm text-muted-foreground leading-relaxed mb-2">{c.thirdParty_text}</p>
          <ul className="space-y-1 text-sm text-muted-foreground">
            <li>• YouTube: <a href="https://policies.google.com/privacy" className="text-primary underline" target="_blank" rel="noopener noreferrer">Google Privacy Policy</a></li>
            <li>• Vimeo: <a href="https://vimeo.com/privacy" className="text-primary underline" target="_blank" rel="noopener noreferrer">Vimeo Privacy Policy</a></li>
            <li>• Dailymotion: <a href="https://legal.dailymotion.com/en/privacy-policy/" className="text-primary underline" target="_blank" rel="noopener noreferrer">Dailymotion Privacy Policy</a></li>
          </ul>
        </div>

        {/* Advertisements */}
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2">
            <Eye className="h-4 w-4 text-amber-400" />{c.ads_title}
          </h3>
          <p className="text-sm text-muted-foreground leading-relaxed">{c.ads_text}</p>
        </div>

        {/* Cookies */}
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3">{c.cookies_title}</h3>
          <p className="text-sm text-muted-foreground leading-relaxed mb-2">{c.cookies_text}</p>
          <ul className="space-y-1 text-sm text-muted-foreground">
            <li>• <strong>{c.cookies_necessary}</strong> {c.cookies_necessary_t}</li>
            <li>• <strong>{c.cookies_embed}</strong> {c.cookies_embed_t}</li>
          </ul>
        </div>

        {/* Retention */}
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3">{c.retention_title}</h3>
          <ul className="space-y-2 text-sm text-muted-foreground">
            <li>• {c.retention_1}</li><li>• {c.retention_2}</li><li>• {c.retention_3}</li>
          </ul>
        </div>

        {/* Rights */}
        <div className="rounded-2xl bg-card border border-primary/30 p-5 bg-primary/5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2">
            <UserCheck className="h-4 w-4 text-primary" />{c.rights_title}
          </h3>
          <ul className="space-y-2 text-sm text-muted-foreground">
            <li>• <strong>{c.rights_access}</strong> {c.rights_access_t}</li>
            <li>• <strong>{c.rights_rectify}</strong> {c.rights_rectify_t}</li>
            <li>• <strong>{c.rights_erase}</strong> {c.rights_erase_t}</li>
            <li>• <strong>{c.rights_restrict}</strong> {c.rights_restrict_t}</li>
            <li>• <strong>{c.rights_port}</strong> {c.rights_port_t}</li>
            <li>• <strong>{c.rights_object}</strong> {c.rights_object_t}</li>
            <li>• <strong>{c.rights_withdraw}</strong> {c.rights_withdraw_t}</li>
          </ul>
          <p className="text-sm text-primary font-semibold mt-3">
            {c.rights_contact} <a href="mailto:mohammedalrejab@gmail.com" className="underline">mohammedalrejab@gmail.com</a>
          </p>
        </div>

        {/* Security */}
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2">
            <Lock className="h-4 w-4 text-green-500" />{c.security_title}
          </h3>
          <ul className="space-y-2 text-sm text-muted-foreground">
            <li>• {c.security_1}</li><li>• {c.security_2}</li><li>• {c.security_3}</li>
          </ul>
        </div>

        {/* Children */}
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3">{c.children_title}</h3>
          <p className="text-sm text-muted-foreground leading-relaxed">{c.children_text}</p>
        </div>

        {/* Authority */}
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3">{c.authority_title}</h3>
          <p className="text-sm text-muted-foreground leading-relaxed">{c.authority_text}</p>
        </div>

        {/* Contact */}
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2">
            <Mail className="h-4 w-4 text-primary" />{c.contact_title}
          </h3>
          <p className="text-sm text-muted-foreground">{c.contact_text}</p>
          <p className="text-sm text-primary mt-1"><a href="mailto:mohammedalrejab@gmail.com">mohammedalrejab@gmail.com</a></p>
          <p className="text-sm text-primary mt-1" dir="ltr"><a href="tel:+4917684034961">+49 176 84034961</a></p>
        </div>

        <p className="text-center text-xs text-muted-foreground/40 pt-2">{c.version}</p>
      </div>
    </div>
  );
}

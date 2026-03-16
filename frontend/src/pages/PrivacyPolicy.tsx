import { Link } from 'react-router-dom';
import { ArrowRight, ArrowLeft, Shield, Eye, Database, Lock, UserCheck, Globe, Trash2, Mail } from 'lucide-react';
import { useLocale } from '@/hooks/useLocale';

export default function PrivacyPolicy() {
  const { t, dir, isRTL } = useLocale();
  const BackArrow = isRTL ? ArrowRight : ArrowLeft;

  return (
    <div className="min-h-screen pb-24 bg-background" dir={dir} data-testid="privacy-page">
      <div className="sticky top-0 z-50 bg-background/95 backdrop-blur-xl border-b border-border/20 px-4 h-14 flex items-center gap-3">
        <Link to="/more" className="p-2 rounded-xl bg-muted/50 active:scale-95"><BackArrow className="h-5 w-5 text-foreground" /></Link>
        <h1 className="text-lg font-bold text-foreground">{t('privacyPolicy')}</h1>
      </div>
      <div className="px-5 py-6 space-y-5 max-w-3xl mx-auto">

        {/* Last Updated */}
        <p className="text-xs text-muted-foreground text-center">
          {isRTL ? 'آخر تحديث: يوليو 2025' : 'Last updated: July 2025'}
        </p>

        {/* Introduction */}
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2">
            <Shield className="h-4 w-4 text-primary" />
            {isRTL ? 'مقدمة' : 'Introduction'}
          </h3>
          <p className="text-sm text-muted-foreground leading-relaxed">
            {isRTL 
              ? 'نحن في تطبيق "أذان وحكاية" نلتزم بحماية خصوصيتك وبياناتك الشخصية وفقاً للائحة العامة لحماية البيانات (GDPR) الصادرة عن الاتحاد الأوروبي والقوانين الدولية لحماية البيانات. توضح هذه السياسة كيفية جمع واستخدام وحماية وتخزين بياناتك.'
              : 'At "Azan & Hikaya", we are committed to protecting your privacy and personal data in accordance with the EU General Data Protection Regulation (GDPR) and international data protection laws. This policy explains how we collect, use, protect, and store your data.'}
          </p>
        </div>

        {/* Data Controller */}
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2">
            <UserCheck className="h-4 w-4 text-blue-400" />
            {isRTL ? 'المسؤول عن البيانات' : 'Data Controller'}
          </h3>
          <p className="text-sm text-muted-foreground leading-relaxed">
            {isRTL ? 'المسؤول عن معالجة بياناتك الشخصية:' : 'The controller responsible for processing your personal data:'}
          </p>
          <div className="mt-2 bg-muted/30 rounded-xl p-3 text-sm text-foreground/80">
            <p className="font-semibold">{isRTL ? 'محمد الرجب' : 'Mohammed Al-Rejab'}</p>
            <p>{isRTL ? 'البريد: ' : 'Email: '}<a href="mailto:mohammedalrejab@gmail.com" className="text-primary">mohammedalrejab@gmail.com</a></p>
            <p dir="ltr">{isRTL ? 'الهاتف: ' : 'Phone: '}<a href="tel:+4917684034961" className="text-primary">+49 176 84034961</a></p>
          </div>
        </div>

        {/* Data We Collect */}
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2">
            <Database className="h-4 w-4 text-green-400" />
            {isRTL ? 'البيانات التي نجمعها' : 'Data We Collect'}
          </h3>
          <div className="space-y-3">
            <div>
              <p className="text-sm font-semibold text-foreground mb-1">{isRTL ? '1. بيانات الحساب' : '1. Account Data'}</p>
              <ul className="space-y-1 text-sm text-muted-foreground">
                <li>• {isRTL ? 'الاسم والبريد الإلكتروني (عند إنشاء حساب)' : 'Name and email (when creating an account)'}</li>
                <li>• {isRTL ? 'كلمة المرور (مشفرة ومحمية)' : 'Password (encrypted and protected)'}</li>
              </ul>
            </div>
            <div>
              <p className="text-sm font-semibold text-foreground mb-1">{isRTL ? '2. بيانات الموقع' : '2. Location Data'}</p>
              <ul className="space-y-1 text-sm text-muted-foreground">
                <li>• {isRTL ? 'الموقع الجغرافي (فقط بإذنك) لتحديد مواقيت الصلاة واتجاه القبلة' : 'Geographic location (only with your permission) for prayer times and Qibla direction'}</li>
                <li>• {isRTL ? 'لا نخزن سجل مواقعك' : 'We do not store your location history'}</li>
              </ul>
            </div>
            <div>
              <p className="text-sm font-semibold text-foreground mb-1">{isRTL ? '3. بيانات الاستخدام' : '3. Usage Data'}</p>
              <ul className="space-y-1 text-sm text-muted-foreground">
                <li>• {isRTL ? 'المحتوى المنشور (القصص والتعليقات)' : 'Published content (stories and comments)'}</li>
                <li>• {isRTL ? 'تفضيلات التطبيق (اللغة، المظهر، الإشعارات)' : 'App preferences (language, theme, notifications)'}</li>
              </ul>
            </div>
            <div>
              <p className="text-sm font-semibold text-foreground mb-1">{isRTL ? '4. بيانات تقنية' : '4. Technical Data'}</p>
              <ul className="space-y-1 text-sm text-muted-foreground">
                <li>• {isRTL ? 'نوع المتصفح ونظام التشغيل' : 'Browser type and operating system'}</li>
                <li>• {isRTL ? 'عنوان IP (مجهول الهوية)' : 'IP address (anonymized)'}</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Legal Basis (GDPR Article 6) */}
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2">
            <Lock className="h-4 w-4 text-yellow-500" />
            {isRTL ? 'الأساس القانوني للمعالجة (المادة 6 GDPR)' : 'Legal Basis for Processing (GDPR Article 6)'}
          </h3>
          <ul className="space-y-2 text-sm text-muted-foreground">
            <li>• <strong>{isRTL ? 'الموافقة:' : 'Consent:'}</strong> {isRTL ? 'عند تسجيل الحساب أو تفعيل الإشعارات أو الموقع' : 'When registering an account, enabling notifications, or location'}</li>
            <li>• <strong>{isRTL ? 'تنفيذ العقد:' : 'Contract Performance:'}</strong> {isRTL ? 'لتقديم خدمات التطبيق الأساسية' : 'To provide core app services'}</li>
            <li>• <strong>{isRTL ? 'المصالح المشروعة:' : 'Legitimate Interests:'}</strong> {isRTL ? 'تحسين التطبيق وتأمين الخدمة' : 'Improving the app and securing the service'}</li>
          </ul>
        </div>

        {/* How We Use Data */}
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2">
            <Eye className="h-4 w-4 text-purple-400" />
            {isRTL ? 'كيف نستخدم بياناتك' : 'How We Use Your Data'}
          </h3>
          <ul className="space-y-2 text-sm text-muted-foreground">
            <li>• {isRTL ? 'تقديم مواقيت الصلاة الدقيقة بناءً على موقعك' : 'Providing accurate prayer times based on your location'}</li>
            <li>• {isRTL ? 'تخصيص تجربة المستخدم واللغة' : 'Personalizing user experience and language'}</li>
            <li>• {isRTL ? 'إرسال إشعارات الأذان والتذكيرات (بموافقتك)' : 'Sending Azan notifications and reminders (with your consent)'}</li>
            <li>• {isRTL ? 'عرض المحتوى الإسلامي والقصص' : 'Displaying Islamic content and stories'}</li>
            <li>• {isRTL ? 'تحسين خدماتنا وميزاتنا' : 'Improving our services and features'}</li>
          </ul>
        </div>

        {/* Third Party Embeds */}
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2">
            <Globe className="h-4 w-4 text-teal-400" />
            {isRTL ? 'محتوى مضمّن من أطراف ثالثة' : 'Third-Party Embedded Content'}
          </h3>
          <p className="text-sm text-muted-foreground leading-relaxed mb-2">
            {isRTL
              ? 'قد يحتوي التطبيق على محتوى مضمّن (فيديوهات) من منصات مثل YouTube وVimeo وDailymotion. هذه المنصات قد تجمع بياناتك وفقاً لسياسات الخصوصية الخاصة بها:'
              : 'The app may contain embedded content (videos) from platforms such as YouTube, Vimeo, and Dailymotion. These platforms may collect your data according to their own privacy policies:'}
          </p>
          <ul className="space-y-1 text-sm text-muted-foreground">
            <li>• YouTube: <a href="https://policies.google.com/privacy" className="text-primary underline" target="_blank" rel="noopener noreferrer">Google Privacy Policy</a></li>
            <li>• Vimeo: <a href="https://vimeo.com/privacy" className="text-primary underline" target="_blank" rel="noopener noreferrer">Vimeo Privacy Policy</a></li>
            <li>• Dailymotion: <a href="https://legal.dailymotion.com/en/privacy-policy/" className="text-primary underline" target="_blank" rel="noopener noreferrer">Dailymotion Privacy Policy</a></li>
          </ul>
        </div>

        {/* Cookies */}
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3">{isRTL ? 'ملفات تعريف الارتباط (Cookies)' : 'Cookies'}</h3>
          <p className="text-sm text-muted-foreground leading-relaxed mb-2">
            {isRTL
              ? 'نستخدم ملفات تعريف الارتباط الضرورية فقط لعمل التطبيق (مثل تخزين تفضيلات اللغة والمظهر). لا نستخدم ملفات تعريف ارتباط للتتبع أو الإعلانات.'
              : 'We only use strictly necessary cookies for the app to function (such as storing language and theme preferences). We do not use tracking or advertising cookies.'}
          </p>
          <ul className="space-y-1 text-sm text-muted-foreground">
            <li>• <strong>{isRTL ? 'ضرورية:' : 'Necessary:'}</strong> {isRTL ? 'تفضيلات اللغة، المظهر، حالة تسجيل الدخول' : 'Language preferences, theme, login state'}</li>
            <li>• <strong>{isRTL ? 'محتوى مضمّن:' : 'Embedded content:'}</strong> {isRTL ? 'قد تضع المنصات المضمّنة ملفاتها الخاصة' : 'Embedded platforms may set their own cookies'}</li>
          </ul>
        </div>

        {/* Data Retention */}
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3">{isRTL ? 'مدة الاحتفاظ بالبيانات' : 'Data Retention'}</h3>
          <ul className="space-y-2 text-sm text-muted-foreground">
            <li>• {isRTL ? 'بيانات الحساب: حتى تطلب حذف حسابك' : 'Account data: Until you request account deletion'}</li>
            <li>• {isRTL ? 'المحتوى المنشور: حتى تحذفه أو يتم حذف الحساب' : 'Published content: Until you delete it or account is deleted'}</li>
            <li>• {isRTL ? 'بيانات الموقع: لا يتم تخزينها بشكل دائم' : 'Location data: Not permanently stored'}</li>
          </ul>
        </div>

        {/* Your Rights (GDPR) */}
        <div className="rounded-2xl bg-card border border-primary/30 p-5 bg-primary/5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2">
            <UserCheck className="h-4 w-4 text-primary" />
            {isRTL ? 'حقوقك بموجب GDPR' : 'Your Rights Under GDPR'}
          </h3>
          <ul className="space-y-2 text-sm text-muted-foreground">
            <li>• <strong>{isRTL ? 'حق الوصول:' : 'Right of Access:'}</strong> {isRTL ? 'طلب نسخة من بياناتك الشخصية' : 'Request a copy of your personal data'}</li>
            <li>• <strong>{isRTL ? 'حق التصحيح:' : 'Right to Rectification:'}</strong> {isRTL ? 'تعديل بياناتك غير الدقيقة' : 'Correct inaccurate data'}</li>
            <li>• <strong>{isRTL ? 'حق الحذف:' : 'Right to Erasure:'}</strong> {isRTL ? 'طلب حذف جميع بياناتك ("الحق في النسيان")' : 'Request deletion of all your data ("Right to be Forgotten")'}</li>
            <li>• <strong>{isRTL ? 'حق التقييد:' : 'Right to Restriction:'}</strong> {isRTL ? 'تقييد معالجة بياناتك' : 'Restrict processing of your data'}</li>
            <li>• <strong>{isRTL ? 'حق نقل البيانات:' : 'Right to Data Portability:'}</strong> {isRTL ? 'الحصول على بياناتك بتنسيق قابل للنقل' : 'Receive your data in a portable format'}</li>
            <li>• <strong>{isRTL ? 'حق الاعتراض:' : 'Right to Object:'}</strong> {isRTL ? 'الاعتراض على معالجة بياناتك' : 'Object to processing of your data'}</li>
            <li>• <strong>{isRTL ? 'سحب الموافقة:' : 'Withdraw Consent:'}</strong> {isRTL ? 'سحب موافقتك في أي وقت' : 'Withdraw your consent at any time'}</li>
          </ul>
          <p className="text-sm text-primary font-semibold mt-3">
            {isRTL ? 'لممارسة أي من هذه الحقوق، تواصل معنا عبر:' : 'To exercise any of these rights, contact us at:'}
            {' '}<a href="mailto:mohammedalrejab@gmail.com" className="underline">mohammedalrejab@gmail.com</a>
          </p>
        </div>

        {/* Data Security */}
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2">
            <Lock className="h-4 w-4 text-green-500" />
            {isRTL ? 'حماية البيانات' : 'Data Security'}
          </h3>
          <ul className="space-y-2 text-sm text-muted-foreground">
            <li>• {isRTL ? 'تشفير البيانات أثناء النقل (HTTPS/TLS)' : 'Data encryption in transit (HTTPS/TLS)'}</li>
            <li>• {isRTL ? 'تشفير كلمات المرور بخوارزميات bcrypt' : 'Password hashing with bcrypt algorithms'}</li>
            <li>• {isRTL ? 'لن نبيع أو نشارك بياناتك مع أطراف ثالثة لأغراض تجارية' : 'We will never sell or share your data with third parties for commercial purposes'}</li>
          </ul>
        </div>

        {/* Children */}
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3">{isRTL ? 'حماية الأطفال' : "Children's Privacy"}</h3>
          <p className="text-sm text-muted-foreground leading-relaxed">
            {isRTL
              ? 'التطبيق مناسب لجميع الأعمار. لا نجمع بيانات شخصية من الأطفال دون سن 16 عاماً بدون موافقة ولي الأمر.'
              : 'The app is suitable for all ages. We do not collect personal data from children under 16 without parental consent.'}
          </p>
        </div>

        {/* Supervisory Authority */}
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3">{isRTL ? 'هيئة الرقابة' : 'Supervisory Authority'}</h3>
          <p className="text-sm text-muted-foreground leading-relaxed">
            {isRTL
              ? 'لديك الحق في تقديم شكوى إلى هيئة حماية البيانات المختصة في بلدك أو في ألمانيا (BfDI - المفوض الاتحادي لحماية البيانات وحرية المعلومات).'
              : 'You have the right to lodge a complaint with the competent data protection authority in your country or in Germany (BfDI - Federal Commissioner for Data Protection and Freedom of Information).'}
          </p>
        </div>

        {/* Contact */}
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2">
            <Mail className="h-4 w-4 text-primary" />
            {isRTL ? 'تواصل معنا' : 'Contact Us'}
          </h3>
          <p className="text-sm text-muted-foreground">
            {isRTL ? 'لأي استفسارات حول سياسة الخصوصية أو لممارسة حقوقك:' : 'For any privacy inquiries or to exercise your rights:'}
          </p>
          <p className="text-sm text-primary mt-1">
            <a href="mailto:mohammedalrejab@gmail.com">mohammedalrejab@gmail.com</a>
          </p>
          <p className="text-sm text-primary mt-1" dir="ltr">
            <a href="tel:+4917684034961">+49 176 84034961</a>
          </p>
        </div>

        <p className="text-center text-xs text-muted-foreground/40 pt-2">
          {isRTL ? 'آخر تحديث: يوليو 2025 | الإصدار 2.0' : 'Last updated: July 2025 | Version 2.0'}
        </p>
      </div>
    </div>
  );
}

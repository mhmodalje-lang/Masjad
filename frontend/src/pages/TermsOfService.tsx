import { Link } from 'react-router-dom';
import { ArrowRight, ArrowLeft, FileText, AlertCircle, ShieldCheck, Ban, Scale, Globe } from 'lucide-react';
import { useLocale } from '@/hooks/useLocale';

export default function TermsOfService() {
  const { t, dir, isRTL } = useLocale();
  const BackArrow = isRTL ? ArrowRight : ArrowLeft;

  return (
    <div className="min-h-screen pb-24 bg-background" dir={dir} data-testid="terms-page">
      <div className="sticky top-0 z-50 bg-background/95 backdrop-blur-xl border-b border-border/20 px-4 h-14 flex items-center gap-3">
        <Link to="/more" className="p-2 rounded-xl bg-muted/50 active:scale-95"><BackArrow className="h-5 w-5 text-foreground" /></Link>
        <h1 className="text-lg font-bold text-foreground">{t('termsOfService')}</h1>
      </div>
      <div className="px-5 py-6 space-y-5 max-w-3xl mx-auto">

        <p className="text-xs text-muted-foreground text-center">
          {isRTL ? 'آخر تحديث: يوليو 2025' : 'Last updated: July 2025'}
        </p>

        {/* Introduction */}
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2">
            <FileText className="h-4 w-4 text-primary" />
            {isRTL ? 'مقدمة' : 'Introduction'}
          </h3>
          <p className="text-sm text-muted-foreground leading-relaxed">
            {isRTL
              ? 'باستخدام تطبيق "أذان وحكاية"، أنت توافق على الالتزام بهذه الشروط والأحكام. إذا لم توافق على أي جزء من هذه الشروط، يرجى عدم استخدام التطبيق.'
              : 'By using the "Azan & Hikaya" app, you agree to be bound by these Terms of Service. If you do not agree to any part of these terms, please do not use the app.'}
          </p>
        </div>

        {/* Service Description */}
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2">
            <Globe className="h-4 w-4 text-blue-400" />
            {isRTL ? 'وصف الخدمة' : 'Service Description'}
          </h3>
          <p className="text-sm text-muted-foreground leading-relaxed">
            {isRTL
              ? '"أذان وحكاية" هو تطبيق إسلامي مجاني يقدم مواقيت الصلاة، القرآن الكريم، الأدعية والأذكار، القصص الإسلامية، الرقية الشرعية، وأدوات إسلامية أخرى. التطبيق متاح على الويب كتطبيق ويب تقدمي (PWA).'
              : '"Azan & Hikaya" is a free Islamic app providing prayer times, Holy Quran, duas and adhkar, Islamic stories, Ruqyah, and other Islamic tools. The app is available on the web as a Progressive Web App (PWA).'}
          </p>
        </div>

        {/* User Accounts */}
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2">
            <ShieldCheck className="h-4 w-4 text-green-400" />
            {isRTL ? 'حسابات المستخدمين' : 'User Accounts'}
          </h3>
          <ul className="space-y-2 text-sm text-muted-foreground">
            <li>• {isRTL ? 'يجب تقديم معلومات دقيقة عند إنشاء حساب' : 'You must provide accurate information when creating an account'}</li>
            <li>• {isRTL ? 'أنت مسؤول عن الحفاظ على أمان حسابك وكلمة مرورك' : 'You are responsible for maintaining the security of your account and password'}</li>
            <li>• {isRTL ? 'يجب أن يكون عمرك 16 عاماً على الأقل لإنشاء حساب (وفقاً لـ GDPR)' : 'You must be at least 16 years old to create an account (per GDPR)'}</li>
            <li>• {isRTL ? 'يحق لك حذف حسابك في أي وقت' : 'You have the right to delete your account at any time'}</li>
          </ul>
        </div>

        {/* User Content */}
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2">
            <FileText className="h-4 w-4 text-purple-400" />
            {isRTL ? 'المحتوى المنشور من المستخدمين' : 'User Generated Content'}
          </h3>
          <ul className="space-y-2 text-sm text-muted-foreground">
            <li>• {isRTL ? 'أنت المسؤول عن المحتوى الذي تنشره (القصص والتعليقات)' : 'You are responsible for content you publish (stories and comments)'}</li>
            <li>• {isRTL ? 'يجب أن يكون المحتوى إسلامياً ومناسباً ولا يخالف الشريعة' : 'Content must be Islamic, appropriate, and not violate Islamic principles'}</li>
            <li>• {isRTL ? 'نحتفظ بحق مراجعة وحذف أي محتوى غير مناسب' : 'We reserve the right to review and remove any inappropriate content'}</li>
            <li>• {isRTL ? 'يُمنع نشر محتوى يحض على الكراهية أو العنف أو التمييز' : 'Publishing content promoting hatred, violence, or discrimination is prohibited'}</li>
          </ul>
        </div>

        {/* Embedded Content & Copyright */}
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2">
            <Scale className="h-4 w-4 text-yellow-500" />
            {isRTL ? 'المحتوى المضمّن وحقوق النشر' : 'Embedded Content & Copyright'}
          </h3>
          <p className="text-sm text-muted-foreground leading-relaxed mb-2">
            {isRTL
              ? 'قد يحتوي التطبيق على محتوى مضمّن (embedded) من منصات خارجية مثل YouTube وVimeo. يتم تضمين هذا المحتوى عبر تقنية الإطارات (iframe) المقدمة رسمياً من هذه المنصات، وهي طريقة مشروعة تحترم حقوق النشر.'
              : 'The app may contain embedded content from external platforms such as YouTube and Vimeo. This content is embedded via iframe technology officially provided by these platforms, which is a legitimate method that respects copyright.'}
          </p>
          <ul className="space-y-1 text-sm text-muted-foreground">
            <li>• {isRTL ? 'جميع حقوق الفيديوهات المضمّنة تعود لأصحابها الأصليين' : 'All rights to embedded videos belong to their original creators'}</li>
            <li>• {isRTL ? 'نستخدم فقط روابط التضمين الرسمية من كل منصة' : 'We only use official embed links from each platform'}</li>
            <li>• {isRTL ? 'لا نقوم بتحميل أو إعادة رفع أي محتوى محمي بحقوق النشر' : 'We do not download or re-upload any copyrighted content'}</li>
          </ul>
        </div>

        {/* Prohibited Actions */}
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2">
            <Ban className="h-4 w-4 text-red-400" />
            {isRTL ? 'الإجراءات المحظورة' : 'Prohibited Actions'}
          </h3>
          <ul className="space-y-2 text-sm text-muted-foreground">
            <li>• {isRTL ? 'محاولة اختراق أو تعطيل التطبيق' : 'Attempting to hack or disrupt the app'}</li>
            <li>• {isRTL ? 'انتحال شخصية مستخدمين آخرين' : 'Impersonating other users'}</li>
            <li>• {isRTL ? 'استخدام التطبيق لأغراض غير قانونية' : 'Using the app for illegal purposes'}</li>
            <li>• {isRTL ? 'نشر محتوى مسيء أو مخالف للآداب الإسلامية' : 'Publishing offensive content or content contrary to Islamic ethics'}</li>
            <li>• {isRTL ? 'جمع بيانات المستخدمين الآخرين بدون إذن' : 'Collecting other users\' data without permission'}</li>
          </ul>
        </div>

        {/* Disclaimer */}
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2">
            <AlertCircle className="h-4 w-4 text-orange-400" />
            {isRTL ? 'إخلاء المسؤولية' : 'Disclaimer'}
          </h3>
          <ul className="space-y-2 text-sm text-muted-foreground">
            <li>• {isRTL ? 'مواقيت الصلاة تقريبية وقد تختلف حسب الموقع وطريقة الحساب' : 'Prayer times are approximate and may vary by location and calculation method'}</li>
            <li>• {isRTL ? 'قسم الرقية الشرعية للاستماع والتحصين وليس بديلاً عن العلاج الطبي' : 'The Ruqyah section is for listening and protection, not a substitute for medical treatment'}</li>
            <li>• {isRTL ? 'المساعد الذكي يقدم معلومات عامة وليس فتاوى شرعية رسمية' : 'The AI assistant provides general information, not official religious rulings'}</li>
            <li>• {isRTL ? 'التطبيق مقدم "كما هو" بدون ضمانات صريحة أو ضمنية' : 'The app is provided "as is" without express or implied warranties'}</li>
          </ul>
        </div>

        {/* Governing Law */}
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3">{isRTL ? 'القانون المعمول به' : 'Governing Law'}</h3>
          <p className="text-sm text-muted-foreground leading-relaxed">
            {isRTL
              ? 'تخضع هذه الشروط لقوانين الاتحاد الأوروبي وجمهورية ألمانيا الاتحادية. أي نزاع ينشأ عن استخدام التطبيق يخضع للاختصاص القضائي الألماني.'
              : 'These terms are governed by the laws of the European Union and the Federal Republic of Germany. Any disputes arising from the use of the app shall be subject to German jurisdiction.'}
          </p>
        </div>

        {/* Changes */}
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3">{isRTL ? 'التعديلات على الشروط' : 'Changes to Terms'}</h3>
          <p className="text-sm text-muted-foreground leading-relaxed">
            {isRTL
              ? 'نحتفظ بحق تعديل هذه الشروط في أي وقت. سيتم إخطارك بأي تغييرات جوهرية. استمرارك في استخدام التطبيق بعد التعديل يعني موافقتك على الشروط الجديدة.'
              : 'We reserve the right to modify these terms at any time. You will be notified of any material changes. Your continued use of the app after modification constitutes acceptance of the new terms.'}
          </p>
        </div>

        {/* Contact */}
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3">{isRTL ? 'تواصل معنا' : 'Contact Us'}</h3>
          <p className="text-sm text-muted-foreground">
            {isRTL ? 'لأي استفسارات حول شروط الاستخدام:' : 'For any inquiries about the Terms of Service:'}
          </p>
          <p className="text-sm text-primary mt-1"><a href="mailto:mohammedalrejab@gmail.com">mohammedalrejab@gmail.com</a></p>
        </div>

        <p className="text-center text-xs text-muted-foreground/40 pt-2">
          {isRTL ? 'آخر تحديث: يوليو 2025' : 'Last updated: July 2025'}
        </p>
      </div>
    </div>
  );
}

import { Link } from 'react-router-dom';
import { ArrowRight, Shield } from 'lucide-react';

export default function PrivacyPolicy() {
  return (
    <div className="min-h-screen pb-24 bg-background" dir="rtl" data-testid="privacy-page">
      <div className="sticky top-0 z-50 bg-background/95 backdrop-blur-xl border-b border-border/20 px-4 h-14 flex items-center gap-3">
        <Link to="/more" className="p-2 rounded-xl bg-muted/50 active:scale-95"><ArrowRight className="h-5 w-5 text-foreground" /></Link>
        <h1 className="text-lg font-bold text-foreground">سياسة الخصوصية</h1>
      </div>
      <div className="px-5 py-6 space-y-5">
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2"><Shield className="h-4 w-4 text-primary" />مقدمة</h3>
          <p className="text-sm text-muted-foreground leading-relaxed">نحن في تطبيق أذان وحكاية نلتزم بحماية خصوصيتك وبياناتك الشخصية. توضح هذه السياسة كيفية جمع واستخدام وحماية معلوماتك.</p>
        </div>
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3">البيانات التي نجمعها</h3>
          <ul className="space-y-2 text-sm text-muted-foreground">
            <li>• معلومات الحساب (الاسم والبريد الإلكتروني)</li>
            <li>• الموقع الجغرافي (لتحديد مواقيت الصلاة واتجاه القبلة)</li>
            <li>• بيانات الاستخدام (لتحسين تجربة المستخدم)</li>
            <li>• المحتوى المنشور (القصص والتعليقات)</li>
          </ul>
        </div>
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3">كيف نستخدم بياناتك</h3>
          <ul className="space-y-2 text-sm text-muted-foreground">
            <li>• تقديم مواقيت الصلاة الدقيقة بناءً على موقعك</li>
            <li>• تخصيص تجربة المستخدم والمحتوى</li>
            <li>• إرسال إشعارات الأذان والتذكيرات</li>
            <li>• تحسين خدماتنا وميزاتنا</li>
          </ul>
        </div>
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3">حماية البيانات</h3>
          <p className="text-sm text-muted-foreground leading-relaxed">نستخدم تقنيات تشفير متقدمة لحماية بياناتك. لن نبيع أو نشارك بياناتك الشخصية مع أطراف ثالثة دون موافقتك الصريحة.</p>
        </div>
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3">حقوقك</h3>
          <ul className="space-y-2 text-sm text-muted-foreground">
            <li>• الوصول إلى بياناتك الشخصية</li>
            <li>• تعديل أو حذف حسابك في أي وقت</li>
            <li>• إلغاء الاشتراك في الإشعارات</li>
            <li>• طلب حذف جميع بياناتك</li>
          </ul>
        </div>
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3">تواصل معنا</h3>
          <p className="text-sm text-muted-foreground">لأي استفسارات حول سياسة الخصوصية:</p>
          <p className="text-sm text-primary mt-1">mohammadalrejab@gmail.com</p>
        </div>
        <p className="text-center text-xs text-muted-foreground/40 pt-2">آخر تحديث: مارس 2026</p>
      </div>
    </div>
  );
}

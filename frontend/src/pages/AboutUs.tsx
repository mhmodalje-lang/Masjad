import { Link } from 'react-router-dom';
import { ArrowRight, Heart, Star, Shield, Users, Globe, Sparkles } from 'lucide-react';

export default function AboutUs() {
  return (
    <div className="min-h-screen pb-24 bg-background" dir="rtl" data-testid="about-page">
      <div className="sticky top-0 z-50 bg-background/95 backdrop-blur-xl border-b border-border/20 px-4 h-14 flex items-center gap-3">
        <Link to="/more" className="p-2 rounded-xl bg-muted/50 active:scale-95"><ArrowRight className="h-5 w-5 text-foreground" /></Link>
        <h1 className="text-lg font-bold text-foreground">من نحن</h1>
      </div>
      <div className="px-5 py-6 space-y-6">
        <div className="text-center mb-8">
          <div className="h-20 w-20 mx-auto rounded-2xl bg-gradient-to-br from-primary/20 to-primary/5 flex items-center justify-center mb-4">
            <Sparkles className="h-10 w-10 text-primary" />
          </div>
          <h2 className="text-2xl font-black text-foreground">أذان وحكاية</h2>
          <p className="text-sm text-muted-foreground mt-2">تطبيق إسلامي شامل لكل مسلم</p>
        </div>
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2"><Heart className="h-4 w-4 text-red-400" />رسالتنا</h3>
          <p className="text-sm text-muted-foreground leading-relaxed">نهدف إلى تقديم تجربة إسلامية رقمية متكاملة تجمع بين التكنولوجيا الحديثة والقيم الإسلامية الأصيلة. نسعى لخدمة المسلمين حول العالم بأدوات تساعدهم في عبادتهم وتعلمهم الديني.</p>
        </div>
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2"><Star className="h-4 w-4 text-primary" />مميزاتنا</h3>
          <ul className="space-y-3 text-sm text-muted-foreground">
            <li className="flex items-start gap-2"><Shield className="h-4 w-4 text-green-400 mt-0.5 shrink-0" />مواقيت صلاة دقيقة مع إشعارات الأذان</li>
            <li className="flex items-start gap-2"><Shield className="h-4 w-4 text-green-400 mt-0.5 shrink-0" />قراءة القرآن الكريم مع التفسير</li>
            <li className="flex items-start gap-2"><Shield className="h-4 w-4 text-green-400 mt-0.5 shrink-0" />مساعد ذكي مدعوم بالذكاء الاصطناعي</li>
            <li className="flex items-start gap-2"><Shield className="h-4 w-4 text-green-400 mt-0.5 shrink-0" />حكايات وقصص إسلامية ملهمة</li>
            <li className="flex items-start gap-2"><Shield className="h-4 w-4 text-green-400 mt-0.5 shrink-0" />أدعية وأذكار يومية</li>
            <li className="flex items-start gap-2"><Shield className="h-4 w-4 text-green-400 mt-0.5 shrink-0" />حاسبة الزكاة والتسبيح</li>
            <li className="flex items-start gap-2"><Shield className="h-4 w-4 text-green-400 mt-0.5 shrink-0" />الرقية الشرعية</li>
          </ul>
        </div>
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2"><Users className="h-4 w-4 text-blue-400" />فريقنا</h3>
          <p className="text-sm text-muted-foreground leading-relaxed">تم تطوير هذا التطبيق بحب وإخلاص لخدمة الأمة الإسلامية. نعمل باستمرار على تحسين التطبيق وإضافة ميزات جديدة.</p>
          <p className="text-sm text-primary font-bold mt-3">المؤسس: محمد الرجب</p>
        </div>
        <div className="rounded-2xl bg-card border border-border/30 p-5">
          <h3 className="text-base font-bold text-foreground mb-3 flex items-center gap-2"><Globe className="h-4 w-4 text-teal-400" />تواصل معنا</h3>
          <p className="text-sm text-muted-foreground">البريد: <a href="mailto:mohammadalrejab@gmail.com" className="text-primary">mohammadalrejab@gmail.com</a></p>
          <p className="text-sm text-muted-foreground mt-1">الهاتف: <a href="tel:+4917684034961" className="text-primary" dir="ltr">+4917684034961</a></p>
        </div>
        <p className="text-center text-xs text-muted-foreground/40 pt-4">أذان وحكاية v2.0 | جميع الحقوق محفوظة © 2026</p>
      </div>
    </div>
  );
}

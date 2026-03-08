

## المشكلة

هناك خلل في ترتيب تحميل البيانات (race condition):

1. عند فتح صفحة `/admin`، يعمل `useAdmin` فوراً
2. لكن `useAuth` لم ينتهِ بعد من تحميل بيانات المستخدم (`user = null`)
3. `useAdmin` يرى أن `user = null` فيضع `isAdmin = false` و `loading = false`
4. `AdminDashboard` يرى `!loading && !isAdmin` فيعيد التوجيه فوراً مع رسالة "غير مصرح لك"

البيانات في قاعدة البيانات صحيحة — كلا الحسابين مسجلان كمدير.

## الحل

تعديل `useAdmin` ليأخذ بعين الاعتبار حالة تحميل `useAuth`:

```typescript
// src/hooks/useAdmin.tsx
export function useAdmin() {
  const { user, loading: authLoading } = useAuth();
  const [isAdmin, setIsAdmin] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (authLoading) {
      setLoading(true);
      return;
    }
    
    if (!user) {
      setIsAdmin(false);
      setLoading(false);
      return;
    }

    setLoading(true);
    supabase
      .rpc('is_admin', { _user_id: user.id })
      .then(({ data, error }) => {
        setIsAdmin(!error && !!data);
        setLoading(false);
      });
  }, [user, authLoading]);

  return { isAdmin, loading };
}
```

تغيير واحد فقط في ملف `src/hooks/useAdmin.tsx` — إضافة انتظار `authLoading` قبل فحص صلاحية المدير.


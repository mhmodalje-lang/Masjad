import { useEffect, useState } from 'react';
import { supabase } from '@/integrations/supabase/client';
import { useAuth } from '@/hooks/useAuth';

export function useAdmin() {
  const { user } = useAuth();
  const [isAdmin, setIsAdmin] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user) {
      setIsAdmin(false);
      setLoading(false);
      return;
    }

    setLoading(true);
    supabase
      .rpc('is_admin', { _user_id: user.id })
      .then(({ data, error }) => {
        if (error) {
          console.error('Admin check error:', error);
          setIsAdmin(false);
        } else {
          setIsAdmin(!!data);
        }
        setLoading(false);
      });
  }, [user]);

  return { isAdmin, loading };
}

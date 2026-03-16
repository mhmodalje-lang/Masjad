import { useLocale } from '@/hooks/useLocale';
// Sohba has been replaced by Stories page
import { Navigate } from 'react-router-dom';
export default function Sohba() {
  return <Navigate to="/stories" replace />;
}

import { ReactNode } from 'react';
import { BottomNav } from './BottomNav';
import InstallBanner from '@/components/InstallBanner';

export function AppLayout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen w-full overflow-x-hidden bg-background">
      <main className="w-full overflow-x-hidden pb-safe">{children}</main>
      <BottomNav />
      <InstallBanner />
    </div>
  );
}

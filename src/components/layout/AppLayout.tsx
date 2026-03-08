import { ReactNode } from 'react';
import { BottomNav } from './BottomNav';

export function AppLayout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen bg-background">
      <main className="pb-safe">{children}</main>
      <BottomNav />
    </div>
  );
}

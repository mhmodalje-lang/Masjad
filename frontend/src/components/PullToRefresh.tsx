/**
 * PullToRefresh - Native-like pull-to-refresh gesture
 * Works in both native and web modes
 * Shows a smooth loading indicator when pulling down
 */
import { useState, useRef, useCallback, useEffect } from 'react';
import { motion, useMotionValue, useTransform, AnimatePresence } from 'framer-motion';
import { hapticFeedback, isNativeApp } from '@/lib/nativeBridge';
import { RefreshCw } from 'lucide-react';

const PULL_THRESHOLD = 80;
const MAX_PULL = 120;

interface PullToRefreshProps {
  onRefresh: () => Promise<void>;
  children: React.ReactNode;
  disabled?: boolean;
}

export function PullToRefresh({ onRefresh, children, disabled = false }: PullToRefreshProps) {
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [isPulling, setIsPulling] = useState(false);
  const pullDistance = useMotionValue(0);
  const startY = useRef(0);
  const containerRef = useRef<HTMLDivElement>(null);
  const didTriggerHaptic = useRef(false);

  const opacity = useTransform(pullDistance, [0, PULL_THRESHOLD], [0, 1]);
  const scale = useTransform(pullDistance, [0, PULL_THRESHOLD], [0.5, 1]);
  const rotate = useTransform(pullDistance, [0, MAX_PULL], [0, 360]);

  const handleTouchStart = useCallback((e: TouchEvent) => {
    if (disabled || isRefreshing) return;
    const scrollTop = containerRef.current?.scrollTop ?? window.scrollY;
    if (scrollTop > 5) return;
    startY.current = e.touches[0].clientY;
    didTriggerHaptic.current = false;
  }, [disabled, isRefreshing]);

  const handleTouchMove = useCallback((e: TouchEvent) => {
    if (disabled || isRefreshing || startY.current === 0) return;
    const scrollTop = containerRef.current?.scrollTop ?? window.scrollY;
    if (scrollTop > 5) return;

    const currentY = e.touches[0].clientY;
    const diff = currentY - startY.current;

    if (diff > 0) {
      const pull = Math.min(diff * 0.5, MAX_PULL);
      pullDistance.set(pull);
      setIsPulling(true);

      // Haptic when threshold reached
      if (pull >= PULL_THRESHOLD && !didTriggerHaptic.current) {
        didTriggerHaptic.current = true;
        hapticFeedback('medium');
      }
    }
  }, [disabled, isRefreshing, pullDistance]);

  const handleTouchEnd = useCallback(async () => {
    if (disabled || isRefreshing) return;
    const currentPull = pullDistance.get();

    if (currentPull >= PULL_THRESHOLD) {
      setIsRefreshing(true);
      hapticFeedback('success');
      pullDistance.set(60);
      try {
        await onRefresh();
      } finally {
        setIsRefreshing(false);
      }
    }

    pullDistance.set(0);
    setIsPulling(false);
    startY.current = 0;
  }, [disabled, isRefreshing, onRefresh, pullDistance]);

  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;

    el.addEventListener('touchstart', handleTouchStart, { passive: true });
    el.addEventListener('touchmove', handleTouchMove, { passive: true });
    el.addEventListener('touchend', handleTouchEnd, { passive: true });

    return () => {
      el.removeEventListener('touchstart', handleTouchStart);
      el.removeEventListener('touchmove', handleTouchMove);
      el.removeEventListener('touchend', handleTouchEnd);
    };
  }, [handleTouchStart, handleTouchMove, handleTouchEnd]);

  return (
    <div ref={containerRef} className="relative min-h-full">
      {/* Pull indicator */}
      <AnimatePresence>
        {(isPulling || isRefreshing) && (
          <motion.div
            className="absolute top-0 left-0 right-0 flex items-center justify-center z-50 pointer-events-none"
            style={{ height: 60 }}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <motion.div
              className="w-10 h-10 rounded-full bg-card shadow-lg border border-border/50 flex items-center justify-center"
              style={{ opacity, scale }}
            >
              {isRefreshing ? (
                <RefreshCw className="h-5 w-5 text-primary animate-spin" />
              ) : (
                <motion.div style={{ rotate }}>
                  <RefreshCw className="h-5 w-5 text-muted-foreground" />
                </motion.div>
              )}
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Content with pull offset */}
      <motion.div style={{ y: useTransform(pullDistance, [0, MAX_PULL], [0, 60]) }}>
        {children}
      </motion.div>
    </div>
  );
}

/**
 * NativePageTransition - iOS/Android-like page transitions
 * Provides slide animations that mimic native app navigation
 * Uses Framer Motion for smooth 60fps animations
 */
import { motion } from 'framer-motion';
import { useLocation } from 'react-router-dom';

// Simple fade transition that feels native and doesn't cause layout issues
const pageVariants = {
  initial: {
    opacity: 0,
  },
  enter: {
    opacity: 1,
    transition: {
      duration: 0.2,
      ease: [0.25, 0.1, 0.25, 1],
    },
  },
  exit: {
    opacity: 0,
    transition: {
      duration: 0.15,
      ease: [0.25, 0.1, 0.25, 1],
    },
  },
};

export function NativePageTransition({ children }: { children: React.ReactNode }) {
  const location = useLocation();

  return (
    <motion.div
      key={location.pathname}
      variants={pageVariants}
      initial="initial"
      animate="enter"
      exit="exit"
      className="w-full min-h-full"
    >
      {children}
    </motion.div>
  );
}

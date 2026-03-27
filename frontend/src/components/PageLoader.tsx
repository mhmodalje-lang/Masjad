/**
 * PageLoader - Loading component for Suspense fallbacks
 * Shows a smooth loading animation while lazy pages load
 */
import { motion } from 'framer-motion';

export default function PageLoader() {
  const isDark = document.documentElement.classList.contains('dark');
  
  return (
    <div className="min-h-[60vh] flex flex-col items-center justify-center px-4">
      {/* Animated Mosque Icon */}
      <motion.div
        className="mb-6"
        animate={{ 
          scale: [1, 1.1, 1],
          opacity: [0.6, 1, 0.6]
        }}
        transition={{ 
          duration: 1.5, 
          repeat: Infinity, 
          ease: 'easeInOut' 
        }}
      >
        <div className={`w-16 h-16 rounded-2xl flex items-center justify-center ${
          isDark ? 'bg-emerald-900/30' : 'bg-emerald-100'
        }`}>
          <span className="text-3xl">🕌</span>
        </div>
      </motion.div>
      
      {/* Loading Bar */}
      <div className={`w-48 h-1.5 rounded-full overflow-hidden ${
        isDark ? 'bg-white/10' : 'bg-gray-200'
      }`}>
        <motion.div
          className="h-full rounded-full bg-gradient-to-r from-emerald-500 to-teal-500"
          animate={{ x: ['-100%', '100%'] }}
          transition={{ duration: 1.2, repeat: Infinity, ease: 'easeInOut' }}
          style={{ width: '60%' }}
        />
      </div>
      
      <p className={`mt-4 text-sm ${
        isDark ? 'text-white/40' : 'text-gray-400'
      }`}>
        جاري التحميل...
      </p>
    </div>
  );
}

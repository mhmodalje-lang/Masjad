import React, { useState } from 'react';
import { useLocale } from '@/hooks/useLocale';
import { ChevronLeft, ChevronRight, BookOpen } from 'lucide-react';
import { cn } from '@/lib/utils';

/* ═══════════════════════════════════════════════════════════════
   SALAH TEACHING GUIDE - Accurate Islamic Prayer Position Illustrations
   Source: Based on authentic fiqh (Islamic jurisprudence) references
   Illustrations: SVG silhouettes showing correct body positions
   ═══════════════════════════════════════════════════════════════ */

// SVG Prayer Position Illustrations - Accurate and Clear
const PrayerIllustration: React.FC<{ position: string; size?: number }> = ({ position, size = 200 }) => {
  const w = size;
  const h = size;

  const illustrations: Record<string, React.ReactNode> = {
    // Step 1: Standing with intention - person standing straight facing forward
    qiyam_niyyah: (
      <svg width={w} height={h} viewBox="0 0 200 240" fill="none" xmlns="http://www.w3.org/2000/svg">
        {/* Prayer mat */}
        <ellipse cx="100" cy="225" rx="60" ry="10" fill="#2D5A27" opacity="0.3" />
        <rect x="40" y="215" width="120" height="8" rx="4" fill="#2D5A27" opacity="0.5" />
        {/* Qibla arrow */}
        <path d="M100 10 L110 25 L103 25 L103 40 L97 40 L97 25 L90 25 Z" fill="#D4A853" opacity="0.6" />
        <text x="100" y="52" textAnchor="middle" fill="#D4A853" fontSize="8" opacity="0.7">القبلة</text>
        {/* Body - Standing straight */}
        <circle cx="100" cy="75" r="16" fill="#1B5E20" /> {/* Head */}
        <rect x="86" y="91" width="28" height="55" rx="6" fill="#2E7D32" /> {/* Torso */}
        {/* Thobe/clothing */}
        <path d="M82 95 Q100 90 118 95 L120 180 Q100 185 80 180 Z" fill="#388E3C" opacity="0.8" />
        {/* Arms at sides */}
        <rect x="72" y="95" width="10" height="45" rx="4" fill="#2E7D32" />
        <rect x="118" y="95" width="10" height="45" rx="4" fill="#2E7D32" />
        {/* Legs */}
        <rect x="88" y="175" width="10" height="40" rx="4" fill="#1B5E20" />
        <rect x="102" y="175" width="10" height="40" rx="4" fill="#1B5E20" />
        {/* Eyes looking down (at sujud spot) */}
        <circle cx="95" cy="73" r="2" fill="white" />
        <circle cx="105" cy="73" r="2" fill="white" />
        <circle cx="95" cy="74" r="1" fill="#333" />
        <circle cx="105" cy="74" r="1" fill="#333" />
      </svg>
    ),

    // Step 2: Takbir - Hands raised to ears
    takbir: (
      <svg width={w} height={h} viewBox="0 0 200 240" fill="none" xmlns="http://www.w3.org/2000/svg">
        <ellipse cx="100" cy="225" rx="60" ry="10" fill="#2D5A27" opacity="0.3" />
        <rect x="40" y="215" width="120" height="8" rx="4" fill="#2D5A27" opacity="0.5" />
        {/* Body */}
        <circle cx="100" cy="75" r="16" fill="#1B5E20" />
        <path d="M82 95 Q100 90 118 95 L120 180 Q100 185 80 180 Z" fill="#388E3C" opacity="0.8" />
        {/* Arms RAISED to ears - key position */}
        <rect x="65" y="55" width="10" height="42" rx="4" fill="#2E7D32" transform="rotate(-10 70 76)" />
        <rect x="125" y="55" width="10" height="42" rx="4" fill="#2E7D32" transform="rotate(10 130 76)" />
        {/* Hands (palms facing qibla) */}
        <rect x="60" y="48" width="14" height="16" rx="3" fill="#A5D6A7" stroke="#2E7D32" strokeWidth="1" />
        <rect x="126" y="48" width="14" height="16" rx="3" fill="#A5D6A7" stroke="#2E7D32" strokeWidth="1" />
        {/* Fingers spread */}
        <line x1="62" y1="48" x2="62" y2="42" stroke="#2E7D32" strokeWidth="2" strokeLinecap="round" />
        <line x1="66" y1="48" x2="66" y2="40" stroke="#2E7D32" strokeWidth="2" strokeLinecap="round" />
        <line x1="70" y1="48" x2="70" y2="42" stroke="#2E7D32" strokeWidth="2" strokeLinecap="round" />
        <line x1="130" y1="48" x2="130" y2="42" stroke="#2E7D32" strokeWidth="2" strokeLinecap="round" />
        <line x1="134" y1="48" x2="134" y2="40" stroke="#2E7D32" strokeWidth="2" strokeLinecap="round" />
        <line x1="138" y1="48" x2="138" y2="42" stroke="#2E7D32" strokeWidth="2" strokeLinecap="round" />
        {/* Legs */}
        <rect x="88" y="175" width="10" height="40" rx="4" fill="#1B5E20" />
        <rect x="102" y="175" width="10" height="40" rx="4" fill="#1B5E20" />
        {/* Allahu Akbar text */}
        <text x="100" y="28" textAnchor="middle" fill="#D4A853" fontSize="11" fontWeight="bold">اللّهُ أَكْبَر</text>
      </svg>
    ),

    // Step 3: Standing with hands on chest
    qiyam_qiraa: (
      <svg width={w} height={h} viewBox="0 0 200 240" fill="none" xmlns="http://www.w3.org/2000/svg">
        <ellipse cx="100" cy="225" rx="60" ry="10" fill="#2D5A27" opacity="0.3" />
        <rect x="40" y="215" width="120" height="8" rx="4" fill="#2D5A27" opacity="0.5" />
        {/* Body */}
        <circle cx="100" cy="75" r="16" fill="#1B5E20" />
        <path d="M82 95 Q100 90 118 95 L120 180 Q100 185 80 180 Z" fill="#388E3C" opacity="0.8" />
        {/* Arms folded on chest - RIGHT over LEFT */}
        <rect x="80" y="102" width="40" height="8" rx="3" fill="#2E7D32" />
        <rect x="78" y="108" width="44" height="8" rx="3" fill="#1B5E20" />
        {/* Highlight right over left */}
        <rect x="82" y="104" width="36" height="4" rx="2" fill="#A5D6A7" opacity="0.4" />
        {/* Legs */}
        <rect x="88" y="175" width="10" height="40" rx="4" fill="#1B5E20" />
        <rect x="102" y="175" width="10" height="40" rx="4" fill="#1B5E20" />
        {/* Eyes looking down */}
        <circle cx="96" cy="74" r="1.5" fill="#333" />
        <circle cx="104" cy="74" r="1.5" fill="#333" />
      </svg>
    ),

    // Step 4: Reciting Al-Fatiha (same as hands on chest, with Quran glow)
    qiyam_fatiha: (
      <svg width={w} height={h} viewBox="0 0 200 240" fill="none" xmlns="http://www.w3.org/2000/svg">
        <ellipse cx="100" cy="225" rx="60" ry="10" fill="#2D5A27" opacity="0.3" />
        <rect x="40" y="215" width="120" height="8" rx="4" fill="#2D5A27" opacity="0.5" />
        {/* Glow effect for recitation */}
        <circle cx="100" cy="110" r="30" fill="#FFF9C4" opacity="0.15" />
        <circle cx="100" cy="110" r="20" fill="#FFF9C4" opacity="0.1" />
        {/* Body */}
        <circle cx="100" cy="75" r="16" fill="#1B5E20" />
        <path d="M82 95 Q100 90 118 95 L120 180 Q100 185 80 180 Z" fill="#388E3C" opacity="0.8" />
        {/* Arms folded on chest */}
        <rect x="80" y="102" width="40" height="8" rx="3" fill="#2E7D32" />
        <rect x="78" y="108" width="44" height="8" rx="3" fill="#1B5E20" />
        {/* Legs */}
        <rect x="88" y="175" width="10" height="40" rx="4" fill="#1B5E20" />
        <rect x="102" y="175" width="10" height="40" rx="4" fill="#1B5E20" />
        {/* Quran verse indicator */}
        <text x="100" y="20" textAnchor="middle" fill="#D4A853" fontSize="9">الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ</text>
        <text x="100" y="32" textAnchor="middle" fill="#D4A853" fontSize="8" opacity="0.7">سورة الفاتحة</text>
      </svg>
    ),

    // Step 5: Ruku (Bowing) - Back straight like a table
    ruku: (
      <svg width={w} height={h} viewBox="0 0 200 240" fill="none" xmlns="http://www.w3.org/2000/svg">
        <ellipse cx="100" cy="225" rx="60" ry="10" fill="#2D5A27" opacity="0.3" />
        <rect x="40" y="215" width="120" height="8" rx="4" fill="#2D5A27" opacity="0.5" />
        {/* Head - positioned forward */}
        <circle cx="62" cy="105" r="14" fill="#1B5E20" />
        {/* Back - FLAT like a table (key point!) */}
        <rect x="60" y="100" width="55" height="15" rx="5" fill="#388E3C" />
        {/* Dotted line showing flat back */}
        <line x1="55" y1="107" x2="120" y2="107" stroke="#A5D6A7" strokeWidth="1" strokeDasharray="4,3" opacity="0.5" />
        {/* Lower body - vertical */}
        <rect x="105" y="108" width="15" height="60" rx="5" fill="#2E7D32" />
        {/* Legs - straight */}
        <rect x="105" y="165" width="10" height="50" rx="4" fill="#1B5E20" />
        <rect x="118" y="165" width="10" height="50" rx="4" fill="#1B5E20" />
        {/* Arms going down to knees - HANDS ON KNEES */}
        <line x1="80" y1="112" x2="105" y2="155" stroke="#2E7D32" strokeWidth="8" strokeLinecap="round" />
        <line x1="90" y1="112" x2="118" y2="155" stroke="#2E7D32" strokeWidth="8" strokeLinecap="round" />
        {/* Hands on knees */}
        <circle cx="105" cy="158" r="5" fill="#A5D6A7" />
        <circle cx="118" cy="158" r="5" fill="#A5D6A7" />
        {/* Dhikr */}
        <text x="100" y="30" textAnchor="middle" fill="#D4A853" fontSize="9" fontWeight="bold">سُبْحَانَ رَبِّيَ الْعَظِيم</text>
      </svg>
    ),

    // Step 6: Rising from Ruku
    itidal: (
      <svg width={w} height={h} viewBox="0 0 200 240" fill="none" xmlns="http://www.w3.org/2000/svg">
        <ellipse cx="100" cy="225" rx="60" ry="10" fill="#2D5A27" opacity="0.3" />
        <rect x="40" y="215" width="120" height="8" rx="4" fill="#2D5A27" opacity="0.5" />
        {/* Body - standing straight */}
        <circle cx="100" cy="68" r="16" fill="#1B5E20" />
        <path d="M82 88 Q100 83 118 88 L120 175 Q100 180 80 175 Z" fill="#388E3C" opacity="0.8" />
        {/* Arms at sides */}
        <rect x="72" y="90" width="10" height="45" rx="4" fill="#2E7D32" />
        <rect x="118" y="90" width="10" height="45" rx="4" fill="#2E7D32" />
        {/* Legs */}
        <rect x="88" y="172" width="10" height="42" rx="4" fill="#1B5E20" />
        <rect x="102" y="172" width="10" height="42" rx="4" fill="#1B5E20" />
        {/* Up arrow showing rising motion */}
        <path d="M45 120 L50 135 L47 135 L47 155 L43 155 L43 135 L40 135 Z" fill="#A5D6A7" opacity="0.4" />
        {/* Dhikr */}
        <text x="100" y="25" textAnchor="middle" fill="#D4A853" fontSize="8" fontWeight="bold">سَمِعَ اللّهُ لِمَنْ حَمِدَه</text>
        <text x="100" y="40" textAnchor="middle" fill="#D4A853" fontSize="7" opacity="0.7">رَبَّنَا وَلَكَ الْحَمْد</text>
      </svg>
    ),

    // Step 7: First Sujud (Prostration) - 7 body parts on ground
    sujud_1: (
      <svg width={w} height={h} viewBox="0 0 200 240" fill="none" xmlns="http://www.w3.org/2000/svg">
        <ellipse cx="100" cy="225" rx="70" ry="10" fill="#2D5A27" opacity="0.3" />
        <rect x="30" y="215" width="140" height="8" rx="4" fill="#2D5A27" opacity="0.5" />
        {/* Ground line */}
        <line x1="25" y1="205" x2="175" y2="205" stroke="#4CAF50" strokeWidth="1" opacity="0.3" />
        {/* Head touching ground (forehead + nose) */}
        <circle cx="55" cy="195" r="13" fill="#1B5E20" />
        {/* Mark showing forehead touching ground */}
        <line x1="48" y1="205" x2="62" y2="205" stroke="#D4A853" strokeWidth="2" />
        {/* Back - angled upward */}
        <path d="M65 190 Q90 170 110 160" stroke="#388E3C" strokeWidth="14" strokeLinecap="round" fill="none" />
        {/* Upper body fill */}
        <path d="M60 192 Q85 172 108 162 L115 168 Q88 178 65 198 Z" fill="#388E3C" opacity="0.8" />
        {/* Hips raised */}
        <ellipse cx="118" cy="155" rx="12" ry="10" fill="#2E7D32" />
        {/* Legs - knees on ground */}
        <path d="M115 162 L125 195 L130 205" stroke="#1B5E20" strokeWidth="10" strokeLinecap="round" fill="none" />
        <path d="M120 162 L135 195 L145 205" stroke="#1B5E20" strokeWidth="10" strokeLinecap="round" fill="none" />
        {/* Arms/Palms on ground next to head */}
        <line x1="65" y1="188" x2="42" y2="200" stroke="#2E7D32" strokeWidth="7" strokeLinecap="round" />
        <line x1="65" y1="188" x2="80" y2="200" stroke="#2E7D32" strokeWidth="7" strokeLinecap="round" />
        {/* Palm markers on ground */}
        <rect x="35" y="199" width="12" height="7" rx="2" fill="#A5D6A7" />
        <rect x="73" y="199" width="12" height="7" rx="2" fill="#A5D6A7" />
        {/* Toes on ground */}
        <rect x="126" y="200" width="8" height="6" rx="2" fill="#A5D6A7" />
        <rect x="140" y="200" width="8" height="6" rx="2" fill="#A5D6A7" />
        {/* 7 body parts markers */}
        <text x="100" y="25" textAnchor="middle" fill="#D4A853" fontSize="9" fontWeight="bold">سُبْحَانَ رَبِّيَ الأَعْلَى</text>
        <text x="100" y="42" textAnchor="middle" fill="#81C784" fontSize="7">السجود على ٧ أعضاء</text>
        {/* Small number indicators for 7 parts */}
        <circle cx="55" cy="207" r="4" fill="#D4A853" opacity="0.7" />
        <text x="55" y="210" textAnchor="middle" fill="white" fontSize="5">1</text>
        <circle cx="41" cy="207" r="4" fill="#D4A853" opacity="0.7" />
        <text x="41" y="210" textAnchor="middle" fill="white" fontSize="5">2</text>
        <circle cx="79" cy="207" r="4" fill="#D4A853" opacity="0.7" />
        <text x="79" y="210" textAnchor="middle" fill="white" fontSize="5">3</text>
        <circle cx="130" cy="207" r="4" fill="#D4A853" opacity="0.7" />
        <text x="130" y="210" textAnchor="middle" fill="white" fontSize="5">6</text>
        <circle cx="144" cy="207" r="4" fill="#D4A853" opacity="0.7" />
        <text x="144" y="210" textAnchor="middle" fill="white" fontSize="5">7</text>
      </svg>
    ),

    // Step 8: Sitting between two prostrations
    juloos: (
      <svg width={w} height={h} viewBox="0 0 200 240" fill="none" xmlns="http://www.w3.org/2000/svg">
        <ellipse cx="100" cy="225" rx="60" ry="10" fill="#2D5A27" opacity="0.3" />
        <rect x="40" y="215" width="120" height="8" rx="4" fill="#2D5A27" opacity="0.5" />
        {/* Head */}
        <circle cx="100" cy="100" r="15" fill="#1B5E20" />
        {/* Upper body */}
        <rect x="87" y="115" width="26" height="35" rx="5" fill="#388E3C" />
        {/* Sitting body - on left foot */}
        <path d="M85 148 Q100 152 115 148 L115 185 Q100 190 85 185 Z" fill="#2E7D32" opacity="0.8" />
        {/* Left leg - spread beneath (iftirash) */}
        <path d="M85 180 L60 200 L55 205" stroke="#1B5E20" strokeWidth="10" strokeLinecap="round" fill="none" />
        {/* Right foot - upright */}
        <path d="M115 180 L130 195 L135 205" stroke="#1B5E20" strokeWidth="10" strokeLinecap="round" fill="none" />
        <line x1="135" y1="205" x2="135" y2="190" stroke="#1B5E20" strokeWidth="6" strokeLinecap="round" />
        {/* Hands on thighs */}
        <rect x="78" y="155" width="10" height="18" rx="3" fill="#A5D6A7" />
        <rect x="112" y="155" width="10" height="18" rx="3" fill="#A5D6A7" />
        {/* Dhikr */}
        <text x="100" y="35" textAnchor="middle" fill="#D4A853" fontSize="10" fontWeight="bold">رَبِّ اغْفِرْ لِي</text>
      </svg>
    ),

    // Step 9: Second Sujud (same as first - reuse sujud_1)
    sujud_2: (
      <svg width={w} height={h} viewBox="0 0 200 240" fill="none" xmlns="http://www.w3.org/2000/svg">
        <ellipse cx="100" cy="225" rx="70" ry="10" fill="#2D5A27" opacity="0.3" />
        <rect x="30" y="215" width="140" height="8" rx="4" fill="#2D5A27" opacity="0.5" />
        <line x1="25" y1="205" x2="175" y2="205" stroke="#4CAF50" strokeWidth="1" opacity="0.3" />
        <circle cx="55" cy="195" r="13" fill="#1B5E20" />
        <line x1="48" y1="205" x2="62" y2="205" stroke="#D4A853" strokeWidth="2" />
        <path d="M60 192 Q85 172 108 162 L115 168 Q88 178 65 198 Z" fill="#388E3C" opacity="0.8" />
        <ellipse cx="118" cy="155" rx="12" ry="10" fill="#2E7D32" />
        <path d="M115 162 L125 195 L130 205" stroke="#1B5E20" strokeWidth="10" strokeLinecap="round" fill="none" />
        <path d="M120 162 L135 195 L145 205" stroke="#1B5E20" strokeWidth="10" strokeLinecap="round" fill="none" />
        <line x1="65" y1="188" x2="42" y2="200" stroke="#2E7D32" strokeWidth="7" strokeLinecap="round" />
        <line x1="65" y1="188" x2="80" y2="200" stroke="#2E7D32" strokeWidth="7" strokeLinecap="round" />
        <rect x="35" y="199" width="12" height="7" rx="2" fill="#A5D6A7" />
        <rect x="73" y="199" width="12" height="7" rx="2" fill="#A5D6A7" />
        <rect x="126" y="200" width="8" height="6" rx="2" fill="#A5D6A7" />
        <rect x="140" y="200" width="8" height="6" rx="2" fill="#A5D6A7" />
        <text x="100" y="25" textAnchor="middle" fill="#D4A853" fontSize="9" fontWeight="bold">سُبْحَانَ رَبِّيَ الأَعْلَى</text>
        {/* Second sujud label */}
        <text x="100" y="42" textAnchor="middle" fill="#81C784" fontSize="7">السجدة الثانية</text>
        {/* ② marker */}
        <circle cx="170" cy="140" r="12" fill="#D4A853" opacity="0.6" />
        <text x="170" y="144" textAnchor="middle" fill="white" fontSize="10" fontWeight="bold">٢</text>
      </svg>
    ),

    // Step 10: Tashahhud - Sitting with index finger pointing
    tashahhud: (
      <svg width={w} height={h} viewBox="0 0 200 240" fill="none" xmlns="http://www.w3.org/2000/svg">
        <ellipse cx="100" cy="225" rx="60" ry="10" fill="#2D5A27" opacity="0.3" />
        <rect x="40" y="215" width="120" height="8" rx="4" fill="#2D5A27" opacity="0.5" />
        {/* Head */}
        <circle cx="100" cy="95" r="15" fill="#1B5E20" />
        {/* Upper body */}
        <rect x="87" y="110" width="26" height="35" rx="5" fill="#388E3C" />
        {/* Sitting body */}
        <path d="M85 143 Q100 147 115 143 L115 182 Q100 187 85 182 Z" fill="#2E7D32" opacity="0.8" />
        {/* Left leg - spread beneath */}
        <path d="M85 178 L60 198 L55 205" stroke="#1B5E20" strokeWidth="10" strokeLinecap="round" fill="none" />
        {/* Right foot */}
        <path d="M115 178 L130 193 L135 205" stroke="#1B5E20" strokeWidth="10" strokeLinecap="round" fill="none" />
        {/* Left hand on thigh */}
        <rect x="78" y="152" width="10" height="18" rx="3" fill="#A5D6A7" />
        {/* Right hand - INDEX FINGER POINTING (key feature!) */}
        <rect x="112" y="152" width="10" height="14" rx="3" fill="#A5D6A7" />
        {/* Index finger pointing */}
        <line x1="117" y1="152" x2="117" y2="138" stroke="#A5D6A7" strokeWidth="3" strokeLinecap="round" />
        {/* Glow on finger */}
        <circle cx="117" cy="136" r="4" fill="#FFF9C4" opacity="0.3" />
        {/* Arrow showing pointing */}
        <path d="M117 135 L114 140 L120 140 Z" fill="#D4A853" opacity="0.6" />
        {/* Dhikr */}
        <text x="100" y="28" textAnchor="middle" fill="#D4A853" fontSize="7" fontWeight="bold">أَشْهَدُ أَنْ لَا إِلَهَ إِلَّا اللَّه</text>
        <text x="100" y="42" textAnchor="middle" fill="#D4A853" fontSize="7" opacity="0.8">التحيات والصلاة الإبراهيمية</text>
      </svg>
    ),

    // Step 11: Tasleem - Turning head right and left
    tasleem: (
      <svg width={w} height={h} viewBox="0 0 200 240" fill="none" xmlns="http://www.w3.org/2000/svg">
        <ellipse cx="100" cy="225" rx="60" ry="10" fill="#2D5A27" opacity="0.3" />
        <rect x="40" y="215" width="120" height="8" rx="4" fill="#2D5A27" opacity="0.5" />
        {/* Body sitting */}
        <rect x="87" y="115" width="26" height="35" rx="5" fill="#388E3C" />
        <path d="M85 148 Q100 152 115 148 L115 185 Q100 190 85 185 Z" fill="#2E7D32" opacity="0.8" />
        {/* Left leg */}
        <path d="M85 180 L60 200 L55 205" stroke="#1B5E20" strokeWidth="10" strokeLinecap="round" fill="none" />
        {/* Right foot */}
        <path d="M115 180 L130 195 L135 205" stroke="#1B5E20" strokeWidth="10" strokeLinecap="round" fill="none" />
        {/* Head turned slightly right */}
        <circle cx="108" cy="100" r="15" fill="#1B5E20" />
        {/* Right arrow */}
        <path d="M145 90 L160 90 L155 85 M160 90 L155 95" stroke="#D4A853" strokeWidth="2" strokeLinecap="round" fill="none" />
        <text x="162" y="100" fill="#D4A853" fontSize="7" opacity="0.7">→</text>
        {/* Left arrow */}
        <path d="M55 90 L40 90 L45 85 M40 90 L45 95" stroke="#81C784" strokeWidth="2" strokeLinecap="round" fill="none" />
        <text x="32" y="100" fill="#81C784" fontSize="7" opacity="0.7">←</text>
        {/* Hands on thighs */}
        <rect x="78" y="155" width="10" height="18" rx="3" fill="#A5D6A7" />
        <rect x="112" y="155" width="10" height="18" rx="3" fill="#A5D6A7" />
        {/* Salam text */}
        <text x="155" y="78" textAnchor="middle" fill="#D4A853" fontSize="7" fontWeight="bold">يميناً</text>
        <text x="45" y="78" textAnchor="middle" fill="#81C784" fontSize="7" fontWeight="bold">يساراً</text>
        <text x="100" y="25" textAnchor="middle" fill="#D4A853" fontSize="9" fontWeight="bold">السَّلَامُ عَلَيْكُمْ وَرَحْمَةُ اللَّه</text>
        {/* Completion star */}
        <text x="100" y="55" textAnchor="middle" fill="#FFC107" fontSize="14">⭐</text>
      </svg>
    ),
  };

  return (
    <div className="flex items-center justify-center">
      {illustrations[position] || illustrations['qiyam_niyyah']}
    </div>
  );
};

// Step color mapping
const STEP_COLORS: Record<string, { bg: string; border: string; text: string; badge: string }> = {
  qiyam_niyyah: { bg: 'from-emerald-900/40 to-emerald-800/20', border: 'border-emerald-600/30', text: 'text-emerald-400', badge: 'bg-emerald-600' },
  takbir: { bg: 'from-amber-900/40 to-amber-800/20', border: 'border-amber-600/30', text: 'text-amber-400', badge: 'bg-amber-600' },
  qiyam_qiraa: { bg: 'from-teal-900/40 to-teal-800/20', border: 'border-teal-600/30', text: 'text-teal-400', badge: 'bg-teal-600' },
  qiyam_fatiha: { bg: 'from-yellow-900/40 to-yellow-800/20', border: 'border-yellow-600/30', text: 'text-yellow-400', badge: 'bg-yellow-600' },
  ruku: { bg: 'from-blue-900/40 to-blue-800/20', border: 'border-blue-600/30', text: 'text-blue-400', badge: 'bg-blue-600' },
  itidal: { bg: 'from-cyan-900/40 to-cyan-800/20', border: 'border-cyan-600/30', text: 'text-cyan-400', badge: 'bg-cyan-600' },
  sujud_1: { bg: 'from-green-900/40 to-green-800/20', border: 'border-green-600/30', text: 'text-green-400', badge: 'bg-green-600' },
  juloos: { bg: 'from-purple-900/40 to-purple-800/20', border: 'border-purple-600/30', text: 'text-purple-400', badge: 'bg-purple-600' },
  sujud_2: { bg: 'from-green-900/40 to-green-800/20', border: 'border-green-600/30', text: 'text-green-400', badge: 'bg-green-600' },
  tashahhud: { bg: 'from-indigo-900/40 to-indigo-800/20', border: 'border-indigo-600/30', text: 'text-indigo-400', badge: 'bg-indigo-600' },
  tasleem: { bg: 'from-rose-900/40 to-rose-800/20', border: 'border-rose-600/30', text: 'text-rose-400', badge: 'bg-rose-600' },
};

interface SalahStep {
  step: number;
  position: string;
  title: string;
  description: string;
  dhikr_ar: string;
  dhikr_transliteration: string;
  body_position: string;
}

interface SalahGuideProps {
  steps: SalahStep[];
}

const SalahGuide: React.FC<SalahGuideProps> = ({ steps }) => {
  const { t, dir } = useLocale();
  const isRtl = dir === 'rtl';
  const [currentStep, setCurrentStep] = useState(0);
  const [viewMode, setViewMode] = useState<'card' | 'list'>('card');

  if (!steps || steps.length === 0) return null;

  const step = steps[currentStep];
  const colors = STEP_COLORS[step?.position] || STEP_COLORS.qiyam_niyyah;

  const goNext = () => setCurrentStep(prev => Math.min(prev + 1, steps.length - 1));
  const goPrev = () => setCurrentStep(prev => Math.max(prev - 1, 0));

  return (
    <div className="space-y-3" dir={dir}>
      {/* Header */}
      <div className="text-center p-4 rounded-2xl bg-gradient-to-br from-green-500/15 to-emerald-500/10 border border-green-400/30">
        <span className="text-3xl">🕌</span>
        <h3 className="font-bold mt-1 text-lg">{isRtl ? 'تعليم الصلاة خطوة بخطوة' : 'Learn Prayer Step by Step'}</h3>
        <p className="text-xs text-muted-foreground mt-1">
          {isRtl ? 'مصدر: الفقه الإسلامي الصحيح • رسومات توضيحية دقيقة' : 'Source: Authentic Islamic Jurisprudence • Accurate Illustrations'}
        </p>
        {/* View mode toggle */}
        <div className="flex items-center justify-center gap-2 mt-2">
          <button
            onClick={() => setViewMode('card')}
            className={cn("px-3 py-1 rounded-full text-xs font-medium transition-all", viewMode === 'card' ? 'bg-green-600 text-white' : 'bg-white/10 text-muted-foreground')}
          >
            {isRtl ? 'بطاقات' : 'Cards'}
          </button>
          <button
            onClick={() => setViewMode('list')}
            className={cn("px-3 py-1 rounded-full text-xs font-medium transition-all", viewMode === 'list' ? 'bg-green-600 text-white' : 'bg-white/10 text-muted-foreground')}
          >
            {isRtl ? 'قائمة' : 'List'}
          </button>
        </div>
      </div>

      {/* CARD VIEW - Interactive step-by-step */}
      {viewMode === 'card' && (
        <>
          {/* Step Progress Bar */}
          <div className="flex gap-1 px-2">
            {steps.map((s, i) => (
              <button
                key={s.step}
                onClick={() => setCurrentStep(i)}
                className={cn(
                  "flex-1 h-2 rounded-full transition-all duration-300",
                  i === currentStep ? 'bg-green-500 scale-y-125' : i < currentStep ? 'bg-green-700' : 'bg-white/10'
                )}
              />
            ))}
          </div>

          {/* Step Counter */}
          <div className="text-center">
            <span className={cn("inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-bold", colors.badge, "text-white")}>
              {isRtl ? `الخطوة ${step.step} من ${steps.length}` : `Step ${step.step} of ${steps.length}`}
            </span>
          </div>

          {/* Main Step Card */}
          <div className={cn("rounded-2xl border p-4 bg-gradient-to-br", colors.bg, colors.border, "transition-all duration-500")}>
            {/* Step Title */}
            <h4 className={cn("text-lg font-bold text-center mb-3", colors.text)}>
              {step.title}
            </h4>

            {/* Illustration */}
            <div className="flex justify-center mb-4 bg-black/20 rounded-xl p-3">
              <PrayerIllustration position={step.position} size={200} />
            </div>

            {/* Body Position Indicator */}
            {step.body_position && (
              <div className="text-center mb-3 px-3 py-2 rounded-lg bg-white/5 border border-white/10">
                <span className="text-xs text-muted-foreground">
                  {isRtl ? '🦴 وضع الجسم: ' : '🦴 Body Position: '}
                </span>
                <span className="text-xs font-medium">{step.body_position}</span>
              </div>
            )}

            {/* Description */}
            <div className="p-3 rounded-xl bg-white/5 border border-white/10 mb-3">
              <p className="text-sm leading-relaxed" dir={dir}>
                {step.description}
              </p>
            </div>

            {/* Dhikr / Recitation */}
            {step.dhikr_ar && (
              <div className="p-3 rounded-xl bg-amber-500/10 border border-amber-500/20">
                <div className="flex items-center gap-2 mb-2">
                  <BookOpen className="h-4 w-4 text-amber-400" />
                  <span className="text-xs font-bold text-amber-400">{isRtl ? 'الذكر' : 'Dhikr / Recitation'}</span>
                </div>
                <p className="text-base font-bold text-amber-300 text-center leading-loose" dir="rtl">
                  {step.dhikr_ar}
                </p>
                {step.dhikr_transliteration && (
                  <p className="text-xs text-amber-400/70 text-center mt-1 italic" dir="ltr">
                    {step.dhikr_transliteration}
                  </p>
                )}
              </div>
            )}
          </div>

          {/* Navigation Buttons */}
          <div className="flex items-center justify-between gap-3 px-2">
            <button
              onClick={isRtl ? goNext : goPrev}
              disabled={isRtl ? currentStep >= steps.length - 1 : currentStep <= 0}
              className="flex items-center gap-1 px-4 py-2 rounded-xl bg-white/10 hover:bg-white/20 disabled:opacity-30 disabled:cursor-not-allowed transition-all text-sm font-medium"
            >
              <ChevronRight className="h-4 w-4" />
              {isRtl ? 'التالي' : 'Previous'}
            </button>
            <span className="text-xs text-muted-foreground">
              {step.step} / {steps.length}
            </span>
            <button
              onClick={isRtl ? goPrev : goNext}
              disabled={isRtl ? currentStep <= 0 : currentStep >= steps.length - 1}
              className="flex items-center gap-1 px-4 py-2 rounded-xl bg-green-600 hover:bg-green-700 disabled:opacity-30 disabled:cursor-not-allowed transition-all text-sm font-medium text-white"
            >
              {isRtl ? 'السابق' : 'Next'}
              <ChevronLeft className="h-4 w-4" />
            </button>
          </div>
        </>
      )}

      {/* LIST VIEW - All steps visible */}
      {viewMode === 'list' && (
        <div className="space-y-3">
          {steps.map((s, i) => {
            const c = STEP_COLORS[s.position] || STEP_COLORS.qiyam_niyyah;
            return (
              <div key={s.step} className={cn("rounded-xl border p-3 bg-gradient-to-br", c.bg, c.border)}>
                <div className="flex items-start gap-3">
                  {/* Step number */}
                  <div className={cn("w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold text-white shrink-0", c.badge)}>
                    {s.step}
                  </div>
                  <div className="flex-1 min-w-0">
                    {/* Title */}
                    <h5 className={cn("font-bold text-sm", c.text)}>{s.title}</h5>

                    {/* Mini illustration */}
                    <div className="flex justify-center my-2 bg-black/20 rounded-lg p-2">
                      <PrayerIllustration position={s.position} size={140} />
                    </div>

                    {/* Description */}
                    <p className="text-xs text-muted-foreground leading-relaxed">{s.description}</p>

                    {/* Dhikr */}
                    {s.dhikr_ar && (
                      <div className="mt-2 p-2 rounded-lg bg-amber-500/10 border border-amber-500/20">
                        <p className="text-sm font-bold text-amber-300 text-center" dir="rtl">{s.dhikr_ar}</p>
                        {s.dhikr_transliteration && (
                          <p className="text-[10px] text-amber-400/60 text-center mt-0.5 italic" dir="ltr">{s.dhikr_transliteration}</p>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Islamic Reference Footer */}
      <div className="text-center p-3 rounded-xl bg-white/5 border border-white/10">
        <p className="text-[10px] text-muted-foreground">
          {isRtl
            ? '📚 المرجع: صفة صلاة النبي ﷺ — الشيخ محمد ناصر الدين الألباني • ويكيميديا كومنز (رخصة حرة)'
            : '📚 Reference: The Prophet\'s Prayer Described ﷺ — Shaykh al-Albani • Wikimedia Commons (Free License)'}
        </p>
      </div>
    </div>
  );
};

export default SalahGuide;

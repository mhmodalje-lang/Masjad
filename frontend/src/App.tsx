import { lazy, Suspense, useState, useCallback } from "react";
import React from "react";
import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route, Navigate, useLocation } from "react-router-dom";
import { AnimatePresence } from "framer-motion";
import { LocaleProvider } from "@/hooks/useLocale";
import { AuthProvider } from "@/hooks/useAuth";
import { UnifiedPrayerProvider } from "@/hooks/useUnifiedPrayer";
import { ThemeProvider } from "@/components/ThemeProvider";
import { PermissionManager } from "@/components/PermissionManager";
import { AppLayout } from "@/components/layout/AppLayout";
import { AdConfigProvider } from "@/hooks/useAdConfig";
import { useSEO } from "@/hooks/useSEO";
import { usePrefetch } from "@/hooks/usePrefetch";
import { NativeAppProvider } from "@/components/NativeAppProvider";
import { NativePageTransition } from "@/components/NativePageTransition";
import { isNativeApp } from "@/lib/nativeBridge";
import SplashScreen from "@/components/SplashScreen";
import ScrollToTop from "@/components/ScrollToTop";
import CookieConsent from "@/components/CookieConsent";
import GDPRAdConsent from "@/components/GDPRAdConsent";
import AnalyticsTracker from "@/components/AnalyticsTracker";
import ErrorBoundary from "@/components/ErrorBoundary";
import AgeGate, { hasPassedAgeGate } from "@/components/AgeGate";
import OfflineNotice from "@/components/OfflineNotice";
import RateApp from "@/components/RateApp";
import AppTrackingTransparency from "@/components/AppTrackingTransparency";
import Index from "./pages/Index";

const PrayerTimes = lazy(() => import("./pages/PrayerTimes"));
const Qibla = lazy(() => import("./pages/Qibla"));
const Quran = lazy(() => import("./pages/Quran"));
const SurahView = lazy(() => import("./pages/SurahView"));
const Tasbeeh = lazy(() => import("./pages/Tasbeeh"));
const Duas = lazy(() => import("./pages/Duas"));
const More = lazy(() => import("./pages/More"));
const PrayerTracker = lazy(() => import("./pages/PrayerTracker"));
const ZakatCalculator = lazy(() => import("./pages/ZakatCalculator"));
const Auth = lazy(() => import("./pages/Auth"));
const Stories = lazy(() => import("./pages/Stories"));
const Install = lazy(() => import("./pages/Install"));
const AdminDashboard = lazy(() => import("./pages/AdminDashboard"));
const Account = lazy(() => import("./pages/Account"));
const DailyDuas = lazy(() => import("./pages/DailyDuas"));
const MosquePrayerTimes = lazy(() => import("./pages/MosquePrayerTimes"));
const RamadanChallenge = lazy(() => import("./pages/RamadanChallenge"));
const RamadanCalendar = lazy(() => import("./pages/RamadanCalendar"));
const QuranGoal = lazy(() => import("./pages/QuranGoal"));
const DhikrSettings = lazy(() => import("./pages/DhikrSettings"));
const NotificationSettings = lazy(() => import("./pages/NotificationSettings"));
const Ruqyah = lazy(() => import("./pages/Ruqyah"));
const AsmaAlHusna = lazy(() => import("./pages/AsmaAlHusna"));
const RamadanCards = lazy(() => import("./pages/RamadanCards"));
const RamadanBook = lazy(() => import("./pages/RamadanBook"));
const PeriodTracker = lazy(() => import("./pages/PeriodTracker"));
const Profile = lazy(() => import("./pages/Profile"));
const Messages = lazy(() => import("./pages/Messages"));
const Store = lazy(() => import("./pages/Store"));
const Rewards = lazy(() => import("./pages/Rewards"));
const PointsBalance = lazy(() => import("./pages/PointsBalance"));
const AiAssistant = lazy(() => import("./pages/AiAssistant"));
const Marketplace = lazy(() => import("./pages/Marketplace"));
const Explore = lazy(() => import("./pages/Explore"));
const Sohba = lazy(() => import("./pages/Sohba"));
const AboutUs = lazy(() => import("./pages/AboutUs"));
const PrivacyPolicy = lazy(() => import("./pages/PrivacyPolicy"));
const ContactUs = lazy(() => import("./pages/ContactUs"));
const Donations = lazy(() => import("./pages/Donations"));
const TermsOfService = lazy(() => import("./pages/TermsOfService"));
const NotFound = lazy(() => import("./pages/NotFound"));
// Social Platform Pages (used from Stories/حكاياتي page)
const SocialProfile = lazy(() => import("./pages/SocialProfile"));
const VideoReels = lazy(() => import("./pages/VideoReels"));
const CreatePost = lazy(() => import("./pages/CreatePost"));
const KidsZone = lazy(() => import("./pages/KidsZone"));
const LiveStreams = lazy(() => import("./pages/LiveStreams"));
const BarakaMarket = lazy(() => import("./pages/BarakaMarket"));
const Tafsir = lazy(() => import("./pages/Tafsir"));
const FortyNawawi = lazy(() => import("./pages/FortyNawawi"));
const DataDeletion = lazy(() => import("./pages/DataDeletion"));
const ContentPolicy = lazy(() => import("./pages/ContentPolicy"));

const queryClient = new QueryClient();

function SEOWrapper({ children }: { children: React.ReactNode }) {
  useSEO();
  usePrefetch();
  return <>{children}</>;
}

// Pages that should be accessible without AgeGate (for store review & Google Ads compliance)
const PUBLIC_PATHS = ['/privacy', '/terms', '/about', '/contact', '/delete-data', '/content-policy'];

function isPublicPath(): boolean {
  return PUBLIC_PATHS.some(p => window.location.pathname.startsWith(p));
}

const App = () => {
  const [splashDone, setSplashDone] = useState(() => {
    // Skip splash for public/policy pages (store reviewers & crawlers need instant access)
    if (isPublicPath()) return true;
    return sessionStorage.getItem('splash_shown') === '1';
  });
  const [ageGatePassed, setAgeGatePassed] = useState(() => {
    // Skip AgeGate for public/policy pages (store reviewers & crawlers need instant access)
    if (isPublicPath()) return true;
    return hasPassedAgeGate();
  });

  const handleSplashComplete = useCallback(() => {
    sessionStorage.setItem('splash_shown', '1');
    setSplashDone(true);
  }, []);

  if (!splashDone) {
    return <SplashScreen onComplete={handleSplashComplete} />;
  }

  if (!ageGatePassed) {
    return (
      <ThemeProvider>
        <LocaleProvider>
          <AgeGate onPass={() => setAgeGatePassed(true)} />
        </LocaleProvider>
      </ThemeProvider>
    );
  }

  const isNative = isNativeApp();

  return (
    <QueryClientProvider client={queryClient}>
      <ErrorBoundary>
        <ThemeProvider>
          <LocaleProvider>
            <AuthProvider>
              <UnifiedPrayerProvider>
                <AdConfigProvider>
                  <TooltipProvider>
                    <Toaster />
                    <Sonner />
                    <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
                      <NativeAppProvider>
                        <ScrollToTop />
                        <AnalyticsTracker />
                        <SEOWrapper>
                          <PermissionManager />
                          <AppLayout>
                            <ErrorBoundary>
                              <Suspense fallback={<div className="min-h-screen" />}>
                                <NativePageTransition>
                                  <Routes>
                                    <Route path="/" element={<Index />} />
                                    <Route path="/social-profile/:userId" element={<SocialProfile />} />
                                    <Route path="/reels" element={<VideoReels />} />
                                    <Route path="/create-post" element={<CreatePost />} />
                                    <Route path="/prayer-times" element={<PrayerTimes />} />
                                    <Route path="/qibla" element={<Qibla />} />
                                    <Route path="/quran" element={<Quran />} />
                                    <Route path="/quran/:id" element={<SurahView />} />
                                    <Route path="/tasbeeh" element={<Tasbeeh />} />
                                    <Route path="/duas" element={<Duas />} />
                                    <Route path="/more" element={<More />} />
                                    <Route path="/tracker" element={<PrayerTracker />} />
                                    <Route path="/zakat" element={<ZakatCalculator />} />
                                    <Route path="/stories" element={<Stories />} />
                                    <Route path="/auth" element={<Auth />} />
                                    <Route path="/account" element={<Account />} />
                                    <Route path="/admin" element={<AdminDashboard />} />
                                    <Route path="/install" element={<Install />} />
                                    <Route path="/daily-duas" element={<DailyDuas />} />
                                    <Route path="/mosque-times" element={<MosquePrayerTimes />} />
                                    <Route path="/ramadan-challenge" element={<RamadanChallenge />} />
                                    <Route path="/ramadan-calendar" element={<RamadanCalendar />} />
                                    <Route path="/quran-goal" element={<QuranGoal />} />
                                    <Route path="/dhikr-settings" element={<DhikrSettings />} />
                                    <Route path="/notifications" element={<NotificationSettings />} />
                                    <Route path="/ruqyah" element={<Ruqyah />} />
                                    <Route path="/asma-al-husna" element={<AsmaAlHusna />} />
                                    <Route path="/ramadan-cards" element={<RamadanCards />} />
                                    <Route path="/ramadan-book" element={<RamadanBook />} />
                                    <Route path="/period-tracker" element={<PeriodTracker />} />
                                    <Route path="/profile" element={<Profile />} />
                                    <Route path="/profile/:userId" element={<Profile />} />
                                    <Route path="/messages" element={<Messages />} />
                                    <Route path="/store" element={<Store />} />
                                    <Route path="/rewards" element={<Rewards />} />
                                    <Route path="/points" element={<PointsBalance />} />
                                    <Route path="/ai-assistant" element={<AiAssistant />} />
                                    <Route path="/marketplace" element={<Marketplace />} />
                                    <Route path="/explore" element={<Explore />} />
                                    <Route path="/sohba" element={<Sohba />} />
                                    <Route path="/about" element={<AboutUs />} />
                                    <Route path="/privacy" element={<PrivacyPolicy />} />
                                    <Route path="/contact" element={<ContactUs />} />
                                    <Route path="/donations" element={<Donations />} />
                                    <Route path="/terms" element={<TermsOfService />} />
                                    <Route path="/arabic-academy" element={<Navigate to="/kids-zone" replace />} />
                                    <Route path="/kids-zone" element={<KidsZone />} />
                                    <Route path="/baraka-market" element={<BarakaMarket />} />
                                    <Route path="/tafsir" element={<Tafsir />} />
                                    <Route path="/forty-nawawi" element={<FortyNawawi />} />
                                    <Route path="/delete-data" element={<DataDeletion />} />
                                    <Route path="/content-policy" element={<ContentPolicy />} />
                                    <Route path="/live-streams" element={<LiveStreams />} />
                                    <Route path="*" element={<NotFound />} />
                                  </Routes>
                                </NativePageTransition>
                              </Suspense>
                            </ErrorBoundary>
                          </AppLayout>
                          {/* Web-only overlays */}
                          {!isNative && <CookieConsent />}
                          <GDPRAdConsent />
                          <OfflineNotice />
                          {/* Native-only components */}
                          {isNative && <RateApp />}
                          {isNative && <AppTrackingTransparency />}
                        </SEOWrapper>
                      </NativeAppProvider>
                    </BrowserRouter>
                  </TooltipProvider>
                </AdConfigProvider>
              </UnifiedPrayerProvider>
            </AuthProvider>
          </LocaleProvider>
        </ThemeProvider>
      </ErrorBoundary>
    </QueryClientProvider>
  );
};

export default App;

import { initializeApp, getApps } from 'firebase/app';
import { getAuth, GoogleAuthProvider, signInWithPopup, signInWithRedirect, getRedirectResult, onAuthStateChanged } from 'firebase/auth';

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY || 'AIzaSyARC894IHre42NgUXiLkrVDf9_vApNc9GM',
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN || 'hxhdh-78bec.firebaseapp.com',
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID || 'hxhdh-78bec',
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET || 'hxhdh-78bec.appspot.com',
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID || '388343656632',
};

const app = getApps().length ? getApps()[0] : initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const googleProvider = new GoogleAuthProvider();
googleProvider.addScope('email');
googleProvider.addScope('profile');
googleProvider.setCustomParameters({ prompt: 'select_account' });

export async function signInWithGoogle(): Promise<{ idToken: string; user: any } | null> {
  try {
    const result = await signInWithPopup(auth, googleProvider);
    const idToken = await result.user.getIdToken();
    return { idToken, user: result.user };
  } catch (err: any) {
    if (err.code === 'auth/popup-blocked') {
      // Try redirect
      await signInWithRedirect(auth, googleProvider);
    }
    console.error('Google sign-in error:', err);
    return null;
  }
}

export async function getGoogleRedirectResult() {
  try {
    const result = await getRedirectResult(auth);
    if (result) {
      const idToken = await result.user.getIdToken();
      return { idToken, user: result.user };
    }
    return null;
  } catch (_e) {
    return null;
  }
}

export { onAuthStateChanged };
export default app;

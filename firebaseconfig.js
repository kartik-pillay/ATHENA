// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.17.1/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/9.17.1/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/9.17.1/firebase-firestore.js";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyCVsyW7UMpS34Wu5hn-HpLe71DiIXis05k",
  authDomain: "fir-mood-tracker.firebaseapp.com",
  projectId: "fir-mood-tracker",
  storageBucket: "fir-mood-tracker.firebasestorage.app",
  messagingSenderId: "475637581812",
  appId: "1:475637581812:web:ddd5346ef5766994a8dba1",
  measurementId: "G-YNFPFWNQ58"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const db = getFirestore(app);

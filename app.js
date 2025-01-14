import { auth, db } from "./firebaseconfig.js";
import { 
  createUserWithEmailAndPassword, 
  signInWithEmailAndPassword, 
  onAuthStateChanged,
  signOut 
} from "https://www.gstatic.com/firebasejs/9.17.1/firebase-auth.js";
import { 
  doc, 
  getDoc, 
  setDoc, 
  updateDoc, 
  Timestamp 
} from "https://www.gstatic.com/firebasejs/9.17.1/firebase-firestore.js";

// Handle Signup
// Handle Signup
const signupForm = document.getElementById("signup-form");
if (signupForm) {
  signupForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = document.getElementById("signup-email").value;
    const password = document.getElementById("signup-password").value;

    try {
      await createUserWithEmailAndPassword(auth, email, password);
      alert("Signup successful!");
      window.location.href = "basic.html"; // Redirect to basic.html
    } catch (error) {
      alert("Error signing up: " + error.message);
    }
  });
}

// Handle Login
const loginForm = document.getElementById("login-form");
if (loginForm) {
  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = document.getElementById("login-email").value;
    const password = document.getElementById("login-password").value;

    try {
      await signInWithEmailAndPassword(auth, email, password);
      alert("Login successful!");
      window.location.href = "landing.html"; // Redirect to landing page
    } catch (error) {
      alert("Error logging in: " + error.message);
    }
  });
}

// Handle Mood Prompt and Journal on Landing Page
if (window.location.pathname.endsWith("landing.html")) {
  document.addEventListener("DOMContentLoaded", async () => {
    onAuthStateChanged(auth, async (user) => {
      if (!user) {
        window.location.href = "index.html"; // Redirect to login page if not logged in
        return;
      }

      const userDocRef = doc(db, "users", user.uid);
      const userDoc = await getDoc(userDocRef);
      const today = new Date().toDateString();

      // Initialize Mood Modal and Journal
      const moodModal = document.getElementById("mood-modal");
      const moodButtons = document.querySelectorAll(".mood-btn");
      const journalTextarea = document.getElementById("journal-textarea");
      const saveJournalBtn = document.getElementById("save-journal-btn");

      // Check if mood is already tracked for the day
      if (!userDoc.exists() || userDoc.data().lastUpdated !== today) {
        // Show Mood Modal
        moodModal.classList.remove("hidden");

        moodButtons.forEach((btn) => {
          btn.addEventListener("click", async () => {
            const mood = btn.dataset.mood;
            try {
              await setDoc(userDocRef, {
                mood,
                lastUpdated: today,
                journal: "", // Journal is initially empty
                timestamp: Timestamp.now(),
              });
              alert("Mood saved!");
              moodModal.classList.add("hidden"); // Hide mood modal
            } catch (error) {
              console.error("Error saving mood:", error);
              alert("Failed to save mood. Please try again.");
            }
          });
        });
      }

      // Save Journal
      saveJournalBtn.addEventListener("click", async () => {
        const journalContent = journalTextarea.value.trim();
        if (journalContent === "") {
          alert("Please write something in the journal.");
          return;
        }

        try {
          await updateDoc(userDocRef, { journal: journalContent });
          alert("Journal saved successfully!");
        } catch (error) {
          console.error("Error saving journal:", error);
          alert("Failed to save journal. Please try again.");
        }
      });
    });
  });
}

// Handle Sign Out with Journal Check
const signOutBtn = document.getElementById("signout-btn");
if (signOutBtn) {
  signOutBtn.addEventListener("click", async () => {
    const user = auth.currentUser;
    if (user) {
      const userDocRef = doc(db, "users", user.uid);
      const userDoc = await getDoc(userDocRef);

      if (userDoc.exists() && !userDoc.data().journal) {
        const journalTextarea = document.getElementById("journal-textarea");
        const journalContent = journalTextarea.value.trim();

        if (journalContent === "") {
          alert("Please write your journal for today before signing out.");
          return;
        }

        try {
          await updateDoc(userDocRef, { journal: journalContent });
          alert("Journal saved successfully!");
        } catch (error) {
          console.error("Error saving journal:", error);
          alert("Failed to save journal. Please try again.");
          return;
        }
      }

      try {
        await signOut(auth);
        alert("Signed out successfully!");
        window.location.href = "index.html"; // Redirect to login page
      } catch (error) {
        console.error("Error signing out:", error);
        alert("Error signing out. Please try again.");
      }
    }
  });
}

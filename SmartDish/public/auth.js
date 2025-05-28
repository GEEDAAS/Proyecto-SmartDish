import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-app.js";
import {
  getAuth,
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword
} from "https://www.gstatic.com/firebasejs/10.8.1/firebase-auth.js";

// 🔥 Tu configuración de Firebase
const firebaseConfig = {
    apiKey: "AIzaSyDUjhN2w7R_PFOX5Gm8dKR3OumyIjuL5Ls",
    authDomain: "smartdish-firebase.firebaseapp.com",
    projectId: "smartdish-firebase",
    storageBucket: "smartdish-firebase.firebasestorage.app",
    messagingSenderId: "368626565954",
    appId: "1:368626565954:web:75a1430960caa98f14bedb",
    measurementId: "G-F492ZZGJTJ"
  };

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// === Login ===
const loginBtn = document.getElementById("login");
if (loginBtn) {
  loginBtn.addEventListener("click", () => {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    signInWithEmailAndPassword(auth, email, password)
      .then(() => {
        window.location.href = "index.html";
      })
      .catch((error) => {
        alert("Error al iniciar sesión:\n" + error.message);
      });
  });
}

// === Registro ===
const registrarBtn = document.getElementById("registrar");
if (registrarBtn) {
  registrarBtn.addEventListener("click", () => {
    const email = document.getElementById("registro-email").value;
    const password = document.getElementById("registro-password").value;

    createUserWithEmailAndPassword(auth, email, password)
      .then(() => {
        alert("Registro exitoso. Redirigiendo...");
        window.location.href = "index.html";
      })
      .catch((error) => {
        alert("Error al registrar:\n" + error.message);
      });
  });
}

import { GoogleAuthProvider, signInWithPopup } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-auth.js";

const googleBtn = document.getElementById("login-google");
if (googleBtn) {
  googleBtn.addEventListener("click", () => {
    const provider = new GoogleAuthProvider();
    signInWithPopup(auth, provider)
      .then((result) => {
        window.location.href = "index.html";
      })
      .catch((error) => {
        alert("Error al iniciar sesión con Google:\n" + error.message);
      });
  });
}

import { sendPasswordResetEmail } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-auth.js";

const recuperarBtn = document.getElementById("recuperar-btn");
if (recuperarBtn) {
  recuperarBtn.addEventListener("click", () => {
    const email = document.getElementById("recuperar-email").value;

    if (!email) {
      alert("Por favor, ingresa tu correo.");
      return;
    }

    sendPasswordResetEmail(auth, email)
      .then(() => {
        alert("Enlace de recuperación enviado. Revisa tu correo.");
      })
      .catch((error) => {
        alert("Error al enviar el enlace:\n" + error.message);
      });
  });
}

const togglePassword = document.getElementById('toggle-password');
const passwordInput = document.getElementById('password');

if (togglePassword && passwordInput) {
  togglePassword.addEventListener('click', () => {
    const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordInput.setAttribute('type', type);

    // Cambiar ícono visual
    togglePassword.textContent = type === 'password' ? '👁️' : '🙈';
  });
}
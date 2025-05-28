import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-app.js";
import { getAuth, onAuthStateChanged, signOut } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-auth.js";

// Config de Firebase
const firebaseConfig = {
  apiKey: "AIzaSyDUjhN2w7R_PFOX5Gm8dKR3OumyIjuL5Ls",
  authDomain: "smartdish-firebase.firebaseapp.com",
  projectId: "smartdish-firebase",
  storageBucket: "smartdish-firebase.appspot.com",
  messagingSenderId: "368626565954",
  appId: "1:368626565954:web:75a1430960caa98f14bedb",
  measurementId: "G-F492ZZGJTJ"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// Verificar sesión activa
onAuthStateChanged(auth, (user) => {
  if (!user) {
    window.location.href = "login.html";
  } else {
    console.log("Usuario autenticado:", user.email);
    iniciarApp();
  }
});

// Botón logout
const logoutBtn = document.getElementById('logout');
if (logoutBtn) {
  logoutBtn.addEventListener('click', () => {
    signOut(auth).then(() => {
      window.location.href = "login.html";
    }).catch((error) => {
      alert("Error al cerrar sesión: " + error.message);
    });
  });
}

function iniciarApp() {
  // Broker para ESP32 (datos)
  const clientMosquitto = mqtt.connect('wss://test.mosquitto.org:8081/mqtt');

  // Broker para ESP32-CAM (foto)
  const clientHiveMQ = mqtt.connect('wss://broker.hivemq.com:8884/mqtt');

  const btnDispensar = document.getElementById('btn-dispensar');
  const btnDispensarAgua = document.getElementById('btn-dispensar-agua');
  const comidaEstado = document.getElementById('comida');
  const btnCapturar = document.getElementById('capturar-btn');
  const temp = document.getElementById('temp');
  const hum = document.getElementById('hum');
  const ledDispensando = document.getElementById('led-dispensando');
  const pesoSpan = document.getElementById('peso');
  const btnVerFoto = document.getElementById('ver-foto-btn');
  const btnAnalizarFoto = document.getElementById('analizar-foto-btn');
  const resultadoIA = document.getElementById('resultado-ia');
  const imgResult = document.getElementById('img-result');

  // === CLIENTE MQTT Mosquitto (ESP32) ===
  clientMosquitto.on('connect', () => {
    console.log('✅ Conectado a Mosquitto (ESP32)');
    clientMosquitto.subscribe('smartdish/peso');
    clientMosquitto.subscribe('smartdish/estadoPlato');
    clientMosquitto.subscribe('smartdish/temp_hum');
    clientMosquitto.subscribe('smartdish/led_dispensando');
  });

  clientMosquitto.on('message', (topic, message) => {
    const msg = message.toString();

    if (topic === 'smartdish/peso') {
      pesoSpan.textContent = msg
    }

    if (topic === 'smartdish/estadoPlato') {
      comidaEstado.textContent = msg === '1' ? '🐶 El perro comió' : '🐾 No ha comido';
      comidaEstado.style.color = msg === '1' ? 'green' : 'red';
    }

    if (topic === 'smartdish/temp_hum') {
      const [t, h] = msg.split(',');
      temp.textContent = `${t} °C`;
      hum.textContent = `${h} %`;
    }

    if (topic === 'smartdish/led_dispensando') {
      ledDispensando.textContent = msg === '1' ? 'Encendido' : 'Apagado';
    }
  });

  // === Botón DISPENSAR - publica en Mosquitto ===
  if (btnDispensar) {
    btnDispensar.addEventListener('click', () => {
      clientMosquitto.publish('smartdish/comida', 'dispensar');
      alert('📦 Comando enviado: DISPENSAR');
    });
  }

  if (btnDispensarAgua) {
    btnDispensarAgua.addEventListener('click', () => {
      clientMosquitto.publish('smartdish/agua', 'dispensar_agua');
      alert('💧 Comando enviado: DISPENSAR AGUA');
    });
  }

  // === CLIENTE MQTT HiveMQ (ESP32-CAM) ===
  clientHiveMQ.on('connect', () => {
    console.log('📸 Conectado a HiveMQ (ESP32-CAM)');
  });

  if (btnCapturar) {
    btnCapturar.addEventListener('click', () => {
      if (btnVerFoto) btnVerFoto.style.display = 'none';

      clientHiveMQ.publish('smartdish/camara', 'capturar');
      alert("📸 Comando 'capturar' enviado");

      setTimeout(() => {
        if (btnVerFoto) btnVerFoto.style.display = 'inline-block';
        if (btnAnalizarFoto) btnAnalizarFoto.style.display = 'inline-block';
      }, 2000);
    });
  }

  if (btnAnalizarFoto) {
    btnAnalizarFoto.addEventListener('click', async () => {
      resultadoIA.textContent = 'Analizando...';
      imgResult.style.display = 'none';

      try {
        const response = await fetch('http://localhost:5000/captura_proxy');
        if (!response.ok || !response.headers.get("content-type")?.includes("image")) {
          throw new Error("La cámara no devolvió una imagen válida");
        }

        const blob = await response.blob();

        const formData = new FormData();
        formData.append('imagen', blob, 'captura.jpg');

        const res = await fetch('http://localhost:5000/detectar', {
          method: 'POST',
          body: formData
        });

        if (!res.ok) {
          const text = await res.text();
          console.error("Error HTML del backend:", text);
          throw new Error("El servidor de IA falló");
        }

        const data = await res.json();

        if (data.resultado === 'perro') {
          resultadoIA.textContent = '✅ Se detectó perro o mascota';
          imgResult.src = `http://localhost:5000/resultado/${data.nombre}`;
          imgResult.style.display = 'block';
        } else {
          resultadoIA.textContent = '❌ No se detectó perro';
        }
      } catch (err) {
        console.error("Error al enviar imagen a IA:", err);
        resultadoIA.textContent = 'Error al analizar imagen';
      }
    });
  }

  if (btnVerFoto) {
    btnVerFoto.addEventListener('click', () => {
      window.open('http://10.0.16.40/captura.jpg', '_blank');
      btnVerFoto.style.display = 'none';
    });
  }
}

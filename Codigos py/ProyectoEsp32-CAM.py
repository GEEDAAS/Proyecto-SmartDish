import camera
import os
import socket
import time
from umqttsimple import MQTTClient
import network

# MQTT Config
MQTT_BROKER = "broker.hivemq.com"
MQTT_TOPIC = b"smartdish/camara"
CLIENT_ID = "smartdish_esp32"

# ==== Iniciar cámara ====
def iniciar_camara():
    try:
        camera.init(0, format=camera.JPEG)
        camera.framesize(camera.FRAME_QVGA)  # Resolución 320x240
        print("Cámara iniciada correctamente.")
    except Exception as e:
        print("Error al iniciar cámara:", e)

# ==== Capturar foto ====
def capturar_foto():
    try:
        buf = camera.capture()
        with open("captura.jpg", "wb") as f:
            f.write(buf)
        print("📸 Foto capturada y guardada como captura.jpg")
    except Exception as e:
        print("Error al capturar foto:", e)

# ==== Servidor web para servir la imagen ====
def iniciar_servidor():
    try:
        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
        s = socket.socket()
        s.bind(addr)
        s.listen(1)
        print("🌐 Servidor web iniciado en puerto 80...")

        while True:
            cl, addr = s.accept()
            print('Cliente conectado desde', addr)
            request = cl.recv(1024)

            if b"/captura.jpg" in request:
                try:
                    with open("captura.jpg", "rb") as f:
                        img = f.read()
                    cl.send(b"HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\n\r\n")
                    cl.send(img)
                except:
                    cl.send(b"HTTP/1.1 404 Not Found\r\n\r\nImagen no disponible.")
            else:
                cl.send(b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
                cl.send(b"<h1>ESP32-CAM activa</h1><p>Usa /captura.jpg para ver la imagen capturada.</p>")

            cl.close()
    except Exception as e:
        print("Error en servidor web:", e)

# ==== Callback MQTT ====
def callback(topic, msg):
    print("📡 Mensaje MQTT recibido:", topic, msg)
    if msg == b'capturar':
        capturar_foto()

# ==== Función principal ====
def main():
    iniciar_camara()

    # MQTT
    try:
        print("Conectando a MQTT...")
        client = MQTTClient(CLIENT_ID, MQTT_BROKER)
        client.set_callback(callback)
        client.connect()
        client.subscribe(MQTT_TOPIC)
        print("✅ MQTT conectado y suscrito al tópico:", MQTT_TOPIC.decode())
    except Exception as e:
        print("❌ Error al conectar a MQTT:", e)
        return

    # Iniciar servidor en hilo aparte
    try:
        import _thread
        _thread.start_new_thread(iniciar_servidor, ())
    except Exception as e:
        print("⚠ Error iniciando el servidor en hilo:", e)

    # Loop principal
    while True:
        try:
            client.check_msg()
        except Exception as e:
            print("⚠ Error revisando mensajes MQTT:", e)
        time.sleep(1)

main()
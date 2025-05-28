import network
import time

SSID = 'Lab-Base-Datos-TecNM-D'
PASSWORD = 'Bas3deDat0sD11'   

def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    print("Conectando al WiFi...")
    while not wlan.isconnected():
        time.sleep(1)
    print("Conectado:", wlan.ifconfig())

conectar_wifi()

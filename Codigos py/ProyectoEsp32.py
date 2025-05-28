import network
import machine
import time
from umqtt.simple import MQTTClient
import dht
from hx711 import HX711

# ==== CONFIGURACIÓN GENERAL ====

# WiFi
SSID = 'Lab-Base-Datos-TecNM-D'
PASSWORD = 'Bas3deDat0sD11'

# MQTT
MQTT_BROKER = 'test.mosquitto.org'
MQTT_TOPIC_SUB = b'smartdish/comida'
MQTT_TOPIC_AGUA = b'smartdish/agua'          # Nuevo tópico para dispensar agua
MQTT_TOPIC_PUB = b'smartdish/estadoPlato'    # estado: ¿el perro comió?
MQTT_TOPIC_TEMPHUM = b'smartdish/temp_hum'
MQTT_TOPIC_LED = b'smartdish/led_dispensando'
MQTT_TOPIC_PESO = b'smartdish/peso'
CLIENT_ID = 'smartdish_esp32'

# Pines
servo = machine.PWM(machine.Pin(14), freq=50)
ldr = machine.ADC(machine.Pin(34))
ldr.atten(machine.ADC.ATTN_11DB)

dht_sensor = dht.DHT11(machine.Pin(27))

led_rojo = machine.Pin(25, machine.Pin.OUT)
led_verde = machine.Pin(26, machine.Pin.OUT)
led_azul = machine.Pin(33, machine.Pin.OUT)

bomba_agua = machine.Pin(18, machine.Pin.OUT)  # Pin para controlar bomba de agua
bomba_agua.off()  # Apagar bomba inicialmente

# === CONFIGURACIÓN DEL SENSOR DE PESO ===
hx = HX711(d_out=32, pd_sck=15, channel=HX711.CHANNEL_A_128)
offset = hx.read()
escala = 1000  # Ajustar según calibración real

# ==== FUNCIONES AUXILIARES ====

def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    print("Conectando a WiFi...")
    while not wlan.isconnected():
        time.sleep(1)
    print("WiFi conectado:", wlan.ifconfig())

def mover_servo(pos):
    duty = int((pos / 180) * 102 + 26)
    servo.duty(duty)

def leer_ldr():
    valor = ldr.read()
    print("Valor LDR:", valor)
    # Determinar si el perro comió (menos luz = comió)
    if valor < 2500:
        print("🐾 El perro comió")
        return b'1'
    else:
        print("🐾 El perro NO ha comido")
        return b'0'

def leer_dht11():
    try:
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()
        print(f"Temperatura: {temp}°C, Humedad: {hum}%")
        return f"{temp},{hum}".encode()
    except Exception as e:
        print("Error al leer DHT11:", e)
        return b'0,0'

def leer_peso():
    try:
        lectura = hx.read()
        peso = (lectura - offset) / escala
        print("Peso estimado:", peso, "g")

        # Determinar si HAY comida (peso suficiente)
        if peso >= 10:  # Puedes ajustar este umbral
            led_verde.on()
            led_rojo.off()
        else:
            led_verde.off()
            led_rojo.on()

        return str(round(peso, 2)).encode()
    except Exception as e:
        print("Error leyendo peso:", e)
        led_verde.off()
        led_rojo.on()
        return b'0.00'

def dispensar_agua(segundos=5):
    print(f"Dispensando agua por {segundos} segundos...")
    bomba_agua.on()  # Activar bomba
    time.sleep(segundos)
    bomba_agua.off()  # Apagar bomba
    print("Bomba apagada.")

def callback(topic, msg):
    print(f"Mensaje recibido: {topic} - {msg}")
    if msg == b'dispensar':
        led_azul.on()
        client.publish(MQTT_TOPIC_LED, b'1')
        time.sleep(0.5)
        mover_servo(150)
        time.sleep(1)
        mover_servo(0)
        led_azul.off()
        client.publish(MQTT_TOPIC_LED, b'0')
    elif msg == b'dispensar_agua':
        dispensar_agua(5)  # Dispensar agua por 5 segundos

# ==== PROGRAMA PRINCIPAL ====

try:
    conectar_wifi()
    mover_servo(0)
    bomba_agua.off()  # Apagar bomba por si acaso
    time.sleep(1)

    client = MQTTClient(CLIENT_ID, MQTT_BROKER)
    client.set_callback(callback)
    client.connect()
    client.subscribe(MQTT_TOPIC_SUB)
    client.subscribe(MQTT_TOPIC_AGUA)   # Suscribirse al tópico de agua
    print("Conectado a MQTT. Esperando comandos...")

    ultimo_envio = time.time()

    while True:
        client.check_msg()

        estado = leer_ldr()  # 🐶 ¿El perro comió?
        client.publish(MQTT_TOPIC_PUB, estado)

        peso_actual = leer_peso()
        client.publish(MQTT_TOPIC_PESO, peso_actual)

        if time.time() - ultimo_envio > 2:
            client.publish(MQTT_TOPIC_TEMPHUM, leer_dht11())
            ultimo_envio = time.time()

        time.sleep(5)

except KeyboardInterrupt:
    print("Programa interrumpido manualmente")
    client.disconnect()
    servo.deinit()
    bomba_agua.off()

except Exception as e:
    print("Error general:", e)
    client.disconnect()
    servo.deinit()
    bomba_agua.off()

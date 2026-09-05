from machine import Pin
import network
import time

TRIGGER_PIN = Pin(2, Pin.OUT)
ECHO_PIN = Pin(18, Pin.IN)
BOTON_SOS = Pin(4, Pin.IN, Pin.PULL_UP)

GND_SIMULADO = Pin(19, Pin.OUT)
GND_SIMULADO.off()

def conectar_wifi():
    print("START NET...")
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect("Wokwi-GUEST", "")
    
    intentos = 0
    while not wlan.isconnected() and intentos < 10:
        print("Connecting...")
        time.sleep(1)
        intentos += 1
        
    if wlan.isconnected():
        print("ONLINE!")
        print("IP:", wlan.ifconfig())
    else:
        print("ERROR")

def medir_distancia():
    TRIGGER_PIN.off()
    time.sleep_us(2)
    TRIGGER_PIN.on()
    time.sleep_us(10)
    TRIGGER_PIN.off()
    
    inicio_timeout = time.ticks_ms()
    while ECHO_PIN.value() == 0:
        inicio_pulso = time.ticks_us()
        if time.ticks_diff(time.ticks_ms(), inicio_timeout) > 100:
            return 0
            
    while ECHO_PIN.value() == 1:
        fin_pulso = time.ticks_us()
        
    duracion = time.ticks_diff(fin_pulso, inicio_pulso)
    distancia_cm = (duracion * 0.0343) / 2
    return distancia_cm

def disparar_alerta_sos():
    print("\n==========================================")
    print("🚨 EMERGENCY: SOS BUTTON PRESSED!")
    print("==========================================")
    print("1. Capturing environment image via camera...")
    print("2. Gathering GPS telemetry (Lat: -32.95, Lon: -68.83)...")
    print("3. Building Multimodal Payload for GenAI Cloud...")
    
    payload = {
        "device_id": "GUARDIAN-IA-001",
        "timestamp": time.time(),
        "alert_type": "USER_SOS",
        "gps": {"lat": -32.95, "lon": -68.83},
        "ai_prompt": "Describe immediate hazards in the scene."
    }
    
    print("4. Payload ready for Gemini 1.5 Flash API.")
    print("5. Awaiting AI response speech synthesis...")
    print("==========================================\n")
    time.sleep(2)

print("SYSTEM START")
conectar_wifi()

while True:
    if BOTON_SOS.value() == 0:
        disparar_alerta_sos()
        
    distancia = medir_distancia()
    
    if 0 < distancia < 50:
        print("ALERT! Distance:", distancia, "cm")
    elif distancia >= 50:
        print("CLEAR! Distance:", distancia, "cm")
        
    time.sleep(0.5)

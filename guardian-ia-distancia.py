from machine import Pin
import network
import time

TRIGGER_PIN = Pin(2, Pin.OUT)
ECHO_PIN = Pin(18, Pin.IN)

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

print("SYSTEM START")
conectar_wifi()

while True:
    distancia = medir_distancia()
    
    if 0 < distancia < 50:
        print("ALERT! Distance:", distancia, "cm")
    elif distancia >= 50:
        print("CLEAR! Distance:", distancia, "cm")
        
    time.sleep(0.5)

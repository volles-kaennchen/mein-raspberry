import time
import board
import busio
import usb_hid

from configurations import configurations_map
from empty_classes import EmptyConfiguration, EmptyMacro

from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_hid.keyboard import Keyboard
import adafruit_dotstar
from digitalio import DigitalInOut, Direction

print("--- Macropad Bootvorgang startet ---")

# CS-Pin auf Low setzen, um Level Shifter für LEDs zu aktivieren
cs = DigitalInOut(board.GP17)
cs.direction = Direction.OUTPUT
cs.value = 0

# Setup für die 16 APA102 LEDs
num_pixels = 16
pixels = adafruit_dotstar.DotStar(board.GP18, board.GP19, num_pixels, brightness=0.2, auto_write=False)
print("[OK] LEDs initialisiert (16 Pixels)")

# Setup für I2C IO Expander (Tasten-Auslesung)
try:
    i2c = busio.I2C(board.GP5, board.GP4)
    device = I2CDevice(i2c, 0x20)
    print("[OK] I2C Expander auf Adresse 0x20 gefunden")
except Exception as e:
    print(f"[ERROR] I2C Verbindung fehlgeschlagen: {e}")

keyboard = Keyboard(usb_hid.devices)

class ButtonMode:
    CONFIGURATION_CHOSER = 0
    MACRO_CHOSER = 1

# SEQUENTIELLE AUSLESE MIT BIT-FIX
def read_button_states():
    pressed = [0] * 16
    with device:
        device.write(bytes([0x0]))
        result = bytearray(2)
        device.readinto(result)
        
        b = (result[0] & 0xFF) | ((result[1] & 0xFF) << 8)

        for i in range(16):
            if not (1 << i) & b:
                pressed[i] = 1
    return pressed

held = [0] * 16
last_state = [0] * 16
debounce_time = [0.0] * 16
DEBOUNCE_DELAY = 0.020  

button_mode = ButtonMode.CONFIGURATION_CHOSER
last_button_mode = -1
chosen_configuration = 8  

print("\n[READY] System bereit. Modus: PROFILAUSWAHL. Warte auf Taste 8...\n")

def updateLeds():
    global last_button_mode
    
    if button_mode == last_button_mode:
        return
        
    last_button_mode = button_mode
    
    if button_mode == ButtonMode.CONFIGURATION_CHOSER:
        print("[LED] Wechsle zu Menü-Farben")
        for i in range(16):
            if i < len(configurations_map):
                pixels[i] = configurations_map[i].getColor()
            else:
                pixels[i] = (0, 0, 0)
        pixels.show()
        
    elif button_mode == ButtonMode.MACRO_CHOSER:
        print(f"[LED] Wechsle zu Profil-Farben für Index {chosen_configuration}")
        config = configurations_map[chosen_configuration]
        
        if hasattr(config, "getButtonColors"):
            button_colors = config.getButtonColors()
            for i in range(16):
                if i in button_colors:
                    pixels[i] = button_colors[i]
                else:
                    pixels[i] = (0, 0, 0)
        else:
            for i in range(16):
                if i < min(len(config.getMacros()), 15) and not issubclass(config.getMacros()[i], EmptyMacro):
                    pixels[i] = config.getColor()
                else: 
                    pixels[i] = (0, 0, 0)

        pixels[8] = (0, 255, 0)    # Grün für Aktiv / Start
        pixels[12] = (255, 0, 0)   # Rot für Zurück / Aus ('C')
        pixels.show()
        
def readButton():
    global button_mode, chosen_configuration, held, last_state, debounce_time

    current_time = time.monotonic()
    raw_pressed = read_button_states()

    for i in range(16):
        if raw_pressed[i] != last_state[i]:
            debounce_time[i] = current_time
            last_state[i] = raw_pressed[i]

        if (current_time - debounce_time[i]) > DEBOUNCE_DELAY:
            
            # --- TASTE IST GEDRÜCKT ---
            if raw_pressed[i]: 
                
                # MODUS: PROFIL AUSWÄHLEN (Menü)
                if button_mode == ButtonMode.CONFIGURATION_CHOSER:
                    if i == 8: 
                        if i < len(configurations_map) and not issubclass(configurations_map[i], EmptyConfiguration):
                            chosen_configuration = i
                            button_mode = ButtonMode.MACRO_CHOSER
                            print(f"\n[MODUS] >>> GAMING AKTIVIERT <<< Profil: {configurations_map[i].getName()}")
                            for k in range(16): held[k] = 0
                            held[i] = 1
                
                # MODUS: GAMING PAD AKTIV
                elif button_mode == ButtonMode.MACRO_CHOSER:
                    if i == 12 and not held[i]: 
                        held[i] = 1
                        button_mode = ButtonMode.CONFIGURATION_CHOSER
                        keyboard.release_all() 
                        print("\n[MODUS] <<< GAMING BEENDET >>> Zurück im Menü. Alle Tasten losgelassen.")
                        for k in range(16): held[k] = 0
                        
                    elif not held[i] and i != 12:
                        held[i] = 1 
                        if chosen_configuration < len(configurations_map):
                            macros = configurations_map[chosen_configuration].getMacros()
                            if i < len(macros) and not issubclass(macros[i], EmptyMacro):
                                macro_name = macros[i].getMacroName() if hasattr(macros[i], "getMacroName") else "Unbekannt"
                                print(f"[PRESS] Taste {i} gedrückt -> Makro: {macro_name}")
                                macros[i].getMacro()

            # --- TASTE WIRD LOSGELASSEN ---
            else:
                if held[i]:
                    held[i] = 0 
                    if button_mode == ButtonMode.MACRO_CHOSER and chosen_configuration < len(configurations_map):
                        macros = configurations_map[chosen_configuration].getMacros()
                        if i < len(macros):
                            macro = macros[i]
                            # --- HIER IST DER GEÄNDERTE BEREICH ---
                            if hasattr(macro, "getReleaseCode"):
                                release_code = macro.getReleaseCode()
                                if release_code is not None:  # Verhindert Fehlzündungen bei .send()-Makros
                                    macro_name = macro.getMacroName() if hasattr(macro, "getMacroName") else "Unbekannt"
                                    print(f"[RELEASE] Taste {i} losgelassen -> Release Code für: {macro_name}")
                                    keyboard.release(release_code)
                            # --------------------------------------

while True:
    updateLeds()
    readButton()

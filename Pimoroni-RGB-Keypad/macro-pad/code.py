import time
import board
import busio
import usb_hid
import adafruit_dotstar
from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from digitalio import DigitalInOut, Direction

print("--- Macropad Start ---")

# ------------------------------------------------------------------
# Farben (R, G, B)
# ------------------------------------------------------------------
ROT = (255, 41, 48)
ORANGE = (255, 141, 41)
GELB = (255, 248, 41)
GRUEN = (155, 255, 41)
MINT = (41, 255, 141)
HELLBLAU = (41, 155, 255)
LILA = (141, 41, 255)
ROSA = (255, 41, 155)
AUS = (0, 0, 0)

# ------------------------------------------------------------------
# Tastenbelegung: Index 0-15 = Taste 0-F
# Eintrag: (Name, (Tastenkombination), Farbe)  |  None = nicht belegt
# ------------------------------------------------------------------
POWER_KEY = 15  # Taste F = Ein/Aus

MACROS = [
    ("ESC",            (Keycode.ESCAPE,),                                  ROT),       # 0
    ("WIN+TAB",        (Keycode.GUI, Keycode.TAB),                         HELLBLAU),  # 1
    ("STRG+W",         (Keycode.CONTROL, Keycode.W),                       ROT),       # 2
    ("WIN+SHIFT+S",    (Keycode.GUI, Keycode.SHIFT, Keycode.S),            ORANGE),    # 3
    ("STRG+S",         (Keycode.CONTROL, Keycode.S),                       GRUEN),     # 4
    ("STRG+F",         (Keycode.CONTROL, Keycode.F),                       ORANGE),    # 5
    ("STRG+Z",         (Keycode.CONTROL, Keycode.Z),                       LILA),      # 6
    ("STRG+Y",         (Keycode.CONTROL, Keycode.Y),                       LILA),      # 7
    ("TAB",            (Keycode.TAB,),                                     HELLBLAU),  # 8
    ("STRG+A",         (Keycode.CONTROL, Keycode.A),                       GRUEN),     # 9
    ("STRG+SHIFT+C",   (Keycode.CONTROL, Keycode.SHIFT, Keycode.C),        ROSA),      # A
    ("STRG+SHIFT+V",   (Keycode.CONTROL, Keycode.SHIFT, Keycode.V),        ROSA),      # B
    ("STRG+C",         (Keycode.CONTROL, Keycode.C),                       GELB),      # C
    ("STRG+V",         (Keycode.CONTROL, Keycode.V),                       GELB),      # D
    None,                                                                              # E
    None,                                                                              # F (Power, wird separat behandelt)
]

KEY_NAMES = "0123456789ABCDEF"
DEBOUNCE = 0.03  # Sekunden Wartezeit gegen Prellen

# ------------------------------------------------------------------
# Hardware
# ------------------------------------------------------------------
# CS-Pin auf Low: aktiviert den Level Shifter der LEDs
cs = DigitalInOut(board.GP17)
cs.direction = Direction.OUTPUT
cs.value = 0

pixels = adafruit_dotstar.DotStar(board.GP18, board.GP19, 16, brightness=0.2, auto_write=False)
print("[OK] LEDs bereit")

try:
    i2c = busio.I2C(board.GP5, board.GP4)
    device = I2CDevice(i2c, 0x20)
    print("[OK] I2C Expander 0x20 gefunden")
except Exception as e:
    print("[FEHLER] I2C:", e)
    raise

keyboard = Keyboard(usb_hid.devices)


def read_button_states():
    """Liefert Liste mit 16 Werten: 1 = Taste gedrueckt, 0 = nicht gedrueckt."""
    result = bytearray(2)
    with device:
        device.write(bytes([0x0]))
        device.readinto(result)
    bits = result[0] | (result[1] << 8)
    # Im Expander bedeutet Bit = 0 "gedrueckt"
    return [0 if (bits >> i) & 1 else 1 for i in range(16)]


macros_on = False  # Startzustand: AUS, nur Taste F leuchtet


def update_leds():
    for i in range(16):
        if i == POWER_KEY:
            pixels[i] = MINT if macros_on else ROT
        elif macros_on and MACROS[i] is not None:
            pixels[i] = MACROS[i][2]
        else:
            pixels[i] = AUS
    pixels.show()


def handle_key(i):
    """Wird genau einmal pro Tastendruck aufgerufen."""
    global macros_on
    print("[TASTE]", KEY_NAMES[i], "gedrueckt")

    if i == POWER_KEY:
        macros_on = not macros_on
        print("[POWER] Makros sind jetzt", "EIN" if macros_on else "AUS")
        update_leds()
        return

    if not macros_on:
        print("[IGNORIERT] Makros sind AUS")
        return

    macro = MACROS[i]
    if macro is None:
        print("[IGNORIERT] Taste", KEY_NAMES[i], "ist nicht belegt")
        return

    name, keys, _ = macro
    print("[MAKRO] Sende:", name)
    keyboard.send(*keys)  # drueckt alle Tasten und laesst sie sofort wieder los


# ------------------------------------------------------------------
# Hauptschleife
# ------------------------------------------------------------------
update_leds()
print("[BEREIT] Makros AUS. Taste F schaltet Makros ein/aus.")

while True:
    pressed = read_button_states()
    if 1 in pressed:
        key = pressed.index(1)       # nur die erste gedrueckte Taste beachten
        time.sleep(DEBOUNCE)         # kurz warten (Entprellen)
        if read_button_states()[key]:  # noch gedrueckt? Dann ist es ein echter Druck
            handle_key(key)
            while 1 in read_button_states():  # warten, bis alle Tasten losgelassen sind
                time.sleep(0.01)
            time.sleep(DEBOUNCE)
    time.sleep(0.01)

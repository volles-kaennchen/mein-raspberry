## Hardware: Pimoroni RGB Keypad
https://shop.pimoroni.com/en-eu/products/pico-rgb-keypad-base?variant=32369517166675

| Merkmal | Spezifikation |
| :--- | :--- |
| **Produkt** | Pimoroni RGB Keypad (Pico RGB Keypad Base) |
| **Mikrocontroller** | Kein eigener (nutzt den Raspberry Pi Pico / Pico W) |
| **Kompatible Boards** | Raspberry Pi Pico, Pico W |
| **Tasten** | 16 mechanische Tasten (4×4 Matrix) |
| **Switch-Typ** | Hot-Swap (MX-kompatibel) |
| **RGB-Beleuchtung** | 16 individuell adressierbare APA102 RGB-LEDs |
| **LED-Controller** | IS31FL3731 (LED-Matrix-Treiber) |
| **Schnittstelle** | I²C (für LED-Steuerung) + GPIO für Tastenmatrix |
| **Stromversorgung** | Über den Pico (USB / VSYS) |
| **Betriebsspannung** | 3,3 V Logik |
| **Erweiterung** | Optionales Acryl-Case / Stackable Base |
| **Firmware-Support** | MicroPython / CircuitPython / C/C++ SDK |
| **Abmessungen** | ca. 5 × 5 cm |

# Allgemeine Info
## Initialisierung

### Hardware, Helligkeit und erster Refresh

```
import picokeypad
keypad = picokeypad.PicoKeypad()
keypad.set_brightness(1.0)
keypad.update()
```

## LED

### Der zentrale Befehl für alles visuelle

	index = 0–15
	r,g,b = 0x00 – 0xFF

```
keypad.illuminate(index, r, g, b)
```
### LEDs anzeigen

```
keypad.update()
```

```
keypad.illuminate(index, r, g, b)
keypad.update()
```

## Einzelne Farben definieren

```
import picokeypad
keypad = picokeypad.PicoKeypad()
keypad.set_brightness(1.0)
keypad.update()
```

## Eingabe speichern

```
sequence = []
sequence.append(index)
```

## Tasteneingabe

	genauer Bitwert (1, 2, 4, 8 … 32768)

```
button_states = keypad.get_button_states()
```

## Sequenz abspielen

```
for step in sequence:
    keypad.illuminate(step, *colors[step])
    keypad.update()
    sleep(0.2)
    
    keypad.illuminate(step, 0, 0, 0)
    keypad.update()
```

### Initialisierung der Tasten
```
NUM_PADS = keypad.get_num_pads()
```

```
def get_index(button_states):
    if button_states == 0:
        return None
    return int(math.log2(button_states))
```

## Playback

```
def play_sequence():
    for step in sequence:
        show(step)
        sleep(0.2)
        clear(step)
        sleep(0.1)
```

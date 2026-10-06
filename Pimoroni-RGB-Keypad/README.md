## Hardware: Raspberry Pi Pico
https://www.berrybase.de/en/raspberry-pi-pico-w-rp2040-wlan-microcontroller-board

| Merkmal | Spezifikation |
| :--- | :--- |
| **Mikrocontroller** | RP2040 |
| **CPU** | Dual-Core ARM Cortex-M0+ |
| **Taktfrequenz** | bis 133 MHz |
| **SRAM** | 264 KB |
| **Flash-Speicher** | 2 MB QSPI Flash |
| **WLAN** | 2,4 GHz IEEE 802.11n *(nur beim Pico W)* |
| **Bluetooth** | Bluetooth 5.2 *(nur beim Pico W)* |
| **GPIOs** | 26 nutzbare GPIO-Pins |
| **ADC** | 3 externe 12-Bit-ADC-Eingänge |
| **PWM** | 16 Kanäle |
| **Schnittstellen** | 2× UART, 2× SPI, 2× I²C |
| **USB** | USB 1.1 Host/Device |
| **PIO** | 8 State Machines (2 PIO-Blöcke) |
| **Betriebsspannung** | 1,8–5,5 V Eingang (VSYS) |
| **Logikpegel** | 3,3 V |
| **Abmessungen** | 51 × 21 mm |
| **Temperaturbereich** | −20 °C bis +70 °C |

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

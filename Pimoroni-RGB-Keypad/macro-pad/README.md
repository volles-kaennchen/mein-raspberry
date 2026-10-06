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

---
### Die richtigen Dateien auf den Pico laden

## Erstes Setup 

https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/circuitpython

CircuitPython 10.2.1: https://circuitpython.org/board/raspberry_pi_pico/
Dateien herunterladen
BOOTSEL Taste am Pico gedrückt halten und Pico mit PC verbinden
Wenn sich der Dateimanager öffnet, die UF2 auf das Laufwerk kopieren
-> Interface schließt sich, wenn Installation erfolgreich

Github: https://github.com/adafruit/Adafruit_CircuitPython_Bundle oder Bundle Version 10.x: https://circuitpython.org/libraries 

1. Dateien herunterladen und entpacken
2. Dateien in Thonny auf den Pico in das Verzeichnis ***lib** kopieren:
	adafruit_hid
	adafruit_bus_device
	adafruit_dotstar 

---
### Ordnerstruktur CIRCUITPY 
```
lib/
	adafruit_hid/         
	adafruit_bus_device/   
	adafruit_dotstar.py    
code.py       
```

### 4x4 Matrix LED 
#### Farbauswahl (Beispiel)
```
#FF299B | RGB (255, 41, 155) - Rosa 
#FF8D29 | RGB (255, 141, 41) - Orange 
#29FF8D | RGB (41, 255, 141) - Mint 
#299BFF | RGB (41, 155, 255) - Hellblau 
#8D29FF | RGB (141, 41, 255) - Lila 
#9BFF29 | RGB (155, 255, 41) - Grün 
#FFF829 | RGB (255, 248, 41) - Gelb 
#FF2930 | RGB (255, 41, 48)  - Rot 
```
#### Tastenvergabe (Beispiel)
```txt
- ESC (Abbrechen / Schließen von Dialogen)
- WIN + TAB (Öffnet die Windows-Taskansicht)
- STRG + W (Schließt das aktuelle Fenster oder den aktuellen Browser-Tab)
- WIN + SHIFT + S (Öffnet das Snipping Tool zum Erstellen von Bildschirmfotos)
- STRG + S (Speichert das aktuelle Dokument oder die Datei)
- STRG + F (Öffnet die Suchfunktion (Finden) im aktiven Programm)
- STRG + Z (Macht die letzte Aktion rückgängig)
- STRG + Y (Wiederholt die zuvor rückgängig gemachte Aktion)
- TAB (Wechselt zum nächsten Eingabefeld oder Element)
- STRG + A (Markiert den gesamten Inhalt)
- STRG + SHIFT + C (Code Kopieren)
- STRG + SHIFT + V (Code Einfügen)
- STRG + C (Kopieren)
- STRG + V (Einfügen)
- EIN/AUS – (Funktion zum Ein/Ausschalten)
```

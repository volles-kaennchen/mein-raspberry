---
author: volles-kaennchen
created: 08-06-2026 20:56:25
updated: 08-06-2026 20:56:25
topic: RSPB-Baukasten
tags:
  - pipico
  - raspberry
  - pimoroni
  - macropad
  - rgbkeypad
---

# 📝 Pi Pico 2040

> [!abstract] Spezifikationen Hardware
> einfügen

# 📝 Pimoroni RGB Keypad

> [!abstract] Spezifikationen Hardware
> 16 x APA102 addressable RGB LEDs

---
## 🛠️ Die richtigen Dateien auf den Pico laden

### Erstes Setup 

https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/circuitpython

CircuitPython 10.2.1: https://circuitpython.org/board/raspberry_pi_pico/
	Dateien herunterladen
	BOOTSEL Taste am Pico gedrückt halten und Pico mit PC verbinden
	Wenn sich der Dateimanager öffnet, die UF2 auf das Laufwerk kopieren
	Interface schließt sich, wenn Installation erfolgreich

A: Github: https://github.com/adafruit/Adafruit_CircuitPython_Bundle 
B: Bundle Version 10.x: https://circuitpython.org/libraries 

1. Dateien herunterladen und entpacken
2. Dateien in Thonny auf den Pico in das Verzeichnis ***lib** kopieren:
	adafruit_hid
	adafruit_bus_device
	adafruit_dotstar 

(Dazu vorher den Ordner ***lib*** öffnen – entweder per Doppelklick oder über die Shell mit cd.)

---
## 🛠️ Ordnerstruktur 

### CIRCUITPY (Laufwerk)
```
lib/
	adafruit_hid/         
	adafruit_bus_device/   
	adafruit_dotstar.py    
code.py (Hauptprogramm)       
configurations.py  (Tastenbelegung und Farben)  
abstract_classes.py (Hilfsfunktionen für die Makros)
empty_classes.py (Vorgabe für die Makros)
```

---
## 🛠️ Main Datei

### Datei: code.py
```
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

  

# CS-Pin auf Low setzen, um Level Shifter für LEDs zu aktivieren

cs = DigitalInOut(board.GP17)

cs.direction = Direction.OUTPUT

cs.value = 0

  

# Setup für die 16 APA102 LEDs

num_pixels = 16

pixels = adafruit_dotstar.DotStar(board.GP18, board.GP19, num_pixels, brightness=0.2, auto_write=False)

  

# Setup für I2C IO Expander (Tasten-Auslesung)

i2c = busio.I2C(board.GP5, board.GP4)

device = I2CDevice(i2c, 0x20)

  

keyboard = Keyboard(usb_hid.devices)

  

class ButtonMode:

    CONFIGURATION_CHOSER = 0

    MACRO_CHOSER = 1

  

# Originale Auslese-Funktion von dottxado

def read_button_states(x, y):

    pressed = [0] * 16

    with device:

        device.write(bytes([0x0]))

        result = bytearray(2)

        device.readinto(result)

        b = result[0] | result[1] << 8

  

        for i in range(x, y):

            if not (1 << i) & b:

                pressed[i] = 1

            else:

                pressed[i] = 0

    return pressed

  

held = [0] * 16

button_mode = ButtonMode.CONFIGURATION_CHOSER

last_button_mode = ''

chosen_configuration = 0

  

# LED-Manager erweitert um deine Wunsch-Einzelfarben

def updateLeds():

    global last_button_mode

    # Modus 1: Profilauswahl beim Start

    if button_mode == ButtonMode.CONFIGURATION_CHOSER and last_button_mode != ButtonMode.CONFIGURATION_CHOSER:

        last_button_mode = ButtonMode.CONFIGURATION_CHOSER

        for i in range(16):

            if i < len(configurations_map):

                pixels[i] = configurations_map[i].getColor()

            else:

                pixels[i] = (0, 0, 0)

        pixels.show()

    # Modus 2: Makro-Modus (Dein Gaming Pad ist aktiv)

    elif button_mode == ButtonMode.MACRO_CHOSER and last_button_mode != ButtonMode.MACRO_CHOSER:

        last_button_mode = ButtonMode.MACRO_CHOSER

        config = configurations_map[chosen_configuration]

        # Wenn das Profil Einzelfarben hat (getButtonColors), lade diese!

        if hasattr(config, "getButtonColors"):

            button_colors = config.getButtonColors()

            for i in range(16):

                if i in button_colors:

                    pixels[i] = button_colors[i]

                else:

                    pixels[i] = (0, 0, 0)

        else:

            # Fallback auf die globale Profilfarbe

            for i in range(16):

                if i < min(len(config.getMacros()), 15) and not issubclass(config.getMacros()[i], EmptyMacro):

                    pixels[i] = config.getColor()

                else:

                    pixels[i] = (0, 0, 0)

  

        # Taste 15 bleibt die weisse Menütaste zum Zurückspringen

        pixels[15] = (255, 255, 255)

        pixels.show()

# Tasten-Abfrage mit integrierter Press & Release Logik für Windows-Gaming

def readButton(delay):

    global button_mode

    global chosen_configuration

    global configurations_map

    global held

  

    pressed = read_button_states(0, 16)

    for i in range(16):

        if pressed[i]:

            # --- MODUS: PROFIL AUSWÄHLEN ---

            if button_mode == ButtonMode.CONFIGURATION_CHOSER:

                if i < len(configurations_map) and not issubclass(configurations_map[i], EmptyConfiguration):

                    chosen_configuration = i

                    button_mode = ButtonMode.MACRO_CHOSER

                    time.sleep(delay)

            # --- MODUS: REINES GAMING / MAKROS ---

            elif button_mode == ButtonMode.MACRO_CHOSER:

                if not held[i]:

                    held[i] = 1  # Flanke merken (Taste ist jetzt gedrückt)

                    if chosen_configuration < len(configurations_map):

                        macros = configurations_map[chosen_configuration].getMacros()

                        if i < len(macros) and not issubclass(macros[i], EmptyMacro):

                            # .getMacro() feuert .send() oder .press()

                            macros[i].getMacro()

                        else:

                            configurations_map[chosen_configuration].nothing()

  

                # Taste 15 bringt uns zurück ins Menü

                if i == 15:

                    button_mode = ButtonMode.CONFIGURATION_CHOSER

                    time.sleep(delay)

        else:

            # --- REACTION ON RELEASE (Taste wird losgelassen) ---

            if button_mode == ButtonMode.MACRO_CHOSER and held[i]:

                held[i] = 0  # Flanke zurücksetzen

                if chosen_configuration < len(configurations_map):

                    macros = configurations_map[chosen_configuration].getMacros()

                    if i < len(macros):

                        macro = macros[i]

                        # Prüfen, ob das Makro einen Release-Code für Windows hat (z.B. Pfeiltasten)

                        if hasattr(macro, "getReleaseCode"):

                            keyboard.release(macro.getReleaseCode())

  

while True:

    updateLeds()

    # Da wir reaktionsschnelles Gaming wollen, senken wir den Entprell-Delay auf 0.1 Sekunden

    readButton(0.1)

    time.sleep(0.001)
```
---
## 🛠️ Konfiguration

### Datei: configurations.py
```
import usb_hid

import time

  

from abstract_classes import AbstractConfiguration, AbstractMacro

from empty_classes import EmptyConfiguration, EmptyMacro

from adafruit_hid.keyboard import Keyboard

from adafruit_hid.keycode import Keycode

  

keyboard = Keyboard(usb_hid.devices)

  

# ==============================================================================

# HIER DEINE MAKROS EINTRAGEN / ERWEITERN

# ==============================================================================

  

class EscapeMacro(AbstractMacro):

    def getMacroName(): return 'ESC'

    def getMacro(): keyboard.send(Keycode.ESCAPE)

  

class SaveMacro(AbstractMacro):

    def getMacroName(): return 'Save'

    def getMacro(): keyboard.send(Keycode.CONTROL, Keycode.S)

  

class CopyMacro(AbstractMacro):

    def getMacroName(): return 'Copy'

    def getMacro(): keyboard.send(Keycode.CONTROL, Keycode.C)

  

class PasteMacro(AbstractMacro):

    def getMacroName(): return 'Paste'

    def getMacro(): keyboard.send(Keycode.CONTROL, Keycode.V)

  

class TabMacro(AbstractMacro):

    def getMacroName(): return 'Tab'

    def getMacro(): keyboard.send(Keycode.TAB)

  

# Gaming-Tasten nutzen .press() zum Halten und definieren .getReleaseCode()

class SpeedMacro(AbstractMacro):

    def getMacroName(): return 'Speed'

    def getMacro(): keyboard.press(Keycode.CONTROL)

    def getReleaseCode(): return Keycode.CONTROL

  

class UpMacro(AbstractMacro):

    def getMacroName(): return 'Up'

    def getMacro(): keyboard.press(Keycode.UP_ARROW)

    def getReleaseCode(): return Keycode.UP_ARROW

  

class E_Macro(AbstractMacro):

    def getMacroName(): return 'E'

    def getMacro(): keyboard.send(Keycode.E)

  

class LeftMacro(AbstractMacro):

    def getMacroName(): return 'Left'

    def getMacro(): keyboard.press(Keycode.LEFT_ARROW)

    def getReleaseCode(): return Keycode.LEFT_ARROW

  

class CrouchMacro(AbstractMacro):

    def getMacroName(): return 'Crouch'

    def getMacro(): keyboard.press(Keycode.END)

    def getReleaseCode(): return Keycode.END

  

class RightMacro(AbstractMacro):

    def getMacroName(): return 'Right'

    def getMacro(): keyboard.press(Keycode.RIGHT_ARROW)

    def getReleaseCode(): return Keycode.RIGHT_ARROW

  

class ShiftMacro(AbstractMacro):

    def getMacroName(): return 'Shift'

    def getMacro(): keyboard.press(Keycode.SHIFT)

    def getReleaseCode(): return Keycode.SHIFT

  

class DownMacro(AbstractMacro):

    def getMacroName(): return 'Down'

    def getMacro(): keyboard.press(Keycode.DOWN_ARROW)

    def getReleaseCode(): return Keycode.DOWN_ARROW

  

class I_Macro(AbstractMacro):

    def getMacroName(): return 'I'

    def getMacro(): keyboard.send(Keycode.I)

  
  

# ==============================================================================

# DEIN PROFIL (Gaming Pad an Position 0)

# ==============================================================================

  

class GamingPad(AbstractConfiguration):

    def getName():

        return 'Gaming Pad'

    def getColor():

        # Profilfarbe im Hauptmenü (z.B. lila leuchtend vor Auswahl)

        return (40, 0, 80)

    # Deine gewünschten Einzelfarben für den Macro-Modus

    def getButtonColors():

        return {  

            0: (250, 255, 0),

            1: (0, 7, 255),

            2: (0, 230, 255),  

            3: (0, 230, 255),  

            4: (250, 255, 0),

            5: (7, 255, 0),

            6: (255, 0, 137),

            7: (255, 103, 0),

            8: (57, 0, 169),

            9: (255, 0, 137),

            10: (7, 255, 0),

            11: (255, 0, 137),

            12: (57, 0, 169),  

            13: (7, 255, 0),  

            14: (255, 0, 137),  

            15: (255, 103, 0)  

        }

  

    def getMacros():

        return [

            EscapeMacro,    # Taste 0

            SaveMacro,      # Taste 1

            CopyMacro,      # Taste 2

            PasteMacro,     # Taste 3

            TabMacro,       # Taste 4

            SpeedMacro,     # Taste 5

            UpMacro,        # Taste 6

            E_Macro,        # Taste 7

            EmptyMacro,     # Taste 8

            LeftMacro,      # Taste 9

            CrouchMacro,    # Taste 10

            RightMacro,     # Taste 11

            EmptyMacro,     # Taste 12

            ShiftMacro,     # Taste 13

            DownMacro,      # Taste 14

            I_Macro         # Taste 15

        ]

  

configurations_map = [ GamingPad ]
```
---
## 🛠️ Abstrakte Klassen

Diese Datei dient als **Schablone** oder Vertrag. Sie sagt dem Anwender und Python, wie ein Makro oder eine Konfiguration _grundsätzlich_ aufgebaut sein muss, damit das Hauptprogramm (`code.py`) nicht abstürzt.
### Datei: abstract_classes.py
```
class AbstractConfiguration:


    def getName():

        return ""


    def getColor():

        return (0, 0, 0)


    def getMacros():

        return []


    def nothing():

        pass

  

class AbstractMacro:


    def getMacroName():

        return ""


    def getMacro():

        pass
```

---
## 🛠️ Leere Klassen

Diese Datei wird **aktiv im Code benutzt**, um leere Tasten oder ungenutzte Profil-Slots zu füllen. Das Keypad hat 16 Tasten. Wenn z.B. nur 14 Makros belegt sind, müssen die restlichen 2 Tasten trotzdem mit irgendwas gefüllt werden.
#### Zusammenhang mit "configurations.py" 
```
if i < len(macros) and not issubclass(macros[i], EmptyMacro):
    macros[i].getMacro() # Feuere das Makro nur ab, wenn es KEIN EmptyMacro ist!
```
---
### Datei: empty_classes.py
```
from abstract_classes import AbstractConfiguration, AbstractMacro
 

class EmptyConfiguration(AbstractConfiguration):


    def getName():

        return ""


    def getColor():

        return (0, 0, 0)


    def getMacros():

        return []


    def nothing():

        pass

  

class EmptyMacro(AbstractMacro):


    def getMacroName():

        return ""


    def getMacro():

        pass
```

---

### Übersetzung der Tasten in HID-Keycodes
Makros definieren (HID Befehle): 
```
TASTEN_BELEGUNG = {
    0: [Keycode.ESCAPE],
    1: [Keycode.CONTROL, Keycode.S],
    2: [Keycode.CONTROL, Keycode.C],
    3: [Keycode.CONTROL, Keycode.V],
    4: [Keycode.TAB],
    5: [Keycode.CONTROL],
    6: [Keycode.UP_ARROW],
    7: [Keycode.E], 
    8: [Keycode.#],
    9: [Keycode.LEFT_ARROW],
    10: [Keycode.END],
    11: [Keycode.RIGHT_ARROW],
    12: [Keycode.#],
    13: [Keycode.SHIFT],
    14: [Keycode.DOWN_ARROW],
    15: [Keycode.I] # Keycode.E 
}
```
## 🛠️Tasten, Farben und Funktionen

Keyboard Layout US (da Sprache vom Pico, Skript (Ada, py etc.) dieselbe sein müssen)
Bei der Tastenbelegung daher aufpassen (z.B. vertauschte Buchstaben Y und Z)
### Personalisierte Farben

```
colors = {  
0: (250, 255, 0),
1: (0, 7, 255),
2: (0, 230, 255),  
3: (0, 230, 255),  
4: (250, 255, 0),
5: (7, 255, 0),
6: (255, 0, 137),
7: (255, 103, 0),
8: (57, 0, 169),
9: (255, 0, 137),
10: (7, 255, 0),
11: (255, 0, 137),
12: (57, 0, 169),  
14: (7, 255, 0),
15: (255, 0, 137),  
16: (255, 103, 0)  
}
```

---

## 🛠️ Eingaben spezifizieren

### Erkennung der steigenden Flanke
Triggern von Tasten (Makros)

___Eine Taste soll erst dann wieder triggern, wenn sie vorher losgelassen wurde. Einmal kurz tippen, Aktion einmal ausführen.___
```kb.send()```

Befehl senden (drückt und lässt alle Tasten in der Liste gleichzeitig los)
```kb.send(*TASTEN_BELEGUNG[index])```

---
### Press & Release"-Logik
Kontinuierliche Eingaben (Bewegungstasten)

___Solange der Finger auf der Taste ist, muss das Signal "Taste ist gedrückt" an den PC gesendet werden. Erst beim Loslassen wird das Signal gestoppt.___
```kb.press()``` und ```kb.release()```

Anstatt nur den finalen Index zu berechnen, prüfen wir die einzelnen Bits.
Wenn Taste gedrückt wird: Signal "halten" aktivieren
```kb.press(*TASTEN_BELEGUNG[index])```

Wenn Taste losgelassen wird: Signal aufheben
```kb.release(*TASTEN_BELEGUNG[index])```



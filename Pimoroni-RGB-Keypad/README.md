## 🛠️ Initialisierung

### Hardware, Helligkeit und erster Refresh

```
import picokeypad
keypad = picokeypad.PicoKeypad()
keypad.set_brightness(1.0)
keypad.update()
```
---
## 🛠️ LED

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
---
## 🛠️Einzelne Farben definieren

```
import picokeypad
keypad = picokeypad.PicoKeypad()
keypad.set_brightness(1.0)
keypad.update()
```
---
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
## 🛠️Eingabe speichern

```
sequence = []
sequence.append(index)
```
---
## 🛠️Tasteneingabe

	genauer Bitwert (1, 2, 4, 8 … 32768)

```
button_states = keypad.get_button_states()
```
---
## 🛠️Sequenz abspielen

```
for step in sequence:
    keypad.illuminate(step, *colors[step])
    keypad.update()
    sleep(0.2)
    
    keypad.illuminate(step, 0, 0, 0)
    keypad.update()
```
---
## 🛠️Tasten und Funktionen

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

---
## 🛠️Playback

```
def play_sequence():
    for step in sequence:
        show(step)
        sleep(0.2)
        clear(step)
        sleep(0.1)
```

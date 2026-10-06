## 🛠️ Initialisierung

### Hardware, Helligkeit und erster Refresh

```
import picokeypad
keypad = picokeypad.PicoKeypad()
keypad.set_brightness(1.0)
keypad.update()
```

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

## 🛠️Einzelne Farben definieren

```
import picokeypad
keypad = picokeypad.PicoKeypad()
keypad.set_brightness(1.0)
keypad.update()
```

## 🛠️Eingabe speichern

```
sequence = []
sequence.append(index)
```

## 🛠️Tasteneingabe

	genauer Bitwert (1, 2, 4, 8 … 32768)

```
button_states = keypad.get_button_states()
```

## 🛠️Sequenz abspielen

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

## 🛠️Playback

```
def play_sequence():
    for step in sequence:
        show(step)
        sleep(0.2)
        clear(step)
        sleep(0.1)
```

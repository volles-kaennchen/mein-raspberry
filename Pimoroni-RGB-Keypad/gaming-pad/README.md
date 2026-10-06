# Projekt noch nicht fertig
- Inhalt: ```kb.send()```;```kb.press()``` und ```kb.release()```;
- Buggs: `held`, `last_state` und `debounce_time`
-     Flankenerkennung, Erkennen des Wechsels von "nicht gedrückt" zu "gedrückt" mit Timing-Fehler
- Ghost Inputs: `keyboard.press()` hält eine Taste dauerhaft gedrückt. Wird das Loslassen verpasst, bleibt die Taste hängen
-  Klassen: `SpeedMacro`, `UpMacro`, `ShiftMacro

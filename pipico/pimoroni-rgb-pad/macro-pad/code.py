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
					held[i] = 1  # Flanke merken (Taste ist jetzt gedrückt)
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
				held[i] = 0  # Flanke zurücksetzen
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
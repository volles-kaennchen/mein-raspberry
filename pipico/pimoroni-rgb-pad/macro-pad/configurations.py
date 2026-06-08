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
			EscapeMacro,    # Taste 0
			SaveMacro,      # Taste 1
			CopyMacro,      # Taste 2
			PasteMacro,     # Taste 3
			TabMacro,       # Taste 4
			SpeedMacro,     # Taste 5
			UpMacro,        # Taste 6
			E_Macro,        # Taste 7
			EmptyMacro,     # Taste 8
			LeftMacro,      # Taste 9
			CrouchMacro,    # Taste 10
			RightMacro,     # Taste 11
			EmptyMacro,     # Taste 12
			ShiftMacro,     # Taste 13
			DownMacro,      # Taste 14
			I_Macro         # Taste 15
		]

configurations_map = [ GamingPad ]
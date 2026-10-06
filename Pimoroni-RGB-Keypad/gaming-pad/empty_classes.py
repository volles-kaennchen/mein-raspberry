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

import ntpath

# context
class Context:
	window = None
	settingsPath = ""
	basedir = ""
	scriptModules = None
	textModules = None

	def __init__(self, window, settingsPath):
		self.window = window
		self.settingsPath = settingsPath

	def window(self):
		return self.window

	def settingsPath(self):
		return self.settingsPath

	def getBaseDir(self):
		return ntpath.dirname(self.settingsPath) + "/"

	def setSettings(self, settings):
		self.settings = settings

	def settings(self):
		return self.settings

	def isSublimeRJS(self):
		return self.settingsPath is not ""

	def resetModules(self):
		self.scriptModules = []
		self.textModules = []

	def addScriptModule(self, module):
		self.scriptModules.append(module)

	def getScriptModules(self):
		return self.scriptModules

	def addTextModule(self, module):
		self.textModules.append(module)

	def getTextModules(self):
		return self.textModules


# module
class Module:
	name = ""
	path = ""
	type = ""
	package = ""

	def __init__(self, name, path, ext, type, package):
		self.name = name
		self.path = path
		self.ext = ext
		self.type = type
		self.package = package

	def name(self):
		return self.name

	def package(self):
		return self.package

	def getImportString(self):
		if self.type == "script":
			return self.package + self.name.split(self.ext)[0]
		elif self.type == "text":
			return "text!" + self.package + self.name

	def getRefrenceString(self):
		return self.name.split(self.ext)[0]

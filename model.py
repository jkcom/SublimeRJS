import ntpath

# context
class Context:
	window = None
	settingsPath = ""
	basedir = ""
	modules = None

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
		self.modules = []

	def addModule(self, module):
		self.modules.append(module)

	def getModules(self):
		return self.modules


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

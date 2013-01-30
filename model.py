

# context
class Context:
	window = None
	settingsPath = ""

	def __init__(self, window, settingsPath):
		self.window = window
		self.settingsPath = settingsPath

	def window(self):
		return self.window

	def settingsPath(self):
		return self.settingsPath

	def isSublimeRJS(self):
		return self.settingsPath is not ""

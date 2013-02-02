import sublime
import json

class ModuleEdit:

	def __init__(self, content):
		self.content = content
		#parse
		defineRegion = self.getDefineRegion()
		defineString = content[defineRegion.begin():defineRegion.end()]
		#parse modules
		modulesStart = defineString.find("[")
		modulesEnd = defineString.find("]")
		modulesTemp = defineString[(modulesStart+1):(modulesEnd)]
		modulesTemp = modulesTemp.replace("'", '')
		modulesTemp = modulesTemp.replace('"', '')
		modulesTemp = modulesTemp.replace(' ', '')
		self.modules = modulesTemp.split(",")
		if (self.modules[0] == ""):
			self.modules = []
		#parse refrences
		refrencesStart = defineString.find("(", modulesEnd)
		refrencesEnd = defineString.find(")")
		refrencesTemp = defineString[(refrencesStart + 1):refrencesEnd].split(" ")
		self.refrences = "".join(refrencesTemp).split(",")
		if (self.refrences[0] == ""):
			self.refrences = []


	def getDefineRegion(self):
		startIndex = self.content.find("define(")
		endIndex = self.content.find("{", startIndex)
		return sublime.Region(startIndex, endIndex)

	def addModule(self, module):
		self.modules.append(module.getImportString())
		self.refrences.append(module.getRefrenceString())

	def render(self):
		output = "define(["
		# modules
		isFirst = True
		for module in self.modules:
			if not isFirst:
				output += ", "
			else:
				isFirst = False
			output += "'" + module + "'"
		output += "]"
		# fundtion
		output += ", function("
		# refrences
		isFirst = True
		for refrence in self.refrences:
			if not isFirst:
				output += ", "
			else:
				isFirst = False
			output += refrence
		output += ")"
		return output

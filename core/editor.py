import sublime
import math

class ModuleEdit:

	def __init__(self, content, context):
		self.content = content
		self.context = context
		#parse
		defineRegion = self.getDefineRegion()
		defineString = content[defineRegion.begin():defineRegion.end()]
		#parse modules
		modulesStart = defineString.find("[")
		if modulesStart > -1:
			modulesEnd = defineString.find("]")
			modulesTemp = defineString[(modulesStart + 1):(modulesEnd)]
			modulesTemp = modulesTemp.replace("'", '')
			modulesTemp = modulesTemp.replace('"', '')
			modulesTemp = modulesTemp.replace(' ', '')
			self.modules = modulesTemp.split(",")
			if (self.modules[0] == ""):
				self.modules = []
		else:
			self.modules = []
		#parse refrences
		refrencesStart = defineString.rfind("(")
		refrencesEnd = defineString.find(")")
		refrencesTemp = defineString[(refrencesStart + 1):refrencesEnd].split(" ")
		self.refrences = "".join(refrencesTemp).split(",")
		if (self.refrences[0] == ""):
			self.refrences = []

	def getModuleList(self):
		commentList = "\n    /*\n    *    Module list\n"
		commentList += "    *\n"

		commentList += self.renderListGroup(self.modulesCollection["autoModules"], True)
		commentList += self.renderListGroup(self.modulesCollection["scriptModules"], True)
		commentList += self.renderListGroup(self.modulesCollection["textModules"], False)

		commentList += "    */"

		return commentList

	def renderListGroup(self, items, addBlankLine):
		if len(items) == 0:
			return ""
		listBody = ""
		sortedKeys = sorted(items, reverse = False)
		numSpaces = 20
		for x in range(0, len(sortedKeys)):
			listBody += "    *    " + sortedKeys[x]
			spaces = numSpaces - len(sortedKeys[x])
			for y in range(0, spaces):
				listBody += " "
			listBody += items[sortedKeys[x]] + "\n"
		if addBlankLine == True:
			listBody += "    *" + "\n"
		return listBody

	def getDefineRegion(self):
		startIndex = self.content.find("define(")

		if self.content.find("*    Module list") is not -1:
			endIndex = self.content.find("*/", startIndex) + 2
		else:
			endIndex = self.content.find("{", startIndex) + 1
		return sublime.Region(startIndex, endIndex)

	def addModule(self, module, moduleString):
		if (module is None):
			self.modules.append(moduleString)
			self.refrences.append(moduleString)
		else:
			self.modules.append(module.getImportString())
			self.refrences.append(module.getRefrenceString())

		self.updateModuleList()

	def render(self):
		output = "define("
		# modules
		if len(self.modules) > 0:
			isFirst = True
			output += "["
			for module in self.modules:
				if not isFirst:
					output += ", "
				else:
					isFirst = False
				output += "'" + module + "'"
			output += "], "
		# fundtion
		output += "function("
		# refrences
		isFirst = True
		for refrence in self.refrences:
			if not isFirst:
				output += ", "
			else:
				isFirst = False
			output += refrence
		output += ") {"
		print "settings is ", self.context.settings["list_modules"], self.context.settings["list_modules"] == "true"
		if str(self.context.settings["list_modules"]) == "true":
			print "add list"
			output += "\n" + self.getModuleList()
		
		return output

	def getModules(self):
		modules = []
		for importString in self.modules:
			module = self.context.getModuleByImportString(importString)
			if module is not None:
				modules.append(module)
		return modules

	def removeModule(self, module):
		self.modules.pop(self.modules.index(module.getImportString()))
		self.refrences.pop(self.refrences.index(module.getRefrenceString()))

		self.updateModuleList()

	def updateModuleList(self):
		# run throug for module list
		self.modulesCollection = {
			"autoModules": {},
			"scriptModules": {},
			"textModules": {}
		}
		for importString in self.modules:
			module = self.context.getModuleByImportString(importString)
			if module is not None:
				if module.getImportString() in self.context.settings["auto_add"]:
					self.modulesCollection["autoModules"][module.getRefrenceString()] = module.getRelativePath()
				elif module.type == "script":
					self.modulesCollection["scriptModules"][module.getRefrenceString()] = module.getRelativePath()
				elif module.type == "text":
					self.modulesCollection["textModules"][module.getRefrenceString()] = module.getRelativePath()

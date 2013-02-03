import sublime

class ModuleEdit:

	def __init__(self, content, context):
		self.content = content
		self.context = context
		#parse
		defineRegion = self.getDefineRegion()
		defineString = content[defineRegion.begin():defineRegion.end()]
		#parse modules
		modulesStart = defineString.find("[")
		print "ms", modulesStart
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


	def getDefineRegion(self):
		startIndex = self.content.find("define(")
		endIndex = self.content.find("{", startIndex)
		return sublime.Region(startIndex, endIndex)

	def addModule(self, module):
		self.modules.append(module.getImportString())
		self.refrences.append(module.getRefrenceString())

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
		output += ") "
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

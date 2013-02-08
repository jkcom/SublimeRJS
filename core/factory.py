import sys
sys.path.append("core")

import os
import model
import editor
import ntpath

global shadowList

global createConfig
createConfig = {}

global context


def createModule(newContext, newCreateConfig):
	global context
	global createConfig
	global shadowList
	context = newContext
	createConfig = newCreateConfig
	if createConfig["type"] == "script":
		packages = context.getScriptPackages()
	elif createConfig["type"] == "text":
		packages = context.getTextPackages()

	context.window.show_quick_panel(packages, onPackageSelected, 0)
	shadowList = packages


def onPackageSelected(selectionIndex):
	global createConfig
	global shadowList
	moduleSuggestiong = shadowList[selectionIndex]
	if createConfig["type"] == "script":
		print "SCRIPT"
		for sp in context.settings["script_folders"]:
			packagePath = context.getBaseDir()+ sp + "/" + moduleSuggestiong
			if os.path.exists(packagePath) == True:
				createConfig["packageBase"] = sp
	elif createConfig["type"] == "text":
		print "TEXT"
		for sp in context.settings["text_folders"]:
			packagePath = context.getBaseDir()+ sp + "/" + moduleSuggestiong
			if os.path.exists(packagePath) == True:
				createConfig["packageBase"] = sp


	context.window.show_input_panel("Name your new module", moduleSuggestiong+createConfig["name"], onNameDone, onNameChange, onNamceCancle)


def onNameDone(inputString):
	global createConfig
	global context
	global shadowList
	moduleFile = context.getBaseDir() + createConfig["packageBase"] + "/" + inputString
	createConfig["moduleFile"] = moduleFile
	print moduleFile

	name = moduleFile[moduleFile.rfind("/"):]
	if not "." in name:
		if createConfig["type"] == "script":
			ext = ".js"
			name += ext
		elif createConfig["type"] == "text":
			ext = ".html"
			name += ext
	else:
		ext = name[name.rfind("."):]

	moduleDir = moduleFile[0:moduleFile.rfind("/")]
	moduleFile = moduleDir + name
	createConfig["moduleFile"] = moduleFile
	if os.path.exists(moduleDir) == False:
		os.makedirs(moduleDir)


	# ask for snippet
	if context.settings["module_templates"] is not "":
		snippetsDir = context.getBaseDir() + context.settings["module_templates"]
		snippets = []
		shadowList =[]
		snippets.append("Blank")
		shadowList.append("")
		for file in os.listdir(snippetsDir):
			dirfile = os.path.join(snippetsDir, file)
			if os.path.isfile(dirfile):
				snippets.append(ntpath.basename(file))
				shadowList.append(dirfile)

		context.window.show_quick_panel(snippets, onSnippetSelected, 0)
	else:
		finish("")

def onSnippetSelected(selectionIndex):
	global shadowList
	if selectionIndex == 0:
		finish("")
	else:
		moduleName = createConfig["moduleFile"][createConfig["moduleFile"].rfind("/") + 1:createConfig["moduleFile"].rfind(".")]
		f = open(shadowList[selectionIndex], "r")
		data = f.read()
		snippet = data
		snippet = snippet.replace("$MODULE_NAME", moduleName)
		f.close()
		finish(snippet)


def finish(snippet):
	global createConfig
	global context
	fileContent = ""
	if createConfig["type"] == "script":
		fileContent = "define(function(){});"
		if len(context.settings["auto_add"]) > 0:
			for module in context.settings["auto_add"]:
				addEdit = editor.ModuleEdit(fileContent, context)
				addEdit.addModule(context.getModuleByImportString(module))
				fileContent = addEdit.render()+ "{\n"+snippet+"\n});";	

	file = open(createConfig["moduleFile"], 'w+')
	file.write(fileContent)
	file.close()

	# callback to let module be imported
	if createConfig["type"] == "script":
		temp = (createConfig["moduleFile"]).split(context.getBaseDir() + createConfig["packageBase"] + "/")[1];
		importString = temp[0:temp.rfind(".")]
	elif createConfig["type"] == "text":
		temp = (createConfig["moduleFile"]).split(context.getBaseDir() + createConfig["packageBase"] + "/")[1];
		importString = "text!" + temp
	createConfig["callback"](importString, createConfig)


def onNameChange(input):
	pass

def onNamceCancle(input):
	pass

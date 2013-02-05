import os
import model
import editor

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
	moduleSuggestiong = shadowList[selectionIndex] + createConfig["name"]
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


	context.window.show_input_panel("Name your new module", moduleSuggestiong, onNameDone, onNameChange, onNamceCancle)


def onNameDone(inputString):
	global createConfig
	global context
	moduleFile = context.getBaseDir() + createConfig["packageBase"] + "/" + inputString
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

	print name, ext

	moduleDir = moduleFile[0:moduleFile.rfind("/")]
	moduleFile = moduleDir + name
	if os.path.exists(moduleDir) == False:
		os.makedirs(moduleDir)

	fileContent = "define(function(){});"
	if len(context.settings["autoadd"]) > 0:
		for module in context.settings["autoadd"]:
			print "add module ", module
			addEdit = editor.ModuleEdit(fileContent, context)
			addEdit.addModule(context.getModuleByImportString(module))
			fileContent = addEdit.render()+ "{});";

	file = open(moduleFile, 'w+')
	file.write(fileContent)
	file.close()
	createConfig["callback"]()
	# create module

	#package = file.split(parseConfig.folder)[1][1:].split(ntpath.basename(file))[0]
	#module = model.Module(ntpath.basename(file), ntpath.dirname(file), ext, createConfig["type"], package)
	# check module for aliases
	#moduleAliasMap = context.getModuleAliasMap()
	#if module.getImportString() in moduleAliasMap:
	#	module.setImportAlias(moduleAliasMap[module.getImportString()])
	# check for refrence aliases
	#if module.getImportString() in context.settings["aliases"]:
	#	module.setRefrenceAlias(context.settings["aliases"][module.getImportString()])
	# add to context
	#if module.type == "script":
	#	context.addScriptModule(module)
	#elif module.type == "text":
	#	context.addTextModule(module)
	pass

def onNameChange(input):
	pass

def onNamceCancle(input):
	pass

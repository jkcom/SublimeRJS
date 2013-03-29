import sys
sys.path.append("core")

from threading import Thread

import os
import os.path
import re

global context
global moveConfig
global shadowList
global threads
global moduleToMove
global t 
global onModuleMoved

# test commit

def moveModuleInView(activeContext, onModuleMovedCallBack):
	global onModuleMoved
	onModuleMoved = onModuleMovedCallBack
	global context
	context = activeContext

	global moduleToMove
	
#	get module to move
	moduleToMove = context.getModuleByFullPath(context.window.active_view().file_name())
	if moduleToMove is None:
		return


	global moveConfig
	global shadowList

	moveConfig = {
		"type": moduleToMove.type,
		"fullPath": moduleToMove.getFullPath(),
		"name": moduleToMove.name[0:moduleToMove.name.find(".")],
		"importString":moduleToMove.package + moduleToMove.name.split(moduleToMove.ext)[0]
	}
	
	
	if moveConfig["type"] == "script":
		packages = context.getScriptPackages()
	elif moveConfig["type"] == "text":
		packages = context.getTextPackages()

	context.window.show_quick_panel(packages, onPackageSelected, 0)
	shadowList = packages


def onPackageSelected(selectionIndex):
	global moveConfig
	global shadowList
	moduleSuggestiong = shadowList[selectionIndex]
	if selectionIndex == -1:
		return
	if selectionIndex == 0:
		moduleSuggestiong = ""


	if moveConfig["type"] == "script":
		packagePath = context.getBaseDir()+ context.settings["script_folder"] + "/" + moduleSuggestiong
		if os.path.exists(packagePath) == True:
			moveConfig["packageBase"] = context.settings["script_folder"]
	elif moveConfig["type"] == "text":
		
		packagePath = context.getBaseDir()+ context.settings["text_folder"] + "/" + moduleSuggestiong
		if os.path.exists(packagePath) == True:
			moveConfig["packageBase"] = context.settings["text_folder"]

	context.window.show_input_panel("Change module path/name to: ", moduleSuggestiong+moveConfig["name"], onNameDone, onNameChange, onNamceCancle)

def onNameDone(inputString):

	global moveConfig
	global onModuleMoved
	global context

	moveConfig["newImportString"] = inputString
	moveConfig["newName"] = inputString[inputString.rfind("/")+1:]
	
	moveModule()
	onModuleMoved()

	updateModules()
	
	
	pass

def moveModule():
	global moduleToMove
	global context
	global moveConfig
	context.window.run_command("close_file")

	if moduleToMove.type is "text":
		current = context.settings["text_folder"] + "/" +moveConfig["importString"]
		new = context.settings["text_folder"] + "/" +moveConfig["newImportString"]
	else:
		current = context.settings["script_folder"] + "/" +moveConfig["importString"]
		new = context.settings["script_folder"] + "/" +moveConfig["newImportString"]

	newFullPath  = moduleToMove.getFullPath().replace(current, new)


	dir = os.path.dirname(newFullPath)

	if not os.path.exists(dir):
		os.makedirs(dir)

	os.rename(moduleToMove.getFullPath(), newFullPath)
	context.window.open_file(newFullPath)

	pass


def onNameChange(input):
	pass

def onNamceCancle(input):
	pass

def updateModules():
	global moveConfig
	global context
	global moduleToMove
	global t


	if moduleToMove.type is "text":
		#moveConfig["importString"] = "text!" + context.settings["texts_name"] + "/" + moveConfig["importString"] + ".html"
		#moveConfig["newImportString"] = "text!" + context.settings["texts_name"] + "/" + moveConfig["newImportString"] + ".html"
		pass
	
	# update module refs
	modulesList = context.getScriptModules()
	if moduleToMove in modulesList:
		modulesList.remove(moduleToMove)
	count = 0
	t = Thread(target=update, args=(modulesList, moveConfig, updateDone))
	t.start()



def updateDone():
	pass
    

def update(modules, moveConfig, callback):
	global moduleToMove
	for module in modules:
		f = open(module.getFullPath(), "r")
		data = f.read()
		f.close();

		if data.find("define([") is not -1 and data.find(moveConfig["importString"]) is not -1:
			updateModule(module, data, moveConfig)

	callback();
	pass

def updateModule(module, data, moveConfig):
	
	#update import string
	data = data.replace("'"+moveConfig["importString"]+"'", "'"+moveConfig["newImportString"]+"'", 1)
	#data = re.sub('\\b'+moveConfig["importString"]+'\\b', moveConfig["importString"], data)

	#update variable name
	if moveConfig["name"] is not moveConfig["newName"]:
		data = re.sub('\\b'+moveConfig["name"]+'\\b', moveConfig["newName"], data)

	f = open(module.getFullPath(), "w+")
	f.write(data)
	f.close()
	pass




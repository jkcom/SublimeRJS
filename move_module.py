import sys
sys.path.append("core")

from threading import Thread

import os
import os.path

global context
global moveConfig
global shadowList
global threads
global moduleToMove
global t 
global onModuleMoved

def moveModuleInView(activeContext, onModuleMovedCallBack):
	global onModuleMoved
	onModuleMoved = onModuleMovedCallBack
	global context
	context = activeContext

	global moduleToMove
	
#	get module to move
	print "move", context.window.active_view().file_name()
	moduleToMove = context.getModuleByFullPath(context.window.active_view().file_name())
	if moduleToMove is None:
		return


	global moveConfig
	global shadowList

	moveConfig = {
		"type": moduleToMove.type,
		"fullPath": moduleToMove.getFullPath(),
		"name": moduleToMove.name[0:moduleToMove.name.find(".")],
		"importString":moduleToMove.getImportString()
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


	moveConfig["newImportString"] = inputString
	moveModule()
	onModuleMoved()

	updateModules()
	
	
	pass

def moveModule():
	global moduleToMove
	global context
	context.window.run_command("close_file")
	newFullPath  = moduleToMove.getFullPath().replace(moveConfig["importString"], moveConfig["newImportString"])


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
	
	# update module refs
	modulesList = context.getScriptModules()
	modulesList.remove(moduleToMove)
	count = 0
	t = Thread(target=update, args=(modulesList, moveConfig, updateDone))
	t.start()



def updateDone():
	print "update done"
	
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
	print "update module", module.name
	print "change package at : ", moveConfig["importString"]
	print "change package at : ", moveConfig["newImportString"]

	#update import string
	data = data.replace(moveConfig["importString"], moveConfig["newImportString"], 1)


	f = open(module.getFullPath(), "w+")
	f.write(data)
	f.close()
	pass




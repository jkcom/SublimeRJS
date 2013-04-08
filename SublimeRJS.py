import sys
sys.path.append( "core")

import model

import sublime
import sublime_plugin
import move_module


import file_search
import module_parser
import editor
import context_helper
import factory
import json
import shutil
import pprint


global context
context = None

global contextWindow
contextWindow = None

global shadowList
shadowList = None

global moduleAddInLine
moduleAddInLine = None

global moduelOpenInLine
moduleOpenInLine = None

global currentModuleEdit

# update contexts
def getContext(window):
	global context
	global contextWindow
	# clean up old context
	context = None
	contextWindow = window

	# find sublime settings file in new active window
	if window is not None:
		for folder in window.folders():
			file_search.findFile(folder, "SublimeRJS.sublime-settings", onSearchedForSettings)


# on searched for contexs.get("script_folders")
def onSearchedForSettings(file):
	if file is not None:
		setContext(model.Context(contextWindow, file))
	else:
		pass


# set context
def setContext(newContext):
	global context
	context = newContext

	# hack to get back to main thread
	sublime.set_timeout(initContext, 1)


# load settings
def initContext():
	global context
	context_helper.initializeContext(context)
	module_parser.parseModules(context, onModulePareDone)

def onModulePareDone(): 
	sublime.set_timeout(checkModulesAddInLine, 1)


def checkModulesAddInLine():
	global moduleAddInLine
	global moduleOpenInLine
	module = context.getModuleByImportString(moduleAddInLine)
	if module is not None:
		addModule(module)
		moduleAddInLine = None
	if moduleOpenInLine is not None:
		openModuleFile(context.getModuleByImportString(moduleOpenInLine))
		moduleOpenInLine = None
	pass


def openModuleFile(module):
	if module.type == "script":
		focus = int(context.settings["script_group"])
		sublime.active_window().focus_group(focus)
	elif module.type == "text":
		focus = int(context.settings["text_group"])
		sublime.active_window().focus_group(focus)
	sublime.active_window().open_file(module.getFullPath())


# application listner
class AppListener(sublime_plugin.EventListener):

	def on_post_save(self, view):
		global context
		if context is not None:
			if sublime.active_window().active_view().file_name() == context.settingsPath:
				getContext(sublime.active_window())
		pass

	def on_activated(self, view):
		if context is not None:
			if sublime.active_window() is not None:
				if sublime.active_window().id() != context.window.id():
					getContext(sublime.active_window())
			else:
				getContext(sublime.active_window())
		else:
			getContext(sublime.active_window())
			

def updateContext():
	getContext(sublime.active_window())
	pass

def moveModule():
	global context
	move_module.moveModuleInView(context, updateContext)

# select module
def selectModule(onSelectCallback, group):
	global shadowList
	global context
	shadowList = []
	list = []

	for module in group:
		module = filterModule(module)
		if module is not None:
			list.append([module.name, module.package])
			shadowList.append(module)
	context.window.show_quick_panel(list, onSelectCallback, 0)

def filterModule(module):
	if len(context.settings["excludes"]) > 0:
		for exclude in context.settings["excludes"]:
			if context.getBaseDir() + exclude in module.path + "/" + module.name:
				return None
	return module

def addModule(module):
	if module is None:
		return
	global context
	addEdit = editor.ModuleEdit(context.window.active_view().substr(sublime.Region(0, context.window.active_view().size())), context)
	# get define region
	defineRegion = addEdit.getDefineRegion()
	addEdit.addModule(module, "")
	edit = context.window.active_view().begin_edit()
	context.window.active_view().replace(edit, defineRegion, addEdit.render())
	context.window.active_view().end_edit(edit)


def onScriptSelectAdd(selectionIndex):
	if selectionIndex == -1:
		return
	global shadowList
	addModule(shadowList[selectionIndex])


def onTextSelectAdd(selectionIndex):
	if selectionIndex == -1:
		return
	global shadowList
	addModule(shadowList[selectionIndex])

# remove module
def removeModule():
	global context
	global currentModuleEdit
	currentModuleEdit = editor.ModuleEdit(context.window.active_view().substr(sublime.Region(0, context.window.active_view().size())), context)
	modules = currentModuleEdit.getModules()
	selectModule(onModuleSelectRemove, modules)

def onModuleSelectRemove(selectionIndex):
	if selectionIndex == -1:
		return
	global shadowList
	global currentModuleEdit
	global context
	currentModuleEdit.removeModule(shadowList[selectionIndex])
	edit = context.window.active_view().begin_edit()
	context.window.active_view().replace(edit, currentModuleEdit.getDefineRegion(), currentModuleEdit.render())
	context.window.active_view().end_edit(edit)

def createModule(importOnCreated, type):
	global context
	region = context.window.active_view().sel()[0]
	moduleName = ""
	if region.begin() != region.end():
		moduleName = context.window.active_view().substr(region)
	createConfig = {
		"type": type,
		"callback": onModuleCreated,
		"name": moduleName,
		"importOnCreated":importOnCreated
	}

	factory.createModule(context, createConfig)

def onModuleCreated(importString, createConfig):
	global moduleAddInLine
	global moduleOpenInLine
	if createConfig["importOnCreated"] == True:
		moduleAddInLine = importString
	moduleOpenInLine = importString
	module_parser.parseModules(context, onModulePareDone)


# main callback
def onMainActionSelected(selectionIndex):
	global context
	if selectionIndex == -1:
		return
	if len(context.settings["text_folder"]) > 0:
		if (selectionIndex == 0):
			selectModule(onScriptSelectAdd, context.getScriptModules())
		elif (selectionIndex == 1):
			selectModule(onTextSelectAdd, context.getTextModules())
		elif selectionIndex == 2:
			removeModule()
		elif selectionIndex == 3:
			createModule(False, "script")
		elif selectionIndex == 4:
			createModule(False, "text")
		elif selectionIndex == 5:
			createModule(True, "script")
		elif selectionIndex == 6:
			createModule(True, "text")
		elif selectionIndex == 7:
			moveModule()
	else:
		if (selectionIndex == 0):
			selectModule(onScriptSelectAdd, context.getScriptModules())
		elif selectionIndex == 1:
			removeModule()
		elif selectionIndex == 2:
			createModule(False, "script")
		elif selectionIndex == 3:
			createModule(True, "script")
		elif selectionIndex == 4:
			moveModule()


def onScriptSelectOpen(selectionIndex):
	if selectionIndex == -1:
		return
	global shadowList
	sublime.active_window().open_file(shadowList[selectionIndex].getFullPath())
	pass


def onTextSelectOpen(selectionIndex):
	if selectionIndex == -1:
		return
	global shadowList
	sublime.active_window().open_file(shadowList[selectionIndex].getFullPath())
	pass


def openModule(index):
	global context
	if context.settings["script_group"] == str(index):
		selectModule(onScriptSelectOpen, context.getScriptModules())
	elif context.settings["text_group"] == str(index):
		selectModule(onTextSelectOpen, context.getTextModules())


class SublimeRjsOpen1Command(sublime_plugin.WindowCommand):
	def run(slef):
		sublime.active_window().focus_group(0)
		openModule(0)


class SublimeRjsOpen2Command(sublime_plugin.WindowCommand):
	def run(slef):
		sublime.active_window().focus_group(1)
		openModule(1)


class SublimeRjsOpen3Command(sublime_plugin.WindowCommand):
	def run(slef):
		sublime.active_window().focus_group(2)
		openModule(2)


class SublimeRjsCommand(sublime_plugin.WindowCommand):
    def run(self):
    	global context
    	# get selection
    	createAndImportScript = "Create and import SCRIPT module"
    	createAndImportText = "Create and import TEXT module"
    	region = context.window.active_view().sel()[0]
    	if region.begin() != region.end():
    		createAndImportScript += " '" +context.window.active_view().substr(region)+"'"
    		createAndImportText += " '" +context.window.active_view().substr(region)+"'"

    	if len(context.settings["text_folder"]) > 0:
    		options = ["Import SCRIPT module", "Import TEXT module", "Remove module", "Create SCRIPT module", "Create TEXT module", createAndImportScript, createAndImportText, "Move/Rename module"]
    	else:
    		options = ["Import SCRIPT module", "Remove module", "Create SCRIPT module", createAndImportScript, "Move/Rename module"]
    	self.window.show_quick_panel(options, onMainActionSelected, 0)


class AddSublimeRjsCommand(sublime_plugin.ApplicationCommand):
	def run(self, dirs):
		srcFile = sublime.packages_path() + "/SublimeRJS/SublimeRJS Project.sublime-settings"
		destFile = dirs[0] + "/SublimeRJS.sublime-settings"
		shutil.copyfile(srcFile, destFile)
		sublime.active_window().open_file(destFile)
		getContext(sublime.active_window())		

# startup
getContext(sublime.active_window())

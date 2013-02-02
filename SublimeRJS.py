import sublime
import sublime_plugin

import json
from pprint import pprint

import model
import file_search
import module_parser
import editor

global context
context = None

global contextWindow
contextWindow = None

global shadowList
shadowList = None


# update contexts
def getContext(window):
	global context
	global contextWindow
	# clean up old context
	context = None
	contextWindow = window

	# find sublime settings file in new active window
	for folder in window.folders():
		file_search.findFile(folder, "SublimeRJS.sublime-settings", onSearchedForSettings)


# on searched for contexs.get("script_folders")
def onSearchedForSettings(file):
	if file is not None:
		setContext(model.Context(contextWindow, file))
	else:
		print "No SublimeRJS Context"


# set context
def setContext(newContext):
	global context
	context = newContext

	# hack to get back to main thread
	sublime.set_timeout(loadSettings, 1)


# load settings
def loadSettings():
	global context
	json_data = open(context.settingsPath)
	data = json.load(json_data)
	pprint(data)
	json_data.close()
	context.setSettings(data)
	module_parser.parseModules(context)


# application listner
class AppListener(sublime_plugin.EventListener):

	def on_post_save(self, view):
		pass

	def on_activated(self, view):
		if context is not None:
			if view.window() is not None:
 				if view.window().id() != context.window.id():
					getContext(view.window())
			else:
				getContext(view.window)
		else:
			getContext(view.window())


# select module
def selectModule(onSelectCallback):
	global shadowList
	global context
	shadowList = []
	list = []

	for module in context.getModules():
		list.append([module.name, module.package])
	context.window.show_quick_panel(list, onSelectCallback, 0)


def onModuleSelectAdd(selectionIndex):
	global context
	edit = editor.ModuleEdit(context.window.active_view().substr(sublime.Region(0, context.window.active_view().size())))
	


# main callback
def onMainActionSelected(selectionIndex):
	if (selectionIndex == 0):
		selectModule(onModuleSelectAdd)


class SublimeRjsCommand(sublime_plugin.WindowCommand):
    def run(self):
    	self.window.show_quick_panel(["Add module", "Create module", "Remove module"], onMainActionSelected, 0)


# startup
getContext(sublime.active_window())

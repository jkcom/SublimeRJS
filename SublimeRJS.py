import sublime
import sublime_plugin
import file_search
import model
import json
from pprint import pprint

global context
context = None

global contextWindow
contextWindow = None


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
	sublime.set_timeout(loadSettings, 1)


# load settings
def loadSettings():
	global context
	json_data = open(context.settingsPath)
	data = json.load(json_data)
	pprint(data)
	json_data.close()
	print data["script_folders"][0]


# application listner
class AppListener(sublime_plugin.EventListener):

	def on_post_save(self, view):
		pass

	def on_activated(self, view):
		print "Activated"
		if context is not None:
 			if view.window().id() != context.window.id():
				getContext(view.window())
		else:
			getContext(view.window())


# startup
getContext(sublime.active_window())

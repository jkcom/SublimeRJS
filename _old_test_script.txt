import sublime
import sublime_plugin
import os
import re
import threading
import shutil
from os.path import basename
import json
from pprint import pprint


s = sublime.load_settings("BoneFixr.sublime-settings")


class AddSublimeRjsCommand(SublimeRJS, sublime_plugin.ApplicationCommand):
	def run(self, dirs):
		srcFile = sublime.packages_path() + "/SublimeRJS/SublimeRJS Project.sublime-settings"
		destFile = dirs[0] + "/SublimeRJS.sublime-settings"
		print("SRC : " + srcFile)
		print("SRC : " + destFile)
		print(dir(sublime))
		print(sublime.active_window().open_file(destFile))
		json_data=open(destFile)
		data = json.load(json_data)
		pprint(data)
		json_data.close()
		print data["script_folders"][0]



class SublimeRjsCommand(sublime_plugin.WindowCommand):
    def run(self):
    	#self.window.show_quick_panel(["Add module", "Create module", "Remove module"], self._quick_panel_callback, 0)
        print("test : " + str(s.get("script_folders")[0]))


class Module:
	_name = ""
	_package = ""
	_filename = ""

	def __init__(self, name, package, filename, moduleType):
		self._name = name
		self._filename = filename
		self._package = package
		self._moduleType = moduleType

	def name(self):
		return self._name

	def package(self):
		return self._package

	def filename(self):
		return self._filename

	def moduleType(self):
		return self._moduleType

class SublimeRJS:
	_modules = []
	_active = None

	def setActive(self, active):
		self._active = active

	def getActive(self):
		return self._active

	def clear(self):
		self._modules = []

	def addFunc(self, name, package, filename):
		self._modules.append(Method(name, package, filename))

	def get_autocomplete_list(self, word):
		autocomplete_list = []

		print word
		for method_obj in self._modules:
			if word.lower() in method_obj.name().lower():
				method_str_to_append = method_obj.name() + '(' + method_obj.package()+ ')'
				method_file_location = method_obj.filename();
				autocomplete_list.append((method_str_to_append + '\t' + method_file_location,method_str_to_append)) 
		return autocomplete_list



class ParsingThread(threading.Thread):

	def __init__(self, collector, open_folder_arr, timeout_seconds):
		self.collector = collector
		self.timeout = timeout_seconds
		self.open_folder_arr = open_folder_arr
		threading.Thread.__init__(self)

	def get_javascript_files(self, dir_name, *args):
		self.fileList = []
		for file in os.listdir(dir_name):
			dirfile = os.path.join(dir_name, file)
			if os.path.isfile(dirfile):
				fileName, fileExtension = os.path.splitext(dirfile)
				if fileExtension == ".js" and ".min." not in fileName:
					self.fileList.append(dirfile)
			elif os.path.isdir(dirfile):
				self.fileList += self.get_javascript_files(dirfile, *args)
		return self.fileList

	def run(self):
		for folder in self.open_folder_arr:
			print(folder)
			jsfiles = self.get_javascript_files(folder)
			for file_name in jsfiles:
				file_name

	def stop(self):
		if self.isAlive():
			self._Thread__stop()


class SublimeRJSCollector(SublimeRJS, sublime_plugin.EventListener):

	_collector_thread = None

	def on_post_save(self, view):
		self.clear()
		open_folder_arr = view.window().folders()
		if self._collector_thread != None:
			self._collector_thread.stop()
		self._collector_thread = ParsingThread(self, open_folder_arr, 30)
		self._collector_thread.start()

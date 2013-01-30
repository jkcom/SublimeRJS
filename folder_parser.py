import threading
import os
import ntpath
import sublime_plugin


global _collector_thread
_collector_thread = None


def find(folder, fileName):
	print "Search for : " + fileName + " in " + folder
	global _collector_thread
	if _collector_thread != None:
		_collector_thread.stop()
	print "GOT HERE"
	_collector_thread = ParsingThread([], folder, 30)
	_collector_thread.start()
	return ""


class ParsingThread(threading.Thread):

	def __init__(self, collector, folder, timeout_seconds):
		self.collector = collector
		self.timeout = timeout_seconds
		self.folder = folder
		threading.Thread.__init__(self)

	def get_javascript_files(self, dir_name, *args):
		self.fileList = []
		for file in os.listdir(dir_name):
			dirfile = os.path.join(dir_name, file)
			if os.path.isfile(dirfile):
				fileName, fileExtension = os.path.splitext(dirfile)
				print fileName
				if fileExtension == ".js" and ".min." not in fileName:
					self.fileList.append(dirfile)
			elif os.path.isdir(dirfile):
				self.fileList += self.get_javascript_files(dirfile, *args)
		return self.fileList

	def run(self):
		print "RUN THREAD"
		jsfiles = self.get_javascript_files(self.folder)
		for file_name in jsfiles:
			file_name

	def stop(self):
		if self.isAlive():
			self._Thread__stop()



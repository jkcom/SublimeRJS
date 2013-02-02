import threading
import os
import ntpath
import Queue

global _collectorSingle_thread
_collectorSingle_thread = None

global foundCallback
global que
que = Queue.Queue()


def checkQue():
	global timer
	global que
	global foundCallback
	if que.empty():
		foundCallback(None)
	else:
		foundCallback(que.get())



def findFile(folder, fileName, callback):
	global foundCallback
	foundCallback = callback
	global _collectorSingle_thread
	global timer
	global que
	# stop old
	if _collectorSingle_thread != None:
		_collectorSingle_thread.stop()
	# start thread
	_collectorSingle_thread = ParsingForSingleThread([], folder, fileName, que, 30)
	_collectorSingle_thread.start()


class ParsingForSingleThread(threading.Thread):

	def __init__(self, collector, folder, fileName, que, timeout_seconds):
		self.que = que
		self.collector = collector
		self.timeout = timeout_seconds
		self.folder = folder
		self.fileName = fileName
		threading.Thread.__init__(self)

	def get_javascript_files(self, dir_name, fileToFind):
		for file in os.listdir(dir_name):
			dirfile = os.path.join(dir_name, file)
			if os.path.isfile(dirfile):
				if ntpath.basename(dirfile) == fileToFind:
					self.que.put(dirfile)
					break
			elif os.path.isdir(dirfile):
				self.get_javascript_files(dirfile, fileToFind)



	def run(self):
		self.get_javascript_files(self.folder, self.fileName)
		checkQue()

	def stop(self):
		if self.isAlive():
			self._Thread__stop()

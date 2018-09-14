import time
import logging

class Timer(object):
	def __init__(self, name, startDebugLevel = "DEBUG", endDebugLevel = "DEBUG"):
		self.name = name
		self.startDebugLevel = startDebugLevel
		self.endDebugLevel = endDebugLevel

	def __enter__(self):
		self.startTmstmp = time.time()
		msg = 'Timer ' + self.name + ": start."
		logging.debug(msg) if self.startDebugLevel == "DEBUG" else logging.info(msg)

	def __exit__(self, type, value, traceback):
		msg = 'Timer ' + self.name + ": " + str(round(time.time() - self.startTmstmp, 1)) + " sec."
		logging.debug(msg) if self.endDebugLevel == "DEBUG" else logging.info(msg)
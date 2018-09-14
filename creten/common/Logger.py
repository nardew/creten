import logging

class Logger(object):
	DEBUG_LEVEL = 1
	INFO_LEVEL = 2

	GLOB_LOG_LEVEL = INFO_LEVEL

	def __init__(self, logPrefix = None, logDebug = True, logInfo = True, logForceDebug = False):
		self.logPrefix = logPrefix + ' ' if logPrefix else ''
		self.logDebug = logDebug
		self.logInfo = logInfo
		self.logForceDebug = logForceDebug

	def error(self, msg):
		msg = self.logPrefix + str(msg)
		logging.info('ERROR ' + str(msg))

	def info(self, msg):
		if self.logInfo:
			msg = self.logPrefix + str(msg)
			logging.info(str(msg))

	def debug(self, msg):
		if (self.logDebug and Logger.GLOB_LOG_LEVEL == Logger.DEBUG_LEVEL) or self.logForceDebug:
			msg = self.logPrefix + str(msg)
			logging.info(str(msg))

	def init(self, logDebug = None, logInfo = None, logForceDebug = None):
		if logDebug is not None:
			self.logDebug = logDebug

		if logInfo is not None:
			self.logInfo = logInfo

		if logForceDebug is not None:
			self.logForceDebug = logForceDebug
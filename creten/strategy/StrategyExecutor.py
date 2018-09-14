from common.Logger import Logger

class StrategyExecutor(object):
	def __init__(self):
		self.strategies = []

		self.log = Logger()

	def addStrategy(self, strategy):
		self.strategies.append(strategy)

	def removeAllStrategies(self):
		self.strategies = []

	def execute(self, candle):
		self.log.debug('Processing candle: ' + str(candle))

		# TODO should catch exceptions otherwise one faulty strategy will break all the remaining ones
		for strategy in self.strategies:
			strategy.execute(candle)
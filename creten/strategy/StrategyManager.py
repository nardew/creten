from common.Logger import Logger

class StrategyExecutor(object):
	def __init__(self):
		self.strategies = []

		self.log = Logger()

	def addStrategy(self, strategy):
		self.strategies.append(strategy)

	def getStrategies(self):
		return self.strategies

	def execute(self, candle):
		self.log.debug('Processing candle: ' + str(candle))

		# TODO should catch exceptions otherwise one faulty strategy will break all the remaining ones
		for strategy in self.strategies:
			strategy.execute(candle)

class StrategyManager(object):
	def __init__(self):
		self.strategyExecutors = []

		self.log = Logger()

	def reset(self):
		self.strategyExecutors = []

	def addStrategyExecutor(self, strategyExecutor):
		self.strategyExecutors.append(strategyExecutor)

	def getStrategy(self, strategyExecId):
		for strategy in self.getStrategies():
			if strategy.getStrategyExecId() == strategyExecId:
				return strategy

	def getStrategies(self):
		for se in self.strategyExecutors:
			for s in se.getStrategies():
				yield s


from indicators.Indicator import Indicator
from indicators.EMA import EMA

class MACD(Indicator):
	def __init__(self, fastPeriod, slowPeriod, signalPeriod, timeSeries = None):
		super(MACD, self).__init__()

		self.fastPeriod = fastPeriod
		self.slowPeriod = slowPeriod
		self.signalPeriod = signalPeriod

		self.emaFast = EMA(fastPeriod)
		self.emaSlow = EMA(slowPeriod)
		self.signalLine = EMA(signalPeriod)
		self.macdLine = []

		self.addSubIndicator(self.emaFast)
		self.addSubIndicator(self.emaSlow)

		self.initialize(timeSeries)

	def _calculate(self):
		if len(self.emaFast) > 0 and len(self.emaSlow) > 0:
			self.macdLine.append(self.emaFast[-1] - self.emaSlow[-1])
			self.signalLine.addValue(self.macdLine[-1])

	def removeValue(self):
		super(MACD, self).removeValue()

		if len(self.macdLine) > 0:
			self.macdLine.pop(-1)
		self.signalLine.removeValue()

	def removeAll(self):
		super(MACD, self).removeAll()

		self.macdLine = []
		self.signalLine.removeAll()

	def getMACDLine(self):
		return self.macdLine

	def getSignalLine(self):
		return self.signalLine
from indicators.Indicator import Indicator
from indicators.SMA import SMA
from indicators.StdDev import StdDev
from indicators.ATR import ATR

class SFX(Indicator):
	def __init__(self, atrPeriod, stdDevPeriod, stdDevSmoothingPeriod, timeSeries = None):
		super(SFX, self).__init__()

		self.atrPeriod = atrPeriod
		self.stdDevPeriod = stdDevPeriod
		self.stdDevSmoothingPeriod = stdDevSmoothingPeriod

		self.atr = ATR(self.atrPeriod)
		self.stdDev = StdDev(self.stdDevPeriod)
		self.smaStdDev = []

		self.addSubIndicator(self.atr)
		self.addSubIndicator(self.stdDev)

		self.initialize(timeSeries)

	def _calculate(self):
		if len(self.stdDev) < self.stdDevSmoothingPeriod:
			return

		self.smaStdDev.append(sum(self.stdDev[-self.stdDevSmoothingPeriod:]) / float(self.stdDevSmoothingPeriod))


	def removeValue(self):
		super(SFX, self).removeValue()

		if len(self.smaStdDev) > 0:
			self.smaStdDev.pop(-1)

	def removeAll(self):
		super(SFX, self).removeAll()

		self.smaStdDev = []

	def getATR(self):
		return self.atr

	def getStdDev(self):
		return self.stdDev

	def getSMAStdDev(self):
		return self.smaStdDev
from indicators.Indicator import Indicator
from indicators.SMA import SMA
from indicators.StdDev import StdDev

class BB(Indicator):
	def __init__(self, period, stdDevMult, timeSeries = None):
		super(BB, self).__init__()

		self.period = period
		self.stdDevMult = stdDevMult

		self.stdDev = StdDev(self.period)
		self.cb = SMA(self.period)
		self.lb = []
		self.ub = []

		self.addSubIndicator(self.cb)
		self.addSubIndicator(self.stdDev)

		self.initialize(timeSeries)

	def _calculate(self):
		if len(self.timeSeries) < self.period:
			return

		stdDev = self.stdDev[-1]

		self.lb.append(self.cb[-1] - self.stdDevMult * stdDev)
		self.ub.append(self.cb[-1] + self.stdDevMult * stdDev)


	def removeValue(self):
		super(BB, self).removeValue()

		if len(self.ub) > 0:
			self.ub.pop(-1)

		if len(self.lb) > 0:
			self.lb.pop(-1)

	def removeAll(self):
		super(BB, self).removeAll()

		self.ub = []
		self.lb = []

	def getCentralBand(self):
		return self.cb

	def getUpperBand(self):
		return self.ub

	def getLowerBand(self):
		return self.lb
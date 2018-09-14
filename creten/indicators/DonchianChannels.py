from indicators.Indicator import Indicator

class DonchianChannels(Indicator):
	def __init__(self, period, timeSeries = None):
		super(DonchianChannels, self).__init__()

		self.period = period

		self.cb = []
		self.lb = []
		self.ub = []

		self.initialize(timeSeries)

	def _calculate(self):
		if len(self.timeSeries) < self.period:
			return

		maxHigh = max(self.timeSeries[-self.period:], key = lambda x: x.getHigh()).getHigh()
		minLow = min(self.timeSeries[-self.period:], key = lambda x: x.getLow()).getLow()

		self.cb.append((maxHigh + minLow) / 2.0)
		self.lb.append(maxHigh)
		self.ub.append(minLow)


	def removeValue(self):
		super(DonchianChannels, self).removeValue()

		if len(self.ub) > 0:
			self.ub.pop(-1)

		if len(self.lb) > 0:
			self.lb.pop(-1)

	def removeAll(self):
		super(DonchianChannels, self).removeAll()

		self.cb = []
		self.ub = []
		self.lb = []

	def getCentralBand(self):
		return self.cb

	def getUpperBand(self):
		return self.ub

	def getLowerBand(self):
		return self.lb
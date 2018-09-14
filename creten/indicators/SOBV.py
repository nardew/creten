from indicators.Indicator import Indicator
from indicators.OBV import OBV

class SOBV(Indicator):
	def __init__(self, period, timeSeries = None):
		super(SOBV, self).__init__()

		self.period = period

		self.obv = OBV()
		self.addSubIndicator(self.obv)

		self.maObv = []

		self.initialize(timeSeries)

	def _calculate(self):
		if len(self.obv) < self.period:
			return

		self.maObv.append(sum(self.obv[-self.period:]) / float(self.period))

	def removeValue(self):
		super(SOBV, self).removeValue()

		if len(self.maObv) > 0:
			self.maObv.pop(-1)

	def removeAll(self):
		super(SOBV, self).removeAll()

		self.maObv = []

	def getOBV(self):
		return self.obv

	def getSOBV(self):
		return self.maObv
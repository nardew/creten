from math import sqrt
from indicators.SingleValueIndicator import SingleValueIndicator
from indicators.WMA import WMA

class HMA(SingleValueIndicator):
	def __init__(self, period, timeSeries = None):
		super(HMA, self).__init__()

		self.period = period

		self.wma = WMA(period)
		self.wma2 = WMA(period / 2)
		self.hma = WMA(int(sqrt(period)))

		self.addSubIndicator(self.wma)
		self.addSubIndicator(self.wma2)

		self.initialize(timeSeries)

	def _calculate(self):
		if len(self.wma) < sqrt(self.period):
			return

		self.hma.addValue(2.0 * self.wma2[-1] - self.wma[-1])

		if len(self.hma) < 1:
			return

		self.values.append(self.hma[-1])

	def removeValue(self):
		super(HMA, self).removeValue()

		self.hma.removeValue()

	def removeAll(self):
		super(HMA, self).removeAll()

		self.hma.removeAll()
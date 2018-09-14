from indicators.SingleValueIndicator import SingleValueIndicator
from indicators.SMA import SMA

class ATR(SingleValueIndicator):
	def __init__(self, period, timeSeries = None):
		super(ATR, self).__init__()

		self.period = period
		self.tr = []

		self.initialize(timeSeries)

	def _calculate(self):
		if len(self.timeSeries) == 1:
			self.tr.append(self.timeSeries[-1].getHigh() - self.timeSeries[-1].getLow())
		else:
			self.tr.append(max(
				self.timeSeries[-1].getHigh() - self.timeSeries[-1].getLow(),
				abs(self.timeSeries[-1].getHigh() - self.timeSeries[-2].getClose()),
				abs(self.timeSeries[-1].getLow() - self.timeSeries[-2].getClose()),
			))

			if len(self.timeSeries) == self.period:
				self.values.append(sum(self.tr) / self.period)
			elif len(self.timeSeries) > self.period:
				self.values.append((self.values[-1] * (self.period - 1) + self.tr[-1]) / self.period)

	def removeValue(self):
		super(ATR, self).removeValue()

		if len(self.tr) > 0:
			self.tr.pop(-1)

	def removeAll(self):
		super(ATR, self).removeAll()

		self.tr = []
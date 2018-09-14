from indicators.SingleValueIndicator import SingleValueIndicator
from math import sqrt

class StdDev(SingleValueIndicator):
	def __init__(self, period, timeSeries = None):
		super(StdDev, self).__init__()

		self.period = period

		self.initialize(timeSeries)

	def _calculate(self):
		if len(self.timeSeries) < self.period:
			return

		mean = sum(self.timeSeries[-self.period:]) / self.period
		self.values.append(sqrt(sum([(item - mean)**2 for item in self.timeSeries[-self.period:]]) / self.period))
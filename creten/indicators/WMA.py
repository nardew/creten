from indicators.SingleValueIndicator import SingleValueIndicator

class WMA(SingleValueIndicator):
	def __init__(self, period, timeSeries = None):
		super(WMA, self).__init__()

		self.period = int(period)

		self.denomSum = period * (period + 1) / 2.0

		self.initialize(timeSeries)

	def _calculate(self):
		if len(self.timeSeries) < self.period:
			return
		else:
			s = 0.0
			for i in range(self.period, 0, -1):
				index = len(self.timeSeries) - self.period + i - 1 # decreases from end of array with increasing i
				s += self.timeSeries[index] * i

			self.values.append(s / self.denomSum)
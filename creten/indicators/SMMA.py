from indicators.SingleValueIndicator import SingleValueIndicator

class SMMA(SingleValueIndicator):
	def __init__(self, period, timeSeries = None):
		super(SMMA, self).__init__()

		self.period = period

		self.initialize(timeSeries)

	def _calculate(self):
		if len(self.timeSeries) < self.period:
			return
		elif len(self.timeSeries) == self.period:
			self.values.append(float(sum(self.timeSeries)) / self.period)
		else:
			self.values.append((self.values[-1] * (self.period - 1) + self.timeSeries[-1]) / self.period)
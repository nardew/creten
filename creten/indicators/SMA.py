from indicators.SingleValueIndicator import SingleValueIndicator

class SMA(SingleValueIndicator):
	def __init__(self, period, timeSeries = None):
		super(SMA, self).__init__()

		self.period = period

		self.initialize(timeSeries)

	def _calculate(self):
		if len(self.timeSeries) < self.period:
			return
		else:
			self.values.append(float(sum(self.timeSeries[len(self.timeSeries) - self.period:len(self.timeSeries)])) / self.period)
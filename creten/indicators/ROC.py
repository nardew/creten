from indicators.SingleValueIndicator import SingleValueIndicator

class ROC(SingleValueIndicator):
	def __init__(self, period, timeSeries = None):
		super(ROC, self).__init__()

		self.period = period

		self.initialize(timeSeries)

	def _calculate(self):
		if len(self.timeSeries) < self.period + 1:
			return
		else:
			self.values.append(100.0 * (self.timeSeries[-1] - self.timeSeries[-self.period - 1]) / self.timeSeries[-self.period - 1])
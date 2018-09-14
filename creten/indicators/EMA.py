from indicators.SingleValueIndicator import SingleValueIndicator
from indicators.SMA import SMA

class EMA(SingleValueIndicator):
	def __init__(self, period, timeSeries = None):
		super(EMA, self).__init__()

		self.period = period

		self.initialize(timeSeries)

	def _calculate(self):
		if len(self.timeSeries) < self.period:
			return
		elif len(self.timeSeries) == self.period:
			init = SMA(self.period, self.timeSeries[:self.period])
			self.values.append(init.getValues()[0])
		else:
			mult = 2.0 / (self.period + 1.0)

			self.values.append(float(mult * self.timeSeries[-1] + (1.0 - mult) * self.values[-1]))


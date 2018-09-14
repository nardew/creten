from indicators.SingleValueIndicator import SingleValueIndicator
from indicators.EMA import EMA

class DEMA(SingleValueIndicator):
	def __init__(self, period, timeSeries = None):
		super(DEMA, self).__init__()

		self.period = period

		self.ema = EMA(period)
		self.addSubIndicator(self.ema)

		self.emaEma = EMA(period)

		self.initialize(timeSeries)

	def _calculate(self):
		if len(self.ema) < 1:
			return

		self.emaEma.addValue(self.ema[-1])

		if len(self.emaEma) < 1:
			return

		self.values.append(2.0 * self.ema[-1] - self.emaEma[-1])

	def removeValue(self):
		super(DEMA, self).removeValue()

		self.emaEma.removeValue()

	def removeAll(self):
		super(DEMA, self).removeAll()

		self.emaEma.removeAll()
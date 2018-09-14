from indicators.SingleValueIndicator import SingleValueIndicator
from indicators.EMA import EMA

class TEMA(SingleValueIndicator):
	def __init__(self, period, timeSeries = None):
		super(TEMA, self).__init__()

		self.period = period

		self.ema = EMA(period)
		self.addSubIndicator(self.ema)

		self.emaEma = EMA(period)
		self.emaEmaEma = EMA(period)

		self.initialize(timeSeries)

	def _calculate(self):
		if len(self.ema) < 1:
			return

		self.emaEma.addValue(self.ema[-1])

		if len(self.emaEma) < 1:
			return

		self.emaEmaEma.addValue(self.emaEma[-1])

		if len(self.emaEmaEma) < 1:
			return

		self.values.append(3.0 * self.ema[-1] - 3.0 * self.emaEma[-1] + self.emaEmaEma[-1])

	def removeValue(self):
		super(TEMA, self).removeValue()

		self.emaEma.removeValue()
		self.emaEmaEma.removeValue()

	def removeAll(self):
		super(TEMA, self).removeAll()

		self.emaEma.removeAll()
		self.emaEmaEma.removeAll()
from indicators.SingleValueIndicator import SingleValueIndicator
from indicators.EMA import EMA

class MassIndex(SingleValueIndicator):
	def __init__(self, emaPeriod, emaEmaPeriod, emaRatioPeriod, timeSeries = None):
		super(MassIndex, self).__init__()

		self.emaPeriod = emaPeriod
		self.emaEmaPeriod = emaEmaPeriod
		self.emaRatioPeriod = emaRatioPeriod

		self.ema = EMA(emaPeriod)
		self.emaEma = EMA(emaEmaPeriod)
		self.emaRatio = []

		self.initialize(timeSeries)

	def _calculate(self):
		self.ema.addValue(self.timeSeries[-1].getHigh() - self.timeSeries[-1].getLow())

		if len(self.ema) < 1:
			return

		self.emaEma.addValue(self.ema[-1])

		if len(self.emaEma) < 1:
			return

		self.emaRatio.append(self.ema[-1] / float(self.emaEma[-1]))

		if len(self.emaRatio) < self.emaRatioPeriod:
			return

		self.values.append(sum(self.emaRatio[-self.emaRatioPeriod:]))

	def removeValue(self):
		super(MassIndex, self).removeValue()

		self.ema.removeValue()
		self.emaEma.removeValue()
		if len(self.emaRatio) > 1:
			self.emaRatio.pop(-1)

	def removeAll(self):
		super(MassIndex, self).removeAll()

		self.ema.removeAll()
		self.emaEma.removeAll()
		self.emaRatio = []
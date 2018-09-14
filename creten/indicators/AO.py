from indicators.SingleValueIndicator import SingleValueIndicator
from indicators.SMA import SMA

class AO(SingleValueIndicator):
	def __init__(self, periodFast, periodSlow, timeSeries = None):
		super(AO, self).__init__()

		self.periodFast = periodFast
		self.periodSlow = periodSlow

		self.smaFast = SMA(periodFast)
		self.smaSlow = SMA(periodSlow)

		self.initialize(timeSeries)

	def _calculate(self):
		candle = self.timeSeries[-1]
		median = (candle.getHigh() + candle.getLow()) / 2.0

		self.smaFast.addValue(median)
		self.smaSlow.addValue(median)

		if len(self.smaFast) < 1 or len(self.smaSlow) < 1:
			return

		self.values.append(self.smaFast[-1] - self.smaSlow[-1])

	def removeValue(self):
		super(AO, self).removeValue()

		self.smaFast.removeValue()
		self.smaSlow.removeValue()

	def removeAll(self):
		super(AO, self).removeAll()

		self.smaFast.removeAll()
		self.smaSlow.removeAll()
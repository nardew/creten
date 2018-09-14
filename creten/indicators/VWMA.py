from indicators.SingleValueIndicator import SingleValueIndicator

class VWMA(SingleValueIndicator):
	def __init__(self, period, timeSeries = None):
		super(VWMA, self).__init__()

		self.period = period

		self.initialize(timeSeries)

	def _calculate(self):
		if len(self.timeSeries) < self.period:
			return
		else:
			s = 0.0
			v = 0.0
			for candle in self.timeSeries[-self.period:]:
				s += candle.getClose() * candle.getVolume()
				v += candle.getVolume()

			self.values.append(s / v)
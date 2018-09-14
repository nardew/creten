from indicators.SingleValueIndicator import SingleValueIndicator

class OBV(SingleValueIndicator):
	def __init__(self, timeSeries = None):
		super(OBV, self).__init__()

		self.initialize(timeSeries)

	def _calculate(self):
		if len(self.timeSeries) == 1:
			self.values.append(self.timeSeries[0].getVolume())
		else:
			candle = self.timeSeries[-1]
			prevCandle = self.timeSeries[-2]

			if candle.getClose() == prevCandle.getClose():
				self.values.append(self.values[-1])
			elif candle.getClose() > prevCandle.getClose():
				self.values.append(self.values[-1] + candle.getVolume())
			else:
				self.values.append(self.values[-1] - candle.getVolume())
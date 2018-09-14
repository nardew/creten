from indicators.Indicator import Indicator

class Stoch(Indicator):
	def __init__(self, period, smoothingPeriod, timeSeries):
		super(Stoch, self).__init__()

		self.period = period
		self.smoothingPeriod = smoothingPeriod
		self.valuesK = []
		self.valuesD = []

		self.initialize(timeSeries)

	def _calculate(self):
		if len(self.timeSeries) < self.period:
			return

		recentTimeSeries = self.timeSeries[-1 * self.period:]

		highs = [candle.getHigh() for candle in recentTimeSeries]
		lows = [candle.getLow() for candle in recentTimeSeries]

		maxHigh = max(highs)
		minLow = min(lows)

		if maxHigh == minLow:
			k = 100.0
		else:
			k = 100.0 * (self.timeSeries[-1].getClose() - minLow) / (maxHigh - minLow)

		self.valuesK.append(k)

		if len(self.valuesK) >= self.smoothingPeriod:
			self.valuesD.append(float(sum(self.valuesK[-1 * self.smoothingPeriod:])) / self.smoothingPeriod)

	def removeValue(self):
		super(Stoch, self).removeValue()

		if len(self.valuesK) > 0:
			self.valuesK.pop(-1)

		if len(self.valuesD) > 0:
			self.valuesD.pop(-1)

	def removeAll(self):
		super(Stoch, self).removeAll()

		self.valuesK = []
		self.valuesD = []

	def getValuesK(self):
		return self.valuesK

	def getValuesD(self):
		return self.valuesD
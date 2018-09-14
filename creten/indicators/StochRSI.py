from indicators.Indicator import Indicator
from indicators.RSI import RSI

class StochRSI(Indicator):
	def __init__(self, rsiPeriod, stochPeriod, smoothingPeriodK, smoothingPeriodD, timeSeries = None):
		super(StochRSI, self).__init__()

		self.stochPeriod = stochPeriod
		self.smoothingPeriodK = smoothingPeriodK
		self.smoothingPeriodD = smoothingPeriodD
		self.valuesK = []
		self.valuesSlowK = []
		self.valuesD = []
		self.rsi = RSI(rsiPeriod)

		self.addSubIndicator(self.rsi)

		self.initialize(timeSeries)

	def _calculate(self):

		if len(self.rsi.getValues()) < self.stochPeriod:
			return

		recentRsi = self.rsi[-1 * self.stochPeriod:]

		maxHigh = max(recentRsi)
		minLow = min(recentRsi)

		if maxHigh == minLow:
			k = 100.0
		else:
			k = 100.0 * (self.rsi[-1] - minLow) / (maxHigh - minLow)

		self.valuesK.append(k)

		if len(self.valuesK) >= self.smoothingPeriodK:
			self.valuesSlowK.append(float(sum(self.valuesK[-1 * self.smoothingPeriodK:])) / self.smoothingPeriodK)

		if len(self.valuesSlowK) >= self.smoothingPeriodD:
			self.valuesD.append(float(sum(self.valuesSlowK[-1 * self.smoothingPeriodD:])) / self.smoothingPeriodD)

	def removeValue(self):
		super(StochRSI, self).removeValue()

		if len(self.valuesK) > 0:
			self.valuesK.pop(-1)

		if len(self.valuesSlowK) > 0:
			self.valuesSlowK.pop(-1)

		if len(self.valuesD) > 0:
			self.valuesD.pop(-1)

	def removeAll(self):
		super(StochRSI, self).removeAll()

		self.valuesK = []
		self.valuesSlowK = []
		self.valuesD = []

	def getValuesK(self):
		return self.valuesK

	def getValuesSlowK(self):
		return self.valuesSlowK

	def getValuesD(self):
		return self.valuesD
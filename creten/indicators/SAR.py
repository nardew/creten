from indicators.Indicator import Indicator

class SARValue:
	UP = 1
	DOWN = 2

	def __init__(self, value, trend, ep, accelFactor):
		self.value = value
		self.trend = trend
		self.ep = ep
		self.accelFactor = accelFactor

	def getValue(self):
		return self.value

	def getTrend(self):
		return self.trend

class SAR(Indicator):
	SAR_INIT_LEN = 5

	def __init__(self, initAccelFactor, accelFactorInc, maxAccelFactor, timeSeries = None):
		super(SAR, self).__init__()

		self.initAccelFactor = initAccelFactor
		self.accelFactorInc = accelFactorInc
		self.maxAccelFactor = maxAccelFactor

		self.sar = []

		self.initialize(timeSeries)

	def _calculate(self):
		if len(self.timeSeries) < SAR.SAR_INIT_LEN:
			return

		if len(self.sar) == 0:
			minLow = min(self.timeSeries[-SAR.SAR_INIT_LEN:], key = lambda x: x.getLow()).getLow()
			maxHigh = max(self.timeSeries[-SAR.SAR_INIT_LEN:], key = lambda x: x.getHigh()).getHigh()

			self.sar.append(SARValue(minLow, SARValue.UP, maxHigh, self.initAccelFactor))
		else:
			lastSar = self.sar[-1]

			newSarVal = lastSar.value + lastSar.accelFactor * (lastSar.ep - lastSar.value)
			newTrend = lastSar.trend
			newEp = lastSar.ep
			newAccelFactor = lastSar.accelFactor

			# if new SAR overlaps last lows/highs (depending on the trend), cut it at that value
			if lastSar.trend == SARValue.UP and newSarVal > min(self.timeSeries[-2].getLow(), self.timeSeries[-3].getLow()):
				newSarVal = min(self.timeSeries[-2].getLow(), self.timeSeries[-3].getLow())
			elif lastSar.trend == SARValue.DOWN and newSarVal < max(self.timeSeries[-2].getHigh(), self.timeSeries[-3].getHigh()):
				newSarVal = max(self.timeSeries[-2].getHigh(), self.timeSeries[-3].getHigh())

			# update extreme point
			if lastSar.trend == SARValue.UP and self.timeSeries[-1].getHigh() > lastSar.ep:
				newEp = self.timeSeries[-1].getHigh()
			elif lastSar.trend == SARValue.DOWN and self.timeSeries[-1].getLow() < lastSar.ep:
				newEp = self.timeSeries[-1].getLow()

			# if extreme point was updated, increase acceleration factor
			if newEp != lastSar.ep:
				newAccelFactor = newAccelFactor + self.accelFactorInc
				if newAccelFactor > self.maxAccelFactor:
					newAccelFactor = self.maxAccelFactor

			# check if trend is reversed and initialize new initial values
			if lastSar.trend == SARValue.UP and newSarVal > self.timeSeries[-1].getLow():
				newSarVal = max(lastSar.ep, self.timeSeries[-1].getHigh())
				newEp = self.timeSeries[-1].getLow()
				newTrend = SARValue.DOWN
				newAccelFactor = self.initAccelFactor
			elif lastSar.trend == SARValue.DOWN and newSarVal < self.timeSeries[-1].getHigh():
				newSarVal = min(lastSar.ep, self.timeSeries[-1].getLow())
				newEp = self.timeSeries[-1].getHigh()
				newTrend = SARValue.UP
				newAccelFactor = self.initAccelFactor

			self.sar.append(SARValue(newSarVal, newTrend, newEp, newAccelFactor))

	def removeValue(self):
		super(SAR, self).removeValue()

		if len(self.sar) > 0:
			self.sar.pop(-1)

	def removeAll(self):
		super(SAR, self).removeAll()

		self.sar = []

	def getSAR(self):
		return self.sar
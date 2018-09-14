from indicators.Indicator import Indicator

class Ichimoku(Indicator):
	def __init__(self, kijunPeriod, tenkanPeriod, chikouLagPeriod, senkouSlowPeriod, senkouLookUpPeriod, timeSeries):
		super(Ichimoku, self).__init__()

		self.kijunPeriod = kijunPeriod
		self.tenkanPeriod = tenkanPeriod
		self.chikouLagPeriod = chikouLagPeriod
		self.senkouLookUpPeriod = senkouLookUpPeriod
		self.senkouSlowPeriod = senkouSlowPeriod

		self.baseLine = []              # Kijun Sen
		self.conversionLine = []        # Tenkan Sen
		self.laggingLine = []           # Chikou Span
		self.cloudFastLine = []         # Senkou Span
		self.cloudSlowLine = []         # Senkou Span

		self.initialize(timeSeries)

	def _calculate(self):
		if len(self.timeSeries) >= self.kijunPeriod:
			maxHigh = max(self.timeSeries[-self.kijunPeriod:], key = lambda x: x.getHigh()).getHigh()
			minLow = min(self.timeSeries[-self.kijunPeriod:], key = lambda x: x.getLow()).getLow()

			self.baseLine.append((maxHigh + minLow) / 2.0)

		if len(self.timeSeries) >= self.tenkanPeriod:
			maxHigh = max(self.timeSeries[-self.tenkanPeriod:], key = lambda x: x.getHigh()).getHigh()
			minLow = min(self.timeSeries[-self.tenkanPeriod:], key = lambda x: x.getLow()).getLow()

			self.conversionLine.append((maxHigh + minLow) / 2.0)

		if len(self.timeSeries) >= self.chikouLagPeriod:
			self.laggingLine.append(self.timeSeries[-1].getClose())

		if len(self.baseLine) >= self.senkouLookUpPeriod + 1and len(self.conversionLine) >= self.senkouLookUpPeriod + 1:
			self.cloudFastLine.append((self.baseLine[-self.senkouLookUpPeriod - 1] + self.conversionLine[-self.senkouLookUpPeriod - 1]) / 2.0)

		if len(self.timeSeries) >= self.senkouSlowPeriod + self.senkouLookUpPeriod + 1:
			maxHigh = max(self.timeSeries[-self.senkouSlowPeriod - self.senkouLookUpPeriod - 1:-self.senkouLookUpPeriod - 1], key = lambda x: x.getHigh()).getHigh()
			minLow = min(self.timeSeries[-self.senkouSlowPeriod - self.senkouLookUpPeriod - 1:-self.senkouLookUpPeriod - 1], key = lambda x: x.getLow()).getLow()

			self.cloudSlowLine.append((maxHigh + minLow) / 2.0)

	def removeValue(self):
		super(Ichimoku, self).removeValue()

		if len(self.baseLine) > 0:
			self.baseLine.pop(-1)

		if len(self.conversionLine) > 0:
			self.conversionLine.pop(-1)

		if len(self.laggingLine) > 0:
			self.laggingLine.pop(-1)

		if len(self.cloudFastLine) > 0:
			self.cloudFastLine.pop(-1)

		if len(self.cloudSlowLine) > 0:
			self.cloudSlowLine.pop(-1)

	def removeAll(self):
		super(Ichimoku, self).removeAll()

		self.baseLine = []
		self.conversionLine = []
		self.laggingLine = []
		self.cloudFastLine = []
		self.cloudSlowLine = []

	def getBaseLine(self):
		return self.baseLine

	def getConversionLine(self):
		return self.conversionLine

	def getLaggingLine(self):
		return self.laggingLine

	def getCloudSlowLine(self):
		return self.cloudSlowLine

	def getCloudFastLine(self):
		return self.cloudFastLine
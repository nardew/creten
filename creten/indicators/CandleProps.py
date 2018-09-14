from indicators.Indicator import Indicator

class CandleProps(Indicator):
	def __init__(self, timeSeries = None):
		super(CandleProps, self).__init__()

		self.bodyPerc = []

		self.initialize(timeSeries)

	def _calculate(self):
		if (self.timeSeries[-1].getHigh() - self.timeSeries[-1].getLow()) != 0:
			bodyPerc = abs(100.0 * (float(self.timeSeries[-1].getClose() - self.timeSeries[-1].getOpen())) / (self.timeSeries[-1].getHigh() - self.timeSeries[-1].getLow()))
		else:
			bodyPerc = 0.0

		self.bodyPerc.append(bodyPerc)

	def removeValue(self):
		super(CandleProps, self).removeValue()

		if len(self.bodyPerc) > 0:
			self.bodyPerc.pop(-1)

	def removeAll(self):
		super(CandleProps, self).removeAll()

		self.bodyPerc = []

	def getBodyPerc(self):
		return self.bodyPerc
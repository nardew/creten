from indicators.SingleValueIndicator import SingleValueIndicator
from indicators.SMA import SMA

class UO(SingleValueIndicator):
	def __init__(self, periodFast, periodMid, periodSlow, timeSeries = None):
		super(UO, self).__init__()

		self.periodFast = periodFast
		self.periodMid = periodMid
		self.periodSlow = periodSlow

		self.buyPress = []
		self.trueRange = []

		self.initialize(timeSeries)

	def _calculate(self):
		if len(self.timeSeries) < 2:
			return

		self.buyPress.append(self.timeSeries[-1].getClose() - min(self.timeSeries[-1].getLow(), self.timeSeries[-2].getClose()))
		self.trueRange.append(max(self.timeSeries[-1].getHigh(), self.timeSeries[-2].getClose()) - min(self.timeSeries[-1].getLow(), self.timeSeries[-2].getClose()))

		if len(self.buyPress) < self.periodSlow:
			return

		avgFast = sum(self.buyPress[-self.periodFast:]) / float(sum(self.trueRange[-self.periodFast:]))
		avgMid = sum(self.buyPress[-self.periodMid:]) / float(sum(self.trueRange[-self.periodMid:]))
		avgSlow = sum(self.buyPress[-self.periodSlow:]) / float(sum(self.trueRange[-self.periodSlow:]))

		self.values.append(100.0 * (4.0 * avgFast + 2.0 * avgMid + avgSlow) / 7.0)

	def removeValue(self):
		super(UO, self).removeValue()

		if len(self.buyPress) > 1:
			self.buyPress.pop(-1)
		if len(self.trueRange) > 1:
			self.trueRange.pop(-1)

	def removeAll(self):
		super(UO, self).removeAll()

		self.buyPress = []
		self.trueRange = []
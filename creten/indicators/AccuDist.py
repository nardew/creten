from indicators.SingleValueIndicator import SingleValueIndicator
from indicators.SMA import SMA

class AccuDist(SingleValueIndicator):
	def __init__(self, timeSeries = None):
		super(AccuDist, self).__init__()

		self.initialize(timeSeries)

	def _calculate(self):
		if len(self.timeSeries) < 1:
			return

		candle = self.timeSeries[-1]

		mfm = ((candle.getClose() - candle.getLow()) - (candle.getHigh() - candle.getClose())) / float(candle.getHigh() - candle.getLow())
		mfv = mfm * candle.getVolume()

		if len(self.values) == 0:
			self.values.append(mfv)
		else:
			self.values.append(self.values[-1] + mfv)
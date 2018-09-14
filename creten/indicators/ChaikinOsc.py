from indicators.SingleValueIndicator import SingleValueIndicator
from indicators.EMA import EMA
from indicators.AccuDist import AccuDist

class ChaikinOsc(SingleValueIndicator):
	def __init__(self, periodFast, periodSlow, timeSeries = None):
		super(ChaikinOsc, self).__init__()

		self.periodFast = periodFast
		self.periodSlow = periodSlow

		self.accuDist = AccuDist()

		self.emaFast = EMA(periodFast)
		self.emaSlow = EMA(periodSlow)

		self.addSubIndicator(self.accuDist)

		self.initialize(timeSeries)

	def _calculate(self):
		if len(self.accuDist) < 1:
			return

		self.emaFast.addValue(self.accuDist[-1])
		self.emaSlow.addValue(self.accuDist[-1])

		if len(self.emaFast) < 1 or len(self.emaSlow) < 1:
			return

		self.values.append(self.emaFast[-1] - self.emaSlow[-1])

	def removeValue(self):
		super(ChaikinOsc, self).removeValue()

		self.emaFast.removeValue()
		self.emaSlow.removeValue()

	def removeAll(self):
		super(ChaikinOsc, self).removeAll()

		self.emaFast.removeAll()
		self.emaSlow.removeAll()
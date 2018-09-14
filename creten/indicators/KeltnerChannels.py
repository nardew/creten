from indicators.Indicator import Indicator
from indicators.EMA import EMA
from indicators.ATR import ATR

class KeltnerChannels(Indicator):
	def __init__(self, maPeriod, atrPeriod, atrMultUp, atrMultDown, timeSeries = None):
		super(KeltnerChannels, self).__init__()

		self.maPeriod = maPeriod
		self.atrPeriod = atrPeriod
		self.atrMultUp = atrMultUp
		self.atrMultDown = atrMultDown

		self.atr = ATR(self.atrPeriod)
		self.cb = EMA(self.maPeriod)
		self.lb = []
		self.ub = []

		self.addSubIndicator(self.cb)
		self.addSubIndicator(self.atr)

		self.initialize(timeSeries)

	def _calculate(self):
		if len(self.cb) < 1 or len(self.atr) < 1:
			return

		atr = self.atr[-1]

		self.lb.append(self.cb[-1] - self.atrMultDown * atr)
		self.ub.append(self.cb[-1] + self.atrMultUp * atr)


	def removeValue(self):
		super(KeltnerChannels, self).removeValue()

		if len(self.ub) > 0:
			self.ub.pop(-1)

		if len(self.lb) > 0:
			self.lb.pop(-1)

	def removeAll(self):
		super(KeltnerChannels, self).removeAll()

		self.ub = []
		self.lb = []

	def getCentralBand(self):
		return self.cb

	def getUpperBand(self):
		return self.ub

	def getLowerBand(self):
		return self.lb
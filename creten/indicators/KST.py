from indicators.Indicator import Indicator
from indicators.SMA import SMA
from indicators.ROC import ROC

class KST(Indicator):
	def __init__(self, roc1Period, roc1MAPeriod, roc2Period, roc2MAPeriod, roc3Period, roc3MAPeriod, roc4Period, roc4MAPeriod, signalPeriod, timeSeries = None):
		super(KST, self).__init__()

		self.roc1Period = roc1Period
		self.roc1MAPeriod = roc1MAPeriod
		self.roc2Period = roc2Period
		self.roc2MAPeriod = roc2MAPeriod
		self.roc3Period = roc3Period
		self.roc3MAPeriod = roc3MAPeriod
		self.roc4Period = roc4Period
		self.roc4MAPeriod = roc4MAPeriod
		self.signalPeriod = signalPeriod

		self.roc1 = ROC(roc1Period)
		self.roc2 = ROC(roc2Period)
		self.roc3 = ROC(roc3Period)
		self.roc4 = ROC(roc4Period)

		self.roc1MA = SMA(roc1MAPeriod)
		self.roc2MA = SMA(roc2MAPeriod)
		self.roc3MA = SMA(roc3MAPeriod)
		self.roc4MA = SMA(roc4MAPeriod)
		self.kst = []
		self.signalLine = SMA(signalPeriod)

		self.addSubIndicator(self.roc1)
		self.addSubIndicator(self.roc2)
		self.addSubIndicator(self.roc3)
		self.addSubIndicator(self.roc4)

		self.initialize(timeSeries)

	def _calculate(self):
		if len(self.roc1) > 0:
			self.roc1MA.addValue(self.roc1[-1])
		if len(self.roc2) > 0:
			self.roc2MA.addValue(self.roc2[-1])
		if len(self.roc3) > 0:
			self.roc3MA.addValue(self.roc3[-1])
		if len(self.roc4) > 0:
			self.roc4MA.addValue(self.roc4[-1])

		if len(self.roc1MA) < 1 or len(self.roc2MA) < 1 or len(self.roc3MA) < 1 or len(self.roc4MA) < 1:
			return

		self.kst.append(1.0 * self.roc1MA[-1] + 2.0 * self.roc2MA[-1] + 3.0 * self.roc3MA[-1] + 4.0 * self.roc4MA[-1])

		if len(self.kst) < 1:
			return

		self.signalLine.addValue(self.kst[-1])

	def removeValue(self):
		super(KST, self).removeValue()

		if len(self.kst) > 0:
			self.kst.pop(-1)
		self.roc1MA.removeValue()
		self.roc2MA.removeValue()
		self.roc3MA.removeValue()
		self.roc4MA.removeValue()
		self.signalLine.removeValue()

	def removeAll(self):
		super(KST, self).removeAll()

		self.kst = []
		self.roc1MA.removeAll()
		self.roc2MA.removeAll()
		self.roc3MA.removeAll()
		self.roc4MA.removeAll()
		self.signalLine.removeAll()

	def getKST(self):
		return self.kst

	def getSignalLine(self):
		return self.signalLine
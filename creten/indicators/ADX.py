from indicators.Indicator import Indicator
from indicators.ATR import ATR

class ADX(Indicator):
	def __init__(self, periodDI, periodADX, timeSeries = None):
		super(ADX, self).__init__()

		self.periodDI = periodDI
		self.periodADX = periodADX

		self.atr = ATR(periodDI)
		self.addSubIndicator(self.atr)

		self.pDM = []
		self.nDM = []

		self.sPDM = []
		self.sNDM = []

		self.pDI = []
		self.nDI = []

		self.dmi = []

		self.adx = []

		self.initialize(timeSeries)

	def _calculate(self):
		if len(self.timeSeries) < 2:
			return

		cC = self.timeSeries[-1]
		pC = self.timeSeries[-2]

		if (cC.getHigh() - pC.getHigh() > pC.getLow() - cC.getLow() and cC.getHigh() - pC.getHigh() > 0):
			self.pDM.append(cC.getHigh() - pC.getHigh())
		else:
			self.pDM.append(0)

		if (pC.getLow() - cC.getLow() > cC.getHigh() - pC.getHigh() and pC.getLow() - cC.getLow() > 0):
			self.nDM.append(pC.getLow() - cC.getLow())
		else:
			self.nDM.append(0)

		if len(self.pDM) == self.periodDI:
			self.sPDM.append(sum(self.pDM[-self.periodDI:]) / float(self.periodDI))
			self.sNDM.append(sum(self.nDM[-self.periodDI:]) / float(self.periodDI))
		elif len(self.pDM) > self.periodDI:
			self.sPDM.append((self.sPDM[-1] * (self.periodDI - 1) + self.pDM[-1]) / float(self.periodDI))
			self.sNDM.append((self.sNDM[-1] * (self.periodDI - 1) + self.nDM[-1]) / float(self.periodDI))

			self.pDI.append(100.0 * self.sPDM[-1] / float(self.atr[-1]))
			self.nDI.append(100.0 * self.sNDM[-1] / float(self.atr[-1]))

			self.dmi.append(100.0 * float(abs(self.pDI[-1] - self.nDI[-1])) / (self.pDI[-1] + self.nDI[-1]))

			if len(self.dmi) == self.periodADX:
				self.adx.append(sum(self.dmi) / float(self.periodADX))
			elif len(self.dmi) > self.periodADX:
				self.adx.append((self.adx[-1] * (self.periodADX - 1) + self.dmi[-1]) / float(self.periodADX))

	def removeValue(self):
		super(ADX, self).removeValue()

		if len(self.pDM) > 0:
			self.pDM.pop(-1)

		if len(self.nDM) > 0:
			self.nDM.pop(-1)

		if len(self.pDI) > 0:
			self.pDI.pop(-1)

		if len(self.nDI) > 0:
			self.nDI.pop(-1)

		if len(self.sPDM) > 0:
			self.sPDM.pop(-1)

		if len(self.sNDM) > 0:
			self.sNDM.pop(-1)

		if len(self.dmi) > 0:
			self.dmi.pop(-1)

		if len(self.adx) > 0:
			self.adx.pop(-1)

	def removeAll(self):
		super(ADX, self).removeAll()

		self.pDM = []
		self.nDM = []
		self.pDI = []
		self.nDI = []
		self.sPDM = []
		self.sNDM = []
		self.dmi = []
		self.adx = []

	def getPlusDI(self):
		return self.pDI

	def getMinusDI(self):
		return self.nDI

	def getADX(self):
		return self.adx
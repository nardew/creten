from indicators.Indicator import Indicator

class HL(object):
	HIGH = 1
	LOW = 2

	def __init__(self, item, type):
		self.item = item
		self.type = type

class PivotsHL(Indicator):
	def __init__(self, highLeftDist, lowLeftDist, timeSeries = None):
		super(PivotsHL, self).__init__()

		self.highLeftDist = highLeftDist
		self.lowLeftDist = lowLeftDist

		self.pivots = []
		self.highPivots = []
		self.lowPivots = []

		self.initialize(timeSeries)

	def _calculate(self):
		if len(self.timeSeries) < 2:
			return

		valHigh = self.timeSeries[-2].getHigh()
		valLow = self.timeSeries[-2].getLow()
		maxHigh = max(self.timeSeries[-self.highLeftDist:-1], key=lambda x: x.getHigh()).getHigh()
		minLow = min(self.timeSeries[-self.lowLeftDist:-1], key=lambda x: x.getLow()).getLow()

		if valHigh >= maxHigh:
			if len(self.pivots) == 0 or self.pivots[-1].type == HL.LOW:
				self.pivots.append(HL(self.timeSeries[-2], HL.HIGH))
				self.highPivots.append(self.timeSeries[-2])
			elif valHigh >= self.pivots[-1].item.getHigh():
				self.pivots[-1] = HL(self.timeSeries[-2], HL.HIGH)
				self.highPivots[-1] = self.timeSeries[-2]
		elif valLow <= minLow:
			if len(self.pivots) == 0 or self.pivots[-1].type == HL.HIGH:
				self.pivots.append(HL(self.timeSeries[-2], HL.LOW))
				self.lowPivots.append(self.timeSeries[-2])
			elif valLow <= self.pivots[-1].item.getLow():
				self.pivots[-1] = HL(self.timeSeries[-2], HL.LOW)
				self.lowPivots[-1] = self.timeSeries[-2]

	def removeAll(self):
		super(PivotsHL, self).removeAll()

		self.pivots = []
		self.lowPivots = []
		self.highPivots = []

	def getPivots(self):
		return self.pivots

	def getLowPivots(self):
		return self.lowPivots

	def getHighPivots(self):
		return self.highPivots
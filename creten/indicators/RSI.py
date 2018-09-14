from indicators.SingleValueIndicator import SingleValueIndicator

class RSI(SingleValueIndicator):
	def __init__(self, period, timeSeries = None):
		super(RSI, self).__init__()

		self.period = period

		self.lastAvgGain = 0.0
		self.lastAvgLoss = 0.0
		self.prevLastAvgGain = 0.0
		self.prevLastAvgLoss = 0.0

		self.initialize(timeSeries)

	def _calculate(self):
		self.prevLastAvgGain = self.lastAvgGain
		self.prevLastAvgLoss = self.lastAvgLoss

		if len(self.timeSeries) < self.period + 1:
			return
		elif len(self.timeSeries) == self.period + 1:
			# calculate inital changes in price
			initChanges = [self.timeSeries[i] - self.timeSeries[i - 1] for i in range(1, self.period)]

			# initialize average gain and loss
			self.lastAvgGain = float(sum(initChanges[i] for i in range(len(initChanges)) if initChanges[i] > 0)) / (self.period - 1)
			self.lastAvgLoss = float(sum(-1 * initChanges[i] for i in range(len(initChanges)) if initChanges[i] < 0)) / (self.period - 1)

		change = self.timeSeries[-1] - self.timeSeries[-2]

		gain = change if change > 0 else 0.0
		loss = -1 * change if change < 0 else 0.0

		self.lastAvgGain = float(self.lastAvgGain * (self.period - 1) + gain) / self.period
		self.lastAvgLoss = float(self.lastAvgLoss * (self.period - 1) + loss) / self.period

		if self.lastAvgLoss == 0:
			rsi = 100.0
		else:
			rs = self.lastAvgGain / self.lastAvgLoss
			rsi = 100.0 - (100.0 / (1.0 + rs))

		self.values.append(rsi)

	def removeValue(self):
		super(RSI, self).removeValue()

		self.lastAvgGain = self.prevLastAvgGain
		self.lastAvgLoss = self.prevLastAvgLoss

	def removeAll(self):
		super(RSI, self).removeAll()

		self.lastAvgGain = 0.0
		self.lastAvgLoss = 0.0
		self.prevLastAvgGain = 0.0
		self.prevLastAvgLoss = 0.0
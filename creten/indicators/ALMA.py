from indicators.SingleValueIndicator import SingleValueIndicator
from math import exp

class ALMA(SingleValueIndicator):
	def __init__(self, window, offset, sigma, timeSeries = None):
		super(ALMA, self).__init__()

		self.window = window
		self.offset = offset
		self.sigma = sigma

		# calculate weights and normalisation factor (wSum)
		self.w = []
		self.wSum = 0.0
		s = self.window / float(self.sigma)
		m = int((self.window - 1) * self.offset)
		for i in range(0, self.window):
			self.w.append(exp(-1 * (i - m) * (i - m) / (2 * s * s)))
			self.wSum += self.w[-1]

		self.initialize(timeSeries)

	def _calculate(self):
		if len(self.timeSeries) < self.window:
			return

		alma = 0.0
		for i in range(0, self.window):
			alma += self.timeSeries[len(self.timeSeries) - self.window + i] * self.w[i]

		self.values.append(alma / self.wSum)

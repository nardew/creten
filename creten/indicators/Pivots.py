import datetime
from indicators.Indicator import Indicator
from collections import OrderedDict

class Pivots(Indicator):
	PIVOT_PERIOD_DAY = 1
	PIVOT_PERIOD_WEEK = 2

	PIVOT_TYPE_STANDARD = 1
	PIVOT_TYPE_FIBONACCI = 2
	PIVOT_TYPE_WOODIE = 3
	PIVOT_TYPE_DEMARK = 4
	PIVOT_TYPE_CAMARILLA = 5

	def __init__(self, pivotType, periodType, periodOffsetHour, timeSeries = None):
		super(Pivots, self).__init__()

		self.pivotType = pivotType
		self.periodType = periodType
		self.periodOffsetHour = periodOffsetHour

		self.high = OrderedDict()
		self.low = OrderedDict()
		self.close = OrderedDict()
		self.open = OrderedDict()

		self.pp = OrderedDict()
		self.s1 = OrderedDict()
		self.s2 = OrderedDict()
		self.s3 = OrderedDict()
		self.s4 = OrderedDict()
		self.r1 = OrderedDict()
		self.r2 = OrderedDict()
		self.r3 = OrderedDict()
		self.r4 = OrderedDict()

		self.initialize(timeSeries)

	def _getPeriodKeyFormat(self):
		if self.periodType == Pivots.PIVOT_PERIOD_DAY:
			return '%Y%m%d'
		elif self.periodType == Pivots.PIVOT_PERIOD_WEEK:
			return '%Y%W'
		else:
			return None

	def _calculate(self):
		candle = self.timeSeries[-1]

		periodKey = candle.getOpenTime().strftime(self._getPeriodKeyFormat())

		if not periodKey in self.open:
			# if it is first candle of this period, inititalize high, low and open
			self.high[periodKey] = candle.getHigh()
			self.low[periodKey] = candle.getLow()
			self.open[periodKey] = candle.getOpen()
		else:
			# always store the curent high and low of the period
			if candle.getHigh() > self.high[periodKey]:
				self.high[periodKey] = candle.getHigh()
			if candle.getLow() < self.low[periodKey]:
				self.low[periodKey] = candle.getLow()

		# store trailing close
		self.close[periodKey] = candle.getClose()
		
		currHigh = self.high[periodKey]
		currLow = self.low[periodKey]
		currOpen = self.open[periodKey]
		currClose = self.close[periodKey]
		
		if self.pivotType == Pivots.PIVOT_TYPE_STANDARD:
			self.pp[periodKey] = (currHigh + currLow + currClose) / 3.0

			self.s1[periodKey] = self.pp[periodKey] * 2.0 - currHigh
			self.s2[periodKey] = self.pp[periodKey] - (currHigh - currLow)
			self.s3[periodKey] = currLow - 2.0 * (currHigh - self.pp[periodKey])

			self.r1[periodKey] = self.pp[periodKey] * 2.0 - currLow
			self.r2[periodKey] = self.pp[periodKey] + (currHigh - currLow)
			self.r3[periodKey] = currHigh + 2.0 * (self.pp[periodKey] - currLow)
		elif self.pivotType == Pivots.PIVOT_TYPE_FIBONACCI:
			self.pp[periodKey] = (currHigh + currLow + currClose) / 3.0

			self.s1[periodKey] = self.pp[periodKey] - (currHigh - currLow) * 0.382
			self.s2[periodKey] = self.pp[periodKey] - (currHigh - currLow) * 0.618
			self.s3[periodKey] = self.pp[periodKey] - (currHigh - currLow) * 1.0

			self.r1[periodKey] = self.pp[periodKey] + (currHigh - currLow) * 0.382
			self.r2[periodKey] = self.pp[periodKey] + (currHigh - currLow) * 0.618
			self.r3[periodKey] = self.pp[periodKey] + (currHigh - currLow) * 1.0
		elif self.pivotType == Pivots.PIVOT_TYPE_WOODIE:
			self.pp[periodKey] = (currHigh + currLow + 2.0 * currClose) / 4.0

			self.s1[periodKey] = 2.0 * self.pp[periodKey] - currHigh
			self.s2[periodKey] = self.pp[periodKey] - (currHigh - currLow)
			self.s3[periodKey] = currLow - 2.0 * (currHigh - self.pp[periodKey])

			self.r1[periodKey] = 2.0 * self.pp[periodKey] - currLow
			self.r2[periodKey] = self.pp[periodKey] + (currHigh - currLow)
			self.r3[periodKey] = currHigh + 2.0 * (self.pp[periodKey] - currLow)
		elif self.pivotType == Pivots.PIVOT_TYPE_CAMARILLA:
			self.pp[periodKey] = (currHigh + currLow + currClose) / 3.0

			self.s1[periodKey] = currClose - (currHigh - currLow) * 1.1 / 12.0
			self.s2[periodKey] = currClose - (currHigh - currLow) * 1.1 / 6.0
			self.s3[periodKey] = currClose - (currHigh - currLow) * 1.1 / 4.0
			self.s4[periodKey] = currClose - (currHigh - currLow) * 1.1 / 2.0

			self.r1[periodKey] = currClose + (currHigh - currLow) * 1.1 / 12.0
			self.r2[periodKey] = currClose + (currHigh - currLow) * 1.1 / 6.0
			self.r3[periodKey] = currClose + (currHigh - currLow) * 1.1 / 4.0
			self.r4[periodKey] = currClose + (currHigh - currLow) * 1.1 / 2.0
		elif self.pivotType == Pivots.PIVOT_TYPE_DEMARK:
			if currClose < currOpen:
				x = currHigh + 2.0 * currLow + currClose
			elif currClose > currOpen:
				x = 2.0 * currHigh + currLow + currClose
			else:
				x = currHigh + currLow + 2.0 * currClose

			self.pp[periodKey] = x / 4.0

			self.s1[periodKey] = x / 2.0 - currHigh

			self.r1[periodKey] = x / 2.0 - currLow
		else:
			raise Exception()

	def getPP(self):
		if len(self.pp) > 1:
			return list(self.pp.values())[:-1]
		return None

	def getS(self, level):
		s = getattr(self, 's' + str(level))

		if len(s) > 1:
			return list(s.values())[:-1]
		return None

	def getR(self, level):
		r = getattr(self, 'r' + str(level))

		if len(r) > 1:
			return list(r.values())[:-1]
		return None

	def levelCrossedUp(self, candle, prevCandle):
		orderedLevels = [self.r4, self.r3, self.r2, self.r1, self.pp, self.s1, self.s2, self.s3, self.s4]

		for level in orderedLevels:
			level = level.values()
			if level and len(level) > 2:
				if candle.isGreen() and candle.getHigh() > level[-2] and candle.getLow() < level[-2]:
					return level[-2]
				elif candle.isGreen() and candle.getHigh() > level[-2] and candle.getLow() > level[-2] and prevCandle.getHigh() < level[-2]:
					return level[-2]

		return None
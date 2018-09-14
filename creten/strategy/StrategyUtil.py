from collections import Iterable

class StrategyUtil:
	@staticmethod
	def crossUp(l1, l2, preMidDelta = 0, postMinDelta = 0):
		return l1[-1] > l2[-1] and l1[-2] < l2[-2] and abs(l1[-2] - l2[-2]) >= preMidDelta and abs(l1[-1] - l2[-1]) >= postMinDelta

	@staticmethod
	def crossDown(l1, l2, preMidDelta = 0, postMinDelta = 0):
		return l1[-1] < l2[-1] and l1[-2] > l2[-2] and abs(l1[-2] - l2[-2]) >= preMidDelta and abs(
			l1[-1] - l2[-1]) >= postMinDelta

	@staticmethod
	def strictly_increasing(seq, count = None):
		if not isinstance(seq[0], list):
			seq = [seq]

		for s in seq:
			if count:
				tmpCount = count
			else:
				tmpCount = len(s)

			if not all(x < y for x, y in zip(s[-tmpCount:], s[-tmpCount+1:])):
				return False

		return True

	@staticmethod
	def increasing(seq, count = None):
		if not isinstance(seq[0], Iterable):
			seq = [seq]

		for s in seq:
			if count:
				tmpCount = count
			else:
				tmpCount = len(s)

			if not all(x <= y for x, y in zip(s[-tmpCount:], s[-tmpCount+1:])):
				return False

		return True

	@staticmethod
	def strictly_decreasing(seq, count = None):
		if not isinstance(seq[0], list):
			seq = [seq]

		for s in seq:
			if count:
				tmpCount = count
			else:
				tmpCount = len(s)

			if not all(x >= y for x, y in zip(s[-tmpCount:], s[-tmpCount+1:])):
				return False

		return True

	@staticmethod
	def decreasing(seq, count = None):
		if not isinstance(seq[0], list):
			seq = [seq]

		for s in seq:
			if count:
				tmpCount = count
			else:
				tmpCount = len(s)

			if not all(x > y for x, y in zip(s[-tmpCount:], s[-tmpCount+1:])):
				return False

		return True

	@staticmethod
	def getCandleIndicatorBearCrossing(candle, indValue):
		if candle.getHigh() < indValue:
			return candle.getOpen()
		elif candle.getUpperBody() < indValue:
			return candle.getOpen()
		elif candle.getUpperBody() > indValue and candle.getLowerBody() < indValue:
			if candle.isGreen():
				return candle.getOpen()
			else:
				return indValue
		else:
			return indValue
from db_managers.DbCodeMapper import IntervalMapper

class Candle(object):
	def __init__(self, baseAsset = None, quoteAsset = None, interval = None, openTime = None, open = None, high = None,
	             low = None, close = None, volume = None, closeTime = None, quoteAssetVolume = None, tradesNb = None,
	             takerBuyBaseAssetVol = None, takerBuyQuoteAssetVol = None, isClosing = None):
		self.baseAsset = baseAsset
		self.quoteAsset = quoteAsset
		self.interval = interval
		self.openTime = openTime
		self.open = float(open)
		self.high = float(high)
		self.low = float(low)
		self.close = float(close)
		self.volume = float(volume)
		self.closeTime = closeTime
		self.quoteAssetVolume = quoteAssetVolume
		self.tradesNb = int(tradesNb)
		self.takerBuyBaseAssetVol = takerBuyBaseAssetVol
		self.takerBuyQuoteAssetVol = takerBuyQuoteAssetVol
		self.isClosing = isClosing

	def getSymbol(self):
		return self.baseAsset + self.quoteAsset

	def getQuoteAsset(self):
		return self.quoteAsset

	def getBaseAsset(self):
		return self.baseAsset

	def getInterval(self):
		return self.interval

	def getOpenTime(self):
		return self.openTime

	def getCloseTime(self):
		return self.closeTime

	def getOpen(self):
		return self.open

	def setClose(self, close):
		self.close = close

	def getClose(self):
		return self.close

	def getHigh(self):
		return self.high

	def getLow(self):
		return self.low

	def getVolume(self):
		return self.volume

	def getIsClosing(self):
		return self.isClosing

	def getUpperBody(self):
		return max(self.open, self.close)

	def getLowerBody(self):
		return min(self.open, self.close)

	def isGreen(self):
		return self.close > self.open

	def __hash__(self):
		return hash((self.getSymbol(), self.openTime, self.closeTime))

	def __eq__(self, other):
		return (self.getSymbol(), self.openTime, self.closeTime) == (other.getSymbol(), other.openTime, other.closeTime)

	# Allow mathematical operations over candles. The operation uses closing price of the candle.
	def __radd__(self, other):
		return self.__add__(other)

	def __add__(self, other):
		if isinstance(other, Candle):
			return self.close + other.close
		else:
			return self.close + other

	def __sub__(self, other):
		if isinstance(other, Candle):
			return self.close - other.close
		else:
			return self.close - other

	def __rsub__(self, other):
		return other - self.close

	def __rmul__(self, other):
		return self.__mul__(other)

	def __mul__(self, other):
		if isinstance(other, Candle):
			return self.close * other.close
		else:
			return self.close * other

	# Python 3.x support
	def __rtruediv__(self, other):
		return other / float(self.close)

	# Python 3.x support
	def __truediv__(self, other):
		if isinstance(other, Candle):
			return self.close / float(other.close)
		else:
			return self.close / float(other)

	# Python 2.x support
	def __rdiv__(self, other):
		return other / float(self.close)

	# Python 2.x support
	def __div__(self, other):
		if isinstance(other, Candle):
			return self.close / float(other.close)
		else:
			return self.close / float(other)

	def __str__(self):
		return "symbol " + self.getSymbol() + \
			   ", interval " + IntervalMapper.getDbValue(self.interval) + \
			   ", open time " + str(self.openTime) + \
		       ", open " + str(self.open) + \
		       ", high " + str(self.high) + \
		       ", low " + str(self.low) + \
		       ", close " + str(self.close) + \
		       ", close time " + str(self.closeTime) + \
			   ", closing " + str(self.isClosing)
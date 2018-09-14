import time
from market_data.IndicatorManager import IndicatorManager

class MarketDataManager(object):
	def __init__(self, exchangeClient):
		self.exchangeClient = exchangeClient

		self.candleMap = {}

		self.indicatorManager = IndicatorManager(self.candleMap)

	def init(self, pair, interval):
		candles = self.exchangeClient.getCandles(pair = pair, interval = interval, limit = 500)

		key = pair.getSymbol() + str(interval)
		self.candleMap[key] = candles

	def processCandle(self, newCandle):
		key = newCandle.getSymbol() + str(newCandle.getInterval())

		if not key in self.candleMap:
			self.candleMap[key] = []

		candles = self.candleMap[key]

		lastCandle = None
		if len(candles) > 0:
			lastCandle = candles[-1]

		if lastCandle:
			if lastCandle.getCloseTime() == newCandle.getCloseTime():
				candles[-1] = newCandle
				self.indicatorManager.updateCandle(newCandle)
			else:
				candles.append(newCandle)
				self.indicatorManager.addCandle(newCandle)
		else:
			candles.append(newCandle)
			self.indicatorManager.addCandle(newCandle)

	def removeAllCandles(self):
		self.candleMap.clear()
		self.indicatorManager = IndicatorManager(self.candleMap)

	def getCandles(self, symbol, interval, limit = None):
		if limit:
			return self.candleMap[symbol + str(interval)][-limit:]
		else:
			return self.candleMap[symbol + str(interval)]

	def getIndicatorManager(self):
		return self.indicatorManager
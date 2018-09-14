import os
import csv
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from clients.ExchangeClient import ExchangeClient
from market_data.Candle import Candle
from market_data.SymbolRules import SymbolRules
from orders.OrderResponse import OrderResponse
from orders.OrderState import OrderState
from orders.OrderSide import OrderSide
from orders.OrderType import OrderType
from clients.FileDataMapper import FileIntervalMapper
from market_data.CretenInterval import CretenInterval
from json_schemas import FileExchangeSchema

class FileBacktestClient(ExchangeClient):
	def __init__(self, exchangeConfigPath):
		super(FileBacktestClient, self).__init__(exchangeConfigPath)

		self.log.info("Loading input data file '" + self.exchangeConf['data']['inputFile'] + "'")
		if not os.path.isfile(self.exchangeConf['data']['inputFile']):
			raise Exception("Input CSV data file could not be loaded. '" + os.path.realpath(self.exchangeConf['data']['inputFile']) + "' does not correspond to a valid file.")

		self.data = []
		with open(os.path.realpath(self.exchangeConf['data']['inputFile'])) as myFile:
			csvData = csv.reader(myFile, delimiter = str(self.exchangeConf['data']['separator']), quotechar = '|')

			self.data = sorted(csvData, key=lambda x: datetime.strptime(x[0], self.exchangeConf['data']['timeFormat']))
		self.log.debug('Loaded candles: ' + str(len(self.data)))

	def getExchangeConfigSchema(self):
		return FileExchangeSchema.schema

	@staticmethod
	def _calcClosingTmstmp(startTmstmp, interval):
		closeTmstmp = startTmstmp

		if interval == CretenInterval.INTERVAL_1MINUTE:
			closeTmstmp += timedelta(minutes = 1)
		elif interval == CretenInterval.INTERVAL_3MINUTE:
			closeTmstmp += timedelta(minutes = 3)
		elif interval == CretenInterval.INTERVAL_5MINUTE:
			closeTmstmp += timedelta(minutes = 5)
		elif interval == CretenInterval.INTERVAL_15MINUTE:
			closeTmstmp += timedelta(minutes = 15)
		elif interval == CretenInterval.INTERVAL_30MINUTE:
			closeTmstmp += timedelta(minutes = 30)
		elif interval == CretenInterval.INTERVAL_1HOUR:
			closeTmstmp += timedelta(hours = 1)
		elif interval == CretenInterval.INTERVAL_2HOUR:
			closeTmstmp += timedelta(hours = 2)
		elif interval == CretenInterval.INTERVAL_4HOUR:
			closeTmstmp += timedelta(hours = 4)
		elif interval == CretenInterval.INTERVAL_6HOUR:
			closeTmstmp += timedelta(hours = 6)
		elif interval == CretenInterval.INTERVAL_8HOUR:
			closeTmstmp += timedelta(hours = 8)
		elif interval == CretenInterval.INTERVAL_12HOUR:
			closeTmstmp += timedelta(hours = 12)
		elif interval == CretenInterval.INTERVAL_1DAY:
			closeTmstmp += timedelta(days = 1)
		elif interval == CretenInterval.INTERVAL_3DAY:
			closeTmstmp += timedelta(days = 3)
		elif interval == CretenInterval.INTERVAL_1WEEK:
			closeTmstmp += timedelta(weeks = 1)
		elif interval == CretenInterval.INTERVAL_1MONTH:
			closeTmstmp += relativedelta(months = 1)

		closeTmstmp -= timedelta(seconds = 1)

		return closeTmstmp

	def getRawClient(self):
		return None

	def getCandles(self, pair, interval, limit = None, startTime = None, endTime = None):
		if pair.getSymbol() != self.exchangeConf['baseAsset'] + self.exchangeConf['quoteAsset']:
			raise Exception('Requested symbol ' + pair.getSymbol() + ' does not match loaded symbol ' + self.exchangeConf['baseAsset'] + self.exchangeConf['quoteAsset'] + '.')

		if interval != FileIntervalMapper.getCretenValue(self.exchangeConf['data']['interval']):
			raise Exception('Requested interval ' + str(FileIntervalMapper.getFileValue(interval)) + ' does not match loaded interval ' + self.exchangeConf['data']['interval'] + '.')

		candles = []
		for row in self.data:
			fi = self.exchangeConf['data']['fieldIndex']

			openTime = datetime.strptime(row[fi['openTmstmp']], self.exchangeConf['data']['timeFormat'])
			closeTime = self._calcClosingTmstmp(datetime.strptime(row[fi['openTmstmp']], self.exchangeConf['data']['timeFormat']), interval)

			if openTime >= startTime and closeTime <= endTime:
				candles.append(
					Candle(baseAsset = pair.getBaseAsset(),
					       quoteAsset = pair.getQuoteAsset(),
					       interval = interval,
					       openTime = openTime,
					       open = float(row[fi['open']]),
					       high = float(row[fi['high']]),
					       low = float(row[fi['low']]),
					       close = float(row[fi['close']]),
					       volume = row[fi['volume']],
					       closeTime = closeTime,
					       quoteAssetVolume = -1,
					       tradesNb = -1,
					       takerBuyBaseAssetVol = -1,
					       takerBuyQuoteAssetVol = -1,
					       isClosing = True))
				self.log.debug(candles[-1])

		return candles

	def getExchangeInfo(self, symbols = None):
		try:
			sr = SymbolRules(symbol = self.exchangeConf['baseAsset'] + self.exchangeConf['quoteAsset'],
			                 status = None,
			                 baseAssetPrecision = self.exchangeConf['rules']['baseAssetPrecision'],
			                 quoteAssetPrecision = self.exchangeConf['rules']['quoteAssetPrecision'],
			                 orderTypes = None,
			                 icebergAllowed = None,
			                 minPrice = Decimal(self.exchangeConf['rules']['minPrice']),
			                 maxPrice = Decimal(self.exchangeConf['rules']['maxPrice']),
			                 minPriceDenom = Decimal(self.exchangeConf['rules']['minPriceDenom']),
			                 minQty = Decimal(self.exchangeConf['rules']['minQty']),
			                 maxQty = Decimal(self.exchangeConf['rules']['maxQty']),
			                 minQtyDenom = Decimal(self.exchangeConf['rules']['minQtyDenom']),
			                 minNotional = Decimal(self.exchangeConf['rules']['minNotional']))
		except:
			self.log.error("Could not load market rules! Please check the input exchange configuration and input data files.")
			raise

		return [sr]

	def getPortfolio(self):
		return {}


	def createBuyMarketOrder(self, baseAsset, quoteAsset, qty, clientOrderId, currMarketPrice = None):
		orderResponse = OrderResponse(baseAsset = baseAsset, quoteAsset = quoteAsset, orderSide = OrderSide.BUY, orderType = OrderType.MARKET, price = currMarketPrice, origQty = qty, lastExecutedQty = qty, sumExecutedQty = qty,
		                              orderState = OrderState.FILLED, clientOrderId = clientOrderId,
		                              extOrderRef = clientOrderId)

		return orderResponse

	def createBuyLimitOrder(self, baseAsset, quoteAsset, qty, price, clientOrderId):
		orderResponse = OrderResponse(baseAsset = baseAsset, quoteAsset = quoteAsset, orderSide = OrderSide.BUY, orderType = OrderType.LIMIT, origQty = qty, lastExecutedQty = 0, sumExecutedQty = 0,
		                              price = price, orderState = OrderState.OPENED, clientOrderId = clientOrderId,
		                              extOrderRef = clientOrderId)

		return orderResponse

	def createBuyStopLossLimitOrder(self, baseAsset, quoteAsset, qty, stopPrice, price, clientOrderId):
		orderResponse = OrderResponse(baseAsset = baseAsset, quoteAsset = quoteAsset, orderSide = OrderSide.BUY, orderType = OrderType.STOP_LOSS_LIMIT, origQty = qty, lastExecutedQty = 0, sumExecutedQty = 0,
		                              price = price, orderState = OrderState.OPENED, clientOrderId = clientOrderId,
		                              extOrderRef = clientOrderId)

		return orderResponse

	def createSellMarketOrder(self, baseAsset, quoteAsset, qty, clientOrderId, currMarketPrice = None):
		orderResponse = OrderResponse(baseAsset = baseAsset, quoteAsset = quoteAsset, orderSide = OrderSide.SELL, orderType = OrderType.MARKET, price = currMarketPrice, origQty = qty, lastExecutedQty = qty, sumExecutedQty = qty,
		                              orderState = OrderState.FILLED, clientOrderId = clientOrderId,
		                              extOrderRef = clientOrderId)

		return orderResponse

	def createSellLimitOrder(self, baseAsset, quoteAsset, qty, price, clientOrderId):
		orderResponse = OrderResponse(baseAsset = baseAsset, quoteAsset = quoteAsset, orderSide = OrderSide.SELL, orderType = OrderType.LIMIT, origQty = qty, lastExecutedQty = 0, sumExecutedQty = 0,
		                              price = price, orderState = OrderState.OPENED, clientOrderId = clientOrderId,
		                              extOrderRef = clientOrderId)

		return orderResponse

	def createSellStopLossLimitOrder(self, baseAsset, quoteAsset, qty, stopPrice, price, clientOrderId):
		orderResponse = OrderResponse(baseAsset = baseAsset, quoteAsset = quoteAsset, orderSide = OrderSide.SELL, orderType = OrderType.STOP_LOSS_LIMIT, origQty = qty, lastExecutedQty = 0, sumExecutedQty = 0,
		                              price = price, orderState = OrderState.OPENED, clientOrderId = clientOrderId,
		                              extOrderRef = clientOrderId)

		return orderResponse

	def cancelOrder(self, baseAsset, quoteAsset, clientOrderId = None, extOrderRef = None):
		return OrderResponse(baseAsset = baseAsset, quoteAsset = quoteAsset, orderState = OrderState.OPENED, clientOrderId = clientOrderId,
		                              extOrderRef = clientOrderId)
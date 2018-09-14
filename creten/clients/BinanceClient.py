from decimal import Decimal
from datetime import datetime
import time
from binance.client import Client
from clients.ExchangeClient import ExchangeClient
from market_data.Candle import Candle
from market_data.Position import Position
from market_data.SymbolRules import SymbolRules
from orders.OrderResponse import OrderResponse
from orders.OrderState import OrderState
from orders.OrderSide import OrderSide
from orders.OrderType import OrderType
from clients.BinanceDataMapper import BinanceIntervalMapper

class ClientProxy(Client):
	def __init__(self, api_key, api_secret, requests_params = None):
		super(ClientProxy, self).__init__(api_key, api_secret, requests_params)

	def get_klines(self, **params):
		if 'limit' in params and params['limit'] is None:
			params.pop('limit', None)

		if 'startTime' in params and params['startTime'] is None:
			params.pop('startTime', None)

		if 'endTime' in params and params['endTime'] is None:
			params.pop('endTime', None)

		return self._get('klines', data = params)


class BinanceClient(ExchangeClient):
	def __init__(self, apiKey, secKey, exchangeConfigPath):
		super(BinanceClient, self).__init__(exchangeConfigPath)

		self.client = ClientProxy(apiKey, secKey)

	def getRawClient(self):
		return self.client

	def getCandles(self, pair, interval, limit = None, startTime = None, endTime = None):
		klines = self.client.get_klines(symbol = pair.getSymbol(), interval = BinanceIntervalMapper.getBinanceValue(interval),
		                                limit = limit, startTime = int(time.mktime(startTime.timetuple()) * 1000) if startTime else None,
		                                endTime = int(time.mktime(endTime.timetuple()) * 1000) if endTime else None)

		candles = []
		for kline in klines:
			candles.append(
				Candle(baseAsset = pair.getBaseAsset(), quoteAsset = pair.getQuoteAsset(), interval = interval, openTime = datetime.fromtimestamp(int(kline[0]) / 1000), open = float(kline[1]), high = float(kline[2]),
				       low = float(kline[3]), close = float(kline[4]), volume = kline[5], closeTime = datetime.fromtimestamp(int(kline[6]) / 1000),
				       quoteAssetVolume = kline[7], tradesNb = kline[8], takerBuyBaseAssetVol = kline[9],
				       takerBuyQuoteAssetVol = kline[10], isClosing = True))

		return candles

	def getExchangeInfo(self, symbols = None):
		rules = self.client.get_exchange_info()

		symbolRules = []
		for symbol in rules['symbols']:
			if not symbols or symbol['symbol'] in symbols:
				self.log.debug('Raw market rule: ' + str(symbol))

				sr = SymbolRules(symbol = symbol['symbol'],
					status = symbol['status'],
				    baseAssetPrecision = symbol['baseAssetPrecision'],
				    quoteAssetPrecision = symbol['quotePrecision'],
				    orderTypes = symbol['orderTypes'],
				    icebergAllowed = symbol['icebergAllowed'])

				for filter in symbol['filters']:
					if filter['filterType'] == 'PRICE_FILTER':
						sr.minPrice = Decimal(filter['minPrice'])
						sr.maxPrice = Decimal(filter['maxPrice'])
						sr.minPriceDenom = Decimal(filter['tickSize'])
					elif filter['filterType'] == 'LOT_SIZE':
						sr.minQty = Decimal(filter['minQty'])
						sr.maxQty = Decimal(filter['maxQty'])
						sr.minQtyDenom = Decimal(filter['stepSize'])
					elif filter['filterType'] == 'MIN_NOTIONAL':
						sr.minNotional = Decimal(filter['minNotional'])

				self.updateSymbolRuleFromConfig(sr)

				symbolRules.append(sr)

		return symbolRules

	def getPortfolio(self):
		account = self.client.get_account()

		portfolio = {}
		for balance in account['balances']:
			free = float(balance['free'])
			locked = float(balance['locked'])

			portfolio[balance['asset']] = Position(asset = balance['asset'], free = free, locked = locked)

		return portfolio


	def createBuyMarketOrder(self, baseAsset, quoteAsset, qty, clientOrderId, currMarketPrice = None):
		rawResponse = self.client.create_order(
			symbol = baseAsset + quoteAsset,
			side = Client.SIDE_BUY,
			type = Client.ORDER_TYPE_MARKET,
			quantity = qty,
			newClientOrderId = clientOrderId,
			newOrderRespType = Client.ORDER_RESP_TYPE_FULL)

		nominalVal = 0.0
		for fill in rawResponse['fills']:
			nominalVal += float(fill['price']) * float(fill['qty'])
		avgPrice = nominalVal / float(qty)

		orderResponse = OrderResponse(baseAsset = baseAsset, quoteAsset = quoteAsset, orderSide = OrderSide.BUY, orderType = OrderType.MARKET, price = avgPrice, origQty = qty, lastExecutedQty = qty, sumExecutedQty = qty,
		                              orderState = OrderState.FILLED, clientOrderId = clientOrderId,
		                              extOrderRef = rawResponse['orderId'], rawData = rawResponse)

		return orderResponse

	def createBuyLimitOrder(self, baseAsset, quoteAsset, qty, price, clientOrderId):
		self.log.debug('createBuyLimitOrder: symbol [' + baseAsset + quoteAsset + '], qty [' + str(qty) + ' ], price [' + str(price) + '], clientOrderId [' + str(clientOrderId) + ']')

		rawResponse = self.client.create_order(
			symbol = baseAsset + quoteAsset,
			side = Client.SIDE_BUY,
			type = Client.ORDER_TYPE_LIMIT,
			quantity = qty,
			price = price,
			timeInForce = Client.TIME_IN_FORCE_GTC,
			newClientOrderId = clientOrderId,
			newOrderRespType = Client.ORDER_RESP_TYPE_FULL)

		orderResponse = OrderResponse(baseAsset = baseAsset, quoteAsset = quoteAsset, orderSide = OrderSide.BUY, orderType = OrderType.LIMIT, origQty = qty, lastExecutedQty = 0, sumExecutedQty = 0,
		                              price = price, orderState = OrderState.OPENED, clientOrderId = clientOrderId,
		                              extOrderRef = clientOrderId, rawData = rawResponse)

		return orderResponse

	def createBuyStopLossLimitOrder(self, baseAsset, quoteAsset, qty, stopPrice, price, clientOrderId):
		rawResponse = self.client.create_order(
			symbol = baseAsset + quoteAsset,
			side = Client.SIDE_BUY,
			type = Client.ORDER_TYPE_STOP_LOSS_LIMIT,
			quantity = qty,
			price = price,
			stopPrice = stopPrice,
			timeInForce = Client.TIME_IN_FORCE_GTC,
			newClientOrderId = clientOrderId,
			newOrderRespType = Client.ORDER_RESP_TYPE_FULL)

		orderResponse = OrderResponse(baseAsset, quoteAsset, orderSide = OrderSide.BUY, orderType = OrderType.STOP_LOSS_LIMIT, origQty = qty, lastExecutedQty = 0, sumExecutedQty = 0,
		                              price = price, orderState = OrderState.OPENED, clientOrderId = clientOrderId,
		                              extOrderRef = clientOrderId, rawData = rawResponse)

		return orderResponse

	def createSellMarketOrder(self, baseAsset, quoteAsset, qty, clientOrderId, currMarketPrice = None):
		rawResponse = self.client.create_order(
			symbol = baseAsset + quoteAsset,
			side = Client.SIDE_SELL,
			type = Client.ORDER_TYPE_MARKET,
			quantity = qty,
			newClientOrderId = clientOrderId,
			newOrderRespType = Client.ORDER_RESP_TYPE_FULL)

		nominalVal = 0.0
		for fill in rawResponse['fills']:
			nominalVal += float(fill['price']) * float(fill['qty'])
		avgPrice = nominalVal / float(qty)

		orderResponse = OrderResponse(baseAsset = baseAsset, quoteAsset = quoteAsset, orderSide = OrderSide.SELL, orderType = OrderType.MARKET, price = avgPrice, origQty = qty, lastExecutedQty = qty, sumExecutedQty = qty,
		                              orderState = OrderState.FILLED, clientOrderId = clientOrderId,
		                              extOrderRef = rawResponse['orderId'], rawData = rawResponse)

		return orderResponse

	def createSellLimitOrder(self, baseAsset, quoteAsset, qty, price, clientOrderId):
		rawResponse = self.client.create_order(
			symbol = baseAsset + quoteAsset,
			side = Client.SIDE_SELL,
			type = Client.ORDER_TYPE_LIMIT,
			quantity = qty,
			price = price,
			timeInForce = Client.TIME_IN_FORCE_GTC,
			newClientOrderId = clientOrderId,
			newOrderRespType = Client.ORDER_RESP_TYPE_FULL)

		orderResponse = OrderResponse(baseAsset = baseAsset, quoteAsset = quoteAsset, orderSide = OrderSide.SELL, orderType = OrderType.LIMIT, origQty = qty, lastExecutedQty = 0, sumExecutedQty = 0,
		                              price = price, orderState = OrderState.OPENED, clientOrderId = clientOrderId,
		                              extOrderRef = clientOrderId, rawData = rawResponse)

		return orderResponse

	def createSellStopLossLimitOrder(self, baseAsset, quoteAsset, qty, stopPrice, price, clientOrderId):
		rawResponse = self.client.create_order(
			symbol = baseAsset + quoteAsset,
			side = Client.SIDE_SELL,
			type = Client.ORDER_TYPE_STOP_LOSS_LIMIT,
			quantity = qty,
			price = price,
			stopPrice = stopPrice,
			timeInForce = Client.TIME_IN_FORCE_GTC,
			newClientOrderId = clientOrderId,
			newOrderRespType = Client.ORDER_RESP_TYPE_FULL)

		orderResponse = OrderResponse(baseAsset = baseAsset, quoteAsset = quoteAsset, orderSide = OrderSide.SELL, orderType = OrderType.STOP_LOSS_LIMIT, origQty = qty, lastExecutedQty = 0, sumExecutedQty = 0,
		                              price = price, orderState = OrderState.OPENED, clientOrderId = clientOrderId,
		                              extOrderRef = clientOrderId, rawData = rawResponse)

		return orderResponse

	def cancelOrder(self, baseAsset, quoteAsset, clientOrderId = None, extOrderRef = None):
		if extOrderRef:
			rawResponse = self.client.cancel_order(symbol = baseAsset + quoteAsset, orderId = extOrderRef)
		elif clientOrderId:
			rawResponse = self.client.cancel_order(symbol = baseAsset + quoteAsset, origClientOrderId = clientOrderId)
		else:
			raise Exception()

		orderResponse = OrderResponse(baseAsset = baseAsset, quoteAsset = quoteAsset, orderState = OrderState.OPENED, rawData = rawResponse)

		return orderResponse
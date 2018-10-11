from abc import ABCMeta
from dateutil.relativedelta import relativedelta
from datetime import timedelta
from clients.ExchangeClient import ExchangeClient
from market_data.CretenInterval import CretenInterval
from market_data.SymbolRules import SymbolRules
from orders.OrderResponse import OrderResponse
from orders.OrderState import OrderState
from orders.OrderSide import OrderSide
from orders.OrderType import OrderType
from decimal import Decimal

class OfflineExchangeClient(ExchangeClient):
	__metaclass__ = ABCMeta

	def __init__(self, exchangeConfigPath):
		super(OfflineExchangeClient, self).__init__(exchangeConfigPath)

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

	def createOrder(self, orderSide, orderType, baseAsset, quoteAsset, qty, stopPrice, price, clientOrderId):
		orderResponse = OrderResponse(baseAsset = baseAsset, quoteAsset = quoteAsset, orderSide = orderSide,
		                              orderType = orderType, price = price, origQty = qty,
		                              lastExecutedQty = 0, sumExecutedQty = 0,
		                              orderState = OrderState.OPENED, clientOrderId = clientOrderId,
		                              extOrderRef = clientOrderId)

		return orderResponse

	def cancelOrder(self, baseAsset, quoteAsset, clientOrderId = None, extOrderRef = None):
		return OrderResponse(baseAsset = baseAsset, quoteAsset = quoteAsset, orderState = OrderState.OPENED, clientOrderId = clientOrderId,
		                              extOrderRef = clientOrderId)
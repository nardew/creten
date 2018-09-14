from abc import ABCMeta, abstractmethod
from threading import RLock
from common.Db import Db
from common.Logger import Logger
from common.Settings import Settings
from common.ListOperations import makeList
from market_data.Pair import Pair

class CandleSubscriptionKey(object):
	def __init__(self, pair, cretenInterval):
		self.pair = pair
		self.cretenInterval = cretenInterval

	def __hash__(self):
		return hash((self.pair.getBaseAsset(), self.pair.getQuoteAsset(), self.cretenInterval))

	def __eq__(self, other):
		return (self.pair.getBaseAsset(), self.pair.getQuoteAsset(), self.cretenInterval) == (other.pair.getBaseAsset(), other.pair.getQuoteAsset(), other.cretenInterval)

class ExchangeDataListener:
	__metaclass__ = ABCMeta

	def __init__(self, exchangeClient, marketDataManager, marketRulesManager, portfolioManager, orderManager):
		self.exchangeClient = exchangeClient
		self.marketDataManager = marketDataManager
		self.marketRulesManager = marketRulesManager
		self.portfolioManager = portfolioManager
		self.orderManager = orderManager

		self.candleSubscriptions = []
		self.candleListenerCallbackMap = {}
		self.callbackPortfolio = None
		self.callbackOrders = None

		self.cretenExecDetlId = None

		self.lock = RLock()

		self.log = Logger()

	@abstractmethod
	def start(self):
		pass

	@abstractmethod
	def parseCandleUpdate(self, msg):
		pass

	@abstractmethod
	def parseOrderUpdate(self, msg):
		pass

	@abstractmethod
	def parsePortfolioUpdate(self, msg):
		pass

	def setCretenExecDetlId(self, id):
		self.cretenExecDetlId = id

	def resetCandleListener(self):
		self.candleSubscriptions = []
		self.candleListenerCallbackMap = {}

	def resetUserDataListener(self):
		self.callbackPortfolio = None
		self.callbackOrders = None

	def registerCandleListener(self, pair, cretenInterval, callback):
		self.candleSubscriptions.append(CandleSubscriptionKey(pair, cretenInterval))
		self.candleListenerCallbackMap[CandleSubscriptionKey(pair, cretenInterval)] = makeList(callback)

	def registerUserDataListener(self, callbackPortfolio = None, callbackOrders = None):
		self.callbackPortfolio = makeList(callbackPortfolio)
		self.callbackOrders = makeList(callbackOrders)

	def processCandleUpdate(self, msg):
		with self.lock:
			self.log.debug('Candle message received: ' + str(msg))

			try:
				# 1. parse incoming message
				candle = self.parseCandleUpdate(msg)

				# 2. update market data manager
				self.marketDataManager.processCandle(candle)

				# 3. invoke custom callbacks
				for callback in self.candleListenerCallbackMap[
					CandleSubscriptionKey(Pair(candle.getBaseAsset(), candle.getQuoteAsset()), candle.getInterval())]:
					callback(candle)

				Db.Session().commit()
			except:
				self.log.error('Candle processing failed! Msg [' + str(msg) + ']')

				Db.Session().rollback()
				raise
			finally:
				Db.Session.remove()

			try:
				# 4. create outbound orders
				self.orderManager.sentOrders(self.cretenExecDetlId)
				Db.Session().commit()
			except:
				self.log.error('Candle processing failed while generating outbound orders! Msg [' + str(msg) + ']')

				Db.Session().rollback()
				raise
			finally:
				Db.Session.remove()

	def processOrderUpdate(self, msg):
		with self.lock:
			try:
				orderResponse = self.parseOrderUpdate(msg)

				# TODO verify that the order is incoming from this instance of creten
				# process only orders originating from creten
				if orderResponse.getClientOrderId()[:len(Settings.ORDER_REFERENCE_PREFIX)] == Settings.ORDER_REFERENCE_PREFIX:
					self.orderManager.processOrderUpdate(orderResponse)

					if self.callbackOrders:
						for callback in self.callbackOrders:
							callback(orderResponse)
				else:
					self.log.info('Order message received for an order not originating from Creten. Msg [' + str(msg) + ']')

				Db.Session().commit()
			except:
				self.log.error('Order update processing failed! Msg [' + str(msg) + ']')

				Db.Session().rollback()
				raise
			finally:
				Db.Session.remove()

			try:
				# create outbound orders
				self.orderManager.sentOrders(self.cretenExecDetlId)
				Db.Session().commit()
			except:
				self.log.error('Order update processing failed while generating outbound orders! Msg [' + str(msg) + ']')

				Db.Session().rollback()
				raise
			finally:
				Db.Session.remove()

	def processPortfolioUpdate(self, msg):
		with self.lock:
			try:
				positions = self.parsePortfolioUpdate(msg)
				for position in positions:
					self.portfolioManager.addPosition(position)

					if self.callbackPortfolio:
						for callback in self.callbackPortfolio:
							callback(position)

				Db.Session().commit()
			except:
				self.log.error('Portfolio update processing failed! Msg [' + str(msg) + ']')

				Db.Session().rollback()
				raise
			finally:
				Db.Session.remove()
from colorama import Style, Fore, Back
from abc import ABCMeta, abstractmethod
from db_entities.Trade import Trade
from db_entities.db_codes import REF_TRADE_STATE
from market_data.Pair import Pair
from common.Logger import Logger
from common.Db import Db
from market_data.PositionAllocator import PositionAllocator

class CretenStrategy:
	__metaclass__ = ABCMeta

	def __init__(self, strategyExecId, pair, exchangeClient, marketDataManager, marketRulesManager, portfolioManager, orderManager):
		self.strategyExecId = strategyExecId
		self.pair = pair
		self.exchangeClient = exchangeClient
		self.marketDataManager = marketDataManager
		self.marketRulesManager = marketRulesManager
		self.portfolioManager = portfolioManager
		self.orderManager = orderManager

		self.positionAllocator = PositionAllocator(portfolioManager, None)

		self.log = Logger()

	def getStrategyExecId(self):
		return self.strategyExecId

	@abstractmethod
	def execute(self, candle):
		pass

	def persistStrategyParams(self, tradeId):
		pass

	def tradeClosed(self, tradeId):
		self.log.info(self.__class__.__name__ + ': trade ' + str(tradeId) + ' closed')

	def getActiveTrades(self, pair = None):
		if not pair:
			pair = self.pair

		return Db.Session().query(Trade).filter(Trade.trade_state.in_([REF_TRADE_STATE.OPEN_PENDING, REF_TRADE_STATE.OPENED, REF_TRADE_STATE.CLOSE_PENDING]),
		                                      Trade.base_asset == pair.getBaseAsset(),
		                                      Trade.quote_asset == pair.getQuoteAsset(),
		                                      Trade.strategy_exec_id == self.strategyExecId).all()

	def openTrade(self, tradeType, candle, orders):
		self.log.info('')
		self.log.info('>>> [' + str(candle) + ']')
		self.log.info(Style.BRIGHT + Back.BLUE + Fore.LIGHTWHITE_EX + self.__class__.__name__ + ': OPEN' + Style.RESET_ALL)

		if len(self.getActiveTrades(Pair(candle.getBaseAsset(), candle.getQuoteAsset()))) > 0:
			raise Exception("A new trade was attempted to be opened while there still exists another active trade.")

		trade = self.orderManager.openTrade(self.strategyExecId, tradeType, candle, orders)
		self.log.info('Trade ' + str(trade.trade_id) + ' OPENED.')

		# persist custom strategy parameters
		self.persistStrategyParams(trade.trade_id)

	def openOrder(self, trade, candle, orders):
		self.log.info('>>> [' + str(candle) + ']')
		self.log.info(self.__class__.__name__ + ': NEW ORDERS')

		self.orderManager.openOrder(trade, candle, orders)
from strategy.CretenStrategy import CretenStrategy
from orders.OrderBuyMarket import OrderBuyMarket
from orders.OrderSellMarket import OrderSellMarket
from orders.TradeType import TradeType
from common.ListOperations import minListLen

# Trading strategy based on MACD and AO:
# ENTRY: MACD line gets over signal len and AO gets positive
# EXIT: MACD line gets below signal len and AO gets negative
class MACD_AOStrategy(CretenStrategy):
	def __init__(self, strategyExecId, pair, exchangeClient, marketDataManager, marketRulesManager, portfolioManager, orderManager, params):
		super(MACD_AOStrategy, self).__init__(strategyExecId, pair, exchangeClient, marketDataManager, marketRulesManager, portfolioManager, orderManager)

		self.params = params

		self.macdBullCross = False
		self.macdBearCross = False

	def execute(self, candle):
		self.log.debug(self.__class__.__name__)

		if not candle.getIsClosing():
			return

		indMgr = self.marketDataManager.getIndicatorManager()

		# load MACD and AO from the cache
		macd = indMgr.getMACD(candle.getInterval(), candle.getSymbol(), self.params['macdFastMa'], self.params['macdSlowMa'], self.params['macdSignal'])
		ao = indMgr.getAO(candle.getInterval(), candle.getSymbol(), self.params['aoFastMa'], self.params['aoSlowMa'])

		# make sure we have enough input values
		if not minListLen([macd.getMACDLine(), macd.getSignalLine(), ao], 2):
			return

		self.log.debug('MACD: ' + str(macd.getMACDLine()[-1]))
		self.log.debug('MACD signal: ' + str(macd.getSignalLine()[-1]))
		self.log.debug('AO: ' + str(ao[-1]))

		# record bullish crossing
		if macd.getMACDLine()[-1] > macd.getSignalLine()[-1] and macd.getMACDLine()[-2] < macd.getSignalLine()[-2]:
			self.macdBullCross = True
			self.macdBearCross = False

		# record bear crossing
		if macd.getMACDLine()[-1] < macd.getSignalLine()[-1] and macd.getMACDLine()[-2] > macd.getSignalLine()[-2]:
			self.macdBullCross = False
			self.macdBearCross = True

		# check if we are already in a trade or not
		trades = self.getActiveTrades()
		if len(trades) == 0:
				# if macd is over signal line (bullish crossing) and ao is positive, then buy
				if self.macdBullCross and ao[-1] > 0:
					o = OrderBuyMarket(qty = 100)
					self.openTrade(TradeType.LONG, candle, [o])
		else:
			# if macd is below signal line (bearish crossing) and ao is negative, then sell
			if self.macdBearCross and ao[-1] <= 0:
				o = OrderSellMarket(qty = 100)
				self.openOrder(trades[-1], candle, [o])
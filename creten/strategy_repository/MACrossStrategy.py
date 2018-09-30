from strategy.CretenStrategy import CretenStrategy
from orders.OrderBuyMarket import OrderBuyMarket
from orders.OrderSellMarket import OrderSellMarket
from orders.TradeType import TradeType
from common.ListOperations import minListLen

# Trading strategy based on moving averages and their crossing:
# ENTRY: fast moving average gets above slow moving average
# EXIT: fast moving average gets below slow moving average
class MACrossStrategy(CretenStrategy):
	def __init__(self, strategyExecId, pair, exchangeClient, marketDataManager, marketRulesManager, portfolioManager, orderManager, params):
		super(MACrossStrategy, self).__init__(strategyExecId, pair, exchangeClient, marketDataManager, marketRulesManager, portfolioManager, orderManager)

		self.params = params

	def execute(self, candle):
		self.log.debug(self.__class__.__name__)

		if not candle.getIsClosing():
			return

		indMgr = self.marketDataManager.getIndicatorManager()

		# load EMAs from the cache
		emaS = indMgr.getEMA(candle.getInterval(), candle.getSymbol(), self.params['slow_ma'])
		emaF = indMgr.getEMA(candle.getInterval(), candle.getSymbol(), self.params['fast_ma'])

		if not minListLen([emaF, emaS], 2):
			return

		# check if we are already in a trade or not
		trades = self.getActiveTrades()
		if len(trades) == 0:
			# fast EMA got above slow EMA -> buy
			if emaF[-1] > emaS[-1] and emaF[-2] < emaS[-2]:
				o = OrderBuyMarket(qty = 10)
				self.openTrade(TradeType.LONG, candle, [o])
		else:
			# fast EMA got below slow EMA -> sell
			if emaF[-1] < emaS[-1] and emaF[-2] > emaS[-2]:
				o = OrderSellMarket(qty = 10)
				self.openOrder(trades[-1], candle, [o])
from strategy.CretenStrategy import CretenStrategy
from orders.OrderBuyMarket import OrderBuyMarket
from orders.OrderSellStopLossLimit import OrderSellStopLossLimit
from orders.OrderSellMarket import OrderSellMarket
from orders.TradeType import TradeType
from common.ListOperations import minListLen

# Trading strategy based on bollinger bands
# ENTRY: 1/ price got below lower bollinger band, 2/ then got back above the central line, 3/ central line is increasing
# EXIT: price got above upper bollinger band
class BollingerBounceStrategy(CretenStrategy):
	def __init__(self, cretenExecDetlId, pair, strategyConf, exchangeClient, marketDataManager, marketRulesManager, portfolioManager, orderManager):
		super(BollingerBounceStrategy, self).__init__(cretenExecDetlId, pair, strategyConf, exchangeClient, marketDataManager, marketRulesManager, portfolioManager, orderManager)
		self.lowerCross = False

	def tradeClosed(self, tradeId):
		self.lowerCross = False

	def execute(self, candle):
		self.log.debug(self.__class__.__name__)

		if not candle.getIsClosing():
			return

		# load bollinger bands from the cache
		bb = self.marketDataManager.getIndicatorManager().getBB(candle.getInterval(), candle.getSymbol(), self.params['period'], self.params['stdDevMult'])

		# if we do not have enough input data, wait
		if not minListLen([bb.getCentralBand()], self.params["lookBackPeriod"]):
			return

		# check if we are already in a trade or not
		trades = self.getActiveTrades()
		if len(trades) == 0:
			# record that we got below the lower bollinger band
			if not self.lowerCross and candle.getClose() < bb.getLowerBand()[-1]:
				self.lowerCross = True

			# if previously we got below lower bollinger band, got back above the central line and the central line is increasing, then buy
			if self.lowerCross and candle.getClose() > bb.getCentralBand()[-1] and bb.getCentralBand()[-1] > bb.getCentralBand()[-self.params["lookBackPeriod"]]:
				self.lowerCross = False
				o1 = OrderBuyMarket(qty = 1)
				o2 = OrderSellStopLossLimit(qty = 1, stopPrice = bb.getLowerBand()[-1], price = bb.getLowerBand()[-1])
				self.openTrade(TradeType.LONG, candle, [o1, o2])
		else:
			# if we got above upper bollinger band, then sell
			if candle.getClose() > bb.getUpperBand()[-1]:
				o1 = OrderSellMarket(qty = 1)
				self.updateTrade(trades[0], candle, [o1])
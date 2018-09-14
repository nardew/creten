from strategy.CretenStrategy import CretenStrategy
from orders.OrderBuyMarket import OrderBuyMarket
from orders.OrderSellStopLossLimit import OrderSellStopLossLimit
from orders.OrderSellMarket import OrderSellMarket
from orders.TradeType import TradeType
from common.ListOperations import minListLen

class BollingerBounceStrategy(CretenStrategy):
	def __init__(self, strategyExecId, pair, exchangeClient, marketDataManager, marketRulesManager, portfolioManager, orderManager, params):
		super(BollingerBounceStrategy, self).__init__(strategyExecId, pair, exchangeClient, marketDataManager, marketRulesManager, portfolioManager, orderManager)

		self.params = params

		self.lowerCross = False

	def execute(self, candle):
		self.log.debug(self.__class__.__name__)

		if not candle.getIsClosing():
			return

		indMgr = self.marketDataManager.getIndicatorManager()

		bb = indMgr.getBB(candle.getInterval(), candle.getSymbol(), self.params['period'], self.params['stdDevMult'])

		if not minListLen([bb.getCentralBand()], self.params["lookBackPeriod"]):
			return

		trades = self.getActiveTrades()
		if len(trades) == 0:
			if not self.lowerCross and candle.getClose() < bb.getLowerBand()[-1]:
				self.lowerCross = True

			if self.lowerCross and candle.getClose() > bb.getCentralBand()[-1] and bb.getCentralBand()[-1] > bb.getCentralBand()[-self.params["lookBackPeriod"]]:
				self.lowerCross = False
				o1 = OrderBuyMarket(qty = 1)
				o2 = OrderSellStopLossLimit(qty = 1, stopPrice = bb.getLowerBand()[-1], price = bb.getLowerBand()[-1])
				self.openTrade(TradeType.LONG, candle, [o1, o2])
		else:
			if candle.getClose() > bb.getUpperBand()[-1]:
				o1 = OrderSellMarket(qty = 1)
				self.openOrder(trades[0], candle, [o1])
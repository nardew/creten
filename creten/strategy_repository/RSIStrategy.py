from strategy.CretenStrategy import CretenStrategy
from orders.OrderBuyMarket import OrderBuyMarket
from orders.OrderSellMarket import OrderSellMarket
from orders.OrderSellStopLossLimit import OrderSellStopLossLimit
from orders.TradeType import TradeType
from common.ListOperations import minListLen

# Trading strategy based on RSI and EMA indicators:
# ENTRY: RSI got oversold -> returned back above limit + price above EMA
# EXIT: price below (entry price - constant) or RSI got overbought
class RSIStrategy(CretenStrategy):
	def __init__(self, strategyExecId, pair, exchangeClient, marketDataManager, marketRulesManager, portfolioManager, orderManager, params):
		super(RSIStrategy, self).__init__(strategyExecId, pair, exchangeClient, marketDataManager, marketRulesManager, portfolioManager, orderManager)

		self.params = params

		self.gotOversold = False

	def tradeClosed(self, tradeId):
		self.gotOversold = False

	def execute(self, candle):
		self.log.debug(self.__class__.__name__)

		# React only to closing candles. Relevant only for realtime test, backtest always works with closing candles.
		if not candle.getIsClosing():
			return

		# Fetch RSI and EMA indicators from the cache
		rsi = self.marketDataManager.getIndicatorManager().getRSI(candle.getInterval(), candle.getSymbol(), self.params['rsiPeriod'])
		ema = self.marketDataManager.getIndicatorManager().getEMA(candle.getInterval(), candle.getSymbol(), self.params['emaPeriod'])

		# If RSI indicator does not contain at least 1 value, do not apply strategy at this point
		if not minListLen([rsi, ema], 1):
			return

		self.log.debug("RSI value: " + str(rsi[-1]))
		self.log.debug("EMA value: " + str(ema[-1]))

		trades = self.getActiveTrades()
		# Check if we are already in a trade or not. If not, evaluate strategy's ENTRY conditions. If yes, evaluate
		# strategies EXIT conditions.
		if len(trades) == 0:
			# First check if we moved to the oversold region.
			# If yes, record it in an auxaliary variable gotOversold.
			if not self.gotOversold and rsi[-1] < self.params['rsiOversold']:
				self.gotOversold = True

			# If we entered oversold region (gotOversold = True), RSI returned back above specified limit and we are above EMA,
			# our ENTRY conditions are met and we file opening orders.
			if self.gotOversold and rsi[-1] >= self.params['rsiSignal'] and candle.getClose() > ema[-1]:
				# a buy market order of 1 BTC
				orderBuy = OrderBuyMarket(qty = 1)
				# a stoploss sell order at price lower by 80 compared to current price
				orderStopLoss = OrderSellStopLossLimit(qty = 1, stopPrice = candle.getClose() - 80, price = candle.getClose() - 80)

				# initiate the trade with the two above orders
				self.openTrade(TradeType.LONG, candle, [orderBuy, orderStopLoss])
		else:
			# If we are in an active trade and RSI got into overbought region, we close the trade by a sell market order
			if rsi[-1] > self.params['rsiOverbought']:
				orderSell = OrderSellMarket(qty = 1)
				self.openOrder(trades[-1], candle, [orderSell])

				# reset gotOversold flag
				self.gotOversold = False
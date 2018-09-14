import datetime
from clients.ExchangeDataListener import ExchangeDataListener
from common.ListOperations import makeList

class BacktestDataListener(ExchangeDataListener):
	def __init__(self, exchangeClient, marketDataManager, marketRulesManager, portfolioManager, orderManager):
		super(BacktestDataListener, self).__init__(exchangeClient, marketDataManager, marketRulesManager, portfolioManager, orderManager)

		self.startTimestampMs = None
		self.endTimestampMs = None
		self.baseAsset = None
		self.quoteAsset = None
		self.interval = None

	def init(self, startTimestampMs, endTimestampMs):
		self.startTimestampMs = startTimestampMs
		self.endTimestampMs = endTimestampMs

	def parseCandleUpdate(self, msg):
		return msg

	def parseOrderUpdate(self, msg):
		return msg

	def parsePortfolioUpdate(self, msg):
		return makeList(msg)

	def start(self):
		for candleSubscription in self.candleSubscriptions:
			self.log.info('Loading historical data for symbol ' + candleSubscription.pair.getBaseAsset() + candleSubscription.pair.getQuoteAsset())
			candles = []
			tmpStartTimestampMs = self.startTimestampMs
			while True:
				self.log.debug('Start timestamp ' + str(tmpStartTimestampMs))

				rawCandles = self.exchangeClient.getCandles(pair = candleSubscription.pair,
				                                            interval = candleSubscription.cretenInterval,
				                                            startTime = tmpStartTimestampMs, endTime = self.endTimestampMs)

				self.log.debug('Loaded candles: ' + str(len(rawCandles)))

				if len(rawCandles) == 0:
					break

				candles = candles + rawCandles

				tmpStartTimestampMs = candles[-1].getCloseTime()

			self.log.info('Loading historical data completed')
			self.log.info('')

			self.log.info('Starting backtesting')
			for candle in candles:
				self.processCandleUpdate(candle)
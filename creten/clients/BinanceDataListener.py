from datetime import datetime
from clients.ExchangeDataListener import ExchangeDataListener, CandleSubscriptionKey
from binance.websockets import BinanceSocketManager
from clients.BinanceDataMapper import BinanceIntervalMapper, BinanceOrderSideMapper, BinanceOrderTypeMapper, BinanceOrderStateMapper
from market_data.Candle import Candle
from market_data.Position import Position
from clients.SupportedQuoteAsset import SupportedQuoteAsset, BINANCE_SUPPORTED_QUOTE_ASSET
from orders.OrderResponse import OrderResponse

class BinanceDataListener(ExchangeDataListener):
	PORTFOLIO_UPDATE_STRING = 'outboundAccountInfo'
	ORDER_UPDATE_STRING = 'executionReport'

	def __init__(self, exchangeClient, marketDataManager, marketRulesManager, portfolioManager, orderManager):
		super(BinanceDataListener, self).__init__(exchangeClient, marketDataManager, marketRulesManager, portfolioManager, orderManager)

		self.binanceSocket = BinanceSocketManager(self.exchangeClient.getRawClient())
		self.binanceSocket.setDaemon(True)

		self.log.init(logForceDebug = False)

	def dispatchUserDataUpdate(self, msg):
		self.log.debug('User data message received: ' + str(msg))

		if msg['e'] == self.PORTFOLIO_UPDATE_STRING:
			self.processPortfolioUpdate(msg)
		elif msg['e'] == self.ORDER_UPDATE_STRING:
			self.processOrderUpdate(msg)

	def parseOrderUpdate(self, msg):
		symbol = msg['s']
		quoteAsset = SupportedQuoteAsset.getQuoteAsset(symbol, BINANCE_SUPPORTED_QUOTE_ASSET)
		baseAsset = symbol[:len(symbol) - len(quoteAsset)]

		orderResponse = OrderResponse(baseAsset = baseAsset, quoteAsset = quoteAsset,
		                              orderSide = BinanceOrderSideMapper.getCretenValue(msg['S']),
		                              orderType = BinanceOrderTypeMapper.getCretenValue(msg['o']),
		                              origQty = msg['q'], lastExecutedQty = msg['l'], sumExecutedQty = msg['z'],
		                              price = msg['p'], orderTmstmp = datetime.fromtimestamp(msg['T'] / 1000),
		                              orderState = BinanceOrderStateMapper.getCretenValue(msg['X']),
		                              clientOrderId = msg['c'], extOrderRef = msg['i'], rawData = msg)

		return orderResponse

	def parsePortfolioUpdate(self, msg):
		positions = []
		for balance in msg['B']:
			asset = balance['a']
			free = float(balance['f'])
			locked = float(balance['l'])

			# TODO do only for subscribed pairs
			positions.append(Position(asset, free, locked))

		return positions

	def parseCandleUpdate(self, msg):
		symbol = msg['s']
		quoteAsset = SupportedQuoteAsset.getQuoteAsset(symbol, BINANCE_SUPPORTED_QUOTE_ASSET)
		baseAsset = symbol[:len(symbol) - len(quoteAsset)]

		interval = msg['k']['i']

		kline = msg['k']

		cretenInterval = BinanceIntervalMapper.getCretenValue(interval)

		candle = Candle(baseAsset = baseAsset, quoteAsset = quoteAsset, interval = cretenInterval,
				openTime = datetime.fromtimestamp(int(kline['t']) / 1000), open = kline['o'], high = kline['h'], low = kline['l'], close = kline['c'],
			   volume = kline['v'], closeTime = datetime.fromtimestamp(int(kline['T']) / 1000), quoteAssetVolume = kline['q'], tradesNb = kline['n'],
			   takerBuyBaseAssetVol = kline['V'], takerBuyQuoteAssetVol = kline['Q'], isClosing = kline['x'])

		return candle

	def start(self):
		# subsribe candle listeners
		for candleSubscription in self.candleSubscriptions:
			binanceInterval = BinanceIntervalMapper.getBinanceValue(candleSubscription.cretenInterval)
			self.binanceSocket.start_kline_socket(candleSubscription.pair.getSymbol(), self.processCandleUpdate, binanceInterval)

		# subscribe user data listener
		self.binanceSocket.start_user_socket(self.dispatchUserDataUpdate)

		# start listening
		self.binanceSocket.start()
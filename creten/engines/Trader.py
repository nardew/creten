from market_data.MarketDataManager import MarketDataManager
from market_data.PortfolioManager import PortfolioManager
from clients.BinanceDataListener import BinanceDataListener
from market_data.CretenInterval import CretenInterval
from strategy_repository.BigThree import BigThree
from strategy.StrategyExecutor import StrategyExecutor

class Trader(object):
	def __init__(self, exchangeClient):
		self.exchangeClient = exchangeClient

		self.marketDataManager = MarketDataManager(self.exchangeClient)
		self.portfolioManager = PortfolioManager(self.exchangeClient)

		self.exchangeDataListener = BinanceDataListener(self.exchangeClient, self.marketDataManager, self.portfolioManager)

		self.bigThree = BigThree('XLM', 'ETH', self.exchangeClient, self.marketDataManager, self.portfolioManager)

		self.creten = StrategyExecutor()
		self.creten.addStrategy(self.bigThree)

		# initialize data
		self.marketDataManager.init('XLMETH', CretenInterval.INTERVAL_1MINUTE)
		self.portfolioManager.init()

		self.exchangeDataListener.registerPortfolioListener()
		self.exchangeDataListener.registerKlineListener("XLMETH", CretenInterval.INTERVAL_1MINUTE, self.creten.processKline)

	def run(self):
		self.exchangeDataListener.start()
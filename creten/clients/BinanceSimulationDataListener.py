from clients.BinanceDataListener import BinanceDataListener
from common.ListOperations import makeList

class BinanceSimulationDataListener(BinanceDataListener):
	def __init__(self, exchangeClient, marketDataManager, marketRulesManager, portfolioManager, orderManager):
		super(BinanceSimulationDataListener, self).__init__(exchangeClient, marketDataManager, marketRulesManager, portfolioManager, orderManager)

	def parseOrderUpdate(self, msg):
		return msg

	def parsePortfolioUpdate(self, msg):
		return makeList(msg)
import time
import json
import jsonschema
from common.Db import Db
from engines.CretenEngine import CretenEngine
from engines.ExchangeEventSimulator import ExchangeEventSimulator
from strategy.StrategyFactory import StrategyFactory
from db_managers.ExecManager import ExecManager
from market_data.MarketRulesManager import MarketRulesManager
from market_data.MarketDataManager import MarketDataManager
from market_data.PortfolioManager import PortfolioManager
from orders.OrderManager import OrderManager
from clients.BinanceSimulationDataListener import BinanceSimulationDataListener
from market_data.CretenInterval import CretenInterval
from strategy.StrategyExecutor import StrategyExecutor
from market_data.Pair import Pair
from json_schemas import RealtimetestSchema

class RealTimeSimulator(CretenEngine):
	def __init__(self, exchangeClient, inputConfRaw, cretenExecId):
		super(RealTimeSimulator, self).__init__()

		self.exchangeClient = exchangeClient
		self.inputConfRaw = inputConfRaw
		self.cretenExecId = cretenExecId

		self.marketDataManager = MarketDataManager(self.exchangeClient)
		self.marketRulesManager = MarketRulesManager(self.exchangeClient)
		self.portfolioManager = PortfolioManager(self.exchangeClient)
		self.orderManager = OrderManager(self.exchangeClient, self.marketRulesManager)

		self.exchangeDataListener = BinanceSimulationDataListener(self.exchangeClient, self.marketDataManager, self.marketRulesManager, self.portfolioManager, self.orderManager)
		self.exchangeEventSimulator = ExchangeEventSimulator(self.marketDataManager, self.orderManager, self.portfolioManager, self.exchangeDataListener)

	def run(self):
		self.log.info('');
		self.log.info('Starting real time simulation')

		inputConf = json.loads(self.inputConfRaw)
		jsonschema.validate(inputConf, RealtimetestSchema.schema)

		with Db.session_scope():
			ced = ExecManager.createCretenExecDetl(self.cretenExecId, inputConf['realtimetest'])
			cretenExecDetlId = ced.creten_exec_detl_id

		self.exchangeDataListener.setCretenExecDetlId(cretenExecDetlId)
		self.exchangeEventSimulator.setCretenExecDetlId(cretenExecDetlId)

		cretenInterval = getattr(CretenInterval, "INTERVAL_" + inputConf['realtimetest']['interval'])

		for pairConf in inputConf['realtimetest']['pairs']:
			pair = Pair(baseAsset = pairConf[0], quoteAsset = pairConf[1])

			self.marketDataManager.init(pair, cretenInterval)
			self.marketRulesManager.init(pair.getSymbol())

			strategyExecutor = StrategyExecutor()

			for strategyConf in inputConf['realtimetest']['strategies']:
				strategy = StrategyFactory.getStrategy(strategyConf, pair, cretenExecDetlId,
				                                       self.exchangeClient, self.marketDataManager,
				                                       self.marketRulesManager, self.portfolioManager,
				                                       self.orderManager)
				strategyExecutor.addStrategy(strategy)

			self.exchangeDataListener.registerCandleListener(pair, cretenInterval, [self.exchangeEventSimulator.simulateEvent, strategyExecutor.execute])

		self.portfolioManager.init()
		self.exchangeDataListener.registerUserDataListener()

		self.exchangeDataListener.start()

		while True:
			time.sleep(1)
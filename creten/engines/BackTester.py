from colorama import Fore, Back, Style
import json
import jsonschema
from datetime import datetime
from common.Db import Db
from clients.BacktestDataListener import BacktestDataListener
from engines.ExchangeEventSimulator import ExchangeEventSimulator
from market_data.MarketDataManager import MarketDataManager
from market_data.MarketRulesManager import MarketRulesManager
from market_data.PortfolioManager import PortfolioManager
from orders.OrderManager import OrderManager
from market_data.CretenInterval import CretenInterval
from strategy.StrategyManager import StrategyManager, StrategyExecutor
from market_data.Position import Position
from engines.CretenEngine import CretenEngine
from strategy.StrategyFactory import StrategyFactory
from db_managers.ExecManager import ExecManager
from db_managers.TradeManager import TradeManager
from db_entities.db_codes import REF_EXEC_STATE, REF_TRADE_STATE, REF_ORDER_STATE
from orders.Order import Order
from orders.OrderSide import OrderSide
from common.Timer import Timer
from strategy.StrategyPerformance import StrategyPerformance
from market_data.Pair import Pair
from engines.BacktestGenerator import BacktestGenerator
from json_schemas import BacktestSchema
from common.constants import BACKTEST_TMSTMP_FORMAT

class BackTester(CretenEngine):
	def __init__(self, exchangeClient, inputConfRaw, cretenExecId):
		super(BackTester, self).__init__()

		self.exchangeClient = exchangeClient
		self.inputConfRaw = inputConfRaw
		self.cretenExecId = cretenExecId

		self.marketDataManager = MarketDataManager(self.exchangeClient)
		self.marketRulesManager = MarketRulesManager(self.exchangeClient)
		self.portfolioManager = PortfolioManager(self.exchangeClient)
		self.strategyManager = StrategyManager()
		self.orderManager = OrderManager(self.exchangeClient, self.marketRulesManager, self.strategyManager)

		self.exchangeDataListener = BacktestDataListener(self.exchangeClient, self.marketDataManager, self.marketRulesManager, self.portfolioManager, self.orderManager)
		self.exchangeEventSimulator = ExchangeEventSimulator(self.marketDataManager, self.orderManager, self.portfolioManager, self.exchangeDataListener)

	def initPortfolio(self, portfolio):
		self.portfolioManager.clear()

		for position in portfolio:
			self.portfolioManager.addPosition(Position(position['asset'], position['quantity']))

	def _revertOpenTrades(self, strategyExecId):
		trades = TradeManager.getAllTrades(strategyExecId = strategyExecId, tradeState = REF_TRADE_STATE.OPENED)
		self.log.debug('')
		self.log.debug('Open trades to be reversed: ' + str(len(trades)))

		for trade in trades:
			self.log.debug('Reverting open trade ' + str(trade.trade_id))
			orders = TradeManager.getAllOrders(tradeId = trade.trade_id, orderState = [REF_ORDER_STATE.FILLED, REF_ORDER_STATE.PARTIALLY_FILLED])

			for dbOrder in orders:
				order = Order()
				order.setFromEntity(dbOrder)

				self.log.debug('Reverting order ' + str(order))

				basePosition = self.portfolioManager.getPosition(trade.base_asset)
				quotePosition = self.portfolioManager.getPosition(trade.quote_asset)

				if order.getOrderSide() == OrderSide.BUY:
					basePosition.setFree(basePosition.getFree() - float(order.getQty()))
					quotePosition.setFree(quotePosition.getFree() + float(order.getQty() * order.getPrice()))
				else:
					basePosition.setFree(basePosition.getFree() + float(order.getQty()))
					quotePosition.setFree(quotePosition.getFree() - float(order.getQty() * order.getPrice()))

				# transaction nesting is required to ensure that session invalidation in below method does not
				# detach objects (trades and orders) loaded and iterated within this method
				Db.Session().begin_nested()
				self.exchangeDataListener.processPortfolioUpdate(basePosition)
				Db.Session().begin_nested()
				self.exchangeDataListener.processPortfolioUpdate(quotePosition)

	def _showPerformance(self, strategyExecId):
		self.log.info('')
		self.log.info(Style.BRIGHT + Back.BLUE + Fore.LIGHTWHITE_EX + 'PERFORMANCE' + Style.RESET_ALL)

		perf = StrategyPerformance(strategyExecId)
		perf.printStats()

	def run(self):
		with Timer("BackTester::run", endDebugLevel = 'INFO'):
			inputConf = json.loads(self.inputConfRaw)
			jsonschema.validate(inputConf, BacktestSchema.schema)

			# generate backtest configuration based on the input file
			if 'backtestConf' in inputConf:
				for conf in inputConf['backtestConf']:
					backtestConf = BacktestGenerator.getBacktest(conf)

					self.log.debug("Generated backtest config: " + str(backtestConf))
					self.log.debug('')

					if 'backtest' not in inputConf:
						inputConf['backtest'] = []
					inputConf['backtest'] += backtestConf

			for conf in inputConf['backtest']:
				with Db.session_scope():
					ced = ExecManager.createCretenExecDetl(self.cretenExecId, conf)
					cretenExecDetlId = ced.creten_exec_detl_id

				self.exchangeDataListener.setCretenExecDetlId(cretenExecDetlId)
				self.exchangeEventSimulator.setCretenExecDetlId(cretenExecDetlId)

				for pairConf in conf['pairs']:
					pair = Pair(baseAsset = pairConf[0], quoteAsset = pairConf[1])

					self.log.info('')
					self.log.info('Loading market rules')
					self.marketRulesManager.init([pair.getSymbol()])
					self.log.info('Loading market rules completed')
					self.log.info('')

					for strategyConf in conf['strategies']:
						strategy = StrategyFactory.getStrategy(strategyConf, pair, cretenExecDetlId,
						                                       self.exchangeClient, self.marketDataManager,
						                                       self.marketRulesManager, self.portfolioManager, self.orderManager)

						self.strategyManager.reset()
						strategyExecutor = StrategyExecutor()
						strategyExecutor.addStrategy(strategy)
						self.strategyManager.addStrategyExecutor(strategyExecutor)

						startTimestamp = datetime.strptime(conf['start_tmstmp'], BACKTEST_TMSTMP_FORMAT)
						endTimestamp = datetime.strptime(conf['end_tmstmp'], BACKTEST_TMSTMP_FORMAT)

						self.log.info('Backtesting period: ' + str(startTimestamp) + ' - ' + str(endTimestamp))
						self.log.info('')

						self.exchangeDataListener.resetCandleListener()
						self.exchangeDataListener.resetUserDataListener()
						self.marketDataManager.removeAllCandles()
						self.orderManager.reset()

						self.log.info('Initialize portfolio:')
						for position in conf['portfolio']:
							self.log.info('\t' + position['asset'] + ': ' + str(position['quantity']))
						self.log.info('')
						self.initPortfolio(conf['portfolio'])

						interval = getattr(CretenInterval, "INTERVAL_" + conf['interval'])
						self.exchangeDataListener.init(startTimestamp, endTimestamp)
						self.exchangeDataListener.registerCandleListener(pair, interval, [self.exchangeEventSimulator.simulateEvent, strategyExecutor.execute])

						self.exchangeDataListener.start()

						# revert open trades in order not to interfere with overall statistics
						self._revertOpenTrades(strategy.getStrategyExecId())

						# evaluate results
						pos = self.portfolioManager.getPosition(pair.getQuoteAsset())
						self.log.info('')
						self.log.info('Final balance for ' + pair.getQuoteAsset() + ': ' + str(pos.getFree()))

						# calculate metrics
						self._showPerformance(strategy.getStrategyExecId())

				ced.exec_state = REF_EXEC_STATE.FINISHED
				with Db.session_scope():
					Db.Session().add(ced)
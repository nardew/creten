import importlib
from common.Db import Db
from common.Logger import Logger
from db_managers.ExecManager import ExecManager

class StrategyFactory(object):
	@staticmethod
	def getStrategy(strategyConf, pair, cretenExecDetlId, exchangeClient, marketDataManager,
	                marketRulesManager, portfolioManager, orderManager):
		modulePath = "strategy_repository." + strategyConf['strategy_name']
		if "module_path" in strategyConf:
			modulePath = strategyConf['module_path']

		try:
			strategyModule = importlib.import_module(modulePath)
			strategyClass = getattr(strategyModule, strategyConf['strategy_name'])

			s = strategyClass(
				cretenExecDetlId,
				pair,
				strategyConf,
				exchangeClient,
				marketDataManager,
				marketRulesManager,
				portfolioManager,
				orderManager)
		except:
			log = Logger()
			log.error("Cannot create instance of strategy [" + strategyConf['strategy_name'] + "]! Module path [" + modulePath + "].")

			raise

		return s
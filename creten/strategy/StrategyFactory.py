import importlib
from common.Db import Db
from common.Logger import Logger
from db_managers.ExecManager import ExecManager

class StrategyFactory(object):
	@staticmethod
	def getStrategy(strategyConf, pair, cretenExecDetlId, exchangeClient, marketDataManager,
	                marketRulesManager, portfolioManager, orderManager):
		with Db.session_scope():
			se = ExecManager.createStrategyExec(cretenExecDetlId, strategyConf, pair)
			strategyExecId = se.strategy_exec_id

		modulePath = "strategy_repository." + strategyConf['strategy_name']
		if "module_path" in strategyConf:
			modulePath = strategyConf['module_path']

		try:
			strategyModule = importlib.import_module(modulePath)
			strategyClass = getattr(strategyModule, strategyConf['strategy_name'])

			s = strategyClass(
				strategyExecId,
				pair,
				exchangeClient,
				marketDataManager,
				marketRulesManager,
				portfolioManager,
				orderManager,
				strategyConf['params'] if "params" in strategyConf else None)
		except:
			log = Logger()
			log.error("Cannot create instance of strategy [" + strategyConf['strategy_name'] + "]! Module path [" + modulePath + "].")

			raise

		return s
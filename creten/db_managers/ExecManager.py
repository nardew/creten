import json
from datetime import datetime
from common.Db import Db
from db_entities.CretenExec import CretenExec
from db_entities.CretenExecDetl import CretenExecDetl
from db_entities.StrategyExec import StrategyExec
from db_entities.db_codes import REF_EXEC_TYPE, REF_EXEC_STATE
from common.constants import PARAM_MODE_BACKTEST, PARAM_MODE_REALTIMETEST, BACKTEST_TMSTMP_FORMAT

class ExecManager():
	@staticmethod
	def createCretenExec(mode, inputConf):
		ce = CretenExec()
		ce.conf = inputConf

		inputJson = json.loads(inputConf)

		try:
			ce.dscp = inputJson['dscp']
		except KeyError:
			pass

		if mode == PARAM_MODE_BACKTEST:
			ce.exec_type = REF_EXEC_TYPE.BACKTEST
		elif mode == PARAM_MODE_REALTIMETEST:
			ce.exec_type = REF_EXEC_TYPE.REALTIMETEST

		Db.Session().add(ce)
		Db.Session().flush()

		return ce

	@staticmethod
	def createCretenExecDetl(cretenExecId, inputConf):
		ced = CretenExecDetl()
		ced.creten_exec_id = cretenExecId
		ced.exec_state = str(REF_EXEC_STATE.STARTED) # conversion to string due to SQLite
		ced.conf = json.dumps(inputConf)
		ced.interval = inputConf['interval']

		try:
			ced.start_tmstmp = datetime.strptime(inputConf['start_tmstmp'], BACKTEST_TMSTMP_FORMAT)
		except KeyError:
			pass

		try:
			ced.end_tmstmp = datetime.strptime(inputConf['end_tmstmp'], BACKTEST_TMSTMP_FORMAT)
		except KeyError:
			pass

		try:
			ced.dscp = inputConf['dscp']
		except KeyError:
			pass

		Db.Session().add(ced)
		Db.Session().flush()

		return ced

	@staticmethod
	def createStrategyExec(cretenExecDetlId, strategyConf, pair):
		se = StrategyExec()
		se.creten_exec_detl_id = cretenExecDetlId
		se.base_asset = pair.getBaseAsset()
		se.quote_asset = pair.getQuoteAsset()
		se.conf = json.dumps(strategyConf)

		try:
			se.dscp = strategyConf['dscp']
		except KeyError:
			pass

		Db.Session().add(se)
		Db.Session().flush()

		return se
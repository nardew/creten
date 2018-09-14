from common.Logger import Logger

class BacktestGenerator(object):
	log = Logger()

	@staticmethod
	def getBacktest(conf):
		backtests = []

		BacktestGenerator.log.debug('Backtest generator config: ' + str(conf))
		BacktestGenerator.log.debug('')

		if conf['name'] == 'TEST_GEN':
			backtest = {
				"pairs": conf['pairs'],
				"interval": conf['interval'],
				"start_tmstmp": conf['start_tmstmp'],
				"end_tmstmp": conf['end_tmstmp'],
				"portfolio": conf['portfolio'],
				"commission": conf['commission']
			}

			strategies = []
			for maType in conf['maTypes']:
				for maPeriod in range(conf['minMA'],  conf['maxMA'], conf['stepMA']):
					strategies.append({
								"strategy_name": "BTCScalp",
								"params": {
									"maType": maType,
									"maPeriod": maPeriod
								}
							}
					)

			backtest.update({'strategies': strategies})
			backtests.append(backtest)

		return backtests
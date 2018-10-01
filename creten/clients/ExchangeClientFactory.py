from common.constants import PARAM_MODE_BACKTEST, PARAM_MODE_TRADING, PARAM_MODE_REALTIMETEST, PARAM_EXCHANGE_BINANCE, PARAM_EXCHANGE_FILE, PARAM_EXCHANGE_DB
from clients.FileBacktestClient import FileBacktestClient
from clients.DbBacktestClient import DbBacktestClient

class ExchangeClientFactory:
	@staticmethod
	def getExchangeClient(args):
		if args['mode'] == PARAM_MODE_BACKTEST and args['exchange'] == PARAM_EXCHANGE_BINANCE:
			from clients.BinanceBacktestClient import BinanceBacktestClient
			return BinanceBacktestClient(
				args['apikey'],
				args['seckey'],
				args['exchangeconfig'] if "exchangeconfig" in args else None)
		elif args['mode'] == PARAM_MODE_REALTIMETEST and args['exchange'] == PARAM_EXCHANGE_BINANCE:
			from clients.BinanceSimulationClient import BinanceSimulationClient
			return BinanceSimulationClient(
				args['apikey'],
				args['seckey'],
				args['exchangeconfig'] if "exchangeconfig" in args else None)
		elif args['mode'] == PARAM_MODE_TRADING and args['exchange'] == PARAM_EXCHANGE_BINANCE:
			from clients.BinanceClient import BinanceClient
			return BinanceClient(
				args['apikey'],
				args['seckey'],
				args['exchangeconfig'] if "exchangeconfig" in args else None)
		elif args['mode'] == PARAM_MODE_BACKTEST and args['exchange'] == PARAM_EXCHANGE_FILE:
			return FileBacktestClient(args['exchangeconfig'])
		elif args['mode'] == PARAM_MODE_BACKTEST and args['exchange'] == PARAM_EXCHANGE_DB:
			return DbBacktestClient(args['exchangeconfig'])
		else:
			raise Exception("Unsupported combination of mode '" + args['mode'] + "' and exchange '" + args['exchange'] + "'.")
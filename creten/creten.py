import argparse
import logging
import os
import datetime
from colorama import Fore, Back, Style
import re
from common.Db import Db
from common.constants import PARAM_MODE_BACKTEST, PARAM_MODE_TRADING, PARAM_MODE_REALTIMETEST, PARAM_EXCHANGE_BINANCE, PARAM_EXCHANGE_FILE, DEFAULT_CLIENT_SETTINGS_PATH
from clients.ExchangeClientFactory import ExchangeClientFactory
from common.Logger import Logger
from common.Settings import Settings

def printLogo():
	print(Style.BRIGHT + Fore.LIGHTYELLOW_EX + Back.RED + "creten v0.1" + Style.RESET_ALL)

def initLogger(logLevel, logFile):
	if logLevel == 'debugall' or logLevel == 'debugalll':
		logging.getLogger().setLevel(logging.DEBUG)
		Logger.GLOB_LOG_LEVEL = Logger.DEBUG_LEVEL
	elif logLevel == 'debug':
		logging.getLogger().setLevel(logging.INFO)
		Logger.GLOB_LOG_LEVEL = Logger.DEBUG_LEVEL
	else:
		logging.getLogger().setLevel(logging.INFO)
		Logger.GLOB_LOG_LEVEL = Logger.INFO_LEVEL

	if logFile:
		class ColorlessFormatter(logging.Formatter):
			def __init__(self, fmt = None, dateFmt = None):
				super(ColorlessFormatter, self).__init__(fmt, dateFmt)

			def format(self, record):
				msg = super(ColorlessFormatter, self).format(record)
				return re.sub('\\033\[[0-9]+m', '', msg)

		fileLogger = logging.FileHandler("Creten_{0}.log".format(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
		logFormatter = ColorlessFormatter("%(asctime)s %(levelname)-5.5s %(message)s")
		fileLogger.setFormatter(logFormatter)
		logging.getLogger().addHandler(fileLogger)

	stdoutLogger = logging.StreamHandler()
	stdoutLogger.setFormatter(logging.Formatter('%(message)s'))
	logging.getLogger().addHandler(stdoutLogger)

def parseArgs():
	"""Configuration of command line arguments.
	"""

	parser = argparse.ArgumentParser(description='CRETEN - Crypto Exchange Trading Engine')
	parser.add_argument('-m', '--mode', choices=[PARAM_MODE_TRADING, PARAM_MODE_REALTIMETEST, PARAM_MODE_BACKTEST], help='Mode in which creten will be running',
	                    required=True)
	parser.add_argument('-e', '--exchange', choices=[PARAM_EXCHANGE_BINANCE, PARAM_EXCHANGE_FILE], help='Exchange to connect to', required = True)
	parser.add_argument('--inputconfig', help = 'Input configuration file for the execution', required = True)
	parser.add_argument('--exchangeconfig', help = 'Custom configuration of the selected exchange', required = False)
	parser.add_argument('--clientconfig', help = 'Path to a file with client settings', default = os.path.join(os.path.dirname(os.path.abspath(__file__)), DEFAULT_CLIENT_SETTINGS_PATH), required = False)
	parser.add_argument('--apikey', help='API key', required=False)
	parser.add_argument('--seckey', help='Secret key', required=False)
	parser.add_argument('--logfile', help = 'Print all messages into log file besides standard output', action='store_true')
	parser.add_argument('-l', '--loglevel', default = 'info', choices=['debugalll', 'debugall', 'debug', 'info'],
	                    help = 'Logging level. Select debugalll for debugging creten, libraries and db connection; '
	                           'debugall for debugging creten and libraries; '
	                           'debug for debugging creten')

	return vars(parser.parse_args())

def printInfo(args):
	logging.info('')
	logging.info('Time: ' + str(datetime.datetime.now()))
	logging.info('Mode: ' + args['mode'])
	logging.info('Exchange: ' + args['exchange'])
	logging.info('Global log mode: ' + args['loglevel'])

def initClientConfig(args):
	if not os.path.isfile(args['clientconfig']):
		raise Exception('Client config file could not be loaded. ' + os.path.realpath(
			args['clientconfig']) + " does not correspond to a valid file.")

	Settings.initClientConfig(clientConfigPath = args['clientconfig'])

printLogo()

args = parseArgs()

initLogger(args['loglevel'], args['logfile'])

initClientConfig(args)

printInfo(args)

Db.init(Settings.client['DB_CONNECTION']['ENGINE'],
		Settings.client['DB_CONNECTION']['USER'],
        Settings.client['DB_CONNECTION']['PASSWORD'],
        Settings.client['DB_CONNECTION']['HOST'],
        Settings.client['DB_CONNECTION']['PORT'],
        Settings.client['DB_CONNECTION']['DB'],
        True if args['loglevel'] == 'debugalll' else False)

# following packages must be imported only after database initilization
from engines.BackTester import BackTester
from engines.RealTimeSimulator import RealTimeSimulator
from db_managers.ExecManager import ExecManager

if not os.path.isfile(args['inputconfig']):
	raise Exception('Input configuration file could not be loaded. ' + os.path.realpath(args['inputconfig']) + " does not correspond to a valid file.")

with open(os.path.realpath(args['inputconfig'])) as myfile:
	inputConf = myfile.read()

with Db.session_scope():
	cretenExec = ExecManager.createCretenExec(args['mode'], inputConf)
	cretenExecId = cretenExec.creten_exec_id

log = Logger()

log.debug("Creating exchange client...")
client = ExchangeClientFactory.getExchangeClient(args)

log.debug("Creating creten engine...")
if args['mode'] == PARAM_MODE_BACKTEST:
	simulator = BackTester(client, inputConf, cretenExecId)
	simulator.run()
elif args['mode'] == PARAM_MODE_REALTIMETEST:
	simulator = RealTimeSimulator(client, inputConf, cretenExecId)
	simulator.run()
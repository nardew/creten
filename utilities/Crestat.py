import argparse
import logging
import os
import datetime
from sqlalchemy import desc
from colorama import Fore, Back, Style
from prettytable import PrettyTable
from common.Db import Db
from common.constants import DEFAULT_CLIENT_SETTINGS_PATH, CRETEN_APP_ROOT_DIR_ENV_VAR
from common.Logger import Logger
from common.Settings import Settings

def printLogo():
	print(Style.BRIGHT + Fore.LIGHTWHITE_EX + Back.GREEN + "Crestat v0.1" + Style.RESET_ALL)

def initLogger(logLevel):
	if logLevel == 'debugall' or logLevel == 'debugalll':
		logging.getLogger().setLevel(logging.DEBUG)
		Logger.GLOB_LOG_LEVEL = Logger.DEBUG_LEVEL
	elif logLevel == 'debug':
		logging.getLogger().setLevel(logging.INFO)
		Logger.GLOB_LOG_LEVEL = Logger.DEBUG_LEVEL
	else:
		logging.getLogger().setLevel(logging.INFO)
		Logger.GLOB_LOG_LEVEL = Logger.INFO_LEVEL

	stdoutLogger = logging.StreamHandler()
	stdoutLogger.setFormatter(logging.Formatter('%(message)s'))
	logging.getLogger().addHandler(stdoutLogger)

def parseArgs():
	"""Configuration of command line arguments.
	"""

	try:
		defaultClientConfigPath = os.environ[CRETEN_APP_ROOT_DIR_ENV_VAR] + '/' + DEFAULT_CLIENT_SETTINGS_PATH
	except KeyError:
		print('ERROR: ' + CRETEN_APP_ROOT_DIR_ENV_VAR + ' environment variable does not exist! Please initialize it with CRETEN root dir.')
		raise

	parser = argparse.ArgumentParser(description='Crestat')
	parser.add_argument('--clientconfig', help = 'Path to a file with client settings', default = defaultClientConfigPath)
	parser.add_argument('--logfile', help = 'Print all messages into log file besides standard output', action='store_true')
	parser.add_argument('-p', '--precision', default = 2, help = 'Decimal precision to be used in the output')
	parser.add_argument('-c', '--count', default = 1, help = 'Number of executions to be evaluated')
	parser.add_argument('-f', '--file', help = 'Export results into a CSV file', action = 'store_true')
	parser.add_argument('-l', '--loglevel', default = 'info', choices=['debugalll', 'debugall', 'debug', 'info'],
	                    help = 'Logging level. Select debugalll for debugging creten, libraries and db connection; '
	                           'debugall for debugging creten and libraries; '
	                           'debug for debugging creten')

	return vars(parser.parse_args())

def printInfo(args):
	logging.info('')
	logging.info('Time: ' + str(datetime.datetime.now()))
	logging.info('Global log mode: ' + args['loglevel'])

args = parseArgs()
initLogger(args['loglevel'])

if not os.path.isfile(args['clientconfig']):
	raise Exception('Client config file could not be loaded. ' + os.path.realpath(args['clientconfig']) + " does not correspond to a valid file.")

Settings.initClientConfig(clientConfigPath = args['clientconfig'])

printLogo()
printInfo(args)

Db.init(Settings.client['DB_CONNECTION']['ENGINE'],
		Settings.client['DB_CONNECTION']['USER'],
        Settings.client['DB_CONNECTION']['PASSWORD'],
        Settings.client['DB_CONNECTION']['HOST'],
        Settings.client['DB_CONNECTION']['PORT'],
        Settings.client['DB_CONNECTION']['DB'],
        True if args['loglevel'] == 'debugalll' else False)

# must be imported after db session has been initialised
from db_entities.CretenExec import CretenExec
from db_entities.CretenExecDetl import CretenExecDetl
from db_entities.StrategyExec import StrategyExec
from strategy.StrategyPerformance import StrategyPerformance

log = Logger()

logging.info('')
with Db.session_scope():
	cretenExecs = Db.Session().query(CretenExec.creten_exec_id).order_by(desc(CretenExec.creten_exec_id)).limit(args['count']).all()

	log.debug('Executions to be evaluated: ' + str(cretenExecs))

	strategyExecs = Db.Session().query(StrategyExec).filter(CretenExecDetl.creten_exec_id.in_([x[0] for x in cretenExecs]),
	    CretenExecDetl.creten_exec_detl_id == StrategyExec.creten_exec_detl_id).order_by(desc(StrategyExec.strategy_exec_id)).all()

	f = None
	if args['file']:
		f = open('Crestat_{0}.log'.format(datetime.datetime.now().strftime('%Y%m%d%H%M%S')), 'w')

	t = PrettyTable()
	t.field_names = ['SEI', 'Trades', 'Won', 'Lost', 'Won [%]', 'Gain', 'Loss', 'Gross profit', 'Gain/Loss',
	                 'Avg gain', 'Max gain', 'Avg loss', 'Max loss', 'Avg trade length', 'Max trade length']

	if args['file']:
		f.write(';'.join(t.field_names) + '\n')

	p = args['precision']

	for se in strategyExecs:
		log.debug('Evaluating strategy exec ' + str(se.strategy_exec_id))
		sp = StrategyPerformance(se.strategy_exec_id)

		#sp.printStats()

		wonPerc = round(100 * sp.getNoWin() / float(sp.getNoTrades()), p) if sp.getNoTrades() > 0 else None
		lostPerc = round(100 * sp.getNoLoss() / float(sp.getNoTrades()), p) if sp.getNoTrades() > 0 else None
		gainLossR = round(sp.getWin() / sp.getLoss(), p) if sp.getLoss() else None

		fields = [se.strategy_exec_id,
		           sp.getNoTrades(),
		           sp.getNoWin(),
		           sp.getNoLoss(),
		            wonPerc,
		           round(sp.getWin(), p) if sp.getWin() else None,
		           round(sp.getLoss(), p) if sp.getLoss() else None,
		          sp.getGrossProfit(),
		           gainLossR,
		           round(sp.getAvgWin(), p) if sp.getAvgWin() else None,
		           round(sp.getMaxWin(), p) if sp.getMaxWin() else None,
		           round(sp.getAvgLoss(), p) if sp.getAvgLoss() else None,
		           round(sp.getMaxLoss(), p) if sp.getMaxLoss() else None,
		           sp.getAvgTradeLengthStr(),
		           sp.getMaxTradeLengthStr()]

		t.add_row(fields)

		if args['file']:
			f.write(';'.join([str(x) for x in fields]) + '\n')

	print(t)

	if args['file']:
		f.close()
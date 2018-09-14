import argparse
from colorama import Fore, Back, Style
from binance.client import Client

print(Style.BRIGHT + Fore.LIGHTWHITE_EX + Back.BLUE + "Cremon v0.1" + Style.RESET_ALL)


def printLine():
	print('------------------------')


def parseArgs():
	"""Configuration of command line arguments.
	"""

	parser = argparse.ArgumentParser(description='Cremon - Crypto exchange monitoring')
	parser.add_argument('--apikey', help='API key', required=True)
	parser.add_argument('--seckey', help='Secret key', required=True)

	return vars(parser.parse_args())


def getLatestPrice(prices, symbol):
	for pair in prices:
		if pair['symbol'] == symbol:
			return float(pair['price'])

	return None


def getBalance(symbol, balances):
	for balance in balances:
		if symbol == balance['asset']:
			return float(balance['free'])

	return 0.0


args = parseArgs()

binClient = Client(args['apikey'], args['seckey'])

print('\n')
print('DEPOSITS')
printLine()

deposit_coins = [
	'ETH',
	'LTC',
	'BTC'
]

depositValBTC = 0.0
nonBTCDeposit = {}
for depCoin in deposit_coins:
	deposits = binClient.get_deposit_history(asset=depCoin)

	depositCoinVal = 0.0
	for deposit in deposits['depositList']:
		# print deposit

		if depCoin == 'BTC':
			depositCoinVal += deposit['amount']
			depositValBTC += deposit['amount']
		else:
			klines = binClient.get_klines(symbol=depCoin + 'BTC', interval='1m', limit=1,
			                              startTime=deposit['insertTime'])
			depositCoinVal += deposit['amount']
			depositValBTC += float(klines[0][4]) * deposit['amount']

			nonBTCDeposit[depCoin] = {'isBuyer': True, 'price': float(klines[0][4]), 'qty': deposit['amount'],
			                          'commission': 0}

	print(depCoin + ': ' + str(depositCoinVal))

print('Overall: ' + str(depositValBTC) + ' BTC')

acctStatus = binClient.get_account()
prices = binClient.get_all_tickers()

print('\n')
print('COIN GAINS')
printLine()

symbols = [
	'XVG',
	'POE',
	'XLM',
	'LEND',
	'TRX',
	'BNB',
	'LTC',
	'ADA',
	'NEO',
	'POWR',
	'ICX',
	'ETH'
]

commission = 0.0

for symbol in sorted(symbols):
	pair = symbol + "BTC"

	trades = binClient.get_my_trades(symbol=pair)

	spread = 0.0

	if symbol in nonBTCDeposit:
		trades.append(nonBTCDeposit[symbol])

	#print symbol
	for trade in trades:
		#print trade

		commission += float(trade['commission'])
		if trade['isBuyer']:
			spread -= float(trade['price']) * float(trade['qty'])
		else:
			spread += float(trade['price']) * float(trade['qty'])

	bal = getBalance(symbol, acctStatus['balances'])
	price = getLatestPrice(prices, pair)

	print(symbol.rjust(4) + ': ' + '{:8.5f}'.format(spread + bal * price))

print('Commission: ' + str(commission) + ' BNB, ' + str(commission * getLatestPrice(prices, "BNBBTC")) + ' BTC')

print('\n')
print('PORTFOLIO')
printLine()

portfolioValBTC = 0.0
for balance in sorted(acctStatus['balances'], key=lambda bal: float(bal['free']), reverse=True):
	coinValBTC = 0.0
	priceBTC = 0.0

	if float(balance['free']) > 0:
		# print balance

		if balance['asset'] == 'BTC':
			coinValBTC = float(balance['free'])

			# process open trades
			openTrades = binClient.get_open_orders()
			for trade in openTrades:
				#print trade
				rmnqQty = float(trade['origQty']) - float(trade['executedQty'])
				coinValBTC += rmnqQty * float(trade['price'])

			portfolioValBTC += coinValBTC
			priceBTC = 1
		else:
			pair = balance['asset'] + 'BTC'
			price = getLatestPrice(prices, pair)

			if price:
				portfolioValBTC += float(balance['free']) * price
				coinValBTC = float(balance['free']) * price
				priceBTC = price

		print(balance['asset'].rjust(4) + ': qty=' + '{:20.10f}'.format(float(balance['free'])) + ', value=' + str(coinValBTC))

portfolioGainVal = portfolioValBTC - depositValBTC
portfolioGainPerc = 100 * portfolioGainVal / depositValBTC
print('Overall: ' + str(portfolioValBTC) + ' BTC (diff ' + str(portfolioGainVal) + ' BTC, ' + '{:4.2f}'.format(
	portfolioGainPerc) + ' %)')

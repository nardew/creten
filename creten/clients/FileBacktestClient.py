import os
import csv
from datetime import datetime
from decimal import Decimal
from clients.OfflineExchangeClient import OfflineExchangeClient
from market_data.Candle import Candle
from clients.FileDataMapper import FileIntervalMapper
from json_schemas import FileExchangeSchema

class FileBacktestClient(OfflineExchangeClient):
	def __init__(self, exchangeConfigPath):
		super(FileBacktestClient, self).__init__(exchangeConfigPath)

		self.log.info("Loading input data file '" + self.exchangeConf['data']['inputFile'] + "'")
		if not os.path.isfile(self.exchangeConf['data']['inputFile']):
			raise Exception("Input CSV data file could not be loaded. '" + os.path.realpath(self.exchangeConf['data']['inputFile']) + "' does not correspond to a valid file.")

		self.data = []
		with open(os.path.realpath(self.exchangeConf['data']['inputFile'])) as myFile:
			csvData = csv.reader(myFile, delimiter = str(self.exchangeConf['data']['separator']), quotechar = '|')

			self.data = sorted(csvData, key=lambda x: datetime.strptime(x[0], self.exchangeConf['data']['timeFormat']))
		self.log.debug('Loaded candles: ' + str(len(self.data)))

	def getExchangeConfigSchema(self):
		return FileExchangeSchema.schema

	def getCandles(self, pair, interval, limit = None, startTime = None, endTime = None):
		if pair.getSymbol() != self.exchangeConf['baseAsset'] + self.exchangeConf['quoteAsset']:
			raise Exception('Requested symbol ' + pair.getSymbol() + ' does not match loaded symbol ' + self.exchangeConf['baseAsset'] + self.exchangeConf['quoteAsset'] + '.')

		if interval != FileIntervalMapper.getCretenValue(self.exchangeConf['data']['interval']):
			raise Exception('Requested interval ' + str(FileIntervalMapper.getFileValue(interval)) + ' does not match loaded interval ' + self.exchangeConf['data']['interval'] + '.')

		candles = []
		for row in self.data:
			fm = self.exchangeConf['data']['fieldMap']

			openTime = datetime.strptime(row[fm['openTmstmp']], self.exchangeConf['data']['timeFormat'])
			closeTime = self._calcClosingTmstmp(datetime.strptime(row[fm['openTmstmp']], self.exchangeConf['data']['timeFormat']), interval)

			if openTime >= startTime and closeTime <= endTime:
				candles.append(
					Candle(baseAsset = pair.getBaseAsset(),
					       quoteAsset = pair.getQuoteAsset(),
					       interval = interval,
					       openTime = openTime,
					       open = Decimal(row[fm['open']]),
					       high = Decimal(row[fm['high']]),
					       low = Decimal(row[fm['low']]),
					       close = Decimal(row[fm['close']]),
					       volume = row[fm['volume']],
					       closeTime = closeTime,
					       quoteAssetVolume = -1,
					       tradesNb = -1,
					       takerBuyBaseAssetVol = -1,
					       takerBuyQuoteAssetVol = -1,
					       isClosing = True))
				self.log.debug(candles[-1])

		return candles
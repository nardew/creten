from datetime import datetime
from decimal import Decimal
from common.Db import Db
from clients.OfflineExchangeClient import OfflineExchangeClient
from market_data.Candle import Candle
from clients.DbExchangeDataMapper import DbExchangeIntervalMapper
from json_schemas import DbExchangeSchema

class DbBacktestClient(OfflineExchangeClient):
	def __init__(self, exchangeConfigPath):
		super(DbBacktestClient, self).__init__(exchangeConfigPath)

	def getExchangeConfigSchema(self):
		return DbExchangeSchema.schema

	def getCandles(self, pair, interval, limit = None, startTime = None, endTime = None):
		if pair.getSymbol() != self.exchangeConf['baseAsset'] + self.exchangeConf['quoteAsset']:
			raise Exception('Requested symbol ' + pair.getSymbol() + ' does not match loaded symbol ' + self.exchangeConf['baseAsset'] + self.exchangeConf['quoteAsset'] + '.')

		if interval != DbExchangeIntervalMapper.getCretenValue(self.exchangeConf['data']['interval']):
			raise Exception('Requested interval ' + str(DbExchangeIntervalMapper.getDbValue(interval)) + ' does not match loaded interval ' + self.exchangeConf['data']['interval'] + '.')

		fm = self.exchangeConf['data']['fieldMap']
		# if order of the fields is changed, do not forget to updated indices in sqlCandle below
		sqlQuery = 'SELECT ' + \
		           fm['openTmstmp'] + ', ' + \
		           fm['open'] + ', ' + \
		           fm['high'] + ', ' + \
		           fm['low'] + ', ' + \
		           fm['close'] + ', ' + \
		           fm['volume'] + \
		           ' FROM ' + self.exchangeConf['data']['db']['tableName']
		self.log.debug('Query to load input candles: ' + sqlQuery)
		sqlCandles = Db.Session().execute(sqlQuery).fetchall()
		sqlCandles.sort(key = lambda x: datetime.strptime(x[0], self.exchangeConf['data']['timeFormat']))

		candles = []
		for sqlCandle in sqlCandles:
			openTime = datetime.strptime(sqlCandle[0], self.exchangeConf['data']['timeFormat'])
			closeTime = self._calcClosingTmstmp(datetime.strptime(sqlCandle[0], self.exchangeConf['data']['timeFormat']), interval)

			if openTime >= startTime and closeTime <= endTime:
				candles.append(
					Candle(baseAsset = pair.getBaseAsset(),
					       quoteAsset = pair.getQuoteAsset(),
					       interval = interval,
					       openTime = openTime,
					       open = Decimal(sqlCandle[1]),
					       high = Decimal(sqlCandle[2]),
					       low = Decimal(sqlCandle[3]),
					       close = Decimal(sqlCandle[4]),
					       volume = sqlCandle[5],
					       closeTime = closeTime,
					       quoteAssetVolume = -1,
					       tradesNb = -1,
					       takerBuyBaseAssetVol = -1,
					       takerBuyQuoteAssetVol = -1,
					       isClosing = True))
				self.log.debug(candles[-1])

		return candles
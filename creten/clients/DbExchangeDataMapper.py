from market_data.CretenInterval import CretenInterval

class DbExchangeDataMapper:
	@classmethod
	def getCretenValue(cls, value):
		return cls.mapping[value]

	@classmethod
	def getDbValue(cls, cretenValue):
		for key, value in cls.mapping.items():
			if value == cretenValue:
				return key

		return None

class DbExchangeIntervalMapper(DbExchangeDataMapper):
	mapping = {
		"1MINUTE": CretenInterval.INTERVAL_1MINUTE,
		"3MINUTE": CretenInterval.INTERVAL_3MINUTE,
		"5MINUTE": CretenInterval.INTERVAL_5MINUTE,
		"15MINUTE": CretenInterval.INTERVAL_15MINUTE,
		"30MINUTE": CretenInterval.INTERVAL_30MINUTE,
		"1HOUR": CretenInterval.INTERVAL_1HOUR,
		"2HOUR": CretenInterval.INTERVAL_2HOUR,
		"4HOUR": CretenInterval.INTERVAL_4HOUR,
		"6HOUR": CretenInterval.INTERVAL_6HOUR,
		"8HOUR": CretenInterval.INTERVAL_8HOUR,
		"12HOUR": CretenInterval.INTERVAL_12HOUR,
		"1DAY": CretenInterval.INTERVAL_1DAY,
		"3DAY": CretenInterval.INTERVAL_3DAY,
		"1WEEK": CretenInterval.INTERVAL_1WEEK,
		"1MONTH": CretenInterval.INTERVAL_1MONTH
	}
from binance.client import Client
from market_data.CretenInterval import CretenInterval
from orders.OrderState import OrderState
from orders.OrderSide import OrderSide
from orders.OrderType import OrderType

class BinanceDataMapper:
	@classmethod
	def getCretenValue(cls, value):
		return cls.mapping[value]

	@classmethod
	def getBinanceValue(cls, cretenValue):
		for key, value in cls.mapping.items():
			if value == cretenValue:
				return key

		return None

class BinanceIntervalMapper(BinanceDataMapper):
	mapping = {
		Client.KLINE_INTERVAL_1MINUTE: CretenInterval.INTERVAL_1MINUTE,
		Client.KLINE_INTERVAL_3MINUTE: CretenInterval.INTERVAL_3MINUTE,
		Client.KLINE_INTERVAL_5MINUTE: CretenInterval.INTERVAL_5MINUTE,
		Client.KLINE_INTERVAL_15MINUTE: CretenInterval.INTERVAL_15MINUTE,
		Client.KLINE_INTERVAL_30MINUTE: CretenInterval.INTERVAL_30MINUTE,
		Client.KLINE_INTERVAL_1HOUR: CretenInterval.INTERVAL_1HOUR,
		Client.KLINE_INTERVAL_2HOUR: CretenInterval.INTERVAL_2HOUR,
		Client.KLINE_INTERVAL_4HOUR: CretenInterval.INTERVAL_4HOUR,
		Client.KLINE_INTERVAL_6HOUR: CretenInterval.INTERVAL_6HOUR,
		Client.KLINE_INTERVAL_8HOUR: CretenInterval.INTERVAL_8HOUR,
		Client.KLINE_INTERVAL_12HOUR: CretenInterval.INTERVAL_12HOUR,
		Client.KLINE_INTERVAL_1DAY: CretenInterval.INTERVAL_1DAY,
		Client.KLINE_INTERVAL_3DAY: CretenInterval.INTERVAL_3DAY,
		Client.KLINE_INTERVAL_1WEEK: CretenInterval.INTERVAL_1WEEK,
		Client.KLINE_INTERVAL_1MONTH: CretenInterval.INTERVAL_1MONTH
	}

class BinanceOrderStateMapper(BinanceDataMapper):
	mapping = {
		"NEW": OrderState.OPENED,
		"PARTIALLY_FILLED": OrderState.PARTIALLY_FILLED,
		"FILLED": OrderState.FILLED,
		"CANCELED": OrderState.CANCELED,
		"PENDING_CANCEL": OrderState.CANCEL_PENDING_INT,
		"REJECTED": OrderState.REJECTED,
		"EXPIRED": OrderState.EXPIRED
	}

class BinanceOrderSideMapper(BinanceDataMapper):
	mapping = {
		"BUY": OrderSide.BUY,
		"SELL": OrderSide.SELL
	}

class BinanceOrderTypeMapper(BinanceDataMapper):
	mapping = {
		"MARKET": OrderType.MARKET,
		"LIMIT": OrderType.LIMIT,
		"STOP_LOSS_LIMIT": OrderType.STOP_LOSS_LIMIT,
		"STOP_LOSS": OrderType.STOP_LOSS_MARKET
	}
from orders.OrderSide import OrderSide
from orders.OrderType import OrderType
from orders.OrderState import OrderState
from orders.TradeType import TradeType
from orders.TradeState import TradeState
from market_data.CretenInterval import CretenInterval
from db_entities.db_codes import REF_ORDER_TYPE, REF_TRADE_TYPE, REF_ORDER_SIDE, REF_TRADE_STATE, REF_ORDER_STATE, REF_INTERVAL

class DbCodeMapper:
	@classmethod
	def getDbValue(cls, value):
		if isinstance(value, list):
			return [cls.getDbValue(x) for x in value]
		else:
			return cls.mapping[value]

	@classmethod
	def getCretenValue(cls, dbValue):
		if isinstance(dbValue, list):
			return [cls.getCretenValue(x) for x in dbValue]
		else:
			for key, value in cls.mapping.items():
				if value == dbValue:
					return key

		raise Exception("No key found for value [" + str(dbValue) + "]!")

class IntervalMapper(DbCodeMapper):
	mapping = {
		CretenInterval.INTERVAL_1MINUTE: REF_INTERVAL.INTERVAL_1MINUTE,
		CretenInterval.INTERVAL_3MINUTE: REF_INTERVAL.INTERVAL_3MINUTE,
		CretenInterval.INTERVAL_5MINUTE: REF_INTERVAL.INTERVAL_5MINUTE,
		CretenInterval.INTERVAL_15MINUTE: REF_INTERVAL.INTERVAL_15MINUTE,
		CretenInterval.INTERVAL_30MINUTE: REF_INTERVAL.INTERVAL_30MINUTE,
		CretenInterval.INTERVAL_1HOUR: REF_INTERVAL.INTERVAL_1HOUR,
		CretenInterval.INTERVAL_2HOUR: REF_INTERVAL.INTERVAL_2HOUR,
		CretenInterval.INTERVAL_4HOUR: REF_INTERVAL.INTERVAL_4HOUR,
		CretenInterval.INTERVAL_6HOUR: REF_INTERVAL.INTERVAL_6HOUR,
		CretenInterval.INTERVAL_8HOUR: REF_INTERVAL.INTERVAL_8HOUR,
		CretenInterval.INTERVAL_12HOUR: REF_INTERVAL.INTERVAL_12HOUR,
		CretenInterval.INTERVAL_1DAY: REF_INTERVAL.INTERVAL_1DAY,
		CretenInterval.INTERVAL_3DAY: REF_INTERVAL.INTERVAL_3DAY,
		CretenInterval.INTERVAL_1WEEK: REF_INTERVAL.INTERVAL_1WEEK,
		CretenInterval.INTERVAL_1MONTH: REF_INTERVAL.INTERVAL_1MONTH
	}

class OrderSideMapper(DbCodeMapper):
	mapping = {
		OrderSide.BUY: REF_ORDER_SIDE.BUY,
		OrderSide.SELL: REF_ORDER_SIDE.SELL
	}

class OrderTypeMapper(DbCodeMapper):
	mapping = {
		OrderType.MARKET: REF_ORDER_TYPE.MARKET,
		OrderType.LIMIT: REF_ORDER_TYPE.LIMIT,
		OrderType.STOP_LOSS_LIMIT: REF_ORDER_TYPE.STOP_LOSS_LIMIT,
		OrderType.STOP_LOSS_MARKET: REF_ORDER_TYPE.STOP_LOSS_MARKET
	}

class OrderStateMapper(DbCodeMapper):
	mapping = {
		OrderState.OPEN_PENDING_INT: REF_ORDER_STATE.OPEN_PENDING_INT,
		OrderState.OPEN_PENDING_EXT: REF_ORDER_STATE.OPEN_PENDING_EXT,
		OrderState.OPEN_FAILED: REF_ORDER_STATE.OPEN_FAILED,
		OrderState.OPENED: REF_ORDER_STATE.OPENED,
		OrderState.PARTIALLY_FILLED: REF_ORDER_STATE.PARTIALLY_FILLED,
		OrderState.FILLED: REF_ORDER_STATE.FILLED,
		OrderState.CANCEL_PENDING_INT: REF_ORDER_STATE.CANCEL_PENDING_INT,
		OrderState.CANCEL_PENDING_EXT: REF_ORDER_STATE.CANCEL_PENDING_EXT,
		OrderState.CANCEL_FAILED: REF_ORDER_STATE.CANCEL_FAILED,
		OrderState.CANCELED: REF_ORDER_STATE.CANCELLED,
		OrderState.REJECTED: REF_ORDER_STATE.REJECTED,
		OrderState.EXPIRED: REF_ORDER_STATE.EXPIRED
	}

class TradeTypeMapper(DbCodeMapper):
	mapping = {
		TradeType.LONG: REF_TRADE_TYPE.LONG
	}

class TradeStateMapper(DbCodeMapper):
	mapping = {
		TradeState.OPEN_PENDING: REF_TRADE_STATE.OPEN_PENDING,
		TradeState.OPEN_FAILED: REF_TRADE_STATE.OPEN_FAILED,
		TradeState.OPENED: REF_TRADE_STATE.OPENED,
		TradeState.CLOSE_PENDING: REF_TRADE_STATE.CLOSE_PENDING,
		TradeState.CLOSE_FAILED: REF_TRADE_STATE.CLOSE_FAILED,
		TradeState.CLOSED: REF_TRADE_STATE.CLOSED
	}
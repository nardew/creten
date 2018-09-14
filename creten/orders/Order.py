from orders.OrderSide import OrderSide
from orders.OrderType import OrderType
from db_managers.DbCodeMapper import OrderStateMapper, OrderSideMapper, OrderTypeMapper

class Order(object):
	def __init__(self, orderSide = None, orderType = None, qty = None, price = None, stopPrice = None, orderState = None,
	             orderId = None, tradeId = None, intOrderRef = None, initTmstmp = None, openTmstmp = None, filledTmstmp = None):
		self.orderSide = orderSide
		self.orderType = orderType
		self.qty = qty
		self.price = price
		self.stopPrice = stopPrice
		self.orderState = orderState
		self.orderId = orderId
		self.tradeId = tradeId
		self.intOrderRef = intOrderRef
		self.initTmstmp = initTmstmp
		self.openTmstmp = openTmstmp
		self.filledTmstmp = filledTmstmp

	def setFromEntity(self, orderEntity):
		self.orderSide = OrderSideMapper.getCretenValue(orderEntity.order_side)
		self.orderType = OrderTypeMapper.getCretenValue(orderEntity.order_type)
		self.qty = orderEntity.qty
		self.price = orderEntity.price
		self.stopPrice = orderEntity.stop_price
		self.orderState = OrderStateMapper.getCretenValue(orderEntity.order_state)
		self.orderId = orderEntity.order_id
		self.tradeId = orderEntity.trade_id
		self.intOrderRef = orderEntity.int_order_ref
		self.initTmstmp = orderEntity.init_tmstmp
		self.openTmstmp = orderEntity.open_tmstmp
		self.filledTmstmp = orderEntity.filled_tmstmp

	def getOrderSide(self):
		return self.orderSide

	def getOrderType(self):
		return self.orderType

	def getQty(self):
		return self.qty

	def setQty(self, qty):
		self.qty = qty

	def getStopPrice(self):
		return self.stopPrice

	def setStopPrice(self, stopPrice):
		self.stopPrice = stopPrice

	def getPrice(self):
		return self.price

	def setPrice(self, price):
		self.price = price

	def getOrderId(self):
		return self.orderId

	def setOrderId(self, orderId):
		self.orderId = orderId

	def getOrderState(self):
		return self.orderState

	def setOrderState(self, orderState):
		self.orderState = orderState

	def getTradeId(self):
		return self.tradeId

	def getIntOrderRef(self):
		return self.intOrderRef

	def getInitTmstmp(self):
		return self.initTmstmp

	def getOpenTmstmp(self):
		return self.openTmstmp

	def getFilledTmstmp(self):
		return self.filledTmstmp

	def __str__(self):
		return 'orderSide ' + (OrderSideMapper.getDbValue(self.orderSide) if self.orderSide else str(None)) \
		+ ', orderType ' + (OrderTypeMapper.getDbValue(self.orderType) if self.orderType else str(None)) \
		+ ', qty ' + str(self.qty) \
		+ ', price ' + str(self.price) \
		+ ', stopPrice ' + str(self.stopPrice) \
		+ ', orderState ' + (OrderStateMapper.getDbValue(self.orderState) if self.orderState else str(None)) \
		+ ', orderId ' + str(self.orderId)
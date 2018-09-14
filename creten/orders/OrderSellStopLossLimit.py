from orders.Order import Order
from orders.OrderType import OrderType
from orders.OrderSide import OrderSide

class OrderSellStopLossLimit(Order):
	def __init__(self, qty, stopPrice, price):
		super(OrderSellStopLossLimit, self).__init__(OrderSide.SELL, OrderType.STOP_LOSS_LIMIT, qty = qty, stopPrice = stopPrice, price = price)
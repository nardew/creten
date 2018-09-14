from orders.Order import Order
from orders.OrderType import OrderType
from orders.OrderSide import OrderSide

class OrderBuyStopLossLimit(Order):
	def __init__(self, qty, stopPrice, price):
		super(OrderBuyStopLossLimit, self).__init__(OrderSide.BUY, OrderType.STOP_LOSS_LIMIT, qty = qty, stopPrice = stopPrice, price = price)
from orders.Order import Order
from orders.OrderType import OrderType
from orders.OrderSide import OrderSide

class OrderBuyLimit(Order):
	def __init__(self, qty, price):
		super(OrderBuyLimit, self).__init__(OrderSide.BUY, OrderType.LIMIT, qty = qty, price = price)
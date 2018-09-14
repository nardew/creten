from orders.Order import Order
from orders.OrderType import OrderType
from orders.OrderSide import OrderSide

class OrderSellLimit(Order):
	def __init__(self, qty, price):
		super(OrderSellLimit, self).__init__(OrderSide.SELL, OrderType.LIMIT, qty = qty, price = price)
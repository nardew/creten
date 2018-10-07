from orders.Order import Order
from orders.OrderType import OrderType
from orders.OrderSide import OrderSide

class OrderBuyTakeProfitLimit(Order):
	def __init__(self, qty, stopPrice, price):
		super(OrderBuyTakeProfitLimit, self).__init__(OrderSide.BUY, OrderType.TAKE_PROFIT_LIMIT, qty = qty, stopPrice = stopPrice, price = price)
from orders.Order import Order
from orders.OrderType import OrderType
from orders.OrderSide import OrderSide

class OrderSellTakeProfitLimit(Order):
	def __init__(self, qty, stopPrice, price):
		super(OrderSellTakeProfitLimit, self).__init__(OrderSide.SELL, OrderType.TAKE_PROFIT_LIMIT, qty = qty, stopPrice = stopPrice, price = price)
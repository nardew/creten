from orders.Order import Order
from orders.OrderType import OrderType
from orders.OrderSide import OrderSide

class OrderBuyMarket(Order):
	def __init__(self, qty):
		super(OrderBuyMarket, self).__init__(OrderSide.BUY, OrderType.MARKET, qty = qty)
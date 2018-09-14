from orders.Order import Order
from orders.OrderType import OrderType
from orders.OrderSide import OrderSide

class OrderSellMarket(Order):
	def __init__(self, qty):
		super(OrderSellMarket, self).__init__(OrderSide.SELL, OrderType.MARKET, qty = qty)
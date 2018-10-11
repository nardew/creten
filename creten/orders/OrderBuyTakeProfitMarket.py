from orders.Order import Order
from orders.OrderType import OrderType
from orders.OrderSide import OrderSide

class OrderBuyTakeProfitMarket(Order):
	def __init__(self, qty, stopPrice):
		super(OrderBuyTakeProfitMarket, self).__init__(OrderSide.BUY, OrderType.TAKE_PROFIT_MARKET, qty = qty, stopPrice = stopPrice)
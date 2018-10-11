from orders.Order import Order
from orders.OrderType import OrderType
from orders.OrderSide import OrderSide

class OrderSellTakeProfitMarket(Order):
	def __init__(self, qty, stopPrice):
		super(OrderSellTakeProfitMarket, self).__init__(OrderSide.SELL, OrderType.TAKE_PROFIT_MARKET, qty = qty, stopPrice = stopPrice)
from orders.Order import Order
from orders.OrderType import OrderType
from orders.OrderSide import OrderSide

class OrderSellStopLossMarket(Order):
	def __init__(self, qty, stopPrice):
		super(OrderSellStopLossMarket, self).__init__(OrderSide.SELL, OrderType.STOP_LOSS_MARKET, qty = qty, stopPrice = stopPrice)
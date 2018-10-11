from orders.Order import Order
from orders.OrderType import OrderType
from orders.OrderSide import OrderSide

class OrderBuyStopLossMarket(Order):
	def __init__(self, qty, stopPrice):
		super(OrderBuyStopLossMarket, self).__init__(OrderSide.BUY, OrderType.STOP_LOSS_MARKET, qty = qty, stopPrice = stopPrice)
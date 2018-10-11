from clients.BinanceClient import BinanceClient
from orders.OrderResponse import OrderResponse
from orders.OrderState import OrderState
from orders.OrderType import OrderType
from orders.OrderSide import OrderSide

class BinanceBacktestClient(BinanceClient):
	def __init__(self, apiKey, secKey, exchangeConfigPath):
		super(BinanceBacktestClient, self).__init__(apiKey, secKey, exchangeConfigPath)

	def createOrder(self, orderSide, orderType, baseAsset, quoteAsset, qty, stopPrice, price, clientOrderId):
		orderResponse = OrderResponse(baseAsset = baseAsset, quoteAsset = quoteAsset, orderSide = orderSide,
		                              orderType = orderType, price = price, origQty = qty,
		                              lastExecutedQty = 0, sumExecutedQty = 0,
		                              orderState = OrderState.OPENED, clientOrderId = clientOrderId,
		                              extOrderRef = clientOrderId)

		return orderResponse

	def cancelOrder(self, baseAsset, quoteAsset, clientOrderId = None, extOrderRef = None):
		return OrderResponse(baseAsset = baseAsset, quoteAsset = quoteAsset, orderState = OrderState.OPENED, clientOrderId = clientOrderId,
		                              extOrderRef = clientOrderId)

from clients.BinanceClient import BinanceClient
from orders.OrderResponse import OrderResponse
from orders.OrderState import OrderState
from orders.OrderType import OrderType
from orders.OrderSide import OrderSide

class BinanceBacktestClient(BinanceClient):
	def __init__(self, apiKey, secKey, exchangeConfigPath):
		super(BinanceBacktestClient, self).__init__(apiKey, secKey, exchangeConfigPath)

	def createBuyMarketOrder(self, baseAsset, quoteAsset, qty, clientOrderId, currMarketPrice = None):
		orderResponse = OrderResponse(baseAsset = baseAsset, quoteAsset = quoteAsset, orderSide = OrderSide.BUY, orderType = OrderType.MARKET, price = currMarketPrice, origQty = qty, lastExecutedQty = qty, sumExecutedQty = qty,
		                              orderState = OrderState.FILLED, clientOrderId = clientOrderId,
		                              extOrderRef = clientOrderId)

		return orderResponse

	def createBuyLimitOrder(self, baseAsset, quoteAsset, qty, price, clientOrderId):
		orderResponse = OrderResponse(baseAsset = baseAsset, quoteAsset = quoteAsset, orderSide = OrderSide.BUY, orderType = OrderType.LIMIT, origQty = qty, lastExecutedQty = 0, sumExecutedQty = 0,
		                              price = price, orderState = OrderState.OPENED, clientOrderId = clientOrderId,
		                              extOrderRef = clientOrderId)

		return orderResponse

	def createBuyStopLossLimitOrder(self, baseAsset, quoteAsset, qty, stopPrice, price, clientOrderId):
		orderResponse = OrderResponse(baseAsset = baseAsset, quoteAsset = quoteAsset, orderSide = OrderSide.BUY, orderType = OrderType.STOP_LOSS_LIMIT, origQty = qty, lastExecutedQty = 0, sumExecutedQty = 0,
		                              price = price, orderState = OrderState.OPENED, clientOrderId = clientOrderId,
		                              extOrderRef = clientOrderId)

		return orderResponse

	def createSellMarketOrder(self, baseAsset, quoteAsset, qty, clientOrderId, currMarketPrice = None):
		orderResponse = OrderResponse(baseAsset = baseAsset, quoteAsset = quoteAsset, orderSide = OrderSide.SELL, orderType = OrderType.MARKET, price = currMarketPrice, origQty = qty, lastExecutedQty = qty, sumExecutedQty = qty,
		                              orderState = OrderState.FILLED, clientOrderId = clientOrderId,
		                              extOrderRef = clientOrderId)

		return orderResponse

	def createSellLimitOrder(self, baseAsset, quoteAsset, qty, price, clientOrderId):
		orderResponse = OrderResponse(baseAsset = baseAsset, quoteAsset = quoteAsset, orderSide = OrderSide.SELL, orderType = OrderType.LIMIT, origQty = qty, lastExecutedQty = 0, sumExecutedQty = 0,
		                              price = price, orderState = OrderState.OPENED, clientOrderId = clientOrderId,
		                              extOrderRef = clientOrderId)

		return orderResponse

	def createSellStopLossLimitOrder(self, baseAsset, quoteAsset, qty, stopPrice, price, clientOrderId):
		orderResponse = OrderResponse(baseAsset = baseAsset, quoteAsset = quoteAsset, orderSide = OrderSide.SELL, orderType = OrderType.STOP_LOSS_LIMIT, origQty = qty, lastExecutedQty = 0, sumExecutedQty = 0,
		                              price = price, orderState = OrderState.OPENED, clientOrderId = clientOrderId,
		                              extOrderRef = clientOrderId)

		return orderResponse

	def cancelOrder(self, baseAsset, quoteAsset, clientOrderId = None, extOrderRef = None):
		return OrderResponse(baseAsset = baseAsset, quoteAsset = quoteAsset, orderState = OrderState.OPENED, clientOrderId = clientOrderId,
		                              extOrderRef = clientOrderId)

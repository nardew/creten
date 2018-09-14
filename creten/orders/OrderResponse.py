class OrderResponse(object):
	def __init__(self, baseAsset = None, quoteAsset = None, orderSide = None, orderType = None, price = None, origQty = None, lastExecutedQty = None,
	             sumExecutedQty = None, orderState = None, orderTmstmp = None,
	             clientOrderId = None, extOrderRef = None, rawData = None):
		self.baseAsset = baseAsset
		self.quoteAsset = quoteAsset
		self.orderSide = orderSide
		self.orderType = orderType
		self.price = price
		self.origQty = origQty
		self.lastExecutedQty = lastExecutedQty
		self.sumExecutedQty = sumExecutedQty
		self.orderState = orderState
		self.extOrderRef = extOrderRef
		self.clientOrderId = clientOrderId
		self.orderTmstmp = orderTmstmp
		self.rawData = rawData

	def getSymbol(self):
		return self.baseAsset + self.quoteAsset

	def getBaseAsset(self):
		return self.baseAsset

	def getQuoteAsset(self):
		return self.quoteAsset

	def getOrderSide(self):
		return self.orderSide

	def getOrderType(self):
		return self.orderType

	def getPrice(self):
		return self.price

	def getOrigQty(self):
		return self.origQty

	def getLastExecutedQty(self):
		return self.lastExecutedQty

	def getSumExecutedQty(self):
		return self.sumExecutedQty

	def getOrderState(self):
		return self.orderState

	def getClientOrderId(self):
		return self.clientOrderId

	def getExtOrderRef(self):
		return self.extOrderRef

	def getRawData(self):
		return self.rawData

	def getOrderTmstmp(self):
		return self.orderTmstmp
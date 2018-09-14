class SymbolRules(object):
	def __init__(self, symbol = None, status = None, baseAssetPrecision = None, quoteAssetPrecision = None, orderTypes = None,
	             icebergAllowed = None, minPrice = None, maxPrice = None, minPriceDenom = None, minQty = None, maxQty = None,
	             minQtyDenom = None, minNotional = None):
		self.symbol = symbol
		self.status = status
		self.baseAssetPrecision = baseAssetPrecision
		self.quoteAssetPrecision = quoteAssetPrecision
		self.orderTypes = orderTypes
		self.icebergAllowed = icebergAllowed
		self.minPrice = minPrice
		self.maxPrice = maxPrice
		self.minPriceDenom = minPriceDenom
		self.minQty = minQty
		self.maxQty = maxQty
		self.minQtyDenom = minQtyDenom
		self.minNotional = minNotional
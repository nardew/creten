class Pair(object):
	def __init__(self, baseAsset, quoteAsset):
		self.baseAsset = baseAsset
		self.quoteAsset = quoteAsset

	def getBaseAsset(self):
		return self.baseAsset

	def getQuoteAsset(self):
		return self.quoteAsset

	def getSymbol(self):
		return self.baseAsset + self.quoteAsset
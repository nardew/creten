class Trade(object):
	def __init__(self, tradeId = None, baseAsset = None, quoteAsset = None, initTmstmp = None):
		self.tradeId = tradeId
		self.baseAsset = baseAsset
		self.quoteAsset = quoteAsset
		self.initTmstmp = initTmstmp

	def setFromEntity(self, entity):
		self.tradeId = entity.trade_id
		self.baseAsset = entity.base_asset
		self.quoteAsset = entity.quote_asset
		self.initTmstmp = entity.init_tmstmp

	def getTradeId(self):
		return self.tradeId

	def getBaseAsset(self):
		return self.baseAsset

	def getQuoteAsset(self):
		return self.quoteAsset

	def getInitTmstmp(self):
		return self.initTmstmp
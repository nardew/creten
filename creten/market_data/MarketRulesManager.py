from common.Logger import Logger

class MarketRulesManager(object):
	def __init__(self, exchangeClient):
		self.exchangeClient = exchangeClient

		self.symbolRules = {}
		self.commission = 0.0

		self.log = Logger(logForceDebug = False)

	def init(self, symbols):
		rules = self.exchangeClient.getExchangeInfo(symbols)

		for rule in rules:
			self.log.debug('Market rules for ' + str(rule.symbol) + ':')
			self.log.debug('\tTrading status: ' + str(rule.status))
			self.log.debug('\tQuote asset precision: ' + str(rule.quoteAssetPrecision))
			self.log.debug('\tBase asset precision: ' + str(rule.baseAssetPrecision))
			self.log.debug('\tOrder types: ' + str(rule.orderTypes))
			self.log.debug('\tIceberg allowed: ' + str(rule.icebergAllowed))
			self.log.debug('\tMin price: ' + str(rule.minPrice))
			self.log.debug('\tMax price: ' + str(rule.maxPrice))
			self.log.debug('\tMin price denomination: ' + str(rule.minPriceDenom))
			self.log.debug('\tMin quantity: ' + str(rule.minQty))
			self.log.debug('\tMax quantity: ' + str(rule.maxQty))
			self.log.debug('\tMin quantity denomination: ' + str(rule.minQtyDenom))
			self.log.debug('\tMin notional: ' + str(rule.minNotional))

			self.symbolRules[rule.symbol] = rule

	def getSymbolRules(self, baseAsset, quoteAsset):
		return self.symbolRules[baseAsset + quoteAsset]

	def setCommission(self, commission):
		self.commission = commission

	def getCommission(self):
		return self.commission
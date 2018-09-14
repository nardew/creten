import os
import json
import jsonschema
from abc import ABCMeta, abstractmethod
from common.Logger import Logger
from json_schemas import ExchangeConfigSchema

class ExchangeClient(object):
	__metaclass__ = ABCMeta

	def __init__(self, exchangeConfigPath):
		self.log = Logger(logForceDebug = False)

		self.exchangeConf = None
		if exchangeConfigPath:
			self.log.info('')
			self.log.info("Loading exchange configuration file '" + exchangeConfigPath + "'")
			if not os.path.isfile(exchangeConfigPath):
				raise Exception("Exchange configuration file could not be loaded. '" + os.path.realpath(
					exchangeConfigPath) + "' does not correspond to a valid file.")

			with open(os.path.realpath(exchangeConfigPath)) as myfile:
				self.exchangeConf = json.loads(myfile.read())
				jsonschema.validate(self.exchangeConf, self.getExchangeConfigSchema())
		else:
			self.log.debug("No exchange configuration file provided.")

	def updateSymbolRuleFromConfig(self, symbolRule):
		rules = None
		if self.exchangeConf and "marketRules" in self.exchangeConf:
			for marketRule in self.exchangeConf['marketRules']:
				if marketRule['baseAsset'] + marketRule['quoteAsset'] == symbolRule.symbol:
					rules = marketRule

		if rules:
			self.log.info('Updating market rules from configuration file')
			try:
				symbolRule.baseAssetPrecision = rules['baseAssetPrecision']
				self.log.debug('baseAssetPrecision updated')
			except KeyError:
				pass
			try:
				symbolRule.quoteAssetPrecision = rules['quoteAssetPrecision']
				self.log.debug('quoteAssetPrecision updated')
			except KeyError:
				pass
			try:
				symbolRule.minPrice = rules['minPrice']
				self.log.debug('minPrice updated')
			except KeyError:
				pass
			try:
				symbolRule.maxPrice = rules['maxPrice']
				self.log.debug('maxPrice updated')
			except KeyError:
				pass
			try:
				symbolRule.minPriceDenom = rules['minPriceDenom']
				self.log.debug('minPriceDenom updated')
			except KeyError:
				pass
			try:
				symbolRule.minQty = rules['minQty']
				self.log.debug('minQty updated')
			except KeyError:
				pass
			try:
				symbolRule.maxQty = rules['maxQty']
				self.log.debug('maxQty updated')
			except KeyError:
				pass
			try:
				symbolRule.minQtyDenom = rules['minQtyDenom']
				self.log.debug('minQtyDenom updated')
			except KeyError:
				pass
			try:
				symbolRule.minNotional = rules['minNotional']
				self.log.debug('minNotional updated')
			except KeyError:
				pass

	def getExchangeConfigSchema(self):
		return ExchangeConfigSchema.schema

	@abstractmethod
	def getRawClient(self):
		pass

	@abstractmethod
	def getCandles(self, pair, interval, limit = None, startTime = None, endTime = None):
		pass

	@abstractmethod
	def getExchangeInfo(self, symbols = None):
		pass

	@abstractmethod
	def getPortfolio(self):
		pass

	@abstractmethod
	def createBuyMarketOrder(self, baseAsset, quoteAsset, qty, clientOrderId, currMarketPrice = None):
		pass

	@abstractmethod
	def createBuyLimitOrder(self, baseAsset, quoteAsset, qty, price, clientOrderId):
		pass

	@abstractmethod
	def createBuyStopLossLimitOrder(self, baseAsset, quoteAsset, qty, stopPrice, price, clientOrderId):
		pass

	@abstractmethod
	def createSellMarketOrder(self, baseAsset, quoteAsset, qty, clientOrderId, currMarketPrice = None):
		pass

	@abstractmethod
	def createSellLimitOrder(self, baseAsset, quoteAsset, qty, price, clientOrderId):
		pass

	@abstractmethod
	def createSellStopLossLimitOrder(self, baseAsset, quoteAsset, qty, stopPrice, price, clientOrderId):
		pass

	@abstractmethod
	def cancelOrder(self, baseAsset, quoteAsset, clientOrderId = None, extOrderRef = None):
		pass
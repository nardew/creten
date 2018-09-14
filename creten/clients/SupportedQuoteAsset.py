BINANCE_SUPPORTED_QUOTE_ASSET = {
	'BTC',
	'ETH',
	'USDT',
	'BNB'
}

class SupportedQuoteAsset:
	@staticmethod
	def getQuoteAsset(symbol, supportedAssetMap):
		for val in supportedAssetMap:
			if symbol.endswith(val):
				return val

		return None
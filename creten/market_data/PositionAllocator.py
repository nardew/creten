class PositionAllocator(object):
	def __init__(self, portfolioManager, marketRulesManager):
		self.portfolioManager = portfolioManager
		self.marketRulesManager = marketRulesManager
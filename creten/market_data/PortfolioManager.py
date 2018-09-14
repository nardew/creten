from threading import RLock
from market_data.Position import Position

class PortfolioManager(object):
	def __init__(self, exchangeClient):
		self.exchangeClient = exchangeClient

		self.portfolio = {}

		self.lock = RLock()

	def init(self):
		with self.lock:
			self.portfolio = self.exchangeClient.getPortfolio()

	def addPosition(self, position):
		with self.lock:
			self.portfolio[position.getAsset()] = position

	def getPosition(self, asset):
		with self.lock:
			if not asset in self.portfolio:
				self.portfolio[asset] = Position(asset, 0, 0)

			return self.portfolio[asset]

	def clear(self):
		with self.lock:
			self.portfolio = {}
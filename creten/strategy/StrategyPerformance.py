from datetime import timedelta
from math import sqrt
from prettytable import PrettyTable
from db_managers.TradeManager import TradeManager
from db_entities.db_codes import REF_TRADE_STATE, REF_ORDER_STATE, REF_ORDER_SIDE
from common.Logger import Logger

class StrategyPerformance(object):
	def __init__(self, strategyExecId):
		self.strategyExecId = strategyExecId

		self.log = Logger()

		self.tradeProfits = {}
		self.tradeLength = {}

		self.grossProfit = 0
		self.avgGrossProfit = 0
		self.stdDev = 0
		self.gainLossR = 0
		self.noTrades = 0
		self.win = 0
		self.loss = 0
		self.noWin = 0
		self.noLoss = 0
		self.maxWin = 0
		self.avgWin = 0
		self.maxLoss = 0
		self.avgLoss = 0
		self.maxTradeLength = timedelta(0)
		self.maxTradeLengthStr = None
		self.avgTradeLength = 0
		self.avgTradeLengthStr = None

		self.maxDrawdown = 0
		self.avgDrawdown = 0

		self.sharpRatio = 0

		self._calcStats()

	def getNoTrades(self):
		return self.noTrades

	def getGrossProfit(self):
		return self.grossProfit

	def getAvgGrossProfit(self):
		return self.avgGrossProfit

	def getStdDev(self):
		return self.stdDev

	def getWin(self):
		return self.win

	def getLoss(self):
		return self.loss

	def getNoWin(self):
		return self.noWin

	def getNoLoss(self):
		return self.noLoss

	def getMaxWin(self):
		return self.maxWin

	def getMaxLoss(self):
		return self.maxLoss

	def getAvgWin(self):
		return self.avgWin

	def getAvgLoss(self):
		return self.avgLoss

	def getMaxTradeLengthStr(self):
		return self.maxTradeLengthStr

	def getAvgTradeLengthStr(self):
		return self.avgTradeLengthStr

	def _calcStats(self):
		trades = TradeManager.getAllTrades(strategyExecId = self.strategyExecId, tradeState = REF_TRADE_STATE.CLOSED)

		if len(trades) > 0:
			for trade in trades:
				self.log.debug('Evaluating trade ' + str(trade.trade_id))
				orders = TradeManager.getAllOrders(tradeId = trade.trade_id, orderState = REF_ORDER_STATE.FILLED)

				profit = 0.0
				for order in orders:
					if order.order_side == REF_ORDER_SIDE.BUY:
						profit -= float(order.price) * float(order.qty)
					else:
						profit += float(order.price) * float(order.qty)

				self.tradeProfits[trade.trade_id] = profit

				tradeLength = trade.close_tmstmp - trade.open_tmstmp
				self.tradeLength[trade.trade_id] = tradeLength
				if tradeLength > self.maxTradeLength:
					self.maxTradeLength = tradeLength

				self.grossProfit += profit

				if profit >= 0:
					self.win += profit
					self.noWin += 1

					if profit > self.maxWin:
						self.maxWin = profit
				else:
					self.loss += abs(profit)
					self.noLoss += 1

					if abs(profit) > self.maxLoss:
						self.maxLoss = abs(profit)

			######

			self.avgTradeLength = sum([l.total_seconds() for l in self.tradeLength.values()]) / float(len(trades))

			self.avgWin = self.win / float(self.noWin) if self.noWin > 0 else None
			self.avgLoss = self.loss / float(self.noLoss) if self.noLoss > 0 else None

			self.noTrades = len(trades)
			self.avgGrossProfit = self.grossProfit / float(self.noTrades)

			diff = 0.0
			for profit in self.tradeProfits.values():
				diff += (profit - self.avgGrossProfit) ** 2
			self.stdDev = sqrt(diff / len(self.tradeProfits.values()))

			mtl = self._convertSeconds(self.maxTradeLength.total_seconds())
			self.maxTradeLengthStr = '{} days {}h:{}m:{}s'.format(mtl[0], mtl[1], mtl[2], mtl[3])
			atl = self._convertSeconds(self.avgTradeLength)
			self.avgTradeLengthStr = '{} days {}h:{}m:{}s'.format(atl[0], atl[1], atl[2], atl[3])

	@staticmethod
	def _convertSeconds(totalSeconds):
		days, remainder = divmod(totalSeconds, 86400)
		hours, remainder = divmod(remainder, 60 * 60)
		minutes, seconds = divmod(remainder, 60)

		return int(days), int(hours), int(minutes), int(seconds)

	def printStats2(self):
		self.log.info('Number of trades: ' + str(self.noTrades))
		r = round(100 * self.noWin / float(self.noTrades), 2) if self.noTrades > 0 else 0
		self.log.info('Won trades: ' + str(self.noWin) + ' (' + str(r) + '%)')
		r = round(100 * self.noLoss / float(self.noTrades), 2) if self.noTrades > 0 else 0
		self.log.info('Lost trades: ' + str(self.noLoss) + ' (' + str(r) + '%)')

		self.log.info('')
		self.log.info('Gross profit: ' + str(self.grossProfit))
		self.log.info('Gain: ' + str(self.win))
		self.log.info('Loss: ' + str(self.loss))
		r = self.win / float(self.loss) if self.loss != 0 else 0
		self.log.info('Gain loss ratio: ' + str(r))

		self.log.info('')
		self.log.info('Average gross profit: ' + str(self.avgGrossProfit))
		self.log.info('Max gain: ' + str(self.maxWin))
		self.log.info('Average gain: ' + str(self.avgWin))
		self.log.info('Max loss: ' + str(self.maxLoss))
		self.log.info('Average loss: ' + str(self.avgLoss))

		self.log.info('')
		mtl = self._convertSeconds(self.maxTradeLength.total_seconds())
		self.log.info('Max trade length: ' + '{} days {}h:{}m:{}s'.format(mtl[0], mtl[1], mtl[2], mtl[3]))
		atl = self._convertSeconds(self.avgTradeLength)
		self.log.info('Average trade length: ' + '{} days {}h:{}m:{}s'.format(atl[0], atl[1], atl[2], atl[3]))
		self.log.info('')

	def printStats(self):
		t = PrettyTable()
		t.field_names = ['SEI', 'Trades', 'Won', 'Lost', 'Won [%]', 'Gross profit', 'Gain', 'Loss', 'Gain/Loss',
		                 'Avg gain', 'Max gain', 'Avg loss', 'Max loss', 'Avg trade length', 'Max trade length']

		p = 2

		wonPerc = round(100 * self.getNoWin() / float(self.getNoTrades()), p) if self.getNoTrades() > 0 else None
		gainLossR = round(self.getWin() / self.getLoss(), p) if self.getLoss() else None

		fields = [self.strategyExecId,
		          self.getNoTrades(),
		          self.getNoWin(),
		          self.getNoLoss(),
		          wonPerc,
		          self.getGrossProfit(),
		          round(self.getWin(), p) if self.getWin() else None,
		          round(self.getLoss(), p) if self.getLoss() else None,
		          gainLossR,
		          round(self.getAvgWin(), p) if self.getAvgWin() else None,
		          round(self.getMaxWin(), p) if self.getMaxWin() else None,
		          round(self.getAvgLoss(), p) if self.getAvgLoss() else None,
		          round(self.getMaxLoss(), p) if self.getMaxLoss() else None,
		          self.getAvgTradeLengthStr(),
		          self.getMaxTradeLengthStr()]

		t.add_row(fields)

		self.log.info(t)
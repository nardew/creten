from indicators.AccuDist import AccuDist
from indicators.ADX import ADX
from indicators.ALMA import ALMA
from indicators.AO import AO
from indicators.ATR import ATR
from indicators.BB import BB
from indicators.CandleProps import CandleProps
from indicators.ChaikinOsc import ChaikinOsc
from indicators.DEMA import DEMA
from indicators.DonchianChannels import DonchianChannels
from indicators.EMA import EMA
from indicators.HMA import HMA
from indicators.Ichimoku import Ichimoku
from indicators.KeltnerChannels import KeltnerChannels
from indicators.KST import KST
from indicators.MACD import MACD
from indicators.MassIndex import MassIndex
from indicators.OBV import OBV
from indicators.Pivots import Pivots
from indicators.PivotsHL import PivotsHL
from indicators.RSI import RSI
from indicators.ROC import ROC
from indicators.SAR import SAR
from indicators.SFX import SFX
from indicators.SMA import SMA
from indicators.SMMA import SMMA
from indicators.SOBV import SOBV
from indicators.Stoch import Stoch
from indicators.StochRSI import StochRSI
from indicators.TEMA import TEMA
from indicators.UO import UO
from indicators.VWMA import VWMA
from indicators.WMA import WMA

class IndicatorManager:
	def __init__(self, candleMap):
		self.candleMap = candleMap

		self.indMap = {}

	def getIndKey(self, *parms):
		key = ''
		for parm in parms:
			key += 'X' + str(parm)

		return key

	def getCandles(self, symbol, cretenInterval):
		candleMapKey = symbol + str(cretenInterval)
		return self.candleMap[candleMapKey]

	def setupIndMap(self, symbol, cretenInterval):
		if not symbol in self.indMap:
			self.indMap[symbol] = {}

		if not cretenInterval in self.indMap[symbol]:
			self.indMap[symbol][cretenInterval] = {}

	def getAccuDist(self, cretenInterval, symbol):
		self.setupIndMap(symbol, cretenInterval)
		indKey = self.getIndKey('AccuDist')
		if not indKey in self.indMap[symbol][cretenInterval]:
			self.indMap[symbol][cretenInterval][indKey] = AccuDist(self.getCandles(symbol, cretenInterval))

		return self.indMap[symbol][cretenInterval][indKey]

	def getADX(self, cretenInterval, symbol, periodDI, periodADX):
		self.setupIndMap(symbol, cretenInterval)
		indKey = self.getIndKey('ADX', periodDI, periodADX)
		if not indKey in self.indMap[symbol][cretenInterval]:
			self.indMap[symbol][cretenInterval][indKey] = ADX(periodDI, periodADX, self.getCandles(symbol, cretenInterval))

		return self.indMap[symbol][cretenInterval][indKey]

	def getALMA(self, cretenInterval, symbol, window, offset, sigma):
		self.setupIndMap(symbol, cretenInterval)
		indKey = self.getIndKey('ALMA', window, offset, sigma)
		if not indKey in self.indMap[symbol][cretenInterval]:
			self.indMap[symbol][cretenInterval][indKey] = ALMA(window, offset, sigma, self.getCandles(symbol, cretenInterval))

		return self.indMap[symbol][cretenInterval][indKey]

	def getAO(self, cretenInterval, symbol, periodFast, periodSlow):
		self.setupIndMap(symbol, cretenInterval)
		indKey = self.getIndKey('AO', periodFast, periodSlow)
		if not indKey in self.indMap[symbol][cretenInterval]:
			self.indMap[symbol][cretenInterval][indKey] = AO(periodFast, periodSlow, self.getCandles(symbol, cretenInterval))

		return self.indMap[symbol][cretenInterval][indKey]

	def getATR(self, cretenInterval, symbol, period):
		self.setupIndMap(symbol, cretenInterval)
		indKey = self.getIndKey('ATR', period)
		if not indKey in self.indMap[symbol][cretenInterval]:
			self.indMap[symbol][cretenInterval][indKey] = ATR(period, self.getCandles(symbol, cretenInterval))

		return self.indMap[symbol][cretenInterval][indKey]

	def getBB(self, cretenInterval, symbol, period, stdDevMult):
		self.setupIndMap(symbol, cretenInterval)
		indKey = self.getIndKey('BB', period, stdDevMult)
		if not indKey in self.indMap[symbol][cretenInterval]:
			self.indMap[symbol][cretenInterval][indKey] = BB(period, stdDevMult, self.getCandles(symbol, cretenInterval))

		return self.indMap[symbol][cretenInterval][indKey]

	def getChaikinOsc(self, cretenInterval, symbol, periodFast, periodSlow):
		self.setupIndMap(symbol, cretenInterval)
		indKey = self.getIndKey('ChaikinOsc', periodFast, periodSlow)
		if not indKey in self.indMap[symbol][cretenInterval]:
			self.indMap[symbol][cretenInterval][indKey] = ChaikinOsc(periodFast, periodSlow, self.getCandles(symbol, cretenInterval))

		return self.indMap[symbol][cretenInterval][indKey]

	def getSMA(self, cretenInterval, symbol, period):
		self.setupIndMap(symbol, cretenInterval)
		indKey = self.getIndKey('SMA', period)
		if not indKey in self.indMap[symbol][cretenInterval]:
			self.indMap[symbol][cretenInterval][indKey] = SMA(period, self.getCandles(symbol, cretenInterval))

		return self.indMap[symbol][cretenInterval][indKey]

	def getEMA(self, cretenInterval, symbol, period):
		self.setupIndMap(symbol, cretenInterval)
		indKey = self.getIndKey('EMA', period)
		if not indKey in self.indMap[symbol][cretenInterval]:
			self.indMap[symbol][cretenInterval][indKey] = EMA(period, self.getCandles(symbol, cretenInterval))

		return self.indMap[symbol][cretenInterval][indKey]

	def getIchimoku(self, cretenInterval, symbol, kijunPeriod, tenkanPeriod, chikouLagPeriod, senkouSlowPeriod, senkouLookUpPeriod):
		self.setupIndMap(symbol, cretenInterval)
		indKey = self.getIndKey('Ichimoku', kijunPeriod, tenkanPeriod, chikouLagPeriod, senkouSlowPeriod, senkouLookUpPeriod)
		if not indKey in self.indMap[symbol][cretenInterval]:
			self.indMap[symbol][cretenInterval][indKey] = Ichimoku(kijunPeriod, tenkanPeriod, chikouLagPeriod, senkouSlowPeriod, senkouLookUpPeriod, self.getCandles(symbol, cretenInterval))

		return self.indMap[symbol][cretenInterval][indKey]

	def getDonchianChannels(self, cretenInterval, symbol, period):
		self.setupIndMap(symbol, cretenInterval)
		indKey = self.getIndKey('DonchianChannels', period)
		if not indKey in self.indMap[symbol][cretenInterval]:
			self.indMap[symbol][cretenInterval][indKey] = DonchianChannels(period, self.getCandles(symbol, cretenInterval))

		return self.indMap[symbol][cretenInterval][indKey]

	def getKeltnerChannels(self, cretenInterval, symbol, maPeriod, atrPeriod, atrMultUp, atrMultDown):
		self.setupIndMap(symbol, cretenInterval)
		indKey = self.getIndKey('KeltnerChannels', maPeriod, atrPeriod, atrMultUp, atrMultDown)
		if not indKey in self.indMap[symbol][cretenInterval]:
			self.indMap[symbol][cretenInterval][indKey] = KeltnerChannels(maPeriod, atrPeriod, atrMultUp, atrMultDown, self.getCandles(symbol, cretenInterval))

		return self.indMap[symbol][cretenInterval][indKey]

	def getKST(self, cretenInterval, symbol, roc1Period, roc1MAPeriod, roc2Period, roc2MAPeriod, roc3Period, roc3MAPeriod, roc4Period, roc4MAPeriod, signalPeriod):
		self.setupIndMap(symbol, cretenInterval)
		indKey = self.getIndKey('KST', roc1Period, roc1MAPeriod, roc2Period, roc2MAPeriod, roc3Period, roc3MAPeriod, roc4Period, roc4MAPeriod, signalPeriod)
		if not indKey in self.indMap[symbol][cretenInterval]:
			self.indMap[symbol][cretenInterval][indKey] = KST(roc1Period, roc1MAPeriod, roc2Period, roc2MAPeriod, roc3Period, roc3MAPeriod, roc4Period, roc4MAPeriod, signalPeriod, self.getCandles(symbol, cretenInterval))

		return self.indMap[symbol][cretenInterval][indKey]

	def getDEMA(self, cretenInterval, symbol, period):
		self.setupIndMap(symbol, cretenInterval)
		indKey = self.getIndKey('DEMA', period)
		if not indKey in self.indMap[symbol][cretenInterval]:
			self.indMap[symbol][cretenInterval][indKey] = DEMA(period, self.getCandles(symbol, cretenInterval))

		return self.indMap[symbol][cretenInterval][indKey]

	def getHMA(self, cretenInterval, symbol, period):
		self.setupIndMap(symbol, cretenInterval)
		indKey = self.getIndKey('HMA', period)
		if not indKey in self.indMap[symbol][cretenInterval]:
			self.indMap[symbol][cretenInterval][indKey] = HMA(period, self.getCandles(symbol, cretenInterval))

		return self.indMap[symbol][cretenInterval][indKey]

	def getSMMA(self, cretenInterval, symbol, period):
		self.setupIndMap(symbol, cretenInterval)
		indKey = self.getIndKey('SMMA', period)
		if not indKey in self.indMap[symbol][cretenInterval]:
			self.indMap[symbol][cretenInterval][indKey] = SMMA(period, self.getCandles(symbol, cretenInterval))

		return self.indMap[symbol][cretenInterval][indKey]

	def getOBV(self, cretenInterval, symbol):
		self.setupIndMap(symbol, cretenInterval)
		indKey = self.getIndKey('OBV')
		if not indKey in self.indMap[symbol][cretenInterval]:
			self.indMap[symbol][cretenInterval][indKey] = OBV(self.getCandles(symbol, cretenInterval))

		return self.indMap[symbol][cretenInterval][indKey]

	def getSOBV(self, cretenInterval, symbol, period):
		self.setupIndMap(symbol, cretenInterval)
		indKey = self.getIndKey('SOBV', period)
		if not indKey in self.indMap[symbol][cretenInterval]:
			self.indMap[symbol][cretenInterval][indKey] = SOBV(period, self.getCandles(symbol, cretenInterval))

		return self.indMap[symbol][cretenInterval][indKey]

	def getRSI(self, cretenInterval, symbol, period):
		self.setupIndMap(symbol, cretenInterval)
		indKey = self.getIndKey('RSI', period)
		if not indKey in self.indMap[symbol][cretenInterval]:
			self.indMap[symbol][cretenInterval][indKey] = RSI(period, self.getCandles(symbol, cretenInterval))

		return self.indMap[symbol][cretenInterval][indKey]

	def getROC(self, cretenInterval, symbol, period):
		self.setupIndMap(symbol, cretenInterval)
		indKey = self.getIndKey('ROC', period)
		if not indKey in self.indMap[symbol][cretenInterval]:
			self.indMap[symbol][cretenInterval][indKey] = ROC(period, self.getCandles(symbol, cretenInterval))

		return self.indMap[symbol][cretenInterval][indKey]

	def getStoch(self, cretenInterval, symbol, period, smoothingPeriod):
		self.setupIndMap(symbol, cretenInterval)
		indKey = self.getIndKey('Stoch', period, smoothingPeriod)
		if not indKey in self.indMap[symbol][cretenInterval]:
			self.indMap[symbol][cretenInterval][indKey] = Stoch(period, smoothingPeriod, self.getCandles(symbol, cretenInterval))

		return self.indMap[symbol][cretenInterval][indKey]

	def getStochRSI(self, cretenInterval, symbol, rsiPeriod, stochPeriod, smoothingPeriodK, smoothingPeriodD):
		self.setupIndMap(symbol, cretenInterval)
		indKey = self.getIndKey('StochRSI', rsiPeriod, stochPeriod, smoothingPeriodK, smoothingPeriodD)
		if not indKey in self.indMap[symbol][cretenInterval]:
			self.indMap[symbol][cretenInterval][indKey] = StochRSI(rsiPeriod, stochPeriod, smoothingPeriodK, smoothingPeriodD, self.getCandles(symbol, cretenInterval))

		return self.indMap[symbol][cretenInterval][indKey]

	def getMACD(self, cretenInterval, symbol, fastPeriod, slowPeriod, signalPeriod):
		self.setupIndMap(symbol, cretenInterval)
		indKey = self.getIndKey('MACD', fastPeriod, slowPeriod, signalPeriod)
		if not indKey in self.indMap[symbol][cretenInterval]:
			self.indMap[symbol][cretenInterval][indKey] = MACD(fastPeriod, slowPeriod, signalPeriod, self.getCandles(symbol, cretenInterval))

		return self.indMap[symbol][cretenInterval][indKey]

	def getMassIndex(self, cretenInterval, symbol, emaPeriod, demaPeriod, emaRatioPeriod):
		self.setupIndMap(symbol, cretenInterval)
		indKey = self.getIndKey('MassIndex', emaPeriod, demaPeriod, emaRatioPeriod)
		if not indKey in self.indMap[symbol][cretenInterval]:
			self.indMap[symbol][cretenInterval][indKey] = MassIndex(emaPeriod, demaPeriod, emaRatioPeriod, self.getCandles(symbol, cretenInterval))

		return self.indMap[symbol][cretenInterval][indKey]

	def getSAR(self, cretenInterval, symbol, initAccelFactor, accelFactorInc, maxAccelFactor):
		self.setupIndMap(symbol, cretenInterval)
		indKey = self.getIndKey('SAR', initAccelFactor, accelFactorInc, maxAccelFactor)
		if not indKey in self.indMap[symbol][cretenInterval]:
			self.indMap[symbol][cretenInterval][indKey] = SAR(initAccelFactor, accelFactorInc, maxAccelFactor, self.getCandles(symbol, cretenInterval))

		return self.indMap[symbol][cretenInterval][indKey]

	def getSFX(self, cretenInterval, symbol, atrPeriod, stdDevPeriod, stdDevSmoothingPeriod):
		self.setupIndMap(symbol, cretenInterval)
		indKey = self.getIndKey('SFX', atrPeriod, stdDevPeriod, stdDevSmoothingPeriod)
		if not indKey in self.indMap[symbol][cretenInterval]:
			self.indMap[symbol][cretenInterval][indKey] = SFX(atrPeriod, stdDevPeriod, stdDevSmoothingPeriod, self.getCandles(symbol, cretenInterval))

		return self.indMap[symbol][cretenInterval][indKey]

	def getCandleProps(self, cretenInterval, symbol):
		self.setupIndMap(symbol, cretenInterval)
		indKey = self.getIndKey('CandleProps')
		if not indKey in self.indMap[symbol][cretenInterval]:
			self.indMap[symbol][cretenInterval][indKey] = CandleProps(self.getCandles(symbol, cretenInterval))

		return self.indMap[symbol][cretenInterval][indKey]

	def getPivots(self, cretenInterval, symbol, pivotType, periodType):
		self.setupIndMap(symbol, cretenInterval)
		indKey = self.getIndKey('Pivots', pivotType, periodType)
		if not indKey in self.indMap[symbol][cretenInterval]:
			self.indMap[symbol][cretenInterval][indKey] = Pivots(pivotType, periodType, 0, self.getCandles(symbol, cretenInterval))

		return self.indMap[symbol][cretenInterval][indKey]

	def getPivotsHL(self, cretenInterval, symbol, highDist, lowDist):
		self.setupIndMap(symbol, cretenInterval)
		indKey = self.getIndKey('PivotsHL', highDist, lowDist)
		if not indKey in self.indMap[symbol][cretenInterval]:
			self.indMap[symbol][cretenInterval][indKey] = PivotsHL(highDist, lowDist, self.getCandles(symbol, cretenInterval))

		return self.indMap[symbol][cretenInterval][indKey]

	def getTEMA(self, cretenInterval, symbol, period):
		self.setupIndMap(symbol, cretenInterval)
		indKey = self.getIndKey('TEMA', period)
		if not indKey in self.indMap[symbol][cretenInterval]:
			self.indMap[symbol][cretenInterval][indKey] = TEMA(period, self.getCandles(symbol, cretenInterval))

		return self.indMap[symbol][cretenInterval][indKey]

	def getUO(self, cretenInterval, symbol, periodFast, periodMid, periodSlow):
		self.setupIndMap(symbol, cretenInterval)
		indKey = self.getIndKey('UO', periodFast, periodMid, periodSlow)
		if not indKey in self.indMap[symbol][cretenInterval]:
			self.indMap[symbol][cretenInterval][indKey] = UO(periodFast, periodMid, periodSlow, self.getCandles(symbol, cretenInterval))

		return self.indMap[symbol][cretenInterval][indKey]

	def getVWMA(self, cretenInterval, symbol, period):
		self.setupIndMap(symbol, cretenInterval)
		indKey = self.getIndKey('VWMA', period)
		if not indKey in self.indMap[symbol][cretenInterval]:
			self.indMap[symbol][cretenInterval][indKey] = VWMA(period, self.getCandles(symbol, cretenInterval))

		return self.indMap[symbol][cretenInterval][indKey]

	def getWMA(self, cretenInterval, symbol, period):
		self.setupIndMap(symbol, cretenInterval)
		indKey = self.getIndKey('WMA', period)
		if not indKey in self.indMap[symbol][cretenInterval]:
			self.indMap[symbol][cretenInterval][indKey] = WMA(period, self.getCandles(symbol, cretenInterval))

		return self.indMap[symbol][cretenInterval][indKey]

	def addCandle(self, candle):
		if candle.getSymbol() in self.indMap and candle.getInterval() in self.indMap[candle.getSymbol()]:
			for key, ind in self.indMap[candle.getSymbol()][candle.getInterval()].items():
				ind.addValue(candle)

	def updateCandle(self, candle):
		if candle.getSymbol() in self.indMap and candle.getInterval() in self.indMap[candle.getSymbol()]:
			for key, ind in self.indMap[candle.getSymbol()][candle.getInterval()].items():
				ind.updateValue(candle)
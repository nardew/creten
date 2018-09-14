from strategy.CretenStrategy import CretenStrategy
from indicators.Pivots import Pivots
from indicators.PivotsHL import HL
from indicators.SAR import SARValue

class IndicatorMonitor(CretenStrategy):
	def __init__(self, strategyExecId, pair, exchangeClient, marketDataManager, marketRulesManager, portfolioManager, orderManager,
	             params):
		super(IndicatorMonitor, self).__init__(strategyExecId, pair, exchangeClient, marketDataManager, marketRulesManager, portfolioManager, orderManager)

		self.params = params

	@staticmethod
	def getIfExists(array, index):
		val = None
		try:
			val = array[index]
		finally:
			return val

	def printInd(self, label, indicator, index):
		self.log.info("\t" + label + ": " + str(IndicatorMonitor.getIfExists(indicator, index)))

	@staticmethod
	def printPivotsHL(pivotsHL):
		s = ""
		for pivot in pivotsHL:
			if pivot.type == HL.HIGH:
				s += "H " + str(pivot.item.getOpenTime()) + " "
			else:
				s += "L " + str(pivot.item.getOpenTime()) + " "

		return s

	@staticmethod
	def printSAR(sar):
		s = ""
		for x in sar:
			if x.trend == SARValue.UP:
				s += "U "
			else:
				s += "D "

			s += str(x.value) + " "

		return s

	def execute(self, candle):
		self.log.debug(self.__class__.__name__)

		indMgr = self.marketDataManager.getIndicatorManager()

		# indicators
		accuDist = indMgr.getAccuDist(candle.getInterval(), candle.getSymbol())
		adx = indMgr.getADX(candle.getInterval(), candle.getSymbol(), self.params['ADX']['periodDI'], self.params['ADX']['periodADX'])
		alma = indMgr.getALMA(candle.getInterval(), candle.getSymbol(), self.params['ALMA']['window'], self.params['ALMA']['offset'], self.params['ALMA']['sigma'])
		ao = indMgr.getAO(candle.getInterval(), candle.getSymbol(), self.params['AO']['periodFast'], self.params['AO']['periodSlow'])
		atr = indMgr.getATR(candle.getInterval(), candle.getSymbol(), self.params['ATR']['period'])
		bb = indMgr.getBB(candle.getInterval(), candle.getSymbol(), self.params['BB']['period'], self.params['BB']['stdDevMult'])
		chaikinOsc = indMgr.getChaikinOsc(candle.getInterval(), candle.getSymbol(), self.params['ChaikinOsc']['periodFast'], self.params['ChaikinOsc']['periodSlow'])
		ema = indMgr.getEMA(candle.getInterval(), candle.getSymbol(), self.params['EMA']['period'])
		donchianChannels = indMgr.getDonchianChannels(candle.getInterval(), candle.getSymbol(), self.params['DonchianChannels']['period'])
		hma = indMgr.getHMA(candle.getInterval(), candle.getSymbol(), self.params['HMA']['period'])
		ichimoku = indMgr.getIchimoku(candle.getInterval(), candle.getSymbol(), self.params['Ichimoku']['kijunPeriod'], self.params['Ichimoku']['tenkanPeriod'], self.params['Ichimoku']['chikouLagPeriod'], self.params['Ichimoku']['senkouSlowPeriod'], self.params['Ichimoku']['senkouLookUpPeriod'])
		keltnerChannels = indMgr.getKeltnerChannels(candle.getInterval(), candle.getSymbol(), self.params['KeltnerChannels']['maPeriod'], self.params['KeltnerChannels']['atrPeriod'], self.params['KeltnerChannels']['atrMultUp'], self.params['KeltnerChannels']['atrMultDown'])
		kst = indMgr.getKST(candle.getInterval(), candle.getSymbol(), self.params['KST']['roc1Period'], self.params['KST']['roc1MAPeriod'], self.params['KST']['roc2Period'], self.params['KST']['roc2MAPeriod'], self.params['KST']['roc3Period'], self.params['KST']['roc3MAPeriod'], self.params['KST']['roc4Period'], self.params['KST']['roc4MAPeriod'], self.params['KST']['signalPeriod'])
		dema = indMgr.getDEMA(candle.getInterval(), candle.getSymbol(), self.params['DEMA']['period'])
		macd = indMgr.getMACD(candle.getInterval(), candle.getSymbol(), self.params['MACD']['fastPeriod'], self.params['MACD']['slowPeriod'], self.params['MACD']['signalPeriod'])
		massIndex = indMgr.getMassIndex(candle.getInterval(), candle.getSymbol(), self.params['MassIndex']['emaPeriod'], self.params['MassIndex']['demaPeriod'], self.params['MassIndex']['emaRatioPeriod'])
		obv = indMgr.getOBV(candle.getInterval(), candle.getSymbol())
		smma = indMgr.getSMMA(candle.getInterval(), candle.getSymbol(), self.params['RMA']['period'])
		rsi = indMgr.getRSI(candle.getInterval(), candle.getSymbol(), self.params['RSI']['period'])
		roc = indMgr.getROC(candle.getInterval(), candle.getSymbol(), self.params['ROC']['period'])
		sar = indMgr.getSAR(candle.getInterval(), candle.getSymbol(), self.params['SAR']['initAccelFactor'], self.params['SAR']['accelFactorInc'], self.params['SAR']['maxAccelFactor'])
		sfx = indMgr.getSFX(candle.getInterval(), candle.getSymbol(), self.params['SFX']['atrPeriod'], self.params['SFX']['stdDevPeriod'], self.params['SFX']['stdDevSmoothing'])
		sma = indMgr.getSMA(candle.getInterval(), candle.getSymbol(), self.params['SMA']['period'])
		sobv = indMgr.getSOBV(candle.getInterval(), candle.getSymbol(), self.params['SOBV']['period'])
		stoch = indMgr.getStoch(candle.getInterval(), candle.getSymbol(), self.params['Stoch']['stochPeriod'], self.params['Stoch']['smoothingPeriod'])
		stochRsi = indMgr.getStochRSI(candle.getInterval(), candle.getSymbol(), self.params['StochRSI']['rsiPeriod'], self.params['StochRSI']['stochPeriod'], self.params['StochRSI']['smoothingPeriodK'], self.params['StochRSI']['smoothingPeriodD'])
		pivotStd = indMgr.getPivots(candle.getInterval(), candle.getSymbol(), Pivots.PIVOT_TYPE_STANDARD, Pivots.PIVOT_PERIOD_DAY)
		pivotFib = indMgr.getPivots(candle.getInterval(), candle.getSymbol(), Pivots.PIVOT_TYPE_FIBONACCI, Pivots.PIVOT_PERIOD_DAY)
		pivotWoodie = indMgr.getPivots(candle.getInterval(), candle.getSymbol(), Pivots.PIVOT_TYPE_WOODIE, Pivots.PIVOT_PERIOD_DAY)
		pivotCam = indMgr.getPivots(candle.getInterval(), candle.getSymbol(), Pivots.PIVOT_TYPE_CAMARILLA, Pivots.PIVOT_PERIOD_DAY)
		pivotDeMark = indMgr.getPivots(candle.getInterval(), candle.getSymbol(), Pivots.PIVOT_TYPE_DEMARK, Pivots.PIVOT_PERIOD_DAY)
		pivotsHL = indMgr.getPivotsHL(candle.getInterval(), candle.getSymbol(), self.params['PivotsHL']['highDist'], self.params['PivotsHL']['lowDist'])
		tema = indMgr.getTEMA(candle.getInterval(), candle.getSymbol(), self.params['TEMA']['period'])
		uo = indMgr.getUO(candle.getInterval(), candle.getSymbol(), self.params['UO']['periodFast'], self.params['UO']['periodMid'], self.params['UO']['periodSlow'])
		vwma = indMgr.getVWMA(candle.getInterval(), candle.getSymbol(), self.params['VWMA']['period'])
		wma = indMgr.getWMA(candle.getInterval(), candle.getSymbol(), self.params['WMA']['period'])

		if not self.params['onClose'] or (self.params['onClose'] and candle.getIsClosing()):
			self.log.info(str(candle) + (' CLOSED' if candle.getIsClosing() else ''))

			self.printInd("AccuDist", accuDist, -1)

			self.printInd("ADX", adx.getADX(), -1)
			self.printInd("ADX +DI", adx.getPlusDI(), -1)
			self.printInd("ADX -DI", adx.getMinusDI(), -1)

			self.printInd("ALMA", alma, -1)

			self.printInd("AO", ao, -1)

			self.printInd("ATR", atr, -1)

			self.printInd("BB CeB", bb.getCentralBand(), -1)
			self.printInd("BB UpB", bb.getUpperBand(), -1)
			self.printInd("BB LoB", bb.getLowerBand(), -1)

			self.printInd("ChaikinOsc", chaikinOsc, -1)

			self.printInd("EMA", ema, -1)

			self.printInd("DC CeB", donchianChannels.getCentralBand(), -1)
			self.printInd("DC UpB", donchianChannels.getUpperBand(), -1)
			self.printInd("DC LoB", donchianChannels.getLowerBand(), -1)

			self.printInd("DEMA", dema, -1)

			self.printInd("HMA", hma, -1)

			self.printInd("Ichimoku base", ichimoku.getBaseLine(), -1)
			self.printInd("Ichimoku conv", ichimoku.getConversionLine(), -1)
			self.printInd("Ichimoku lag", ichimoku.getLaggingLine(), -1)
			self.printInd("Ichimoku cloud slow", ichimoku.getCloudSlowLine(), -1)
			self.printInd("Ichimoku cloud fast", ichimoku.getCloudFastLine(), -1)

			self.printInd("KeltnerChannels CeB", keltnerChannels.getCentralBand(), -1)
			self.printInd("KeltnerChannels UpB", keltnerChannels.getUpperBand(), -1)
			self.printInd("KeltnerChannels LoB", keltnerChannels.getLowerBand(), -1)

			self.printInd("KST kstLine", kst.getKST(), -1)
			self.printInd("KST signalLine", kst.getSignalLine(), -1)

			self.printInd("MACD macdLine", macd.getMACDLine(), -1)
			self.printInd("MACD signalLine", macd.getSignalLine(), -1)

			self.printInd("Mass index", massIndex.getValues(), -1)

			self.printInd("OBV", obv, -1)

			self.printInd("SMMA", smma, -1)

			self.printInd("RSI", rsi, -1)

			self.printInd("ROC", roc, -1)

			self.log.info("\t" + 'SAR' + ": " + IndicatorMonitor.printSAR(sar.getSAR()[-20:]))

			self.printInd("SFX ATR", sfx.getATR(), -1)
			self.printInd("SFX StdDev", sfx.getStdDev(), -1)
			self.printInd("SFX StdDevSmoothed", sfx.getSMAStdDev(), -1)

			self.printInd("SMA", sma, -1)

			self.printInd("SOBV", sobv.getSOBV(), -1)

			self.printInd("Stoch K", stoch.getValuesK(), -1)
			self.printInd("Stoch D", stoch.getValuesD(), -1)

			self.printInd("StochRSI K", stochRsi.getValuesSlowK(), -1)
			self.printInd("StochRSI D", stochRsi.getValuesD(), -1)

			self.log.info("\t" + 'Pivot Standard' + ": P: " + str(IndicatorMonitor.getIfExists(pivotStd.getPP(), -1)) +
			                ', S1: ' + str(IndicatorMonitor.getIfExists(pivotStd.getS(1), -1)) +
							', S2: ' + str(IndicatorMonitor.getIfExists(pivotStd.getS(2), -1)) +
							', S3: ' + str(IndicatorMonitor.getIfExists(pivotStd.getS(3), -1)) +
                            ', R1: ' + str(IndicatorMonitor.getIfExists(pivotStd.getR(1), -1)) +
                            ', R2: ' + str(IndicatorMonitor.getIfExists(pivotStd.getR(2), -1)) +
                            ', R3: ' + str(IndicatorMonitor.getIfExists(pivotStd.getR(3), -1)))
			self.log.info("\t" + 'Pivot Fibonacci' + ": P: " + str(IndicatorMonitor.getIfExists(pivotFib.getPP(), -1)) +
			              ', S1: ' + str(IndicatorMonitor.getIfExists(pivotFib.getS(1), -1)) +
			              ', S2: ' + str(IndicatorMonitor.getIfExists(pivotFib.getS(2), -1)) +
			              ', S3: ' + str(IndicatorMonitor.getIfExists(pivotFib.getS(3), -1)) +
			              ', R1: ' + str(IndicatorMonitor.getIfExists(pivotFib.getR(1), -1)) +
			              ', R2: ' + str(IndicatorMonitor.getIfExists(pivotFib.getR(2), -1)) +
			              ', R3: ' + str(IndicatorMonitor.getIfExists(pivotFib.getR(3), -1)))
			self.log.info("\t" + 'Pivot Woodie' + ": P: " + str(IndicatorMonitor.getIfExists(pivotWoodie.getPP(), -1)) +
			              ', S1: ' + str(IndicatorMonitor.getIfExists(pivotWoodie.getS(1), -1)) +
			              ', S2: ' + str(IndicatorMonitor.getIfExists(pivotWoodie.getS(2), -1)) +
			              ', S3: ' + str(IndicatorMonitor.getIfExists(pivotWoodie.getS(3), -1)) +
			              ', R1: ' + str(IndicatorMonitor.getIfExists(pivotWoodie.getR(1), -1)) +
			              ', R2: ' + str(IndicatorMonitor.getIfExists(pivotWoodie.getR(2), -1)) +
			              ', R3: ' + str(IndicatorMonitor.getIfExists(pivotWoodie.getR(3), -1)))
			self.log.info("\t" + 'Pivot Camarilla' + ": P: " + str(IndicatorMonitor.getIfExists(pivotCam.getPP(), -1)) +
			              ', S1: ' + str(IndicatorMonitor.getIfExists(pivotCam.getS(1), -1)) +
			              ', S2: ' + str(IndicatorMonitor.getIfExists(pivotCam.getS(2), -1)) +
			              ', S3: ' + str(IndicatorMonitor.getIfExists(pivotCam.getS(3), -1)) +
			              ', S4: ' + str(IndicatorMonitor.getIfExists(pivotCam.getS(4), -1)) +
			              ', R1: ' + str(IndicatorMonitor.getIfExists(pivotCam.getR(1), -1)) +
			              ', R2: ' + str(IndicatorMonitor.getIfExists(pivotCam.getR(2), -1)) +
			              ', R3: ' + str(IndicatorMonitor.getIfExists(pivotCam.getR(3), -1)) +
			              ', R4: ' + str(IndicatorMonitor.getIfExists(pivotCam.getR(4), -1)))
			self.log.info("\t" + 'Pivot DeMark' + ": P: " + str(IndicatorMonitor.getIfExists(pivotDeMark.getPP(), -1)) +
			              ', S1: ' + str(IndicatorMonitor.getIfExists(pivotDeMark.getS(1), -1)) +
			              ', R1: ' + str(IndicatorMonitor.getIfExists(pivotDeMark.getR(1), -1)))

			self.log.info("\t" + 'PivotsHL' + ": " + IndicatorMonitor.printPivotsHL(pivotsHL.getPivots()))

			self.printInd("TEMA", tema, -1)

			self.printInd("UO", uo, -1)

			self.printInd("VWMA", vwma, -1)

			self.printInd("WMA", wma, -1)

			self.log.info('')
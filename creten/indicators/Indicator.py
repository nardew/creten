from abc import ABCMeta, abstractmethod
from collections import Sequence

class Indicator(object):
	__metaclass__ = ABCMeta

	def __init__(self):
		self.timeSeries = []
		self.subIndicators = []

	@abstractmethod
	def _calculate(self):
		pass

	def addSubIndicator(self, indicator):
		self.subIndicators.append(indicator)

	def initialize(self, timeSeries):
		self.removeAll()

		if timeSeries:
			for value in timeSeries:
				self.addValue(value)

	def addValue(self, value):
		for subIndicator in self.subIndicators:
			subIndicator.addValue(value)

		self.timeSeries.append(value)
		self._calculate()

	def updateValue(self, value):
		self.removeValue()
		self.addValue(value)

	def removeValue(self):
		for subIndicator in self.subIndicators:
			subIndicator.removeValue()

		self.timeSeries.pop(-1)

	def removeAll(self):
		for subIndicator in self.subIndicators:
			subIndicator.removeAll()

		self.timeSeries = []

	def setTimeSeries(self, timeSeries, initialize = True):
		if initialize:
			self.timeSeries = []
			self.initialize(timeSeries)
		else:
			self.timeSeries = timeSeries


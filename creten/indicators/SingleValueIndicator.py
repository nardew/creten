from abc import ABCMeta, abstractmethod
from collections import Sequence
from indicators.Indicator import Indicator

class SingleValueIndicator(Indicator, Sequence):
	__metaclass__ = ABCMeta

	def __init__(self):
		super(SingleValueIndicator, self).__init__()

		self.values = []

	@abstractmethod
	def _calculate(self):
		pass

	def __getitem__(self, index):
		return self.values[index]

	def __len__(self):
		return len(self.values)

	def removeValue(self):
		super(SingleValueIndicator, self).removeValue()

		if len(self.values) > 0:
			self.values.pop(-1)

	def removeAll(self):
		super(SingleValueIndicator, self).removeAll()

		self.values = []

	def getValues(self):
		return self.values

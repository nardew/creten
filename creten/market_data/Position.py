class Position(object):
	def __init__(self, asset, free, locked = 0, reference = None):
		self.asset = asset
		self.free = free
		self.locked = locked
		self.reference = reference

	def getAsset(self):
		return self.asset

	def getFree(self):
		return self.free

	def getLocked(self):
		return self.locked

	def getReference(self):
		return self.reference

	def setFree(self, free):
		self.free = free

	def setLocked(self, locked):
		self.locked = locked
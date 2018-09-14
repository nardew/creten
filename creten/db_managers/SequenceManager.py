from threading import RLock
from common.Db import Db
from db_entities.Sequence import Sequence

class SequenceManager:
	__singleton_lock = RLock()
	__singleton_instance = None

	SEQ_INCREMENT = 50

	CRETEN_EXEC_ID = 1
	TRADE_ID = 2

	SEQ_COLUMN_MAP = {
		CRETEN_EXEC_ID: "creten_exec_id",
		TRADE_ID: 'trade_id'
	}

	def __init__(self):
		with SequenceManager.__singleton_lock:
			self.seqValMap = {}
			self.seqUsedMap = {}

			seq = Db.Session().query(Sequence).filter().first()
			self.seq = seq

			for key, val in SequenceManager.SEQ_COLUMN_MAP.items():
				self.seqValMap[key] = getattr(seq, val)
				self.seqUsedMap[key] = SequenceManager.SEQ_INCREMENT

	@classmethod
	def instance(cls):
		if not cls.__singleton_instance:
			with cls.__singleton_lock:
				if not cls.__singleton_instance:
					cls.__singleton_instance = cls()
		return cls.__singleton_instance

	@classmethod
	def getSequence(cls, sequenceName):
		with SequenceManager.__singleton_lock:
			i = cls.instance()

			# check if we exhausted cached values
			if i.seqUsedMap[sequenceName] == SequenceManager.SEQ_INCREMENT:
				# update value in the db
				currVal = getattr(i.seq, SequenceManager.SEQ_COLUMN_MAP[sequenceName])
				setattr(i.seq, SequenceManager.SEQ_COLUMN_MAP[sequenceName], currVal + SequenceManager.SEQ_INCREMENT)
				try:
					Db.Session().commit()
				except:
					Db.Session().rollback()
					raise

				# reset cache counter
				i.seqUsedMap[sequenceName] = 0

			i.seqValMap[sequenceName] += 1
			i.seqUsedMap[sequenceName] += 1

			return i.seqValMap[sequenceName]

	@classmethod
	def getCretenExecId(cls):
		with SequenceManager.__singleton_lock:
			return SequenceManager.getSequence(SequenceManager.CRETEN_EXEC_ID)

	@classmethod
	def getTradeId(cls):
		with SequenceManager.__singleton_lock:
			return SequenceManager.getSequence(SequenceManager.TRADE_ID)
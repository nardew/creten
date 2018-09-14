from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
from common.Logger import Logger

class Db:
	engine = None
	user = None
	password = None
	port = None
	host = None
	dbname = None

	Session = None
	Base = None
	metadata = None

	@staticmethod
	def init(engineType, user, password, host, port, db, debug = False):
		Db.engineType = engineType
		Db.user = user
		Db.password = password
		Db.port = port
		Db.host = host
		Db.db = db

		log = Logger()

		if engineType == 'sqlite':
			engineConnStr = engineType + ':///' + db
			engineConnStrLog = engineConnStr
		else:
			engineConnStr = engineType + '://' + user + ':' + password + '@' + host + ':' + str(port) + '/' + db
			engineConnStrLog = engineType + '://' + user + '@' + host + ':' + str(port) + '/' + db

		log.info('Db connection: ' + engineConnStrLog)
		log.debug('Db connection full: ' + engineConnStr)

		engine = create_engine(engineConnStr, echo = debug)
		session_factory = sessionmaker(bind = engine)
		Db.Session = scoped_session(session_factory)

		Db.Base = declarative_base(bind=engine)
		Db.metadata = Db.Base.metadata

	@staticmethod
	@contextmanager
	def session_scope():
		"""Provide a transactional scope around a series of operations."""
		session = Db.Session()
		try:
			yield session
			session.commit()
		except:
			session.rollback()
			raise
		finally:
			session.close()
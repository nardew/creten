from sqlalchemy import Column, DateTime, BigInteger, String, text
from common.Db import Db

class Trade(Db.Base):
	__tablename__ = 'trade'

	trade_id = Column(BigInteger, primary_key=True)
	strategy_exec_id = Column(BigInteger, nullable = False)
	base_asset = Column(String(4), nullable=False)
	quote_asset = Column(String(4), nullable=False)
	isrt_tmstmp = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
	trade_state = Column(String(64), nullable = False)
	lst_upd_tmstmp = Column(DateTime, nullable = False, server_default = text("CURRENT_TIMESTAMP"))
	init_tmstmp = Column(DateTime, nullable = False)
	open_tmstmp = Column(DateTime)
	close_tmstmp = Column(DateTime)
	trade_type = Column(String(64), nullable = False)
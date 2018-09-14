from sqlalchemy import Column, BigInteger, Text, String
from common.Db import Db

class StrategyExec(Db.Base):
    __tablename__ = 'strategy_exec'

    strategy_exec_id = Column(BigInteger, primary_key=True)
    creten_exec_detl_id = Column(BigInteger, nullable = False)
    base_asset = Column(String(4), nullable = False)
    quote_asset = Column(String(4), nullable = False)
    conf = Column(Text, nullable=False)
    dscp = Column(Text, nullable = True)
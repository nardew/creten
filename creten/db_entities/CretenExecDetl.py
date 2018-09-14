from sqlalchemy import Column, DateTime, BigInteger, String, text, Text
from common.Db import Db

class CretenExecDetl(Db.Base):
    __tablename__ = 'creten_exec_detl'

    creten_exec_detl_id = Column(BigInteger, primary_key=True)
    creten_exec_id = Column(BigInteger, nullable = False)
    isrt_tmstmp = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    exec_state = Column(String(64), nullable=False)
    conf = Column(Text, nullable=False)
    interval = Column(String(64), nullable=False)
    start_tmstmp = Column(DateTime, nullable=True)
    end_tmstmp = Column(DateTime, nullable=True)
    dscp = Column(Text, nullable = True)
from sqlalchemy import Column, DateTime, BigInteger, String, text, Text
from common.Db import Db

class CretenExec(Db.Base):
    __tablename__ = 'creten_exec'

    creten_exec_id = Column(BigInteger, primary_key=True)
    isrt_tmstmp = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    exec_type = Column(String(32), nullable = False)
    conf = Column(Text, nullable = False)
    dscp = Column(Text, nullable = True)
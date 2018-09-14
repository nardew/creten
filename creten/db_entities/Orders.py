from sqlalchemy import Column, DateTime, BigInteger, String, text, Numeric
from common.Db import Db

class Orders(Db.Base):
    __tablename__ = 'orders'

    order_id = Column(BigInteger, primary_key=True)
    trade_id = Column(BigInteger, nullable=False)
    order_side = Column(String(64), nullable = False)
    order_type = Column(String(64), nullable=False)
    order_state = Column(String(64), nullable = False)
    qty = Column(Numeric(30,10), nullable=False)
    price = Column(Numeric(30,10))
    stop_price = Column(Numeric(30,10))
    isrt_tmstmp = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    lst_upd_tmstmp = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    ext_order_ref = Column(String(64))
    int_order_ref = Column(String(64))
    init_tmstmp = Column(DateTime, nullable = False)
    open_tmstmp = Column(DateTime)
    filled_tmstmp = Column(DateTime)
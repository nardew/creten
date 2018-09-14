from common.Db import Db
from db_entities.db_codes import REF_ORDER_STATE
from db_entities.Orders import Orders
from db_entities.Trade import Trade
from db_entities.StrategyExec import StrategyExec
from common.ListOperations import makeList

class TradeManager():
	@staticmethod
	def getAllTrades(strategyExecId = None, tradeState = None):
		q = Db.Session().query(Trade)

		if strategyExecId:
			q = q.filter(Trade.strategy_exec_id == strategyExecId)

		if tradeState:
			tradeState = makeList(tradeState)
			q = q.filter(Trade.trade_state.in_(tradeState))

		return q.all()

	@staticmethod
	def getTrade(tradeId):
		trades = Db.Session().query(Trade).filter(Trade.trade_id == tradeId).all()

		if len(trades) == 0:
			raise Exception()

		if len(trades) > 1:
			raise Exception()

		return trades[0]

	@staticmethod
	def getOrder(orderId = None, intOrderRef = None):
		orders = Db.Session().query(Orders)

		if orderId:
			orders = orders.filter(Orders.order_id == orderId)

		if intOrderRef:
			orders = orders.filter(Orders.int_order_ref == intOrderRef)

		orders = orders.all()

		if len(orders) == 0:
			raise Exception()

		if len(orders) > 1:
			raise Exception()

		return orders[0]

	@staticmethod
	def getAllOrders(cretenExecDetlId = None, tradeId = None, orderSide = None, orderType = None, orderState = None):
		q = Db.Session().query(Orders)

		if cretenExecDetlId:
			q = q.filter(StrategyExec.creten_exec_detl_id == cretenExecDetlId, StrategyExec.strategy_exec_id == Trade.strategy_exec_id,
			             Trade.trade_id == Orders.trade_id)

		if tradeId:
			q = q.filter(Orders.trade_id == tradeId)

		if orderSide:
			orderSide = makeList(orderSide)
			q = q.filter(Orders.order_side.in_(orderSide))

		if orderType:
			orderType = makeList(orderType)
			q = q.filter(Orders.order_type.in_(orderType))

		if orderState:
			orderState = makeList(orderState)
			q = q.filter(Orders.order_state.in_(orderState))

		return q.all()

	@staticmethod
	def getPendOrders(tradeId):
		return Db.Session().query(Orders).filter(
			Orders.trade_id == tradeId,
			Orders.order_state.in_(
				[REF_ORDER_STATE.OPENED,
				 REF_ORDER_STATE.OPEN_PENDING_INT,
				 REF_ORDER_STATE.OPEN_PENDING_EXT,
				 REF_ORDER_STATE.PARTIALLY_FILLED,
				 REF_ORDER_STATE.CANCEL_PENDING_INT,
				 REF_ORDER_STATE.CANCEL_PENDING_EXT])).all()


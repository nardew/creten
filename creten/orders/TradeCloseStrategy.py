from common.Logger import Logger
from orders.TradeCloseType import TradeCloseType
from orders.OrderSide import OrderSide
from orders.OrderState import OrderState
from orders.OrderType import OrderType
from orders.TradeState import TradeState
from db_managers.TradeManager import TradeManager
from db_managers.DbCodeMapper import OrderSideMapper, OrderTypeMapper, OrderStateMapper, TradeStateMapper, TradeCloseTypeMapper

class TradeCloseStrategy:
	log = Logger()

	@staticmethod
	def evalTradeClose(tradeCloseType, trade, orderResponse, orderManager):
		if TradeCloseTypeMapper.getCretenValue(tradeCloseType) == TradeCloseType.ORDER_DRIVEN:
			# start closing trade when SELL is filled and there is no other open SELL
			if orderResponse.getOrderSide() == OrderSide.SELL and \
			     orderResponse.getOrderState() == OrderState.FILLED and \
			     orderResponse.getOrderType() in [OrderType.LIMIT, OrderType.MARKET]:
				pendSellOrders = TradeManager.getAllOrders(tradeId = trade.trade_id,
				                                           orderSide = OrderSideMapper.getDbValue(OrderSide.SELL),
				                                           orderType = OrderTypeMapper.getDbValue(
					                                           [OrderType.LIMIT, OrderType.MARKET]),
				                                           orderState = OrderStateMapper.getDbValue(
					                                           [OrderState.OPENED, OrderState.OPEN_PENDING_EXT]))
				if len(pendSellOrders) == 0:
					openOrders = TradeManager.getPendOrders(trade.trade_id)
					if len(openOrders) > 0:
						TradeCloseStrategy.log.debug('Trade ' + str(trade.trade_id) + ' CLOSING.')
						trade.trade_state = TradeStateMapper.getDbValue(TradeState.CLOSE_PENDING)

						for openOrder in openOrders:
							openOrder.order_state = OrderStateMapper.getDbValue(OrderState.CANCEL_PENDING_INT)
							orderManager.storeOrder(openOrder)
					else:
						orderManager.closeTrade(trade, orderResponse.getOrderTmstmp())

			# start closing trade when first STOP_LOSS_SELL is filled
			elif orderResponse.getOrderSide() == OrderSide.SELL and \
			     orderResponse.getOrderState() == OrderState.FILLED and \
			     orderResponse.getOrderType() in [OrderType.STOP_LOSS_LIMIT, OrderType.STOP_LOSS_MARKET]:
				openOrders = TradeManager.getPendOrders(trade.trade_id)
				if len(openOrders) > 0:
					TradeCloseStrategy.log.debug('Trade ' + str(trade.trade_id) + ' CLOSING.')
					trade.trade_state = TradeStateMapper.getDbValue(TradeState.CLOSE_PENDING)

					for openOrder in openOrders:
						openOrder.order_state = OrderStateMapper.getDbValue(OrderState.CANCEL_PENDING_INT)
						orderManager.storeOrder(openOrder)
				else:
					orderManager.closeTrade(trade, orderResponse.getOrderTmstmp())
		else:
			raise Exception("Unrecognized trade close type [" + tradeCloseType + "]!")
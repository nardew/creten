from decimal import Decimal
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
		# ORDER DRIVEN closing strategy
		# close trade when:
		#   - first SELL order is filled, or
		#   - first STOP LOSS SELL order is filled
		if TradeCloseTypeMapper.getCretenValue(tradeCloseType) == TradeCloseType.ORDER_DRIVEN:
			if orderResponse.getOrderSide() == OrderSide.SELL and \
			     orderResponse.getOrderState() == OrderState.FILLED and \
			     orderResponse.getOrderType() in [OrderType.LIMIT, OrderType.MARKET, OrderType.TAKE_PROFIT_LIMIT, OrderType.TAKE_PROFIT_MARKET]:
				pendSellOrders = TradeManager.getAllOrders(tradeId = trade.trade_id,
				                                           orderSide = OrderSideMapper.getDbValue(OrderSide.SELL),
				                                           orderType = OrderTypeMapper.getDbValue(
					                                           [OrderType.LIMIT, OrderType.MARKET, OrderType.TAKE_PROFIT_LIMIT, OrderType.TAKE_PROFIT_MARKET]),
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

		# QUANTITY DRIVEN closing strategy
		# close trade when:
		#   - sum of bought and sold quantities nets
		elif TradeCloseTypeMapper.getCretenValue(tradeCloseType) == TradeCloseType.QUANTITY_DRIVEN:
			TradeCloseStrategy.log.debug('Evaluate quantity driven trade close condition...')
			filledOrders = TradeManager.getAllOrders(tradeId = trade.trade_id,
			                                         orderState = OrderStateMapper.getDbValue([OrderState.FILLED]))
			qty = Decimal(0)
			for o in filledOrders:
				TradeCloseStrategy.log.debug(str(o.order_side) + ' ' + str(o.qty))
				if o.order_side == OrderSideMapper.getDbValue(OrderSide.BUY):
					qty += o.qty
				else:
					qty -= o.qty
			TradeCloseStrategy.log.debug('Remaining quantity [' + ('{:.' + str(10) + 'f}').format(qty) + ']')

			if qty == 0:
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
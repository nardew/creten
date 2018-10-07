USE `creten`;

DROP TABLE IF EXISTS `creten_exec`;
CREATE TABLE `creten_exec` (
  `creten_exec_id` bigint NOT NULL AUTO_INCREMENT,
  `isrt_tmstmp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `exec_type` varchar(32) NOT NULL,
  `conf` text NOT NULL,
  `dscp` text,
  PRIMARY KEY (`creten_exec_id`)
);

DROP TABLE IF EXISTS `creten_exec_detl`;
CREATE TABLE `creten_exec_detl` (
  `creten_exec_detl_id` bigint NOT NULL AUTO_INCREMENT,
  `creten_exec_id` bigint NOT NULL,
  `isrt_tmstmp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `exec_state` varchar(64) NOT NULL,
  `conf` text NOT NULL,
  `creten_interval` varchar(64) NOT NULL,
  `start_tmstmp` timestamp DEFAULT NULL,
  `end_tmstmp` timestamp DEFAULT NULL,
  `dscp` text,
  PRIMARY KEY (`creten_exec_detl_id`)
);

DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders` (
  `order_id` bigint NOT NULL AUTO_INCREMENT,
  `trade_id` bigint NOT NULL,
  `order_type` varchar(64) NOT NULL,
  `order_state` varchar(64) NOT NULL,
  `qty` decimal(30,10) NOT NULL,
  `price` decimal(30,10) DEFAULT NULL,
  `stop_price` decimal(30,10) DEFAULT NULL,
  `isrt_tmstmp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `lst_upd_tmstmp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `ext_order_ref` varchar(64) DEFAULT NULL,
  `order_side` varchar(64) NOT NULL,
  `int_order_ref` varchar(64) DEFAULT NULL,
  `filled_tmstmp` timestamp DEFAULT NULL,
  `open_tmstmp` timestamp NULL DEFAULT NULL,
  `init_tmstmp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`order_id`),
  UNIQUE KEY `idx_orders_int_order_ref` (`int_order_ref`),
  KEY `idx_orders_trade_id` (`trade_id`)
);

DROP TABLE IF EXISTS `strategy_exec`;
CREATE TABLE `strategy_exec` (
  `strategy_exec_id` bigint NOT NULL AUTO_INCREMENT,
  `creten_exec_detl_id` bigint NOT NULL,
  `conf` text NOT NULL,
  `dscp` text,
  `base_asset` varchar(4) NOT NULL,
  `quote_asset` varchar(4) NOT NULL,
  `trade_close_type` varchar(64) NOT NULL,
  PRIMARY KEY (`strategy_exec_id`),
  KEY `idx_strategy_exec_creten_exec_detl_id` (`creten_exec_detl_id`)
);

DROP TABLE IF EXISTS `trade`;
CREATE TABLE `trade` (
  `trade_id` bigint NOT NULL AUTO_INCREMENT,
  `strategy_exec_id` bigint NOT NULL,
  `base_asset` varchar(4) NOT NULL,
  `quote_asset` varchar(4) NOT NULL,
  `isrt_tmstmp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `trade_state` varchar(64) NOT NULL,
  `lst_upd_tmstmp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `open_tmstmp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `close_tmstmp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `trade_type` varchar(64) NOT NULL,
  `init_tmstmp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`trade_id`),
  KEY `index2` (`trade_state`),
  KEY `idx_trade_strategy_exec_id` (`strategy_exec_id`)
);
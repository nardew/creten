DROP TABLE IF EXISTS "creten_exec";
CREATE TABLE "creten_exec" (
  "creten_exec_id" bigserial,
  "isrt_tmstmp" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "exec_type" varchar(32) NOT NULL,
  "conf" text NOT NULL,
  "dscp" text
);

DROP TABLE IF EXISTS "creten_exec_detl";
CREATE TABLE "creten_exec_detl" (
  "creten_exec_detl_id" bigserial,
  "creten_exec_id" bigint NOT NULL,
  "isrt_tmstmp" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "exec_state" varchar(64) NOT NULL,
  "interval" varchar(64) NOT NULL,
  "conf" text NOT NULL,
  "start_tmstmp" timestamp DEFAULT NULL,
  "end_tmstmp" timestamp DEFAULT NULL,
  "dscp" text
);

DROP TABLE IF EXISTS "orders";
CREATE TABLE "orders" (
  "order_id" bigserial,
  "trade_id" bigint NOT NULL,
  "order_type" varchar(64) NOT NULL,
  "order_state" varchar(64) NOT NULL,
  "qty" decimal(30,10) NOT NULL,
  "price" decimal(30,10) DEFAULT NULL,
  "stop_price" decimal(30,10) DEFAULT NULL,
  "isrt_tmstmp" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "lst_upd_tmstmp" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "ext_order_ref" varchar(64) DEFAULT NULL,
  "order_side" varchar(64) NOT NULL,
  "int_order_ref" varchar(64) DEFAULT NULL,
  "filled_tmstmp" timestamp DEFAULT NULL,
  "open_tmstmp" timestamp NULL DEFAULT NULL,
  "init_tmstmp" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);
DROP INDEX IF EXISTS "idx_orders_int_order_ref";
CREATE UNIQUE INDEX "idx_orders_int_order_ref" on "orders" ("int_order_ref");
DROP INDEX IF EXISTS "idx_orders_trade_id";
CREATE INDEX "idx_orders_trade_id" on "orders" ("trade_id");

DROP TABLE IF EXISTS "strategy_exec";
CREATE TABLE "strategy_exec" (
  "strategy_exec_id" bigserial,
  "creten_exec_detl_id" bigint NOT NULL,
  "conf" text NOT NULL,
  "dscp" text,
  "base_asset" varchar(4) NOT NULL,
  "quote_asset" varchar(4) NOT NULL
);
DROP INDEX IF EXISTS "idx_strategy_exec_creten_exec_detl_id";
CREATE INDEX "idx_strategy_exec_creten_exec_detl_id" on "strategy_exec" ("creten_exec_detl_id");

DROP TABLE IF EXISTS "trade";
CREATE TABLE "trade" (
  "trade_id" bigserial,
  "strategy_exec_id" bigint NOT NULL,
  "base_asset" varchar(4) NOT NULL,
  "quote_asset" varchar(4) NOT NULL,
  "isrt_tmstmp" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "trade_state" varchar(64) NOT NULL,
  "lst_upd_tmstmp" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "open_tmstmp" timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  "close_tmstmp" timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  "trade_type" varchar(64) NOT NULL,
  "init_tmstmp" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);
DROP INDEX IF EXISTS "idx_trade_trade_state";
CREATE INDEX "idx_trade_trade_state" on "trade" ("trade_state");
DROP INDEX IF EXISTS "idx_trade_strategy_exec_id";
CREATE INDEX "idx_trade_strategy_exec_id" on "trade" ("strategy_exec_id");
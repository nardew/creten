![CRETEN](./logo_bw.png) CRETEN 
====


[![](https://img.shields.io/badge/python-2.7-blue.svg)](https://www.python.org/downloads/release/python-2715/) [![](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-365/)

_**Cr**ypto **E**xchange **T**rading **En**gine_, or **_creten_** for short, is a modern Python-based framework for developers and curious minds of all sorts who are after an elegant system to design, backtest and execute trading strategies in the evergrowing crypto market.

First of all, it is important to understand that `creten` is **not** a trading bot that you install and become rich, though there are many exemplary strategies bundled with the framework. The ultimate mission of `creten` is to equip developers with means (a framework) enabling them to quickly develop their own trading strategies, evaluate their performance via backtesting and realtime testing (paper trading) and once the state-of-the art strategy proves profitable, execute them in real crypto market.

## Features

Devising a competitive trading strategy which is profitable long term and which outsmarts other participants in the market is unfortunately something that `creten` will not help you with. What it **will** help you with is to materialize your idea into a concise Python code, provide you with many standard and less standard technical indicators, let you test your strategy thoroughly on online or offline data, automate execution for as many currency pairs, time windows and timeframes as desirable and finally record statistics from every single run for sake of performance comparison. Once confidence is reached, `creten` can run as a trading bot in real market according to your strategy.

#### Execution modes

`creten` can run in three modes:
1. **backtest**

   Backtesting allows you to evaluate performance of your strategy on historical data. You have an option to backtest on offline data (stored in a csv file or database) or on online data downloaded from an exchange. The main parameters of backtest will be currency pair(s) (ETH/BTC, BTC/USDT, ADA/ETH, ...), time window of the data (arbitrary time span, the only limitation is your data source) and timeframe (from 1 minute up to 1 month).
   
1. **realtime test (paper trading)**

   Unlike backting, realtime testing consists of listening to realtime market data feed (i.e. prices of the selected currency pairs) and simulating your strategy calls under real conditions. This type of testing is closer to real trading than backtesting is since you have access and can react to online data, such as prices and depth, in realtime. The results can be sometimes significantly different from backtesting which bases your calls only on the data captured at the candle close. The obvious disadvantage of realtime testing is the small testing set of input data, unless you leave realtime testing running for days or weeks.

1. **real trader**

   The last and the most exciting mode of `creten` is the real trading where you have skin in the game. Real trading is similar to realtime test, only you trade with real assets. Make sure that you let `creten` trade according to the strategy only if it earns consistently in backtesting and realtime testing. There is no warranty for loss of your resources, please read *Warranty* section carefully.
   
   __*Important note:*__ It goes without saying that `creten` was tested as much as possible in all three modes. Nevertheless, the real trading mode is currently *disabled* by default until `creten` undergoes wider testing from the community under conditions which were not initially assumed.

#### Exchanges

`creten`supports two type of exchanges - offline ones (market data are stored locally) and online ones (market data fetched from the exchange via its API). Following table outlines all exchanges which are currently supported. It is expected that number of supported exchanges will grow with time.

| Name | Type | Support | Description |
| --- | --- | --- | --- | 
| *File* | offline | full | Data are stored in a CSV file with the structure defined in the input configuration file
| *Database* | offline | full | Data are stored in a database file with the structure defined in the input configuration file
| ![binance](https://user-images.githubusercontent.com/1294454/29604020-d5483cdc-87ee-11e7-94c7-d1a8d9169293.jpg) | online | full | 

As you can see only binance online exchange is supported at the moment. binance is the biggest exchange according to the market cap and has complete API, which makes it a natural choice when deciding which exchange to support as a first one.

All exchanges incorporated into `creten` are accessed via websockets if possible to guarantee that your account is not blocked due to high number of requests. This is one of the criteria when considering new exchanges to be added into `creten` in the future.

Currently each exchange is implemented in `creten` separately but our target is to utilise an external package (namely [ccxt](https://github.com/ccxt/ccxt)) which will provide a unified interface to vast variety of online exchanges. The reason why ccxt was not used from the begnning is its lack of full support of websockets (see previous paragraph).  

#### Technical indicators

`creten` provides many buil-in technical indicators. New indicators can be implemented easily or added from an external library. 

| Type | Indicators |
| :---: | --- |
| **trend** | Average Direction Index (ADX) <br> Awesome Oscillator (AO) <br> Ichimoku Kinko Hyo <br> Know Sure Thing (KST) <br> Moving Average Convergence Divergence (MACD) <br> Mass Index <br> Moving Average (ALMA, SMA, SMMA, DEMA, EMA, HMA, TEMA, VWMA, WMA) <br> Parabolic SAR <br> SFX TOR
| **support/resistance** | Pivot (Standard, Fibonnaci, Woodie, DeMark, Camarilla) <br> High/Low Pivots <br> Fibonnaci Retracements
| **momentum** | Chaikin Oscillator <br> Rate of Change (ROC) <br> Relative strength index (RSI) <br> Stochastic Oscillator <br> Stochastic RSI <br> Ultimate oscillator
| **volume** | Accumulation/Distribtuin (ADL) <br> On-balance Volume (OBV)
| **volatility** | Average True Range (ATR) <br> Bollinger Bands (BB) <br> Donchian Channel (DC) <br> Keltner Channel (KC) <br> Standard deviation

#### Order types

When it comes to order types many available open source trading engines provide ability to file buy/sell order at market price, some allow you to create a limit order. While these are sufficient in majority of simpler strategies, more advanced strategies will definitely miss other order types which are supported by many exchanges. Goal of `creten` is to give as much power and freedom to developer as possible and therefore `creten` fully supports following order types:

| Order type | Description |
| --- | --- |
buy/sell market order | buy/sell at the market price (order executed immediately)
buy/sell limit order | buy/sell at specified price (order executed once specified price is reached)
buy/sell stop loss market order | file a buy/sell market order when price reaches specified stop price
buy/sell stop loss limit order | file a buy/sell limit order at specified price when price reaches specified stop price
buy/sell take profit market order | similar to buy/sell stop loss limit order
buy/sell take profit limit order | similar to buy/sell stop loss limit order 

#### Trades vs. orders

Most frameworks you find around view trades as a pair of orders where trade starts with a buy/sell order and ceases with the opposite order. This is perfectly fine for strategies where you repetitively buy and sell as a reaction to current market data. But what if your buying/selling approach is more sophisticated? What if you want to stack buying orders over time, for instance when market is evolving in your favour? Or what if you want to always place both a limit order and a stop loss order at the same time and let either of the orders close the trade? What if you want to add new stop losses as your trade is evolving? Many trading packages with trades formed of only a pair of buy and sell orders will not allow this.

`creten` was specifically designed with above questions in mind from the very beginning and its view of trades is more general. In fact, `creten` defines a trade as a set of orders of arbitrary number. Trade is initiated with the first order and closes when ceratin conditions are met (not necessarily when all orders are executed). To reuse previous example, imagine that your strategy is to first issue together a buy market order and a sell limit order and then with each subsequent candle you place a new stop loss, e.g. using parabolic SAR. It means after 20 candles since the trade has been initiated your trade may still be active and will consit of 20 pending orders and you can continue adding additional orders of all types as you wish. The closing condition for this type of trade is that your (1) sell limit order or (2) stop loss order gets executed. When this happens, `creten` will automatically cancel the remaining pending orders since the trade is not active anymore.

Being able to construct trades from many different orders and even update the set while trade is running gives developer a great opportunity to build his strategy without any limitation.

#### Database engines

Every `creten`'s execution is recorded in the database, including details of execution itself, details of all trades, details of all orders and so on and so forth. In other words, database and data stored in it are crucial driving elements of `creten`.

`creten` is using powerful `SQLAlchemy` ORM framework to abstract interaction with database engine and therefore it is able to run with most of the standard databases seemlessly. Database engines which were successfully tested with `creten` (and hence are officially supported) and for which `creten` contains environment preperation scripts (see *Installation* section) are:
- SQLite
- MySQL
- MariaDB
- PostgreSQL

Supporting a new database engine is straightfowawrd. It is required only to:
- make sure that the database engine is supported by `SQLAlchemy` (which should not be a concern)
- create a new environment preparation DDL script if none of the existing ones can be reused (due to some specificities of the given DDL)

#### Performance evaluation

Due to recording every bit of trading data in the database it is very easy to gather statistics of any kind and evaluate strategy's performance. At the end of backtesting `creten` automaticaly outputs performance parameters of the current run, for realtime testing or trading the parameters need to be retrieved from the database manually (SQL queries are provided with the package, see files in `db_queries/`).

If you want to compare performance of different strategies and for some reason you are not willing to run SQL queries, you can use provided utility `utilities/crestat.py` which displays statistics of the last *X* runs of `creten` (where *X* can be chosen).

Statistics shown after end of backtesting or retrieved via `crestat.py` include total number of trades, number of won trades, gross profit, gain/loss ratio, max and average gain, max and average loss, average trade duration, max trade duration and others.

## Limitations

`creten` is a new project which means there will be technical issues hidden here and there. Although we tried to test the whole application thoroughly the smooth and bugfree execution will be ensured only after some time of public using and testing.

Besides techincal issues there is clearly some functionality still missing. The main gaps as we see them are:
- trading mode is currently disabled, only backtesting and realtime testing is enabled
- only few (one) exchanges are supported at the moment
- only long trades are supported (i.e. no shorting)

All above gaps will be worked on based on the availability and priorities.

## Installation

Following paragraphs will guide you through the exhaustive set of steps to get `creten` running properly. Installation procedure is common for both Python 2.x and Python 3.x (all differences marked where relevant) and is illustrated on Linux/MacOS.

##### 0. Prerequisites

In order to be able to use `creten`, you need have following components installed on your system:
- `git`
- `Python 2.x` or `Python 3.x` (`creten` was intensively tested with `Python 2.7` and `Python 3.6`)
- a database engine (see *Features* section for supported engines)

##### 1. Clone `creten` to your local filesystem

Choose a destination folder where `creten` will be downloaded and execute

`$ git clone git@github.com:nardew/creten.git`

##### 2. Create and enter a Python virtual environment [optional]

Since `creten` uses several external packages, it is recommended to run it in a Python's virtual environment in order to simplify dependency download and resolution. Nevertheless, this step is not mandatory if you are experienced with installation and management of external dependencies.

To create an empty virtual environment, use following commands. If you want learn more about Python's virtual environments consult one of the many online sources.
```
$ virtualenv -p <python_version> <virtual_env_dir>, e.g. virtualenv -p python3 creten_env
$ source creten_env/bin/activate
(creten_env) $
```
If all went well, you should see the name of the virtual environment prepended to your command line.
  
##### 3. Install dependencies
All external dependencies are provided in `creten/requirements.txt` file. To download and install them, run:

`(creten_env) $ pip install -r requirements.txt`

**Note:** The above will download all dependencies but the database interface. Each developer will use the database engine of her/his own choice and it is not desirable to have all of them installed by default. Please install yours manually (e.g. `pip install pymysql` for MySQL).

##### 4. Create a database layout

Based on the database engine of your choice, apply manually one of the DDLs contained in `env_setup` folder:
- MySQL/MariaDB: `env_setup/DDL_MySQL.sql`
- PostgreSQL: `env_setup/DDL_PostgreSQL.sql`
- SQLite: `env_setup/DDL_SQLite.sql`

##### 5. Check `creten`'s help page to verify installation
`(creten_env) creten$ python creten.py -h`

Above command should return description of all command line parameters.

##### 6. Setup environment variable for `creten` root directory

In order to be able to run predefined examples, you need to setup an environment variable which will point to `creten`'s application folder (i.e. the one containing `creten.py` file). This step can be automated by updating the user's profile script. Once the environment variable is defined, source `profile.sh`.

```
(creten_env) $ export CRETEN_APP_ROOT_DIR=<creten application dir>
(creten_env) $ source profile.sh
```

##### 7. Execute one of the bundled examples

The easiest way to verify that `creten` was setup properly is to run one of the provided examples:

- backtest moving average cross strategy on offline data
```
(creten_env) $ cd examples/backtest/file_exchange_ma_cross
(creten_env) examples/backtest/file_exchange_ma_cross $ ./execute.sh
```
- backtest bollinger bounce strategy on binance
```
(creten_env) $ cd examples/backtest/binance_boll_bounce
(creten_env) examples/backtest/binance_boll_bounce $ ./execute.sh
```

After running either of the examples you should see `creten` to execute the selected trading strategy and display results at the end. If it is what happend, then congratulation, you are set to create and execute your own trading strategies.
  
## Usage

Okay, you managed to install `creten` and execute of the examples successfuly. What does it take to create a new strategy from the scratch and backtest it? Keep on reading.  

In the following paragraphs we are going to create a simple strategy based on the RSI indicator. The strategy will first wait until RSI gets oversold (its value decreases below 20) and then it will wait until it gets back over 50. At this point it files a buy market order for 1 BTC against USDT and a stop loss sell order at a price of say 80 USDT lower than the buy price. The strategy will file a sell market order as soon as RSI gets overbought above 80. This strategy will hardly make money consistently but it will serve for illustration of `creten`'s capabilities nicely. The strategy will be backtested on binance between 01/04/2018 and 31/08/2018 at 1 hour timeframe.

In order to create and backtest a strategy, we need to:
1. implement the strategy in Python code
1. create an input JSON file with input configuration such as time window, timeframe and other parameters
1. execute `creten` with above files

First let's start with implementation of a blank strategy which will simply print candle properties of every incoming candle. Each `creten` strategy is represented by a Python class (let's call it `RSIStrategy`) inheriting from `CretenStrategy` class and implementing method `execute(...)`. In the simplest form, a valid strategy class looks like follows (ignore attributes in the constructor for the time being, they are mandatory but out of scope of this discussion):

```python
from strategy.CretenStrategy import CretenStrategy

class RSIStrategy(CretenStrategy):
    def __init__(self, strategyExecId, pair, exchangeClient, marketDataManager, marketRulesManager, portfolioManager, orderManager, params):
	super(RSIStrategy, self).__init__(strategyExecId, pair, exchangeClient, marketDataManager, marketRulesManager, portfolioManager, orderManager)

    def execute(self, candle):
        print(candle)
```

If we backtest this strategy, we will simply see properties of all incoming candles. Let's save the strategy into `creten/strategy_repository/RSIStrategy.py`.

Now on we go with preparation of the input configuration file. Each configuration file is a JSON file with minimal mandatory schema defined in `creten/json_schemas/BacktestSchema.py`. The structure is pretty selfexplanatory, for our example we will use following configuration:

```python
{
    "backtest": [{
        "strategies": [{
            "strategy_name": "RSIStrategy",
        }],
        "pairs": [
            ["BTC", "USDT"]
        ],
        "interval": "1HOUR",
        "start_tmstmp": "20180401000000",
        "end_tmstmp": "20180831000000",
        "portfolio": [{
            "asset": "USDT",
            "quantity": 10000
        }]
    }]
}
```

Above configuration says that we run a (single) backtest of our (single) RSIStrategy on data for (single) BTC/USDT pair between 01/04/2018 and 31/08/2018 at 1 hour timeframe. The reason why we say *single* is that those attributes are arrays and can be provided with multiple input data (multiple backtests on multiple strategies on multiple pairs). We save above configuration into `creten/rsi_input_config.json`.

Before we execute our fresh strategy, we need to make sure that we setup database connection in `creten/common/client_settings.json` properly. Once done, execute `creten` as follows:

`creten $ python creten.py -m backtest -e binance --apikey $APIKEY --seckey $SECKEY --inputconfig rsi_input_config.json`

Ideally, you should see following output:

```
creten v0.1

Time: 2018-09-26 23:11:06.606848
Mode: backtest
Exchange: binance
Global log mode: info
Db connection: mysql+pymysql://creten@127.0.0.1:3306/creten
Loading market rules
Loading market rules completed

Backtesting period: 2018-04-01 00:00:00 - 2018-08-31 00:00:00

Initialize portfolio:
	USDT: 0

Loading historical data for symbol BTCUSDT
Loading historical data completed

Starting backtesting
symbol BTCUSDT, interval 1HOUR, open time 2018-04-01 00:00:00, open 6923.02, high 6987.71, low 6889.71, close 6974.39, close time 2018-04-01 00:59:59.999000, closing True
symbol BTCUSDT, interval 1HOUR, open time 2018-04-01 01:00:00, open 6962.91, high 6990.84, low 6888.53, close 6923.91, close time 2018-04-01 01:59:59.999000, closing True
symbol BTCUSDT, interval 1HOUR, open time 2018-04-01 02:00:00, open 6922.0, high 7040.0, low 6922.0, close 6971.11, close time 2018-04-01 02:59:59.999000, closing True
symbol BTCUSDT, interval 1HOUR, open time 2018-04-01 03:00:00, open 6980.01, high 7049.98, low 6968.26, close 7000.01, close time 2018-04-01 03:59:59.999000, closing True
...
symbol BTCUSDT, interval 1HOUR, open time 2018-08-30 22:00:00, open 6809.98, high 6945.02, low 6800.0, close 6916.01, close time 2018-08-30 22:59:59.999000, closing True
symbol BTCUSDT, interval 1HOUR, open time 2018-08-30 23:00:00, open 6916.01, high 6960.79, low 6909.14, close 6940.98, close time 2018-08-30 23:59:59.999000, closing True
symbol BTCUSDT, interval 1HOUR, open time 2018-08-31 00:00:00, open 6942.12, high 6955.99, low 6922.0, close 6943.12, close time 2018-08-31 00:59:59.999000, closing True

Final balance for USDT: 0

PERFORMANCE
+-----+--------+-----+------+---------+--------------+------+------+-----------+----------+----------+----------+----------+------------------+------------------+
| SEI | Trades | Won | Lost | Won [%] | Gross profit | Gain | Loss | Gain/Loss | Avg gain | Max gain | Avg loss | Max loss | Avg trade length | Max trade length |
+-----+--------+-----+------+---------+--------------+------+------+-----------+----------+----------+----------+----------+------------------+------------------+
| 1   |   0    |  0  |  0   |   None  |      0       | None | None |    None   |   None   |   None   |   None   |   None   |       None       |       None       |
+-----+--------+-----+------+---------+--------------+------+------+-----------+----------+----------+----------+----------+------------------+------------------+
```

As advertised, the strategy simply output properties of the processed candle.

Now we can start tweaking our so-far-blank strategy. We will logically split the strategy into two parts - one part containing a code active when we are *not* in any trade (to test enter conditions of a trade) and another part containing a code active when we *are* in a trade (to test exit conditions of the trade). Our `execute` menthod will look like this:

```python
def execute(self, candle):        
    # Check if we are already in a trade or not. If not, evaluate strategy's ENTRY conditions. If yes, evaluate
    # strategy's EXIT conditions.
    trades = self.getActiveTrades()		
    if len(trades) == 0:
        # we are not in any trade
        pass	    
    else:
        # we are in a trade
        pass
``` 

Recalling design of our strategy, we need at least an RSI indicator and a flag denoting if we entered the oversold region in order to enter a trade. In the following code we initialize RSI indicator, keep track of entering an oversold region and prepare entry and exit conditions of the trade.

```python
def __init__(self, ...):
    super(RSIStrategy, self).__init__(...)

    self.gotOversold = False

def execute(self, candle):
    # Fetch RSI indicators from the cache
    rsi = self.marketDataManager.getIndicatorManager().getRSI(candle.getInterval(), candle.getSymbol(), 14)

    # If RSI indicator does not contain at least 1 value, do not apply strategy at this point
    if not minListLen([rsi], 1):
        return

    self.log.debug("RSI value: " + str(rsi[-1]))

    # Check if we are already in a trade or not. If not, evaluate strategy's ENTRY conditions. If yes, evaluate
    # strategies EXIT conditions.
    trades = self.getActiveTrades()		
    if len(trades) == 0:
        # First check if we moved to the oversold region.
        # If yes, record it in an auxaliary variable gotOversold.
        if not self.gotOversold and rsi[-1] < 20:
            self.gotOversold = True

        # If we entered oversold region (gotOversold = True) and RSI returned back above specified limit,
        # our ENTRY conditions are met and we file opening orders.
        if self.gotOversold and rsi[-1] >= 50:
            # a buy market order of 1 BTC
            # a stoploss sell order at price lower by 80 compared to current price
            pass
    else:
        # If we are in an active trade and RSI got into overbought region, we close the trade by a sell market order
        if rsi[-1] > 80:
            # a sell market order
            pass
            
            # reset gotOversold flag
            self.gotOversold = False
```

The skeleton and all decision points of our strategy are ready. The last missing piece is to fire buy and sell orders. Complete strategy is defined below:

```python
def __init__(self, ...):
    super(RSIStrategy, self).__init__(...)

    self.gotOversold = False

def execute(self, candle):
    # Fetch RSI indicators from the cache
    rsi = self.marketDataManager.getIndicatorManager().getRSI(candle.getInterval(), candle.getSymbol(), 14)

    # If RSI indicator does not contain at least 1 value, do not apply strategy at this point
    if not minListLen([rsi], 1):
        return

    self.log.debug("RSI value: " + str(rsi[-1]))

    # Check if we are already in a trade or not. If not, evaluate strategy's ENTRY conditions. If yes, evaluate
    # strategies EXIT conditions.
    trades = self.getActiveTrades()		
    if len(trades) == 0:
        # First check if we moved to the oversold region.
        # If yes, record it in an auxaliary variable gotOversold.
        if not self.gotOversold and rsi[-1] < 20:
            self.gotOversold = True

        # If we entered oversold region (gotOversold = True) and RSI returned back above specified limit,
        # our ENTRY conditions are met and we file opening orders.
        if self.gotOversold and rsi[-1] >= 50:
            # a buy market order of 1 BTC
            orderBuy = OrderBuyMarket(qty = 1)
            # a stoploss sell order at price lower by 80 compared to current price
            orderStopLoss = OrderSellStopLossLimit(qty = 1, stopPrice = candle.getClose() - 80, price = candle.getClose() - 80)

            # initiate the trade with the two above orders
            self.openTrade(TradeType.LONG, candle, [orderBuy, orderStopLoss])
    else:
        # If we are in an active trade and RSI got into overbought region, we close the trade by a sell market order
        if rsi[-1] > 80:
            # a sell market order
            orderSell = OrderSellMarket(qty = 1)
            self.openOrder(trades[-1], candle, [orderSell])
            
            # reset gotOversold flag
            self.gotOversold = False
```

That's it. With minimum technical knowledge we were able to create a complete trading strategy (and on given input data even profitable one). If you run it with the previosly defined input configuration, you should see following output:

```bash
creten v0.1

Time: 2018-09-26 23:38:40.416168
Mode: backtest
Exchange: binance
Global log mode: info
Db connection: mysql+pymysql://creten@127.0.0.1:3306/creten
Loading market rules
Loading market rules completed

Backtesting period: 2018-04-01 00:00:00 - 2018-08-31 00:00:00

Initialize portfolio:
	USDT: 0

Loading historical data for symbol BTCUSDT
Loading historical data completed

Starting backtesting

>>> [symbol BTCUSDT, interval 1HOUR, open time 2018-05-29 13:00:00, open 7192.13, high 7483.78, low 7185.0, close 7405.61, close time 2018-05-29 13:59:59.999000, closing True]
RSIStrategy: OPEN
Order: orderSide BUY, orderType MARKET, qty 1.00000000, price None, stopPrice None, orderState OPEN_PENDING_INT, orderId 45622
Order: orderSide SELL, orderType STOP_LOSS_LIMIT, qty 1.00000000, price 7325.60000000, stopPrice 7325.60000000, orderState OPEN_PENDING_INT, orderId 45623
Trade 315193 OPENED.
>>> [symbol BTCUSDT, interval 1HOUR, open time 2018-05-30 17:00:00, open 7374.04, high 7382.0, low 7290.0, close 7324.81, close time 2018-05-30 17:59:59.999000, closing True]
Filling stop loss order 45623
Trade 315193 CLOSED.
Gain: -80.01000000

>>> [symbol BTCUSDT, interval 1HOUR, open time 2018-06-18 18:00:00, open 6458.01, high 6687.87, low 6450.0, close 6644.95, close time 2018-06-18 18:59:59.999000, closing True]
RSIStrategy: OPEN
Order: orderSide BUY, orderType MARKET, qty 1.00000000, price None, stopPrice None, orderState OPEN_PENDING_INT, orderId 45624
Order: orderSide SELL, orderType STOP_LOSS_LIMIT, qty 1.00000000, price 6564.94000000, stopPrice 6564.94000000, orderState OPEN_PENDING_INT, orderId 45625
Trade 315194 OPENED.
>>> [symbol BTCUSDT, interval 1HOUR, open time 2018-06-20 03:00:00, open 6670.0, high 6677.65, low 6551.81, close 6618.99, close time 2018-06-20 03:59:59.999000, closing True]
Filling stop loss order 45625
Trade 315194 CLOSED.
Gain: -80.01000000

>>> [symbol BTCUSDT, interval 1HOUR, open time 2018-06-25 13:00:00, open 6182.0, high 6238.0, low 6177.0, close 6232.82, close time 2018-06-25 13:59:59.999000, closing True]
RSIStrategy: OPEN
Order: orderSide BUY, orderType MARKET, qty 1.00000000, price None, stopPrice None, orderState OPEN_PENDING_INT, orderId 45626
Order: orderSide SELL, orderType STOP_LOSS_LIMIT, qty 1.00000000, price 6152.81000000, stopPrice 6152.81000000, orderState OPEN_PENDING_INT, orderId 45627
Trade 315195 OPENED.
>>> [symbol BTCUSDT, interval 1HOUR, open time 2018-06-25 14:00:00, open 6231.0, high 6274.77, low 6061.97, close 6110.0, close time 2018-06-25 14:59:59.999000, closing True]
Filling stop loss order 45627
Trade 315195 CLOSED.
Gain: -80.01000000

>>> [symbol BTCUSDT, interval 1HOUR, open time 2018-06-30 00:00:00, open 5919.61, high 6300.0, low 5917.0, close 6243.38, close time 2018-06-30 00:59:59.999000, closing True]
RSIStrategy: OPEN
Order: orderSide BUY, orderType MARKET, qty 1.00000000, price None, stopPrice None, orderState OPEN_PENDING_INT, orderId 45628
Order: orderSide SELL, orderType STOP_LOSS_LIMIT, qty 1.00000000, price 6163.38000000, stopPrice 6163.38000000, orderState OPEN_PENDING_INT, orderId 45629
Trade 315196 OPENED.
>>> [symbol BTCUSDT, interval 1HOUR, open time 2018-07-02 17:00:00, open 6612.98, high 6649.97, low 6608.99, close 6630.08, close time 2018-07-02 17:59:59.999000, closing True]
RSIStrategy: NEW ORDERS
Order: orderSide SELL, orderType MARKET, qty 1.00000000, price None, stopPrice None, orderState OPEN_PENDING_INT, orderId 45630
Trade 315196 CLOSED.
Gain: 386.70000000

>>> [symbol BTCUSDT, interval 1HOUR, open time 2018-07-15 10:00:00, open 6282.63, high 6360.17, low 6281.17, close 6320.0, close time 2018-07-15 10:59:59.999000, closing True]
RSIStrategy: OPEN
Order: orderSide BUY, orderType MARKET, qty 1.00000000, price None, stopPrice None, orderState OPEN_PENDING_INT, orderId 45631
Order: orderSide SELL, orderType STOP_LOSS_LIMIT, qty 1.00000000, price 6240.00000000, stopPrice 6240.00000000, orderState OPEN_PENDING_INT, orderId 45632
Trade 315197 OPENED.
>>> [symbol BTCUSDT, interval 1HOUR, open time 2018-07-16 11:00:00, open 6380.49, high 6537.0, low 6375.3, close 6526.03, close time 2018-07-16 11:59:59.999000, closing True]
RSIStrategy: NEW ORDERS
Order: orderSide SELL, orderType MARKET, qty 1.00000000, price None, stopPrice None, orderState OPEN_PENDING_INT, orderId 45633
Trade 315197 CLOSED.
Gain: 206.03000000

>>> [symbol BTCUSDT, interval 1HOUR, open time 2018-08-11 19:00:00, open 6110.07, high 6488.0, low 6108.98, close 6439.0, close time 2018-08-11 19:59:59.999000, closing True]
RSIStrategy: OPEN
Order: orderSide BUY, orderType MARKET, qty 1.00000000, price None, stopPrice None, orderState OPEN_PENDING_INT, orderId 45634
Order: orderSide SELL, orderType STOP_LOSS_LIMIT, qty 1.00000000, price 6359.00000000, stopPrice 6359.00000000, orderState OPEN_PENDING_INT, orderId 45635
Trade 315198 OPENED.
>>> [symbol BTCUSDT, interval 1HOUR, open time 2018-08-11 21:00:00, open 6385.7, high 6395.84, low 6351.0, close 6387.85, close time 2018-08-11 21:59:59.999000, closing True]
Filling stop loss order 45635
Trade 315198 CLOSED.
Gain: -80.00000000

>>> [symbol BTCUSDT, interval 1HOUR, open time 2018-08-15 04:00:00, open 6218.75, high 6295.0, low 6203.52, close 6256.95, close time 2018-08-15 04:59:59.999000, closing True]
RSIStrategy: OPEN
Order: orderSide BUY, orderType MARKET, qty 1.00000000, price None, stopPrice None, orderState OPEN_PENDING_INT, orderId 45636
Order: orderSide SELL, orderType STOP_LOSS_LIMIT, qty 1.00000000, price 6176.94000000, stopPrice 6176.94000000, orderState OPEN_PENDING_INT, orderId 45637
Trade 315199 OPENED.
>>> [symbol BTCUSDT, interval 1HOUR, open time 2018-08-22 03:00:00, open 6461.04, high 6842.47, low 6448.87, close 6808.96, close time 2018-08-22 03:59:59.999000, closing True]
RSIStrategy: NEW ORDERS
Order: orderSide SELL, orderType MARKET, qty 1.00000000, price None, stopPrice None, orderState OPEN_PENDING_INT, orderId 45638
Trade 315199 CLOSED.
Gain: 552.01000000

Final balance for USDT: 824.710000000001

PERFORMANCE
+-----+--------+-----+------+---------+------------------+---------+--------+-----------+----------+----------+----------+----------+-------------------+------------------+
| SEI | Trades | Won | Lost | Won [%] |   Gross profit   |   Gain  |  Loss  | Gain/Loss | Avg gain | Max gain | Avg loss | Max loss |  Avg trade length | Max trade length |
+-----+--------+-----+------+---------+------------------+---------+--------+-----------+----------+----------+----------+----------+-------------------+------------------+
| 816 |   7    |  3  |  4   |  42.86  | 824.710000000001 | 1144.74 | 320.03 |    3.58   |  381.58  |  552.01  |  80.01   |  80.01   | 1 days 22h:17m:8s | 7 days 0h:0m:0s  |
+-----+--------+-----+------+---------+------------------+---------+--------+-----------+----------+----------+----------+----------+-------------------+------------------+
```

Overall our strategy entered 7 trades with 42% success rate and gross profit of 824.71 USDT.

The complete strategy (with some tweaks) can be found in `creten/strategy_repository/RSIStrategy.py`, the input configuration and a wrapper script in `creten/examples/backtest/binance_rsi/`. In order to get feel of `creten` further, feel free to consult other examples in `creten/examples`.

## How can I help?

I am glad you asked! `creten` is still a young project and the biggest contribution at the moment is to:
- spread the word
- file bugs, issues, feature requests or any critique
- feel free to come with your own idea :-)

## Get in touch

If you feel you want to get in touch either with developers or community, you can:
- use Github Issues if it is related to `creten` development
- join the [Telegram group](https://t.me/joinchat/H-VJNFAYoelyD35GF6gojw)
- follow [![Twitter Follow](https://img.shields.io/twitter/follow/cretenframework.svg?style=social&label=@cretenframework)](https://twitter.com/cretenframework)
- send a good old e-mail to <img src="http://safemail.justlikeed.net/e/0d7145ca3282ff04393182056c826bc6.png" align="absbottom">

## Warranty

There is none. As it goes with open source, neither `creten` nor any of its developers is responsible for any loss due to your strategy or bugs in the code. By using it you acknowledge that you are aware of the risk and will suffer all potential consequencies. `creten` does not give any financial advice. If unsure, do not run `creten` in the real trading mode.
# CRETEN

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
# CRETEN

[![](https://img.shields.io/badge/python-2.7-blue.svg)](https://www.python.org/downloads/release/python-2715/) [![](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-365/)

_**Cr**ypto **E**xchange **T**rading **En**gine_, or **_creten_** for short, is a modern Python-based framework for developers and curious minds of all sorts helping them design, backtest and execute trading strategies in the evergrowing crypto market.

First of all, it is important to understand that `creten` is **not** a trading bot that you install and it will make you rich, though there are many exemplary strategies bundled with the framework. The ultimate mission of `creten` is to equip developers with means (i.e. a framework) enabling them to quickly develop their own trading strategies, allow them to evaluate the performance via backtesting and realtime testing (paper trading) as easily as possible and once the state-of-the art strategy proves profitable, `creten` can execute it in real crypto market.

## Features

- backtest, realtime test, trader
- exchanges, file exchange
- databases
- indicators
- market data
- all order types
- access to market data

## Installation

Following paragraphs will guide you through the exhaustive set of steps to get `creten` running properly. Installation procedure is common for both Python 2.x and Python 3.x (all differences marked where relevant) and is illustrated on Linux/MacOS.

##### 0. Prerequisites

In order to be able to use `creten`, you need have following components installed on your system:
- `git`
- `Python 2.x` or `Python 3.x` (`creten` was intensively tested with Python 2.7 and Python 3.6)
- a database engine (see *Features* section for supported engines)

##### 1. Clone `creten` to your local filesystem

Choose destination folder where `creten` will be downloaded and run

`$ git clone git@github.com:nardew/creten.git`

##### 2. Create and enter a Python virtual environment [optional]

Since `creten` uses several external packages, it is recommended to use it in a Python's virtual environment in order to ease dependency download and resolution. Nevertheless, this step is not mandatory if you are experienced with installation and management of external dependencies.

To create an empty virtual environment, use following commands. Note that there is a plenty of documentation on the internet explaining virtual environments in detail.
```
$ virtualenv -p <python_version> <virtual_env_dir>, e.g. virtualenv -p python3 creten_env
$ source creten_env/bin/activate
(creten_env) $
```
If all went well, you should see name of the virtual environment prepended to your command line.
  
##### 3. Install dependencies
`creten` contains file `creten/requirements.txt` which lists all mandatory dependencies. To download and install them, run:

`(creten_env) $ pip install -r requirements.txt`

**Note:** The above will download all dependencies but the database engine interface. Database interface is not included in the file with requirements since different developers will use a different interface of their own choice and it is not practical to install all interfaces by default. Please install it manually (e.g. `pip install pymysql` for MySQL)

##### 4. Create database layout

Based on the database engine of your choice, manually apply one of the DDLs contained in `env_setup` folder:
- MySQL/MariaDB: `env_setup/DDL_MySQL.sql`
- PostgreSQL: `env_setup/DDL_PostgreSQL.sql`
- SQLite: `env_setup/DDL_SQLite.sql`

##### 5. Check `creten` help page to verify installation
`(creten_env) creten$ python creten.py -h`

Above command should return description of all command line parameters.

##### 6. Setup environment variable for `creten` root directory

In order to be able to run predefined examples, you need to setup an environment variable which will point to `creten`'s application folder (i.e. the one containing creten.py file, not its parent!). This step can be automated by updating the user's profile script. Once the environment variable is defined, source `profile.sh`.

```
(creten_env) $ export CRETEN_APP_ROOT_DIR=<creten application dir>
(creten_env) $ source profile.sh
```

##### 7. Execute one of the bundled examples

There are several examples bundled with `creten`, to verify that installation of `creten` has been successful, execute one of them.

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
- file bugs, issues, feature requests or any critique in general
- feel free to come with your own idea :-)

## Get in touch

If you feel you want to get in touch, either with developers or community:
- use Github Issues if it is related to `creten` development
- join the [Telegram group](https://t.me/joinchat/H-VJNFAYoelyD35GF6gojw)
- follow [![Twitter Follow](https://img.shields.io/twitter/follow/cretenframework.svg?style=social&label=@cretenframework)](https://twitter.com/cretenframework)
- send a good old e-mail to <img src="http://safemail.justlikeed.net/e/0d7145ca3282ff04393182056c826bc6.png" align="absbottom">
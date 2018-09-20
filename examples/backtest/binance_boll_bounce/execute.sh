#!/usr/bin/env bash

if [ -z "$CRETEN_APP_ROOT_DIR" ]; then
    echo "ERROR: CRETEN_APP_ROOT_DIR is not set. Please initialize it with CRETEN application root dir."
    exit 1
fi

if [ ! -d "$CRETEN_APP_ROOT_DIR" ]; then
    echo "ERROR: CRETEN_APP_ROOT_DIR (\"$CRETEN_APP_ROOT_DIR\") does not correspond to a valid directory. Please initialize it with CRETEN application root dir."
    exit 1
fi

python ${CRETEN_APP_ROOT_DIR}/creten.py -m backtest -e binance --inputconfig input_config.json $@

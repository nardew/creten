schema = {
	"$schema": "http://json-schema.org/draft-06/schema#",

	"$comment": "Definition of the setup for backtesting.",
	"type": "object",
	"properties": {
		"backtest": {
			"$comment": "Each definition of backtest will be executed one by one sequentially.",
			"type": "array",
			"items": {
				"type": "object",
				"properties": {
					"strategies": {
						"$comment": "Strategies to be evaluated. Executed one by one sequentially.",
						"type": "array",
						"items": {
							"type": "object",
							"properties": {
								"strategy_name": {
									"$comment": "Strategy name. It must correspond to a valid class within module of same name located in strategy_repository folder (unless module_path attribute is defined).",
									"type": "string"
								},
								"module_path": {
									"$comment": "Cutome module path in case strategy class is not located in strategy_repository/<strategy_name>.",
									"type": "string"
								}
							},
							"required": ["strategy_name"]
						},
						"minItems": 1
					},
					"pairs": {
						"$comment": "Pairs to be used for backtesting. Each pair is represented by an array of two elements (e.g. [['BTC', 'USDT'], ['XLM', 'BTC'], ['ADA', 'BTC'], ...].",
						"type": "array",
						"items": {
							"type": "array",
							"items": {
								"type": "string"
							},
							"minItems": 2,
							"maxItems": 2
						},
						"minItems": 1
					},
					"interval": {
						"$comment": "Timeframe of the price data to be backtested.",
						"type": "string",
						"enum": [
							"1MINUTE",
							"3MINUTE",
							"5MINUTE",
							"15MINUTE",
							"30MINUTE",
							"1HOUR",
							"2HOUR",
							"4HOUR",
							"6HOUR",
							"8HOUR",
							"12HOUR",
							"1DAY",
							"3DAY",
							"1WEEK",
							"1MONTH"
						]
					},
					"start_tmstmp": {
						"$comment": "Starting timestamp of the backtesting. Format %Y%m%d%H%M%S",
						"type": "string",
						"pattern": "^[0-9]{14}$"
					},
					"end_tmstmp": {
						"$comment": "Ending timestamp of the backtesting. Format %Y%m%d%H%M%S",
						"type": "string",
						"pattern": "^[0-9]{14}$"
					},
				},
				"required": ["strategies", "pairs", "interval", "start_tmstmp", "end_tmstmp"]
			},
			"minItems": 1
		},
	},
	"required": ["backtest"]
}
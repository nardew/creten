schema = {
	"$schema": "http://json-schema.org/draft-06/schema#",

	"$comment": "Definition of the setup for realtime simulation.",
	"type": "object",
	"properties": {
		"realtimetest": {
			"$comment": "All definition of realtime tests will be executed in parallel.",
			"type": "object",
			"properties": {
				"strategies": {
					"$comment": "Strategies to be evaluated. Executed in parallel.",
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
					"$comment": "Timeframe of the price data to be tested.",
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
			},
			"required": ["strategies", "pairs", "interval"]
		},
	},
	"required": ["realtimetest"]
}
schema = {
	"$schema": "http://json-schema.org/draft-06/schema#",

	"$comment": "Definition of the custom exchange with price data included in the specified CSV file.",
	"type": "object",
	"properties": {
		"baseAsset": {
			"$comment": "Base asset of the pair in the input CSV file, e.g. BTC, ETH, XLM, ADA, ...",
			"type": "string"
		},
		"quoteAsset": {
			"$comment": "Quote asset of the pair in the input CSV file, e.g. BTC, ETH, USDT, ...",
			"type": "string"
		},
		"rules": {
			"$comment": "Definition of market rules for data included in the input CSV file.",
			"type": "object",
			"properties": {
				"baseAsset": {
					"$comment": "Base asset of the corresponding market rules, e.g. BTC, ETH, XLM, ADA, ...",
					"type": "string"
				},
				"quoteAsset": {
					"$comment": "Quote asset of the corresponding market rules, e.g. BTC, ETH, USDT, ...",
					"type": "string"
				},
				"baseAssetPrecision": {
					"$comment": "Number of decimals in the quanitity of the base asset, e.g. 2, 6, 8, ...",
					"$ref" : "#/definitions/stringNumber",
				},
				"quoteAssetPrecision": {
					"$comment": "Number of decimals in the price of the quote asset, e.g. 2, 6, 8, ...",
					"$ref" : "#/definitions/stringNumber",
				},
				"minPrice": {
					"$comment": "Minimum price.",
					"$ref" : "#/definitions/stringNumber",
				},
				"maxPrice": {
					"$comment": "Maximum price.",
					"$ref" : "#/definitions/stringNumber",
				},
				"minPriceDenom": {
					"$comment": "Step that the price can be increased/decreased by.",
					"$ref" : "#/definitions/stringNumber",
				},
				"minQty": {
					"$comment": "Minimum quantity",
					"$ref" : "#/definitions/stringNumber",
				},
				"maxQty": {
					"$comment": "Maximum quantity",
					"$ref" : "#/definitions/stringNumber",
				},
				"minQtyDenom": {
					"$comment": "Step that the quantity can be increased/decreased by.",
					"$ref" : "#/definitions/stringNumber",
				},
				"minNotional": {
					"$comment": "Minimum notial value, calculated as price * quantity.",
					"$ref" : "#/definitions/stringNumber",
				}
			},
		},
		"data": {
			"$comment": "Section describing the input price data.",
			"type": "object",
			"properties": {
				"db": {
					"$comment": "Db description with the input data",
					"type": "object",
					"properties": {
						"tableName": {
							"$comment": "Name of the table containing input data",
							"type": "string"
						}
					},
					"required": ["tableName"]
				},
				"fieldMap": {
					"$comment": "Specifies structure of the input CSV file. For each of the below attributes it maps corresponding column in the CSV file (starting from 0). Each attribute should be assigned a unique number (though it is not enforced by the application).",
					"type": "object",
					"properties": {
						"openTmstmp": {
							"type": "string"
						},
						"open": {
							"type": "string"
						},
						"high": {
							"type": "string"
						},
						"low": {
							"type": "string"
						},
						"close": {
							"type": "string"
						},
						"volume": {
							"type": "string"
						},
					},
					"required": ["openTmstmp", "open", "high", "low", "close", "volume"]
				},
				"timeFormat": {
					"$comment": "Defines format of the timestamps in the input CSV file. Format needs to be in Python notation (e.g. %Y/%m/%d for daily data).",
					"type": "string",
				},
				"interval": {
					"$comment": "Timeframe of the price data included in the input CSV file.",
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
			"required": ["db", "fieldMap", "timeFormat", "interval"]
		}
	},

	"required": ["baseAsset", "quoteAsset", "rules", "data"],

	"definitions": {
        "stringNumber": {
	        "type": "string",
			"pattern": "^[0-9]+\.?[0-9]*$"
        }
    },
}
schema = {
	"$schema": "http://json-schema.org/draft-06/schema#",

	"$comment": "Additional exchange customization to complement/rewrite exchange settings fetched directly from the exchange.",
	"type": "object",
	"properties": {
		"marketRules": {
			"$comment": "Definition of symbol rules that will overwrite rules fetched directly from the exchange.",
			"type": "array",
			"items": {
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
				"required": ["baseAsset", "quoteAsset"]
			}
		}
	},

	"definitions": {
        "stringNumber": {
	        "type": "string",
			"pattern": "^[0-9]+\.?[0-9]*$"
        }
    }
}
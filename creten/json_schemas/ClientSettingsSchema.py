schema = {
	"$schema": "http://json-schema.org/draft-06/schema#",

	"$comment": "Client settings.",
	"type": "object",
	"properties": {
		"DB_CONNECTION": {
			"$comment": "Definition of the database connection.",
			"type": "object",
			"properties": {
				"ENGINE": {
					"$comment": "Database engine, e.g. mysql+pymysql.",
					"type": "string"
				},
				"HOST": {
					"$comment": "Database host, e.g. 127.0.0.1",
					"type": "string"
				},
				"PORT": {
					"$comment": "Port where database is listening, e.g. 3306.",
					"type": "number"
				},
				"USER": {
					"$comment": "Username to be used to connect to the database.",
					"type": "string"
				},
				"PASSWORD": {
					"$comment": "Password to be used to connect to the database.",
					"type": "string"
				},
				"DB": {
					"$comment": "Database name/path if applicable (relevant e.g. for MySQL, MariaDb and other database engines).",
					"type": "string"
				}
			}
		},

		"TRADES": {
			"$comment": "Default trade parameters",
			"type": "object",
			"properties": {
				"DEFAULT_TRADE_CLOSE_TYPE": {
					"$comment": "Default strategy deciding when trade is marked as closed.",
					"type": "string",
					"enum": [
						"ORDER_DRIVEN",
						"QUANTITY_DRIVEN"
					]
				},
				"DEFAULT_MAX_PARALLEL_TRADES": {
					"$comment": "Maximum number of trades created by one strategy that can be active at the same time.",
					"type": "number",
					"minimum": 1
				},
				"DEFAULT_PARALLEL_TRADES_MIN_DIST": {
					"$comment": "If more than one trade can be active, define the minimum distance of the next active trade.",
					"type": "number",
					"minimum": 1
				}
			},
			"required": ["DEFAULT_TRADE_CLOSE_TYPE", "DEFAULT_MAX_PARALLEL_TRADES", "DEFAULT_PARALLEL_TRADES_MIN_DIST"]
		}
	},
	"required": ["DB_CONNECTION", "TRADES"]
}
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
		}
	},
	"required": ["DB_CONNECTION"]
}
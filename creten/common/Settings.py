import json
import jsonschema
import os
from json_schemas import ClientSettingsSchema

class Settings:

	# String which is prepended to Creten's internal reference assigned to every outgoing order
	ORDER_REFERENCE_PREFIX = 'CRTN'

	client = None
	@staticmethod
	def initClientConfig(clientConfigPath = None):
		if clientConfigPath:
			with open(os.path.realpath(clientConfigPath)) as myFile:
				conf = myFile.read()
				Settings.client = json.loads(conf)
				jsonschema.validate(Settings.client, ClientSettingsSchema.schema)
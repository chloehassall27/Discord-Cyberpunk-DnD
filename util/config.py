import json
from marshmallow import Schema, fields

class ConfigSchema(Schema):
    currency_symbol = fields.String(required=True)
    dm_role = fields.String(required=True)
    admins = fields.List(fields.String, required=True)

def loadConfig():
    f = open('prefs.json')
    config = json.load(f)
    f.close()
    return ConfigSchema().load(config)

config = loadConfig()

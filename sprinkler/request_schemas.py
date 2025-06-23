from marshmallow import Schema, fields
from marshmallow.validate import Range

class UpdateSettingsSchema(Schema):
    motor_pin = fields.Int(required=True, validate=Range(min=1, max=27))
    sensor_pin = fields.Int(required=True, validate=Range(min=1, max=17))
    latitude = fields.Float(required=True, validate=Range(min=-90.0, max=90.0))
    longitude = fields.Float(required=True, validate=Range(min=-180.0, max=180.0))
    timezone = fields.Str(required=True) # gonna trust you on this one...
    precipitation_threshold = fields.Float(required=True, validate=Range(min=0.0, min_inclusive=False))
    sensor_day_limit = fields.Int(required=True, validate=Range(min=2))
    watering_time = fields.Int(required=True, validate=Range(min=1))


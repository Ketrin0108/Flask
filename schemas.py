from marshmallow import Schema, fields


class UserSchema(Schema):
    first_name = fields.Str(required=True, validate=fields.Length(1))
    last_name = fields.Str(required=True)
    idea_id = fields.Int(required=False)

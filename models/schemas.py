from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    public_id = fields.Str()
    name = fields.Str()
    email = fields.Email()
    password = fields.Str(load_only=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

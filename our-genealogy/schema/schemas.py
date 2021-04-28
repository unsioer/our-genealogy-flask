from flask import abort, make_response, jsonify
from marshmallow import Schema,fields,ValidationError
def check_data(schema, data):
    try:
        return schema().load(data)
    except ValidationError as e:
        abort(make_response(jsonify(code=400, message=str(e.messages), result=None), 400))

class PersonSchema(Schema):
    name = fields.Str(required=True)
    gender = fields.Bool(required=True)
    family = fields.Str(required=True)
    living = fields.Bool(required=True)
    born = fields.Str()
    death = fields.Str()
    description = fields.Str()
    avatar_url = fields.Str()

class FamilySchema(Schema):
    create_by = fields.Str(required=True)
    create_on = fields.Str()
    surname = fields.Str(required=True)
    name = fields.Str(required=True)
    area = fields.Str(required=True)
    is_public = fields.Bool(required=True)
    tanghao = fields.Str()
    description = fields.Str()
    members = fields.List(fields.Str())
    relation = fields.List(fields.Str())
    admins = fields.List(fields.Str())
    read_admins = fields.List(fields.Str())
    avatar_url = fields.Str()

class RelationSchema(Schema):
    from_person = fields.Int(required=True)
    to_person = fields.Int(required=True)
    family_id = fields.Int(required=True)
    type = fields.Int(required=True,validate=lambda n: 1 <= n <= 6)
    special = fields.Int(required=True,validate=lambda n: 0 <= n <= 3)

# todo:information validation
class RegisterUserSchema(Schema):
    email = fields.Email(required=True)
    nickname = fields.Str(required=True)
    password = fields.Str(required=True)
    phone = fields.Str(required=True)

#T
class LoginUsersSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

class CommentSchema(Schema):
    content = fields.Str(required=True)
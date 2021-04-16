from models.user import User
import json
from flask import Blueprint, request, abort
from utils.utils import *
from utils.ApiError import *
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity
)
from schema.schemas import(
    check_data,
    PersonSchema,
    FamilySchema,
    RelationSchema,
    RegisterUserSchema,
    LoginUsersSchema
)
from extensions import mongo


user_bp = Blueprint('user', __name__)

@user_bp.route('/', methods=['POST'],strict_slashes=False)
def register_user():
    data = json.loads(request.get_data())
    data = check_data(RegisterUserSchema, data)
    if mongo.db.user.find({"data": data['email']}):
        raise ApiError(EMAIL_ALREADY_EXIST)
    user = User(entries=data)
    user.type = 0
    #设定注册时间
    user.register_time = currentTime()
    #加密
    user.passwordHash()
    #生成ID
    user.id = generateID()
    print(user.id)
    print(user.serialize())
    mongo.db.user.insert_one(user.serialize())
    return user.serialize()


@user_bp.route('/', methods=['GET'])
@jwt_required()
def query_user_self():
    currentUserId = get_jwt_identity()
    users = mongo.db.user.find_one_or_404({'_id': currentUserId})
    user = User(entries=users)
    return user.serialize()


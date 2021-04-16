
from models.user import User
import json
from flask import Blueprint, request, abort, jsonify
from utils.utils import *
from utils.ApiError import *
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity,
)
from schema.schemas import(
    check_data,
    LoginUsersSchema
)
from extensions import mongo

auth_bp = Blueprint('auth',__name__)



@auth_bp.route('/login', methods=['POST'])
def login():
    data = json.loads(request.get_data())
    check_data(LoginUsersSchema, data)
    user = mongo.db.user.find_one_or_404({'email': data['email']})
    user = User(user)
    result = user.check_password(data['password'])
        # no need to use jwt_claim now
    additional_claims = {"is_admin":False}
    if result:
        if user.type==1:
            additional_claims['is_admin']=True
        access_token = create_access_token(identity=user.id,additional_claims=additional_claims)
        # add admin special jwt
        # add logout
        return jsonify(access_token=access_token)
    else:
        raise ApiError(WRONG_PASSWORD)

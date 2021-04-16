from flask import Blueprint, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from extensions import mongo
from models.user import User

admin_bp = Blueprint("admin",__name__)
@admin_bp.route('/user/<string:id>', methods=['GET'])
@jwt_required()
def query_user(id):
    is_admin = get_jwt()['is_admin']
    currentUserId = get_jwt_identity()
    users = mongo.db.user.find_one_or_404({'_id': id})
    user = User(entries=users)
    print(currentUserId)
    if user.id == currentUserId or is_admin:
        return user.serialize()
    else:
        abort(403)
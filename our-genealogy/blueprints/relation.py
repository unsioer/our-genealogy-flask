from flask import Blueprint, request
import json

from models.family import Family
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity, get_jwt
)

from models.relation import Relation
from utils.utils import generateID
from utils.ApiError import *
from extensions import mongo
from utils.authCheck import *
from schema.schemas import (
    check_data,
    FamilySchema, RelationSchema
)

relation_bp = Blueprint("relation", __name__)


@relation_bp.route('/<string:id>', methods=['GET'])
@jwt_required()
def get_relation(id):
    is_admin = get_jwt()['is_admin']
    currentUserId = get_jwt_identity()
    relation = mongo.db.relation.find_one_or_404({'_id': id})
    family = mongo.db.family.find_one_or_404({'_id': relation['family_id']})
    family = Family(entries=family)

    if relation[
        'user_id'] == currentUserId or check_family_read_auth(family,currentUserId,is_admin):
        relation = Relation(entries=relation)
        return relation.serialize()
    else:
        raise ApiError(NO_AUTH, 403)


@relation_bp.route('/<string:id>', methods=['DELETE'])
@jwt_required()
def delete_relation(id):
    is_admin = get_jwt()['is_admin']
    query = {"_id": id}
    currentUserId = get_jwt_identity()
    relation = mongo.db.relation.find_one_or_404(query)
    family = mongo.db.family.find_one_or_404({'_id': relation['family_id']})
    family = Family(entries=family)
    if relation['user_id'] == currentUserId or check_family_edit_auth(family,currentUserId,is_admin):
        result = mongo.db.relation.delete_one(query).deleted_count
        print(result)
        return "ok"
    else:
        raise ApiError(NO_AUTH, 403)


@relation_bp.route('/', methods=['POST'],strict_slashes=False)
@jwt_required()
def add_relation():
    is_admin = get_jwt()['is_admin']
    data = json.loads(request.get_data())
    data = check_data(RelationSchema, data)
    current_user_id = get_jwt_identity()
    relation = Relation(entries=data)
    family = mongo.db.family.find_one_or_404({'_id': relation.family_id})
    family = Family(entries=family)

    if check_family_edit_auth(family,current_user_id,is_admin):  # todo:need to add admins
        relation.id = generateID()
        relation.user_id = current_user_id
        mongo.db.relation.insert_one(relation)
        return relation.serialize()
    else:
        raise ApiError(NO_AUTH, 403)

@relation_bp.route('/<string:id>', methods=['PUT'])
def update_relation(id):
    is_admin = get_jwt()['is_admin']
    query = {"_id": id}
    data = json.loads(request.get_data())
    data = check_data(RelationSchema, data)
    currentUserId = get_jwt_identity()
    relation = mongo.db.relation.find_one_or_404(query)
    family = mongo.db.family.find_one_or_404({'_id': relation['family_id']})
    family = Family(entries=family)
    if relation.user_id == currentUserId or check_family_edit_auth(family,currentUserId,is_admin):
        update_data = {"$set": data}
        mongo.db.relation.update_one(query, update_data)
        relation = Relation(entries=data)
    else:
        raise ApiError(NO_AUTH,403)
    return relation.serialize()


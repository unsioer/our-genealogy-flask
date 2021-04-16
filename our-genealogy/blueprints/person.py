from flask import Blueprint,request
import json
from models.person import Person
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity, get_jwt
)

from utils.utils import generateID
from utils.authCheck import *
from utils.ApiError import *
from extensions import mongo
from schema.schemas import(
    check_data,
    PersonSchema
)

person_bp = Blueprint("person",__name__)

@person_bp.route('/<string:id>', methods=['GET'])
@jwt_required()
def query_person(id):
    is_admin = get_jwt()['is_admin']
    print(is_admin)
    currentUserId = get_jwt_identity()
    persons = mongo.db.person.find_one_or_404({'_id': id})
    person = Person(entries=persons)
    print(person.family)
    family = mongo.db.family.find_one_or_404({"_id":person.family})

    family = Family(entries=family)
    print(currentUserId)
    if person.user_id == currentUserId or check_family_read_auth(family,currentUserId,is_admin):
        return person.serialize()
    else:
       raise ApiError(NO_AUTH,403)

@person_bp.route('/', methods=['POST'],strict_slashes=False)
@jwt_required()
def add_person():  #
    currentUserId = get_jwt_identity()
    data = json.loads(request.get_data())
    data = check_data(PersonSchema, data)  #
    person = Person(entries=data)
    person.user_id = currentUserId
    person.id = generateID()
    print(person.serialize())
    mongo.db.person.insert_one(person.serialize())
    return person.serialize()

@person_bp.route('/<string:id>', methods=['PUT'])
@jwt_required()
def update_person(id):
    print(id)
    is_admin = get_jwt()['is_admin']
    currentUserId = get_jwt_identity()
    query = {"_id": id}
    data = json.loads(request.get_data())
    data = check_data(PersonSchema, data)

    person = mongo.db.person.find_one_or_404({'_id': id})
    family = mongo.db.family.find_one_or_404({"_id":person['family']})
    family = Family(entries=family)

    if person['user_id'] == currentUserId or check_family_edit_auth(family,currentUserId,is_admin):
        update_data = {"$set": data}
        mongo.db.person.update_one(query, update_data)
        person = Person(entries=data)
        return person.serialize()
    else:
        raise ApiError(NO_AUTH,403)

@person_bp.route('/<string:id>', methods=['DELETE'])
@jwt_required()
def delete_person(id):
    is_admin = get_jwt()['is_admin']
    currentUserId = get_jwt_identity()
    query = {"_id": id}
    person = mongo.db.person.find_one_or_404(query)
    family = mongo.db.family.find_one_or_404({"_id":person['family']})
    family = Family(entries=family)

    if person['user_id'] == currentUserId or check_family_edit_auth(family,currentUserId,is_admin):
        result = mongo.db.person.delete_one(query).deleted_count
    else:
        raise ApiError(NO_AUTH,403)
    return "ok"


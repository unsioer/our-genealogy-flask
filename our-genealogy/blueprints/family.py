from flask import Blueprint, request, jsonify
import json

from models.family import Family
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_jwt
)

from utils.utils import generateID
from utils.authCheck import *
from utils.ApiError import *
from extensions import mongo
from schema.schemas import (
    check_data,
    FamilySchema
)

family_bp = Blueprint("family", __name__)


@family_bp.route('/<string:id>', methods=['GET'])
@jwt_required()
def get_family(id):
    currentUserId = get_jwt_identity()
    is_admin = get_jwt()['is_admin']
    family = mongo.db.family.find_one_or_404({'_id': id})
    family = Family(entries=family)
    # todo: judge special jwt,public family
    if check_family_read_auth(family, currentUserId, is_admin):
        memberList = []
        for member in family.members:
            person = mongo.db.person.find_one_or_404({'_id': member})
            memberList.append(person)
        family.members = memberList

        return family.serialize()
    else:
        raise ApiError(NO_AUTH, 403)


@family_bp.route('/<string:id>', methods=['DELETE'])
@jwt_required()
def delete_family(id):
    is_admin = get_jwt()['is_admin']
    currentUserId = get_jwt_identity()
    query = {"_id": id}
    family = mongo.db.family.find_one_or_404({'_id': id})
    family = Family(entries=family)
    if check_family_read_auth(family, currentUserId, is_admin):
        result = mongo.db.family.delete_one(query).deleted_count
    ## todo:maybe need to delete the connection between family & person
    if result != 0:
        return "ok"
    else:
        raise ApiError(NOT_FOUND, 404)


@family_bp.route('/<string:id>', methods=['PUT'])
def update_family(id):
    is_admin = get_jwt()['is_admin']
    currentUserId = get_jwt_identity()
    query = {"_id": id}
    data = json.loads(request.get_data())
    data = check_data(FamilySchema, data)
    family = mongo.db.family.find_one_or_404({'_id': id})
    family = Family(entries=family)
    if check_family_edit_auth(family, currentUserId, is_admin):
        update_data = {"$set": data}
        mongo.db.family.update_one(query, update_data)
        family = Family(entries=data)
        return family.serialize()
    else:
        raise ApiError(NO_AUTH, 403)


@family_bp.route('/', methods=['POST'],strict_slashes=False)
@jwt_required()
def add_family():
    data = json.loads(request.get_data())
    data = check_data(FamilySchema, data)  #
    currentUserId = get_jwt_identity()
    family = Family(entries=data)
    family.created_by = currentUserId
    family.id = generateID()
    print(family)
    mongo.db.family.insert_one(family.serialize())
    return family.serialize()


@family_bp.route('/<string:id>/details', methods=['GET'])
@jwt_required()
def get_family_detail(id):
    is_admin = get_jwt()['is_admin']
    '''首先 构建出所有的用户信息dict
    id最后应该统一化为string 目前使用的测试数据不统一，因此用了多于代码进行处理
    # dict['id':[dict(person),relation]]
    # person:
    # type:dict
    familyTree[id]:personDict
    # personDict['name']=string
    personDict['mates']:list[person]
    personDict['children']:list[person]
    '''
    currentUserId = get_jwt_identity()
    familyMembersDict = dict()
    # 构建一个由id persondict组成的列表， 并且root是id号即可
    familyTree = dict()
    root = None
    familyMemberQuery = {"family": id}
    family = mongo.db.family.find_one_or_404({'_id': id})
    family = Family(entries=family)
    if check_family_read_auth(family, currentUserId, is_admin):
        familyMebers = list(mongo.db.person.find(familyMemberQuery))
        print(familyMebers)
        # 以id为key建立索引，方便之后查找
        for person in familyMebers:
            # 用id为key建立familyMembers字典，属性为(当前角色，当前角色的孩子id，当前角色的matesId)，采用这些信息构建familyTree
            familyMembersDict[person["_id"]] = [person]
            childrenQuery = {"from_person": str(person["_id"]), "type": 1}
            mateQuery = {"from_person": str(person["_id"]), "$or": [{"type": 3}, {"type": 4}]}
            childrenRelations = list(mongo.db.relation.find(childrenQuery))
            mateRelations = list(mongo.db.relation.find(mateQuery))
            childIds = [r['to_person'] for r in childrenRelations]
            mateIds = [r['to_person'] for r in mateRelations]
            familyMembersDict[person["_id"]].append(childIds)
            familyMembersDict[person["_id"]].append(mateIds)

            # personDict为最终输出时需要用到的数据
            personDict = dict()
            personDict['name'] = person['name']
            personDict['mates'] = []
            personDict['children'] = []
            personDict['image_url'] = ""
            familyTree[person["_id"]] = personDict
        for k, v in familyTree.items():
            if root == None:
                root = k
            childIds = familyMembersDict[k][1]
            for id in childIds:
                # 如果根节点是当前节点的孩子，那么当前节点是根节点
                if root == id:
                    root = k
                familyTree[k]['children'].append(familyTree[id])
            mateIds = familyMembersDict[k][2]
            for mateid in mateIds:
                query = {"_id": mateid}
                mate = mongo.db.person.find_one(query)
                mateDict = dict()
                mateDict['name'] = mate['name']
                mateDict['image_url'] = ""
                familyTree[k]['mates'].append(mateDict)
        print(familyMembersDict)
        return familyTree[root]
    else:
        raise ApiError(NO_AUTH, 403)


@family_bp.route('/all', methods=['GET'])
@jwt_required()
def get_all_families():
    currentUserID = get_jwt_identity()
    # todo: need to add public family
    query = {"$or": [{"admins": {"$in": [currentUserID]}}, {"read_admins": {"$in": [currentUserID]}},
                     {"created_by": currentUserID}, {"is_public": True}]}
    families = list(mongo.db.family.find(query))
    return jsonify(families)

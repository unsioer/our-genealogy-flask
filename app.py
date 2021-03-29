from flask import Flask, render_template, request, abort, jsonify
from flask_jwt_extended import create_access_token
from flask_pymongo import PyMongo
from models.person import Person
from models.family import Family
from models.relation import Relation
from models.user import  User
from  utils.utils import currentTime,generateID
import json
from schema.schemas import(
    check_data,
    PersonSchema,
    FamilySchema,
    RelationSchema,
    RegisterUserSchema,
    LoginUsersSchema
)
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)


app = Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/our_genealogy")
app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/person/<int:id>', methods=['GET'])
@jwt_required()
def query_person(id):
    currentUserId = get_jwt_identity()
    persons = mongo.db.person.find_one_or_404({'_id': id})
    person=Person(entries=persons)
    print(currentUserId)
    if person.user_id==currentUserId or currentUserId==1:
        return person.serialize()
    else:
        abort(403)

@app.route('/person', methods=['POST'])
@jwt_required()
def add_person():    #
    # Now we have to give MongoDB an `_id` column
    currentUserId =get_jwt_identity()
    data = json.loads(request.get_data())
    data = check_data(PersonSchema, data)    #
    try:
        person=Person(entries=data)
        person.user_id = currentUserId
        person.id = generateID()
        print(person.serialize())
        mongo.db.person.insert_one(person.serialize())
    except Exception as e:
        print(e)
        abort(500)
    return person.serialize()


@app.route('/person/<string:id>',methods=['PUT'])
@jwt_required()
def update_person(id):
    print(id)
    currentUserId= get_jwt_identity()
    query = {"_id":id}
    data = json.loads(request.get_data())
    data = check_data(PersonSchema,data)
    try:
        person = mongo.db.person.find_one_or_404({'_id': id})
        if person['user_id']==currentUserId or currentUserId==1:
            update_data = {"$set":data}
            mongo.db.person.update_one(query,update_data)
            person = Person(entries=data)
            return person.serialize()
        else:
            abort(403)
    except Exception as e:
        print(e)
        abort(500)


@app.route('/person/<string:id>',methods=['DELETE'])
@jwt_required()
def delete_person(id):
    currentUserId = get_jwt_identity()
    query = {"_id":id}
    try:
        person = mongo.db.person.find_one_or_404(query)
        if person['user_id']==currentUserId or currentUserId==1:
            result = mongo.db.person.delete_one(query).deleted_count
        else:
            abort(403)
    except Exception as e:
        print(e)
        abort(500)
    return "ok"

@app.route('/family/<string:id>',methods=['GET'])
@jwt_required()
def get_family(id):
    currentUserId = get_jwt_identity()
    family = mongo.db.family.find_one_or_404({'_id': id})
    family=Family(entries=family)
    if family.created_by==currentUserId or currentUserId==1 or currentUserId in family.admins:
        return family.serialize()
    else:
        abort(403)

@app.route('/family/<string:id>',methods=['DELETE'])
@jwt_required()
def delete_family(id):
    currentUserId = get_jwt_identity()
    query = {"_id":id}
    family = mongo.db.family.find_one_or_404({'_id': id})
    family=Family(entries=family)
    if family.created_by==currentUserId or currentUserId==1 or currentUserId in family.admins:
        result = mongo.db.family.delete_one(query).deleted_count
    ## todo:maybe need to delete the connection between family & person
    if result!=0:
        return "ok"
    else:
        abort(404)

@app.route('/family/<string:id>',methods=['PUT'])
def update_family(id):
    currentUserId = get_jwt_identity()
    query = {"_id": id}
    data = json.loads(request.get_data())
    data = check_data(FamilySchema,data)
    family = mongo.db.family.find_one_or_404({'_id': id})
    family = Family(entries=family)
    if  currentUserId == 1 or currentUserId in family.admins:
        try:
            update_data = {"$set":data}
            mongo.db.family.update_one(query,update_data)
            family = Family(entries=data)
            return family.serialize()
        except Exception:
            abort(500)
    abort(403)

@app.route('/family',methods=['POST'])
@jwt_required()
def add_family():
    data = json.loads(request.get_data())
    data = check_data(FamilySchema, data)    #
    currentUserId = get_jwt_identity()
    try:
        family=Family(entries=data)
        if family.admins!=None and currentUserId not in family.admins:
            family.admins.append(currentUserId)
        else:
            family.admins = [currentUserId]
        family.id = generateID()
        mongo.db.family.insert_one(family.serialize())
    except Exception as e:
        print(e)
        abort(500)
    return family.serialize()

@app.route('/relation/<string:id>',methods=['GET'])
@jwt_required()
def get_relation(id):
    currentUserId = get_jwt_identity()
    relation = mongo.db.relation.find_one_or_404({'_id': id})
    if relation['user_id']==currentUserId or currentUserId==1:
        relation=Relation(entries=relation)
        return relation.serialize()
    else:
        abort(403)

@app.route('/relation/<string:id>',methods=['DELETE'])
@jwt_required()
def delete_relation(id):
    query = {"_id":id}
    currentUserId = get_jwt_identity()
    relation = mongo.db.relation.find_one_or_404(query)
    if relation['user_id']==currentUserId or currentUserId==1:
        result = mongo.db.relation.delete_one(query).deleted_count
        print(result)
        return "ok"
    else:
        abort(403)
    ## todo:maybe need to delete the connection between family & person

@app.route('/relation',methods=['POST'])
@jwt_required()
def add_relation():
    data = json.loads(request.get_data())
    data = check_data(RelationSchema, data)
    currentUserId = get_jwt_identity()
    try:
        relation=Relation(entries=data)
        relation.id = generateID()
        relation.user_id = currentUserId
        mongo.db.relation.insert_one(relation)
    except Exception as e:
        print(e)
        abort(500)
    return relation.serialize()

@app.route('/relation/<string:id>',methods=['PUT'])
def update_relation(id):
    query = {"_id":id}
    data = json.loads(request.get_data())
    data = check_data(RelationSchema,data)
    currentUserId = get_jwt_identity()
    try:
        relation = mongo.db.relation.find_one_or_404(query)
        if relation.user_id==currentUserId or currentUserId==1:
            update_data = {"$set": data}
            mongo.db.relation.update_one(query,update_data)
            relation = Relation(entries=data)
    except Exception as e:
        print(e)
        abort(500)
    return relation.serialize()

@app.route('/user',methods=['POST'])
def register_user():
    #TODO TO VALIDATE UNIQUE EMAIL
    data = json.loads(request.get_data())
    data = check_data(RegisterUserSchema, data)
    try:
        user = User(entries=data)
        user.type=0
        #设定注册时间
        user.register_time=currentTime()
        #加密
        user.passwordHash()
        #生成ID
        user.id = generateID()
        print(user.id)
        print(user.serialize())
        mongo.db.user.insert_one(user.serialize())
    except Exception as e:
        print(e)
        abort(500)
    return user.serialize()

@app.route('/login',methods=['POST'])
def login():
    data = json.loads(request.get_data())
    check_data(LoginUsersSchema,data)
    try:
        user = mongo.db.user.find_one_or_404({'email': data['email']})
        user = User(user)
        result = user.check_password(data['password'])
        # no need to use jwt_claim now
        if result:
            access_token = create_access_token(identity=user.id)
            return jsonify(access_token=access_token)
        else:
            return "error password"
    # todo:need ultimate error handler
    except Exception as e:
        print(e)
        abort(500)




if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
    
from flask import Flask, render_template, request,abort
from flask_pymongo import PyMongo
from models.person import Person
from models.family import Family
from models.relation import Relation
import json
from schema.schemas import(
    check_data,
    PersonSchema,
    FamilySchema,
    RelationSchema
)

app = Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/our_genealogy")



@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/person/<int:id>', methods=['GET'])
def query_person(id):
    persons = mongo.db.person.find_one_or_404({'_id': id})
    person=Person(entries=persons)
    return person.serialize()



@app.route('/person', methods=['POST'])
def add_person():
    #
    # Now we have to give MongoDB an `_id` column
    data = json.loads(request.get_data())
    data = check_data(PersonSchema, data)    #
    try:
        person=Person(entries=data)
        print(person.serialize())
        mongo.db.person.insert_one(person)
    except Exception:
        pass
    return person.serialize()


@app.route('/person/<int:id>',methods=['PUT'])
def update_person(id):
    query = {"_id":id}
    data = json.loads(request.get_data())
    data = check_data(PersonSchema,data)
    try:
        mongo.db.person.replace_one(query,data)
        person = Person(entries=data)
    except Exception:
         abort(500)
    return person.serialize()


@app.route('/person/<int:id>',methods=['DELETE'])
def delete_person(id):
    query = {"_id":id}
    result = mongo.db.person.delete_one(query).deleted_count
    if result!=0:
        return "ok"
    else:
        abort(404)
    print(result.deleted_count)
    return "ok"

@app.route('/family/<int:id>',methods=['GET'])
def get_family(id):
    family = mongo.db.family.find_one_or_404({'_id': id})
    family=Family(entries=family)
    return family.serialize()

@app.route('/family/<int:id>',methods=['DELETE'])
def delete_family(id):
    query = {"_id":id}
    result = mongo.db.family.delete_one(query).deleted_count
    ## todo:maybe need to delete the connection between family & person
    if result!=0:
        return "ok"
    else:
        abort(404)
    print(result.deleted_count)
    return "ok"

@app.route('/family/<int:id>',methods=['PUT'])
def update_family(id):
    query = {"_id": id}
    data = json.loads(request.get_data())
    data = check_data(FamilySchema,data)
    try:
        mongo.db.family.replace_one(query,data)
        family = Family(entries=data)
    except Exception:
         abort(500)
    return Family.serialize()

@app.route('/family',methods=['POST'])
def add_family():
    data = json.loads(request.get_data())
    data = check_data(FamilySchema, data)    #
    try:
        family=Family(entries=data)
        mongo.db.family.insert_one(family)
    except Exception:
        pass
    return family.serialize()

@app.route('/relation/<int:id>',methods=['GET'])
def get_relation(id):
    relation = mongo.db.relation.find_one_or_404({'_id': id})
    relation=Relation(entries=relation)
    return relation.serialize()

@app.route('/relation/<int:id>',methods=['DELETE'])
def delete_relation(id):
    query = {"_id":id}
    result = mongo.db.relation.delete_one(query).deleted_count
    ## todo:maybe need to delete the connection between family & person
    if result!=0:
        return "ok"
    else:
        abort(404)
    print(result.deleted_count)
    return "ok"

@app.route('/relation',methods=['POST'])
def add_relation():
    data = json.loads(request.get_data())
    data = check_data(RelationSchema, data)
    try:
        relation=Relation(entries=data)
        mongo.db.relation.insert_one(relation)
    except Exception:
        pass
    return relation.serialize()

@app.route('/relation/<int:id>',methods=['PUT'])
def update_person(id):
    query = {"_id":id}
    data = json.loads(request.get_data())
    data = check_data(RelationSchema,data)
    try:
        mongo.db.relation.replace_one(query,data)
        relation = Relation(entries=data)
    except Exception:
         abort(500)
    return relation.serialize()




if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
    
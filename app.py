from flask import Flask, render_template, request
from flask_pymongo import PyMongo

from models.person import Person
import json
from bson import json_util

app = Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/our_genealogy")

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/person/<int:id>', methods=['GET'])
def query_person(id):    
    if id:    
        persons = mongo.db.person.find({'_id': id})
        if persons:
            person=Person(entries=persons[0])       
            return person.serialize()
        else:    
            return 'No user found!'

@app.route('/person', methods=['POST'])
def add_person():
    # TODO: Validation (use ORM)
    # Now we have to give MongoDB an `_id` column
    data = json.loads(request.get_data())
    try:
        person=Person(entries=data)
        print(person)
        print(person.serialize())
        mongo.db.person.insert_one(person.serialize())
    except Exception:
        pass
    
    return person.serialize()


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
    
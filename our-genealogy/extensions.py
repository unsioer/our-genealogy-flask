from flask_apscheduler import APScheduler
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_redis import FlaskRedis

jwt_manager = JWTManager()
mongo = PyMongo()
redis_client = FlaskRedis()
scheduler = APScheduler()

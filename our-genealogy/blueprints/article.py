
from flask import Blueprint, request, jsonify
import json
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity
)

from models.article import Article
from utils.utils import generateID

from utils.ApiError import *
from extensions import mongo,redis_client
from schema.schemas import(
    check_data,
    PersonSchema
)

articles_bp = Blueprint("articles",__name__)

@articles_bp.route('/articles', methods=['GET'])
def get_articles():
    query = {"access_level": {"$in": [0]}}
    articles = list(mongo.db.article.find(query))
    print(articles)
    return jsonify(articles)


@articles_bp.route('/articles/mine', methods=['GET'])
@jwt_required()
def get_my_articles():
    currentUserID = get_jwt_identity()
    query = {"user_id": {"$in": [currentUserID]}}
    articles = list(mongo.db.article.find(query))
    print(articles)
    return jsonify(articles)


@articles_bp.route('/article/<string:id>', methods=['GET'])
def get_article(id):
    articles = mongo.db.article.find_one_or_404({'_id': id})
    article = Article(entries=articles)
    if article.access_level == 0:
        return article.serialize()
    else:
        raise ApiError(NO_AUTH,403)

@articles_bp.route('/articles/<string:id>/view',methods=['PUT'])
def add_view(id):
    ip = request.remote_addr
    key = ip+":"+id
    if not redis_client.exists(key):
        redis_client.set(key,"True")
        redis_client.expire(key,24*3600) #ip 24h超时，同一ip24h内访问仅计算一次
        article_key = "viewCount:"+id
        redis_client.incr(article_key) #redis中增加浏览数
        #之后定时自动写回
        return "OK"

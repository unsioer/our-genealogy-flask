
from flask import Blueprint, request, jsonify
import json
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity, get_jwt
)

from models.article import Article
from utils.utils import generateID,currentTime

from utils.ApiError import *
from extensions import mongo,redis_client
from schema.schemas import(
    check_data,
    PersonSchema
)
from utils.authCheck import *

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
    # 似乎也要做权限校验 有点麻烦 需要访问数据库
    ip = request.remote_addr
    key = ip+":"+id
    if not redis_client.exists(key):
        redis_client.set(key,"True")
        redis_client.expire(key,24*3600) #ip 24h超时，同一ip24h内访问仅计算一次
        article_key = "viewCount:"+id
        redis_client.incr(article_key) #redis中增加浏览数
        #之后定时自动写回
        return "ok"

@articles_bp.route('/article/<string:id>/like',methods=['PUT'])
@jwt_required()
def add_like(id):
    user_id = get_jwt_identity()
    is_admin = get_jwt()['is_admin']
    like_query={"$and":[{"user_id":user_id},{"article_id":id}]}
    like = mongo.db.like.find_one(like_query)
    if like!=None:
        raise ApiError(REPETITIVE_OPERATION)
    query = {"_id":id}
    articles = mongo.db.article.find_one_or_404({'_id': id})
    article = Article(entries=articles)
    if check_article_like_auth(article,is_admin,user_id):
        update_data = { "$inc": { "like_num":1} }
        mongo.db.article.update_one(query,update_data)
        like = dict()
        like['_id'] = generateID()
        like['user_id']=user_id
        like['article_id'] = article.id
        like['time']=currentTime()
        mongo.db.like.insert_one(like)
        return "ok"
    raise ApiError(NO_AUTH,403)

@articles_bp.route('/article/<string:id>/like',methods=['DELETE'])
@jwt_required()
def cancel_like(id):
    user_id = get_jwt_identity()
    is_admin = get_jwt()['is_admin']
    like_query={"$and":[{"user_id":user_id},{"article_id":id}]}
    query = {"_id":id}
    articles = mongo.db.article.find_one_or_404({'_id': id})
    article = Article(entries=articles)
    if check_article_like_auth(article,is_admin,user_id):
        count = mongo.db.like.delete_one(like_query).deleted_count
        print(count)
        if count!=0:
            update_data = { "$inc": { "like_num":-1} }
            mongo.db.article.update_one(query,update_data)
            return "ok"
        else:
            raise ApiError(NOT_FOUND,404)
    raise ApiError(NO_AUTH,403)


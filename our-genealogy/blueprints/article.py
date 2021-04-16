
from flask import Blueprint, request, jsonify
import json
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity
)

from models.article import Article
from utils.utils import generateID

from utils.ApiError import *
from extensions import mongo
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
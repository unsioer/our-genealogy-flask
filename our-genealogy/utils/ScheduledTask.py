from extensions import redis_client,mongo
from models.article import Article


def add_view():
    article_ids = redis_client.keys("viewCount:*")
    for id in article_ids:
        # print((id.decode()))
        # id = id.decode()
        v = redis_client.get(id)
        article_id = id.split(":")[1]
        viewCount = eval(v)
        # viewCount = eval(v.decode())
        if viewCount!=0:
            print(viewCount)
            redis_client.set(id,0)
            articles = mongo.db.article.find_one_or_404({'_id': article_id})
            article = Article(entries=articles)
            article.click_num+=viewCount
            query = {"_id": article_id}
            update_data = {"$set": {"click_num":article.click_num}}
            mongo.db.article.update_one(query, update_data)

from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(verbose=True)

class BaseConfig:
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
class DevelopmentConfig(BaseConfig):
    MONGO_URI = os.getenv("MONGO_URI")
    REDIS_URL = os.getenv("REDIS_URL")
    JOBS = [
        {
            'id': 'add_view', # 任务id
            'func': 'our-genealogy:utils.ScheduledTask.add_view', # 任务执行程序
            'args': None, # 执行程序参数
            'trigger': 'interval', # 任务执行类型，定时器
            'seconds': 300, # 任务执行时间，单位秒
        }
    ]

config = {
    'development': DevelopmentConfig,
}
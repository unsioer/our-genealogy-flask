from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(verbose=True)

class BaseConfig:
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
class DevelopmentConfig(BaseConfig):
    MONGO_URI = os.getenv("MONGO_URI")

config = {
    'development': DevelopmentConfig,
}
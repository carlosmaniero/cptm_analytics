import settings
from pymongo import MongoClient


def get_database():
    client = MongoClient()
    return client[settings.database_name]

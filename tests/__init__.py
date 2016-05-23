import settings
from core.conf import parse_settings
from pymongo import MongoClient


def setup_module(module):
    '''
    This method will be install the test database, dropping any data
    before this
    '''
    # set the database as test database
    settings.database_name = settings.database_test_name

    # drop the test databse
    connection = MongoClient()
    connection.drop_database(settings.database_name)

    # parse the settings
    parse_settings()

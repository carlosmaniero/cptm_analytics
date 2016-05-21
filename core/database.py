'''
------------------------------------------------------------------------------
Database
------------------------------------------------------------------------------
This module have utils methods about database control.
'''
import settings
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor

_executor = None
_db = None


def get_current_database():
    ''' This function return a PyMongo db object.'''
    global _db
    if _db is None:
        client = MongoClient()
        _db = client[settings.database_name]
    return _db


def get_current_executor():
    '''
    This returns the executor thats will be used to proccess database requests
    '''
    global _executor
    if _executor is None:
        _executor = ThreadPoolExecutor(
            max_workers=settings.data_workers
        )
    return _executor


class DataControl(object):
    '''
    The is a base data control, this include simple function like
    get_database and get_executor.

    Use the @run_on_executor from the tornado.concurrent module, to run it in
    a executor.

    By default, the executor is defined in the get_executor, and this return,
    a default executor. You can specify your executor overriding this module.
    '''
    def __init__(self):
        self.db = self.get_database()
        self.executor = self.get_executor()

    def get_database(self):
        '''
        Get the database used on the data control.

        By default, returns the get_current_database()
        function from this module.
        '''
        return get_current_database()

    def get_executor(self):
        '''
        Get the executor used on the data control.

        By default, returns the get_current_executor()
        function from this module.
        '''
        return get_current_executor()

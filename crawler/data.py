'''
------------------------------------------------------------------------------
Crawler Data
------------------------------------------------------------------------------

This module do the comunication with the mongodb using the DataControl.
'''
import datetime
from tornado.concurrent import run_on_executor
from core.database import DataControl


class CrawlerDataControl(DataControl):
    @run_on_executor
    def add_response(self, response, request_time):
        '''
        Insert a new document in the responses collection.
        This automaticly add a downloaded_in field (datetime).
        '''
        data = {
            'response': response,
            'request_time': request_time,
            'downloaded_in': datetime.datetime.now()
        }
        return self.db.responses.insert(data)

    @run_on_executor
    def count_response(self):
        '''
        Count the total of responses of the responses collection.
        '''
        return self.db.responses.count()

    @run_on_executor
    def pop_response(self):
        '''
        Return a response and delete it from the responses collection.
        '''
        return self.db.responses.find_and_modify(remove=True)

    @run_on_executor
    def add_processed(self, response):
        '''
        Insert a new document in the processed collection.
        This automaticly add a processed_in field (datetime).
        '''
        response['readings'] = [datetime.datetime.now()]
        self.db.processed.insert(response)

    @run_on_executor
    def add_processed_reading(self, response):
        response.setdefault('readings', [])
        response['readings'].append(datetime.datetime.now())
        self.db.processed.save(response)

    @run_on_executor
    def count_processed(self):
        '''
        Count the total of responses of the processed collection.
        '''
        return self.db.processed.count()

    @run_on_executor
    def get_lastest_processed(self):
        '''
        Get the lastest object processed.
        '''
        sort_by = (
            ('processed_in', -1),
        )
        cursor = self.db.processed.find().sort(sort_by).limit(1)
        try:
            latest = cursor[0]
        except IndexError:
            latest = None
        return latest

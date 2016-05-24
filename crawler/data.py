'''
------------------------------------------------------------------------------
Crawler Data
------------------------------------------------------------------------------

This module do the comunication with the mongodb using the DataControl.
'''
import datetime
from tornado.concurrent import run_on_executor
from tornado import gen
from core.database import DataControl


class CrawlerDataControl(DataControl):
    _response_queue = []

    @gen.coroutine
    def add_response(self, response, request_time):
        '''
        Insert a new document in the _responses_queue.
        This automaticly add a downloaded_in field (datetime).
        '''
        data = {
            'response': response,
            'request_time': request_time,
            'downloaded_in': datetime.datetime.now()
        }
        self._response_queue.append(data)
        return data

    @gen.coroutine
    def count_response(self):
        '''
        Count the total of responses.
        '''
        return len(self._response_queue)

    @run_on_executor
    def pop_response(self):
        '''
        Return a response and delete it from the responses collection.
        '''
        return self._response_queue.pop(0)

    @run_on_executor
    def add_processed(self, response):
        '''
        Insert a new document in the processed collection.
        This automaticly add a processed_in field (datetime).
        '''
        now = datetime.datetime.now()
        response['readings'] = [now]
        response['latest_reading'] = now
        response['first_reading'] = now
        self.db.processed.insert(response)
        return response

    @run_on_executor
    def add_processed_reading(self, response):
        response.setdefault('readings', [])
        now = datetime.datetime.now()
        response['readings'].append(now)
        response['latest_reading'] = now
        self.db.processed.save(response)
        return response

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
            ('latest_reading', -1),
        )
        cursor = self.db.processed.find().sort(sort_by).limit(1)
        try:
            latest = cursor[0]
        except IndexError:
            latest = None
        return latest

    @run_on_executor
    def add_line_info(self, line, response):
        data = {
            'line': line,
            'info': response['info'][line],
            'readings': [{
                'reading_in': response['latest_reading'],
                'response': response['_id']
            }],
            'latest_reading': response['latest_reading']
        }
        self.db.line.insert(data)
        return data

    @run_on_executor
    def add_line_reading(self, line_data, response):
        line_data.setdefault('readings', [])
        line_data['readings'].append({
            'reading_in': response['latest_reading'],
            'response': response['_id']
        })
        line_data['latest_reading'] = response['latest_reading']
        self.db.line.save(line_data)
        return response

    @run_on_executor
    def get_lastest_line_info(self, line):
        '''
        Get the lastest line info.
        '''
        sort_by = (
            ('latest_reading', -1),
        )
        cursor = self.db.line.find({'line': line}).sort(sort_by).limit(1)
        try:
            latest = cursor[0]
        except IndexError:
            latest = None
        return latest

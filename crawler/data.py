import datetime
import settings
from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor


class CrawlerDataControl(object):
    def __init__(self):
        self.executor = ThreadPoolExecutor(
            max_workers=settings.crawler_data_workers
        )
        self.db = settings.db

    @run_on_executor
    def add_response(self, response, request_time):
        data = {
            'response': response,
            'request_time': request_time,
            'downloaded_in': datetime.datetime.now()
        }
        self.db.responses.insert(data)

    @run_on_executor
    def count_response(self):
        return self.db.responses.count()

import datetime
from tornado.concurrent import run_on_executor
from core.database import DataControl


class CrawlerDataControl(DataControl):
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

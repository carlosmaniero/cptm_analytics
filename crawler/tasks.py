"""
------------------------------------------------------------------------------
Crawler Tasks
------------------------------------------------------------------------------

This module define the tasks that will be running on the tornado IOLoop using
the concurrent Tornado API
[http://www.tornadoweb.org/en/stable/concurrent.html].
"""
import time
import settings
from tornado import gen
from tornado import log
from concurrent.futures import ThreadPoolExecutor
from core.tasks import Tasks
from crawler.crawler import Crawler
from crawler.data import CrawlerDataControl


class CrawlerTasks(Tasks):
    def __init__(self):
        self._crawler = Crawler()
        self.executor = ThreadPoolExecutor(
            max_workers=settings.crawler_workers
        )
        self.data = CrawlerDataControl()

    @gen.coroutine
    def task_download_data(self):
        while True:
            start_time = time.time()
            response = yield self.run_on_executor(
                self._crawler.download_data
            )
            request_time = time.time() - start_time
            yield self.data.add_response(response, request_time)
            yield gen.sleep(settings.crawler_download_data_interval)

    @gen.coroutine
    def task_process_data(self):
        while True:
            count = yield self.data.count_response()
            log.logging.info('{} to process.'. format(count))
            yield gen.sleep(settings.crawler_download_data_interval)

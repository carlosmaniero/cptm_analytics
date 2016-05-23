'''
------------------------------------------------------------------------------
Crawler Tasks
------------------------------------------------------------------------------

This module define the tasks that will be running on the tornado IOLoop using
the concurrent Tornado API
[http://www.tornadoweb.org/en/stable/concurrent.html].
'''
import time
import settings
from tornado import gen
from tornado import log
from concurrent.futures import ThreadPoolExecutor
from core.tasks import Tasks
from crawler.crawler import Crawler, CrawlerParseException
from crawler.data import CrawlerDataControl


class CrawlerTasks(Tasks):
    '''
    This class is the implementation of all crawler background tasks.
    '''
    def __init__(self):
        self.crawler = Crawler()
        self.executor = ThreadPoolExecutor(
            max_workers=settings.crawler_workers
        )
        self.data = CrawlerDataControl()

    @gen.coroutine
    def task_download_data(self):
        '''
        Call the crawler download_data in a executor
        every settings.crawler_download_data_interval seconds.
        '''
        while True:
            start_time = time.time()
            log.logging.info('Start downloading')
            response = yield self.run_on_executor(
                self.crawler.download_data
            )
            request_time = time.time() - start_time
            log.logging.info('End downloading in {}s'.format(request_time))
            yield self.data.add_response(response, request_time)
            yield gen.sleep(settings.crawler_download_data_interval)

    @gen.coroutine
    def compare_line(self, line, response):
        latest_line = yield self.data.get_lastest_line_info(line)
        if latest_line and latest_line['info'] == response['info'][line]:
            log.logging.info('Log is equal from the {} line'.format(line))
            yield self.data.add_line_reading(latest_line, response)
            return True     # NOQA
        return False        # NOQA

    @gen.coroutine
    def save_lines(self, response):
        for line in self.crawler.LINES:
            log.logging.info('Saving the {} line'.format(line))
            equals = yield self.compare_line(line, response)
            if not equals:
                log.logging.info('Creating a line info from {}'.format(line))
                yield self.data.add_line_info(line, response)

    @gen.coroutine
    def process_data(self, response):
        '''
        Process a response using parse_content and add data to
        processed collection.
        '''
        log.logging.info('Processing the {} response'.format(
            str(response['_id'])
        ))
        try:
            info = self.crawler.parse_content(response['response']['content'])
        except CrawlerParseException:
            # add to error database
            pass
        else:
            del response['response']['content']
            response['info'] = info
            equals = False

            latest_response = yield self.data.get_lastest_processed()
            if latest_response:
                if response['info'] == latest_response['info']:
                    response = yield self.data.add_processed_reading(
                        latest_response
                    )
                    equals = True

            if not equals:
                response = yield self.data.add_processed(response)
            yield self.save_lines(response)

    @gen.coroutine
    def task_process_data(self):
        '''
        Check if has new response and send the responses to
        process_data if found.
        This is executed every settings.crawler_process_data_interval seconds.
        '''
        while True:
            count = yield self.data.count_response()
            log.logging.info('{} to process.'. format(count))

            if count:
                response = yield self.data.pop_response()
                yield self.process_data(response)

            yield gen.sleep(settings.crawler_process_data_interval)

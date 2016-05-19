from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor
import requests
import settings
import time
import datetime
from bs4 import BeautifulSoup


class CrawlerParseException(Exception):
    pass


class Crawler(object):
    executor = ThreadPoolExecutor(max_workers=settings.crawler_workers)

    @run_on_executor
    def fetch_data(self):
        start_request = time.time()
        response = requests.get('http://cptm.sp.gov.br/')
        request_time = time.time() - start_request

        data = {
            'content': response.content,
            'status_code': response.status_code,
            'response_datetime': datetime.datetime.now(),
            'request_time': request_time
        }

        return data

    @run_on_executor
    def parse_content(self, content):
        soup_content = BeautifulSoup(content, 'html.parser')
        status = {}
        all_normal = True

        try:
            for line in lines:
                status[line] = self.get_status_line(soup_content, line)
                if status[line] != 'status_normal':
                    all_normal = False
        except IndexError:
            raise CrawlerParseException('Error on parse Content') 
        else:
            if all_normal:
                del request['content']

            request['status'] = status
            request['process_time'] = time.time() - start_process

            yield from loop.run_in_executor(
                None, db.processed.save, request
            )
            print('[Process]: Processed  in {} seconds'.format(
                request['process_time']
            ))

    def get_problem_nature(self, info):
        if 'Serviços de Manutenção' in info:
            return 'maintenance'
        return 'other'

    def get_status_line(self, soup, line):
        div_line = soup.findAll('div', {'class': line})[0]
        span_info = div_line.findAll('span')[1]
        name = span_info['class'][0]
        data = {
            'name': name
        }
        try:
            info = span_info['data-original-title']
        except KeyError:
            pass
        else:
            data['info'] = info
            data['nature'] = self.get_problem_nature(info)

        return data

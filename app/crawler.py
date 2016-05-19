import requests
import settings
from concurrent.futures import ThreadPoolExecutor
from collections import namedtuple
from bs4 import BeautifulSoup
from tornado.concurrent import run_on_executor


CptmResponse = namedtuple('CptmResponse', ['status_code', 'content'])


class CrawlerParseException(Exception):
    pass


class Crawler(object):
    executor = ThreadPoolExecutor(max_workers=settings.crawler_workers)
    LINES = [
        'rubi', 'diamante', 'esmeralda', 'turquesa', 'coral', 'safira'
    ]
    NATURE_PROBLEMS = (
        ('Serviços de Manutenção', 'maintenance'),
        ('Obras', 'works'),
    )

    @run_on_executor
    def download_data(self):
        response = requests.get('http://cptm.sp.gov.br/')

        return CptmResponse(
            status_code=response.status_code,
            content=response.content
        )

    @run_on_executor
    def parse_content(self, content):
        soup_content = BeautifulSoup(content, 'html.parser')
        status = {}

        try:
            for line in self.LINES:
                status[line] = self.get_status_line(soup_content, line)
        except IndexError:
            raise CrawlerParseException('Error on parse Content')
        else:
            return status

    def get_problem_nature(self, info):
        for (description, nature) in self.NATURE_PROBLEMS:
            if description == info:
                return nature
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

            # Remove extra spaces
            while '  ' in info:
                info = info.replace('  ', ' ')
        except KeyError:
            pass
        else:
            data['info'] = info
            data['nature'] = self.get_problem_nature(info)

        return data

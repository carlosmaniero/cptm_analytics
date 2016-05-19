"""
------------------------------------------------------------------------------
Crawler
------------------------------------------------------------------------------

This module download and process data from CPTM website using the concurrent
Tornado API [http://www.tornadoweb.org/en/stable/concurrent.html].

"""

import requests
import settings
from concurrent.futures import ThreadPoolExecutor
from collections import namedtuple
from bs4 import BeautifulSoup
from tornado.concurrent import run_on_executor


CptmResponse = namedtuple('CptmResponse', ['status_code', 'content'])


class CrawlerParseException(Exception):
    ''' Exception from Crawler parse errors '''
    pass


class Crawler(object):
    ''' WebCrawler to Download CPTM information. '''
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
        '''
            Download Data from CPTM using requests library.
            This run on a ThreadPoolExecutor.

            usage:
                >>> crawler = Crawler()
                >>> response = yield crawler.download_data()

            return:
                CptmResponse
        '''
        response = requests.get(settings.cptm_url)

        return CptmResponse(
            status_code=response.status_code,
            content=response.content
        )

    @run_on_executor
    def parse_content(self, content):
        '''
            Parse content and returns a dict with info.

            args:
                content: A CptmResponse.content data

            usage:
                >>> crawler = Crawler()
                >>> crawler.parse_content(content)

            returns:
                dict

            raises:
                CrawlerParseException if any line from Crawler.LINES
                is not found.
        '''
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
        ''' Get the problem nature '''
        for (description, nature) in self.NATURE_PROBLEMS:
            if description == info:
                return nature
        return 'other'

    def get_status_line(self, soup, line):
        ''' Return the status of a specific line '''
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

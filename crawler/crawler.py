"""
------------------------------------------------------------------------------
Crawler
------------------------------------------------------------------------------

This module download and process data from CPTM website.

"""

import requests
import settings
from bs4 import BeautifulSoup


class CrawlerParseException(Exception):
    ''' Exception from Crawler parse errors '''
    pass


class Crawler(object):
    ''' WebCrawler to Download CPTM information. '''
    LINES = [
        'rubi', 'diamante', 'esmeralda', 'turquesa', 'coral', 'safira'
    ]
    NATURE_PROBLEMS = (
        ('Serviços de Manutenção', 'maintenance'),
        ('Obras', 'works'),
    )

    def download_data(self):
        '''
            Download Data from CPTM using requests library.
            This run on a ThreadPoolExecutor.

            usage:
                >>> crawler = Crawler()
                >>> response = yield crawler.download_data()

            returns:
                {
                    content: ...,
                    status_code: ...
                }
        '''
        response = requests.get(settings.cptm_url)

        return {
            'status_code': response.status_code,
            'content': response.content
        }

    def parse_content(self, content):
        '''
            Parse content and returns a dict with info.

            args:
                content: A CptmResponse.content data

            usage:
                >>> crawler = Crawler()
                >>> crawler.parse_content(content)

            returns:
                a dict with the LINES as keys containing the
                status of CPTM lines.

            raises:
                CrawlerParseException if any line from LINES
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
        ''' Returns the nature of status using the NATURE_PROBLEMS List'''
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

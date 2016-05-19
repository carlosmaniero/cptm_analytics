from crawler.crawler import Crawler


def test_download_data():
    crawler = Crawler()
    response = crawler.download_data()

    assert response['status_code'] == 200


def test_parse_content():
    crawler = Crawler()
    response = crawler.download_data()

    parsed = crawler.parse_content(response['content'])

    for line in Crawler.LINES:
        assert line in parsed

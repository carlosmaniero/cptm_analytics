import pytest
from app.crawler import Crawler


@pytest.mark.gen_test
def test_download_data():
    crawler = Crawler()
    response = yield crawler.download_data()

    assert response.status_code == 200


@pytest.mark.gen_test
def test_parse_content():
    crawler = Crawler()
    response = yield crawler.download_data()

    parsed = yield crawler.parse_content(response.content)

    for line in Crawler.LINES:
        assert line in parsed

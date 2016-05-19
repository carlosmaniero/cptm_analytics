import pytest
from app.crawler import Crawler


@pytest.mark.gen_test
def test_download_data():
    crawler = Crawler()
    response = yield crawler.download_data()

    assert response.status_code == 200

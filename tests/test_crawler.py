import pytest
from tornado import gen
from crawler.crawler import Crawler
from crawler.data import CrawlerDataControl
from crawler.tasks import CrawlerTasks
from tests import setup_module  # NOQA


def test_download_data():
    '''
    Run a single test downloading the CPTM data and checking the status_code
    using the Crawler.download_data().
    '''
    crawler = Crawler()
    response = crawler.download_data()

    assert response['status_code'] == 200


def test_parse_content():
    '''
    Test the Crawler.parse_content() method. This check if all line from the
    Crawler.LINES is in parsed_content function return.
    '''
    crawler = Crawler()
    response = crawler.download_data()

    parsed = crawler.parse_content(response['content'])

    for line in Crawler.LINES:
        assert line in parsed


@pytest.mark.gen_test
def test_download_task():
    '''
    Test the CrawlerTask.task_download_data() this will run the task, and
    check if this work comparing if the total of responses of the database is
    increased before 3 seconds.
    '''
    tasks = CrawlerTasks()
    data = CrawlerDataControl()
    # Check for downloaded data
    total_downloaded = yield data.count_response()

    # Running downloads task
    tasks.task_download_data()

    # Wait for 2 seconds
    yield gen.sleep(2)

    # Check fot downloaded date
    new_total = yield data.count_response()

    # Assert if the crawler works
    assert new_total > total_downloaded


@pytest.mark.gen_test
def test_process_task():
    '''
    This test will call the CrawlerTasks.task_process_data() and will compare
    if the response collection will be decreased and the processed collection
    are increased.
    '''
    tasks = CrawlerTasks()
    data = CrawlerDataControl()
    # Check for downloaded data
    total_downloaded = yield data.count_response()

    # Check if no responses found
    if total_downloaded == 0:
        # Running downloads task
        task_download = tasks.task_download_data()
        total = 0

        while total_downloaded == 0:
            total += 1
            total_downloaded = yield data.count_response()
            # Wait for 3 seconds to get a response
            # If this fails check for CPTM conection
            assert total <= 3
            yield gen.sleep(1)

        # Stop the task_download
        task_download.cancel()

    total_downloaded = yield data.count_response()
    # Check total processed in the database
    total_processed = yield data.count_processed()

    # Start processing task
    task_process = tasks.task_process_data()

    total = 3
    new_total_downloaded = total_downloaded
    while new_total_downloaded == total_downloaded:
        # Wait 3 seconds to process the response
        yield gen.sleep(1)
        new_total_downloaded = yield data.count_response()
        if total_downloaded == new_total_downloaded:
            total -= 1
            assert total > 0
        else:
            # Stop task_process
            task_process.cancel()
            # Check the total in downloaded queue
            new_total_downloaded = yield data.count_response()
            # Check the total processed
            new_total_processed = yield data.count_processed()
            # Calculate the total removed from the downloaded queue
            processed = total_downloaded - new_total_downloaded
            # Check if the total processed is increased
            # in the processed collection
            assert total_processed == new_total_processed - processed

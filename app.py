import tornado.ioloop
import tornado.web
import tornado.gen
import settings
from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor
from pymongo import MongoClient


client = MongoClient()
db = client[settings.database_name]


class MainHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(max_workers=10)

    @run_on_executor
    def get(self):
        global i
        self.write("Hello, world {}".format(i))


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ], **settings.__dict__)


if __name__ == "__main__":
    app = make_app()
    app.listen(settings.port)
    loop = tornado.ioloop.IOLoop.current()
    loop.start()

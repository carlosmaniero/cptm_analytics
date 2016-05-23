import tornado.ioloop
import tornado.web
import tornado.gen
import tornado.options
import settings
from crawler.tasks import CrawlerTasks
from core.tasks import install_tasks
from core.conf import parse_settings


if __name__ == "__main__":
    # parse settings
    parse_settings()

    # parse tornado options
    tornado.options.parse_command_line()

    # running app
    app = tornado.web.Application([], **settings.__dict__)
    app.listen(settings.port)

    # get event loop
    loop = tornado.ioloop.IOLoop.current()

    # Install tasks
    install_tasks(loop, [
        CrawlerTasks
    ])

    # start loop
    try:
        loop.start()
    except KeyboardInterrupt:
        print('\nbye, bye')
        loop.close()

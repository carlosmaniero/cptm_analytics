import tornado.ioloop
import tornado.web
import tornado.gen
import tornado.options
import settings
from crawler.tasks import CrawlerTasks
from core.tasks import install_tasks


if __name__ == "__main__":
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
    loop.start()

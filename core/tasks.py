"""
------------------------------------------------------------------------------
Tasks
------------------------------------------------------------------------------

This module define the tasks that will be running on the tornado IOLoop using
the concurrent Tornado API
[http://www.tornadoweb.org/en/stable/concurrent.html].
"""
from tornado.concurrent import run_on_executor


class Tasks(object):
    @run_on_executor
    def run_on_executor(self, fn, *args, **kwargs):
        return fn(*args, **kwargs)

    def get_all_tasks(self):
        methods = []
        for method in dir(self):
            if method.startswith('task_'):
                fn = getattr(self, method)
                if hasattr(fn, '__call__'):
                    methods.append(fn)
        return methods


def install_tasks(loop, task_classes):
    for task_class in task_classes:
        tasks_control = task_class()
        for task in tasks_control.get_all_tasks():
            loop.add_callback(task)

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
        '''
        Run any function in the in the task executor.

        usage:

            >>> fn_ret = yield self.run_on_executor(fn, *fn_args, **fn_kwargs)

        When the fn_args and fn_kwargs are the args and kwargs from the fn
        and the fn_ret are the return of the fn function.
        '''
        return fn(*args, **kwargs)

    def get_tasks(self):
        '''
        This method return all task methods from this class.
        By default, the this returns any methods started with the task_ prefix.
        '''
        methods = []
        for method in dir(self):
            if method.startswith('task_'):
                fn = getattr(self, method)
                if hasattr(fn, '__call__'):
                    methods.append(fn)
        return methods


def install_tasks(loop, task_classes):
    '''
    This function will add all tasks in the loop using the add_callback method.
    The task_class receive a list of Task class and get all tasks using the
    get_tasks method.

    args:
        loop = A Tornado IOLoop
        task_classes = A list from Task sub Classe.
    '''
    for task_class in task_classes:
        tasks_control = task_class()
        for task in tasks_control.get_tasks():
            loop.add_callback(task)

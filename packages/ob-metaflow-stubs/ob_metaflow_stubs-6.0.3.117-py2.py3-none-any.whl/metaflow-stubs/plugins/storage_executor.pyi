##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.12.27.1+obcheckpoint(0.1.2);ob(v1)                               #
# Generated on 2024-11-13T19:05:29.385300                                        #
##################################################################################

from __future__ import annotations


class MetaflowException(Exception, metaclass=type):
    def __init__(self, msg = "", lineno = None):
        ...
    def __str__(self):
        ...
    ...

class StorageExecutor(object, metaclass=type):
    """
    Thin wrapper around a ProcessPoolExecutor, or a ThreadPoolExecutor where
    the former may be unsafe.
    """
    def __init__(self, use_processes = False):
        ...
    def warm_up(self):
        ...
    def submit(self, *args, **kwargs):
        ...
    ...

def handle_executor_exceptions(func):
    """
    Decorator for handling errors that come from an Executor. This decorator should
    only be used on functions where executor errors are possible. I.e. the function
    uses StorageExecutor.
    """
    ...


##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.12.27.1+obcheckpoint(0.1.2);ob(v1)                               #
# Generated on 2024-11-13T19:05:29.381212                                        #
##################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

class MetaflowException(Exception, metaclass=type):
    def __init__(self, msg = "", lineno = None):
        ...
    def __str__(self):
        ...
    ...

class MetaflowInternalError(metaflow.exception.MetaflowException, metaclass=type):
    ...

class Azure(object, metaclass=type):
    @classmethod
    def get_root_from_config(cls, echo, create_on_absent = True):
        ...
    def __init__(self):
        ...
    def __enter__(self):
        ...
    def __exit__(self, *args):
        ...
    def get(self, key = None, return_missing = False):
        """
        Key MUST be a fully qualified path with uri scheme.  azure://<container_name>/b/l/o/b/n/a/m/e
        """
        ...
    def put(self, key, obj, overwrite = True):
        """
        Key MUST be a fully qualified path.  <container_name>/b/l/o/b/n/a/m/e
        """
        ...
    def info(self, key = None, return_missing = False):
        ...
    ...

class AzureObject(object, metaclass=type):
    def __init__(self, url, path, exists, size):
        ...
    @property
    def path(self):
        ...
    @property
    def url(self):
        ...
    @property
    def exists(self):
        ...
    @property
    def size(self):
        ...
    ...


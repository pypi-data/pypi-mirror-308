######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.12.30.1+obcheckpoint(0.1.4);ob(v1)                                                   #
# Generated on 2024-11-13T23:34:52.896666                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

from ...exception import MetaflowException as MetaflowException

class AirflowException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, msg):
        ...
    ...

class NotSupportedException(metaflow.exception.MetaflowException, metaclass=type):
    ...


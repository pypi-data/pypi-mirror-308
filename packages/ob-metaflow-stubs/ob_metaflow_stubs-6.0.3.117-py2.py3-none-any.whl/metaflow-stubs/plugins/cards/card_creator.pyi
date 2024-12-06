##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.12.27.1+obcheckpoint(0.1.2);ob(v1)                               #
# Generated on 2024-11-13T19:05:29.403239                                        #
##################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.metaflow_current

current: metaflow.metaflow_current.Current

ASYNC_TIMEOUT: int

class CardProcessManager(object, metaclass=type):
    """
    This class is responsible for managing the card creation processes.
    """
    ...

class CardCreator(object, metaclass=type):
    def __init__(self, top_level_options):
        ...
    def create(self, card_uuid = None, user_set_card_id = None, runtime_card = False, decorator_attributes = None, card_options = None, logger = None, mode = "render", final = False, sync = False):
        ...
    ...


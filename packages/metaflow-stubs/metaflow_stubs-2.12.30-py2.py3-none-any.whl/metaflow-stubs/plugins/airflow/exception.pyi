######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.12.30                                                                                #
# Generated on 2024-11-13T13:50:31.339964                                                            #
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


######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.12.30                                                                                #
# Generated on 2024-11-13T13:50:31.350016                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.plugins.pypi.conda_environment

from .conda_environment import CondaEnvironment as CondaEnvironment

class PyPIEnvironment(metaflow.plugins.pypi.conda_environment.CondaEnvironment, metaclass=type):
    ...


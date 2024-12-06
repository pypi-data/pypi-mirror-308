##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.12.27.1+obcheckpoint(0.1.2);ob(v1)                               #
# Generated on 2024-11-13T19:05:29.419845                                        #
##################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.decorators

EXT_PKG: str

class MetaDatum(tuple, metaclass=type):
    """
    MetaDatum(field, value, type, tags)
    """
    @staticmethod
    def __new__(_cls, field, value, type, tags):
        """
        Create new instance of MetaDatum(field, value, type, tags)
        """
        ...
    def __repr__(self):
        """
        Return a nicely formatted representation string
        """
        ...
    def __getnewargs__(self):
        """
        Return self as a plain tuple.  Used by copy and pickle.
        """
        ...
    ...

INFO_FILE: str

class CondaStepDecorator(metaflow.decorators.StepDecorator, metaclass=type):
    """
    Specifies the Conda environment for the step.
    
    Information in this decorator will augment any
    attributes set in the `@conda_base` flow-level decorator. Hence,
    you can use `@conda_base` to set packages required by all
    steps and use `@conda` to specify step-specific overrides.
    
    Parameters
    ----------
    packages : Dict[str, str], default {}
        Packages to use for this step. The key is the name of the package
        and the value is the version to use.
    libraries : Dict[str, str], default {}
        Supported for backward compatibility. When used with packages, packages will take precedence.
    python : str, optional, default None
        Version of Python to use, e.g. '3.7.4'. A default value of None implies
        that the version used will correspond to the version of the Python interpreter used to start the run.
    disabled : bool, default False
        If set to True, disables @conda.
    """
    def __init__(self, attributes = None, statically_defined = False):
        ...
    def is_attribute_user_defined(self, name):
        ...
    def step_init(self, flow, graph, step, decos, environment, flow_datastore, logger):
        ...
    def runtime_init(self, flow, graph, package, run_id):
        ...
    def runtime_task_created(self, task_datastore, task_id, split_index, input_paths, is_cloned, ubf_context):
        ...
    def task_pre_step(self, step_name, task_datastore, meta, run_id, task_id, flow, graph, retry_count, max_retries, ubf_context, inputs):
        ...
    def runtime_step_cli(self, cli_args, retry_count, max_user_code_retries, ubf_context):
        ...
    def runtime_finished(self, exception):
        ...
    ...

class CondaFlowDecorator(metaflow.decorators.FlowDecorator, metaclass=type):
    """
    Specifies the Conda environment for all steps of the flow.
    
    Use `@conda_base` to set common libraries required by all
    steps and use `@conda` to specify step-specific additions.
    
    Parameters
    ----------
    packages : Dict[str, str], default {}
        Packages to use for this flow. The key is the name of the package
        and the value is the version to use.
    libraries : Dict[str, str], default {}
        Supported for backward compatibility. When used with packages, packages will take precedence.
    python : str, optional, default None
        Version of Python to use, e.g. '3.7.4'. A default value of None implies
        that the version used will correspond to the version of the Python interpreter used to start the run.
    disabled : bool, default False
        If set to True, disables Conda.
    """
    def __init__(self, attributes = None, statically_defined = False):
        ...
    def is_attribute_user_defined(self, name):
        ...
    def flow_init(self, flow, graph, environment, flow_datastore, metadata, logger, echo, options):
        ...
    ...


##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.12.27.1+obcheckpoint(0.1.2);ob(v1)                               #
# Generated on 2024-11-13T19:05:29.351938                                        #
##################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.flowspec
    import typing
    import metaflow.parameters
    import metaflow.unbounded_foreach
    import metaflow.datastore.inputs
    import metaflow.exception

class DelayedEvaluationParameter(object, metaclass=type):
    """
    This is a very simple wrapper to allow parameter "conversion" to be delayed until
    the `_set_constants` function in FlowSpec. Typically, parameters are converted
    by click when the command line option is processed. For some parameters, like
    IncludeFile, this is too early as it would mean we would trigger the upload
    of the file too early. If a parameter converts to a DelayedEvaluationParameter
    object through the usual click mechanisms, `_set_constants` knows to invoke the
    __call__ method on that DelayedEvaluationParameter; in that case, the __call__
    method is invoked without any parameter. The return_str parameter will be used
    by schedulers when they need to convert DelayedEvaluationParameters to a
    string to store them
    """
    def __init__(self, name, field, fun):
        ...
    def __call__(self, return_str = False):
        ...
    ...

class Parameter(object, metaclass=type):
    """
    Defines a parameter for a flow.
    
    Parameters must be instantiated as class variables in flow classes, e.g.
    ```
    class MyFlow(FlowSpec):
        param = Parameter('myparam')
    ```
    in this case, the parameter is specified on the command line as
    ```
    python myflow.py run --myparam=5
    ```
    and its value is accessible through a read-only artifact like this:
    ```
    print(self.param == 5)
    ```
    Note that the user-visible parameter name, `myparam` above, can be
    different from the artifact name, `param` above.
    
    The parameter value is converted to a Python type based on the `type`
    argument or to match the type of `default`, if it is set.
    
    Parameters
    ----------
    name : str
        User-visible parameter name.
    default : str or float or int or bool or `JSONType` or a function.
        Default value for the parameter. Use a special `JSONType` class to
        indicate that the value must be a valid JSON object. A function
        implies that the parameter corresponds to a *deploy-time parameter*.
        The type of the default value is used as the parameter `type`.
    type : Type, default None
        If `default` is not specified, define the parameter type. Specify
        one of `str`, `float`, `int`, `bool`, or `JSONType`. If None, defaults
        to the type of `default` or `str` if none specified.
    help : str, optional
        Help text to show in `run --help`.
    required : bool, default False
        Require that the user specified a value for the parameter.
        `required=True` implies that the `default` is not used.
    show_default : bool, default True
        If True, show the default value in the help text.
    """
    def __init__(self, name: str, default: typing.Union[str, float, int, bool, typing.Dict[str, typing.Any], typing.Callable[[], typing.Union[str, float, int, bool, typing.Dict[str, typing.Any]]], None] = None, type: typing.Union[typing.Type[str], typing.Type[float], typing.Type[int], typing.Type[bool], metaflow.parameters.JSONTypeClass, None] = None, help: typing.Optional[str] = None, required: bool = False, show_default: bool = True, **kwargs: typing.Dict[str, typing.Any]):
        ...
    def __repr__(self):
        ...
    def __str__(self):
        ...
    def option_kwargs(self, deploy_mode):
        ...
    def load_parameter(self, v):
        ...
    @property
    def is_string_type(self):
        ...
    def __getitem__(self, x):
        ...
    ...

class MetaflowException(Exception, metaclass=type):
    def __init__(self, msg = "", lineno = None):
        ...
    def __str__(self):
        ...
    ...

class MissingInMergeArtifactsException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, msg, unhandled):
        ...
    ...

class UnhandledInMergeArtifactsException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, msg, unhandled):
        ...
    ...

INCLUDE_FOREACH_STACK: bool

MAXIMUM_FOREACH_VALUE_CHARS: int

INTERNAL_ARTIFACTS_SET: set

class InvalidNextException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, msg):
        ...
    ...

class ParallelUBF(metaflow.unbounded_foreach.UnboundedForeachInput, metaclass=type):
    """
    Unbounded-for-each placeholder for supporting parallel (multi-node) steps.
    """
    def __init__(self, num_parallel):
        ...
    def __getitem__(self, item):
        ...
    ...

class FlowSpec(object, metaclass=_FlowSpecMeta):
    """
    Main class from which all Flows should inherit.
    
    Attributes
    ----------
    index
    input
    """
    def __init__(self, use_cli = True):
        """
        Construct a FlowSpec
        
        Parameters
        ----------
        use_cli : bool, default True
            Set to True if the flow is invoked from __main__ or the command line
        """
        ...
    @property
    def script_name(self) -> str:
        """
        [Legacy function - do not use. Use `current` instead]
        
        Returns the name of the script containing the flow
        
        Returns
        -------
        str
            A string containing the name of the script
        """
        ...
    def __iter__(self):
        """
        [Legacy function - do not use]
        
        Iterate over all steps in the Flow
        
        Returns
        -------
        Iterator[graph.DAGNode]
            Iterator over the steps in the flow
        """
        ...
    def __getattr__(self, name: str):
        ...
    def cmd(self, cmdline, input = {}, output = []):
        """
        [Legacy function - do not use]
        """
        ...
    @property
    def index(self) -> typing.Optional[int]:
        """
        The index of this foreach branch.
        
        In a foreach step, multiple instances of this step (tasks) will be executed,
        one for each element in the foreach. This property returns the zero based index
        of the current task. If this is not a foreach step, this returns None.
        
        If you need to know the indices of the parent tasks in a nested foreach, use
        `FlowSpec.foreach_stack`.
        
        Returns
        -------
        int, optional
            Index of the task in a foreach step.
        """
        ...
    @property
    def input(self) -> typing.Optional[typing.Any]:
        """
        The value of the foreach artifact in this foreach branch.
        
        In a foreach step, multiple instances of this step (tasks) will be executed,
        one for each element in the foreach. This property returns the element passed
        to the current task. If this is not a foreach step, this returns None.
        
        If you need to know the values of the parent tasks in a nested foreach, use
        `FlowSpec.foreach_stack`.
        
        Returns
        -------
        object, optional
            Input passed to the foreach task.
        """
        ...
    def foreach_stack(self) -> typing.Optional[typing.List[typing.Tuple[int, int, typing.Any]]]:
        """
        Returns the current stack of foreach indexes and values for the current step.
        
        Use this information to understand what data is being processed in the current
        foreach branch. For example, considering the following code:
        ```
        @step
        def root(self):
            self.split_1 = ['a', 'b', 'c']
            self.next(self.nest_1, foreach='split_1')
        
        @step
        def nest_1(self):
            self.split_2 = ['d', 'e', 'f', 'g']
            self.next(self.nest_2, foreach='split_2'):
        
        @step
        def nest_2(self):
            foo = self.foreach_stack()
        ```
        
        `foo` will take the following values in the various tasks for nest_2:
        ```
            [(0, 3, 'a'), (0, 4, 'd')]
            [(0, 3, 'a'), (1, 4, 'e')]
            ...
            [(0, 3, 'a'), (3, 4, 'g')]
            [(1, 3, 'b'), (0, 4, 'd')]
            ...
        ```
        where each tuple corresponds to:
        
        - The index of the task for that level of the loop.
        - The number of splits for that level of the loop.
        - The value for that level of the loop.
        
        Note that the last tuple returned in a task corresponds to:
        
        - 1st element: value returned by `self.index`.
        - 3rd element: value returned by `self.input`.
        
        Returns
        -------
        List[Tuple[int, int, Any]]
            An array describing the current stack of foreach steps.
        """
        ...
    def merge_artifacts(self, inputs: metaflow.datastore.inputs.Inputs, exclude: typing.Optional[typing.List[str]] = None, include: typing.Optional[typing.List[str]] = None):
        """
        Helper function for merging artifacts in a join step.
        
        This function takes all the artifacts coming from the branches of a
        join point and assigns them to self in the calling step. Only artifacts
        not set in the current step are considered. If, for a given artifact, different
        values are present on the incoming edges, an error will be thrown and the artifacts
        that conflict will be reported.
        
        As a few examples, in the simple graph: A splitting into B and C and joining in D:
        ```
        A:
          self.x = 5
          self.y = 6
        B:
          self.b_var = 1
          self.x = from_b
        C:
          self.x = from_c
        
        D:
          merge_artifacts(inputs)
        ```
        In D, the following artifacts are set:
          - `y` (value: 6), `b_var` (value: 1)
          - if `from_b` and `from_c` are the same, `x` will be accessible and have value `from_b`
          - if `from_b` and `from_c` are different, an error will be thrown. To prevent this error,
            you need to manually set `self.x` in D to a merged value (for example the max) prior to
            calling `merge_artifacts`.
        
        Parameters
        ----------
        inputs : Inputs
            Incoming steps to the join point.
        exclude : List[str], optional, default None
            If specified, do not consider merging artifacts with a name in `exclude`.
            Cannot specify if `include` is also specified.
        include : List[str], optional, default None
            If specified, only merge artifacts specified. Cannot specify if `exclude` is
            also specified.
        
        Raises
        ------
        MetaflowException
            This exception is thrown if this is not called in a join step.
        UnhandledInMergeArtifactsException
            This exception is thrown in case of unresolved conflicts.
        MissingInMergeArtifactsException
            This exception is thrown in case an artifact specified in `include` cannot
            be found.
        """
        ...
    def next(self, *dsts: typing.Callable[..., None], **kwargs):
        """
        Indicates the next step to execute after this step has completed.
        
        This statement should appear as the last statement of each step, except
        the end step.
        
        There are several valid formats to specify the next step:
        
        - Straight-line connection: `self.next(self.next_step)` where `next_step` is a method in
          the current class decorated with the `@step` decorator.
        
        - Static fan-out connection: `self.next(self.step1, self.step2, ...)` where `stepX` are
          methods in the current class decorated with the `@step` decorator.
        
        - Foreach branch:
          ```
          self.next(self.foreach_step, foreach='foreach_iterator')
          ```
          In this situation, `foreach_step` is a method in the current class decorated with the
          `@step` decorator and `foreach_iterator` is a variable name in the current class that
          evaluates to an iterator. A task will be launched for each value in the iterator and
          each task will execute the code specified by the step `foreach_step`.
        
        Parameters
        ----------
        dsts : Callable[..., None]
            One or more methods annotated with `@step`.
        
        Raises
        ------
        InvalidNextException
            Raised if the format of the arguments does not match one of the ones given above.
        """
        ...
    def __str__(self):
        ...
    def __getstate__(self):
        ...
    ...


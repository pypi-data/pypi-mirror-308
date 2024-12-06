##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.12.27.1+obcheckpoint(0.1.2);ob(v1)                               #
# Generated on 2024-11-13T19:05:29.340728                                        #
##################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.flowspec
    import datetime
    import metaflow_extensions.obcheckpoint.plugins.machine_learning_utilities.datastructures
    import metaflow.client.core
    import metaflow.parameters
    import metaflow._vendor.click.types
    import metaflow.events
    import metaflow.metaflow_current
    import metaflow.runner.metaflow_runner
    import metaflow.datastore.inputs
    import typing
FlowSpecDerived = typing.TypeVar("FlowSpecDerived", bound="FlowSpec", contravariant=False, covariant=False)
StepFlag = typing.NewType("StepFlag", bool)

EXT_PKG: str

def parallel_imap_unordered(func: typing.Callable[[typing.Any], typing.Any], iterable: typing.Iterable[typing.Any], max_parallel: typing.Optional[int] = None, dir: typing.Optional[str] = None) -> typing.Iterator[typing.Any]:
    """
    Parallelizes execution of a function using multiprocessing. The result
    order is not guaranteed.
    
    Parameters
    ----------
    func : Callable[[Any], Any]
        Function taking a single argument and returning a result
    iterable : Iterable[Any]
        Iterable over arguments to pass to fun
    max_parallel int, optional, default None
        Maximum parallelism. If not specified, uses the number of CPUs
    dir : str, optional, default None
        If specified, directory where temporary files are created
    
    Yields
    ------
    Any
        One result from calling func on one argument
    """
    ...

def parallel_map(func: typing.Callable[[typing.Any], typing.Any], iterable: typing.Iterable[typing.Any], max_parallel: typing.Optional[int] = None, dir: typing.Optional[str] = None) -> typing.List[typing.Any]:
    """
    Parallelizes execution of a function using multiprocessing. The result
    order is that of the arguments in `iterable`
    
    Parameters
    ----------
    func : Callable[[Any], Any]
        Function taking a single argument and returning a result
    iterable : Iterable[Any]
        Iterable over arguments to pass to fun
    max_parallel int, optional, default None
        Maximum parallelism. If not specified, uses the number of CPUs
    dir : str, optional, default None
        If specified, directory where temporary files are created
    
    Returns
    -------
    List[Any]
        Results. The items in the list are in the same order as the items
        in `iterable`.
    """
    ...

current: metaflow.metaflow_current.Current

def metadata(ms: str) -> str:
    """
    Switch Metadata provider.
    
    This call has a global effect. Selecting the local metadata will,
    for example, not allow access to information stored in remote
    metadata providers.
    
    Note that you don't typically have to call this function directly. Usually
    the metadata provider is set through the Metaflow configuration file. If you
    need to switch between multiple providers, you can use the `METAFLOW_PROFILE`
    environment variable to switch between configurations.
    
    Parameters
    ----------
    ms : str
        Can be a path (selects local metadata), a URL starting with http (selects
        the service metadata) or an explicit specification <metadata_type>@<info>; as an
        example, you can specify local@<path> or service@<url>.
    
    Returns
    -------
    str
        The description of the metadata selected (equivalent to the result of
        get_metadata()).
    """
    ...

class FlowSpec(object, metaclass=metaflow.flowspec._FlowSpecMeta):
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

class JSONTypeClass(metaflow._vendor.click.types.ParamType, metaclass=type):
    def convert(self, value, param, ctx):
        ...
    def __str__(self):
        ...
    def __repr__(self):
        ...
    ...

JSONType: metaflow.parameters.JSONTypeClass

def S3(*args, **kwargs):
    ...

class IncludeFile(metaflow.parameters.Parameter, metaclass=type):
    """
    Includes a local file as a parameter for the flow.
    
    `IncludeFile` behaves like `Parameter` except that it reads its value from a file instead of
    the command line. The user provides a path to a file on the command line. The file contents
    are saved as a read-only artifact which is available in all steps of the flow.
    
    Parameters
    ----------
    name : str
        User-visible parameter name.
    default : Union[str, Callable[ParameterContext, str]]
        Default path to a local file. A function
        implies that the parameter corresponds to a *deploy-time parameter*.
    is_text : bool, default True
        Convert the file contents to a string using the provided `encoding`.
        If False, the artifact is stored in `bytes`.
    encoding : str, optional, default 'utf-8'
        Use this encoding to decode the file contexts if `is_text=True`.
    required : bool, default False
        Require that the user specified a value for the parameter.
        `required=True` implies that the `default` is not used.
    help : str, optional
        Help text to show in `run --help`.
    show_default : bool, default True
        If True, show the default value in the help text.
    """
    def __init__(self, name: str, required: bool = False, is_text: bool = True, encoding: str = "utf-8", help: typing.Optional[str] = None, **kwargs: typing.Dict[str, str]):
        ...
    def load_parameter(self, v):
        ...
    ...

@typing.overload
def step(f: typing.Callable[[FlowSpecDerived], None]) -> typing.Callable[[FlowSpecDerived, StepFlag], None]:
    """
    Marks a method in a FlowSpec as a Metaflow Step. Note that this
    decorator needs to be placed as close to the method as possible (ie:
    before other decorators).
    
    In other words, this is valid:
    ```
    @batch
    @step
    def foo(self):
        pass
    ```
    
    whereas this is not:
    ```
    @step
    @batch
    def foo(self):
        pass
    ```
    
    Parameters
    ----------
    f : Union[Callable[[FlowSpecDerived], None], Callable[[FlowSpecDerived, Any], None]]
        Function to make into a Metaflow Step
    
    Returns
    -------
    Union[Callable[[FlowSpecDerived, StepFlag], None], Callable[[FlowSpecDerived, Any, StepFlag], None]]
        Function that is a Metaflow Step
    """
    ...

@typing.overload
def step(f: typing.Callable[[FlowSpecDerived, typing.Any], None]) -> typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]:
    ...

def step(f: typing.Union[typing.Callable[[FlowSpecDerived], None], typing.Callable[[FlowSpecDerived, typing.Any], None]]):
    """
    Marks a method in a FlowSpec as a Metaflow Step. Note that this
    decorator needs to be placed as close to the method as possible (ie:
    before other decorators).
    
    In other words, this is valid:
    ```
    @batch
    @step
    def foo(self):
        pass
    ```
    
    whereas this is not:
    ```
    @step
    @batch
    def foo(self):
        pass
    ```
    
    Parameters
    ----------
    f : Union[Callable[[FlowSpecDerived], None], Callable[[FlowSpecDerived, Any], None]]
        Function to make into a Metaflow Step
    
    Returns
    -------
    Union[Callable[[FlowSpecDerived, StepFlag], None], Callable[[FlowSpecDerived, Any, StepFlag], None]]
        Function that is a Metaflow Step
    """
    ...

@typing.overload
def model(*, load: typing.Union[typing.List[str], str, typing.List[typing.Tuple[str, typing.Optional[str]]]] = None, temp_dir_root: str = None) -> typing.Callable[[typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]], typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]]:
    """
    Enables loading / saving of models within a step.
    
    
    Parameters
    ----------
    load : Union[List[str],str,List[Tuple[str,Union[str,None]]]], default: None
        Artifact name/s referencing the models/checkpoints to load. Artifact names refer to the names of the instance variables set to `self`.
        These artifact names give to `load` be reference objects or reference `key` string's from objects created by:
        - `current.checkpoint`
        - `current.model`
        - `current.huggingface_hub`
    
        If a list of tuples is provided, the first element is the artifact name and the second element is the path the artifact needs be unpacked on
        the local filesystem. If the second element is None, the artifact will be unpacked in the current working directory.
        If a string is provided, then the artifact corresponding to that name will be loaded in the current working directory.
    
    temp_dir_root : str, default: None
        The root directory under which `current.model.loaded` will store loaded models
    
    
    
    """
    ...

@typing.overload
def model(f: typing.Callable[[FlowSpecDerived, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, StepFlag], None]:
    ...

@typing.overload
def model(f: typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]:
    ...

def model(f: typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None], None] = None, *, load: typing.Union[typing.List[str], str, typing.List[typing.Tuple[str, typing.Optional[str]]]] = None, temp_dir_root: str = None):
    """
    Enables loading / saving of models within a step.
    
    
    Parameters
    ----------
    load : Union[List[str],str,List[Tuple[str,Union[str,None]]]], default: None
        Artifact name/s referencing the models/checkpoints to load. Artifact names refer to the names of the instance variables set to `self`.
        These artifact names give to `load` be reference objects or reference `key` string's from objects created by:
        - `current.checkpoint`
        - `current.model`
        - `current.huggingface_hub`
    
        If a list of tuples is provided, the first element is the artifact name and the second element is the path the artifact needs be unpacked on
        the local filesystem. If the second element is None, the artifact will be unpacked in the current working directory.
        If a string is provided, then the artifact corresponding to that name will be loaded in the current working directory.
    
    temp_dir_root : str, default: None
        The root directory under which `current.model.loaded` will store loaded models
    
    
    
    """
    ...

@typing.overload
def timeout(*, seconds: int = 0, minutes: int = 0, hours: int = 0) -> typing.Callable[[typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]], typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]]:
    """
    Specifies a timeout for your step.
    
    This decorator is useful if this step may hang indefinitely.
    
    This can be used in conjunction with the `@retry` decorator as well as the `@catch` decorator.
    A timeout is considered to be an exception thrown by the step. It will cause the step to be
    retried if needed and the exception will be caught by the `@catch` decorator, if present.
    
    Note that all the values specified in parameters are added together so if you specify
    60 seconds and 1 hour, the decorator will have an effective timeout of 1 hour and 1 minute.
    
    Parameters
    ----------
    seconds : int, default 0
        Number of seconds to wait prior to timing out.
    minutes : int, default 0
        Number of minutes to wait prior to timing out.
    hours : int, default 0
        Number of hours to wait prior to timing out.
    """
    ...

@typing.overload
def timeout(f: typing.Callable[[FlowSpecDerived, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, StepFlag], None]:
    ...

@typing.overload
def timeout(f: typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]:
    ...

def timeout(f: typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None], None] = None, *, seconds: int = 0, minutes: int = 0, hours: int = 0):
    """
    Specifies a timeout for your step.
    
    This decorator is useful if this step may hang indefinitely.
    
    This can be used in conjunction with the `@retry` decorator as well as the `@catch` decorator.
    A timeout is considered to be an exception thrown by the step. It will cause the step to be
    retried if needed and the exception will be caught by the `@catch` decorator, if present.
    
    Note that all the values specified in parameters are added together so if you specify
    60 seconds and 1 hour, the decorator will have an effective timeout of 1 hour and 1 minute.
    
    Parameters
    ----------
    seconds : int, default 0
        Number of seconds to wait prior to timing out.
    minutes : int, default 0
        Number of minutes to wait prior to timing out.
    hours : int, default 0
        Number of hours to wait prior to timing out.
    """
    ...

@typing.overload
def secrets(*, sources: typing.List[typing.Union[str, typing.Dict[str, typing.Any]]] = []) -> typing.Callable[[typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]], typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]]:
    """
    Specifies secrets to be retrieved and injected as environment variables prior to
    the execution of a step.
    
    Parameters
    ----------
    sources : List[Union[str, Dict[str, Any]]], default: []
        List of secret specs, defining how the secrets are to be retrieved
    """
    ...

@typing.overload
def secrets(f: typing.Callable[[FlowSpecDerived, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, StepFlag], None]:
    ...

@typing.overload
def secrets(f: typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]:
    ...

def secrets(f: typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None], None] = None, *, sources: typing.List[typing.Union[str, typing.Dict[str, typing.Any]]] = []):
    """
    Specifies secrets to be retrieved and injected as environment variables prior to
    the execution of a step.
    
    Parameters
    ----------
    sources : List[Union[str, Dict[str, Any]]], default: []
        List of secret specs, defining how the secrets are to be retrieved
    """
    ...

@typing.overload
def card(*, type: str = "default", id: typing.Optional[str] = None, options: typing.Dict[str, typing.Any] = {}, timeout: int = 45) -> typing.Callable[[typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]], typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]]:
    """
    Creates a human-readable report, a Metaflow Card, after this step completes.
    
    Note that you may add multiple `@card` decorators in a step with different parameters.
    
    Parameters
    ----------
    type : str, default 'default'
        Card type.
    id : str, optional, default None
        If multiple cards are present, use this id to identify this card.
    options : Dict[str, Any], default {}
        Options passed to the card. The contents depend on the card type.
    timeout : int, default 45
        Interrupt reporting if it takes more than this many seconds.
    
    
    """
    ...

@typing.overload
def card(f: typing.Callable[[FlowSpecDerived, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, StepFlag], None]:
    ...

@typing.overload
def card(f: typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]:
    ...

def card(f: typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None], None] = None, *, type: str = "default", id: typing.Optional[str] = None, options: typing.Dict[str, typing.Any] = {}, timeout: int = 45):
    """
    Creates a human-readable report, a Metaflow Card, after this step completes.
    
    Note that you may add multiple `@card` decorators in a step with different parameters.
    
    Parameters
    ----------
    type : str, default 'default'
        Card type.
    id : str, optional, default None
        If multiple cards are present, use this id to identify this card.
    options : Dict[str, Any], default {}
        Options passed to the card. The contents depend on the card type.
    timeout : int, default 45
        Interrupt reporting if it takes more than this many seconds.
    
    
    """
    ...

@typing.overload
def retry(*, times: int = 3, minutes_between_retries: int = 2) -> typing.Callable[[typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]], typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]]:
    """
    Specifies the number of times the task corresponding
    to a step needs to be retried.
    
    This decorator is useful for handling transient errors, such as networking issues.
    If your task contains operations that can't be retried safely, e.g. database updates,
    it is advisable to annotate it with `@retry(times=0)`.
    
    This can be used in conjunction with the `@catch` decorator. The `@catch`
    decorator will execute a no-op task after all retries have been exhausted,
    ensuring that the flow execution can continue.
    
    Parameters
    ----------
    times : int, default 3
        Number of times to retry this task.
    minutes_between_retries : int, default 2
        Number of minutes between retries.
    """
    ...

@typing.overload
def retry(f: typing.Callable[[FlowSpecDerived, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, StepFlag], None]:
    ...

@typing.overload
def retry(f: typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]:
    ...

def retry(f: typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None], None] = None, *, times: int = 3, minutes_between_retries: int = 2):
    """
    Specifies the number of times the task corresponding
    to a step needs to be retried.
    
    This decorator is useful for handling transient errors, such as networking issues.
    If your task contains operations that can't be retried safely, e.g. database updates,
    it is advisable to annotate it with `@retry(times=0)`.
    
    This can be used in conjunction with the `@catch` decorator. The `@catch`
    decorator will execute a no-op task after all retries have been exhausted,
    ensuring that the flow execution can continue.
    
    Parameters
    ----------
    times : int, default 3
        Number of times to retry this task.
    minutes_between_retries : int, default 2
        Number of minutes between retries.
    """
    ...

@typing.overload
def parallel(f: typing.Callable[[FlowSpecDerived, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, StepFlag], None]:
    """
    Decorator prototype for all step decorators. This function gets specialized
    and imported for all decorators types by _import_plugin_decorators().
    """
    ...

@typing.overload
def parallel(f: typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]:
    ...

def parallel(f: typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None], None] = None):
    """
    Decorator prototype for all step decorators. This function gets specialized
    and imported for all decorators types by _import_plugin_decorators().
    """
    ...

@typing.overload
def fast_bakery_internal(f: typing.Callable[[FlowSpecDerived, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, StepFlag], None]:
    """
    Internal decorator to support Fast bakery
    """
    ...

@typing.overload
def fast_bakery_internal(f: typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]:
    ...

def fast_bakery_internal(f: typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None], None] = None):
    """
    Internal decorator to support Fast bakery
    """
    ...

@typing.overload
def checkpoint(*, load_policy: str = "fresh", temp_dir_root: str = None) -> typing.Callable[[typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]], typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]]:
    """
    Enables checkpointing for a step.
    
    
    Parameters
    ----------
    load_policy : str, default: "fresh"
        The policy for loading the checkpoint. The following policies are supported:
            - "eager": Loads the the latest available checkpoint within the namespace.
            With this mode, the latest checkpoint written by any previous task (can be even a different run) of the step
            will be loaded at the start of the task.
            - "none": Do not load any checkpoint
            - "fresh": Loads the lastest checkpoint created within the running Task.
            This mode helps loading checkpoints across various retry attempts of the same task.
            With this mode, no checkpoint will be loaded at the start of a task but any checkpoints
            created within the task will be loaded when the task is retries execution on failure.
    
    temp_dir_root : str, default: None
        The root directory under which `current.checkpoint.directory` will be created.
    
    
    
    """
    ...

@typing.overload
def checkpoint(f: typing.Callable[[FlowSpecDerived, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, StepFlag], None]:
    ...

@typing.overload
def checkpoint(f: typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]:
    ...

def checkpoint(f: typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None], None] = None, *, load_policy: str = "fresh", temp_dir_root: str = None):
    """
    Enables checkpointing for a step.
    
    
    Parameters
    ----------
    load_policy : str, default: "fresh"
        The policy for loading the checkpoint. The following policies are supported:
            - "eager": Loads the the latest available checkpoint within the namespace.
            With this mode, the latest checkpoint written by any previous task (can be even a different run) of the step
            will be loaded at the start of the task.
            - "none": Do not load any checkpoint
            - "fresh": Loads the lastest checkpoint created within the running Task.
            This mode helps loading checkpoints across various retry attempts of the same task.
            With this mode, no checkpoint will be loaded at the start of a task but any checkpoints
            created within the task will be loaded when the task is retries execution on failure.
    
    temp_dir_root : str, default: None
        The root directory under which `current.checkpoint.directory` will be created.
    
    
    
    """
    ...

@typing.overload
def conda(*, packages: typing.Dict[str, str] = {}, libraries: typing.Dict[str, str] = {}, python: typing.Optional[str] = None, disabled: bool = False) -> typing.Callable[[typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]], typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]]:
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
    ...

@typing.overload
def conda(f: typing.Callable[[FlowSpecDerived, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, StepFlag], None]:
    ...

@typing.overload
def conda(f: typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]:
    ...

def conda(f: typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None], None] = None, *, packages: typing.Dict[str, str] = {}, libraries: typing.Dict[str, str] = {}, python: typing.Optional[str] = None, disabled: bool = False):
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
    ...

def huggingface_hub(*, temp_dir_root: typing.Optional[str] = None, load: typing.Union[typing.List[str], typing.List[typing.Tuple[typing.Dict, str]], typing.List[typing.Tuple[str, str]], typing.List[typing.Dict], None]) -> typing.Callable[[typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]], typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]]:
    """
    Decorator that helps cache, version and store models/datasets from huggingface hub.
    
    Parameters
    ----------
    temp_dir_root : str, optional
        The root directory that will hold the temporary directory where objects will be downloaded.
    
    load: Union[List[str], List[Tuple[Dict, str]], List[Tuple[str, str]], List[Dict], None]
        The list of models to load.
    
    
    """
    ...

@typing.overload
def resources(*, cpu: int = 1, gpu: typing.Optional[int] = None, disk: typing.Optional[int] = None, memory: int = 4096, shared_memory: typing.Optional[int] = None) -> typing.Callable[[typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]], typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]]:
    """
    Specifies the resources needed when executing this step.
    
    Use `@resources` to specify the resource requirements
    independently of the specific compute layer (`@batch`, `@kubernetes`).
    
    You can choose the compute layer on the command line by executing e.g.
    ```
    python myflow.py run --with batch
    ```
    or
    ```
    python myflow.py run --with kubernetes
    ```
    which executes the flow on the desired system using the
    requirements specified in `@resources`.
    
    Parameters
    ----------
    cpu : int, default 1
        Number of CPUs required for this step.
    gpu : int, optional, default None
        Number of GPUs required for this step.
    disk : int, optional, default None
        Disk size (in MB) required for this step. Only applies on Kubernetes.
    memory : int, default 4096
        Memory size (in MB) required for this step.
    shared_memory : int, optional, default None
        The value for the size (in MiB) of the /dev/shm volume for this step.
        This parameter maps to the `--shm-size` option in Docker.
    """
    ...

@typing.overload
def resources(f: typing.Callable[[FlowSpecDerived, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, StepFlag], None]:
    ...

@typing.overload
def resources(f: typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]:
    ...

def resources(f: typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None], None] = None, *, cpu: int = 1, gpu: typing.Optional[int] = None, disk: typing.Optional[int] = None, memory: int = 4096, shared_memory: typing.Optional[int] = None):
    """
    Specifies the resources needed when executing this step.
    
    Use `@resources` to specify the resource requirements
    independently of the specific compute layer (`@batch`, `@kubernetes`).
    
    You can choose the compute layer on the command line by executing e.g.
    ```
    python myflow.py run --with batch
    ```
    or
    ```
    python myflow.py run --with kubernetes
    ```
    which executes the flow on the desired system using the
    requirements specified in `@resources`.
    
    Parameters
    ----------
    cpu : int, default 1
        Number of CPUs required for this step.
    gpu : int, optional, default None
        Number of GPUs required for this step.
    disk : int, optional, default None
        Disk size (in MB) required for this step. Only applies on Kubernetes.
    memory : int, default 4096
        Memory size (in MB) required for this step.
    shared_memory : int, optional, default None
        The value for the size (in MiB) of the /dev/shm volume for this step.
        This parameter maps to the `--shm-size` option in Docker.
    """
    ...

@typing.overload
def environment(*, vars: typing.Dict[str, str] = {}) -> typing.Callable[[typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]], typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]]:
    """
    Specifies environment variables to be set prior to the execution of a step.
    
    Parameters
    ----------
    vars : Dict[str, str], default {}
        Dictionary of environment variables to set.
    """
    ...

@typing.overload
def environment(f: typing.Callable[[FlowSpecDerived, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, StepFlag], None]:
    ...

@typing.overload
def environment(f: typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]:
    ...

def environment(f: typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None], None] = None, *, vars: typing.Dict[str, str] = {}):
    """
    Specifies environment variables to be set prior to the execution of a step.
    
    Parameters
    ----------
    vars : Dict[str, str], default {}
        Dictionary of environment variables to set.
    """
    ...

def kubernetes(*, cpu: int = 1, memory: int = 4096, disk: int = 10240, image: typing.Optional[str] = None, image_pull_policy: str = "KUBERNETES_IMAGE_PULL_POLICY", service_account: str = "METAFLOW_KUBERNETES_SERVICE_ACCOUNT", secrets: typing.Optional[typing.List[str]] = None, node_selector: typing.Union[typing.Dict[str, str], str, None] = None, namespace: str = "METAFLOW_KUBERNETES_NAMESPACE", gpu: typing.Optional[int] = None, gpu_vendor: str = "KUBERNETES_GPU_VENDOR", tolerations: typing.List[str] = [], use_tmpfs: bool = False, tmpfs_tempdir: bool = True, tmpfs_size: typing.Optional[int] = None, tmpfs_path: typing.Optional[str] = "/metaflow_temp", persistent_volume_claims: typing.Optional[typing.Dict[str, str]] = None, shared_memory: typing.Optional[int] = None, port: typing.Optional[int] = None, compute_pool: typing.Optional[str] = None, hostname_resolution_timeout: int = 600) -> typing.Callable[[typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]], typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]]:
    """
    Specifies that this step should execute on Kubernetes.
    
    Parameters
    ----------
    cpu : int, default 1
        Number of CPUs required for this step. If `@resources` is
        also present, the maximum value from all decorators is used.
    memory : int, default 4096
        Memory size (in MB) required for this step. If
        `@resources` is also present, the maximum value from all decorators is
        used.
    disk : int, default 10240
        Disk size (in MB) required for this step. If
        `@resources` is also present, the maximum value from all decorators is
        used.
    image : str, optional, default None
        Docker image to use when launching on Kubernetes. If not specified, and
        METAFLOW_KUBERNETES_CONTAINER_IMAGE is specified, that image is used. If
        not, a default Docker image mapping to the current version of Python is used.
    image_pull_policy: str, default KUBERNETES_IMAGE_PULL_POLICY
        If given, the imagePullPolicy to be applied to the Docker image of the step.
    service_account : str, default METAFLOW_KUBERNETES_SERVICE_ACCOUNT
        Kubernetes service account to use when launching pod in Kubernetes.
    secrets : List[str], optional, default None
        Kubernetes secrets to use when launching pod in Kubernetes. These
        secrets are in addition to the ones defined in `METAFLOW_KUBERNETES_SECRETS`
        in Metaflow configuration.
    node_selector: Union[Dict[str,str], str], optional, default None
        Kubernetes node selector(s) to apply to the pod running the task.
        Can be passed in as a comma separated string of values e.g. "kubernetes.io/os=linux,kubernetes.io/arch=amd64"
        or as a dictionary {"kubernetes.io/os": "linux", "kubernetes.io/arch": "amd64"}
    namespace : str, default METAFLOW_KUBERNETES_NAMESPACE
        Kubernetes namespace to use when launching pod in Kubernetes.
    gpu : int, optional, default None
        Number of GPUs required for this step. A value of zero implies that
        the scheduled node should not have GPUs.
    gpu_vendor : str, default KUBERNETES_GPU_VENDOR
        The vendor of the GPUs to be used for this step.
    tolerations : List[str], default []
        The default is extracted from METAFLOW_KUBERNETES_TOLERATIONS.
        Kubernetes tolerations to use when launching pod in Kubernetes.
    use_tmpfs : bool, default False
        This enables an explicit tmpfs mount for this step.
    tmpfs_tempdir : bool, default True
        sets METAFLOW_TEMPDIR to tmpfs_path if set for this step.
    tmpfs_size : int, optional, default: None
        The value for the size (in MiB) of the tmpfs mount for this step.
        This parameter maps to the `--tmpfs` option in Docker. Defaults to 50% of the
        memory allocated for this step.
    tmpfs_path : str, optional, default /metaflow_temp
        Path to tmpfs mount for this step.
    persistent_volume_claims : Dict[str, str], optional, default None
        A map (dictionary) of persistent volumes to be mounted to the pod for this step. The map is from persistent
        volumes to the path to which the volume is to be mounted, e.g., `{'pvc-name': '/path/to/mount/on'}`.
    shared_memory: int, optional
        Shared memory size (in MiB) required for this step
    port: int, optional
        Port number to specify in the Kubernetes job object
    compute_pool : str, optional, default None
        Compute pool to be used for for this step.
        If not specified, any accessible compute pool within the perimeter is used.
    hostname_resolution_timeout: int, default 10 * 60
        Timeout in seconds for the workers tasks in the gang scheduled cluster to resolve the hostname of control task.
        Only applicable when @parallel is used.
    """
    ...

@typing.overload
def catch(*, var: typing.Optional[str] = None, print_exception: bool = True) -> typing.Callable[[typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]], typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]]:
    """
    Specifies that the step will success under all circumstances.
    
    The decorator will create an optional artifact, specified by `var`, which
    contains the exception raised. You can use it to detect the presence
    of errors, indicating that all happy-path artifacts produced by the step
    are missing.
    
    Parameters
    ----------
    var : str, optional, default None
        Name of the artifact in which to store the caught exception.
        If not specified, the exception is not stored.
    print_exception : bool, default True
        Determines whether or not the exception is printed to
        stdout when caught.
    """
    ...

@typing.overload
def catch(f: typing.Callable[[FlowSpecDerived, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, StepFlag], None]:
    ...

@typing.overload
def catch(f: typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]:
    ...

def catch(f: typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None], None] = None, *, var: typing.Optional[str] = None, print_exception: bool = True):
    """
    Specifies that the step will success under all circumstances.
    
    The decorator will create an optional artifact, specified by `var`, which
    contains the exception raised. You can use it to detect the presence
    of errors, indicating that all happy-path artifacts produced by the step
    are missing.
    
    Parameters
    ----------
    var : str, optional, default None
        Name of the artifact in which to store the caught exception.
        If not specified, the exception is not stored.
    print_exception : bool, default True
        Determines whether or not the exception is printed to
        stdout when caught.
    """
    ...

@typing.overload
def pypi(*, packages: typing.Dict[str, str] = {}, python: typing.Optional[str] = None) -> typing.Callable[[typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]], typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]]:
    """
    Specifies the PyPI packages for the step.
    
    Information in this decorator will augment any
    attributes set in the `@pyi_base` flow-level decorator. Hence,
    you can use `@pypi_base` to set packages required by all
    steps and use `@pypi` to specify step-specific overrides.
    
    Parameters
    ----------
    packages : Dict[str, str], default: {}
        Packages to use for this step. The key is the name of the package
        and the value is the version to use.
    python : str, optional, default: None
        Version of Python to use, e.g. '3.7.4'. A default value of None implies
        that the version used will correspond to the version of the Python interpreter used to start the run.
    """
    ...

@typing.overload
def pypi(f: typing.Callable[[FlowSpecDerived, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, StepFlag], None]:
    ...

@typing.overload
def pypi(f: typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]:
    ...

def pypi(f: typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None], None] = None, *, packages: typing.Dict[str, str] = {}, python: typing.Optional[str] = None):
    """
    Specifies the PyPI packages for the step.
    
    Information in this decorator will augment any
    attributes set in the `@pyi_base` flow-level decorator. Hence,
    you can use `@pypi_base` to set packages required by all
    steps and use `@pypi` to specify step-specific overrides.
    
    Parameters
    ----------
    packages : Dict[str, str], default: {}
        Packages to use for this step. The key is the name of the package
        and the value is the version to use.
    python : str, optional, default: None
        Version of Python to use, e.g. '3.7.4'. A default value of None implies
        that the version used will correspond to the version of the Python interpreter used to start the run.
    """
    ...

@typing.overload
def trigger_on_finish(*, flow: typing.Union[typing.Dict[str, str], str, None] = None, flows: typing.List[typing.Union[str, typing.Dict[str, str]]] = [], options: typing.Dict[str, typing.Any] = {}) -> typing.Callable[[typing.Type[FlowSpecDerived]], typing.Type[FlowSpecDerived]]:
    """
    Specifies the flow(s) that this flow depends on.
    
    ```
    @trigger_on_finish(flow='FooFlow')
    ```
    or
    ```
    @trigger_on_finish(flows=['FooFlow', 'BarFlow'])
    ```
    This decorator respects the @project decorator and triggers the flow
    when upstream runs within the same namespace complete successfully
    
    Additionally, you can specify project aware upstream flow dependencies
    by specifying the fully qualified project_flow_name.
    ```
    @trigger_on_finish(flow='my_project.branch.my_branch.FooFlow')
    ```
    or
    ```
    @trigger_on_finish(flows=['my_project.branch.my_branch.FooFlow', 'BarFlow'])
    ```
    
    You can also specify just the project or project branch (other values will be
    inferred from the current project or project branch):
    ```
    @trigger_on_finish(flow={"name": "FooFlow", "project": "my_project", "project_branch": "branch"})
    ```
    
    Note that `branch` is typically one of:
      - `prod`
      - `user.bob`
      - `test.my_experiment`
      - `prod.staging`
    
    Parameters
    ----------
    flow : Union[str, Dict[str, str]], optional, default None
        Upstream flow dependency for this flow.
    flows : List[Union[str, Dict[str, str]]], default []
        Upstream flow dependencies for this flow.
    options : Dict[str, Any], default {}
        Backend-specific configuration for tuning eventing behavior.
    
    
    """
    ...

@typing.overload
def trigger_on_finish(f: typing.Type[FlowSpecDerived]) -> typing.Type[FlowSpecDerived]:
    ...

def trigger_on_finish(f: typing.Optional[typing.Type[FlowSpecDerived]] = None, *, flow: typing.Union[typing.Dict[str, str], str, None] = None, flows: typing.List[typing.Union[str, typing.Dict[str, str]]] = [], options: typing.Dict[str, typing.Any] = {}):
    """
    Specifies the flow(s) that this flow depends on.
    
    ```
    @trigger_on_finish(flow='FooFlow')
    ```
    or
    ```
    @trigger_on_finish(flows=['FooFlow', 'BarFlow'])
    ```
    This decorator respects the @project decorator and triggers the flow
    when upstream runs within the same namespace complete successfully
    
    Additionally, you can specify project aware upstream flow dependencies
    by specifying the fully qualified project_flow_name.
    ```
    @trigger_on_finish(flow='my_project.branch.my_branch.FooFlow')
    ```
    or
    ```
    @trigger_on_finish(flows=['my_project.branch.my_branch.FooFlow', 'BarFlow'])
    ```
    
    You can also specify just the project or project branch (other values will be
    inferred from the current project or project branch):
    ```
    @trigger_on_finish(flow={"name": "FooFlow", "project": "my_project", "project_branch": "branch"})
    ```
    
    Note that `branch` is typically one of:
      - `prod`
      - `user.bob`
      - `test.my_experiment`
      - `prod.staging`
    
    Parameters
    ----------
    flow : Union[str, Dict[str, str]], optional, default None
        Upstream flow dependency for this flow.
    flows : List[Union[str, Dict[str, str]]], default []
        Upstream flow dependencies for this flow.
    options : Dict[str, Any], default {}
        Backend-specific configuration for tuning eventing behavior.
    
    
    """
    ...

@typing.overload
def trigger(*, event: typing.Union[str, typing.Dict[str, typing.Any], None] = None, events: typing.List[typing.Union[str, typing.Dict[str, typing.Any]]] = [], options: typing.Dict[str, typing.Any] = {}) -> typing.Callable[[typing.Type[FlowSpecDerived]], typing.Type[FlowSpecDerived]]:
    """
    Specifies the event(s) that this flow depends on.
    
    ```
    @trigger(event='foo')
    ```
    or
    ```
    @trigger(events=['foo', 'bar'])
    ```
    
    Additionally, you can specify the parameter mappings
    to map event payload to Metaflow parameters for the flow.
    ```
    @trigger(event={'name':'foo', 'parameters':{'flow_param': 'event_field'}})
    ```
    or
    ```
    @trigger(events=[{'name':'foo', 'parameters':{'flow_param_1': 'event_field_1'},
                     {'name':'bar', 'parameters':{'flow_param_2': 'event_field_2'}])
    ```
    
    'parameters' can also be a list of strings and tuples like so:
    ```
    @trigger(event={'name':'foo', 'parameters':['common_name', ('flow_param', 'event_field')]})
    ```
    This is equivalent to:
    ```
    @trigger(event={'name':'foo', 'parameters':{'common_name': 'common_name', 'flow_param': 'event_field'}})
    ```
    
    Parameters
    ----------
    event : Union[str, Dict[str, Any]], optional, default None
        Event dependency for this flow.
    events : List[Union[str, Dict[str, Any]]], default []
        Events dependency for this flow.
    options : Dict[str, Any], default {}
        Backend-specific configuration for tuning eventing behavior.
    
    
    """
    ...

@typing.overload
def trigger(f: typing.Type[FlowSpecDerived]) -> typing.Type[FlowSpecDerived]:
    ...

def trigger(f: typing.Optional[typing.Type[FlowSpecDerived]] = None, *, event: typing.Union[str, typing.Dict[str, typing.Any], None] = None, events: typing.List[typing.Union[str, typing.Dict[str, typing.Any]]] = [], options: typing.Dict[str, typing.Any] = {}):
    """
    Specifies the event(s) that this flow depends on.
    
    ```
    @trigger(event='foo')
    ```
    or
    ```
    @trigger(events=['foo', 'bar'])
    ```
    
    Additionally, you can specify the parameter mappings
    to map event payload to Metaflow parameters for the flow.
    ```
    @trigger(event={'name':'foo', 'parameters':{'flow_param': 'event_field'}})
    ```
    or
    ```
    @trigger(events=[{'name':'foo', 'parameters':{'flow_param_1': 'event_field_1'},
                     {'name':'bar', 'parameters':{'flow_param_2': 'event_field_2'}])
    ```
    
    'parameters' can also be a list of strings and tuples like so:
    ```
    @trigger(event={'name':'foo', 'parameters':['common_name', ('flow_param', 'event_field')]})
    ```
    This is equivalent to:
    ```
    @trigger(event={'name':'foo', 'parameters':{'common_name': 'common_name', 'flow_param': 'event_field'}})
    ```
    
    Parameters
    ----------
    event : Union[str, Dict[str, Any]], optional, default None
        Event dependency for this flow.
    events : List[Union[str, Dict[str, Any]]], default []
        Events dependency for this flow.
    options : Dict[str, Any], default {}
        Backend-specific configuration for tuning eventing behavior.
    
    
    """
    ...

def airflow_s3_key_sensor(*, timeout: int, poke_interval: int, mode: str, exponential_backoff: bool, pool: str, soft_fail: bool, name: str, description: str, bucket_key: typing.Union[str, typing.List[str]], bucket_name: str, wildcard_match: bool, aws_conn_id: str, verify: bool) -> typing.Callable[[typing.Type[FlowSpecDerived]], typing.Type[FlowSpecDerived]]:
    """
    The `@airflow_s3_key_sensor` decorator attaches a Airflow [S3KeySensor](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/_api/airflow/providers/amazon/aws/sensors/s3/index.html#airflow.providers.amazon.aws.sensors.s3.S3KeySensor)
    before the start step of the flow. This decorator only works when a flow is scheduled on Airflow
    and is compiled using `airflow create`. More than one `@airflow_s3_key_sensor` can be
    added as a flow decorators. Adding more than one decorator will ensure that `start` step
    starts only after all sensors finish.
    
    Parameters
    ----------
    timeout : int
        Time, in seconds before the task times out and fails. (Default: 3600)
    poke_interval : int
        Time in seconds that the job should wait in between each try. (Default: 60)
    mode : str
        How the sensor operates. Options are: { poke | reschedule }. (Default: "poke")
    exponential_backoff : bool
        allow progressive longer waits between pokes by using exponential backoff algorithm. (Default: True)
    pool : str
        the slot pool this task should run in,
        slot pools are a way to limit concurrency for certain tasks. (Default:None)
    soft_fail : bool
        Set to true to mark the task as SKIPPED on failure. (Default: False)
    name : str
        Name of the sensor on Airflow
    description : str
        Description of sensor in the Airflow UI
    bucket_key : Union[str, List[str]]
        The key(s) being waited on. Supports full s3:// style url or relative path from root level.
        When it's specified as a full s3:// url, please leave `bucket_name` as None
    bucket_name : str
        Name of the S3 bucket. Only needed when bucket_key is not provided as a full s3:// url.
        When specified, all the keys passed to bucket_key refers to this bucket. (Default:None)
    wildcard_match : bool
        whether the bucket_key should be interpreted as a Unix wildcard pattern. (Default: False)
    aws_conn_id : str
        a reference to the s3 connection on Airflow. (Default: None)
    verify : bool
        Whether or not to verify SSL certificates for S3 connection. (Default: None)
    """
    ...

def nim(*, models: "list[NIM]", backend: str) -> typing.Callable[[typing.Type[FlowSpecDerived]], typing.Type[FlowSpecDerived]]:
    """
    This decorator is used to run NIM containers in Metaflow tasks as sidecars.
    
    User code call
    -----------
    @nim(
        models=['meta/llama3-8b-instruct', 'meta/llama3-70b-instruct'],
        backend='managed'
    )
    
    Valid backend options
    ---------------------
    - 'managed': Outerbounds selects a compute provider based on the model.
    - 🚧 'dataplane': Run in your account.
    
    Valid model options
    ----------------
        - 'meta/llama3-8b-instruct': 8B parameter model
        - 'meta/llama3-70b-instruct': 70B parameter model
        - Upon request, any model here: https://nvcf.ngc.nvidia.com/functions?filter=nvidia-functions
    
    Parameters
    ----------
    models: list[NIM]
        List of NIM containers running models in sidecars.
    backend: str
        Compute provider to run the NIM container.
    """
    ...

@typing.overload
def conda_base(*, packages: typing.Dict[str, str] = {}, libraries: typing.Dict[str, str] = {}, python: typing.Optional[str] = None, disabled: bool = False) -> typing.Callable[[typing.Type[FlowSpecDerived]], typing.Type[FlowSpecDerived]]:
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
    ...

@typing.overload
def conda_base(f: typing.Type[FlowSpecDerived]) -> typing.Type[FlowSpecDerived]:
    ...

def conda_base(f: typing.Optional[typing.Type[FlowSpecDerived]] = None, *, packages: typing.Dict[str, str] = {}, libraries: typing.Dict[str, str] = {}, python: typing.Optional[str] = None, disabled: bool = False):
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
    ...

def airflow_external_task_sensor(*, timeout: int, poke_interval: int, mode: str, exponential_backoff: bool, pool: str, soft_fail: bool, name: str, description: str, external_dag_id: str, external_task_ids: typing.List[str], allowed_states: typing.List[str], failed_states: typing.List[str], execution_delta: "datetime.timedelta", check_existence: bool) -> typing.Callable[[typing.Type[FlowSpecDerived]], typing.Type[FlowSpecDerived]]:
    """
    The `@airflow_external_task_sensor` decorator attaches a Airflow [ExternalTaskSensor](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/sensors/external_task/index.html#airflow.sensors.external_task.ExternalTaskSensor) before the start step of the flow.
    This decorator only works when a flow is scheduled on Airflow and is compiled using `airflow create`. More than one `@airflow_external_task_sensor` can be added as a flow decorators. Adding more than one decorator will ensure that `start` step starts only after all sensors finish.
    
    Parameters
    ----------
    timeout : int
        Time, in seconds before the task times out and fails. (Default: 3600)
    poke_interval : int
        Time in seconds that the job should wait in between each try. (Default: 60)
    mode : str
        How the sensor operates. Options are: { poke | reschedule }. (Default: "poke")
    exponential_backoff : bool
        allow progressive longer waits between pokes by using exponential backoff algorithm. (Default: True)
    pool : str
        the slot pool this task should run in,
        slot pools are a way to limit concurrency for certain tasks. (Default:None)
    soft_fail : bool
        Set to true to mark the task as SKIPPED on failure. (Default: False)
    name : str
        Name of the sensor on Airflow
    description : str
        Description of sensor in the Airflow UI
    external_dag_id : str
        The dag_id that contains the task you want to wait for.
    external_task_ids : List[str]
        The list of task_ids that you want to wait for.
        If None (default value) the sensor waits for the DAG. (Default: None)
    allowed_states : List[str]
        Iterable of allowed states, (Default: ['success'])
    failed_states : List[str]
        Iterable of failed or dis-allowed states. (Default: None)
    execution_delta : datetime.timedelta
        time difference with the previous execution to look at,
        the default is the same logical date as the current task or DAG. (Default: None)
    check_existence: bool
        Set to True to check if the external task exists or check if
        the DAG to wait for exists. (Default: True)
    """
    ...

@typing.overload
def pypi_base(*, packages: typing.Dict[str, str] = {}, python: typing.Optional[str] = None) -> typing.Callable[[typing.Type[FlowSpecDerived]], typing.Type[FlowSpecDerived]]:
    """
    Specifies the PyPI packages for all steps of the flow.
    
    Use `@pypi_base` to set common packages required by all
    steps and use `@pypi` to specify step-specific overrides.
    Parameters
    ----------
    packages : Dict[str, str], default: {}
        Packages to use for this flow. The key is the name of the package
        and the value is the version to use.
    python : str, optional, default: None
        Version of Python to use, e.g. '3.7.4'. A default value of None implies
        that the version used will correspond to the version of the Python interpreter used to start the run.
    """
    ...

@typing.overload
def pypi_base(f: typing.Type[FlowSpecDerived]) -> typing.Type[FlowSpecDerived]:
    ...

def pypi_base(f: typing.Optional[typing.Type[FlowSpecDerived]] = None, *, packages: typing.Dict[str, str] = {}, python: typing.Optional[str] = None):
    """
    Specifies the PyPI packages for all steps of the flow.
    
    Use `@pypi_base` to set common packages required by all
    steps and use `@pypi` to specify step-specific overrides.
    Parameters
    ----------
    packages : Dict[str, str], default: {}
        Packages to use for this flow. The key is the name of the package
        and the value is the version to use.
    python : str, optional, default: None
        Version of Python to use, e.g. '3.7.4'. A default value of None implies
        that the version used will correspond to the version of the Python interpreter used to start the run.
    """
    ...

@typing.overload
def schedule(*, hourly: bool = False, daily: bool = True, weekly: bool = False, cron: typing.Optional[str] = None, timezone: typing.Optional[str] = None) -> typing.Callable[[typing.Type[FlowSpecDerived]], typing.Type[FlowSpecDerived]]:
    """
    Specifies the times when the flow should be run when running on a
    production scheduler.
    
    Parameters
    ----------
    hourly : bool, default False
        Run the workflow hourly.
    daily : bool, default True
        Run the workflow daily.
    weekly : bool, default False
        Run the workflow weekly.
    cron : str, optional, default None
        Run the workflow at [a custom Cron schedule](https://docs.aws.amazon.com/eventbridge/latest/userguide/scheduled-events.html#cron-expressions)
        specified by this expression.
    timezone : str, optional, default None
        Timezone on which the schedule runs (default: None). Currently supported only for Argo workflows,
        which accepts timezones in [IANA format](https://nodatime.org/TimeZones).
    """
    ...

@typing.overload
def schedule(f: typing.Type[FlowSpecDerived]) -> typing.Type[FlowSpecDerived]:
    ...

def schedule(f: typing.Optional[typing.Type[FlowSpecDerived]] = None, *, hourly: bool = False, daily: bool = True, weekly: bool = False, cron: typing.Optional[str] = None, timezone: typing.Optional[str] = None):
    """
    Specifies the times when the flow should be run when running on a
    production scheduler.
    
    Parameters
    ----------
    hourly : bool, default False
        Run the workflow hourly.
    daily : bool, default True
        Run the workflow daily.
    weekly : bool, default False
        Run the workflow weekly.
    cron : str, optional, default None
        Run the workflow at [a custom Cron schedule](https://docs.aws.amazon.com/eventbridge/latest/userguide/scheduled-events.html#cron-expressions)
        specified by this expression.
    timezone : str, optional, default None
        Timezone on which the schedule runs (default: None). Currently supported only for Argo workflows,
        which accepts timezones in [IANA format](https://nodatime.org/TimeZones).
    """
    ...

def project(*, name: str) -> typing.Callable[[typing.Type[FlowSpecDerived]], typing.Type[FlowSpecDerived]]:
    """
    Specifies what flows belong to the same project.
    
    A project-specific namespace is created for all flows that
    use the same `@project(name)`.
    
    Parameters
    ----------
    name : str
        Project name. Make sure that the name is unique amongst all
        projects that use the same production scheduler. The name may
        contain only lowercase alphanumeric characters and underscores.
    
    
    """
    ...

def namespace(ns: typing.Optional[str]) -> typing.Optional[str]:
    """
    Switch namespace to the one provided.
    
    This call has a global effect. No objects outside this namespace
    will be accessible. To access all objects regardless of namespaces,
    pass None to this call.
    
    Parameters
    ----------
    ns : str, optional
        Namespace to switch to or None to ignore namespaces.
    
    Returns
    -------
    str, optional
        Namespace set (result of get_namespace()).
    """
    ...

def get_namespace() -> typing.Optional[str]:
    """
    Return the current namespace that is currently being used to filter objects.
    
    The namespace is a tag associated with all objects in Metaflow.
    
    Returns
    -------
    str, optional
        The current namespace used to filter objects.
    """
    ...

def default_namespace() -> str:
    """
    Resets the namespace used to filter objects to the default one, i.e. the one that was
    used prior to any `namespace` calls.
    
    Returns
    -------
    str
        The result of get_namespace() after the namespace has been reset.
    """
    ...

def get_metadata() -> str:
    """
    Returns the current Metadata provider.
    
    If this is not set explicitly using `metadata`, the default value is
    determined through the Metaflow configuration. You can use this call to
    check that your configuration is set up properly.
    
    If multiple configuration profiles are present, this call returns the one
    selected through the `METAFLOW_PROFILE` environment variable.
    
    Returns
    -------
    str
        Information about the Metadata provider currently selected. This information typically
        returns provider specific information (like URL for remote providers or local paths for
        local providers).
    """
    ...

def default_metadata() -> str:
    """
    Resets the Metadata provider to the default value, that is, to the value
    that was used prior to any `metadata` calls.
    
    Returns
    -------
    str
        The result of get_metadata() after resetting the provider.
    """
    ...

class Metaflow(object, metaclass=type):
    """
    Entry point to all objects in the Metaflow universe.
    
    This object can be used to list all the flows present either through the explicit property
    or by iterating over this object.
    
    Attributes
    ----------
    flows : List[Flow]
        Returns the list of all `Flow` objects known to this metadata provider. Note that only
        flows present in the current namespace will be returned. A `Flow` is present in a namespace
        if it has at least one run in the namespace.
    """
    def __init__(self, _current_metadata: typing.Optional[str] = None):
        ...
    @property
    def flows(self) -> typing.List[metaflow.client.core.Flow]:
        """
        Returns a list of all the flows present.
        
        Only flows present in the set namespace are returned. A flow is present in a namespace if
        it has at least one run that is in the namespace.
        
        Returns
        -------
        List[Flow]
            List of all flows present.
        """
        ...
    def __iter__(self) -> typing.Iterator[metaflow.client.core.Flow]:
        """
        Iterator over all flows present.
        
        Only flows present in the set namespace are returned. A flow is present in a
        namespace if it has at least one run that is in the namespace.
        
        Yields
        -------
        Flow
            A Flow present in the Metaflow universe.
        """
        ...
    def __str__(self) -> str:
        ...
    def __getitem__(self, name: str) -> metaflow.client.core.Flow:
        """
        Returns a specific flow by name.
        
        The flow will only be returned if it is present in the current namespace.
        
        Parameters
        ----------
        name : str
            Name of the Flow
        
        Returns
        -------
        Flow
            Flow with the given name.
        """
        ...
    ...

class Flow(metaflow.client.core.MetaflowObject, metaclass=type):
    """
    A Flow represents all existing flows with a certain name, in other words,
    classes derived from `FlowSpec`. A container of `Run` objects.
    
    Attributes
    ----------
    latest_run : Run
        Latest `Run` (in progress or completed, successfully or not) of this flow.
    latest_successful_run : Run
        Latest successfully completed `Run` of this flow.
    """
    def __init__(self, *args, **kwargs):
        ...
    @property
    def latest_run(self) -> typing.Optional[metaflow.client.core.Run]:
        """
        Returns the latest run (either in progress or completed) of this flow.
        
        Note that an in-progress run may be returned by this call. Use latest_successful_run
        to get an object representing a completed successful run.
        
        Returns
        -------
        Run, optional
            Latest run of this flow
        """
        ...
    @property
    def latest_successful_run(self) -> typing.Optional[metaflow.client.core.Run]:
        """
        Returns the latest successful run of this flow.
        
        Returns
        -------
        Run, optional
            Latest successful run of this flow
        """
        ...
    def runs(self, *tags: str) -> typing.Iterator[metaflow.client.core.Run]:
        """
        Returns an iterator over all `Run`s of this flow.
        
        An optional filter is available that allows you to filter on tags.
        If multiple tags are specified, only runs that have all the
        specified tags are returned.
        
        Parameters
        ----------
        tags : str
            Tags to match.
        
        Yields
        ------
        Run
            `Run` objects in this flow.
        """
        ...
    def __iter__(self) -> typing.Iterator[metaflow.client.core.Task]:
        """
        Iterate over all children Run of this Flow.
        
        Note that only runs in the current namespace are returned unless
        _namespace_check is False
        
        Yields
        ------
        Run
            A Run in this Flow
        """
        ...
    def __getitem__(self, run_id: str) -> metaflow.client.core.Run:
        """
        Returns the Run object with the run ID 'run_id'
        
        Parameters
        ----------
        run_id : str
            Run OD
        
        Returns
        -------
        Run
            Run for this run ID in this Flow
        
        Raises
        ------
        KeyError
            If the run_id does not identify a valid Run object
        """
        ...
    def __getstate__(self):
        ...
    def __setstate__(self, state):
        ...
    ...

class Run(metaflow.client.core.MetaflowObject, metaclass=type):
    """
    A `Run` represents an execution of a `Flow`. It is a container of `Step`s.
    
    Attributes
    ----------
    data : MetaflowData
        a shortcut to run['end'].task.data, i.e. data produced by this run.
    successful : bool
        True if the run completed successfully.
    finished : bool
        True if the run completed.
    finished_at : datetime
        Time this run finished.
    code : MetaflowCode
        Code package for this run (if present). See `MetaflowCode`.
    trigger : MetaflowTrigger
        Information about event(s) that triggered this run (if present). See `MetaflowTrigger`.
    end_task : Task
        `Task` for the end step (if it is present already).
    """
    def steps(self, *tags: str) -> typing.Iterator[metaflow.client.core.Step]:
        """
        [Legacy function - do not use]
        
        Returns an iterator over all `Step` objects in the step. This is an alias
        to iterating the object itself, i.e.
        ```
        list(Run(...)) == list(Run(...).steps())
        ```
        
        Parameters
        ----------
        tags : str
            No op (legacy functionality)
        
        Yields
        ------
        Step
            `Step` objects in this run.
        """
        ...
    @property
    def code(self) -> typing.Optional[metaflow.client.core.MetaflowCode]:
        """
        Returns the MetaflowCode object for this run, if present.
        Code is packed if atleast one `Step` runs remotely, else None is returned.
        
        Returns
        -------
        MetaflowCode, optional
            Code package for this run
        """
        ...
    @property
    def data(self) -> typing.Optional[metaflow.client.core.MetaflowData]:
        """
        Returns a container of data artifacts produced by this run.
        
        You can access data produced by this run as follows:
        ```
        print(run.data.my_var)
        ```
        This is a shorthand for `run['end'].task.data`. If the 'end' step has not yet
        executed, returns None.
        
        Returns
        -------
        MetaflowData, optional
            Container of all artifacts produced by this task
        """
        ...
    @property
    def successful(self) -> bool:
        """
        Indicates whether or not the run completed successfully.
        
        A run is successful if its 'end' step is successful.
        
        Returns
        -------
        bool
            True if the run completed successfully and False otherwise
        """
        ...
    @property
    def finished(self) -> bool:
        """
        Indicates whether or not the run completed.
        
        A run completed if its 'end' step completed.
        
        Returns
        -------
        bool
            True if the run completed and False otherwise
        """
        ...
    @property
    def finished_at(self) -> typing.Optional[datetime.datetime]:
        """
        Returns the datetime object of when the run finished (successfully or not).
        
        The completion time of a run is the same as the completion time of its 'end' step.
        If the 'end' step has not completed, returns None.
        
        Returns
        -------
        datetime, optional
            Datetime of when the run finished
        """
        ...
    @property
    def end_task(self) -> typing.Optional[metaflow.client.core.Task]:
        """
        Returns the Task corresponding to the 'end' step.
        
        This returns None if the end step does not yet exist.
        
        Returns
        -------
        Task, optional
            The 'end' task
        """
        ...
    def add_tag(self, tag: str):
        """
        Add a tag to this `Run`.
        
        Note that if the tag is already a system tag, it is not added as a user tag,
        and no error is thrown.
        
        Parameters
        ----------
        tag : str
            Tag to add.
        """
        ...
    def add_tags(self, tags: typing.Iterable[str]):
        """
        Add one or more tags to this `Run`.
        
        Note that if any tag is already a system tag, it is not added as a user tag
        and no error is thrown.
        
        Parameters
        ----------
        tags : Iterable[str]
            Tags to add.
        """
        ...
    def remove_tag(self, tag: str):
        """
        Remove one tag from this `Run`.
        
        Removing a system tag is an error. Removing a non-existent
        user tag is a no-op.
        
        Parameters
        ----------
        tag : str
            Tag to remove.
        """
        ...
    def remove_tags(self, tags: typing.Iterable[str]):
        """
        Remove one or more tags to this `Run`.
        
        Removing a system tag will result in an error. Removing a non-existent
        user tag is a no-op.
        
        Parameters
        ----------
        tags : Iterable[str]
            Tags to remove.
        """
        ...
    def replace_tag(self, tag_to_remove: str, tag_to_add: str):
        """
        Remove a tag and add a tag atomically. Removal is done first.
        The rules for `Run.add_tag` and `Run.remove_tag` also apply here.
        
        Parameters
        ----------
        tag_to_remove : str
            Tag to remove.
        tag_to_add : str
            Tag to add.
        """
        ...
    def replace_tags(self, tags_to_remove: typing.Iterable[str], tags_to_add: typing.Iterable[str]):
        """
        Remove and add tags atomically; the removal is done first.
        The rules for `Run.add_tag` and `Run.remove_tag` also apply here.
        
        Parameters
        ----------
        tags_to_remove : Iterable[str]
            Tags to remove.
        tags_to_add : Iterable[str]
            Tags to add.
        """
        ...
    def __iter__(self) -> typing.Iterator[metaflow.client.core.Step]:
        """
        Iterate over all children Step of this Run
        
        Yields
        ------
        Step
            A Step in this Run
        """
        ...
    def __getitem__(self, name: str) -> metaflow.client.core.Step:
        """
        Returns the Step object with the step name 'name'
        
        Parameters
        ----------
        name : str
            Step name
        
        Returns
        -------
        Step
            Step for this step name in this Run
        
        Raises
        ------
        KeyError
            If the name does not identify a valid Step object
        """
        ...
    def __getstate__(self):
        ...
    def __setstate__(self, state):
        ...
    @property
    def trigger(self) -> typing.Optional[metaflow.events.Trigger]:
        """
        Returns a container of events that triggered this run.
        
        This returns None if the run was not triggered by any events.
        
        Returns
        -------
        Trigger, optional
            Container of triggering events
        """
        ...
    ...

class Step(metaflow.client.core.MetaflowObject, metaclass=type):
    """
    A `Step` represents a user-defined step, that is, a method annotated with the `@step` decorator.
    
    It contains `Task` objects associated with the step, that is, all executions of the
    `Step`. The step may contain multiple `Task`s in the case of a foreach step.
    
    Attributes
    ----------
    task : Task
        The first `Task` object in this step. This is a shortcut for retrieving the only
        task contained in a non-foreach step.
    finished_at : datetime
        Time when the latest `Task` of this step finished. Note that in the case of foreaches,
        this time may change during execution of the step.
    environment_info : Dict[str, Any]
        Information about the execution environment.
    """
    @property
    def task(self) -> typing.Optional[metaflow.client.core.Task]:
        """
        Returns a Task object belonging to this step.
        
        This is useful when the step only contains one task (a linear step for example).
        
        Returns
        -------
        Task
            A task in the step
        """
        ...
    def tasks(self, *tags: str) -> typing.Iterable[metaflow.client.core.Task]:
        """
        [Legacy function - do not use]
        
        Returns an iterator over all `Task` objects in the step. This is an alias
        to iterating the object itself, i.e.
        ```
        list(Step(...)) == list(Step(...).tasks())
        ```
        
        Parameters
        ----------
        tags : str
            No op (legacy functionality)
        
        Yields
        ------
        Task
            `Task` objects in this step.
        """
        ...
    @property
    def control_task(self) -> typing.Optional[metaflow.client.core.Task]:
        """
        [Unpublished API - use with caution!]
        
        Returns a Control Task object belonging to this step.
        This is useful when the step only contains one control task.
        
        Returns
        -------
        Task
            A control task in the step
        """
        ...
    def control_tasks(self, *tags: str) -> typing.Iterator[metaflow.client.core.Task]:
        """
        [Unpublished API - use with caution!]
        
        Returns an iterator over all the control tasks in the step.
        An optional filter is available that allows you to filter on tags. The
        control tasks returned if the filter is specified will contain all the
        tags specified.
        Parameters
        ----------
        tags : str
            Tags to match
        
        Yields
        ------
        Task
            Control Task objects for this step
        """
        ...
    def __iter__(self) -> typing.Iterator[metaflow.client.core.Task]:
        """
        Iterate over all children Task of this Step
        
        Yields
        ------
        Task
            A Task in this Step
        """
        ...
    def __getitem__(self, task_id: str) -> metaflow.client.core.Task:
        """
        Returns the Task object with the task ID 'task_id'
        
        Parameters
        ----------
        task_id : str
            Task ID
        
        Returns
        -------
        Task
            Task for this task ID in this Step
        
        Raises
        ------
        KeyError
            If the task_id does not identify a valid Task object
        """
        ...
    def __getstate__(self):
        ...
    def __setstate__(self, state):
        ...
    @property
    def finished_at(self) -> typing.Optional[datetime.datetime]:
        """
        Returns the datetime object of when the step finished (successfully or not).
        
        A step is considered finished when all the tasks that belong to it have
        finished. This call will return None if the step has not finished
        
        Returns
        -------
        datetime
            Datetime of when the step finished
        """
        ...
    @property
    def environment_info(self) -> typing.Optional[typing.Dict[str, typing.Any]]:
        """
        Returns information about the environment that was used to execute this step. As an
        example, if the Conda environment is selected, this will return information about the
        dependencies that were used in the environment.
        
        This environment information is only available for steps that have tasks
        for which the code package has been saved.
        
        Returns
        -------
        Dict[str, Any], optional
            Dictionary describing the environment
        """
        ...
    ...

class Task(metaflow.client.core.MetaflowObject, metaclass=type):
    """
    A `Task` represents an execution of a `Step`.
    
    It contains all `DataArtifact` objects produced by the task as
    well as metadata related to execution.
    
    Note that the `@retry` decorator may cause multiple attempts of
    the task to be present. Usually you want the latest attempt, which
    is what instantiating a `Task` object returns by default. If
    you need to e.g. retrieve logs from a failed attempt, you can
    explicitly get information about a specific attempt by using the
    following syntax when creating a task:
    
    `Task('flow/run/step/task', attempt=<attempt>)`
    
    where `attempt=0` corresponds to the first attempt etc.
    
    Attributes
    ----------
    metadata : List[Metadata]
        List of all metadata events associated with the task.
    metadata_dict : Dict[str, str]
        A condensed version of `metadata`: A dictionary where keys
        are names of metadata events and values the latest corresponding event.
    data : MetaflowData
        Container of all data artifacts produced by this task. Note that this
        call downloads all data locally, so it can be slower than accessing
        artifacts individually. See `MetaflowData` for more information.
    artifacts : MetaflowArtifacts
        Container of `DataArtifact` objects produced by this task.
    successful : bool
        True if the task completed successfully.
    finished : bool
        True if the task completed.
    exception : object
        Exception raised by this task if there was one.
    finished_at : datetime
        Time this task finished.
    runtime_name : str
        Runtime this task was executed on.
    stdout : str
        Standard output for the task execution.
    stderr : str
        Standard error output for the task execution.
    code : MetaflowCode
        Code package for this task (if present). See `MetaflowCode`.
    environment_info : Dict[str, str]
        Information about the execution environment.
    """
    def __init__(self, *args, **kwargs):
        ...
    @property
    def metadata(self) -> typing.List[metaflow.client.core.Metadata]:
        """
        Metadata events produced by this task across all attempts of the task
        *except* if you selected a specific task attempt.
        
        Note that Metadata is different from tags.
        
        Returns
        -------
        List[Metadata]
            Metadata produced by this task
        """
        ...
    @property
    def metadata_dict(self) -> typing.Dict[str, str]:
        """
        Dictionary mapping metadata names (keys) and their associated values.
        
        Note that unlike the metadata() method, this call will only return the latest
        metadata for a given name. For example, if a task executes multiple times (retries),
        the same metadata name will be generated multiple times (one for each execution of the
        task). The metadata() method returns all those metadata elements whereas this call will
        return the metadata associated with the latest execution of the task.
        
        Returns
        -------
        Dict[str, str]
            Dictionary mapping metadata name with value
        """
        ...
    @property
    def index(self) -> typing.Optional[int]:
        """
        Returns the index of the innermost foreach loop if this task is run inside at least
        one foreach.
        
        The index is what distinguishes the various tasks inside a given step.
        This call returns None if this task was not run in a foreach loop.
        
        Returns
        -------
        int, optional
            Index in the innermost loop for this task
        """
        ...
    @property
    def data(self) -> metaflow.client.core.MetaflowData:
        """
        Returns a container of data artifacts produced by this task.
        
        You can access data produced by this task as follows:
        ```
        print(task.data.my_var)
        ```
        
        Returns
        -------
        MetaflowData
            Container of all artifacts produced by this task
        """
        ...
    @property
    def artifacts(self) -> typing.NamedTuple:
        """
        Returns a container of DataArtifacts produced by this task.
        
        You can access each DataArtifact by name like so:
        ```
        print(task.artifacts.my_var)
        ```
        This method differs from data() because it returns DataArtifact objects
        (which contain additional metadata) as opposed to just the data.
        
        Returns
        -------
        MetaflowArtifacts
            Container of all DataArtifacts produced by this task
        """
        ...
    @property
    def successful(self) -> bool:
        """
        Indicates whether or not the task completed successfully.
        
        This information is always about the latest task to have completed (in case
        of retries).
        
        Returns
        -------
        bool
            True if the task completed successfully and False otherwise
        """
        ...
    @property
    def finished(self) -> bool:
        """
        Indicates whether or not the task completed.
        
        This information is always about the latest task to have completed (in case
        of retries).
        
        Returns
        -------
        bool
            True if the task completed and False otherwise
        """
        ...
    @property
    def exception(self) -> typing.Optional[typing.Any]:
        """
        Returns the exception that caused the task to fail, if any.
        
        This information is always about the latest task to have completed (in case
        of retries). If successful() returns False and finished() returns True,
        this method can help determine what went wrong.
        
        Returns
        -------
        object
            Exception raised by the task or None if not applicable
        """
        ...
    @property
    def finished_at(self) -> typing.Optional[datetime.datetime]:
        """
        Returns the datetime object of when the task finished (successfully or not).
        
        This information is always about the latest task to have completed (in case
        of retries). This call will return None if the task is not finished.
        
        Returns
        -------
        datetime
            Datetime of when the task finished
        """
        ...
    @property
    def runtime_name(self) -> typing.Optional[str]:
        """
        Returns the name of the runtime this task executed on.
        
        
        Returns
        -------
        str
            Name of the runtime this task executed on
        """
        ...
    @property
    def stdout(self) -> str:
        """
        Returns the full standard out of this task.
        
        If you specify a specific attempt for this task, it will return the
        standard out for that attempt. If you do not specify an attempt,
        this will return the current standard out for the latest *started*
        attempt of the task. In both cases, multiple calls to this
        method will return the most up-to-date log (so if an attempt is not
        done, each call will fetch the latest log).
        
        Returns
        -------
        str
            Standard output of this task
        """
        ...
    @property
    def stdout_size(self) -> int:
        """
        Returns the size of the stdout log of this task.
        
        Similar to `stdout`, the size returned is the latest size of the log
        (so for a running attempt, this value will increase as the task produces
        more output).
        
        Returns
        -------
        int
            Size of the stdout log content (in bytes)
        """
        ...
    @property
    def stderr(self) -> str:
        """
        Returns the full standard error of this task.
        
        If you specify a specific attempt for this task, it will return the
        standard error for that attempt. If you do not specify an attempt,
        this will return the current standard error for the latest *started*
        attempt. In both cases, multiple calls to this
        method will return the most up-to-date log (so if an attempt is not
        done, each call will fetch the latest log).
        
        Returns
        -------
        str
            Standard error of this task
        """
        ...
    @property
    def stderr_size(self) -> int:
        """
        Returns the size of the stderr log of this task.
        
        Similar to `stderr`, the size returned is the latest size of the log
        (so for a running attempt, this value will increase as the task produces
        more output).
        
        Returns
        -------
        int
            Size of the stderr log content (in bytes)
        """
        ...
    @property
    def current_attempt(self) -> int:
        """
        Get the relevant attempt for this Task.
        
        Returns the specific attempt used when
        initializing the instance, or the latest *started* attempt for the Task.
        
        Returns
        -------
        int
            attempt id for this task object
        """
        ...
    @property
    def code(self) -> typing.Optional[metaflow.client.core.MetaflowCode]:
        """
        Returns the MetaflowCode object for this task, if present.
        
        Not all tasks save their code so this call may return None in those cases.
        
        Returns
        -------
        MetaflowCode
            Code package for this task
        """
        ...
    @property
    def environment_info(self) -> typing.Dict[str, typing.Any]:
        """
        Returns information about the environment that was used to execute this task. As an
        example, if the Conda environment is selected, this will return information about the
        dependencies that were used in the environment.
        
        This environment information is only available for tasks that have a code package.
        
        Returns
        -------
        Dict
            Dictionary describing the environment
        """
        ...
    def loglines(self, stream: str, as_unicode: bool = True, meta_dict: typing.Optional[typing.Dict[str, typing.Any]] = None) -> typing.Iterator[typing.Tuple[datetime.datetime, str]]:
        """
        Return an iterator over (utc_timestamp, logline) tuples.
        
        Parameters
        ----------
        stream : str
            Either 'stdout' or 'stderr'.
        as_unicode : bool, default: True
            If as_unicode=False, each logline is returned as a byte object. Otherwise,
            it is returned as a (unicode) string.
        
        Yields
        ------
        Tuple[datetime, str]
            Tuple of timestamp, logline pairs.
        """
        ...
    def __iter__(self) -> typing.Iterator[metaflow.client.core.DataArtifact]:
        """
        Iterate over all children DataArtifact of this Task
        
        Yields
        ------
        DataArtifact
            A DataArtifact in this Step
        """
        ...
    def __getitem__(self, name: str) -> metaflow.client.core.DataArtifact:
        """
        Returns the DataArtifact object with the artifact name 'name'
        
        Parameters
        ----------
        name : str
            Data artifact name
        
        Returns
        -------
        DataArtifact
            DataArtifact for this artifact name in this task
        
        Raises
        ------
        KeyError
            If the name does not identify a valid DataArtifact object
        """
        ...
    def __getstate__(self):
        ...
    def __setstate__(self, state):
        ...
    ...

class DataArtifact(metaflow.client.core.MetaflowObject, metaclass=type):
    """
    A single data artifact and associated metadata. Note that this object does
    not contain other objects as it is the leaf object in the hierarchy.
    
    Attributes
    ----------
    data : object
        The data contained in this artifact, that is, the object produced during
        execution of this run.
    sha : string
        A unique ID of this artifact.
    finished_at : datetime
        Corresponds roughly to the `Task.finished_at` time of the parent `Task`.
        An alias for `DataArtifact.created_at`.
    """
    @property
    def data(self) -> typing.Any:
        """
        Unpickled representation of the data contained in this artifact.
        
        Returns
        -------
        object
            Object contained in this artifact
        """
        ...
    @property
    def size(self) -> int:
        """
        Returns the size (in bytes) of the pickled object representing this
        DataArtifact
        
        Returns
        -------
        int
            size of the pickled representation of data artifact (in bytes)
        """
        ...
    @property
    def sha(self) -> str:
        """
        Unique identifier for this artifact.
        
        This is a unique hash of the artifact (historically SHA1 hash)
        
        Returns
        -------
        str
            Hash of this artifact
        """
        ...
    @property
    def finished_at(self) -> datetime.datetime:
        """
        Creation time for this artifact.
        
        Alias for created_at.
        
        Returns
        -------
        datetime
            Creation time
        """
        ...
    def __getstate__(self):
        ...
    def __setstate__(self, state):
        ...
    ...

class Runner(object, metaclass=type):
    """
    Metaflow's Runner API that presents a programmatic interface
    to run flows and perform other operations either synchronously or asynchronously.
    The class expects a path to the flow file along with optional arguments
    that match top-level options on the command-line.
    
    This class works as a context manager, calling `cleanup()` to remove
    temporary files at exit.
    
    Example:
    ```python
    with Runner('slowflow.py', pylint=False) as runner:
        result = runner.run(alpha=5, tags=["abc", "def"], max_workers=5)
        print(result.run.finished)
    ```
    
    Parameters
    ----------
    flow_file : str
        Path to the flow file to run
    show_output : bool, default True
        Show the 'stdout' and 'stderr' to the console by default,
        Only applicable for synchronous 'run' and 'resume' functions.
    profile : Optional[str], default None
        Metaflow profile to use to run this run. If not specified, the default
        profile is used (or the one already set using `METAFLOW_PROFILE`)
    env : Optional[Dict], default None
        Additional environment variables to set for the Run. This overrides the
        environment set for this process.
    cwd : Optional[str], default None
        The directory to run the subprocess in; if not specified, the current
        directory is used.
    file_read_timeout : int, default 3600
        The timeout until which we try to read the runner attribute file.
    **kwargs : Any
        Additional arguments that you would pass to `python myflow.py` before
        the `run` command.
    """
    def __init__(self, flow_file: str, show_output: bool = True, profile: typing.Optional[str] = None, env: typing.Optional[typing.Dict] = None, cwd: typing.Optional[str] = None, file_read_timeout: int = 3600, **kwargs):
        ...
    def __enter__(self) -> metaflow.runner.metaflow_runner.Runner:
        ...
    def __aenter__(self) -> metaflow.runner.metaflow_runner.Runner:
        ...
    def _Runner__get_executing_run(self, tfp_runner_attribute, command_obj):
        ...
    def run(self, **kwargs) -> metaflow.runner.metaflow_runner.ExecutingRun:
        """
        Blocking execution of the run. This method will wait until
        the run has completed execution.
        
        Parameters
        ----------
        **kwargs : Any
            Additional arguments that you would pass to `python myflow.py` after
            the `run` command, in particular, any parameters accepted by the flow.
        
        Returns
        -------
        ExecutingRun
            ExecutingRun containing the results of the run.
        """
        ...
    def resume(self, **kwargs):
        """
        Blocking resume execution of the run.
        This method will wait until the resumed run has completed execution.
        
        Parameters
        ----------
        **kwargs : Any
            Additional arguments that you would pass to `python ./myflow.py` after
            the `resume` command.
        
        Returns
        -------
        ExecutingRun
            ExecutingRun containing the results of the resumed run.
        """
        ...
    def async_run(self, **kwargs) -> metaflow.runner.metaflow_runner.ExecutingRun:
        """
        Non-blocking execution of the run. This method will return as soon as the
        run has launched.
        
        Note that this method is asynchronous and needs to be `await`ed.
        
        Parameters
        ----------
        **kwargs : Any
            Additional arguments that you would pass to `python myflow.py` after
            the `run` command, in particular, any parameters accepted by the flow.
        
        Returns
        -------
        ExecutingRun
            ExecutingRun representing the run that was started.
        """
        ...
    def async_resume(self, **kwargs):
        """
        Non-blocking resume execution of the run.
        This method will return as soon as the resume has launched.
        
        Note that this method is asynchronous and needs to be `await`ed.
        
        Parameters
        ----------
        **kwargs : Any
            Additional arguments that you would pass to `python myflow.py` after
            the `resume` command.
        
        Returns
        -------
        ExecutingRun
            ExecutingRun representing the resumed run that was started.
        """
        ...
    def __exit__(self, exc_type, exc_value, traceback):
        ...
    def __aexit__(self, exc_type, exc_value, traceback):
        ...
    def cleanup(self):
        """
        Delete any temporary files created during execution.
        """
        ...
    ...

class NBRunner(object, metaclass=type):
    """
    A  wrapper over `Runner` for executing flows defined in a Jupyter
    notebook cell.
    
    Instantiate this class on the last line of a notebook cell where
    a `flow` is defined. In contrast to `Runner`, this class is not
    meant to be used in a context manager. Instead, use a blocking helper
    function like `nbrun` (which calls `cleanup()` internally) or call
    `cleanup()` explictly when using non-blocking APIs.
    
    ```python
    run = NBRunner(FlowName).nbrun()
    ```
    
    Parameters
    ----------
    flow : FlowSpec
        Flow defined in the same cell
    show_output : bool, default True
        Show the 'stdout' and 'stderr' to the console by default,
        Only applicable for synchronous 'run' and 'resume' functions.
    profile : Optional[str], default None
        Metaflow profile to use to run this run. If not specified, the default
        profile is used (or the one already set using `METAFLOW_PROFILE`)
    env : Optional[Dict], default None
        Additional environment variables to set for the Run. This overrides the
        environment set for this process.
    base_dir : Optional[str], default None
        The directory to run the subprocess in; if not specified, the current
        working directory is used.
    file_read_timeout : int, default 3600
        The timeout until which we try to read the runner attribute file.
    **kwargs : Any
        Additional arguments that you would pass to `python myflow.py` before
        the `run` command.
    """
    def __init__(self, flow, show_output: bool = True, profile: typing.Optional[str] = None, env: typing.Optional[typing.Dict] = None, base_dir: typing.Optional[str] = None, file_read_timeout: int = 3600, **kwargs):
        ...
    def nbrun(self, **kwargs):
        """
        Blocking execution of the run. This method will wait until
        the run has completed execution.
        
        Note that in contrast to `run`, this method returns a
        `metaflow.Run` object directly and calls `cleanup()` internally
        to support a common notebook pattern of executing a flow and
        retrieving its results immediately.
        
        Parameters
        ----------
        **kwargs : Any
            Additional arguments that you would pass to `python myflow.py` after
            the `run` command, in particular, any parameters accepted by the flow.
        
        Returns
        -------
        Run
            A `metaflow.Run` object representing the finished run.
        """
        ...
    def nbresume(self, **kwargs):
        """
        Blocking resuming of a run. This method will wait until
        the resumed run has completed execution.
        
        Note that in contrast to `resume`, this method returns a
        `metaflow.Run` object directly and calls `cleanup()` internally
        to support a common notebook pattern of executing a flow and
        retrieving its results immediately.
        
        Parameters
        ----------
        **kwargs : Any
            Additional arguments that you would pass to `python myflow.py` after
            the `resume` command.
        
        Returns
        -------
        Run
            A `metaflow.Run` object representing the resumed run.
        """
        ...
    def run(self, **kwargs):
        """
        Runs the flow.
        """
        ...
    def resume(self, **kwargs):
        """
        Resumes the flow.
        """
        ...
    def async_run(self, **kwargs):
        """
        Non-blocking execution of the run. This method will return as soon as the
        run has launched. This method is equivalent to `Runner.async_run`.
        
        Note that this method is asynchronous and needs to be `await`ed.
        
        
        Parameters
        ----------
        **kwargs : Any
            Additional arguments that you would pass to `python myflow.py` after
            the `run` command, in particular, any parameters accepted by the flow.
        
        Returns
        -------
        ExecutingRun
            ExecutingRun representing the run that was started.
        """
        ...
    def async_resume(self, **kwargs):
        """
        Non-blocking execution of the run. This method will return as soon as the
        run has launched. This method is equivalent to `Runner.async_resume`.
        
        Note that this method is asynchronous and needs to be `await`ed.
        
        Parameters
        ----------
        **kwargs : Any
            Additional arguments that you would pass to `python myflow.py` after
            the `run` command, in particular, any parameters accepted by the flow.
        
        Returns
        -------
        ExecutingRun
            ExecutingRun representing the run that was started.
        """
        ...
    def cleanup(self):
        """
        Delete any temporary files created during execution.
        
        Call this method after using `async_run` or `async_resume`. You don't
        have to call this after `nbrun` or `nbresume`.
        """
        ...
    ...

class Deployer(object, metaclass=type):
    """
    Use the `Deployer` class to configure and access one of the production
    orchestrators supported by Metaflow.
    
    Parameters
    ----------
    flow_file : str
        Path to the flow file to deploy.
    show_output : bool, default True
        Show the 'stdout' and 'stderr' to the console by default.
    profile : Optional[str], default None
        Metaflow profile to use for the deployment. If not specified, the default
        profile is used.
    env : Optional[Dict[str, str]], default None
        Additional environment variables to set for the deployment.
    cwd : Optional[str], default None
        The directory to run the subprocess in; if not specified, the current
        directory is used.
    file_read_timeout : int, default 3600
        The timeout until which we try to read the deployer attribute file.
    **kwargs : Any
        Additional arguments that you would pass to `python myflow.py` before
        the deployment command.
    """
    def __init__(self, flow_file: str, show_output: bool = True, profile: typing.Optional[str] = None, env: typing.Optional[typing.Dict] = None, cwd: typing.Optional[str] = None, file_read_timeout: int = 3600, **kwargs):
        ...
    def _Deployer__make_function(self, deployer_class):
        """
        Create a function for the given deployer class.
        
        Parameters
        ----------
        deployer_class : Type[DeployerImpl]
            Deployer implementation class.
        
        Returns
        -------
        Callable
            Function that initializes and returns an instance of the deployer class.
        """
        ...
    ...

class NBDeployer(object, metaclass=type):
    """
    A  wrapper over `Deployer` for deploying flows defined in a Jupyter
    notebook cell.
    
    Instantiate this class on the last line of a notebook cell where
    a `flow` is defined. In contrast to `Deployer`, this class is not
    meant to be used in a context manager.
    
    ```python
    deployer = NBDeployer(FlowName)
    ar = deployer.argo_workflows(name="madhur")
    ar_obj = ar.create()
    result = ar_obj.trigger(alpha=300)
    print(result.status)
    print(result.run)
    result.terminate()
    ```
    
    Parameters
    ----------
    flow : FlowSpec
        Flow defined in the same cell
    show_output : bool, default True
        Show the 'stdout' and 'stderr' to the console by default,
    profile : Optional[str], default None
        Metaflow profile to use to deploy this run. If not specified, the default
        profile is used (or the one already set using `METAFLOW_PROFILE`)
    env : Optional[Dict[str, str]], default None
        Additional environment variables to set. This overrides the
        environment set for this process.
    base_dir : Optional[str], default None
        The directory to run the subprocess in; if not specified, the current
        working directory is used.
    **kwargs : Any
        Additional arguments that you would pass to `python myflow.py` i.e. options
        listed in `python myflow.py --help`
    """
    def __init__(self, flow, show_output: bool = True, profile: typing.Optional[str] = None, env: typing.Optional[typing.Dict] = None, base_dir: typing.Optional[str] = None, file_read_timeout: int = 3600, **kwargs):
        ...
    def cleanup(self):
        """
        Delete any temporary files created during execution.
        """
        ...
    ...

pkg_name: str

class Checkpoint(object, metaclass=type):
    def __init__(self, temp_dir_root = None, init_dir = False):
        ...
    @property
    def directory(self):
        ...
    def save(self, path = None, metadata = None, latest = True, name = "mfchckpt", storage_format = "files"):
        """
        Saves the checkpoint to the datastore
        
        Parameters
        ----------
        path : Optional[Union[str, os.PathLike]], default: None
            The path to save the checkpoint. Accepts a file path or a directory path.
                - If a directory path is provided, all the contents within that directory will be saved.
                When a checkpoint is reloaded during task retries, `the current.checkpoint.directory` will
                contain the contents of this directory.
                - If a file path is provided, the file will be directly saved to the datastore (with the same filename).
                When the checkpoint is reloaded during task retries, the file with the same name will be available in the
                `current.checkpoint.directory`.
                - If no path is provided then the `Checkpoint.directory` will be saved as the checkpoint.
        
        name : Optional[str], default: "mfchckpt"
            The name of the checkpoint.
        
        metadata : Optional[Dict], default: {}
            Any metadata that needs to be saved with the checkpoint.
        
        latest : bool, default: True
            If True, the checkpoint will be marked as the latest checkpoint.
            This helps determine if the checkpoint gets loaded when the task restarts.
        
        storage_format : str, default: files
            If `tar`, the contents of the directory will be tarred before saving to the datastore.
            If `files`, saves directory directly to the datastore.
        """
        ...
    def __enter__(self):
        ...
    def __exit__(self, exc_type, exc_val, exc_tb):
        ...
    def list(self, name: typing.Optional[str] = None, task: typing.Union["metaflow.Task", str, None] = None, attempt: typing.Union[int, str, None] = None, as_dict: bool = True, within_task: bool = True) -> typing.Iterable[typing.Union[typing.Dict, metaflow_extensions.obcheckpoint.plugins.machine_learning_utilities.datastructures.CheckpointArtifact]]:
        """
        lists the checkpoints in the datastore based on the Task.
        It will always be task scoped.
        
        Usage:
        ------
        
        ```python
        
        Checkpoint().list(name="best") # lists checkpoints in the current task with the name "best"
        Checkpoint().list(task="anotherflow/somerunid/somestep/sometask", name="best") # Identical as the above one but
        Checkpoint().list() # lists all the checkpoints in the current task
        
        ```
        
        Parameters
        ----------
        
        - `name`:
            - name of the checkpoint to filter for
        - `task`:
            - Task object outside the one that is currently set in the `Checkpoint` object; Can be a pathspec string.
        - `attempt`:
            - attempt number of the task (optional filter. If none, then lists all checkpoints from all attempts)
        """
        ...
    def load(self, reference: typing.Union[str, typing.Dict, metaflow_extensions.obcheckpoint.plugins.machine_learning_utilities.datastructures.CheckpointArtifact], path: typing.Optional[str] = None):
        """
        loads a checkpoint reference from the datastore. (resembles a read op)
        
        Parameters
        ----------
        
        `reference` :
            - can be a string, dict or a CheckpointArtifact object:
                - string: a string reference to the checkpoint (checkpoint key)
                - dict: a dictionary reference to the checkpoint
                - CheckpointArtifact: a CheckpointArtifact object reference to the checkpoint
        """
        ...
    ...

def load_model(reference: typing.Union[str, metaflow_extensions.obcheckpoint.plugins.machine_learning_utilities.datastructures.MetaflowDataArtifactReference, dict], path: str):
    ...

def get_aws_client(module, with_error = False, role_arn = None, session_vars = None, client_params = None):
    ...


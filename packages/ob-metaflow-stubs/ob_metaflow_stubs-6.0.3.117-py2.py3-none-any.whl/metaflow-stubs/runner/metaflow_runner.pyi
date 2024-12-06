##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.12.27.1+obcheckpoint(0.1.2);ob(v1)                               #
# Generated on 2024-11-13T19:05:29.365193                                        #
##################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import datetime
    import metaflow.runner.subprocess_manager
    import metaflow.client.core
    import metaflow.events
    import metaflow.runner.metaflow_runner

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

def handle_timeout(tfp_runner_attribute, command_obj: "CommandManager", file_read_timeout: int):
    """
    Handle the timeout for a running subprocess command that reads a file
    and raises an error with appropriate logs if a TimeoutError occurs.
    
    Parameters
    ----------
    tfp_runner_attribute : NamedTemporaryFile
        Temporary file that stores runner attribute data.
    command_obj : CommandManager
        Command manager object that encapsulates the running command details.
    file_read_timeout : int
        Timeout for reading the file.
    
    Returns
    -------
    str
        Content read from the temporary file.
    
    Raises
    ------
    RuntimeError
        If a TimeoutError occurs, it raises a RuntimeError with the command's
        stdout and stderr logs.
    """
    ...

class CommandManager(object, metaclass=type):
    """
    A manager for an individual subprocess.
    """
    def __init__(self, command: typing.List[str], env: typing.Optional[typing.Dict[str, str]] = None, cwd: typing.Optional[str] = None):
        """
        Create a new CommandManager object.
        This does not run the process itself but sets it up.
        
        Parameters
        ----------
        command : List[str]
            The command to run in List form.
        env : Optional[Dict[str, str]], default None
            Environment variables to set for the subprocess; if not specified,
            the current enviornment variables are used.
        cwd : Optional[str], default None
            The directory to run the subprocess in; if not specified, the current
            directory is used.
        """
        ...
    def __aenter__(self) -> metaflow.runner.subprocess_manager.CommandManager:
        ...
    def __aexit__(self, exc_type, exc_value, traceback):
        ...
    def wait(self, timeout: typing.Optional[float] = None, stream: typing.Optional[str] = None):
        """
        Wait for the subprocess to finish, optionally with a timeout
        and optionally streaming its output.
        
        You can only call `wait` if `async_run` has already been called.
        
        Parameters
        ----------
        timeout : Optional[float], default None
            The maximum time to wait for the subprocess to finish.
            If the timeout is reached, the subprocess is killed.
        stream : Optional[str], default None
            If specified, the specified stream is printed to stdout. `stream` can
            be one of `stdout` or `stderr`.
        """
        ...
    def sync_wait(self):
        ...
    def run(self, show_output: bool = False):
        """
        Run the subprocess synchronously. This can only be called once.
        
        This also waits on the process implicitly.
        
        Parameters
        ----------
        show_output : bool, default False
            Suppress the 'stdout' and 'stderr' to the console by default.
            They can be accessed later by reading the files present in:
                - self.log_files["stdout"]
                - self.log_files["stderr"]
        """
        ...
    def async_run(self):
        """
        Run the subprocess asynchronously. This can only be called once.
        
        Once this is called, you can then wait on the process (using `wait`), stream
        logs (using `stream_logs`) or kill it (using `kill`).
        """
        ...
    def stream_log(self, stream: str, position: typing.Optional[int] = None, timeout_per_line: typing.Optional[float] = None, log_write_delay: float = 0.01) -> typing.Iterator[typing.Tuple[int, str]]:
        """
        Stream logs from the subprocess line by line.
        
        Parameters
        ----------
        stream : str
            The stream to stream logs from. Can be one of "stdout" or "stderr".
        position : Optional[int], default None
            The position in the log file to start streaming from. If None, it starts
            from the beginning of the log file. This allows resuming streaming from
            a previously known position
        timeout_per_line : Optional[float], default None
            The time to wait for a line to be read from the log file. If None, it
            waits indefinitely. If the timeout is reached, a LogReadTimeoutError
            is raised. Note that this timeout is *per line* and not cumulative so this
            function may take significantly more time than `timeout_per_line`
        log_write_delay : float, default 0.01
            Improves the probability of getting whole lines. This setting is for
            advanced use cases.
        
        Yields
        ------
        Tuple[int, str]
            A tuple containing the position in the log file and the line read. The
            position returned can be used to feed into another `stream_logs` call
            for example.
        """
        ...
    def emit_logs(self, stream: str = "stdout", custom_logger: typing.Callable[..., None] = print):
        """
        Helper function that can easily emit all the logs for a given stream.
        
        This function will only terminate when all the log has been printed.
        
        Parameters
        ----------
        stream : str, default "stdout"
            The stream to emit logs for. Can be one of "stdout" or "stderr".
        custom_logger : Callable[..., None], default print
            A custom logger function that takes in a string and "emits" it. By default,
            the log is printed to stdout.
        """
        ...
    def cleanup(self):
        """
        Clean up log files for a running subprocesses.
        """
        ...
    def kill(self, termination_timeout: float = 2):
        """
        Kill the subprocess and its descendants.
        
        Parameters
        ----------
        termination_timeout : float, default 2
            The time to wait after sending a SIGTERM to the process and its descendants
            before sending a SIGKILL.
        """
        ...
    ...

class SubprocessManager(object, metaclass=type):
    """
    A manager for subprocesses. The subprocess manager manages one or more
    CommandManager objects, each of which manages an individual subprocess.
    """
    def __init__(self):
        ...
    def __aenter__(self) -> metaflow.runner.subprocess_manager.SubprocessManager:
        ...
    def __aexit__(self, exc_type, exc_value, traceback):
        ...
    def run_command(self, command: typing.List[str], env: typing.Optional[typing.Dict[str, str]] = None, cwd: typing.Optional[str] = None, show_output: bool = False) -> int:
        """
        Run a command synchronously and return its process ID.
        
        Parameters
        ----------
        command : List[str]
            The command to run in List form.
        env : Optional[Dict[str, str]], default None
            Environment variables to set for the subprocess; if not specified,
            the current enviornment variables are used.
        cwd : Optional[str], default None
            The directory to run the subprocess in; if not specified, the current
            directory is used.
        show_output : bool, default False
            Suppress the 'stdout' and 'stderr' to the console by default.
            They can be accessed later by reading the files present in the
            CommandManager object:
                - command_obj.log_files["stdout"]
                - command_obj.log_files["stderr"]
        Returns
        -------
        int
            The process ID of the subprocess.
        """
        ...
    def async_run_command(self, command: typing.List[str], env: typing.Optional[typing.Dict[str, str]] = None, cwd: typing.Optional[str] = None) -> int:
        """
        Run a command asynchronously and return its process ID.
        
        Parameters
        ----------
        command : List[str]
            The command to run in List form.
        env : Optional[Dict[str, str]], default None
            Environment variables to set for the subprocess; if not specified,
            the current enviornment variables are used.
        cwd : Optional[str], default None
            The directory to run the subprocess in; if not specified, the current
            directory is used.
        
        Returns
        -------
        int
            The process ID of the subprocess.
        """
        ...
    def get(self, pid: int) -> typing.Optional["CommandManager"]:
        """
        Get one of the CommandManager managed by this SubprocessManager.
        
        Parameters
        ----------
        pid : int
            The process ID of the subprocess (returned by run_command or async_run_command).
        
        Returns
        -------
        Optional[CommandManager]
            The CommandManager object for the given process ID, or None if not found.
        """
        ...
    def cleanup(self):
        """
        Clean up log files for all running subprocesses.
        """
        ...
    ...

class ExecutingRun(object, metaclass=type):
    """
    This class contains a reference to a `metaflow.Run` object representing
    the currently executing or finished run, as well as metadata related
    to the process.
    
    `ExecutingRun` is returned by methods in `Runner` and `NBRunner`. It is not
    meant to be instantiated directly.
    
    This class works as a context manager, allowing you to use a pattern like
    ```python
    with Runner(...).run() as running:
        ...
    ```
    Note that you should use either this object as the context manager or
    `Runner`, not both in a nested manner.
    """
    def __init__(self, runner: Runner, command_obj: metaflow.runner.subprocess_manager.CommandManager, run_obj: metaflow.client.core.Run):
        """
        Create a new ExecutingRun -- this should not be done by the user directly but
        instead user Runner.run()
        
        Parameters
        ----------
        runner : Runner
            Parent runner for this run.
        command_obj : CommandManager
            CommandManager containing the subprocess executing this run.
        run_obj : Run
            Run object corresponding to this run.
        """
        ...
    def __enter__(self) -> ExecutingRun:
        ...
    def __exit__(self, exc_type, exc_value, traceback):
        ...
    def wait(self, timeout: typing.Optional[float] = None, stream: typing.Optional[str] = None) -> ExecutingRun:
        """
        Wait for this run to finish, optionally with a timeout
        and optionally streaming its output.
        
        Note that this method is asynchronous and needs to be `await`ed.
        
        Parameters
        ----------
        timeout : Optional[float], default None
            The maximum time to wait for the run to finish.
            If the timeout is reached, the run is terminated
        stream : Optional[str], default None
            If specified, the specified stream is printed to stdout. `stream` can
            be one of `stdout` or `stderr`.
        
        Returns
        -------
        ExecutingRun
            This object, allowing you to chain calls.
        """
        ...
    @property
    def returncode(self) -> typing.Optional[int]:
        """
        Gets the return code of the underlying subprocess. A non-zero
        code indicates a failure, `None` a currently executing run.
        
        Returns
        -------
        Optional[int]
            The return code of the underlying subprocess.
        """
        ...
    @property
    def status(self) -> str:
        """
        Returns the status of the underlying subprocess that is responsible
        for executing the run.
        
        The return value is one of the following strings:
        - `timeout` indicates that the run timed out.
        - `running` indicates a currently executing run.
        - `failed` indicates a failed run.
        - `successful` indicates a successful run.
        
        Returns
        -------
        str
            The current status of the run.
        """
        ...
    @property
    def stdout(self) -> str:
        """
        Returns the current stdout of the run. If the run is finished, this will
        contain the entire stdout output. Otherwise, it will contain the
        stdout up until this point.
        
        Returns
        -------
        str
            The current snapshot of stdout.
        """
        ...
    @property
    def stderr(self) -> str:
        """
        Returns the current stderr of the run. If the run is finished, this will
        contain the entire stderr output. Otherwise, it will contain the
        stderr up until this point.
        
        Returns
        -------
        str
            The current snapshot of stderr.
        """
        ...
    def stream_log(self, stream: str, position: typing.Optional[int] = None) -> typing.Iterator[typing.Tuple[int, str]]:
        """
        Asynchronous iterator to stream logs from the subprocess line by line.
        
        Note that this method is asynchronous and needs to be `await`ed.
        
        Parameters
        ----------
        stream : str
            The stream to stream logs from. Can be one of `stdout` or `stderr`.
        position : Optional[int], default None
            The position in the log file to start streaming from. If None, it starts
            from the beginning of the log file. This allows resuming streaming from
            a previously known position
        
        Yields
        ------
        Tuple[int, str]
            A tuple containing the position in the log file and the line read. The
            position returned can be used to feed into another `stream_logs` call
            for example.
        """
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
    def __enter__(self) -> Runner:
        ...
    def __aenter__(self) -> Runner:
        ...
    def _Runner__get_executing_run(self, tfp_runner_attribute, command_obj):
        ...
    def run(self, **kwargs) -> ExecutingRun:
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
    def async_run(self, **kwargs) -> ExecutingRun:
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


##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.12.27.1+obcheckpoint(0.1.2);ob(v1)                               #
# Generated on 2024-11-13T19:05:29.384824                                        #
##################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import io
    import metaflow.plugins.datatools.s3.s3
    import metaflow.exception

def read_in_chunks(dst, src, src_sz, max_chunk_size):
    ...

class MetaflowLocalNotFound(metaflow.exception.MetaflowException, metaclass=type):
    ...

class MetaflowLocalURLException(metaflow.exception.MetaflowException, metaclass=type):
    ...

class Local(object, metaclass=type):
    """
    This class allows you to access the local filesystem in a way similar to the S3 datatools
    client. It is a stripped down version for now and only implements the functionality needed
    for this use case.
    
    In the future, we may want to allow it to be used in a way similar to the S3() client.
    """
    @classmethod
    def get_root_from_config(cls, echo, create_on_absent = True):
        ...
    def __init__(self):
        """
        Initialize a new context for Local file operations. This object is based used as
        a context manager for a with statement.
        """
        ...
    def __enter__(self):
        ...
    def __exit__(self, *args):
        ...
    def get(self, key = None, return_missing = False):
        ...
    def put(self, key, obj, overwrite = True):
        ...
    def info(self, key = None, return_missing = False):
        ...
    ...

class MetaflowS3Exception(metaflow.exception.MetaflowException, metaclass=type):
    ...

class S3(object, metaclass=type):
    """
    The Metaflow S3 client.
    
    This object manages the connection to S3 and a temporary diretory that is used
    to download objects. Note that in most cases when the data fits in memory, no local
    disk IO is needed as operations are cached by the operating system, which makes
    operations fast as long as there is enough memory available.
    
    The easiest way is to use this object as a context manager:
    ```
    with S3() as s3:
        data = [obj.blob for obj in s3.get_many(urls)]
    print(data)
    ```
    The context manager takes care of creating and deleting a temporary directory
    automatically. Without a context manager, you must call `.close()` to delete
    the directory explicitly:
    ```
    s3 = S3()
    data = [obj.blob for obj in s3.get_many(urls)]
    s3.close()
    ```
    You can customize the location of the temporary directory with `tmproot`. It
    defaults to the current working directory.
    
    To make it easier to deal with object locations, the client can be initialized
    with an S3 path prefix. There are three ways to handle locations:
    
    1. Use a `metaflow.Run` object or `self`, e.g. `S3(run=self)` which
       initializes the prefix with the global `DATATOOLS_S3ROOT` path, combined
       with the current run ID. This mode makes it easy to version data based
       on the run ID consistently. You can use the `bucket` and `prefix` to
       override parts of `DATATOOLS_S3ROOT`.
    
    2. Specify an S3 prefix explicitly with `s3root`,
       e.g. `S3(s3root='s3://mybucket/some/path')`.
    
    3. Specify nothing, i.e. `S3()`, in which case all operations require
       a full S3 url prefixed with `s3://`.
    
    Parameters
    ----------
    tmproot : str, default: '.'
        Where to store the temporary directory.
    bucket : str, optional
        Override the bucket from `DATATOOLS_S3ROOT` when `run` is specified.
    prefix : str, optional
        Override the path from `DATATOOLS_S3ROOT` when `run` is specified.
    run : FlowSpec or Run, optional
        Derive path prefix from the current or a past run ID, e.g. S3(run=self).
    s3root : str, optional
        If `run` is not specified, use this as the S3 prefix.
    """
    @classmethod
    def get_root_from_config(cls, echo, create_on_absent = True):
        ...
    def __enter__(self) -> metaflow.plugins.datatools.s3.s3.S3:
        ...
    def __exit__(self, *args):
        ...
    def close(self):
        """
        Delete all temporary files downloaded in this context.
        """
        ...
    def list_paths(self, keys: typing.Optional[typing.Iterable[str]] = None) -> typing.List[metaflow.plugins.datatools.s3.s3.S3Object]:
        """
        List the next level of paths in S3.
        
        If multiple keys are specified, listings are done in parallel. The returned
        S3Objects have `.exists == False` if the path refers to a prefix, not an
        existing S3 object.
        
        For instance, if the directory hierarchy is
        ```
        a/0.txt
        a/b/1.txt
        a/c/2.txt
        a/d/e/3.txt
        f/4.txt
        ```
        The `list_paths(['a', 'f'])` call returns
        ```
        a/0.txt (exists == True)
        a/b/ (exists == False)
        a/c/ (exists == False)
        a/d/ (exists == False)
        f/4.txt (exists == True)
        ```
        
        Parameters
        ----------
        keys : Iterable[str], optional, default None
            List of paths.
        
        Returns
        -------
        List[S3Object]
            S3Objects under the given paths, including prefixes (directories) that
            do not correspond to leaf objects.
        """
        ...
    def list_recursive(self, keys: typing.Optional[typing.Iterable[str]] = None) -> typing.List[metaflow.plugins.datatools.s3.s3.S3Object]:
        """
        List all objects recursively under the given prefixes.
        
        If multiple keys are specified, listings are done in parallel. All objects
        returned have `.exists == True` as this call always returns leaf objects.
        
        For instance, if the directory hierarchy is
        ```
        a/0.txt
        a/b/1.txt
        a/c/2.txt
        a/d/e/3.txt
        f/4.txt
        ```
        The `list_paths(['a', 'f'])` call returns
        ```
        a/0.txt (exists == True)
        a/b/1.txt (exists == True)
        a/c/2.txt (exists == True)
        a/d/e/3.txt (exists == True)
        f/4.txt (exists == True)
        ```
        
        Parameters
        ----------
        keys : Iterable[str], optional, default None
            List of paths.
        
        Returns
        -------
        List[S3Object]
            S3Objects under the given paths.
        """
        ...
    def info(self, key: typing.Optional[str] = None, return_missing: bool = False) -> metaflow.plugins.datatools.s3.s3.S3Object:
        """
        Get metadata about a single object in S3.
        
        This call makes a single `HEAD` request to S3 which can be
        much faster than downloading all data with `get`.
        
        Parameters
        ----------
        key : str, optional, default None
            Object to query. It can be an S3 url or a path suffix.
        return_missing : bool, default False
            If set to True, do not raise an exception for a missing key but
            return it as an `S3Object` with `.exists == False`.
        
        Returns
        -------
        S3Object
            An S3Object corresponding to the object requested. The object
            will have `.downloaded == False`.
        """
        ...
    def info_many(self, keys: typing.Iterable[str], return_missing: bool = False) -> typing.List[metaflow.plugins.datatools.s3.s3.S3Object]:
        """
        Get metadata about many objects in S3 in parallel.
        
        This call makes a single `HEAD` request to S3 which can be
        much faster than downloading all data with `get`.
        
        Parameters
        ----------
        keys : Iterable[str]
            Objects to query. Each key can be an S3 url or a path suffix.
        return_missing : bool, default False
            If set to True, do not raise an exception for a missing key but
            return it as an `S3Object` with `.exists == False`.
        
        Returns
        -------
        List[S3Object]
            A list of S3Objects corresponding to the paths requested. The
            objects will have `.downloaded == False`.
        """
        ...
    def get(self, key: typing.Union[str, metaflow.plugins.datatools.s3.s3.S3GetObject, None] = None, return_missing: bool = False, return_info: bool = True) -> metaflow.plugins.datatools.s3.s3.S3Object:
        """
        Get a single object from S3.
        
        Parameters
        ----------
        key : Union[str, S3GetObject], optional, default None
            Object to download. It can be an S3 url, a path suffix, or
            an S3GetObject that defines a range of data to download. If None, or
            not provided, gets the S3 root.
        return_missing : bool, default False
            If set to True, do not raise an exception for a missing key but
            return it as an `S3Object` with `.exists == False`.
        return_info : bool, default True
            If set to True, fetch the content-type and user metadata associated
            with the object at no extra cost, included for symmetry with `get_many`
        
        Returns
        -------
        S3Object
            An S3Object corresponding to the object requested.
        """
        ...
    def get_many(self, keys: typing.Iterable[typing.Union[str, metaflow.plugins.datatools.s3.s3.S3GetObject]], return_missing: bool = False, return_info: bool = True) -> typing.List[metaflow.plugins.datatools.s3.s3.S3Object]:
        """
        Get many objects from S3 in parallel.
        
        Parameters
        ----------
        keys : Iterable[Union[str, S3GetObject]]
            Objects to download. Each object can be an S3 url, a path suffix, or
            an S3GetObject that defines a range of data to download.
        return_missing : bool, default False
            If set to True, do not raise an exception for a missing key but
            return it as an `S3Object` with `.exists == False`.
        return_info : bool, default True
            If set to True, fetch the content-type and user metadata associated
            with the object at no extra cost, included for symmetry with `get_many`.
        
        Returns
        -------
        List[S3Object]
            S3Objects corresponding to the objects requested.
        """
        ...
    def get_recursive(self, keys: typing.Iterable[str], return_info: bool = False) -> typing.List[metaflow.plugins.datatools.s3.s3.S3Object]:
        """
        Get many objects from S3 recursively in parallel.
        
        Parameters
        ----------
        keys : Iterable[str]
            Prefixes to download recursively. Each prefix can be an S3 url or a path suffix
            which define the root prefix under which all objects are downloaded.
        return_info : bool, default False
            If set to True, fetch the content-type and user metadata associated
            with the object.
        
        Returns
        -------
        List[S3Object]
            S3Objects stored under the given prefixes.
        """
        ...
    def get_all(self, return_info: bool = False) -> typing.List[metaflow.plugins.datatools.s3.s3.S3Object]:
        """
        Get all objects under the prefix set in the `S3` constructor.
        
        This method requires that the `S3` object is initialized either with `run` or
        `s3root`.
        
        Parameters
        ----------
        return_info : bool, default False
            If set to True, fetch the content-type and user metadata associated
            with the object.
        
        Returns
        -------
        Iterable[S3Object]
            S3Objects stored under the main prefix.
        """
        ...
    def put(self, key: typing.Union[str, metaflow.plugins.datatools.s3.s3.S3PutObject], obj: typing.Union[io.RawIOBase, io.BufferedIOBase, str, bytes], overwrite: bool = True, content_type: typing.Optional[str] = None, metadata: typing.Optional[typing.Dict[str, str]] = None) -> str:
        """
        Upload a single object to S3.
        
        Parameters
        ----------
        key : Union[str, S3PutObject]
            Object path. It can be an S3 url or a path suffix.
        obj : PutValue
            An object to store in S3. Strings are converted to UTF-8 encoding.
        overwrite : bool, default True
            Overwrite the object if it exists. If set to False, the operation
            succeeds without uploading anything if the key already exists.
        content_type : str, optional, default None
            Optional MIME type for the object.
        metadata : Dict[str, str], optional, default None
            A JSON-encodable dictionary of additional headers to be stored
            as metadata with the object.
        
        Returns
        -------
        str
            URL of the object stored.
        """
        ...
    def put_many(self, key_objs: typing.List[typing.Union[typing.Tuple[str, typing.Union[io.RawIOBase, io.BufferedIOBase, str, bytes]], metaflow.plugins.datatools.s3.s3.S3PutObject]], overwrite: bool = True) -> typing.List[typing.Tuple[str, str]]:
        """
        Upload many objects to S3.
        
        Each object to be uploaded can be specified in two ways:
        
        1. As a `(key, obj)` tuple where `key` is a string specifying
           the path and `obj` is a string or a bytes object.
        
        2. As a `S3PutObject` which contains additional metadata to be
           stored with the object.
        
        Parameters
        ----------
        key_objs : List[Union[Tuple[str, PutValue], S3PutObject]]
            List of key-object pairs to upload.
        overwrite : bool, default True
            Overwrite the object if it exists. If set to False, the operation
            succeeds without uploading anything if the key already exists.
        
        Returns
        -------
        List[Tuple[str, str]]
            List of `(key, url)` pairs corresponding to the objects uploaded.
        """
        ...
    def put_files(self, key_paths: typing.List[typing.Union[typing.Tuple[str, typing.Union[io.RawIOBase, io.BufferedIOBase, str, bytes]], metaflow.plugins.datatools.s3.s3.S3PutObject]], overwrite: bool = True) -> typing.List[typing.Tuple[str, str]]:
        """
        Upload many local files to S3.
        
        Each file to be uploaded can be specified in two ways:
        
        1. As a `(key, path)` tuple where `key` is a string specifying
           the S3 path and `path` is the path to a local file.
        
        2. As a `S3PutObject` which contains additional metadata to be
           stored with the file.
        
        Parameters
        ----------
        key_paths :  List[Union[Tuple[str, PutValue], S3PutObject]]
            List of files to upload.
        overwrite : bool, default True
            Overwrite the object if it exists. If set to False, the operation
            succeeds without uploading anything if the key already exists.
        
        Returns
        -------
        List[Tuple[str, str]]
            List of `(key, url)` pairs corresponding to the files uploaded.
        """
        ...
    ...


##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.12.27.1+obcheckpoint(0.1.2);ob(v1)                               #
# Generated on 2024-11-13T19:05:29.397865                                        #
##################################################################################

from __future__ import annotations


class MetaflowException(Exception, metaclass=type):
    def __init__(self, msg = "", lineno = None):
        ...
    def __str__(self):
        ...
    ...

DATATOOLS_CLIENT_PARAMS: dict

DATATOOLS_SESSION_VARS: dict

S3_RETRY_COUNT: int

RETRY_WARNING_THRESHOLD: int

TEST_S3_RETRY: bool

TRANSIENT_RETRY_LINE_CONTENT: str

TRANSIENT_RETRY_START_LINE: str

def get_s3_client(s3_role_arn = None, s3_session_vars = None, s3_client_params = None):
    ...

def aws_retry(f):
    ...

def read_in_chunks(dst, src, src_sz, max_chunk_size):
    ...

def get_timestamp(dt):
    """
    Python2 compatible way to compute the timestamp (seconds since 1/1/1970)
    """
    ...


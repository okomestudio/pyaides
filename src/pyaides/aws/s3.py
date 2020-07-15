from logging import getLogger

import boto3
import botocore

log = getLogger(__name__)


_s3 = boto3.client("s3")


def bucket_exists(bucket: str) -> bool:
    """Test if an S3 bucket exists (or the caller has access permission).

    Args:
        bucket: The S3 bucket name.

    Returns:
        :obj:`True` if the object exists, :obj:`False` if not.
    """
    try:
        _s3.head_bucket(Bucket=bucket)
    except botocore.exceptions.ClientError:
        return False
    return True


def object_exists(bucket: str, key: str) -> bool:
    """Test if an S3 object with `key` exists in `bucket`.

    Args:
        bucket: The S3 bucket name.
        key: The name of the S3 object.

    Returns:
        :obj:`True` if the object exists, :obj:`False` if not.
    """
    try:
        _s3.head_object(Bucket=bucket, Key=key)
        exists = True
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "404":
            exists = False
        else:
            raise e
    return exists


def folder_exists(bucket: str, path: str) -> bool:
    """Test if an S3 folder with `path` exists in `bucket`.

    Args:
        bucket: The S3 bucket name.
        path: The name of the S3 folder.

    Returns:
        :obj:`True` if the folder exists, :obj:`False` if not.
    """
    if not path:
        raise ValueError("path cannot be empty")
    if not path.endswith("/"):
        path += "/"
    prefixes = _s3.list_objects_v2(Bucket=bucket, Prefix=path, MaxKeys=1).get(
        "Contents"
    )
    return bool(prefixes)

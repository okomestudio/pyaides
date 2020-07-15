import random
import string

import pytest
from moto import mock_s3


@pytest.fixture(scope="module")
def mock_aws_services():
    mock = mock_s3()
    mock.start()
    yield
    mock.stop()


def random_chars(n=12):
    return "".join(
        random.choice(string.ascii_lowercase + string.digits) for _ in range(n)
    )


@pytest.fixture(scope="class")
def bucket(request, mock_aws_services):
    import boto3
    from pyaides.aws import s3

    cls = request.cls

    bucket = "pyaidestest-" + random_chars()

    boto3_cli = boto3.client("s3", region_name="us-east-1")
    boto3_cli.create_bucket(Bucket=bucket)
    for key in ("1", "2", "a/1", "a/2", "b/c/1", "b/c/2"):
        boto3_cli.put_object(Bucket=bucket, Key=key)

    cls.bucket = bucket
    cls.cli = boto3_cli
    cls.s3 = s3

    yield

    resp = boto3_cli.list_objects_v2(Bucket=bucket)
    boto3_cli.delete_objects(
        Bucket=bucket, Delete={"Objects": [{"Key": o["Key"]} for o in resp["Contents"]]}
    )
    boto3_cli.delete_bucket(Bucket=bucket)


@pytest.mark.usefixtures("bucket")
class TestS3Integration:
    def test_bucket_exists(self):
        assert self.s3.bucket_exists(self.bucket) is True

    def test_bucket_does_not_exist(self):
        assert self.s3.bucket_exists(self.bucket + "nonexisting") is False

    @pytest.mark.parametrize("key", ["1", "2", "a/1", "a/2", "b/c/1", "b/c/2"])
    def test_object_exists(self, key):
        assert self.s3.object_exists(self.bucket, key) is True

    @pytest.mark.parametrize("key", ["asejfi", "1/23"])
    def test_object_does_not_exist(self, key):
        assert self.s3.object_exists(self.bucket, key) is False

    @pytest.mark.parametrize("path", ["a", "b", "b/c"])
    def test_folder_exists(self, path):
        assert self.s3.folder_exists(self.bucket, path) is True

    @pytest.mark.parametrize("path", ["af", "bs", "b/c/1"])
    def test_folder_does_not_exist(self, path):
        assert self.s3.folder_exists(self.bucket, path) is False

    def test_folder_exists_with_empty_path(self):
        with pytest.raises(ValueError):
            self.s3.folder_exists(self.bucket, "")

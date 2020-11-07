from unittest.mock import patch

import pytest
from moto import mock_sqs

from pyaides.aws.sqs.sqs import CLI
from pyaides.aws.sqs.sqs import queue_urls_by_prefix


@pytest.fixture(scope="module")
def mock_aws_services():
    mock = mock_sqs()
    mock.start()
    yield
    mock.stop()


@pytest.fixture
def cli():
    with patch("pyaides.aws.sqs.sqs.cli") as cli:
        yield cli


class TestQueueUrlsByPrefix:
    def test_with_existing_queues(self, cli):
        prefix = "prefix"
        queue_urls = ["a", "b", "c"]
        # with patch("pyaides.aws.sqs.sqs.cli") as cli:
        cli.list_queues.return_value = {"QueueUrls": queue_urls}
        result = list(queue_urls_by_prefix(prefix))
        cli.list_queues.assert_called_with(QueueNamePrefix=prefix, MaxResults=1000)
        assert result == queue_urls

    def test_with_nonexisting_queues(self, cli):
        prefix = "prefix"
        # with patch("pyaides.aws.sqs.sqs.cli") as cli:
        cli.list_queues.return_value = {}
        result = list(queue_urls_by_prefix(prefix))
        cli.list_queues.assert_called_with(QueueNamePrefix=prefix, MaxResults=1000)
        assert result == []


class TestCLIDeleteQueues:
    def test_no_matching_queues(self, cli, capsys):
        with patch("pyaides.aws.sqs.sqs.queue_urls_by_prefix") as func:
            func.return_value = []
            CLI.delete_queues(["prefix"])
        captured = capsys.readouterr()
        assert "No queues match" in captured.out

    def test_matching_queues(self, cli, capsys):
        queues = ["a", "b", "c"]
        prefix = "prefix"
        with patch("pyaides.aws.sqs.sqs.queue_urls_by_prefix") as func, patch(
            "pyaides.aws.sqs.sqs.input"
        ) as input:
            input.return_value = "y"
            func.return_value = queues

            CLI.delete_queues([prefix])

            func.assert_called_once_with(prefix)

            for c, q in zip(cli.delete_queue.call_args_list, queues):
                args, kwargs = c
                assert kwargs["QueueUrl"] == q

        captured = capsys.readouterr()
        assert "a\nb\nc\n" in captured.out

    def test_already_deleted(self, cli, capsys):
        queues = ["a"]
        with patch("pyaides.aws.sqs.sqs.queue_urls_by_prefix") as func, patch(
            "pyaides.aws.sqs.sqs.input"
        ) as input:
            input.return_value = "y"
            func.return_value = queues

            cli.delete_queue.side_effect = Exception()
            cli.exceptions.QueueDoesNotExist = Exception

            CLI.delete_queues(["prefix"])

        captured = capsys.readouterr()
        assert f"{queues[0]} is already deleted" in captured.out

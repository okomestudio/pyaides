import argparse
from logging import getLogger
from typing import Generator

import boto3

log = getLogger(__name__)

cli = boto3.client("sqs")


def queue_urls_by_prefix(
    prefix: str, max_results: int = 1000
) -> Generator[str, None, None]:
    params = {"QueueNamePrefix": prefix, "MaxResults": max_results}
    token = True
    while token:
        resp = cli.list_queues(**params)
        if "QueueUrls" not in resp:
            break

        for queue_url in resp["QueueUrls"]:
            yield queue_url

        token = resp.get("NextToken")
        params["NextToken"] = token


class CLI:
    @classmethod
    def delete_queues(cls, args=None):
        p = argparse.ArgumentParser(description="Delete SQS queues by name prefix.")
        p.add_argument("prefix", type=str, help="Queue name prefix")
        args = p.parse_args(args or None)

        prefix = args.prefix

        queue_urls = list(queue_urls_by_prefix(prefix))
        if not queue_urls:
            print("No queues match the prefix")
            return

        for queue_url in queue_urls:
            print(queue_url)

        val = input("Delete these queues? (y/N) ")

        if val in ("y", "Y"):
            for queue_url in queue_urls:
                try:
                    cli.delete_queue(QueueUrl=queue_url)
                except cli.exceptions.QueueDoesNotExist:
                    print(f"{queue_url} is already deleted")

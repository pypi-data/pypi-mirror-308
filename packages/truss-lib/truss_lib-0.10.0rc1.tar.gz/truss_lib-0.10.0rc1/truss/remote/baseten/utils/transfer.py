import base64
import contextlib
import json
import os
from typing import TYPE_CHECKING, Optional

import boto3
from boto3.s3.transfer import TransferConfig

if TYPE_CHECKING:
    from rich import progress


def base64_encoded_json_str(obj):
    return base64.b64encode(str.encode(json.dumps(obj))).decode("utf-8")


def multipart_upload_boto3(
    file_path,
    bucket_name: str,
    key: str,
    credentials: dict,
    progress_bar: Optional["progress.Progress"],
) -> None:
    s3_resource = boto3.resource("s3", **credentials)
    filesize = os.stat(file_path).st_size

    progress_context = progress_bar if progress_bar else contextlib.nullcontext()
    task_id = (
        progress_bar.add_task("[cyan]Uploading...", total=filesize)
        if progress_bar
        else None
    )

    def callback(bytes_transferred):
        if progress_bar:
            progress_bar.update(task_id, advance=bytes_transferred)

    with progress_context:
        s3_resource.Object(bucket_name, key).upload_file(
            file_path,
            Config=TransferConfig(
                max_concurrency=10,
                use_threads=True,
            ),
            Callback=callback,
        )

from google.cloud import storage
import pytest
import os


@pytest.fixture(scope="function")
def empty_bucket_and_project():
    """
    Fixture for setting up and tearing down a clean state for a testing GCP bucket.

    This fixture connects to the specified GCP project and source bucket using environment variables,
    deletes all blobs in the source bucket before the test, yields the bucket and project to the test function,
    and finally cleans up by deleting all blobs in the source bucket after the test.

    Yields:
        Tuple[storage.bucket.Bucket, str]: A tuple containing the GCP bucket and project name where the bucket is
                                           allocated.
    """
    storage_client = storage.Client(os.environ["PROJECT"])
    bucket = storage_client.bucket(os.environ["SOURCE_BUCKET"])

    for blob in bucket.list_blobs():
        blob.delete()

    yield bucket, storage_client.project

    for blob in bucket.list_blobs():
        blob.delete()

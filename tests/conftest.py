from google.cloud import storage
import pytest
import os


@pytest.fixture(scope="function")
def empty_bucket_and_project():
    storage_client = storage.Client(os.environ['PROJECT'])
    bucket = storage_client.bucket(os.environ['SOURCE_BUCKET'])

    for blob in bucket.list_blobs():
        blob.delete()

    yield bucket, storage_client.project

    for blob in bucket.list_blobs():
        blob.delete()

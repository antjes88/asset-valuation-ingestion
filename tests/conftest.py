from google.cloud import storage
from google.cloud.storage.bucket import Bucket
import pytest
import os
from typing import Tuple, List, Generator, Optional
import warnings

from src import destination_repository, model
from tests.data.asset_valuations import ASSET_VALUATIONS_2018
from src.utils.gcp_clients import create_bigquery_client

warnings.filterwarnings("ignore", category=UserWarning)


@pytest.fixture(scope="session")
def bq_repository() -> destination_repository.BiqQueryDestinationRepository:

    bq_repository = destination_repository.BiqQueryDestinationRepository(
        bigquery_client=create_bigquery_client(os.environ.get("PROJECT"))
    )
    bq_repository.asset_valuations_destination = (
        os.environ["DATASET"] + "." + os.environ["DESTINATION_TABLE"]
    )

    return bq_repository


@pytest.fixture(scope="function")
def repository_with_asset_valuations(
    bq_repository: destination_repository.BiqQueryDestinationRepository,
) -> Generator[
    Tuple[
        destination_repository.BiqQueryDestinationRepository, List[model.AssetValuation]
    ],
    None,
    None,
]:

    bq_repository.load_asset_valuations(ASSET_VALUATIONS_2018)

    yield bq_repository, ASSET_VALUATIONS_2018

    bq_repository.bigquery_client.delete_table(
        os.environ["DATASET"] + "." + os.environ["DESTINATION_TABLE"]
    )


@pytest.fixture(scope="function")
def empty_bucket_and_project() -> Generator[
    Tuple[Bucket, Optional[str]],
    None,
    None,
]:

    def delete_blobs(bucket: Bucket) -> None:
        for blob in bucket.list_blobs():
            blob.delete()

    storage_client = storage.Client(os.environ["PROJECT"])
    bucket: Bucket = storage_client.bucket(os.environ["SOURCE_BUCKET"])

    delete_blobs(bucket)

    yield bucket, storage_client.project

    delete_blobs(bucket)

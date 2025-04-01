import click
import os
from src import source_repository, destination_repository, services
from src.utils.logs import default_module_logger
from src.utils.gcp_clients import create_storage_client, create_bigquery_client

logger = default_module_logger(__file__)


@click.command()
@click.option("--bucket_name", "-bn", required=True, help="Name of the GCP bucket")
@click.option(
    "--file_path", "-fp", required=True, help="Path of the file in the bucket"
)
def load_gcp_file(bucket_name: str, file_path: str):
    """
    Loads a file from a specified Google Cloud Storage bucket and processes it
    through the asset valuation pipeline.

    Args:
        bucket_name (str): The name of the Google Cloud Storage bucket.
        file_path (str): The path to the file within the bucket.
    """
    logger.info(f"Loading file '{file_path}' from bucket '{bucket_name}'")
    file = source_repository.GcpBucketFileSource(
        file_path,
        bucket_name,
        storage_client=create_storage_client(os.environ.get("PROJECT")),
    )
    bigquery = destination_repository.BiqQueryDestinationRepository(
        bigquery_client=create_bigquery_client(os.environ.get("PROJECT"))
    )

    services.asset_valuation_pipeline(file, bigquery)


@click.command()
@click.option(
    "--file_path", "-fp", required=True, help="Path of the file in the local machine"
)
def load_local_file(file_path: str):
    """
    Loads a local file and processes it through the asset valuation pipeline.
    This function initializes a local file source and a BigQuery destination
    repository, then processes the file using the asset valuation pipeline.

    Args:
        file_path (str): The path to the local file to be loaded.
    """
    logger.info(f"Loading file '{file_path}' from local machine")
    file = source_repository.LocalFileSource(file_path)
    bigquery = destination_repository.BiqQueryDestinationRepository(
        bigquery_client=create_bigquery_client(os.environ.get("PROJECT"))
    )

    services.asset_valuation_pipeline(file, bigquery)


@click.command()
@click.option("--bucket_name", "-bn", required=True, help="Name of the GCP bucket")
def load_all_files_from_bucket(bucket_name: str):
    """
    Loads all files from a specified Google Cloud Storage bucket and processes them
    using the asset valuation pipeline.
    This function retrieves all blob names from the specified bucket, iterates through
    each file, and processes it using the asset valuation pipeline. If an error occurs
    while processing a file, it logs the error and continues with the next file.

    Args:
        bucket_name (str): The name of the Google Cloud Storage bucket to load files from.
    Raises:
        Exception: Logs any exceptions that occur during file processing.
    """

    logger.info(f"Listing all files from bucket '{bucket_name}'")
    bigquery_client = create_bigquery_client(os.environ.get("PROJECT"))
    storage_client = create_storage_client(os.environ.get("PROJECT"))
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs()
    blob_names = [blob.name for blob in blobs]

    logger.info(f"Loading all files from bucket '{bucket_name}'")
    for blob_name in blob_names:
        try:
            logger.info(f"Loading file '{blob_name}' from bucket '{bucket_name}'")
            file = source_repository.GcpBucketFileSource(
                blob_name,
                bucket_name,
                storage_client=storage_client,
            )
            bigquery = destination_repository.BiqQueryDestinationRepository(
                bigquery_client=bigquery_client
            )

            services.asset_valuation_pipeline(file, bigquery)
        except Exception as e:
            logger.error(f"Failed to load file '{blob_name}': {e}")

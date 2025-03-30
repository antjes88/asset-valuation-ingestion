import click
import os
from src import source_repository, destination_repository, services
from src.entrypoints.cli.utils import GcsClient
from src.logs import default_module_logger

logger = default_module_logger(__file__)


@click.command()
@click.option("--bucket_name", "-bn", required=True, help="Name of the GCP bucket")
@click.option(
    "--file_path", "-fp", required=True, help="Path of the file in the bucket"
)
def load_gcp_file(bucket_name: str, file_path: str):
    logger.info(f"Loading file '{file_path}' from bucket '{bucket_name}'")
    file = source_repository.GcpBucketFileSource(
        file_path, bucket_name, project_name=os.environ.get("PROJECT")
    )
    bigquery = destination_repository.BiqQueryDestinationRepository(
        project=os.environ.get("PROJECT")
    )

    services.asset_valuation_pipeline(file, bigquery)


@click.command()
@click.option(
    "--file_path", "-fp", required=True, help="Path of the file in the local machine"
)
def load_local_file(file_path: str):
    logger.info(f"Loading file '{file_path}' from local machine")
    file = source_repository.LocalFileSource(file_path)
    bigquery = destination_repository.BiqQueryDestinationRepository(
        project=os.environ.get("PROJECT")
    )

    services.asset_valuation_pipeline(file, bigquery)


@click.command()
@click.option("--bucket_name", "-bn", required=True, help="Name of the GCP bucket")
def load_all_files_from_bucket(bucket_name: str):
    logger.info(f"Loading all files from bucket '{bucket_name}'")
    gcs_client = GcsClient(os.environ["PROJECT"])
    blob_names = gcs_client.list_blob_names_in_bucket(bucket_name)
    for blob_name in blob_names:
        try:
            logger.info(f"Loading file '{blob_name}' from bucket '{bucket_name}'")
            file = source_repository.GcpBucketFileSource(
                blob_name, bucket_name, project_name=os.environ.get("PROJECT")
            )
            bigquery = destination_repository.BiqQueryDestinationRepository(
                project=os.environ.get("PROJECT")
            )

            services.asset_valuation_pipeline(file, bigquery)
        except Exception as e:
            logger.error(f"Failed to load file '{blob_name}': {e}")

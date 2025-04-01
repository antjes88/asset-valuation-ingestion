from google.cloud import storage
from google.cloud import bigquery
from typing import Optional


def create_storage_client(project_id: Optional[str] = None) -> storage.Client:
    """Creates and returns a Google Cloud Storage client.

    Args:
        project_id (str, optional): The Google Cloud project ID.
    Returns:
        google.cloud.storage.Client: A client for interacting with Google Cloud Storage.
    """
    return storage.Client(project=project_id)


def create_bigquery_client(project_id: Optional[str] = None) -> bigquery.Client:
    """Creates and returns a Google BigQuery client.

    Args:
        project_id (str, optional): The Google Cloud project ID.
    Returns:
        google.cloud.bigquery.Client: A client for interacting with Google BigQuery.
    """
    return bigquery.Client(project=project_id)

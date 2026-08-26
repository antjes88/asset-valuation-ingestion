from google.cloud import storage
from google.cloud import bigquery
from typing import Optional


def create_storage_client(project_id: Optional[str] = None) -> storage.Client:

    return storage.Client(project=project_id)


def create_bigquery_client(project_id: Optional[str] = None) -> bigquery.Client:

    return bigquery.Client(project=project_id)

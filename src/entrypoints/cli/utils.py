import os
from dotenv import load_dotenv
from typing import Optional, List
from google.cloud import storage


def env_var_loader(file_name: str, file_path: Optional[str] = None):
    """
    Load environment variables from a specified file using python-dotenv.

    Args:
        file_name (str): The name of the environment file.
        file_path (str, optional): The path to the directory containing the environment file.
    """
    if file_path:
        env_path = os.path.join(file_path, file_name)
    else:
        wd = os.getcwd()
        env_path = os.path.join(wd, file_name)

    if os.path.isfile(env_path):
        load_dotenv(dotenv_path=env_path)


class GcsClient:
    """
    A client for interacting with Google Cloud Storage (GCS).
    This class provides methods to interact with GCS, such as listing blob names
    in a specified bucket.

    Args:
        project (str): The GCP project ID.
    Attributes:
        client (google.cloud.storage.Client): The GCS client instance used to interact
            with Google Cloud Storage.
    Methods:
        list_blob_names_in_bucket(bucket_name: str) -> List[str]:
            Lists all the blob names in the specified GCP bucket.
    """

    def __init__(self, project: str):
        self.client = storage.Client(project=project)

    def list_blob_names_in_bucket(self, bucket_name: str) -> List[str]:
        """
        Lists all blob names in the specified GCP bucket.

        Args:
            bucket_name (str): The name of the GCP bucket.
        Returns:
            List[str]: A list of blob names present in the specified bucket.
        """
        bucket = self.client.bucket(bucket_name)
        blobs = bucket.list_blobs()

        return [blob.name for blob in blobs]

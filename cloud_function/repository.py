from abc import ABC, abstractmethod
from google.cloud import storage
import model
import csv
import datetime as dt
from typing import IO


class FileAbstract(ABC):
    """
    An abstract base class representing a generic file for retrieving asset valuations.

    Arguments:
        file_path (str): The path to the file.
    Attributes:
        file_path (str): The path to the file.
        file_format (str): The format of the file, extracted from the file extension.
        file_type (str): The type of the file, derived from the file name.
    Methods:
        _open():
            Abstract method to open the file. Must be implemented by subclasses.
        _get_asset_valuations_from_generic_source() -> List[model.AssetValuation]:
            Internal method to parse asset valuations from a generic source file.
        get_asset_valuations() -> List[model.AssetValuation]:
            Retrieves asset valuations from the file. Implemented by calling internal methods
            based on the file type.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file_format = file_path.split(".")[-1]
        self.file_type = file_path.split("/")[-1].split("_")[0].lower()

    @abstractmethod
    def _open(self) -> IO:
        """
        Abstract method to open the file. Must be implemented by subclasses.
        """
        raise NotImplementedError

    def _get_asset_valuations_from_generic_source(self) -> list[model.AssetValuation]:
        """
        Internal method to parse asset valuations from a generic source file.
        Generic source file must be a CSV and must contain at least columns:
            date: must follow next pattern 'YYYY-MM-DD'
            value: numerical valuation of asset
            product_name: name of asset

        Returns:
            List[model.AssetValuation]: A list of AssetValuation instances.
        """
        # todo: include check for file format
        asset_valuations = []
        with self._open() as f:
            s_reader = csv.reader(f)

            for row_number, row in enumerate(s_reader):
                if row_number == 0:
                    column_names = row
                    # todo: include check to columns
                else:
                    dictify_row = dict(zip(column_names, row))
                    asset_valuations.append(
                        model.AssetValuation(
                            dt.datetime.strptime(
                                dictify_row["date"], "%Y-%m-%d"
                            ).date(),
                            float(dictify_row["value"]),
                            dictify_row["product_name"],
                        )
                    )

        return asset_valuations

    def get_asset_valuations(self) -> list[model.AssetValuation]:
        """
        Factory method to retrieves asset valuations from the file. Implemented by calling internal methods
        based on the file type.

        Returns:
            List[model.AssetValuation]: A list of AssetValuation instances.

        Raises:
            Exception: Raised if the file type is not recognized.
        """
        if self.file_type == "generic":
            return self._get_asset_valuations_from_generic_source()
        else:
            raise Exception()  # todo: create error specific for table not set


class LocalFile(FileAbstract):
    """
    A concrete implementation of FileAbstract for working with local files.
    This class provides methods for opening and retrieving asset valuations from a local file.

    Arguments:
        file_path (str): The path to the file.
    Attributes:
        file_path (str): The path to the local file.
        file_format (str): The format of the file, extracted from the file extension.
        file_type (str): The type of the file, derived from the file name.
    Methods:
        _open():
            Opens the local file and returns a file object.
        _get_asset_valuations_from_generic_source() -> List[model.AssetValuation]:
            Internal method to parse asset valuations from a generic source file.
        get_asset_valuations() -> List[model.AssetValuation]:
            Retrieves asset valuations from the file. Implemented by calling internal methods
            based on the file type.
    """

    def _open(self) -> IO:
        """
        Opens the local file and returns a file object.

        Returns:
            IO: An open file object.
        """
        return open(self.file_path)


class GcpBucketFile(FileAbstract):
    """
    A concrete implementation of FileAbstract for working with GCP Bucket Blob.
    This class provides methods for opening and retrieving asset valuations from a local file.

    Args:
        file_path (str): The path to the file in the GCP bucket.
        bucket_name (str): The name of the GCP bucket.
        project_name (str, optional): The name of the GCP project. Defaults to None.
    Attributes:
        file_path (str): The path to the local file.
        file_format (str): The format of the file, extracted from the file extension.
        file_type (str): The type of the file, derived from the file name.
        bucket_name (str): The name of the GCP bucket.
        project_name (str, optional): The name of the GCP project. Defaults to None.
        bucket(storage.bucket.Bucket): The GCP Bucket client.
    Methods:
        _open():
            Opens the local file and returns a file object.
        _get_asset_valuations_from_generic_source() -> List[model.AssetValuation]:
            Internal method to parse asset valuations from a generic source file.
        get_asset_valuations() -> List[model.AssetValuation]:
            Retrieves asset valuations from the file. Implemented by calling internal methods
            based on the file type.
        _get_bucket() -> storage.bucket.Bucket:
            Retrieves the GCP bucket.
    """

    def __init__(self, file_path: str, bucket_name: str, project_name: str = None):
        super().__init__(file_path)
        self.bucket_name = bucket_name
        self.project_name = project_name
        self.bucket = self._get_bucket()

    def _get_bucket(self) -> storage.bucket.Bucket:
        """
        Retrieves the GCP bucket.

        Returns:
            storage.bucket.Bucket: The GCP bucket.
        """
        storage_client = storage.Client(self.project_name)
        bucket = storage_client.bucket(self.bucket_name)

        return bucket

    def _open(self) -> IO:
        """
        Opens the file in the GCP bucket and returns a file-like object.

        Returns:
            IO: An open file-like object.
        """
        blob = self.bucket.blob(self.file_path)

        return blob.open()

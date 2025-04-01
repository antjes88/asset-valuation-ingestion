from abc import ABC, abstractmethod
from google.cloud import storage
from google.cloud.storage import Bucket
import csv
import datetime as dt
from typing import IO, Any, List, Optional

from src import model, custom_errors
from src.utils.gcp_clients import create_bigquery_client, create_storage_client


class AbstractSourceRepository(ABC):
    """
    An abstract base class for repository interfaces that define methods
    to extract data from source repositories.

    Methods:
        get_asset_valuations() -> List[model.AssetValuation]:
            Abstract method to retrieve asset valuations from source.
    """

    @abstractmethod
    def get_asset_valuations(self) -> list[model.AssetValuation]:
        """
        Abstract method to retrieve asset valuations from source.

        Returns:
            List[model.AssetValuation]: A list of AssetValuation instances.
        """
        raise NotImplementedError


class FileSourceAbstract(AbstractSourceRepository, ABC):
    """
    An abstract base class representing a generic file from which to retrieve asset valuations.

    Arguments:
        file_path (str): The path to the file.
    Attributes:
        file_path (str): The path to the file.
        file_format (str): The format of the file, extracted from the file extension.
        file_type (str): The type of the file, derived from the file name.
    Methods:
        _open() -> IO[Any]:
            Abstract method to open the file. Must be implemented by subclasses.
        _get_asset_valuations_from_generic_source() -> List[model.AssetValuation]:
            Internal method to parse asset valuations from a generic source file.
        _get_asset_valuations_from_hl_source(self) -> list[model.AssetValuation]:
            Internal method to parse asset valuations from HL source file.
        get_asset_valuations() -> List[model.AssetValuation]:
            Retrieves asset valuations from the file. Implemented by calling internal methods
            based on the file type.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file_format = file_path.split(".")[-1]
        self.file_type = file_path.split("/")[-1].split("_")[0].lower()

    @abstractmethod
    def _open(self) -> IO[Any]:
        """
        Abstract method to open the file. Must be implemented by subclasses.
        """
        raise NotImplementedError

    def _get_asset_valuations_from_generic_source(self) -> List[model.AssetValuation]:
        """
        Internal method to parse asset valuations from a generic source file.
        It checks for file format and headers.
        Generic source file must be a CSV and must contain at least columns:
            date: must follow next pattern 'YYYY-MM-DD'
            value: numerical valuation of asset
            product_name: name of asset
        An example can be found at tests/data/generic_2023_11_24.csv.

        Returns:
            List[model.AssetValuation]: A list of AssetValuation instances.
        Raises:
            custom_errors.FileFormatError: Raised if the format of the file is not a csv
            custom_errors.HeaderNotMatchError: Raised if file headers are not
                                               ["date", "product_name", "value"]
        """
        if self.file_format != "csv":
            raise custom_errors.FileFormatError(self.file_path, self.file_format, "csv")

        asset_valuations: List[model.AssetValuation] = []
        with self._open() as f:
            s_reader = csv.reader(f)

            for row_number, row in enumerate(s_reader):
                if row_number == 0:
                    if [str(elem).lower() for elem in row] != [
                        "product_name",
                        "date",
                        "value",
                    ]:
                        raise custom_errors.HeaderNotMatchError(
                            self.file_path,
                            str([str(elem).lower() for elem in row]).replace("'", ""),
                            "[date, product_name, value]",
                        )

                else:
                    dictify_row = dict(zip(["product_name", "date", "value"], row))
                    asset_valuations.append(
                        model.AssetValuation(
                            date=dt.datetime.strptime(
                                dictify_row["date"], "%Y-%m-%d"
                            ).date(),
                            value=float(dictify_row["value"]),
                            product_name=dictify_row["product_name"],
                            source_file=self.file_path,
                        )
                    )

        return asset_valuations

    def _get_asset_valuations_from_hl_source(self) -> list[model.AssetValuation]:
        """
        Internal method to parse asset valuations from HL source file. It checks for file format.
        HL file format sample can be found at tests/data/hl_2023_11_24.csv.

        Returns:
            List[model.AssetValuation]: A list of AssetValuation instances.
        Raises:
            custom_errors.FileFormatError: Raised if the format of the file is not a csv
        """
        if self.file_format != "csv":
            raise custom_errors.FileFormatError(self.file_path, self.file_format, "csv")

        asset_valuations: List[model.AssetValuation] = []
        with self._open() as f:
            s_reader = csv.reader(f)

            created_date, variable_name, all_extracted, to_accounts = (
                None,
                "spreadsheet created at",
                False,
                False,
            )
            for row in s_reader:

                if all_extracted or len(row) == 0:
                    pass

                elif row[0].strip().lower() == variable_name:
                    created_date = dt.datetime.strptime(row[1][:10], "%d-%m-%Y").date()

                elif row[0].strip().lower() == "total cash:":
                    asset_valuations.append(
                        model.AssetValuation(
                            date=created_date if created_date else dt.date(1990, 1, 1),
                            value=float(row[1].replace(",", "")),
                            product_name="HL - Cash",
                            source_file=self.file_path,
                        )
                    )

                elif row[0] == "Code":
                    to_accounts = True

                elif to_accounts and row[0] != "":
                    asset_valuations.append(
                        model.AssetValuation(
                            date=created_date if created_date else dt.date(1990, 1, 1),
                            value=float(row[4].replace(",", "")),
                            product_name=row[1],
                            source_file=self.file_path,
                        )
                    )

                elif row[0] == "":
                    all_extracted = True

            if created_date is None:
                raise ValueError(
                    f"Expected value '{variable_name}' not found in file: {self.file_path}."
                )

        return asset_valuations

    def get_asset_valuations(self) -> list[model.AssetValuation]:
        """
        Factory method to retrieves asset valuations from the file. Implemented by calling internal methods
        based on the file type.

        Returns:
            List[model.AssetValuation]: A list of AssetValuation instances.
        Raises:
            custom_errors.FileTypeNotImplementedError: Raised if the file type is not recognized.
        """
        if self.file_type == "generic":
            return self._get_asset_valuations_from_generic_source()
        elif self.file_type == "hl":
            return self._get_asset_valuations_from_hl_source()
        else:
            raise custom_errors.FileTypeNotImplementedError(self.file_path)


class LocalFileSource(FileSourceAbstract):
    """
    A concrete implementation of FileAbstract to work with local files.
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
        _get_asset_valuations_from_hl_source(self) -> list[model.AssetValuation]:
            Internal method to parse asset valuations from HL source file.
        get_asset_valuations() -> List[model.AssetValuation]:
            Retrieves asset valuations from the file. Implemented by calling internal methods
            based on the file type.
    """

    def _open(self) -> IO[Any]:
        """
        Opens the local file and returns a file object.

        Returns:
            IO: An open file object.
        """
        return open(self.file_path, encoding="utf-8")


class GcpBucketFileSource(FileSourceAbstract):
    """
    A concrete implementation of FileAbstract to work with GCP Bucket Blob.
    This class provides methods for opening and retrieving asset valuations from a GCP Blob.

    Args:
        file_path (str): The path to the file in the GCP bucket.
        bucket_name (str): The name of the GCP bucket.
        storage_client (storage.Client): A client for interacting with Google Cloud Storage.
    Attributes:
        file_path (str): The path to the local file.
        file_format (str): The format of the file, extracted from the file extension.
        file_type (str): The type of the file, derived from the file name.
        storage_client (storage.Client): A client for interacting with Google Cloud Storage.
        bucket (Bucket): The GCP Bucket client.
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

    def __init__(
        self, file_path: str, bucket_name: str, storage_client: storage.Client
    ):
        super().__init__(file_path)
        self.storage_client = storage_client
        self.bucket: Bucket = self._get_bucket(bucket_name)

    def _get_bucket(self, bucket_name: str) -> Bucket:
        """
        Retrieves the GCP bucket.

        Attributes:
            bucket_name (str): The name of the GCP bucket.
        Returns:
            storage.bucket.Bucket: The GCP bucket.
        """
        bucket: Bucket = self.storage_client.bucket(bucket_name)

        return bucket

    def _open(self) -> IO[Any]:
        """
        Opens the file in the GCP bucket and returns a file-like object.

        Returns:
            IO: An open file-like object.
        """
        blob = self.bucket.blob(self.file_path)

        return blob.open(encoding="utf-8")  # type: ignore

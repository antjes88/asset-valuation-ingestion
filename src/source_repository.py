from abc import ABC, abstractmethod
from google.cloud import storage
from google.cloud.storage import Bucket
import csv
import datetime as dt
from typing import IO, Any, List

from src import model, custom_errors


class AbstractSourceRepository(ABC):

    @abstractmethod
    def get_asset_valuations(self) -> list[model.AssetValuation]:

        raise NotImplementedError


class FileSourceAbstract(AbstractSourceRepository, ABC):

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file_format = file_path.split(".")[-1]
        self.file_type = file_path.split("/")[-1].split("_")[0].lower()

    @abstractmethod
    def _open(self) -> IO[Any]:

        raise NotImplementedError

    def _get_asset_valuations_from_generic_source(self) -> List[model.AssetValuation]:

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

        if self.file_type == "generic":
            return self._get_asset_valuations_from_generic_source()
        elif self.file_type == "hl":
            return self._get_asset_valuations_from_hl_source()
        else:
            raise custom_errors.FileTypeNotImplementedError(self.file_path)


class LocalFileSource(FileSourceAbstract):

    def _open(self) -> IO[Any]:
        """
        Opens the local file and returns a file object.

        Returns:
            IO: An open file object.
        """
        return open(self.file_path, encoding="utf-8")


class GcpBucketFileSource(FileSourceAbstract):

    def __init__(
        self, file_path: str, bucket_name: str, storage_client: storage.Client
    ):
        super().__init__(file_path)
        self.storage_client = storage_client
        self.bucket: Bucket = self._get_bucket(bucket_name)

    def _get_bucket(self, bucket_name: str) -> Bucket:

        bucket: Bucket = self.storage_client.bucket(bucket_name)

        return bucket

    def _open(self) -> IO[Any]:

        blob = self.bucket.blob(self.file_path)

        return blob.open(encoding="utf-8")  # type: ignore

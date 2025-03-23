from abc import ABC, abstractmethod
from typing import Optional, List, Any, Dict
from google.cloud import bigquery

from src import model


class AbstractDestinationRepository(ABC):
    """
    An abstract base class for repository interfaces that define methods
    to load data into destination repositories.

    Methods:
        load_asset_valuations (List[model.AssetValuation]):
            List of AssetValuation instances to be loaded into the repository.
    """

    @abstractmethod
    def load_asset_valuations(
        self, asset_valuations: list[model.AssetValuation]
    ) -> None:
        """
        Abstract method to load Asset Valuations into the repository.

        Args:
            asset_valuations (List[model.AssetValuation]): List of AssetValuation instances
                                                           to be loaded into the repository.
        """
        raise NotImplementedError


class BiqQueryRepository(AbstractDestinationRepository):
    """
    Concrete implementation of the AbstractDestinationRepository for interacting with Google BigQuery.
    This repository class is designed to load asset valuations data into Google BigQuery.

    Args:
        project (str, optional): The Google Cloud project ID. Defaults to None.
    Attributes:
        client (google.cloud.bigquery.Client): The BigQuery client instance.
        asset_valuations_destination (str): The destination table for asset valuations in BigQuery.
    Methods:
        load_asset_valuations(asset_valuations: list[model.AssetValuation]):
            Load asset valuations into BigQuery table indicated by attribute asset_valuations_destination.
    """

    def __init__(self, project: Optional[str] = None):
        self.client = bigquery.Client(project=project)
        self.asset_valuations_destination = "raw.asset_valuations_v2"

    def load_asset_valuations(self, asset_valuations: list[model.AssetValuation]):
        """
        Load Asset Valuations into BigQuery table indicated by attribute asset_valuations_destination.

        Args:
            asset_valuations (List[model.AssetValuation]): List of AssetValuation instances to be loaded
                into BigQuery.
        """

        dictify: List[Dict[str, Any]] = [
            {
                "date": asset_valuation.date.strftime("%Y-%m-%d"),
                "value": asset_valuation.value,
                "product_name": asset_valuation.product_name,
                "__source_file__": asset_valuation.source_file,
                "__creation_date__": asset_valuation.creation_date.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
            }
            for asset_valuation in asset_valuations
        ]
        job_config = bigquery.LoadJobConfig(
            create_disposition=bigquery.CreateDisposition.CREATE_IF_NEEDED,
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
            source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        )
        load_job = self.client.load_table_from_json(
            dictify, self.asset_valuations_destination, job_config=job_config
        )
        load_job.result()

from abc import ABC, abstractmethod
from google.cloud import bigquery
import model


class AbstractRepository(ABC):
    """
    An abstract base class for repository interfaces that define methods to interact with a data source.
    Subclasses of AbstractRepository are expected to implement these methods to handle data storage.

    Methods:
        load_asset_valuations(List[model.AssetValuation]): List of AssetValuation instances to be loaded into the
            repository.
    """

    @abstractmethod
    def load_asset_valuations(self, asset_valuations: list[model.AssetValuation]):
        """
        Abstract method to define the interface for loading Asset Valuations into the repository.

        Args:
            asset_valuations (List[model.AssetValuation]): List of AssetValuation instances to be loaded into
                the repository.
        """
        raise NotImplementedError


class BiqQueryRepository(AbstractRepository):
    """
    A concrete implementation of the AbstractRepository for interacting with Google BigQuery.
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

    def __init__(self, project=None):
        self.client = bigquery.Client(project=project)
        self.asset_valuations_destination = "raw.asset_valuations"

    def load_asset_valuations(self, asset_valuations: list[model.AssetValuation]):
        """
        Load Asset Valuations into BigQuery table indicated by attribute asset_valuations_destination.

        Args:
            asset_valuations (List[model.AssetValuation]): List of AssetValuation instances to be loaded
                into BigQuery.
        """

        dictify = [asset_valuation.to_dict() for asset_valuation in asset_valuations]
        job_config = bigquery.LoadJobConfig(
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
            source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        )
        load_job = self.client.load_table_from_json(
            dictify, self.asset_valuations_destination, job_config=job_config
        )
        load_job.result()

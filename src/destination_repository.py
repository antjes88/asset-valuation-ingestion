from abc import ABC, abstractmethod
from typing import List, Any, Dict
from google.cloud import bigquery

from src import model


class AbstractDestinationRepository(ABC):

    @abstractmethod
    def load_asset_valuations(
        self, asset_valuations: list[model.AssetValuation]
    ) -> None:

        raise NotImplementedError


class BiqQueryDestinationRepository(AbstractDestinationRepository):

    def __init__(self, bigquery_client: bigquery.Client):
        self.bigquery_client = bigquery_client
        self.asset_valuations_destination = "raw.asset_valuations_v2"

    def load_asset_valuations(
        self, asset_valuations: list[model.AssetValuation]
    ) -> None:

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
        load_job = self.bigquery_client.load_table_from_json(
            dictify, self.asset_valuations_destination, job_config=job_config
        )
        load_job.result()

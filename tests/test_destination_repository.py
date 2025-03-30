import os
import datetime as dt
from typing import Tuple, List

from src import model, destination_repository


def test_load_asset_valuations_from_zero(
    repository_with_asset_valuations: Tuple[
        destination_repository.BiqQueryDestinationRepository, List[model.AssetValuation]
    ],
):
    """
    GIVEN a destination repository were no destination table exists and a collection of Asset Valuations
    WHEN they are passed as arguments to BiqQueryRepository.load_asset_valuations()
    THEN Asset Valuations should be loaded into the destination table in the data repository
    """
    bq_repository, asset_valuations = repository_with_asset_valuations
    query_job = bq_repository.client.query(
        f"SELECT * FROM {os.environ['DATASET']}.{os.environ['DESTINATION_TABLE']}"
    )
    rows = query_job.result()
    results_asset_valuations: List[model.AssetValuation] = []
    for row in rows:
        results_asset_valuations.append(
            model.AssetValuation(
                date=row.date,
                value=row.value,
                product_name=row.product_name,
                creation_date=row.__creation_date__,
                source_file=row.__source_file__,
            )
        )

    assert len(asset_valuations) == len(results_asset_valuations)
    for asset_valuation in asset_valuations:
        assert asset_valuation in results_asset_valuations


def test_load_asset_valuations_appending(
    repository_with_asset_valuations: Tuple[
        destination_repository.BiqQueryDestinationRepository, List[model.AssetValuation]
    ],
):
    """
    GIVEN a destination repository with a previous state of destination table exists and a new Asset Valuation to append
    WHEN they are passed as arguments to BiqQueryRepository.load_asset_valuations()
    THEN Asset Valuations should be loaded into the destination table in the data repository
    """
    bq_repository, asset_valuations = repository_with_asset_valuations

    # load new Asset Valuation
    assets_to_append = [
        model.AssetValuation(
            dt.date(2020, 1, 1), 1200.0, "product 6", "dummy_file.csv"
        ),
    ]
    bq_repository.load_asset_valuations(assets_to_append)

    # get Asset Valuations from bigquery
    query_job = bq_repository.client.query(
        f"SELECT * FROM {os.environ['DATASET']}.{os.environ['DESTINATION_TABLE']}"
    )
    rows = query_job.result()
    results_asset_valuations: List[model.AssetValuation] = []
    for row in rows:
        results_asset_valuations.append(
            model.AssetValuation(
                date=row.date,
                value=row.value,
                product_name=row.product_name,
                creation_date=row.__creation_date__,
                source_file=row.__source_file__,
            )
        )
    expected_asset_valuations = asset_valuations + assets_to_append

    assert len(expected_asset_valuations) == len(results_asset_valuations)
    for asset_valuation in expected_asset_valuations:
        assert asset_valuation in results_asset_valuations

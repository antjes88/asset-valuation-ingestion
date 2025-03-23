import os
from typing import List, Tuple

from src import services, source_repository, destination_repository, model
from tests.data.asset_valuations import ASSET_VALUATIONS_2021, ASSET_VALUATIONS_HL


def test_asset_valuation_pipeline_generic(
    repository_with_asset_valuations: Tuple[
        destination_repository.BiqQueryRepository, List[model.AssetValuation]
    ],
):
    """
    GIVEN a generic source file to be appended to destination asset valuation table
    WHEN we call the service asset_valuation_pipeline()
    THEN the destination table must be updated with the new data
    """
    file = source_repository.LocalFile("tests/data/generic_2021_01_01.csv")
    bq_repository, asset_valuations_pre = repository_with_asset_valuations
    services.asset_valuation_pipeline(file, bq_repository)

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
    expected_asset_valuations = asset_valuations_pre + ASSET_VALUATIONS_2021

    assert len(expected_asset_valuations) == len(results_asset_valuations)
    for asset_valuation in expected_asset_valuations:
        assert asset_valuation in results_asset_valuations


def test_asset_valuation_pipeline_hl(
    repository_with_asset_valuations: Tuple[
        destination_repository.BiqQueryRepository, List[model.AssetValuation]
    ],
):
    """
    GIVEN a HL source file to be appended to destination asset valuation table
    WHEN we call the service asset_valuation_pipeline()
    THEN the destination table must be updated with the new data
    """
    file = source_repository.LocalFile("tests/data/hl_2023_11_24.csv")
    bq_repository, asset_valuations_pre = repository_with_asset_valuations
    services.asset_valuation_pipeline(file, bq_repository)

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
    expected_asset_valuations = asset_valuations_pre + ASSET_VALUATIONS_HL

    assert len(expected_asset_valuations) == len(results_asset_valuations)
    for asset_valuation in expected_asset_valuations:
        assert asset_valuation in results_asset_valuations

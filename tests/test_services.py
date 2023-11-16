import services
import source_repository
import model
import os
from tests.data.asset_valuations import ASSET_VALUATIONS_2021


def test_asset_valuation_pipeline_local_file(repository_with_asset_valuations):
    """
    GIVEN a new source file to be appended to destination asset valuation table
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
    results_asset_valuations = []
    for row in rows:
        results_asset_valuations.append(
            model.AssetValuation(
                row.date, row.value, row.product_name, row.creation_date
            )
        )
    expected_asset_valuations = asset_valuations_pre + ASSET_VALUATIONS_2021

    assert len(expected_asset_valuations) == len(results_asset_valuations)
    for asset_valuation in expected_asset_valuations:
        assert asset_valuation in results_asset_valuations

import source_repository
import destination_repository


def asset_valuation_pipeline(
    source_repo: source_repository.FileAbstract,
    destination_repo: destination_repository.AbstractRepository,
):
    """
    Fetches Asset Valuations from the source repository and loads it into the destination repository.

    Args:
        destination_repo (repository.AbstractRepository): The data repository to load Asset Valuations into.
        source_repo (repository.AbstractRepository): The data repository to load Asset Valuations into.
    """
    asset_valuations = source_repo.get_asset_valuations()
    destination_repo.load_asset_valuations(asset_valuations)

from src import source_repository, destination_repository


def asset_valuation_pipeline(
    source_repo: source_repository.AbstractSourceRepository,
    destination_repo: destination_repository.AbstractDestinationRepository,
):
    """
    Fetches Asset Valuations from the source repository and loads it into the destination repository.

    Args:
        destination_repo
            (destination_repository.AbstractDestinationRepository): The data repository to
                                                                    load Asset Valuations into.
        source_repo (source_repository.AbstractSourceRepository): The data repository to load Asset Valuations from.
    """
    asset_valuations = source_repo.get_asset_valuations()
    destination_repo.load_asset_valuations(asset_valuations)

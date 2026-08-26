from src import source_repository, destination_repository


def asset_valuation_pipeline(
    source_repo: source_repository.AbstractSourceRepository,
    destination_repo: destination_repository.AbstractDestinationRepository,
):

    asset_valuations = source_repo.get_asset_valuations()
    destination_repo.load_asset_valuations(asset_valuations)

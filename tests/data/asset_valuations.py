import model
import datetime as dt


ASSET_VALUATIONS_2018 = [
    model.AssetValuation(dt.date(2018, 12, 29), 1200.0, "product 1"),
    model.AssetValuation(dt.date(2018, 12, 29), 5100.0, "product 2"),
    model.AssetValuation(dt.date(2018, 12, 29), 31200.0, "product 3"),
    model.AssetValuation(dt.date(2018, 12, 29), 2500.0, "product 4"),
    model.AssetValuation(dt.date(2018, 12, 29), 100.0, "product 5"),
]

ASSET_VALUATIONS_2021 = [
    model.AssetValuation(dt.date(2021, 1, 1), 1200.0, "product 1"),
    model.AssetValuation(dt.date(2021, 1, 1), 5100.0, "product 2"),
    model.AssetValuation(dt.date(2021, 1, 1), 31200.0, "product 3"),
    model.AssetValuation(dt.date(2021, 1, 1), 2500.0, "product 4"),
    model.AssetValuation(dt.date(2021, 1, 1), 100.0, "product 5"),
]

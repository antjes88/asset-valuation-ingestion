from src import model
import datetime as dt


ASSET_VALUATIONS_2018 = [
    model.AssetValuation(
        dt.date(2018, 12, 29), 1200.0, "product 1", "tests/data/generic_2018_12_29.csv"
    ),
    model.AssetValuation(
        dt.date(2018, 12, 29), 5100.0, "product 2", "tests/data/generic_2018_12_29.csv"
    ),
    model.AssetValuation(
        dt.date(2018, 12, 29), 31200.0, "product 3", "tests/data/generic_2018_12_29.csv"
    ),
    model.AssetValuation(
        dt.date(2018, 12, 29), 2500.0, "product 4", "tests/data/generic_2018_12_29.csv"
    ),
    model.AssetValuation(
        dt.date(2018, 12, 29), 100.0, "product 5", "tests/data/generic_2018_12_29.csv"
    ),
]

ASSET_VALUATIONS_2021 = [
    model.AssetValuation(
        dt.date(2021, 1, 1), 1200.0, "product 1", "tests/data/generic_2021_01_01.csv"
    ),
    model.AssetValuation(
        dt.date(2021, 1, 1), 5100.0, "product 2", "tests/data/generic_2021_01_01.csv"
    ),
    model.AssetValuation(
        dt.date(2021, 1, 1), 31200.0, "product 3", "tests/data/generic_2021_01_01.csv"
    ),
    model.AssetValuation(
        dt.date(2021, 1, 1), 2500.0, "product 4", "tests/data/generic_2021_01_01.csv"
    ),
    model.AssetValuation(
        dt.date(2021, 1, 1), 100.0, "product 5", "tests/data/generic_2021_01_01.csv"
    ),
]

ASSET_VALUATIONS_HL = [
    model.AssetValuation(
        dt.date(2023, 11, 24), 2200.0, "HL - Cash", "tests/data/generic_2021_01_01.csv"
    ),
    model.AssetValuation(
        dt.date(2023, 11, 24),
        10140.45,
        "AXA Framlington Test 1",
        "tests/data/generic_2021_01_01.csv",
    ),
    model.AssetValuation(
        dt.date(2023, 11, 24),
        4200.0,
        "Fidelity Asia Test 2",
        "tests/data/generic_2021_01_01.csv",
    ),
    model.AssetValuation(
        dt.date(2023, 11, 24), 14572.50, "Googles", "tests/data/generic_2021_01_01.csv"
    ),
]

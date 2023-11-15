import model
import datetime as dt
import pytest


def test_asset_valuation_to_dict():
    """
    GIVEN an object of AssetValuation
    WHEN method to_dict() is called
    THEN it should return a dictionary representation of the instance data
    """
    date = dt.date(2023, 1, 1)
    value = 100.0
    product_name = "product 1"
    creation_date = dt.datetime.now()
    asset_valuation = model.AssetValuation(date, value, product_name, creation_date)

    assert asset_valuation.to_dict() == {
        "date": date.strftime("%Y-%m-%d"),
        "value": value,
        "product_name": product_name,
        "creation_date": creation_date.strftime("%Y-%m-%d %H:%M:%S"),
    }


def test_asset_valuation_equality():
    """
    GIVEN 2 asset valuations that have same date, product name and value
    WHEN they are checked for equality
    THEN the result should be that are equal
    """
    date = dt.date(2021, 10, 10)
    value = 0.05
    product_name = "product"

    assert model.AssetValuation(
        date,
        value,
        product_name,
        dt.datetime(
            1990,
            1,
            1,
        ),
    ) == model.AssetValuation(
        date,
        value,
        product_name,
        dt.datetime(
            2020,
            12,
            12,
        ),
    )


@pytest.mark.parametrize(
    "date_left, date_right, value_left, value_right, product_name_left, product_name_right",
    [
        (dt.datetime(2021, 10, 10), dt.datetime(1990, 10, 10), 0.1, 0.1, "GBP", "GBP"),
        (dt.datetime(1990, 10, 10), dt.datetime(1990, 10, 10), 0.1, 0.2, "GBP", "GBP"),
        (dt.datetime(1990, 10, 10), dt.datetime(1990, 10, 10), 0.2, 0.2, "USD", "GBP"),
    ],
)
def test_asset_valuation_inequality(
    date_left,
    date_right,
    value_left,
    value_right,
    product_name_left,
    product_name_right,
):
    """
    GIVEN 2 asset valuations with different dates, values or product names
    WHEN they are checked for equality
    THEN the result should be that are NOT equal
    """
    creation_date = dt.datetime(
        1990,
        1,
        1,
    )

    assert model.AssetValuation(
        date_left, value_left, product_name_left, creation_date
    ) != model.AssetValuation(
        date_right, value_right, product_name_right, creation_date
    )


@pytest.mark.parametrize("value", [1, "string", 0.1, dt.datetime.now()])
def test_asset_valuation_inequality_other(value):
    """
    GIVEN an asset valuation and another data structure
    WHEN they are checked for equality
    THEN the result should be that are NOT equal
    """
    assert model.AssetValuation(dt.datetime.now(), 0.1, "GBP") != value

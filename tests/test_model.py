from cloud_function import model
import datetime as dt


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

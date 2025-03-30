from dataclasses import dataclass
import datetime as dt
from typing import Any


@dataclass(frozen=True)
class AssetValuation:
    """
    Represents the valuation of an asset at a specific date.

    Attributes:
        date (dt.date): The date of the valuation.
        value (float): The valuation of the asset.
        product_name (str): The name of the asset/product.
        source_file (str): The name of the source file from which the valuation was extracted.
        creation_date (dt.datetime, optional): The creation date of the valuation instance.
                                               Defaults to the current date and time.
    Methods:
        to_dict() -> dict:
            Converts the instance data to a dictionary.
    """

    date: dt.date
    value: float
    product_name: str
    source_file: str
    creation_date: dt.datetime = dt.datetime.now()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, AssetValuation):
            return False
        return (
            self.date == other.date
            and self.value == other.value
            and self.product_name == other.product_name
        )

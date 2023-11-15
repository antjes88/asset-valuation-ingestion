from dataclasses import dataclass
import datetime as dt


@dataclass(frozen=True)
class AssetValuation:
    """
    Represents the valuation of an asset at a specific date.

    Attributes:
        date (dt.date): The date of the valuation.
        value (float): The valuation value of the asset.
        product_name (str): The name of the asset/product.
        creation_date (dt.datetime, optional): The creation date of the valuation instance.
            Defaults to the current date and time.
    Methods:
        to_dict() -> dict:
            Converts the instance data to a dictionary.
    """

    date: dt.date
    value: float
    product_name: str
    creation_date: dt.datetime = dt.datetime.now()

    def to_dict(self) -> dict:
        """
        Converts the instance data to a dictionary.

        Returns:
            dict: A dictionary representation of the instance data.
        """
        return {
            "date": self.date.strftime("%Y-%m-%d"),
            "value": self.value,
            "product_name": self.product_name,
            "creation_date": self.creation_date.strftime("%Y-%m-%d %H:%M:%S"),
        }

    def __eq__(self, other) -> bool:
        if not isinstance(other, AssetValuation):
            return False
        return (
            self.date == other.date
            and self.value == other.value
            and self.product_name == other.product_name
        )

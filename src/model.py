from dataclasses import dataclass
import datetime as dt
from typing import Any


@dataclass(frozen=True)
class AssetValuation:

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

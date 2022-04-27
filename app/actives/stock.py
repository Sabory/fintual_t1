from dataclasses import dataclass
from actives.abstract import Active
from datetime import date
from typing import Optional


@dataclass
class Stock(Active):
    """Active object for stocks"""

    active_type: str = "Stock"

    def price(
        self,
        obs_date: Optional[date] = None,
        **kwargs,
    ) -> float:
        """Returns the price of the active at the given date.

        Notes:
           For the calculation of price will use Alphavantage free tier API.

        Args:
           obs_date: Observation date to consult price of.

        Returns:
           Price of the active at the given observation time.
        """

        _p = self.price_handler.get_active_price_by_date(
            symbol=self.symbol,
            obs_date=obs_date,
            active="stock",
            **kwargs,
        )
        return _p

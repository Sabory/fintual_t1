from abc import ABC, abstractmethod
from typing import Optional
from datetime import date


class PriceHandler(ABC):
    """Abstract class for price handlers"""

    @classmethod
    @abstractmethod
    def get_active_price_by_date(
        cls, symbol: str, obs_date: Optional[date] = None, value="close", active="stock"
    ) -> Optional[float]:
        """Returns the price of the active at the given date.

        Notes:
           For the calculation of price will use Alphavantage free tier API.

        Args:
           obs_date: Observation date to consult price of.

        Returns:
           Price of the active at the given observation time.
        """
        pass

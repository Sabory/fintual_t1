from price_handler import abstract_handler
from typing import Optional
from datetime import date
from console import console


class TestPriceHandler(abstract_handler.PriceHandler):
    """Test price handler"""

    @classmethod
    def get_active_price_by_date(
        cls,
        symbol: str,
        obs_date: Optional[date] = None,
        value="close",
        active="stock",
        **kwargs,
    ) -> Optional[float]:
        """Returns the price of the active at the given date.

        Notes:
           For the calculation of price will use Alphavantage free tier API.

        Args:
           obs_date: Observation date to consult price of.

        Returns:
           Price of the active at the given observation time.
        """
        test_price = kwargs.pop("test_price", None)
        if test_price:
            console.log(f"Test price recieded: {test_price}")
            return test_price

        return float(obs_date.year + obs_date.month + obs_date.day)

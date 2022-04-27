from dataclasses import dataclass
from abc import ABC, abstractmethod
from datetime import date

from console import console
from price_handler import abstract_handler, tester_handler


@dataclass
class Active(ABC):
    """Active representation class.
    An active can be a stock, a bond, a commodity, crypto, etc.
    """

    name: str
    symbol: str
    active_type: str
    price_handler: abstract_handler.PriceHandler = tester_handler.TestPriceHandler

    @abstractmethod
    def price(self, obs_date: date) -> float:
        """Returns the price of the active at the given date.

        Args:
           obs_date: Observation date to consult price of.

        Returns:
           Price of the active at the given observation time.

        Notes:
            Maybe should periodically update the price of the active.
            so when asked, it is already cached. Insted of getting
            the value on demand.
        """
        pass

    def get_diff_price_btw_dates(
        self,
        from_date: date,
        to_date: date,
    ) -> dict:
        """Returns the difference in price between two dates.

        Args:
           from_date: Observation date from when to start the difference.
           to_date: Observation date to when to end the difference.

        Returns:
            Dictionary with the difference in price between the two dates.
              example: {
                          'date_from': datetime.date(2020, 1, 1),
                          'price_from': 100,
                          'date_to: datetime.date(2020, 3, 1),
                          'price_to': 110,
                          'delta': 10,
                          'delta_perc': 0.1
                       }

        """
        console.log(
            f"Getting differences for active {self.name}"
            f" between {from_date} and {to_date}"
        )

        if from_date > to_date:
            raise ValueError("from_date must be < to_date")

        _p_from = self.price(obs_date=from_date)
        _p_to = self.price(obs_date=to_date)

        if _p_from is None:
            console.log(f"An error ocurred getting price from {from_date}")
            return None
        if _p_to is None:
            console.log(f"An error ocurred getting price from {to_date}")
            return None

        delta = _p_to - _p_from
        delta_perc = delta / _p_from
        console.log(f"price variaton: {_p_from} ({delta} [{round(delta_perc, 4)} %])")

        return {
            "date_from": from_date,
            "price_from": _p_from,
            "date_to": to_date,
            "price_to": _p_to,
            "delta": delta,
            "delta_perc": delta_perc,
        }

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import date, timedelta


from console import console
from actives.abstract import Active


@dataclass
class Portafolio:
    """Porfafolio of actives.
    Args:
            name(str): Name of the portafolio. Only for internal use.
            actives (List[Active]): List of actives to be included in the porfafolio.

    Todos:
            - Add support for amounts of actives for each active. For now you can have
                    1 unit of each active only. Posible need to create a new class
                    for Transactions for this (added 0.123 of Tesla's stock for example).
            - Add a method to add/remove a new active to the porfafolio.
                    It's important the date of when the active was added/removed
                    (maybe create a Transaction class to track movements
                    of a portafolio) for a better calculation of the real profit.
    """

    name: str = "Risky Steve"
    actives: Optional[List[Active]] = field(default_factory=list)

    def add_active(self, active: Active) -> None:
        """Add a new active to the porfafolio.

        Args:
                active:  Active instance to be added to the porfafolio.
        """
        self.actives.append(active)
        return

    def overall_return(self, from_date: date, to_date: date) -> float:
        """Get Overall return between two given dates for the portafolio

        Args:
                from_date (date): Start date of the period to calculate the profit.
                to_date (date): End date of the period to calculate the profit.
        Returns:
                (float): Portafolio's overall return between the given dates.
                    0.01 means 1%

        """
        if len(self.actives) == 0:
            return 0.0
        if not (isinstance(from_date, date) & isinstance(to_date, date)):
            raise ValueError("Error: `from_date` and `to_date` must be date objects.")
        if from_date > to_date:
            raise ValueError("Error: `from_date` must be before `to_date`.")

        # LOGIC:
        console.log(f"Calculating overall returns for portafolio {self.name}")

        overall_total_return = 0.0
        overall_from_price = 0.0

        for active in self.actives:
            res = active.get_diff_price_btw_dates(from_date, to_date)
            overall_from_price += res["price_from"]
            overall_total_return += res["delta"]

        try:
            overall_return = overall_total_return / overall_from_price
        except ZeroDivisionError:
            overall_return = 0.0

        return overall_return

    def profit(self, from_date: date, to_date: Optional[date] = None) -> float:
        """Get Annualized return between two given dates for the portafolio

        Args:
                from_date (date): Start date of the period to calculate the profit.
                to_date (date): End date of the period to calculate the profit.
        Returns:
                (float): Portafolio's annualized return between the given dates.
        Notes:
                - The annualized return is calculated using the formula:
                    `(1 + (overall return / 100)) ** (1 / years) - 1`
                - The `years` is the natural number of years between
                    `from_date` and `to_date`. If < 1, will not be able
                    to calculate the annualized return.
                    Maybe an option would be to calculate daily return and do the
                    convertion to annualized.
        """
        if to_date is None:
            console.log("Calculating annualized until yesterday.")
            to_date = date.today() - timedelta(days=1)  # price has a delay of 1 day

        if len(self.actives) == 0:
            return 0.0
        if not (isinstance(from_date, date) & isinstance(to_date, date)):
            raise ValueError(
                "Error: `from_date` and `to_date` must be datetime objects."
            )
        if from_date > to_date:
            raise ValueError("Error: `from_date` must be before `to_date`.")

        # transform overal return to annualized return
        days_period = (to_date - from_date).days
        console.log(f"Days passed: {days_period}")

        overall_return = self.overall_return(from_date, to_date)
        console.log(f"Overall return: {overall_return} %")

        annualized_return = (1 + overall_return) ** (365 / days_period) - 1

        return annualized_return

from actives.stock import Stock
from portafolio import Portafolio

from datetime import date

from console import console
from price_handler import tester_handler


def main():
    apple = Stock(
        name="Apple", symbol="AAPL", price_handler=tester_handler.TestPriceHandler
    )
    microsoft = Stock(
        name="Microsoft", symbol="MSFT", price_handler=tester_handler.TestPriceHandler
    )
    google = Stock(
        name="Google", symbol="GOOGL", price_handler=tester_handler.TestPriceHandler
    )

    risky_steve_portafolio = Portafolio(
        name="Risky Steve Portafolio", actives=[apple, microsoft, google]
    )

    to_date = date(2022, 4, 12)
    from_date = date(2002, 4, 12)

    annualized_return = risky_steve_portafolio.profit(
        to_date=to_date, from_date=from_date
    )
    console.log(
        f"Annualized return for {risky_steve_portafolio.name} between dates {from_date}"
        f" and {to_date} is {annualized_return} %"
    )


if __name__ == "__main__":
    main()

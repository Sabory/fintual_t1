import requests
import os
from datetime import date, timedelta, datetime
from typing import List, Optional

from console import console
from price_handler import abstract_handler


class Alphavantage(abstract_handler.PriceHandler):
    """Wrapper for Alphavantage API.

    For more information please visit:
        https://www.alphavantage.co/documentation/
    """

    base_url = "https://www.alphavantage.co/"
    active_types = ("stock", "crypto")
    data_dir = "./data/alphavantage/"
    compact_threshold = 99

    @classmethod
    def _request_active_quote(
        cls, symbol: str, outputsize: str = "compact", active_type: str = "stock"
    ) -> Optional[dict]:
        """Get the active quates from Alphavantage API.

        Args:
           symbol: Symbol of the active (it can be crypto or stock symbol).
           outputsize: Size of the output. 'compact' return last 100 days.
              And 'full' return all available data.
           active_type: Type of the active. 'stock' or 'crypto'.

        Returns:
           dict or None: dictionary with all the daily prices of the active
        """
        console.log(
            f"Getting quotes for active type {active_type} - {symbol}"
            f" (outputsize: {outputsize})"
        )
        if active_type not in cls.active_types:
            raise ValueError("active_type must be 'stock' or 'crypto'")
        if outputsize not in ("compact", "full"):
            raise ValueError("outputsize must be 'compact' or 'full'")

        if active_type == "stock":
            url = (
                f"{cls.base_url}query?function=TIME_SERIES_DAILY&symbol={symbol}"
                + f"&outputsize={outputsize}&apikey="
                + f'{os.getenv("ALPHAVANTAGE_API_KEY")}'
            )

        elif active_type == "crypto":
            url = (
                f"{cls.base_url}query?function=DIGITAL_CURRENCY_DAILY&symbol={symbol}"
                + f"&market=USD&outputsize={outputsize}&apikey="
                + f'{os.getenv("ALPHAVANTAGE_API_KEY")}'
            )
        else:
            console.log(f"active_type: {active_type} not supported yet.")
            return None

        response = requests.get(url)
        if response.ok:
            data = response.json()
        else:
            return None
        if "Error Message" in data:
            console.log(f"Error in Alphanvatage API request: {data['Error Message']}")
            return None
        return data

    def _get_searched_value(searched_value: str, values: dict) -> Optional[float]:
        """Get the searched value from the ticker data.
        Args:
            searched_value: Value to search in the ticker data.
            values: Dictionary with the ticker data of the searched day.
        Returns:
            Value of the searched value (None if not found).
        """
        for value in values:
            if searched_value in value:
                price = values[value]
                price = float(price)
                return price
        console.log(f"Value not found: {searched_value}")
        return None

    def _is_date_in_ticker_data(searched_date: str, dates: List[str]) -> bool:
        """Check if the searched date is in the ticker data.
        Args:
            searched_date: Date to search in the ticker data.
                format: YYYY-MM-DD
            dates: List of dates in the ticker data.
        Returns:
            True if the searched date is in the ticker data, else False.
        """
        if searched_date not in dates:
            dates_list = list(dates)
            _from = dates_list[-1]
            _to = dates_list[0]
            console.log(f"Date not found. Avaliable range: [{_from}, {_to}]")
            return False

        return True

    def _if_obs_date_too_current_replace_with_latest(
        searched_date: date, available_dates: List[str]
    ) -> date:
        """Check if the searched date is most recent than the latest date.

        If the requested date is not available yet, it will be replaced
        by the latest date available.
        """
        # Convert list into datetime objects for greater comparations.
        _available_dates = [
            datetime.strptime(x, "%Y-%m-%d").date() for x in available_dates
        ]

        # get most recent date
        _available_dates.sort(reverse=True)
        latest_record = _available_dates[0]

        if searched_date > latest_record:
            console.log(
                "Warning: searched data is too current and is not available yet."
                f" Getting lastest data: {latest_record}",
                style="yellow",
            )
            return latest_record
        return searched_date

    @classmethod
    def _non_cached_active_price_by_date(
        cls, symbol: str, obs_date: date, value: str, active: str
    ) -> Optional[float]:
        # Define if should get all data or only last 100 days (lighter request)
        output_size = "compact"
        if obs_date <= date.today() - timedelta(days=cls.compact_threshold):
            console.log(
                "Required observation date for the ticket is older than"
                " 100 days. Will have to use 'outputsize=full' to get"
                " the full time series."
            )
            output_size = "full"

        # Get the ticker data
        if active == "stock":
            data = cls._request_active_quote(
                symbol, outputsize=output_size, active_type="stock"
            )
            time_series_key = "Time Series (Daily)"
        elif active == "crypto":
            data = cls._request_active_quote(
                symbol, outputsize=output_size, active_type="crypto"
            )
            time_series_key = "Time Series (Digital Currency Daily)"
        else:
            console.log('Active must be "stock" or "crypto"')
            return None

        # Check if data is available
        if data is None:
            console.log("Error: no valuable data returned from API.")
            return None

        try:
            available_dates = list(data[time_series_key].keys())
        except KeyError as e:
            if "Note" in data:
                if "Thank you for using Alpha Vantage!" in data["Note"]:
                    raise ValueError(
                        "Error: API free tier requests has been exceeded.",
                        "error message: " + data["Note"],
                    )
            else:
                raise ValueError(
                    "Error: no valuable data returned from API.",
                    "error message: " + str(e),
                )
        # Check if requested date is too new and replace it with the latest
        _obs_date = cls._if_obs_date_too_current_replace_with_latest(
            obs_date, available_dates
        )
        _obs_date_str = _obs_date.strftime("%Y-%m-%d")

        # Extract from api response the price of specified date
        _found = cls._is_date_in_ticker_data(
            searched_date=_obs_date_str, dates=available_dates
        )
        if not _found:
            return None

        day_values = data[time_series_key][_obs_date_str]
        price = cls._get_searched_value(searched_value=value, values=day_values)

        console.log(f"{symbol} price on {_obs_date_str}: {price}")

        return price

    @classmethod
    def _price_cached(
        cls, symbol: str, obs_date: date, value: str, active: str
    ) -> Optional[float]:
        """Check the cache folder for the price of the symbol on the obs_date.

        Args:
            symbol: Symbol of the ticket.
            obs_date: Date of the observation.
            value: Value to search in the ticker data.
            active: Type of active (stock or crypto).
        Returns:
            Price of the symbol on the obs_date. If not found in the cache
            folder, will return None
        """
        pass

    @classmethod
    def _save_new_price_data(
        cls, symbol: str, obs_date: date, active: str, data: dict
    ) -> None:
        """Save new price data as json in the cache folder.
        Save method is like a merge so if the data cached is "full" data instead of
        compact, will not loose the full data, istead will add new data instead.

        Args:
            symbol: Symbol of the stock or crypto.
            obs_date: Observation date of the price.
            active: Active type of the stock or crypto.
            data: Data to save.
        Returns:
            None
        """
        pass

    @classmethod
    def get_active_price_by_date(
        cls,
        symbol: str,
        obs_date: Optional[date] = None,
        value="close",
        active="stock",
        **kwargs,
    ) -> Optional[float]:
        """Get stock price for the given date.

        Args:
            symbol: stock symbol (e.g. AAPL, MSFT, GOOGL)
            obs_date: observation date in format YYYY-MM-DD
                API will only return
            value: value of the daily candles to return.
                Default: '4. close': close daily price)
                Accepted values: ('open', 'high', 'low',
                    'close', 'volume', 'market cap')
            active: type of active. Accepted values: ('stock', 'crypto')
                Default: 'stock'

        Returns:
            A float representing the price of the active
                for the asked observation date

        Notes:
            - API only returns data for the las 100 days. if more than
                100 days are required, must specified in the API request
                'outputsize=full' and will return full lenght time series
                of the ticket (+20 years) so it will take more time
                and resources.
            - Because the API returns the daily candles, the most recent
                date available is lastest close market day.
        """
        console.log(
            f"""Getting active price by date for:
             - symbol: {symbol}
             - obs_date: {obs_date}
             - value: {value}
             - active: {active}"""
        )

        # If no obs date delivered, will be replaced by today
        if obs_date is None:
            console.log(
                "Warning: No obs_date provided. Getting today's date.", style="yellow"
            )
            obs_date = date.today()

        # check if price date was already cached
        price_cached = cls._price_cached(symbol, obs_date, value, active)

        if price_cached is None:
            console.log("Price not cached. Getting new data from API.")
            price = cls._non_cached_active_price_by_date(
                symbol=symbol, obs_date=obs_date, value=value, active=active
            )

            # save new price in cache
            cls._save_new_price_data(symbol, obs_date, active, price)

        else:
            price = price_cached
        return price

# Fintual 

## Task
> Construct a simple Portfolio class that has a collection of Stocks and a "Profit" method that receives 2 dates and returns the profit of the Portfolio between those dates. Assume each Stock has a "Price" method that receives a date and returns its price.
> Bonus Track: make the Profit method return the "annualized return" of the portfolio between the given dates.
> [Fintual postulation site](https://jobs.lever.co/fintual/749e4113-3cf7-4098-b52a-1219dcc55db0)

## Solution
The *Stock* object it's going to be extracted to as an *Active*, this way a Portafolio can be a collection of *Active*s. For example, we could add a *Crypto* active or *Bonds* active to a Portfolio in a much easier way instead of having to create a new *Stock* object it self.<br>
All the actives can be found: `./app/actives/` <br>
And the main abstraction for an active can be found: `./app/actives/abstract.py` 

Also for easier implementation of multiple price sources, the price handler was extracted to a *PriceHandler* object. So each *Active* can use the wanted price source. <br>
All the price handlers can be found: `./app/price_handler/` <br>
And the main abstraction for a price handler can be found: `./app/price_handler/abstract_handler.py`

--------------------------------

## Initialization (UNIX based systems)

+ Create virtual environment for project. For the development, I'm using `Python 3.8.10`
```bash
python3 -m venv venv
source venv/bin/activate 
```

+ Install dependencies
```bash
pip3 install -r requirements.txt
```

## Testing

For testing, it's used `Unittest`. Once in the `./app` directory, run:
```bash
python3 -m unittest
```

## Run Example

In the `./app` directory, run:
```bash
python3 main.py
```
This will run an example calculation of a Portafolio's return between two dates. This Portaflio will have 2 main actives, Stocks & Cryptos.


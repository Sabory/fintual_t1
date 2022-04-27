import unittest
from datetime import date

from portafolio import Portafolio
from actives.stock import Stock
from actives.crypto import Crypto


class TestPortafolio(unittest.TestCase):
    def setUp(self):
        self.actives = {
            "stocks": {
                "Apple": Stock(name="Apple", symbol="AAPL"),
                "Google": Stock(name="Google", symbol="GOOG"),
            },
            "cryptos": {
                "Ethereum": Crypto(name="Ethereum", symbol="ETH"),
            },
        }

    def test_init(self):
        portafolio1 = Portafolio(name="p1")
        portafolio2 = Portafolio(name="p2")

        self.assertEqual(portafolio1.name, "p1")
        self.assertEqual(portafolio2.name, "p2")
        self.assertEqual(len(portafolio1.actives), 0)
        self.assertEqual(len(portafolio2.actives), 0)

        portafolio1.add_active(self.actives["stocks"]["Apple"])

        # ensuring default_factory = list is not being referenced to the same list
        # thing that would happend if `actives = []`
        self.assertEqual(portafolio1.name, "p1")
        self.assertEqual(portafolio2.name, "p2")
        self.assertEqual(len(portafolio1.actives), 1)
        self.assertEqual(len(portafolio2.actives), 0)

    def test_overall_return(self):
        # testing uni active portafolio
        # "Diversification is for ****." - Mark Cuban.
        my_portafolio = Portafolio(actives=[self.actives["stocks"]["Apple"]])
        r = my_portafolio.overall_return(
            from_date=date(2001, 2, 1), to_date=date(2022, 2, 1)
        )
        self.assertAlmostEqual(r, 0.004, delta=0.01)

        # testing multi active portafolio of only stocks
        # “For most people, the best thing to do is to own the S&P 500
        #   index fund.” - Warrent Buffet.
        my_portafolio = Portafolio(
            name="Blue chips Steve",
            actives=[
                self.actives["stocks"]["Apple"],
                self.actives["stocks"]["Google"],
            ],
        )
        r = my_portafolio.overall_return(
            from_date=date(2001, 2, 1), to_date=date(2022, 2, 1)
        )
        self.assertAlmostEqual(r, 0.0104, delta=0.01)

        # testing mutli active types portafolio
        # "You can't stop things like Bitcoin." - John McAfee.
        my_portafolio = Portafolio(
            name="Risky Steve",
            actives=[
                self.actives["stocks"]["Apple"],
                self.actives["stocks"]["Google"],
                self.actives["cryptos"]["Ethereum"],
            ],
        )
        r = my_portafolio.overall_return(
            from_date=date(2022, 2, 1), to_date=date(2022, 2, 10)
        )
        self.assertAlmostEqual(r, 0.004, delta=0.01)

    def test_profit(self):
        """test annualize return"""
        pass

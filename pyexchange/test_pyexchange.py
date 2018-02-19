import unittest

from pyexchange.exchange import Exchange, ExchangeHelper
from pyexchange.trader import Trader


class TestExchange(unittest.TestCase):
    def test_transactions_1(self):
        exchange = Exchange()

        aurelius = Trader("M. Aurelius", 10000, 100)
        seneca = Trader("L. A. Seneca", 10000, 100)

        exchange.sell(3, 99, aurelius)
        exchange.sell(8, 101, aurelius)
        self.assertEqual(len(exchange.bids), 0)
        self.assertEqual(len(exchange.asks), 2)

        exchange.buy(10, 100, seneca)

        # Aurelius -> Seneca, 3 units @ 99

        self.assertEqual(aurelius.funds, 10297)
        self.assertEqual(aurelius.units, 97)
        self.assertEqual(seneca.funds, 9703)
        self.assertEqual(seneca.units, 103)

        self.assertEqual(len(exchange.bids), 1)
        self.assertEqual(len(exchange.asks), 1)
        self.assertEqual(len(exchange.transactions), 1)

        exchange.sell(5, 97, aurelius)

        # Aurelius -> Seneca 5 units @ 97

        self.assertEqual(aurelius.funds, 10782)
        self.assertEqual(aurelius.units, 92)
        self.assertEqual(seneca.funds, 9218)
        self.assertEqual(seneca.units, 108)

        self.assertEqual(len(exchange.bids), 1)
        self.assertEqual(len(exchange.asks), 1)
        self.assertEqual(len(exchange.transactions), 2)

        exchange.sell(2, 102, aurelius)
        exchange.sell(3, 98, aurelius)

        # Aurelius -> Seneca, 2 units @ 98

        self.assertEqual(aurelius.funds, 10978)
        self.assertEqual(aurelius.units, 90)
        self.assertEqual(seneca.funds, 9022)
        self.assertEqual(seneca.units, 110)

        self.assertEqual(len(exchange.bids), 0)
        self.assertEqual(len(exchange.asks), 3)
        self.assertEqual(len(exchange.transactions), 3)


class TestExchangeHelper(unittest.TestCase):
    def _get_test_exchange_1(self):
        exchange = Exchange()

        aurelius = Trader("M. Aurelius", 10000, 100)

        exchange.buy(8, 50, aurelius)
        exchange.buy(5, 50, aurelius)
        exchange.buy(6, 51, aurelius)
        exchange.buy(3, 52, aurelius)
        exchange.buy(9, 52, aurelius)
        exchange.buy(2, 50, aurelius)

        exchange.sell(7, 55, aurelius)
        exchange.sell(4, 55, aurelius)
        exchange.sell(8, 54, aurelius)
        exchange.sell(1, 54, aurelius)
        exchange.sell(3, 54, aurelius)
        exchange.sell(5, 53, aurelius)

        return exchange

    def test_collapsed_bids(self):
        exchange = self._get_test_exchange_1()
        collapsed_bids = ExchangeHelper.collapsed_bids(exchange)
        self.assertEqual(collapsed_bids[0].units, 12)
        self.assertEqual(collapsed_bids[0].price, 52)
        self.assertEqual(collapsed_bids[1].units, 6)
        self.assertEqual(collapsed_bids[1].price, 51)
        self.assertEqual(collapsed_bids[2].units, 15)
        self.assertEqual(collapsed_bids[2].price, 50)

    def test_collapsed_asks(self):
        exchange = self._get_test_exchange_1()
        collapsed_asks = ExchangeHelper.collapsed_asks(exchange)
        self.assertEqual(collapsed_asks[0].units, 5)
        self.assertEqual(collapsed_asks[0].price, 53)
        self.assertEqual(collapsed_asks[1].units, 12)
        self.assertEqual(collapsed_asks[1].price, 54)
        self.assertEqual(collapsed_asks[2].units, 11)
        self.assertEqual(collapsed_asks[2].price, 55)


if __name__ == '__main__':
    unittest.main(verbosity=2)

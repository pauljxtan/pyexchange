import unittest

from pyexchange.exchange import Exchange, Trader


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


if __name__ == '__main__':
    unittest.main(verbosity=2)

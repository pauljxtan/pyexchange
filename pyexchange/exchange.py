"""
A simple toy exchange on which some asset/commodity/etc. is bought and sold
with some generic currency.
"""

# TODO:
# -- Logging
# -- Simulations with random trades
# ---- E.g. perfectly efficient market or programmed trader behaviour,
#      "black swans", etc.
# -- CLI/GUI with live updating, etc.
# -- Order expiry
# -- Add multiprocessing

import random
from tabulate import tabulate

from pyexchange.order import Ask, Bid
from pyexchange.trader import Trader, FAKE_TRADER
from pyexchange.transaction import Transaction


class Exchange(object):
    def __init__(self):
        self.bids = []
        self.asks = []
        self.transactions = []

    def buy(self, units, price, buyer, verbose=False):
        """
        Places an order to buy a number of units at the given price per unit.
        """
        if verbose: print("BUY: {} @ {}".format(units, price))

        self.bids.append(Bid(units, price, buyer))
        # Sort the bids in decreasing price
        self.bids.sort(key=lambda bid: -bid.price)
        self.fill_orders()

    def sell(self, units, price, seller, verbose=False):
        """
        Places an order to sell a number of units at the given price per unit.
        """
        if verbose: print("SELL: {} @ {}".format(units, price))

        self.asks.append(Ask(units, price, seller))
        # Sort the asks in increasing price
        self.asks.sort(key=lambda ask: ask.price)
        self.fill_orders()

    def ensure_orders_are_sorted(self):
        self.bids.sort(key=lambda bid: -bid.price)
        self.asks.sort(key=lambda ask: ask.price)

    def fill_orders(self):
        """
        Fills as many orders as possible. (Orders may be partially filled.)
        """
        self.ensure_orders_are_sorted()
        # TODO: Think about how to optimize this
        for i, bid in enumerate(self.bids):
            units_filled = 0
            while units_filled < bid.units:
                for j, ask in enumerate(self.asks):
                    if ask.price <= bid.price:

                        remaining_units = bid.units - units_filled
                        if ask.units > remaining_units:
                            units_to_trade = remaining_units
                        else:
                            units_to_trade = ask.units

                        if not self.trade_is_valid(bid.buyer, ask.seller,
                                                   units_to_trade, ask.price):
                            # TODO: something
                            continue

                        self.asks[j].units -= units_to_trade
                        units_filled += units_to_trade

                        bid.buyer.funds -= ask.price * units_to_trade
                        bid.buyer.units += units_to_trade
                        ask.seller.funds += ask.price * units_to_trade
                        ask.seller.units -= units_to_trade

                        self.transactions.append(
                            Transaction(bid.buyer, ask.seller, units_filled,
                                        ask.price))
                break
            self.bids[i].units -= units_filled

        # Remove filled orders
        self.bids = list(filter(lambda a_bid: a_bid.units > 0, self.bids))
        self.asks = list(filter(lambda an_ask: an_ask.units > 0, self.asks))

    def display_full(self):
        """
        Returns a string with an overall summary of the exchange.
        """
        display = self.display_stats() + "\n"
        display += self.display_orders()
        return display

    def display_stats(self):
        """
        Returns a string with various statistics.
        """
        self.ensure_orders_are_sorted()

        table = [
            ["Mid price: {}".format(ExchangeStats.mid_price(self)),
             "Spread: {}".format(ExchangeStats.spread(self))],
            ["Bid volume: {}".format(ExchangeStats.bid_volume(self)),
             "Ask volume: {}".format(ExchangeStats.ask_volume(self))]
        ]
        return tabulate(table, tablefmt="plain")

    def display_orders(self):
        """
        Returns a string with tabulated buy and sell orders.
        """
        self.ensure_orders_are_sorted()

        table = []
        for _, bid in enumerate(self.collapsed_bids()):
            bid_display = "{} units @ {}".format(bid.units, bid.price)
            table.append([bid_display, ""])

        for i, ask in enumerate(self.collapsed_asks()):
            ask_display = "{} units @ {}".format(ask.units, ask.price)
            if i < len(table):
                table[i][1] = ask_display
            else:
                table.append(["", ask_display])

        headers = ["Bids", "Asks"]
        return tabulate(table, headers, tablefmt="grid")

    # TODO: The following two methods are similar enough that they can
    # probably be combined

    def collapsed_bids(self):
        """
        Return a list with bids of the same price combined.
        E.g. (2 @ 42) + (4 @ 42) -> (6 @ 42)
        """
        self.ensure_orders_are_sorted()

        collapsed = []
        current = Bid(self.bids[0].units, self.bids[0].price, FAKE_TRADER)
        for _, bid in enumerate(self.bids[1:]):
            if bid.price < current.price:
                collapsed.append(current)
                current = Bid(bid.units, bid.price, FAKE_TRADER)
                continue
            current.units += bid.units
        collapsed.append(current)

        return collapsed

    def collapsed_asks(self):
        """
        Return a list with asks of the same price combined.
        """
        self.ensure_orders_are_sorted()

        collapsed = []
        current = Ask(self.asks[0].units, self.asks[0].price, FAKE_TRADER)
        for _, ask in enumerate(self.asks[1:]):
            if ask.price > current.price:
                collapsed.append(current)
                current = Ask(ask.units, ask.price, FAKE_TRADER)
                continue
            current.units += ask.units
        collapsed.append(current)

        return collapsed

    @staticmethod
    def trade_is_valid(buyer, seller, units, price):
        """
        Confirms that the buyer has sufficient funds and the seller has
        sufficient units.
        """
        # TODO: Some sort of logging/notification here
        return buyer.funds >= units * price and seller.units >= units


class ExchangeStats(object):
    @classmethod
    def mid_price(cls, exchange):
        if len(exchange.bids) == 0 or len(exchange.asks) == 0: return None
        return (exchange.bids[0].price + exchange.asks[0].price) / 2.0

    @classmethod
    def spread(cls, exchange):
        if len(exchange.bids) == 0 or len(exchange.asks) == 0: return None
        return exchange.asks[0].price - exchange.bids[0].price

    @classmethod
    def bid_volume(cls, exchange):
        return sum([bid.units for bid in exchange.bids])

    @classmethod
    def ask_volume(cls, exchange):
        return sum([ask.units for ask in exchange.asks])

"""
A simple toy exchange on which some asset/commodity/etc. is bought and sold
with some generic currency.
"""

# TODO:
# -- Logging
# -- CLI/GUI with live updating, etc.
# -- Order expiry
# -- Add multiprocessing

import random
from tabulate import tabulate

from pyexchange.order import Ask, Bid
from pyexchange.trader import Trader, NO_TRADER
from pyexchange.transaction import Transaction


class Exchange(object):
    def __init__(self):
        self._bids = []
        self._asks = []
        self.transactions = []

    @property
    def bids(self):
        return self._bids

    @bids.setter
    def bids(self, bids):
        # Sort by decreasing price and "first-come-first-serve"
        bids.sort(key=lambda bid: (-bid.price, bid.timestamp))
        self._bids = bids

    @property
    def asks(self):
        return self._asks

    @asks.setter
    def asks(self, asks):
        # Sort by increasing price and "first-come-first-serve"
        asks.sort(key=lambda ask: (ask.price, ask.timestamp))
        self._asks = asks

    def buy(self, units, price, buyer, verbose=False):
        """Places an order to buy a number of units at the given price per unit."""
        if verbose: print("BUY: {} @ {}".format(units, price))

        self.bids.append(Bid(units, price, buyer))
        self._fill_orders()

    def sell(self, units, price, seller, verbose=False):
        """Places an order to sell a number of units at the given price per unit."""
        if verbose: print("SELL: {} @ {}".format(units, price))

        self.asks.append(Ask(units, price, seller))
        self._fill_orders()

    def _fill_orders(self):
        """Fills as many orders as possible. (Orders may be partially filled.)"""
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

                        if not self._trade_is_valid(bid.buyer, ask.seller, units_to_trade,
                                                    ask.price):
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
        """Returns a string with an overall summary of the exchange."""
        display = ExchangeHelper.display_stats(self) + "\n"
        display += ExchangeHelper.display_orders(self)
        return display

    @staticmethod
    def _trade_is_valid(buyer, seller, units, price):
        """Confirms that the buyer has sufficient funds and the seller has sufficient units."""
        return buyer.funds >= units * price and seller.units >= units


class ExchangeHelper(object):
    """Non-essential methods for extracting higher-level data from an exchange."""

    @classmethod
    def display_stats(cls, exchange):
        """Returns a string with various statistics."""
        table = [
            ["Mid price: {}".format(cls.mid_price(exchange)),
             "Spread: {}".format(cls.spread(exchange))],
            ["Bid volume: {}".format(cls.bid_volume(exchange)),
             "Ask volume: {}".format(cls.ask_volume(exchange))]
        ]
        return tabulate(table, tablefmt="plain")

    @classmethod
    def display_orders(cls, exchange):
        """Returns a string with tabulated buy and sell orders."""
        table = []
        for _, bid in enumerate(cls.collapsed_bids(exchange)):
            bid_display = "{} units @ {}".format(bid.units, bid.price)
            table.append([bid_display, ""])

        for i, ask in enumerate(cls.collapsed_asks(exchange)):
            ask_display = "{} units @ {}".format(ask.units, ask.price)
            if i < len(table):
                table[i][1] = ask_display
            else:
                table.append(["", ask_display])

        headers = ["Bids", "Asks"]
        return tabulate(table, headers, tablefmt="grid")

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
        """Returns the total units of demand."""
        return sum([bid.units for bid in exchange.bids])

    @classmethod
    def ask_volume(cls, exchange):
        """Returns the total units of supply."""
        return sum([ask.units for ask in exchange.asks])

    @classmethod
    def collapsed_bids(cls, exchange):
        """Returns a list with bids of the same price combined."""
        if len(exchange.bids) == 0: return []

        collapsed = []
        current = Bid(exchange.bids[0].units, exchange.bids[0].price,
                      NO_TRADER)
        for _, bid in enumerate(exchange.bids[1:]):
            if bid.price < current.price:
                collapsed.append(current)
                current = Bid(bid.units, bid.price, NO_TRADER)
                continue
            current.units += bid.units
        collapsed.append(current)

        return collapsed

    @classmethod
    def collapsed_asks(cls, exchange):
        """Returns a list with asks of the same price combined."""
        if len(exchange.asks) == 0: return []

        collapsed = []
        current = Ask(exchange.asks[0].units, exchange.asks[0].price,
                      NO_TRADER)
        for _, ask in enumerate(exchange.asks[1:]):
            if ask.price > current.price:
                collapsed.append(current)
                current = Ask(ask.units, ask.price, NO_TRADER)
                continue
            current.units += ask.units
        collapsed.append(current)

        return collapsed

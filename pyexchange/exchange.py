"""
A simple toy exchange on which some asset/commodity/etc. is bought and sold
with some generic currency.
"""

# TODO:
# -- Logging
# -- Simulations with random trades
# -- CLI interface (live updating, etc.)
# -- Order expiry
# -- Add multiprocessing

from tabulate import tabulate

from pyexchange.order import Ask, Bid
from pyexchange.trader import Trader
from pyexchange.transaction import Transaction


class Exchange(object):
    def __init__(self):
        self.bids = []
        self.asks = []
        self.transactions = []

    def buy(self, units, price, buyer):
        """
        Places an order to buy a number of units at the given price per unit.
        """
        self.bids.append(Bid(units, price, buyer))
        # Sort the bids in decreasing price
        self.bids.sort(key=lambda bid: -bid.price)
        self.fill_orders()

    def sell(self, units, price, seller):
        """
        Places an order to sell a number of units at the given price per unit.
        """
        self.asks.append(Ask(units, price, seller))
        # Sort the asks in increasing price
        self.asks.sort(key=lambda ask: ask.price)
        self.fill_orders()

    def fill_orders(self):
        """
        Fills as many orders as possible. (Orders may be partially filled.)
        """
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

                        if not self.trade_is_valid(bid.buyer, ask.seller, units_to_trade, ask.price):
                            # TODO: something
                            continue

                        self.asks[j].units -= units_to_trade
                        units_filled += units_to_trade

                        bid.buyer.funds -= ask.price * units_to_trade
                        bid.buyer.units += units_to_trade
                        ask.seller.funds += ask.price * units_to_trade
                        ask.seller.units -= units_to_trade

                        self.transactions.append(Transaction(bid.buyer, ask.seller, units_filled, ask.price))
                break
            self.bids[i].units -= units_filled

        # Remove filled orders
        self.bids = list(filter(lambda a_bid: a_bid.units > 0, self.bids))
        self.asks = list(filter(lambda an_ask: an_ask.units > 0, self.asks))

    def display_full(self):
        display = self.display_stats() + "\n"
        display += self.display_orders()
        return display

    def display_stats(self):
        table = [
            ["Mid price: {}".format(self.mid_price()), "Spread: {}".format(self.spread())],
            ["Bid volume: {}".format(self.bid_volume()), "Ask volume: {}".format(self.ask_volume())]
        ]
        return tabulate(table, tablefmt="plain")

    def display_orders(self):
        table = []
        for _, bid in enumerate(self.bids):
            bid_display = "{} units @ {}".format(bid.units, bid.price)
            table.append([bid_display, ""])

        for i, ask in enumerate(self.asks):
            ask_display = "{} units @ {}".format(ask.units, ask.price)
            if i < len(table):
                table[i][1] = ask_display
            else:
                table.append(["", ask_display])

        headers = ["Bids", "Asks"]
        return tabulate(table, headers, tablefmt="grid")

    def mid_price(self):
        return (self.bids[0].price + self.asks[0].price) / 2.0

    def spread(self):
        return self.asks[0].price - self.bids[0].price

    def bid_volume(self):
        return sum([bid.units for bid in self.bids])

    def ask_volume(self):
        return sum([ask.units for ask in self.asks])

    @staticmethod
    def trade_is_valid(buyer, seller, units, price):
        """
        Confirms that the buyer has sufficient funds and the seller has
        sufficient units.
        """
        # TODO: Some sort of logging/notification here
        return buyer.funds >= units * price and seller.units >= units

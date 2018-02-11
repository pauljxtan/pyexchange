"""A simple toy exchange on which some asset/commodity/etc. is bought and sold with some generic currency."""

# TODO:
# -- Logging
# -- Simulations with random trades
# -- CLI interface (live updating, etc.)
# -- Order expiry
# -- Add multiprocessing

from abc import ABC
from datetime import datetime


class Exchange(object):
    def __init__(self):
        self.bids = []
        self.asks = []
        self.transactions = []

    def buy(self, units, price, buyer):
        """Places an order to buy a number of units at the given price per unit."""
        self.bids.append(Bid(units, price, buyer))
        # Sort the bids in decreasing price
        self.bids.sort(key=lambda bid: -bid.price)
        self.fill_orders()

    def sell(self, units, price, seller):
        """Places an order to sell a number of units at the given price per unit."""
        self.asks.append(Ask(units, price, seller))
        # Sort the asks in increasing price
        self.asks.sort(key=lambda ask: ask.price)
        self.fill_orders()

    def fill_orders(self):
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
        self.bids = list(filter(lambda bid: bid.units > 0, self.bids))
        self.asks = list(filter(lambda ask: ask.units > 0, self.asks))

    def trade_is_valid(self, buyer, seller, units, price):
        # TODO: some sort of logging or something
        return buyer.funds >= units * price and seller.units >= units


class Trader(object):
    """A buyer and/or seller on the market."""

    def __init__(self, name, funds=0, units=0):
        self.name = name
        self.funds = funds
        self.units = units

    def __repr__(self):
        return "[Trader: name={}, funds={}, units={}]".format(self.name, self.funds, self.units)


class Order(ABC):
    """An order to buy or a given number of units at some price."""

    def __init__(self, units, price):
        self.units = units
        self.price = price
        self.timestamp = datetime.now()


class Bid(Order):
    """An order to buy a given number of units at some price."""

    def __init__(self, units, price, buyer):
        super(Bid, self).__init__(units, price)
        self.buyer = buyer

    def __repr__(self):
        return "[Bid: units={}, price={}, buyer={}]".format(self.units, self.price, self.buyer)


class Ask(Order):
    """An order to sell a given number of units at some price."""

    def __init__(self, units, price, seller):
        super(Ask, self).__init__(units, price)
        self.seller = seller

    def __repr__(self):
        return "[Ask: units={}, price={}, seller={}]".format(self.units, self.price, self.seller)


class Transaction(object):
    """A single exchange of units and currency between two traders."""

    def __init__(self, buyer, seller, units, price, timestamp=datetime.now()):
        self.buyer = buyer
        self.seller = seller
        self.units = units
        self.price = price
        self.timestamp = timestamp

    def __repr__(self):
        return "[Transaction: buyer={}, seller={}, units={}, price={}]".format(
            self.buyer.name, self.seller.name, self.units, self.price
        )

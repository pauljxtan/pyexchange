from abc import ABC
from datetime import datetime


class Order(ABC):
    def __init__(self, units, price, timestamp):
        self.units = units
        self.price = price
        self.timestamp = timestamp


class Bid(Order):
    """An order to buy a given number of units at some price."""

    def __init__(self, units, price, buyer, timestamp=datetime.now()):
        super(Bid, self).__init__(units, price, timestamp)
        self.buyer = buyer

    def __repr__(self):
        return "[Bid: units={}, price={}, buyer={}]".format(self.units, self.price, self.buyer)


class Ask(Order):
    """An order to sell a given number of units at some price."""

    def __init__(self, units, price, seller, timestamp=datetime.now()):
        super(Ask, self).__init__(units, price, timestamp)
        self.seller = seller

    def __repr__(self):
        return "[Ask: units={}, price={}, seller={}]".format(self.units, self.price, self.seller)

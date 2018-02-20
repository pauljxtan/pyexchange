from datetime import datetime


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
            self.buyer.name, self.seller.name, self.units, self.price)

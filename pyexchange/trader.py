class Trader(object):
    """
    A buyer and/or seller on the market.
    """

    def __init__(self, name, funds=0, units=0):
        self.name = name
        self.funds = funds
        self.units = units

    def __repr__(self):
        return "[Trader: name={}, funds={}, units={}]".format(self.name,
                                                              self.funds,
                                                              self.units)


# A "fake" trader to use as a placeholder
FAKE_TRADER = Trader("Fake Trader", -1, -1)

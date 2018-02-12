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

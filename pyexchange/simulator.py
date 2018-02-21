"""
Random simulations of market activity. Clearly a real-life market exchange is hugely complex so
this will likely be very crude and unrealistic in comparison - but we can still have some fun
with it.

Lots of possibilities here - I'll have to do more research on this.
For instance, perfectly efficient market (random walk); programmed trader behaviour based on
"psychology", e.g., heavy selling when market is down (crashes) and vice versa (bubbles);
Talebsian "black swans"; etc.
"""

import random

from pyexchange.exchange import Exchange
from pyexchange.trader import Trader


class Simulator(object):
    def __init__(self, n_traders=100, trader_funds=10000, trader_units=100,
                 start_price=100, units_stddev=10, price_offset_mean=0, price_offset_stddev=3,
                 prob_buy=0.5):
        self.exchange = Exchange()

        self.traders = [Trader("trader-{}".format(i), trader_funds, trader_units)
                        for i in range(n_traders)]

        # Trade sizes (units) are normally distributed around 1
        self.units_stddev = units_stddev

        # Trade prices are normally distributed around an offset of zero, i.e. market price
        self.price_offset_mean = price_offset_mean
        self.price_offset_stddev = price_offset_stddev

        # Probability that a randomly generated trade will be a buy order
        # E.g. if this value is 0.5 then buys and sells are equally likely -> market is flat
        # (Note: as one would expect, this is the main parameter that makes the market "move")
        self.prob_buy = prob_buy

        self.latest_ask_price = start_price

    def generate_order(self):
        units = abs(int(round(random.gauss(0, self.units_stddev)))) + 1

        # If market has no participants, "reset" the price to the most recent ask
        if len(self.exchange.bids) == 0 and len(self.exchange.asks) == 0:
            price = self.latest_ask_price
            self.exchange.sell(units, price, random.choice(self.traders))
            return

        buying = random.random() < self.prob_buy

        # Determine the offset from the market price
        offset = abs(int(round(random.gauss(self.price_offset_mean, self.price_offset_stddev))))

        if buying:
            if len(self.exchange.asks) == 0: return

            price = self.exchange.asks[0].price - offset
            if price <= 0: return
            self.exchange.buy(units, price, random.choice(self.traders))

        else:  # sell
            if len(self.exchange.bids) == 0: return

            price = self.exchange.bids[0].price + offset
            self.exchange.sell(units, price, random.choice(self.traders))


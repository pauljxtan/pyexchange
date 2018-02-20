"""
Random simulations of market activity. Clearly a real-life market exchange is hugely complex so
this will likely be very crude and unrealistic in comparison.

Lots of possibilities here, I'll have to do more research on this.
For now, some examples: perfectly efficient market (random walk); programmed trader behaviour
based on "psychology", e.g., heavy selling when market is down (crashes) and vice versa (bubbles);
Talebsian "black swans".

Also, we could allow user customization of various parameters, probability weights and so on.
"""
import random

from pyexchange.exchange import Exchange
from pyexchange.trader import Trader

FLAVOURS = {
    'rw': "Random walk",
}


class Simulator(object):
    def __init__(self, flavour='rw', n_traders=100, trader_funds=10000, trader_units=100,
                 start_price=100, trade_units_min=1, trade_units_max=10,
                 price_offset_mean=0, price_offset_stddev=2):
        self.exchange = Exchange()
        self.traders = [Trader("trader-{}".format(i), trader_funds, trader_units)
                        for i in range(n_traders)]
        self.trade_units_min = trade_units_min
        self.trade_units_max = trade_units_max
        self.price_offset_mean = price_offset_mean
        self.price_offset_stddev = price_offset_stddev

        self.prob_buy = 0.5
        self.latest_ask_price = start_price

        if flavour == 'rw':
            pass

    def simulate_order(self):
        # If market has no volume, set price to most recent ask
        if len(self.exchange.bids) == 0 and len(self.exchange.asks) == 0:
            ask = self.latest_ask_price
            self.exchange.sell(random.randint(self.trade_units_min, self.trade_units_max), ask,
                               random.choice(self.traders))

        buy = random.random() < self.prob_buy

        # Determine the offset from the market price
        offset = int(round(random.gauss(self.price_offset_mean, self.price_offset_stddev)))
        while offset < 0:
            offset = int(round(random.gauss(self.price_offset_mean, self.price_offset_stddev)))

        if buy:
            if len(self.exchange.asks) == 0: self.simulate_order()

            bid = self.exchange.asks[0].price - offset
            self.exchange.buy(random.randint(self.trade_units_min, self.trade_units_max), bid,
                              random.choice(self.traders), verbose=True)
        else:
            if len(self.exchange.bids) == 0: self.simulate_order()

            ask = self.exchange.bids[0].price + offset
            self.exchange.sell(random.randint(self.trade_units_min, self.trade_units_max), ask,
                               random.choice(self.traders), verbose=True)

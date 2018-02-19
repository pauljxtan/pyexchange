import random
from tkinter import ttk
import tkinter as tk
import time

from pyexchange.exchange import Exchange, Trader


class Main(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.exchange = Exchange()
        self.text, self.close = self.make_widgets()

        self.text.insert(tk.END, "Welcome to the PyExchange.\n\n")


    def make_widgets(self):
        text = tk.Text(self, height=50, width=50)
        text.pack()

        simulate = ttk.Button(self, text="Simulate",
                              command=self.simulate_callback)
        simulate.pack()

        close = ttk.Button(self, text="Close", command=root.destroy)
        close.pack()

        return text, close

    def simulate(self, n_traders, n_orders, start_price):
        # Here is a crude simulation to start with, eventually needs to be
        # more customizable
        traders = [Trader("trader-{}".format(i), 10000, 100)
                   for i in range(n_traders)]

        ask = start_price
        while n_orders > 0:
            buy_or_sell = random.random()

            # If market has no volume, set price to most recent ask
            if len(self.exchange.bids) == 0 and len(self.exchange.asks) == 0:
                self.exchange.sell(random.randint(1, 10), ask,
                                   random.choice(traders))

            if buy_or_sell < 0.5:
                if len(self.exchange.asks) == 0: continue
                bid = self.exchange.asks[0].price - random.randint(0, 2)
                self.exchange.buy(random.randint(1, 10), bid,
                                  random.choice(traders), verbose=True)
                n_orders -= 1
                self.text.delete("1.0", tk.END)
                self.text.insert(tk.END, self.exchange.display_full())
                self.update_idletasks()
                time.sleep(0.1)
            else:
                if len(self.exchange.bids) == 0: continue
                ask = self.exchange.bids[0].price + random.randint(0, 2)
                self.exchange.sell(random.randint(1, 10), ask,
                              random.choice(traders), verbose=True)
                n_orders -= 1
                self.text.delete("1.0", tk.END)
                self.text.insert(tk.END, self.exchange.display_full())
                self.update_idletasks()
                time.sleep(0.1)

    def simulate_callback(self):
        self.simulate(10, 100, 100)



root = tk.Tk()
main = Main(master=root)
main.mainloop()

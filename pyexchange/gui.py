import random
from tkinter import ttk
import tkinter as tk
import time

from pyexchange.exchange import Exchange, Trader
from pyexchange.simulator import Simulator


class Main(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
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
        self.simulator = Simulator(n_traders=n_traders, start_price=start_price)
        while n_orders > 0:
            self.simulator.simulate_order()
            n_orders -= 1
            self.text.delete("1.0", tk.END)
            self.text.insert(tk.END, self.simulator.exchange.display_full())
            self.update_idletasks()
            time.sleep(0.1)

    def simulate_callback(self):
        self.simulate(10, 100, 100)


root = tk.Tk()
main = Main(master=root)
main.mainloop()

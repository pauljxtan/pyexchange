# pyexchange
A (very) simple object-oriented market exchange simulator in Python.

### Requirements

* Python 3
* tabulate
* tkinter

### Example

```python
from exchange import Exchange, Trader

exchange = Exchange()

aurelius = Trader("M. Aurelius", 10000, 100)
seneca = Trader("L. A. Seneca", 10000, 100)

exchange.sell(3, 99, aurelius)

print(exchange.asks)
# [[Ask: units=3, price=99, seller=[Trader: name=M. Aurelius, funds=10000, units=100]]]

exchange.buy(10, 100, seneca)

# Here Seneca buys 3 units @ 99 from Aurelius

print(exchange.bids)
# [[Bid: units=7, price=100, buyer=[Trader: name=L. A. Seneca, funds=9703, units=103]]]

print(exchange.transactions)
# [[Transaction: buyer=L. A. Seneca, seller=M. Aurelius, units=3, price=99]]

print(aurelius)
print(seneca)
# [Trader: name=M. Aurelius, funds=10297, units=97]
# [Trader: name=L. A. Seneca, funds=9703, units=103]

exchange.sell(5, 101, aurelius)
exchange.sell(3, 102, aurelius)
exchange.sell(7, 103, aurelius)
exchange.buy(6, 99, seneca)
exchange.buy(2, 98, seneca)

print(exchange.display_full())
# Mid price: 100.5  Spread: 1
# Bid volume: 15    Ask volume: 15
# +---------------+---------------+
# | Bids          | Asks          |
# +===============+===============+
# | 7 units @ 100 | 5 units @ 101 |
# +---------------+---------------+
# | 6 units @ 99  | 3 units @ 102 |
# +---------------+---------------+
# | 2 units @ 98  | 7 units @ 103 |
# +---------------+---------------+
```

### Dev notes

Reference [style guide](https://gist.github.com/sloria/7001839).
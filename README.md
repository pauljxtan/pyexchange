# pyexchange
A (very) simple object-oriented market exchange simulator in Python.

### Requirements

* Python 3
* tabulate

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
```

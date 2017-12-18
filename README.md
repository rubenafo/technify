[![PyPI version](https://badge.fury.io/py/technify.svg)](https://badge.fury.io/py/technify)
# technify
Technical analysis framework using  pandas and python.
_Technify_ provides a simple yet powerful framework to generate common technical analysis signals and custom combinations of them.

## Methods

#### Data
* Integation with [yfm](https://github.com/rubenafo/yfMongo)
* Quandl data [Quanld](https://www.quandl.com/): .fromQuandl()

#### Methods
* Moving Averages: ma()
* Exponential Moving Average: ema()
* Crossover detection: addCrossOver()

## Usage

### Loading from Quandl
```python

from technify import Stock

bitusd = Stock()\
    .fromQuandl("BCHARTS/KRAKENUSD", "Close")\
    .addEma(50, "Close")\
    .addEma(200, "Close")\
    .show(range(-60), "Close","ema50", "ema200")
```

[BitcoinUSD](https://github.com/rubenafo/technify/blob/master/imgs/sample1.png)
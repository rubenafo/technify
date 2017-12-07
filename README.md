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

### Integration with yfm library
```python
from stock import Stock
import yfm

y = yfm.fetcher()
sans = y.getTicker("san.mc")
    
s = Stock(sans).addMa(50).addMa(200)
s.addCrossover("ma50", "ma200", "50over200")
s.show("ma50", "ma200", "50over200")
```
### Quandl 
```python
from stock import Stock

usdbit = Stock.fromQuandl("BCHARTS/KRAKENEUR")
usdbit.show("c")
```

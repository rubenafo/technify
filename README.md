[![PyPI version](https://badge.fury.io/py/technify.svg)](https://badge.fury.io/py/technify)
## technify
Technical analysis framework using quandl, ta-lib and pandas library.   

_Technify_ provides a simple yet powerful framework to generate common technical analysis signals using [ta-lib](https://github.com/mrjbq7/ta-lib) and pandas visualization to explore trends in stocks data.   
The data can be provided as _ohlcv_ data or directly from [Quandl](https://www.quandl.com/) by means of the built-in integration.

# Features
* Integration with [Quandl](https://www.quandl.com/) data feed and API auth
* TA-LIB indicators
* Plotting of volume, crossing points and indicators

# Documentation
Check the most up-to-date documentation in the [wiki](https://github.com/rubenafo/technify/wiki)

# Examples

```python
from technify import Stock
from technify import indicators as ind

# The following code:
# 1) add mean average using Close column, time window = 40   
# 2) add crossing of Open column over ma40   
# 3) plot Open, ma40 and the crossing points together, limit to the last 90 values, plot volume using "Volume" column

msft = Stock.fromQuandl("EOD/MSFT") \
  .append(ind.ma, "Close", timeperiod=40, saveas="ma40")\  
  .cross("Open", "ma40", "cross") \           
  .show(["Open", "ma40", "cross"], interval=range(-90), volume="Volume") 
  
```
Some Screenshots |
-----
<img src="https://github.com/rubenafo/technify/blob/master/imgs/t1.png" width="200"> | <img src="https://github.com/rubenafo/technify/blob/master/imgs/t2.png" width="200">

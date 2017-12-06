# technify
Technical analysis framework using  pandas and python.
_Technify_ provides a simple yet powerful framework to generate common technical analysis signals and custom combinations of them.

## Methods 

* moving averages: ma()
* exponential moving average: ema()
* crossover detection

## Usage

```python
from stock import Stock
import yfm
import quandl

if __name__ == "__main__":
    y = yfm.fetcher()
    sans = y.getTicker("san.mc")
    
    s = Stock(data).addMa(50).addMa(200)
    s.addCrossover("ma50", "ma200", "50over200")
    s.show("ma50", "ma200", "50over200")
    ```

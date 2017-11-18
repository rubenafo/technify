from stock import Stock
import yfm

if __name__ == "__main__":
    y = yfm.fetcher()
    sans = y.getTicker("rya.l")
    s = Stock(sans[1:530]).addEma(50).addMa(200)
    s.addCrossover("ema50", "ma200")
    s.show("ema50", "ma200")

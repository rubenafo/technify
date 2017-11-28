from stock import Stock
import yfm

if __name__ == "__main__":
    y = yfm.fetcher()
    sans = y.getTicker("san.mc")
    s = Stock(sans[50:900]).addMa(50).addMa(200)
    s.addCrossover("ma50", "ma200", "maCross")
    s.show("ma50", "ma200", "maCross")

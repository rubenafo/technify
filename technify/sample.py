from stock import Stock
import yfm

if __name__ == "__main__":
    y = yfm.fetcher()
    sans = y.getTicker("rya.l")
    s = Stock(sans[110:150]).addMa(10).addMa(20)
    s.addCrossover("ma10", "ma20", "maCross")
    s.show( "ma10", "ma20", "maCross")

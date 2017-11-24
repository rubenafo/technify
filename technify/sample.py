from stock import Stock
import yfm

if __name__ == "__main__":
    y = yfm.fetcher()
    sans = y.getTicker("rya.l")
    s = Stock(sans[100:]).divide(100).addMa(200).addMa(20)
    s.addCrossover("ma200", "ma20", "maCross")
    s.show( "ma20", "ma200", "maCross")

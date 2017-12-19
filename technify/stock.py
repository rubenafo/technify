from technify.libs import averages as avg
import yfm as yf
import matplotlib.dates as mdates
import pandas as pd
import matplotlib.pyplot as plt
import quandl

plt.style.use('ggplot')

class Stock:

  def __init__ (self, data=None, date="date", indexIsDate=False):
    self.crossOvers = {}
    if data is not None:
        self.data = pd.DataFrame(data)
        if indexIsDate:
            self.data["date"] = data.index
            self.data.date = [d.date() for d in self.data.date]
    else:
        self.data = pd.DataFrame()

  @staticmethod
  def fromQuandl (ticker, colName=None):
    instrumentData = quandl.get(ticker)
    if colName is None:
        raise TypeError ("fromQuandl() missing colName, valid colNames:{}".format(list(instrumentData.columns)))
    if colName is not None:
        instrumentData = instrumentData[colName]
    return Stock(instrumentData, indexIsDate=True)

  def addEma (self, window, srcCol, newCol=None):
    if srcCol is None:
        raise TypeError ("fromQuandl() missing colName, valid colNames:{}".format(list(self.data.columns)))

    columnName = "ema" + str(window) if not newCol else newCol
    col = avg.Averages.ema(self.data, window, srcCol)
    self.data[columnName]= col;
    return self

  def addMa (self, window, srcCol, newCol=None):
    if len(self.data) < window:
        raise ValueError ("MA window = " + str(window) + ", max = " + str(len(self.data)))
    columnName = "ma" + str(window) if not newCol else newCol
    col = avg.Averages.ma(self.data, window, srcCol)
    self.data[columnName] = col
    return self

  def addCol (self, data, srcColName=None, dstColName=None):
    if srcColName == None:
        raise ValueError("Invalid source col name. Options={}".format(data.columns()))
    if dstColName == None:
        dstColName = srcColName
    self.data[dstColName]= data[srcColName]
    return self

  def addCrossover (self, gen1, gen2, crossName):
    low = (self.data.shift(1)[gen1] >  self.data.shift(1)[gen2]) & (self.data[gen1] < self.data[gen2])
    high = (self.data.shift(1)[gen1] < self.data.shift(1)[gen2]) & (self.data[gen1] > self.data[gen2])
    self.data[crossName+"Down"] = low
    self.data[crossName+"Up"] = high
    self.crossOvers[crossName] = gen2
    return self

  def show (self, *args):
        self.fig, self.ax = plt.subplots()
        self.ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
        self.fig.autofmt_xdate()
        colNames = []
        minRange = 0
        maxRange = len(self.data)
        for colName in args:
            if (type(colName) == range):
                minRange = colName.start
                if colName.stop < 0:
                    minRange = len(self.data) + colName.stop
                    maxRange = len(self.data)
                else:
                    maxRange = colName.stop
            elif not colName in self.crossOvers:
                self.ax.plot(self.data.date[minRange:maxRange], self.data[colName][minRange:maxRange])
                colNames.append(colName)
            else:
                cutColumn = self.crossOvers[colName]
                low = self.data[minRange:maxRange][self.data[colName+"Up"]]
                up = self.data[minRange:maxRange][self.data[colName+"Down"]]
                plt.scatter(low.date.values, low[cutColumn].values, s=165, alpha=0.6, c="green")
                plt.scatter(up.date.values, up[cutColumn].values, s=165, alpha=0.6, c="red")
        plt.legend(colNames)
        return self


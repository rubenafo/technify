
import yfm as yf
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import talib as ta
import matplotlib.pyplot as plt
import quandl

plt.style.use('ggplot')

class Stock:

  def __init__ (self, data=None, date="date", indexIsDate=False):
    self.crossOvers = {}
    self.calculatedColumns = {}
    if data is not None:
        self.data = pd.DataFrame(data)
        if indexIsDate:
            self.data["date"] = data.index
            self.data.date = [d.date() for d in self.data.date]
    else:
        self.data = pd.DataFrame()

  @staticmethod
  def fromQuandl (ticker):
    instrumentData = quandl.get(ticker)
    print ("{} - available cols:{}".format(ticker, list(instrumentData.columns)))
    return Stock(instrumentData, indexIsDate=True)

  def addFunc (self, func, cols, output=None, **kwargs):
    outputValues = []
    if len(cols) == 1:
        resultName = output or func.__name__
        outputValues = func(np.asarray(self.data[cols[0]]), **kwargs)
    elif len(cols) == 2:
        resultName = output or func.__name__
        outputValues = func(np.asarray(self.data[cols[0]]),np.asarray(self.data[cols[1]]), **kwargs)
    elif len(cols) == 3:
        resultName = func.__name__
        col0 = np.asarray(self.data["High"])
        col1 = np.asarray(self.data["Low"])
        col2 = np.asarray(self.data["Close"])
        outputValues = func(col0, col1, col2)
    for outputCol in outputValues:
        self.calculatedColumns[outputCol] = outputValues[outputCol]
    print("Calculated cols: {}".format(list(self.calculatedColumns.keys())))
    return self

  def addCol (self, data, srcColName=None, dstColName=None):
    if srcColName is None:
        raise ValueError("Invalid source col name. Options={}".format(data.columns()))
    if dstColName is None:
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
    fig, ax = plt.subplots(2,1,sharex=True)
    fig.subplots_adjust(hspace=0)
    #self.ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
    fig.autofmt_xdate()
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
            ax[0].plot(self.data.date[minRange:maxRange], self.calculatedColumns[colName][minRange:maxRange])
            colNames.append(colName)
        else:
            cutColumn = self.crossOvers[colName]
            low = self.data[minRange:maxRange][self.data[colName+"Up"]]
            up = self.data[minRange:maxRange][self.data[colName+"Down"]]
            plt.scatter(low.date.values, low[cutColumn].values, s=165, alpha=0.6, c="green")
            plt.scatter(up.date.values, up[cutColumn].values, s=165, alpha=0.6, c="red")
    ax[0].legend(colNames)
    ax[1].bar(self.data.date[minRange:maxRange], self.data["Volume (BTC)"][minRange:maxRange])
    ax[1].legend(["Volume (BTC)"])
    plt.show()
    return self


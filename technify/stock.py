
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import quandl

plt.style.use('ggplot')

class Stock:

  def __init__ (self, data=None, date="date", indexIsDate=False):
    if "QUANDL_TOKEN" in os.environ:
        quandl.ApiConfig.api_key = os.environ["QUANDL_TOKEN"]
    self.crossOvers = {}
    self.showVolume = False
    if data is not None:
        self.data = pd.DataFrame(data)
        if indexIsDate:
            self.data["date"] = data.index
            self.data.date = [d.date() for d in self.data.date]
    else:
        self.data = pd.DataFrame()

  @staticmethod
  def fromQuandl (ticker):
    if "QUANDL_TOKEN" in os.environ:
        quandl.ApiConfig.api_key = os.environ["QUANDL_TOKEN"]
    instrumentData = quandl.get(ticker)
    print (">> {} - available cols:{}".format(ticker, list(instrumentData.columns)))
    return Stock(instrumentData, indexIsDate=True)

  def append (self, func, *cols, saveas=[], **kwargs):
    outputValues = []
    if len(cols) == 1:
        outputValues = func(np.asarray(self.data[cols[0]]), **kwargs)
    elif len(cols) == 2:
        outputValues = func(np.asarray(self.data[cols[0]]),np.asarray(self.data[cols[1]]), **kwargs)
    elif len(cols) == 3:
        col0 = np.asarray(self.data[cols[0]])
        col1 = np.asarray(self.data[cols[1]])
        col2 = np.asarray(self.data[cols[2]])
        outputValues = func(col0, col1, col2, **kwargs)
    colNamesLog = []
    for i in range(len(list(outputValues.keys()))):
        outputCol = list(outputValues.keys())[i]
        newColName = saveas[i] if len(saveas) > i else outputCol
        self.data[newColName] = outputValues[outputCol]
        colNamesLog.append(newColName)
    print (">> storing {} results as [{}]".format(func.__name__, ", ".join(colNamesLog)))
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

  def show (self, *displayedCols, interval=None, volume=None, colors=[]):
    if volume is not None:
        fig, ax = plt.subplots(2,1,sharex=True)
    else:
        fig, ax = plt.subplots(1,1,sharex=True)
        ax = [ax]
    fig.subplots_adjust(hspace=0)
    #self.ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
    fig.autofmt_xdate()
    colNames = []
    minRange = 0
    maxRange = len(self.data)
    if interval is not None:
        minRange = interval.start
        if interval.stop < 0:
            minRange = len(self.data) + interval.stop
            maxRange = len(self.data)
        else:
            maxRange = interval.stop
    for i in range(len(displayedCols)):
        colName = displayedCols[i]
        if not colName in self.crossOvers:
            if colName not in self.data.columns:
                print (">> '{}' column not found in data, skipping...".format(colName))
                break
            color = colors[i] if len(colors) > i else None
            ax[0].plot(self.data.date[minRange:maxRange], self.data[colName][minRange:maxRange], color=color)
            colNames.append(colName)
        else:
            cutColumn = self.crossOvers[colName]
            low = self.data[minRange:maxRange][self.data[colName+"Up"]]
            up = self.data[minRange:maxRange][self.data[colName+"Down"]]
            plt.scatter(low.date.values, low[cutColumn].values, s=165, alpha=0.6, c="green")
            plt.scatter(up.date.values, up[cutColumn].values, s=165, alpha=0.6, c="red")
    ax[0].legend(colNames)
    if volume is not None:
        ax[1].bar(self.data.date[minRange:maxRange], self.data[volume][minRange:maxRange])
        ax[1].legend([volume])
    plt.show()
    return self


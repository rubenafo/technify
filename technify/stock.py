
import sys
sys.path.append("./libs")

from libs import averages as avg
import yfm as yf
from portfolio import Portfolio

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.dates as md
import datetime as dt
import matplotlib.dates as mdates
import quandl

plt.style.use('ggplot')

def crossover (f1, f2):
    None

class Stock:

  def __init__ (self, data,o="o", h="h", l="l", c="c", date="date", indexIsDate=False):
    self.crossOvers = {}
    self.data = pd.DataFrame(data)
    self.data = self.data.rename(columns={o:"o", h:"h", l:"l", c:"c", date:"date"})
    if indexIsDate:
        self.data["date"] = data.index
    if not len(self.data):
        raise ValueError ("initialized with empty Dataset")

  def multiply (self, value):
    self.divide(1/value)
    return self

  def divide (self, value):
    self.data["o"] = self.data["o"]/value
    self.data["h"] = self.data["h"]/value
    self.data["l"] = self.data["l"]/value
    self.data["c"] = self.data["c"]/value
    return self

  @staticmethod
  def fromQuandl (ticker):
    instrumentData = quandl.get(ticker)
    return Stock(instrumentData, o="Open", c="Close",h="High", l="Low", indexIsDate=True)

  def addEma (self, window):
    columnName = "ema" + str(window)
    col = avg.Averages.ema(self.data, window, columnName)
    self.data[columnName]= col;
    return self

  def addMa (self, window):
    if len(self.data) < window:
        raise ValueError ("MA window = " + str(window) + ", max = " + str(len(self.data)))
    columnName = "ma" + str(window)
    col = avg.Averages.ma(self.data, window, columnName)
    self.data[columnName] = col
    return self

  def append (self, data, colName):
    self.data[colName]= data
    return self

  def addCrossover (self, gen1, gen2, crossName):
    low = (self.data.shift(1)[gen1] >  self.data.shift(1)[gen2]) & (self.data[gen1] < self.data[gen2])
    high = (self.data.shift(1)[gen1] < self.data.shift(1)[gen2]) & (self.data[gen1] > self.data[gen2])
    self.data[crossName+"Down"] = low
    self.data[crossName+"Up"] = high
    self.crossOvers[crossName] = gen2
    return self

  def show (self, *args):
        colNames = []
        for colName in args:
            if not colName in self.crossOvers:
                plt.plot(self.data.date, self.data[colName])
                colNames.append(colName)
            else:
                cutColumn = self.crossOvers[colName]
                low = self.data[self.data[colName+"Up"]]
                up = self.data[self.data[colName+"Down"]]
                plt.scatter(low.date.values, low[cutColumn].values, s=165, alpha=0.6, c="green")
                plt.scatter(up.date.values, up[cutColumn].values, s=165, alpha=0.6, c="red")
        plt.legend(colNames)


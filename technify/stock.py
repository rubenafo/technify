
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

plt.style.use('ggplot')

def crossover (f1, f2):
    None

class Stock:

  def __init__ (self, data):
    self.data = pd.DataFrame(data)
    if not len(self.data):
        raise ValueError ("initialized with empty Dataset")

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

  def addCrossover (self, gen1, gen2):
    low = (self.data.shift(1)[gen1] >  self.data.shift(1)[gen2]) & (self.data[gen1] < self.data[gen2])
    high = (self.data.shift(1)[gen1] < self.data.shift(1)[gen2]) & (self.data[gen1] > self.data[gen2])
    self.data["down"] = low
    self.data["up"] = high
    return self

  def show (self, col1, col2):
        plt.plot(self.data.date, self.data.c)
        plt.plot(self.data.date, self.data[col1])
        plt.plot(self.data.date, self.data[col2])
        plt.legend(["close", col1, col2])
        l = self.data[self.data.down]
        h = self.data[self.data.up]
        plt.scatter(l.date.values, l[col1].values, s=165, alpha=0.6, edgecolors="b")
        plt.scatter(h.date.values,h[col2].values, s=165, alpha=0.6, edgecolors="g")
        plt.show()



    #p = Portfolio(s)
    #buyHold = p.getBuyAndHold()
    #print (buyHold)
    #emaHold = p.getBuySellStrategy()
    #print(emaHold)
    #print (p.getRelativeReturn(emaHold, buyHold))


  #ax.text(dt.date(2011, 11, 9), 10, "World",fontsize=19)

  ###low = (ts.loc[(ts.shift(1)["ema50"] >  ts.shift(1)["ema400"]) &
  ###             (ts["ema50"] < ts["ema400"])])
  ###high = (ts.loc[(ts.shift(1)["ema50"] < ts.shift(1)["ema400"]) &
  ###             (ts["ema50"] > ts["ema400"])])

  ###plt.scatter(low.date.values, low.ema50.values, s=165, alpha=0.6, edgecolors="g")
  ###plt.scatter(high.date.values,high.ema50.values, s=165, alpha=0.6, edgecolors="b")

  #ax.add_artist(plt.Circle((dt.date(2011,10,2),7), radius=1, color='g'))

  #ax.add_artist(plt.Ellipse((10, 10), (0.2,0.5), color='r'))
  #ax.text(pd.Timestamp("2011-11-10"), 7, "!!!")
  #ax.annotate('Test', (mdates.date2num(dt.date(2011,10,1)), 7), xytext=(25, 25),
  #          textcoords='offset points', arrowprops=dict(arrowstyle='-|>'))
  ###plt.show()
  #print(ts.loc[(ts.shift(1)["ema50"] < ts.shift(1)["ema400"]) &
  #             (ts["ema50"] > ts["ema400"])])


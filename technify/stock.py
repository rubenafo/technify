import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import quandl
import datetime
import matplotlib.dates as mdates
from . import utils

plt.style.use('ggplot')


class Stock:

    def __init__(self, data=None, indexIsDate=False):
        if "QUANDL_TOKEN" in os.environ:
            quandl.ApiConfig.api_key = os.environ["QUANDL_TOKEN"]
        self.crossovers = {}
        self.showVolume = False
        if data is not None:
            self.data = pd.DataFrame(data, dtype=float)
            if indexIsDate:
                self.data["date"] = data.index
                self.data.date = [d.date() for d in self.data.date]
                self.data.index = range(len(self.data))
        else:
            self.data = pd.DataFrame()
        print(">> Stock - available cols:{}".format(list(self.data.columns)))

    @staticmethod
    def fromQuandl(ticker):
        if "QUANDL_TOKEN" in os.environ:
            quandl.ApiConfig.api_key = os.environ["QUANDL_TOKEN"]
        instrumentData = quandl.get(ticker)
        return Stock(instrumentData, indexIsDate=True)

    # Append indicator
    #
    def append(self, func, cols, saveas=[], **kwargs):
        cols = [cols] if type(cols) is not list else cols
        saveas = [saveas] if type(saveas) is not list else saveas
        outputValues = []
        arraycols = list(map(lambda c: np.asarray(self.data[c]), cols))
        if len(cols) == 1:
            outputValues = func(arraycols[0], **kwargs)
        elif len(cols) == 2:
            outputValues = func(arraycols[0], arraycols[1], **kwargs)
        elif len(cols) == 3:
            outputValues = func(arraycols[0], arraycols[1], arraycols[2], **kwargs)
        colNamesLog = []
        for i in range(len(list(outputValues.keys()))):
            outputCol = list(outputValues.keys())[i]
            newColName = saveas[i] if len(saveas) > i else outputCol
            self.data[newColName] = outputValues[outputCol]
            colNamesLog.append(newColName)
        print(">> storing {} results as [{}]".format(func.__name__, ", ".join(colNamesLog)))
        return self

    def addCol(self, data, srcColName=None, dstColName=None):
        if srcColName is None:
            raise ValueError("Invalid source col name. Options={}".format(data.columns()))
        if dstColName is None:
            dstColName = srcColName
        self.data[dstColName] = data[srcColName]
        return self

    def cross(self, gen1, gen2, crossName):
        high = (self.data.shift(1)[gen1] > self.data.shift(1)[gen2]) & (self.data[gen1] < self.data[gen2])
        low = (self.data.shift(1)[gen1] < self.data.shift(1)[gen2]) & (self.data[gen1] > self.data[gen2])
        self.data[crossName + "Down"] = low
        self.data[crossName + "Up"] = high
        self.crossovers[crossName] = (gen1, gen2)
        print(">> storing {} crossing {} as [{}, {}]".format(gen1, gen2, crossName + "Down", crossName + "Up"))
        return self

    # Infer how many subplots we need
    #
    def inferPlots(self, colNames, volume):
        plots = {}
        for i in range(len(colNames)):
            colName = colNames[i]
            if i not in plots:
                plots[i] = [colName] if type(colName) is not list else colName
            else:
                plots[i].append(colName)
        if volume is not None:
            plots[len(plots)] = [volume]
        fig, pls = plt.subplots(len(plots), 1, sharex=True)
        if len(plots) == 1:
            pls = [pls]
        return plots, fig, pls

    def show(self, *displayedCols, interval=None, volume=None, colors=[]):
        plotGroups, fig, plots = self.inferPlots(displayedCols, volume)
        fig.subplots_adjust(hspace=0)
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
        for i in plotGroups:
            colGroup = plotGroups.get(i)
            for colName in colGroup:
                if not colName in self.crossovers:
                    if colName not in self.data.columns:
                        print(">> '{}' column not found in data, skipping...".format(colName))
                        break
                    color = colors[i + colGroup.index(colName)] if len(colors) > i else None
                    if colName == volume:
                        plots[i].bar(self.data.date[minRange:maxRange], self.data[volume][minRange:maxRange])
                    else:
                        plots[i].plot(self.data.date[minRange:maxRange], self.data[colName][minRange:maxRange],
                                      color=color)
                    colNames.append(colName)
                else:
                    low = self.data[minRange:maxRange]
                    low = low[low[colName + "Up"]]
                    up = self.data[minRange:maxRange]
                    up = up[up[colName + "Down"]]
                    upx,upy = self.updateDate(up, self.data, colName)
                    downx,downy = self.updateDate(low, self.data, colName)
                    plots[i].scatter(downx, downy, s=165, alpha=0.6, c="red")
                    plots[i].scatter(upx, upy, s=165, alpha=0.6, c="green")
            plots[i].legend(colGroup)
        plt.show()
        return self

    def updateDate (self, df, dates, colname):
        crossingcol = self.crossovers[colname][0]
        crossedcol = self.crossovers[colname][1]
        upindexes = list(df.index)
        upindexes.extend([u-1 for u in upindexes])
        upindexes.sort()
        alldates = dates.loc[upindexes]
        pairs = list(utils.grouper(upindexes, 2))
        resultx = []
        resulty = []
        for pair in pairs:
            prev = alldates.loc[pair[0]]
            post = alldates.loc[pair[1]]
            date0 = mdates.date2num(prev.date)
            date1 = mdates.date2num(post.date)
            o0 = prev[crossingcol]
            o1 = post[crossingcol]
            c0 = prev[crossedcol]
            c1 = post[crossedcol]
            intersect = utils.intersection(utils.line([date0,o0],[date1,o1]), utils.line([date0,c0],[date1,c1]))
            resultx.append(intersect[0])
            resulty.append(intersect[1])
        return resultx,resulty

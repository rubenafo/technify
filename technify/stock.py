import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import quandl
import datetime

plt.style.use('ggplot')


class Stock:

    def __init__(self, data=None, indexIsDate=False):
        if "QUANDL_TOKEN" in os.environ:
            quandl.ApiConfig.api_key = os.environ["QUANDL_TOKEN"]
        self.crossOvers = {}
        self.showVolume = False
        if data is not None:
            self.data = pd.DataFrame(data)
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
        print(">> {} - available cols:{}".format(ticker, list(instrumentData.columns)))
        return Stock(instrumentData, indexIsDate=True)

    # Append indicator
    #
    def append(self, func, *cols, saveas=[], **kwargs):
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
        self.crossOvers[crossName] = (gen1, gen2)
        print(">> storing {}-{} crossver as {}".format(gen1, gen2, crossName))
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
        for i in plotGroups:
            colGroup = plotGroups.get(i)
            for colName in colGroup:
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
            plots[i].legend(colGroup)
        plt.show()
        return self

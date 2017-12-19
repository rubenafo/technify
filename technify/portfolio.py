#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: return, alpha, beta, sharpe, sortino, drawdown, volatility

import pandas as pd
import math

class Portfolio:

    # The stock dataframe contains ohlc values plus down and up columns
    # indicating when to buy and when to sell
    def __init__(self, stock):
        self.data = stock.data
        self.history = []

    def getRelativeReturn (self, strategy1, strategy2):
        return (strategy1 - strategy2) / strategy2

    def debug (self, buy, price, date, qty, inventory, cash):
        if buy:
            self.history.append({"date":date, "op":"buy", "price":price, "qty":qty, "inventory":inventory, "cash":cash})
        else:
            self.history.append({"date":date,"op":"sell", "price":price, "qty":qty, "inventory":inventory, "cash":cash})

    def getBuyAndHold (self, budget=10000):
        initQty = math.floor(budget / self.data.iloc[0].o)
        initValue = initQty * float(self.data.head(1).o)
        endValue = initQty * float(self.data.tail(1).c)
        returnPerc = (endValue - initValue) * 100 / initValue
        return endValue, str(returnPerc) + "%"

    def getBuySellStrategy (self, budget=10000, buyOnStart=False, sellOnEnd=False):
        self.history.clear()
        availableBudget = budget
        inventory = 0
        if buyOnStart:
            inventory = math.floor(availableBudget / self.dframe.iloc[0].o)
            availableBudget = availableBudget - (inventory * self.dframe.iloc[0].o)
            row = self.dframe.iloc[0]
            self.debug(True, row.o, row.date, inventory, inventory, availableBudget)
        for index in range(0, len(self.dframe)):
            row = self.dframe.loc[index]
            if row.up == True and availableBudget > 0:
                purchased = math.floor(availableBudget / row.c)
                availableBudget -= purchased * row.c
                inventory += purchased
                self.debug(True, row.c, row.date, purchased, inventory, availableBudget)
            elif row.down == True and inventory > 0:
                availableBudget += row.c * inventory
                inventory = 0
                self.debug(False, row.c, row.date, inventory, inventory, availableBudget)
        if sellOnEnd:
            availableBudget += inventory * self.dframe.iloc[-1].c
            inventory= 0
        returnVal = availableBudget + inventory*(self.dframe.iloc[-1].c)
        return returnVal


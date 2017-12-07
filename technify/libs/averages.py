# Copyright 2017 Ruben Afonso, http://www.figurebelow.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from technify.libs.vectors import Vectors
from technify.libs.windowOp import WindowOp

import numpy as np

class Averages:

  # This auxiliary function is used in MA
  @staticmethod
  def sumWindow (series):
    return Vectors.avgVector (series)

  @staticmethod
  def ma (df, period, columName="ma"):
    ma = (df.c.rolling(period).mean())
    return ma

  @staticmethod
  def ema (df, period, newField="ema"):
    result = []
    for i in range(period-1):
      result.append(np.nan)
    k = (2.0/(period+1))
    initSlice = df[0:period]
    previousDay = Vectors.avgVector(initSlice)
    result.append(previousDay)
    emaSlice = df[period:]
    for index, i in emaSlice.iterrows():
        previousDay = i["c"] * float(k) + previousDay * float((1-k))
        result.append(previousDay)
    return result


  @staticmethod
  def weightSum (series, weights):
    result = 0
    for i in range(len(series)):
      result += series[i] * weights[i]
    return float(result/len(weights))

  @staticmethod
  def wma (series, weights):
    result = []
    for i in range(len(weights), len(series)+1):
      windowVal = Averages.weightSum (series[i-len(weights):i], weights)
      result.append (windowVal)
    return result

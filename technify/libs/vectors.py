# Copyright 2014 Ruben Afonso, http://www.figurebelow.com
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

class Vectors:

  @staticmethod
  def diffVectors (series1, series2):
    result = [];
    if (len(series1) != len(series2)):
      raise Exception("Invalid series length")
    for i in range(len(series1)):
      result.append(series1[i] - series2[i])
    return result

  @staticmethod
  def powVector (serie):
    result = []
    for value in serie:
      result.append (pow(value,2))
    return result

  @staticmethod
  def absVector (serie):
    result = []
    for value in serie:
      result.append(abs(value))
    return result

  @staticmethod
  def divVectors (serie1, serie2):
    result = []
    if (len(serie1) != len(serie2)):
      raise Exception("Invalid series length")
    for i in range(len(serie1)):
      result.append (serie1[i] / float(serie2[i]))
    return result

  @staticmethod
  def combineVectors (serie1, serie2, fun):
    result = []
    if len(serie1) != len(serie2) | len(serie1) + len(serie2) < 2:
      raise Exception("Invalid series length")
    for i in range(len(serie1)):
      result.append (fun(serie1[i], serie2[i]))
    return result






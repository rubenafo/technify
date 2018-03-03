import talib as ta

## Momentum functions

def adx(high, low, close, timeperiod=14):
    return {"adx": ta.ADX(high, low, close, timeperiod)}


def adxr(high, low, close, timeperiod=14):
    return {"adxr": ta.ADXR(high, low, close, timeperiod)}


def apo(col, fastperiod=12, slowperiod=26, matype=0):
    return {"apo": ta.APO(col, fastperiod, slowperiod, matype)}


def aroon(high, low, timeperiod=14):
    values = ta.AROON(high, low, timeperiod)
    return {"aroondown": values[0], "aroonup": values[1]}


def aroonosc(high, low, timeperiod=14):
    return {"aroonosc": ta.AROONOSC(high, low, timeperiod)}


def bop(open, high, low, close):
    return {"bop": ta.BOP(open, high, low, close)}


def cci(high, low, close, timeperiod=14):
    return {"cci": ta.CCI(high, low, close, timeperiod)}


def cmo(col, timeperiod=14):
    return {"cmo": ta.CMO(col, timeperiod)}


def dx(high, low, close, timeperiod=14):
    return {"dx": ta.DX(high, low, close, timeperiod)}


def macd(col, fastperiod=12, slowperiod=26, signalperiod=9):
    values = ta.MACD(col, fastperiod, slowperiod, signalperiod)
    return {"macd": values[0], "macdsignal": values[1], "macdhist": values[2]}


def macdext(col, fastperiod=12, fastmatype=0, slowperiod=26, slowmatype=0,
            signalperiod=9, signalmatype=0):
    values = ta.MACDEXT(col, fastperiod, fastmatype, slowperiod, slowmatype, signalperiod)
    return {"macd": values[0], "macdsignal": values[1], "macdhist": values[2]}


def macdfix(col, signalperiod=9):
    values = ta.MACDFIX(col, signalperiod)
    return {"macd": values[0], "macdsignal": values[1], "macdhist": values[2]}


def mfi(high, low, close, volume, timeperiod=14):
    return {"mfi": ta.MFI(high, low, close, volume, timeperiod)}


def minusDI(high, low, close, timeperiod=14):
    return {"minusdi": ta.MINUS_DI(high, low, close, timeperiod)}


def minusDM(high, low, timeperiod=14):
    return {"minusdm": ta.MINUS_DM(high, low, timeperiod)}


def mom(col, timeperiod=10):
    return {"mom": ta.MOM(col, timeperiod)}


def plusDI(high, low, close, timeperiod=14):
    return {"plusdi": ta.PLUS_DI(high, low, close, timeperiod)}


def plusDM(high, low, timeperiod=14):
    return {"plusdm": ta.PLUS_DM(high, low, timeperiod)}


def ppo(col, fastperiod=12, slowperiod=26, matype=0):
    return {"ppo": ta.PPO(col, fastperiod, slowperiod, matype)}


def roc(col, timeperiod=10):
    return {"roc": ta.ROC(col, timeperiod)}


def rocp(col, timeperiod=10):
    return {"rocp": ta.ROCP(col, timeperiod)}


def rocr(col, timeperiod=10):
    return {"rocr": ta.ROCR(col, timeperiod)}


def rocr100(col, timeperiod=10):
    return {"rocr100": ta.ROCR100(col, timeperiod)}


def rsi(col, timeperiod=10):
    return {"rsi": ta.RSI(col, timeperiod)}


def stoch(high, low, close, fastk_period=5, slowk_period=3, slowk_matype=0,
          slowd_period=3, slowd_matype=0):
    values = ta.STOCH(high, low, close, fastk_period, slowk_period, slowk_matype,
                      slowd_period, slowd_matype)
    return {"slowk": values[0], "slowd": values[1]}


def stochf(high, low, close, fastk_period=5, fastd_period=3, fastd_matype=0):
    values = ta.STOCHF(high, low, close, fastk_period, fastd_period, fastd_matype)
    return {"fastk": values[0], "fastd": values[1]}


def stochrsi(col, fastk_period=5, fastd_period=3, fastd_matype=0):
    values = ta.STOCHRSI(col, fastk_period, fastd_period, fastd_matype)
    return {"fastk": values[0], "fastd": values[1]}


def trix(col, timeperiod=30):
    return {"trix": ta.TRIX(col, timeperiod)}


def ultosc(high, low, close, timeperiod1=7, timeperiod2=14, timeperiod3=28):
    return {"ultosc": ta.ULTOSC(high, low, close, timeperiod1, timeperiod2, timeperiod3)}


def willr(high, low, close, timeperiod=14):
    return {"willr": ta.WILLR(high, low, close, timeperiod)}


## Volume indicators

def ad(high, low, close, volume):
    return {"ad": ta.AD(high, low, close, volume)}


def adosc(high, low, close, volume, slowperiod=3, fastperiod=10):
    return {"adosc": ta.ADOSC(high, low, close, volume, slowperiod, fastperiod)}


def obv(close, volume):
    return {"obv": ta.OBV(close, volume)}


## Volatility indicators

def atr(high, low, close, timeperiod=14):
    return {"atr": ta.ATR(high, low, close, timeperiod)}


def natr(high, low, close, timeperiod=14):
    return {"natr": ta.NATR(high, low, close, timeperiod)}


def trange(high, low, close):
    return {"trange": ta.TRANGE(high, low, close)}


## Cycle indicators

def ht_dcperiod(col):
    return {"htdc": ta.HT_DCPERIOD(col)}


def ht_dcphase(col):
    return {"htcdphase": ta.HT_DCPHASE(col)}


def ht_phasor(col):
    values = ta.HT_PHASOR(col)
    return {"inphase": values[0], "quadrature": values[1]}


def ht_sine(col):
    values = ta.HT_SINE(col)
    return {"sine": values[0], "leadsine": values[1]}


def ht_trendmode(col):
    return {"httrendmode": ta.HT_TRENDMODE(col)}

# Overlap indicators

def bbands(col, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0):
    values = ta.BBANDS(col, timeperiod, nbdevup, nbdevdn, matype)
    return {"bbands_ub":values[0], "bbands_mb":values[1], "bbands_lb":values[2]}


def dema(col, timeperiod=30):
    values = ta.DEMA(col, timeperiod)
    return {"dema":values}


def ema(col, timeperiod=30):
    values = ta.EMA(col, timeperiod)
    return {"ema":values}


def trendline(col):
    return {"trendline":ta.HT_TRENDLINE(col)}


def kama(col, timeperiod=30):
    values = ta.KAMA(col, timeperiod)
    return {"kama": values}


def ma(col, timeperiod=30):
    values = ta.MA(col, timeperiod)
    return {"ma":values}


def mama(col, fastlimit=0.05, slowlimit=0.05):
    values = ta.MAMA(col, fastlimit, slowlimit)  # output mama, fama
    return {"mama":values[0], "fama":values[1]}


def mavp(real, periods, minperiod=2, maxperiod=30, matype=0):
    values = ta.MAVP(real, periods, minperiod, maxperiod, matype)
    return {"mavp":values}


def midpoint(col, timeperiod=14):
    values = ta.MIDPOINT(col, timeperiod)
    return {"midpoint":values}


def midprice(high, low, timeperiod=14):
    return {"midprice": ta.MIDPRICE(high, low, timeperiod)}


def sar(high, low, acceleration=0.02, maximum=0.2):
    return {"sar":ta.SAR(high, low, acceleration, maximum)}


def sarext(high, low, startvalue=0, offsetonreverse=0, accelerationinitlong=0.02, accelerationlong=0.02,
           accelerationmaxlong=0.2, accelerationinitshort=0.02, accelerationshort=0.02, accelerationmaxshort=0.2):
    values = ta.SAREXT(high, low, startvalue, offsetonreverse, accelerationinitlong, accelerationlong,
                     accelerationmaxlong, accelerationinitshort, accelerationshort, accelerationmaxshort)
    return {"sarext":values}


def sma(col, timeperiod=30):
    return {"sma":ta.SMA(col, timeperiod)}


def t3(col, timeperiod=5, vfactor=0.7):
    return {"t3": ta.T3(col, timeperiod, vfactor)}


def tema(col, timeperiod=30):
    return {"tema": ta.TEMA(col, timeperiod)}


def trima(col, timeperiod=30):
    return {"trima": ta.TRIMA(col, timeperiod)}


def wma(col, timeperiod=30):
    return {"wma": ta.WMA(col, timeperiod)}

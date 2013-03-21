import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from qstkutil import DataAccess as da
from qstkutil import qsdateutil as du
from qstkutil import tsutil as tsu
import datetime as dt

def allocations(slots):
  def allocations_recursive(slots, next_slot, allocated, remained):
    if next_slot == slots - 1:
      allocated[next_slot] = remained
      yield allocated

      allocated[next_slot] = 0.0
      return

    alloc = 0.0
    while alloc <= remained:
      allocated[next_slot] = alloc
      remained -= alloc

      for a in allocations_recursive(slots, next_slot+1, allocated, remained):
        yield a

      allocated[next_slot] = 0.0
      remained += alloc

      alloc += 0.1

  for a in allocations_recursive(slots, 0, [.0]*slots, 1.0):
    yield a

def optimize(symbols, startday, endday):
  best_sharpe = -10000.0
  best_alloc = None

  for allocation in allocations(len(symbols)):
    result = simulate(symbols, allocation, startday, endday)
    if result["sharpe"] > best_sharpe:
      best_sharpe = result["sharpe"]
      best_alloc = list(allocation)

  print best_alloc
  print simulate(symbols, best_alloc, startday, endday)

def simulate(symbols, allocations, startday, endday):
  """
  @symbols: list of symbols
  @allocations: list of weights
  @startday: ...
  @endday: ...
  """
  timeofday = dt.timedelta(hours=16)
  timestamps = du.getNYSEdays(startday,endday,timeofday)

  dataobj = da.DataAccess('Yahoo')
  close = dataobj.get_data(timestamps, symbols, "close", verbose=False)
  close = close.values
  norm_close = close / close[0, :]

  allocations = allocations / np.sum(allocations)

  portfolio_value = np.dot(norm_close, allocations)
  portfolio_return = portfolio_value.copy()
  tsu.returnize0(portfolio_return)

  sharpe = tsu.get_sharpe_ratio(portfolio_return)
  accum = portfolio_value[-1] / portfolio_value[0]
  average = np.mean(portfolio_return)
  stddev = np.std(portfolio_return)

  result = {"sharpe":sharpe, "cumulative_return":accum, "average":average, "stddev":stddev}

  return result

if __name__ == "__main__":
  print "testing simulate function ..."

  symbols = ["AAPL","GOOG","XOM","GLD"]
  startday = dt.datetime(2011, 1, 1)
  endday = dt.datetime(2011, 12, 31)
  print simulate(symbols, [0.4, 0.0, 0.2, 0.4], startday, endday)

  startday = dt.datetime(2010, 1, 1)
  endday = dt.datetime(2010, 12, 31)
  symbols = ["AXP","HPQ","IBM","HNZ"]
  print simulate(symbols, [.0,.0,.0,0.1], startday, endday)

  print ""
  print "testing portfolio optimizer ..."

  # See "http://wiki.quantsoftware.org/index.php?title=CompInvestI_Homework_1"
  symbols = ["AAPL","GOOG","XOM","GLD"]
  startday = dt.datetime(2011, 1, 1)
  endday = dt.datetime(2011, 12, 31)
  optimize(symbols, startday, endday)

  startday = dt.datetime(2010, 1, 1)
  endday = dt.datetime(2010, 12, 31)
  symbols = ["AXP","HPQ","IBM","HNZ"]
  optimize(symbols, startday, endday)

  # Now the quiz
  startday = dt.datetime(2010, 1, 1)
  endday = dt.datetime(2010, 12, 31)
  symbols = ["C", "GS", "IBM", "HNZ"]
  optimize(symbols, startday, endday)

  startday = dt.datetime(2011, 1, 1)
  endday = dt.datetime(2011, 12, 31)
  symbols = ["BRCM", "TXN", "IBM", "HNZ"]
  optimize(symbols, startday, endday)


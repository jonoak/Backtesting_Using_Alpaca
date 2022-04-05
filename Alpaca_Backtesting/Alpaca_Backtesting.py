'''
Jonathan Oakey
import Alpaca_Backtesting as AB
AB.Test_Backtesting_AllWeatherStrategy()




A famous rebalancing strategy is called the All Weather Portfolio by Ray Dalio. It attempts to produce steady returns through all market conditions by investing in a variety of sectors.

params:
       strategy: the strategy you wish to backtest, an instance of backtrader.Strategy
       symbols: the symbol (str) or list of symbols List[str] you wish to backtest on
       start: start date of backtest in format 'YYYY-MM-DD'
       end: end date of backtest in format: 'YYYY-MM-DD'
       timeframe: the timeframe the strategy trades on (size of bars) -
                   1 min: TimeFrame.Minute, 1 day: TimeFrame.Day, 5 min: TimeFrame(5, TimeFrameUnit.Minute)
       cash: the starting cash of backtest
 '''

from alpaca_trade_api.rest import REST, TimeFrame
from alpaca_trade_api.stream import Stream
import backtrader as bt
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 150

def run_backtest(strategy, symbols, start, end, timeframe=TimeFrame.Day, cash=10000):

  # initialize backtrader broker
  cerebro = bt.Cerebro(stdstats=True)
  cerebro.broker.setcash(cash)

  # add strategy
  cerebro.addstrategy(strategy)

  # add analytics
  # cerebro.addobserver(bt.observers.Value)
  # cerebro.addobserver(bt.observers.BuySell)
  cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='mysharpe')
  # historical data request
  if type(symbols) == str:
    symbol = symbols
    alpaca_data = rest_api.get_bars(symbol, timeframe, start, end, adjustment='all').df
    data = bt.feeds.PandasData(dataname=alpaca_data, name=symbol)
    cerebro.adddata(data)
  elif type(symbols) == list or type(symbols) == set:
    for symbol in symbols:
      alpaca_data = rest_api.get_bars(symbol, timeframe, start, end, adjustment='all').df
      data = bt.feeds.PandasData(dataname=alpaca_data, name=symbol)
      cerebro.adddata(data)


  # run
  initial_portfolio_value = cerebro.broker.getvalue()
  print(f'Starting Portfolio Value: {initial_portfolio_value}')
  results = cerebro.run()
  final_portfolio_value = cerebro.broker.getvalue()
  print(f'Final Portfolio Value: {final_portfolio_value} ---> Return: {(final_portfolio_value/initial_portfolio_value - 1)*100}%')

  strat = results[0]
  print('Sharpe Ratio:', strat.analyzers.mysharpe.get_analysis()['sharperatio'])
  cerebro.plot(iplot= False)


class AllWeatherStrategy(bt.Strategy):

   def __init__(self):
       # the last year we rebalanced (initialized to -1)
       self.year_last_rebalanced = -1 
       self.weights = stocks_and_weights

   def next(self):
       # if we’ve already rebalanced this year
       if self.datetime.date().year == self.year_last_rebalanced:
           return
       # update year last balanced
       self.year_last_rebalanced = self.datetime.date().year
       # enumerate through each security
       for i,d in enumerate(self.datas):
           # rebalance portfolio with desired target percents
           symbol = d._name
           self.order_target_percent(d, target=self.weights[symbol])


def Test_Backtesting_AllWeatherStrategy():
  print("whats your Alpaca API_KEY?")
  API_KEY = input()
  print("whats your Alpaca SECRET_KEY?")
  SECRET_KEY = input()
  import os
  os.system("pip install -r requirements.txt")
  rest_api = REST(API_KEY, SECRET_KEY, 'https://paper-api.alpaca.markets')
  print("list the stocks you want to backtest, seperate them by a comma")
  the_stocks = input()
  the_stocks = the_stocks.split(',')
  stocks_and_weights = {}
  for x in the_stocks:
    print('how much weight for '+ x + " ? (enter a number between 1 and 100")
    the_weight = input()
    stocks_and_weights[x] = float(the_weight) / 100
  print("enter a start date (ex 2015-01-01)")
  start_date = input()
  print("enter a end date (ex 2021-11-01)")
  end_date = input()
  print("enter a the starting capital (ex 10000)")
  starting_capital = int(input())
  run_backtest(AllWeatherStrategy, the_stocks , start_date, end_date, TimeFrame.Day, starting_capital)



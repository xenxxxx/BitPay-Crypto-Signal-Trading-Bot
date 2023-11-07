# import coin as coin
import pandas as pd
from binance.client import Client
import matplotlib.pyplot as plt
from finta import TA
from threading import Thread
import numpy as np
import plotly.graph_objects as go
from Telegram.TelegramBot import *
from decouple import Config, RepositoryEnv


#const values
API_KEY = env.get('API_KEY')
SECRET_API = env.get('SECRET_API')
client = Client(API_KEY, SECRET_API)


class Coin:

    def __init__(self, symbol, interval='1d', indicators: bool = False, HA: bool = False):
        """
        initializing the coin dataframe when we fix the ['open', 'high', 'low', 'close', 'volume'] cols to be float in order to work with TA
        valid intervals - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M

        :param symbol:string, the symbol of the coin
        :param indicators: True if to indicators in the initialization else just create the object without indicators
        :param interval:string, the time interval of the dataframe when the defualt is 1d
        """
        self.__symbol = symbol
        self.__interval = interval
        #candle = client.get_historical_klines(symbol, interval, client._get_earliest_valid_timestamp(symbol ,interval)) # for spot
        self.__candle = client.futures_historical_klines(symbol, interval, client._get_earliest_valid_timestamp(symbol, interval))# for futures
        self.__df = pd.DataFrame(self.__candle, columns=['Date', 'open', 'high', 'low', 'close', 'volume', 'closeTime', 'quoteAssetVolume', 'numberOfTrades', 'takerBuyBaseVol', 'takerBuyQuoteVol', 'ignore'])
        self.__df['Date'] = pd.to_datetime(self.__df['Date']/1000, unit="s")
        self.__df['closeTime'] = pd.to_datetime(self.__df['closeTime']/1000, unit="s")
        numeric_columns = ['open', 'high', 'low', 'close', 'volume', 'quoteAssetVolume', 'takerBuyBaseVol', 'takerBuyQuoteVol']
        self.__df[numeric_columns] = self.__df[numeric_columns].apply(pd.to_numeric, axis=1)

        if HA:
            # make the candles Heinki Ashi
            self.__HA()

        if indicators:
            self.__additional_indicators()


    def __del__(self):
        print("coin obj {} has been deleted".format(self.__symbol))

    # --- private methods ---

    def __additional_indicators(self):
        self.__df['RSI'] = TA.RSI(self.__df, period=14)
        self.__df['RSI_EMA'] = self.__df['RSI'].ewm(span=14).mean()
        self.__df['EMA_FAST'] = TA.EMA(self.__df, period=8)
        self.__df['EMA_SLOW'] = TA.EMA(self.__df, period=21)
        self.__df['SMA200'] = TA.SMA(self.__df, period=200)
        self.__df['ATR'] = TA.ATR(self.__df, period=10)
        self.__df['MACD'] = TA.MACD(self.__df, period_fast=13, period_slow=21, signal=5)['MACD'] - TA.MACD(self.__df, period_fast=13, period_slow=21, signal=5)['SIGNAL']
        self.__support = self.__Add_Support()
        self.__resistance = self.__Add_Resistance()
        self.__fib = self.__Fib_Level()

    def __HA(self):
        df = self.__df.copy()
        df['c'] = (df['open'] + df['high'] + df['low'] + df['close']) / 4
        df['o'] = ((df['open'] + df['close']) / 2).shift(1)
        df.iloc[0, -1] = df['o'].iloc[1]
        df['h'] = df[['high', 'o', 'c']].max(axis=1)
        df['l'] = df[['low', 'o', 'c']].min(axis=1)
        self.__df['open'], self.__df['high'], self.__df['low'], self.__df['close'] = df['o'], df['h'], df['l'], df['c']
        #df.drop(['o', 'h', 'l', 'c'], axis=1)
        del df

    def __Fib_Level(self):
        """
        Taking the last 233 candles, finding the min and the max from them, adding fib series level
        notice the formula is for Uptrend Retracement ! -> UR = H - ((H-L) * percentage)
        [1, 0.88, 0.786, 0.618, 0.5, 0.328, 0]
        :return: List, fib series prices from the lowest to the highest
        """
        flag = False
        for i in [233, 144, 89]:
            try:
                H = max(self.get_df()['high'].iloc[-i:])
                L = min(self.get_df()['low'].iloc[-i:])
                x = lambda h, l, p: h-((h-l)*p)
                fib = [L, x(H, L, 0.88), x(H, L, 0.786), x(H, L, 0.618), (H+L) * 0.5, x(H, L, 0.382), H]
                #print(f"{self.__symbol}\t {fib}, {self.last('close')}")
                flag = True

            except:
                print(f"can do fib with {i}")
            finally:
                if flag:    return fib
                else:
                    continue
        # in case fib series was not possible
        return [0, 0, 0, 0, 0, 0, 0]

    def __isFarFromLevel(self, l, levels):
        return np.sum([abs(l - x) < np.mean(self.__df['high'] - self.__df['low']) for x in levels]) == 0

    def __Add_Support(self):
        """
        Adding support levels to the dataframe
        :return:
        """
        levels = []

        def isSupport(df, i):
            return df['low'][i] < df['low'][i - 1] and df['low'][i] < df['low'][i + 1] and df['low'][i + 1] < df['low'][i + 2] and df['low'][i - 1] < df['low'][i - 2]

        for i in range(2, self.__df.shape[0] - 2):
            if isSupport(self.__df, i):
                l = self.__df['low'][i]
                if self.__isFarFromLevel(l, levels):
                    levels.append((i, l))
        return levels

    def __Add_Resistance(self):
        """
        Adding resistance levels to the dataframe
        :return:
        """
        levels = []

        def isResistance(df, i):
            return df['high'][i] > df['high'][i - 1] and df['high'][i] > df['high'][i + 1] and df['high'][i + 1] > df['high'][i + 2] and df['high'][i - 1] > df['high'][i - 2]

        for i in range(2, self.__df.shape[0] - 2):
            if isResistance(self.__df, i):
                l = self.__df['high'][i]
                if self.__isFarFromLevel(l, levels):
                    levels.append((i, l))
        return levels

    # --- public methods ---

    def RSI_plot(self):
        """
        will display the RSI of the coin with lines of the oversold & overbought
        :return:
        """
        #self.df['RSI'] = TA.RSI(self.df, period=14)
        fig, ax = plt.subplots(1, 1, figsize=(15, 5))
        ax0 = self.__df['RSI'].plot(ax=ax)
        ax0.axhline(30, color='green', ls='--', alpha=0.3)
        ax0.axhline(70, color='green', ls='--', alpha=0.3)
        ax0.axhline(20, color='yellow', ls='--', alpha=0.3)
        ax0.axhline(80, color='yellow', ls='--', alpha=0.3)
        ax0.axhline(10, color='red', ls='--', alpha=0.3)
        ax0.axhline(90, color='red', ls='--', alpha=0.3)

        plt.show()

    def last(self, col='close', i=1):   return self.__df[col].iloc[-i]

    def Buy_Message(self, strategy='Unknow'):
        c = self.last('close')
        atr = self.last('ATR')
        return f"-*-*-* LONG {self.__interval} *-*-*-\nStrategy: {strategy}\nSYMBOL: {self.__symbol}\nENTERY: {c*0.98}\nSTOPLOSS: {c-(atr*1.25)}\nTAKE PROFIT: {c+(atr*1)}"

    def Sell_Message(self, strategy='Unknow'):
        c = self.last('close')
        atr = self.last('ATR')
        return f"-*-*-* SHORT {self.__interval} *-*-*-\nStrategy: {strategy}\nSYMBOL: {self.__symbol}\nENTERY: {c*1.02}\nSTOPLOSS: {c+(atr*1.25)}\nTAKE PROFIT: {c-(atr*1)}"

    def get_df(self): return self.__df

    def get_symbol(self): return self.__symbol

    def get_interval(self): return self.__interval

    def get_last_support(self, i=1): return self.__support[-i][-i]

    def get_last_resistance(self, i=1): return self.__resistance[-i][-i]

    def get_fib(self):  return self.__fib

    def plot(self):
        fig = go.Figure(data=[go.Candlestick(x=self.__df['Date'],
                                             open=self.__df['open'], high=self.__df['high'],
                                             low=self.__df['low'], close=self.__df['close'])
                              ])

        fig.update_layout(xaxis_rangeslider_visible=False)
        fig.show()


def USDT_List():
    """
    read from thr api all the coins and then filter them to be only with usdt exchange
    :return:list, coins/usdt
    """
    usdt_list = []

    tickers = client.futures_ticker()#get_all_tickers()
    for dict in tickers:
        if 'USDT' in dict['symbol'][-4:]:
            usdt_list.append(dict['symbol'])

    return usdt_list

def Cross(coin, fast='EMA_FAST', slow='EMA_SLOW'):
    """
    checking if we have golden cross / death cross
    :param coin: obj
    :return: str, "1" for golden cross, "-1" for death cross, "0" for nothing
    """

    fast_after = coin.last(fast, 2)
    slow_after = coin.last(slow, 2)
    fast_before = coin.last(fast, 3)
    slow_before = coin.last(slow, 3)
    if fast_after > slow_after and fast_before < slow_before:
        return "1"
    if slow_after > fast_after and slow_before < fast_before:
        return "-1"
    return "0"

def Last24hMarket():
    btc = Coin('BTCUSDT')
    eth = Coin('ETHUSDT')
    btc_last24h = ((btc.last('close') - btc.last('close', 2))/btc.last('close', 2)) * 100
    eth_last24h = ((eth.last('close') - eth.last('close', 2))/eth.last('close', 2)) * 100

    return (btc_last24h + eth_last24h) / 2

def Signal(coin):
    result = {'CROSS RSI': '0'}   # will save the return value from the function
    result['CROSS RSI'] = Cross(coin, fast='RSI', slow='RSI_EMA')

    def Long(coin):

        if coin.last() > coin.last('EMA_SLOW'):

            if result['CROSS RSI'] == "1":
                telegram_bot.group_meesage(coin.Buy_Message(strategy='GOLDEN CROSS RSI'))

            if coin.last('MACD', 1) > 0 and coin.last('MACD', 2) < 0:
                telegram_bot.group_meesage(coin.Buy_Message(strategy='MACD'))

            # if coin.last('RSI') < 26:
            #     telegram_bot.group_meesage(coin.Buy_Message(strategy='RSI BELOW 26'))

            if coin.last() / coin.get_last_support() == 0.99 and coin.last('RSI') < 26:
                telegram_bot.group_meesage(coin.Buy_Message(strategy='NEAR SUPPORT LEVEL'))

            if coin.get_fib()[1] * 0.8 > coin.last('close') and coin.get_fib()[2] != 0 and coin.last('RSI') <= 30:
                telegram_bot.group_meesage(coin.Buy_Message(strategy='FIBONACCI LEVEL IS LOW and RSI < 30'))

    def Short(coin):

        if coin.last() < coin.last('EMA_SLOW'):

            if result['CROSS RSI'] == "-1":
                telegram_bot.group_meesage(coin.Sell_Message(strategy='DEATH CROSS RSI'))

            if coin.last('MACD', 1) < 0 and coin.last('MACD', 2) > 0:
                telegram_bot.group_meesage(coin.Sell_Message(strategy='MACD'))
            # if coin.last('RSI') > 74:
            #     telegram_bot.group_meesage(coin.Sell_Message(strategy='RSI ABOVE 80'))

            if coin.get_last_resistance() / coin.last() == 0.99 and coin.last('RSI') > 74:
                telegram_bot.group_meesage(coin.Sell_Message(strategy='NEAR RESISTANCE LEVEL'))

    Long(coin)
    Short(coin)

def Run(coin_list, market, interval="1d"):
    for symbol in coin_list: #splits the the list to few threads so the run on it will be faster (the lower time frame the longer we need to wait)
        try:
            coin = Coin(symbol, interval, True) #working the best on 8h chart
            print('checking ', symbol)

            Signal(coin)

        except:
            print(symbol, "went wrong")
        finally:
            continue

def Split_List(coin_List):
    """
    Here we will split the big list of all the coins we got from the API to mini lists to make after the program
    to run with threads
    :param coin_List: list, all the usdt coins we got from binance API
    :return: List, separate lists of coin_list
    """
    def Split(coin_List):
        approx_sizes = len(coin_List) / n_groups
        groups_cont = [coin_List[int(i * approx_sizes):int((i + 1) * approx_sizes)] for i in range(n_groups)]
        print(groups_cont)
        return groups_cont

    N = len(coin_List)
    if N % 2 == 0:
        n_groups = 4
        return Split(coin_List)
    else:
        n_groups = 3
        return Split(coin_List)

    return coin_List

def Thread_Allocation(Coin_Lists):
    """
    Here I'm using threads to run on the lists, each thread run on a different list
    :param Coin_Lists: List, list of list that have all the coins from the API
    :return:
    """
    threads = []
    # NEED TO CHECK FOR READ WRITE LOCK ON THE TELEGRAM BOT
    market_trend = Last24hMarket()
    print(market_trend)
    for x in range(len(Coin_Lists)):
        t = Thread(target=Run, args=(Coin_Lists[x], market_trend, '1d'))
        threads.append(t)
        t.start()

    # Waiting for all the threads to finish
    for t in threads:
        t.join()

def main():
    #definding the list of coins that are /usdt
    myList = USDT_List()
    #definding the bot to send notification
    print("*-*-* NEW SCAN *-*-*")
    #telegram_bot.group_meesage("New Session")

    # Splitting the list to 2/3/4
    Coin_Lists = Split_List(myList)

    # Allocating threads to the number of lists we splitTH
    Thread_Allocation(Coin_Lists)


def test():
    btc = Coin("UNFIUSDT", '1d', True, HA=True)
    print("MACD 1", btc.last('MACD', 1), "MACD 2", btc.last('MACD', 2))
    print(btc.last('MACD', 1) > 0 and btc.last('MACD', 2) < 0)
    print(btc.get_df())
    Signal(btc)
    btc.plot()
    print(btc.get_last_support())
    print(btc.get_last_resistance())



if __name__ == "__main__":
    main()
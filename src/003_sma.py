# Python实用宝典
# 2020/04/20
# 转载请注明出处
import datetime
import os.path
import sys
import backtrader as bt
from backtrader.indicators import EMA


class TestStrategy(bt.Strategy):
    def __init__(self):
        # 使用移动平均线，使用方法到官方doc查找
        self.bt_sma = bt.indicators.MovingAverageSimple(self.data, period=20)
        self.buy_sell_signal = bt.indicators.CrossOver(self.data.close, self.bt_sma)

    def start(self):
        pass

    def prenext(self):
        pass

    def nextstart(self):
        pass

    def next(self):
        print("a new bar")
        print(self.datas[0].close[0], self.datas[0].datetime.date(0))
        # 访问数据的两种
        #   1.self.data.close[0]
        #   2.self.datas[0].close[0]

        ma_value = self.bt_sma[0]
        pre_ma_value = self.bt_sma[-1]

        if not self.position and self.buy_sell_signal[0] == 1:
            self.order = self.buy()

        if not self.position and self.buy_sell_signal[0] == -1:
            self.order = self.sell()

        if self.position and self.buy_sell_signal[0] == 1:
            self.order = self.close()
            self.order = self.buy()

        if self.position and self.buy_sell_signal[0] == -1:
            self.order = self.close()
            self.order = self.sell()

        # 手动判断上穿下穿
        # if len(self) >= 5:
        #     # sma替换为系统计算的结果:
        #     # ma_value = sum([self.data.close[-cnt] for cnt in range(0, 5)]) / 5
        #     ma_value = self.bt_sma[0]
        #     if self.data.close[0] > ma_value > self.data.close[-1]:
        #         print("上穿", self.data.datetime.date(0))
        #         self.order = self.buy()
        #
        #     if self.data.close[0] < ma_value < self.data.close[-1]:
        #         print("上穿", self.data.datetime.date(0))
        #         self.order = self.sell()


if __name__ == '__main__':
    """
    1.使用系统自带的sma计算方法
    2.使用系统自带的crossover方法
    """
    cerebro = bt.Cerebro()

    cerebro.addstrategy(TestStrategy)

    # 加载数据到模型中
    data = bt.feeds.GenericCSVData(
        dataname="2021_10_12.csv",
        fromdate=datetime.datetime(2021, 5, 1),
        todate=datetime.datetime(2022, 1, 1),
        dtformat='%Y-%m-%d %H:%M:%S',
        datetime=0,
        open=1,
        high=2,
        low=3,
        close=4,
        volume=5,
        openinterest=-1,
        timeframe=bt.TimeFrame.Minutes,
    )

    cerebro.resampledata(data, timeframe=bt.TimeFrame.Days, compression=1, name="BTC")
    cerebro.broker.setcash(10000)
    cerebro.addsizer(bt.sizers.FixedSize, stake=100)
    cerebro.broker.setcommission(commission=0.005)
    cerebro.run()
    cerebro.plot(style='candle')

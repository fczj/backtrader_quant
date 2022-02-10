# Python实用宝典
# 2020/04/20
# 转载请注明出处
import datetime
import os.path
import sys
import backtrader as bt
from backtrader.indicators import EMA


# class MyMovingAverageSimple(bt.indicator):
#     """
#     1.集成indicator
#     2.明确有哪些line
#     3.明确哪些参数
#     4.初始化indicator中的参数
#     5.在next中定义每一个line的值
#     """
#     lines = ("sma",)
#     params = (
#         ("period", 20)
#     )
#
#     def __init__(self):
#         pass


class ThreeBars(bt.Indicator):
    lines = ("up", "down")

    def __init__(self):
        self.addminperiod(5)
        self.plotinfo.plotmaster = self.data

    def next(self):
        self.lines[0][0] = max(
            max(self.data.close.get(ago=-1, size=3)),
            max(self.data.open.get(ago=-1, size=3))
        )
        self.down[0] = min(
            min(self.data.close.get(ago=-1, size=3)),
            min(self.data.open.get(ago=-1, size=3))
        )


class TestStrategy(bt.Strategy):
    def __init__(self):
        self.up_down = ThreeBars(self.data)
        self.buy_signal = bt.indicators.CrossOver(self.data.close, self.up_down)
        self.sell_signal = bt.indicators.CrossOver(self.up_down, self.data.close)

        # 控制是否划线
        self.buy_signal.plotinfo.plot = False
        self.sell_signal.plotinfo.plot = False
        self.up_down.plotinfo.plot = False


    def start(self):
        pass

    def prenext(self):
        pass

    def nextstart(self):
        pass

    def next(self):
        if not self.position and self.buy_signal[0] == 1:
            self.order = self.buy()

        if self.getposition().size < 0 and self.buy_signal[0] == 1:
            self.order = self.close()
            self.order = self.buy()

        if not self.position and self.sell_signal[0] == 1:
            self.order = self.sell()

        if self.getposition().size > 0 and self.sell_signal[0] == 1:
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

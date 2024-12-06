import backtrader as bt
from ffquant.indicators.Trend import Trend
from ffquant.indicators.TrendHold import TrendHold
from ffquant.indicators.TurningPoint import TurningPoint
from ffquant.indicators.ActiveBuySell import ActiveBuySell
from ffquant.utils.Logger import stdout_log

__ALL__ = ['TrendHoldAdjust']

class TrendHoldAdjust(bt.Indicator):
    (BEARISH, NA, BULLISH) = (-1, 0, 1)

    params = (
        ('symbol', 'CAPITALCOM:HK50'),
        ('debug', False),
    )

    lines = ('th_adj',)

    def __init__(self):
        super(TrendHoldAdjust, self).__init__()
        self.addminperiod(1)

        self.trend = Trend(symbol=self.p.symbol, debug=False)
        self.trendhold = TrendHold(symbol=self.p.symbol, debug=False)
        self.tp = TurningPoint(symbol=self.p.symbol, debug=False)
        self.abs = ActiveBuySell(symbol=self.p.symbol, debug=False)
        self.fast_rsi = bt.indicators.RSI(self.data.close, period=3)
        self.slow_rsi = bt.indicators.RSI(self.data.close, period=14)
        self.crossover = bt.indicators.CrossOver(self.fast_rsi, self.slow_rsi)

        # 完成对信号的缓存
        self.trendhold_list = []
        self.tp_list = []
        self.trend_list = []
        self.active_buy_sell_list = []

        # 对上一时刻信号状态的缓存
        self.trendhold_now = TrendHoldAdjust.NA
        self.trendhold_last = TrendHoldAdjust.NA

        self.window_size_short = 5
        self.discount_factor = 0.9

        # whether current value is inherited from previous value
        self.tha_inherited = False

    def next(self):
        self.trendhold_list.append(self.trendhold[0])
        self.tp_list.append(self.tp[0])
        self.trend_list.append(self.trend[0])
        self.active_buy_sell_list.append(self.abs[0])

        if self.trendhold_last is None:
            self.trendhold_last = self.trendhold[0]

        signal_dict = self.signal_calcuate()
        self.trendhold_now = signal_dict['trendhold']

        self.trendhold_last = self.trendhold_now

        self.lines.th_adj[0] = self.trendhold_now


    def signal_calcuate(self):
        # 对信号进行判断和修改
        # 1. 当 trendhold 保持不变的时候，通过 turning point 和 active buy sell 来判断是否需要进行调整。否则以 turning point 和 active buy sell 为主
        # 2. 当 trendhold 变化的时候，如果无明显 turning point 和 active buy sell 的支持，则通过 trend 来判断是否赞成这一次的 trendhold 调整。否则以 turning point 和 active buy sell 为主
        
        signal_dict = {}
        now_trendhold = self.trendhold[0]
        
        # 对 turning point 和 active buy sell 累加，使用 discount factor 进行折现，计算支持度
        tp_list = self.tp_list[-self.window_size_short:] if len(self.tp_list) > self.window_size_short else self.tp_list
        active_buy_sell_list = self.active_buy_sell_list[-self.window_size_short:] if len(self.active_buy_sell_list) > self.window_size_short else self.active_buy_sell_list
        support_tp = 0
        support_active_buy_sell = 0
        for index in range(len(tp_list)):
            support_tp += tp_list[index] * self.discount_factor ** (len(tp_list) - index)
        for index in range(len(active_buy_sell_list)):
            support_active_buy_sell += active_buy_sell_list[index] * self.discount_factor ** (len(active_buy_sell_list) - index)
            
        # 对 trend 累加，计算支持度
        trend_list = self.trend_list[-self.window_size_short:] if len(self.trend_list) > self.window_size_short else self.trend_list
        support_trend = 0
        for index in range(len(trend_list)):
            support_trend += trend_list[index] * self.discount_factor ** (len(trend_list) - index)        
        if self.p.debug:
            stdout_log(f'{self.__class__.__name__}, support_tp: {support_tp}, support_active_buy_sell: {support_active_buy_sell}, support_trend: {support_trend}')

        if now_trendhold == self.trendhold_last:
            if support_tp > 0 and support_active_buy_sell > 0 and now_trendhold == TrendHoldAdjust.BULLISH:
                signal_dict['trendhold'] = TrendHoldAdjust.BULLISH
            elif support_tp < 0 and support_active_buy_sell < 0 and now_trendhold == TrendHoldAdjust.BEARISH:
                signal_dict['trendhold'] = TrendHoldAdjust.BEARISH
            elif support_tp > 0 and support_active_buy_sell > 0 and now_trendhold == TrendHoldAdjust.BEARISH:
                signal_dict['trendhold'] = TrendHoldAdjust.BULLISH
            elif support_tp < 0 and support_active_buy_sell < 0 and now_trendhold == TrendHoldAdjust.BULLISH:
                signal_dict['trendhold'] = TrendHoldAdjust.BEARISH
            else:   
                signal_dict['trendhold'] = self.trendhold_last
        else:
            if support_tp > 0 and support_active_buy_sell > 0 and now_trendhold == TrendHoldAdjust.BEARISH:
                signal_dict['trendhold'] = TrendHoldAdjust.BULLISH
            elif support_tp < 0 and support_active_buy_sell < 0 and now_trendhold == TrendHoldAdjust.BULLISH:
                signal_dict['trendhold'] = TrendHoldAdjust.BEARISH
            elif support_tp > 0 and support_active_buy_sell < 0 and now_trendhold == TrendHoldAdjust.BULLISH:
                if support_trend > 0:
                    signal_dict['trendhold'] = TrendHoldAdjust.BULLISH
                else:
                    signal_dict['trendhold'] = TrendHoldAdjust.BEARISH
            elif support_tp > 0 and support_active_buy_sell < 0 and now_trendhold == TrendHoldAdjust.BEARISH:
                if support_trend > 0:
                    signal_dict['trendhold'] = TrendHoldAdjust.BULLISH
                else:
                    signal_dict['trendhold'] = TrendHoldAdjust.BEARISH
            elif support_tp < 0 and support_active_buy_sell > 0 and now_trendhold == TrendHoldAdjust.BULLISH:
                if support_trend > 0:
                    signal_dict['trendhold'] = TrendHoldAdjust.BULLISH
                else:
                    signal_dict['trendhold'] = TrendHoldAdjust.BEARISH
            elif support_tp < 0 and support_active_buy_sell > 0 and now_trendhold == TrendHoldAdjust.BEARISH:
                if support_trend > 0:
                    signal_dict['trendhold'] = TrendHoldAdjust.BULLISH
                else:
                    signal_dict['trendhold'] = TrendHoldAdjust.BEARISH
            else:
                signal_dict['trendhold'] = self.trendhold_last

        if self.trendhold_last == TrendHoldAdjust.BEARISH and signal_dict['trendhold'] == TrendHoldAdjust.BULLISH:
            if self.crossover != 1:
                if self.p.debug:
                    stdout_log(f"{self.__class__.__name__}, not golden RSI crossover({self.crossover}), keep BEARISH")
                signal_dict['trendhold'] = self.trendhold_last
                self.tha_inherited = True
        elif self.trendhold_last == TrendHoldAdjust.BULLISH and signal_dict['trendhold'] == TrendHoldAdjust.BEARISH:
            if self.crossover != -1:
                if self.p.debug:
                    stdout_log(f"{self.__class__.__name__}, not dead RSI crossover({self.crossover}), keep BULLISH")
                signal_dict['trendhold'] = self.trendhold_last
                self.tha_inherited = True
        else:
            if self.tha_inherited and signal_dict['trendhold'] == TrendHoldAdjust.BULLISH and self.crossover == -1:
                if self.p.debug:
                    stdout_log(f"{self.__class__.__name__}, BULLISH until dead RSI crossover({self.crossover}), reset to original TrendHold")
                signal_dict['trendhold'] = self.trendhold[0]
                self.tha_inherited = False
            elif self.tha_inherited and signal_dict['trendhold'] == TrendHoldAdjust.BEARISH and self.crossover == 1:
                if self.p.debug:
                    stdout_log(f"{self.__class__.__name__}, BEARISH until gold RSI crossover({self.crossover}), reset to original TrendHold")
                signal_dict['trendhold'] = self.trendhold[0]
                self.tha_inherited = False

        return signal_dict
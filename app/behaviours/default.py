
import time

import structlog

class DefaultBehaviour():
    def run(self, symbol_pairs, update_interval, exchange_interface, strategy_analyzer, notifier):
        if symbol_pairs:
            market_data = exchange_interface.get_symbol_markets(symbol_pairs)
        else:
            market_data = exchange_interface.get_exchange_markets()
        while True:
            self.test_strategies(
                market_data,
                strategy_analyzer,
                notifier)
            time.sleep(update_interval)

    def test_strategies(self, market_pairs, strategy_analyzer, notifier):
        for exchange in market_pairs:
            notifier.notify_all(message="New cycle started for - {}".format(exchange))
            for market_pair in market_pairs[exchange]:
                if market_pair != '123/456':
                    rsi_value = strategy_analyzer.analyze_rsi(market_pairs[exchange][market_pair]['symbol'])
                    sma_value, ema_value = strategy_analyzer.analyze_moving_averages(market_pairs[exchange][market_pair]['symbol'])
                    breakout_value, is_breaking_out = strategy_analyzer.analyze_breakout(market_pairs[exchange][market_pair]['symbol'])
                    ichimoku_span_a, ichimoku_span_b, tenkan, kijun = strategy_analyzer.analyze_ichimoku_cloud(market_pairs[exchange][market_pair]['symbol'])
                    macd_value = strategy_analyzer.analyze_macd(market_pairs[exchange][market_pair]['symbol'])
                    if is_breaking_out:
                        notifier.notify_all(message="{} is breaking out! Value: {}, RSI: {} ".format(market_pair, breakout_value, rsi_value))
                    
                    if abs(tenkan-kijun) < 0.000000000001 :
                        notifier.notify_all(message="{} is crossing TK! ".format(market_pair))
                        
                    if rsi_value > 75:
                        notifier.notify_all(message="{} is overbought. ".format(market_pair))
                        
                    if rsi_value < 25:
                        notifier.notify_all(message="{} is oversold. ".format(market_pair))
                        
                    print("{}: \tBreakout: {} \tRSI: {} \tSMA: {} \tEMA: {} \tIMA: {} \tIMB: {} \tITK: {} \tIKJ: {} \t ITKC: {} \tMACD: {}".format(
                        market_pair,
                        breakout_value,
                        format(rsi_value, '.2f'),
                        format(sma_value, '.7f'),
                        format(ema_value, '.7f'),
                        format(ichimoku_span_a, '.7f'),
                        format(ichimoku_span_b, '.7f'),
                        format(tenkan, '.7f'),
                        format(kijun, '.7f'),
                        format(tenkan-kijun, '.7f'),
                        format(macd_value, '.7f')))

import yfinance as yf
import numpy as np
import plotly.graph_objs as go


def get_data(ticker, interval, start, end):
    return yf.download(tickers=ticker, start=start, end=end, interval=interval)


def get_and_process_data(ticker, interval, start, end):
    # Read the data from yahoo
    data = yf.download(tickers=ticker, start=start, end=end, interval=interval)

    # calc ma5 and ma20
    data['MA5'] = data['Close'].rolling(5).mean()
    data['MA20'] = data['Close'].rolling(20).mean()

    # define buy sell signal and position
    data['Signal'] = 0.0
    data['Signal'] = np.where(data['MA5'] > data['MA20'], 1.0, 0.0)
    data['Position'] = data['Signal'].diff()

    # define buy and sell marker positions
    data['position_marker_buy'] = np.where(data['Position'] == 1, data['Open'].shift(1), np.nan)
    data['position_marker_sell'] = np.where(data['Position'] == -1, data['Open'].shift(1), np.nan)

    # define buy and sell price as the open price of the next interval
    data['buy_price'] = np.where(data['Position'] == 1, data['Close'], np.nan)
    data['sell_price'] = np.where(data['Position'] == -1, data['Close'], np.nan)
    return data


def create_plot_ti(data):
    # define buy and sell marker positions
    data = data.copy()
    data['position_marker_buy'] = np.where(data['candlestick_pattern'].str.contains('Bull'), data['Open'].shift(-1), np.nan)
    data['position_marker_sell'] = np.where(data['candlestick_pattern'].str.contains('Bear'), data['Open'].shift(-1), np.nan)
    fig = go.Figure()

    # create candles
    fig.add_trace(go.Candlestick(x=data.index,
                                 open=data['Open'],
                                 high=data['High'],
                                 low=data['Low'],
                                 close=data['Close'], name='market data'))

    # add ma lines
    # fig.add_trace(go.Scatter(x=data.index, y=data['MA20'], line=dict(color='red', width=1.5), name='Death Line'))
    # fig.add_trace(go.Scatter(x=data.index, y=data['MA5'], line=dict(color='orange', width=1.5), name='Gold Line'))

    # add buy sell indicators
    fig.add_trace(go.Scatter(x=data.index, mode='markers', y=data['position_marker_buy'],
                             marker=dict(color='green', size=8, symbol='triangle-up'),
                             name='Buy'))

    fig.add_trace(go.Scatter(x=data.index, mode='markers', y=data['position_marker_sell'],
                             marker=dict(color='red', size=8, symbol='triangle-down'),
                             name='Sell'))
    fig.update_yaxes(fixedrange=False)

    return fig


def create_plot(data):
    fig = go.Figure()

    # create candles
    fig.add_trace(go.Candlestick(x=data.index,
                                 open=data['Open'],
                                 high=data['High'],
                                 low=data['Low'],
                                 close=data['Close'], name='market data'))

    # add ma lines
    fig.add_trace(go.Scatter(x=data.index, y=data['MA20'], line=dict(color='red', width=1.5), name='Death Line'))
    fig.add_trace(go.Scatter(x=data.index, y=data['MA5'], line=dict(color='orange', width=1.5), name='Gold Line'))

    # add buy sell indicators
    fig.add_trace(go.Scatter(x=data.index, mode='markers', y=data['position_marker_buy'],
                             marker=dict(color='green', size=12, symbol='triangle-up'),
                             name='Buy'))

    fig.add_trace(go.Scatter(x=data.index, mode='markers', y=data['position_marker_sell'],
                             marker=dict(color='red', size=12, symbol='triangle-down'),
                             name='Sell'))
    fig.update_yaxes(fixedrange=False)

    return fig


def backtest(data, cash_per_tx=10000):
    buy_sell_df = data[['Signal', 'Position', 'Open', 'Close']].copy()
    buy_sell_df['buy'] = buy_sell_df['Open'].shift(-1)
    buy_sell_df = buy_sell_df[buy_sell_df['Position'] != 0].dropna()
    buy_sell_df['sell'] = buy_sell_df['buy'].shift(-1)

    sell_df = buy_sell_df[buy_sell_df['Position'] == 1].copy()
    sell_df['p_return'] = (sell_df['sell'] - sell_df['buy']) / sell_df['sell']

    sell_df['gain'] = sell_df['p_return'] * cash_per_tx

    return sell_df


def backtest_ti(data, cash_per_tx=1000):
    buy_sell_df = data[['candlestick_pattern', 'Open', 'Close']].copy()
    buy_sell_df['buy'] = buy_sell_df['Open'].shift(-1)
    buy_sell_df = buy_sell_df[buy_sell_df['candlestick_pattern'] != 'NO_PATTERN'].dropna()
    buy_sell_df['sell'] = buy_sell_df['buy'].shift(-1)

    return buy_sell_df


if __name__ == '__main__':
    tickeroo = 'BTC-USD'
    data_90m = get_and_process_data(tickeroo, '90m', '2021-11-01', '2021-11-27')
    fig = create_plot(data_90m)
    fig.show()


import streamlit as st
from helpers import get_and_process_data, create_plot, backtest
from datetime import datetime, timedelta


# Define the sidebar ---------------------------------------------------------------------------------------------------
st.sidebar.markdown('# Options')
ticker = st.sidebar.text_input('Enter a ticker:', 'BTC-USD')
st.sidebar.markdown('### Date Range')
data_start = st.sidebar.date_input('Start', datetime.now() - timedelta(days=2))
data_end = datetime.now()
show_backtest = st.sidebar.checkbox("Show back testing data?")
cash_per_tx = st.sidebar.number_input("Cash per backtest transaction:", value=1000.0)


# Main Panel -----------------------------------------------------------------------------------------------------------
st.title(f'🚀 {ticker} - Buy Sell Indicators 🚀')
st.markdown('---------------------------------------------------------')

f'''### Interval: 90m'''
data_90m = get_and_process_data(ticker, '90m', data_start, data_end)
fig = create_plot(data_90m)
st.plotly_chart(fig)

'''#### Back testing'''
backtest_90m = backtest(data_90m, cash_per_tx)
if show_backtest:
    st.table(backtest_90m[['buy', 'sell', 'p_return', 'gain']])

f'''
Invest on each buy: ${cash_per_tx}\n
Total Return: ${(backtest_90m['p_return'] * cash_per_tx).sum():.2f}\n
% Return: {((backtest_90m['p_return'] * cash_per_tx).sum() / cash_per_tx) * 100:.2f}%
'''

st.markdown('---------------------------------------------------------')

f'''### Interval: 1d'''
data_1d = get_and_process_data(ticker, '1d', data_start, data_end)
fig = create_plot(data_1d)
st.plotly_chart(fig)

'''#### Back testing'''
backtest_1d = backtest(data_1d, cash_per_tx)
if show_backtest:
    st.table(backtest_1d[['buy', 'sell', 'p_return', 'gain']])

f'''
Invest on each buy: ${cash_per_tx}\n
Total Return: ${(backtest_1d['p_return'] * cash_per_tx).sum():.2f}\n
% Return: {((backtest_1d['p_return'] * cash_per_tx).sum() / cash_per_tx) * 100:.2f}%
'''

import json
import statistics

import pandas as pd
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
import yfinance as yf

from CurrencyMonitor.forms import SearchForm


def index(request):
    data = yf.download(
        tickers=['EURUSD=X', 'EURCHF=X', 'GBPUSD=X'],
        group_by='ticker',
        threads=True,
        period='1mo',
        interval='1d'
    )

    data.index = data.index.strftime('%d-%m-%Y')

    labels = list(data.index)

    eurusd = list(data['EURUSD=X']['Adj Close'])
    eurchf = list(data['EURCHF=X']['Adj Close'])
    gbpusd = list(data['GBPUSD=X']['Adj Close'])


    return render(request, 'index.html', {
        'labels': labels,
        'eurusd': eurusd,
        'eurchf': eurchf,
        'gbpusd': gbpusd,

    })

def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST).data.dict()

        ticker_symbol = form['ticker_symbol'].upper()
        start_date = form['start_date']
        end_date = form['end_date']

        data = yf.download(
            tickers=ticker_symbol,
            group_by='ticker',
            threads=True,
            period='1mo',
            interval='1d',
            start=start_date,
            end=end_date
        )

        data.index = data.index.strftime('%d-%m-%Y')
        labels = list(data.index)
        ticker_values = list(data['Adj Close'])

        max_value = max(ticker_values)
        min_value = min(ticker_values)
        mean_value = statistics.mean(ticker_values)

        return render(request, 'history_result.html', {
            'labels': labels,
            'ticker_symbol': [ticker_symbol],
            'ticker_values': ticker_values,
            'max_value': max_value,
            'min_value': min_value,
            'mean_value': mean_value
        })

def ticker(request):
    ticker_df = pd.read_csv('converter/MyTickers.csv')
    json_ticker = ticker_df.reset_index().to_json(orient='records')
    ticker_list = []
    ticker_list = json.loads(json_ticker)

    return render(request, '../templates/ticker.html', {
        'ticker_list': ticker_list[0:20]
    })

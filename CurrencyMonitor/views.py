import json
import statistics
import random

from datetime import datetime, timedelta
from keras.models import Sequential
from keras.layers import Dense, LSTM

import yfinance as yf
import pandas as pd
import numpy as np
from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from CurrencyMonitor.forms import SearchForm, RegistrationForm, PredictionForm

model = None
x_train = None

@login_required
def index(request):
    data = yf.download(
        tickers=['EURUSD=X', 'EURCHF=X', 'GBPUSD=X', 'USDPLN=X', 'EURPLN=X', 'CHFPLN=X'],
        group_by='ticker',
        threads=True,
        period='1mo',
        interval='1d'
    )
    if data.empty:
        return render(request, 'yahoo_finance_down.html')
    else:
        data = data.dropna()
        data.index = data.index.strftime('%d-%m-%Y')

        labels = list(data.index)
        eurusd = list(data['EURUSD=X']['Adj Close'])
        eurchf = list(data['EURCHF=X']['Adj Close'])
        gbpusd = list(data['GBPUSD=X']['Adj Close'])
        usdpln = list(data['USDPLN=X']['Adj Close'])
        eurpln = list(data['EURPLN=X']['Adj Close'])
        chfpln = list(data['CHFPLN=X']['Adj Close'])

    return render(request, 'index.html', {
        'labels': labels,
        'eurusd': eurusd,
        'eurchf': eurchf,
        'gbpusd': gbpusd,
        'usdpln': usdpln,
        'eurpln': eurpln,
        'chfpln': chfpln,
    })
def download_file(request):
    file_path = 'converter/MyTickers.csv'
    file_name = 'MyTickers.csv'
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="%s"' % file_name
        return response

@login_required
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
        data = data.dropna()
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
@login_required
def ticker(request):
    ticker_df = pd.read_csv('converter/MyTickers.csv')
    json_ticker = ticker_df.reset_index().to_json(orient='records')
    ticker_list = json.loads(json_ticker)

    return render(request, '../templates/ticker.html', {
        'ticker_list': ticker_list[0:20]
    })
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if form.is_valid():
            form.save()
            return redirect('/')
        elif not username or not password1 or not password2:
            error = 'You need to fill every field in the form !'
            return render(request, 'register.html', {'error': error})
        elif password1 != password2:
            error = 'The passwords do not match !'
            return render(request, 'register.html', {'error': error})
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/dashboard')
        elif not password or not username:
            error = 'You need to fill every field in the form !'
            return render(request, 'login.html', {'error': error})
        else:
            error = 'Incorrect login information. Please try again.'
            return render(request, 'login.html', {'error': error})
    else:
        return redirect('login')

def logout_view(request):
    logout(request)
    return redirect('/')
def create_x_for_future(arr: np.array, num: int, model) -> np.ndarray:

    predicted = model.predict(arr[-1].reshape(1, 15, 1)) + random.uniform(-0.05, 0.06)

    new_element = arr[arr.shape[0]-1][1:]
    new_element = np.append(new_element, predicted).reshape(1, -1, 1)

    arr = np.append(arr, new_element, 0)

    if(num-1>0):
        return create_x_for_future(arr, num-1, model)
    else:
        return arr
@login_required
def prediction(request):
    if request.method == 'POST':
        form = PredictionForm(request.POST).data.dict()
        ticker_symbol = form['ticker_symbol'].upper()
        num_of_days = form['number_of_days']

    num_of_days = int(num_of_days)

    if num_of_days < 0:
        error = 'You have entered a number less than 0 in the field for the number of days.'
        return render(request, 'day_error.html', {'error': error})
    if num_of_days > 365:
        error = 'You have entered more than 365 days.'
        return render(request, 'day_error.html', {'error': error})

    start_date = datetime(2021, 1, 1, 0, 0, 0, 0)
    end_date = datetime.now()
    final_end_date = end_date + timedelta(days=num_of_days)

    data = yf.download(
        tickers=ticker_symbol,
        group_by='ticker',
        threads=True,
        interval='1d',
        start=start_date,
        end=end_date,
    )
    data = data.dropna()

    data['Date'] = data.index
    data.reset_index(drop=True, inplace=True)
    prediction_table = pd.DataFrame(data[['Date', 'Adj Close']], index=None)

    date = prediction_table.drop(columns='Adj Close')
    train = prediction_table.drop(columns='Date')

    date.drop(date.index[:15], axis=0, inplace=True)
    date.reset_index(drop=True, inplace=True)
    date_list = [x.strftime("%Y-%m-%d") for x in date['Date']]
    date_list += [x.strftime("%Y-%m-%d") for x in pd.date_range(end_date, final_end_date, freq='D')]

    train_np = train.values

    x_train = []
    y_train = []

    for i in range(15, train_np.shape[0]):
        x_train.append(train_np[i - 15:i, 0])
        y_train.append(train_np[i, 0])

    x_train = np.array(x_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    y_train = np.array(y_train)

    model = Sequential()
    model.add(LSTM(100, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(LSTM(100, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))

    model.summary()
    model.compile(optimizer='adam', loss='mean_squared_error')

    for i in range(10):
        model.fit(x_train, y_train, epochs=1, batch_size=1)

    generate_values = create_x_for_future(x_train, num_of_days, model)
    y_data = list(model.predict(generate_values).flatten())

    return render(request, 'prediction_result.html', {
        'x_data': date_list,
        'y_data': y_data,
        'ticker_symbol': [ticker_symbol],
    })

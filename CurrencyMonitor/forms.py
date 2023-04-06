from django import forms

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)

class PredictionForm(forms.Form):
    ticker_symbol = forms.CharField(label='Ticker Symbol', max_length=100),
    number_of_days = forms.CharField(label='Number of days', max_length=100)

class SearchForm(forms.Form):
    ticker_symbol = forms.CharField(label='Ticker Symbol', max_length=100),
    start_date = forms.DateField(label='Start Date')
    end_date = forms.DateField(label='End Date')

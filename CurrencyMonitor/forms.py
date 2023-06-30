from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
    def clean_repeat_password(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Hasła nie są identyczne.')
        return password1

class PredictionForm(forms.Form):
    ticker_symbol = forms.CharField(label='Ticker Symbol', max_length=100),
    number_of_days = forms.CharField(label='Number of days', max_length=100)

class SearchForm(forms.Form):
    ticker_symbol = forms.CharField(label='Ticker Symbol', max_length=100),
    start_date = forms.DateField(label='Start Date')
    end_date = forms.DateField(label='End Date')

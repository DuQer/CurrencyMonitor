from django.urls import path
from django.views.generic import TemplateView
from django.contrib import admin
from .views import index, search, ticker, prediction, download_file, register, login_view, logout_view

urlpatterns = [
    path('', TemplateView.as_view(template_name='login.html'), name='login_page'),
    path('admin/', admin.site.urls),
    path('download/', download_file, name='download_file'),
    path('dashboard/', index),
    path('history-search/', TemplateView.as_view(template_name='history_search.html'), name='history_search_page'),
    path('history/', search, name='history_result'),
    path('ticker/', ticker, name='list_of_tickers'),
    path('login/', login_view, name='login_function'),
    path('register-page/', TemplateView.as_view(template_name='register.html'), name='register_page'),
    path('register/', register, name='register-function'),
    path('logout/', logout_view, name='register-function'),
    path('prediction/', TemplateView.as_view(template_name='prediction_search.html'), name='prediction_page'),
    path('predict/', prediction, name='prediction_result'),
    path('404/', TemplateView.as_view(template_name='404.html'), name='404'),
]
LOGIN_URL = '/login-page/'
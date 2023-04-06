from django.urls import path
from django.views.generic import TemplateView

from .views import index, search, ticker

urlpatterns = [
    path('', index),
    path('history-search/', TemplateView.as_view(template_name='history_search.html'), name='history-search'),
    path('history/', search),
    path('ticker/', ticker),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('prediction/', TemplateView.as_view(template_name='prediction_search.html'), name='prediction_page'),

]

from django.urls import path
from .views import time_series_chart, stock_forecast, stocks_page

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('chart/', time_series_chart, name='time_series_chart'),
    path('stock-forecast/', stock_forecast, name='stock_forecast'),
    path('stocks/', stocks_page, name='stocks_page'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
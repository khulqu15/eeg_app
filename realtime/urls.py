from django.urls import path
from . import views

urlpatterns = [
    path('', views.chart_view, name='chart'),
    path('api/data/', views.api_data, name='api_data'),
    path('api/serial/ports', views.serial_ports_api),
    path('api/serial/connect', views.connect_serial),
]

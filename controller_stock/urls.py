from django.urls import path
from .views import DashboardView, ControllerStockView


urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('stock', ControllerStockView.as_view(), name='stock')
]
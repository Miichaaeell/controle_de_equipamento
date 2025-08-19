from django.urls import path
from .views import DashboardView, ControllerStockView, TrackingView, UpdateControllerStockView


urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('stock', ControllerStockView.as_view(), name='stock'),
    path('tracking', TrackingView.as_view(), name='tracking'),
    path('update_controller/<pk>', UpdateControllerStockView.as_view(), name='update_controller')
]

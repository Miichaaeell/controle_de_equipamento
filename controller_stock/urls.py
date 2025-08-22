from django.urls import path
from .views import DashboardView, ControllerStockView, TrackingView, UpdateControllerStockView, CreateReasonView, ListReasonView, UpdateReasonView


urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    # Urls stock
    path('stock', ControllerStockView.as_view(), name='stock'),

    # Urls tracking
    path('tracking', TrackingView.as_view(), name='tracking'),

    # Urls Controller
    path('update_controller/<pk>', UpdateControllerStockView.as_view(),
         name='update_controller'),

    # Urls Reason
    path('create_reason/', CreateReasonView.as_view(), name='create_reason'),
    path('list_reason', ListReasonView.as_view(), name='list_reason'),
    path('update_reason/<pk>', UpdateReasonView.as_view(), name='update_reason'),
]

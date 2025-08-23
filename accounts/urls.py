from django.urls import path
from .views import LoginView, LogoutView, DetailAccountView, PasswordChangeView

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('detail_account/<pk>', DetailAccountView.as_view(), name='detail_account'),
    path('password_change/<pk>', PasswordChangeView.as_view(),
         name='password_change'),

]

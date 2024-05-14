from django.urls import path,include
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetCompleteView
from . import views

app_name = 'trendshop_website'

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/', include('allauth.urls')),
    path('password-reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
from django.urls import path,include
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetCompleteView
from . import views

app_name = 'trendshop_website'

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/', include('allauth.urls')),
    path('password-reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('category_list/', views.category_view, name='category_list'),
    path('category_list/<int:category_id>/subcategories/', views.subcategory_view, name='subcategory_list'),
    path('subcategory/<int:subcategory_id>/products/', views.product_view, name='product_list'),
    path('add/product/', views.add_product, name='add_product'),
    path('add/category/', views.add_category, name='add_category'),
]

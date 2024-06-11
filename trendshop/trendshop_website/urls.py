from django.urls import path,include
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetCompleteView
from trendshop_website.views import home, OrderListView, OrderDetailView, \
    CartView, IncreaseItemQuantityView, DecreaseItemQuantityView, \
    RemoveItemFromCartView, OrderDeliveredStatusView, \
    OrderRefundedStatusView,add_to_cart,CheckoutView
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
    path('products/update/<int:product_id>/', views.product_update, name='product_update'),
    path('products/delete/<int:product_id>/', views.product_delete, name='product_delete'),
    path('product/<int:product_id>/', views.product_details, name='product_details'),

    path('add-to-cart/<int:product_id>/',views.add_to_cart, name='add_to_cart'),
    path('cart/', CartView.as_view(), name='cart'),
    path('increase-quantity/<int:pk>/', IncreaseItemQuantityView.as_view(), name='increase_quantity'),
    path('decrease-quantity/<int:pk>/', DecreaseItemQuantityView.as_view(), name='decrease_quantity'),
    path('remove-from-cart/<int:pk>/', RemoveItemFromCartView.as_view(), name='remove_from_cart'),

    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order/list/', OrderListView.as_view(), name='order_list'),
    path('order/status/delivered/<int:pk>/', OrderDeliveredStatusView.as_view(), name='delivered_status'),
    path('order/status/refunded/<int:pk>/', OrderRefundedStatusView.as_view(), name='refunded_status'),
    path('order/detail/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
]
3
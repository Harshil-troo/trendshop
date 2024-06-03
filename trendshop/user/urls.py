from django.urls import path,include

from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, PasswordResetView, \
    PasswordResetConfirmView, PasswordChangeView, PasswordChangeDoneView, PasswordResetCompleteView


from user.views import SignupView, ProfileView, UserDeleteView, UserListView, \
    UserAddressCreateView, UserAddressListView, UserAddressUpdateView, UserAddressDeleteView, logout_view
from user.forms import LoginForm
from trendshop import settings




app_name = 'user'

urlpatterns = [

    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name="registration/login.html",
                                     form_class=LoginForm), name='login'),
    path('logout/', logout_view, name='logout'),
    path('user/profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('password/reset/', PasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/set-password,', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password/change/', PasswordChangeView.as_view(), name='password_change'),
    path('password/change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('user/delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    path('user/list/', UserListView.as_view(), name='user_list'),
    path('user-address/create/', UserAddressCreateView.as_view(), name='address_create'),
    path('user-address/list/', UserAddressListView.as_view(), name='address_list'),
    path('user-address/update/<int:pk>/', UserAddressUpdateView.as_view(), name='address_update'),
    path('user-address/delete/<int:pk>/', UserAddressDeleteView.as_view(), name='address_delete'),

]
from django.shortcuts import render,get_object_or_404
"""This file contains class based views for user and user address model."""

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DeleteView, UpdateView, ListView
from django_filters.views import FilterView
from trendshop.views import CustomPermissionRequired
from user.tasks import send_welcome_email
from user.filters import UserFilter
from user.forms import SignupForm, ProfileForm, UserAddressForm,UserForm
from user.models import User, UserAddress
from django.contrib.auth import logout


from django.utils.translation import gettext_lazy as _



class PasswordContextMixin:
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {"title": self.title, "subtitle": None, **(self.extra_context or {})}
        )
        return context

class SignupView(CreateView):
    """
    This class will create new user instance.
    """
    form_class = SignupForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('user:login')

    def post(self, request, *args, **kwargs):
        super(SignupView, self).post(request, *args, **kwargs)
        form = self.get_form()
        if form.is_valid():
            form.save()
            user_email = form.data['email']
            username = form.data['username']
            send_welcome_email.delay(user_email, username)
        else:
            return self.form_invalid(form)
        return redirect(self.success_url)


class ProfileView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    """
    This class will update user if user is authenticated.
    """
    model = User
    form_class = ProfileForm
    template_name = 'admin/user/profile.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('user:profile', kwargs={'pk': pk})

    def test_func(self):
        """
        This method will check whether user has permission or not.
        """
        instance = self.get_object()
        if instance.id == self.request.user.id or self.request.user.is_superuser \
                or self.request.user.is_staff:
            return True


class UserDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    """
    This class will delete user if user is authenticated.
    """
    model = User
    success_url = reverse_lazy('user:login')

    def test_func(self):
        """
        This method will check whether user has permission or not.
        """
        instance = self.get_object()
        if instance.id == self.request.user.id:
            return True


class UserListView(LoginRequiredMixin, CustomPermissionRequired, FilterView):
    """
    This class will return a list of all users only if user is superuser.
    """
    model = User
    template_name = 'admin/user/user_list.html'
    context_object_name = 'users'
    filterset_class = UserFilter

    def get_queryset(self):
        """
        Returns a queryset of user.
        """
        query = self.request.GET.get('search')
        if query:
            return User.objects.filter(
                Q(first_name__icontains=query) | Q(last_name__icontains=query) |
                Q(username__icontains=query) | Q(email__iexact=query) |
                Q(phone_number__exact=query))
        return User.objects.all()


class UserAddressCreateView(CreateView):
    """
    This class will create user address.
    """
    form_class = UserAddressForm
    template_name = 'admin/user_address/user_address_create.html'
    success_url = reverse_lazy('user:address_list')

    def post(self, request, *args, **kwargs):
        """
        This method will assign user to user address.
        """
        form = self.get_form(form_class=self.get_form_class())
        instance = form.save(commit=False)

        if form.is_valid():
            instance.user = request.user
        instance.save()
        return redirect(self.success_url)


class UserAddressListView(LoginRequiredMixin, ListView):
    """
    This class will return a list of addresses of specific user if user is authenticated.
    """
    model = UserAddress
    template_name = 'admin/user_address/user_address_list.html'
    context_object_name = 'addresses'

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        This method will pass extra context to template.
        """
        context = super(UserAddressListView, self).get_context_data(**kwargs)
        context['form'] = UserAddressForm
        return context

    def get_queryset(self):
        """
        Returns a queryset of user address of specific user.
        """
        return UserAddress.objects.filter(user=self.request.user)


class UserAddressUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    """
    This class will update user address if user is authenticated.
    """
    model = UserAddress
    form_class = UserAddressForm
    template_name = 'admin/user_address/user_address_create.html'
    success_url = reverse_lazy('user:address_list')

    def test_func(self):
        """
        This method will check whether user has permission or not.
        """
        instance = self.get_object()
        if instance.user.id == self.request.user.id:
            return True


class UserAddressDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    """
    This class will delete user address if user is authenticated.
    """
    model = UserAddress
    success_url = reverse_lazy('user:address_list')

    def test_func(self):
        """
        This method will check whether user has permission or not.
        """
        instance = self.get_object()
        if instance.user.id == self.request.user.id:
            return True



def logout_view(request):
    logout(request)
    return redirect("trendshop_website:home")


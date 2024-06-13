from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test

from trendshop.views import CustomPermissionRequired
from .forms import ProductsForm,CategoryForm
from .utils import is_seller
from .models import Category,Product

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q, Count, Sum
from django.http import JsonResponse
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, TemplateView, ListView
from django_filters.views import FilterView
from trendshop.views import CustomPermissionRequired
from trendshop_website.filters import OrderFilter
from trendshop_website.forms import OrderAddressForm, AddToCartForm
from trendshop_website.models import Order, Cart, CartItem
from user.models import User

def home(request):
    subcategory = Category.objects.filter(parent__isnull=True)
    return render(request, 'website.html',{'subcategories': subcategory})

def category_view(request):
    parent_category = Category.objects.filter(parent__isnull=True)
    return render(request, 'trendshop_website/category_list.html', {'categories': parent_category})

def subcategory_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    subcategory = Category.objects.filter(parent=category)
    return render(request, 'trendshop_website/subcategory_list.html', {'categories': category,'subcategories': subcategory})

def product_view(request, subcategory_id):
    subcategory = get_object_or_404(Category, id=subcategory_id)
    products = Product.objects.filter(categories=subcategory)
    return render(request, 'trendshop_website/product_list.html', {'subcategory': subcategory, 'products': products})

@login_required
@user_passes_test(is_seller)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('trendshop_website:category_list')
    else:
        form = CategoryForm()
    return render(request, 'trendshop_website/category_add.html', {'form' : form})

@login_required
@user_passes_test(is_seller)
def add_product(request):
    if request.method == 'POST':
        form = ProductsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('trendshop_website:category_list')  # Redirect to a list of products or another relevant page
    else:
        form = ProductsForm()
    return render(request, 'trendshop_website/product_add.html', {'form': form})


def product_update(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = ProductsForm(instance=product)
    subcategory = product.categories.first()
    if subcategory:
        subcategory_id = subcategory.id
    else:
        subcategory_id = None
    if request.method == 'POST':
        form = ProductsForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('trendshop_website:product_list', subcategory_id=subcategory_id)
    return render(request, 'trendshop_website/product_update.html', {'form': form, 'product': product})


def product_delete(request,product_id):
    product = get_object_or_404(Product, id=product_id)
    subcategory = product.categories.first()
    if subcategory:
        subcategory_id = subcategory.id
    else:
        subcategory_id = None
    product.delete()
    if subcategory_id:
        return redirect('trendshop_website:product_list', subcategory_id=subcategory_id)
    else:
        return redirect('trendshop_website:category_list')

def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'trendshop_website/product_detail.html', {"product":product})





def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart,_ = Cart.objects.get_or_create(user=request.user)
    cart, created = CartItem.objects.get_or_create(item=product,user=request.user,cart=cart)
    cart.quantity += 1
    cart.save()
    success_url = reverse("trendshop_website:cart")
    return JsonResponse({"status": "success", "message": "Added To Cart","success_url":success_url})


class CartView(LoginRequiredMixin, ListView):
    model = Cart
    template_name = 'trendshop_website/cart.html'
    context_object_name = 'carts'

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user, status=True)



class IncreaseItemQuantityView(LoginRequiredMixin, UpdateView):
    model = CartItem

    def get(self, request, *args, **kwargs):
        cart_item = get_object_or_404(CartItem, id=kwargs['pk'])
        cart_item.quantity += 1
        cart_item.save()
        return redirect('trendshop_website:cart')

    def post(self, request, *args, **kwargs):
        super(IncreaseItemQuantityView, self).post(request, *args, **kwargs)
        return JsonResponse({'data': 'data'})


class DecreaseItemQuantityView(LoginRequiredMixin, UpdateView):
    model = CartItem

    def get(self, request, *args, **kwargs):
        cart_item = get_object_or_404(CartItem, id=kwargs['pk'])
        if cart_item.quantity < 2:
            cart_item.delete()
        else:
            cart_item.quantity -= 1
            cart_item.save()
        return redirect('trendshop_website:cart')


class RemoveItemFromCartView(LoginRequiredMixin, DeleteView):
    model = CartItem

    def get(self, request, *args, **kwargs):
        cart_item = get_object_or_404(CartItem, id=kwargs['pk'])
        cart_item.delete()
        return redirect('trendshop_website:cart')


class CheckoutView(LoginRequiredMixin, CreateView):
    form_class = OrderAddressForm
    template_name = 'trendshop_website/checkout.html'
    success_url = reverse_lazy('trendshop_website:payment')

    def get_context_data(self, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)
        form = self.get_form()
        form.fields['delivery_address'].queryset = self.request.user.addresses.all()
        context.update({
            'form': form,
            'carts': Cart.objects.filter(user=self.request.user, status=True)
        })
        return context



















class OrderListView(LoginRequiredMixin, FilterView):
    model = Order
    template_name = 'trendshop_website/order_list.html'
    context_object_name = 'orders'
    filterset_class = OrderFilter
    paginate_by = 9

    def get_queryset(self):
        query = self.request.GET.get('search')
        if self.request.user.is_superuser or self.request.user.is_staff:
            if query:
                return Order.objects.filter(
                    Q(order__icontains=query) |
                    Q(status__icontains=query) |
                    Q(user__username__icontains=query) | Q(user__email__icontains=query))
            else:
                return Order.objects.all().order_by('-created')
        else:
            if query:
                return Order.objects.filter(Q(order__icontains=query))
            else:
                return Order.objects.filter(user=self.request.user).order_by('-created')


class OrderDeliveredStatusView(LoginRequiredMixin, CustomPermissionRequired, UpdateView):
    model = Order

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('trendshop_website:order_detail', kwargs={'pk': pk})

    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=kwargs['pk'])
        order.status = 'Delivered'
        order.save()
        return redirect(self.get_success_url())


class OrderRefundedStatusView(LoginRequiredMixin, CustomPermissionRequired, UpdateView):
    model = Order

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('trendshop_website:order_detail', kwargs={'pk': pk})

    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=kwargs['pk'])
        order.status = 'Deleted'
        order.save()
        return redirect(self.get_success_url())


class OrderDetailView(UserPassesTestMixin, LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'trendshop_website/order_detail.html'
    context_object_name = 'order'

    def get(self, request, *args, **kwargs):
        cart, _ = Cart.objects.get_or_create(user=self.request.user, status=True)
        return super().get(request)

    def test_func(self):
        instance = self.get_object()
        if instance.user.id == self.request.user.id or self.request.user.is_superuser \
                or self.request.user.is_staff:
            return True



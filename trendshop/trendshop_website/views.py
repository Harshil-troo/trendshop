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
from trendshop_website.forms import OrderAddressForm, AddToCartForm, NewsLetterSubscriptionForm, ContactUsForm, \
    ReservationForm
from trendshop_website.models import Order, Cart, CartItem, OrderPayment
from user.models import User

def home(request):
    subcategory = Category.objects.filter(parent__isnull=True)
    return render(request, 'website.html',{'subcategories': subcategory})

def category_view(request):
    parent_category = Category.objects.filter(parent__isnull=True)
    return render(request, 'home/category_list.html', {'categories': parent_category})

def subcategory_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    subcategory = Category.objects.filter(parent=category)
    return render(request, 'home/subcategory_list.html', {'categories': category,'subcategories': subcategory})

def product_view(request, subcategory_id):
    subcategory = get_object_or_404(Category, id=subcategory_id)
    products = Product.objects.filter(categories=subcategory)
    return render(request, 'home/product_list.html', {'subcategory': subcategory, 'products': products})

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
    return render(request, 'home/category_add.html', {'form' : form})

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
    return render(request, 'home/product_add.html', {'form': form})


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
    return render(request, 'home/product_update.html', {'form': form, 'product': product})


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
    return render(request, 'home/product_detail.html', {"product":product})



class AdminDashboardView(LoginRequiredMixin, CustomPermissionRequired, TemplateView):
    template_name = 'admin_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(AdminDashboardView, self).get_context_data(**kwargs)
        total_users = User.objects.count()
        total_active_users = User.objects.filter(is_active=True).count()
        total_orders = Order.objects.count()
        total_sales = Order.objects.filter(status='Delivered').aggregate(
            Sum('total_amount'))['total_amount__sum']
        user_data = User.objects.values('date_joined__month').annotate(
            Count('date_joined__month'))
        active_user_data = User.objects.filter(is_active=True).values('date_joined__month') \
            .annotate(Count('date_joined__month'))
        order_data = Order.objects.values('created__month').annotate(Count('created__month'))
        delivered_order_data = Order.objects.filter(status='Delivered').values('created__month') \
            .annotate(Count('created__month'))
        sales_data = Order.objects.filter(status='Delivered').values('created__month').annotate(
            Sum('total_amount'))
        total_sales_data = sales_data.values_list('total_amount__sum', flat=True)
        context.update({
            'total_users': total_users,
            'total_active_users': total_active_users,
            'total_orders': total_orders,
            'total_sales': round(total_sales, 2),
            'user_data': user_data,
            'active_user_data': active_user_data,
            'order_data': order_data,
            'delivered_order_data': delivered_order_data,
            'sales_data': sales_data,
            'total_sales_data': total_sales_data
        })
        return context


class AddToCartView(LoginRequiredMixin, CreateView):
    form_class = AddToCartForm
    success_url = reverse_lazy('trendshop_website:product_list')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.item_id = self.kwargs.get('pk')
        cart = Cart.objects.get(user__id=self.request.user.id, status=True)
        if not Cart.objects.filter(id=cart.id, carts__item=instance.item_id).exists():
            instance.cart = cart
            instance.save()
        else:
            cart_item_quantity = cart.carts.all().get(item__id=instance.item_id)
            total = instance.quantity + cart_item_quantity.quantity
            cart_item_quantity.quantity = total
            cart_item_quantity.save()
        return JsonResponse({"status": "success", "message": "Added To Cart"})


class CartView(LoginRequiredMixin, ListView):
    model = Cart
    template_name = 'cart/cart.html'
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


# class CheckoutView(LoginRequiredMixin, CreateView):
#     form_class = OrderAddressForm
#     template_name = 'cart/checkout.html'
#     success_url = reverse_lazy('trendshop_website:payment')
#
#     def get_context_data(self, **kwargs):
#         context = super(CheckoutView, self).get_context_data(**kwargs)
#         form = self.get_form()
#         form.fields['delivery_address'].queryset = self.request.user.addresses.all()
#         context.update({
#             'form': form,
#             'carts': Cart.objects.filter(user=self.request.user, status=True)
#         })
#         return context


# @login_required
# def order_payment(request):
#     if request.method == 'POST':
#         form = OrderAddressForm(request.POST)
#         order = form.save(commit=False)
#         order.cart = Cart.objects.get(user__id=request.user.id, status=True)
#         order.user = request.user
#         order.save()
#         client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
#         razorpay_order = client.order.create({
#             "amount": int(order.total_amount) * 100, "currency": "INR", "payment_capture": "1"
#         })
#         payment = OrderPayment.objects.create(user=request.user, order=order,
#                                               provider_order_id=razorpay_order["id"])
#         payment.save()
#         return render(request, "frontend/payment/payment.html", {
#             "callback_url": "https://" + "0ce4-2405-204-8386-9f68-596d-4395-a910-7cae.ngrok-free.app" + "/callback/",
#             "razorpay_key": RAZORPAY_KEY_ID,
#             "order": payment,
#         })
#     return render(request, "frontend/payment/payment.html")


# @csrf_exempt
# def callback(request):
#     if "razorpay_signature" in request.POST:
#         payment_id = request.POST.get("razorpay_payment_id", "")
#         provider_order_id = request.POST.get("razorpay_order_id", "")
#         signature_id = request.POST.get("razorpay_signature", "")
#         payment = OrderPayment.objects.get(provider_order_id=provider_order_id)
#         payment.payment_id = payment_id
#         payment.signature_id = signature_id
#         payment.save()
#
#         params_dict = {
#             "razorpay_payment_id": payment_id,
#             "razorpay_order_id": provider_order_id,
#             "razorpay_signature": signature_id
#         }
#
#         client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
#         result = client.utility.verify_payment_signature(params_dict)
#         if result is True:
#             try:
#                 payment.status = 'Success'
#                 payment.order.status = 'Confirmed'
#                 payment.order.save()
#                 payment.save()
#                 return render(request, "frontend/payment/callback.html",
#                               context={"status": payment.status, "order_id": payment.order.pk})
#             except:
#                 payment.status = 'Failure'
#                 payment.order.status = 'Cancelled'
#                 payment.order.save()
#                 payment.save()
#                 return render(request, "frontend/payment/callback.html",
#                               context={"status": payment.status, "order_id": payment.order.pk})
#     else:
#         if request.POST.get("error[metadata]") is None:
#             return render(request, "frontend/payment/callback.html")
#         else:
#             payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
#             provider_order_id = json.loads(request.POST.get("error[metadata]")).get("order_id")
#             payment = OrderPayment.objects.get(provider_order_id=provider_order_id)
#             payment.payment_id = payment_id
#             payment.status = 'Failure'
#             payment.order.status = 'Cancelled'
#             payment.order.save()
#             payment.save()
#             return render(request, "frontend/payment/callback.html",
#                           context={"status": payment.status})


class OrderListView(LoginRequiredMixin, FilterView):
    model = Order
    template_name = 'admin/order/order_list.html'
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
        return reverse('foodmania_website:order_detail', kwargs={'pk': pk})

    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=kwargs['pk'])
        order.status = 'Delivered'
        order.save()
        return redirect(self.get_success_url())


class OrderRefundedStatusView(LoginRequiredMixin, CustomPermissionRequired, UpdateView):
    model = Order

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('foodmania_website:order_detail', kwargs={'pk': pk})

    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=kwargs['pk'])
        order.status = 'Deleted'
        order.save()
        return redirect(self.get_success_url())


class OrderDetailView(UserPassesTestMixin, LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'admin/order/order_detail.html'
    context_object_name = 'order'

    def get(self, request, *args, **kwargs):
        cart, _ = Cart.objects.get_or_create(user=self.request.user, status=True)
        return super().get(request)

    def test_func(self):
        instance = self.get_object()
        if instance.user.id == self.request.user.id or self.request.user.is_superuser \
                or self.request.user.is_staff:
            return True


class ContactUsView(CreateView):
    form_class = ContactUsForm
    success_url = reverse_lazy('foodmania_website:website')


class NewsLetterView(CreateView):
    form_class = NewsLetterSubscriptionForm
    success_url = reverse_lazy('foodmania_website:website')

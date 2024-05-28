from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView

from trendshop.views import CustomPermissionRequired
from .forms import ProductsForm,CategoryForm
from .utils import is_seller
from .models import Category,Product

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


class ProductUpdateView(LoginRequiredMixin, CustomPermissionRequired, UpdateView):
    """
    This class will update food.
    """
    model = Product
    form_class = ProductsForm
    template_name = 'home/product_add.html'
    success_url = reverse_lazy('trendshop_website:product_update')


class ProductDeleteView(LoginRequiredMixin, CustomPermissionRequired, DeleteView):
    """
    This class will delete food.
    """
    model = Product
    success_url = reverse_lazy('trendshop_website:product_delete')
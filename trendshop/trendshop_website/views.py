from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ProductsForm


def home(request):
    return render(request, 'website.html',)

def is_seller(user):
    return user.is_authenticated and user.userprofile.role == 'seller'

@login_required
@user_passes_test(is_seller)
def add_product(request):
    if request.method == 'POST':
        form = ProductsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Redirect to a list of products or another relevant page
    else:
        form = ProductsForm()
    return render(request, 'products/add_product.html', {'form': form})
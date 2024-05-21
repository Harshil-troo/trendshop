from django import forms

from trendshop_website.models import Category,SubCategory,Products

from django import forms
from .models import Category, SubCategory, Products

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title', 'description']

class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['name', 'sub_category']

class ProductsForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['title', 'description', 'categories', 'price', 'stock', 'image']
        widgets = {
            'categories': forms.CheckboxSelectMultiple(),  # To allow multiple category selection with checkboxes
        }


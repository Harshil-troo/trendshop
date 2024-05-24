from django import forms

from trendshop_website.models import Category,Product


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['image','title', 'description','parent']



class ProductsForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'categories', 'price', 'image','stock']



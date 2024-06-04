from django import forms
from trendshop_website.models import CartItem, Order, NewsLetter, ContactUs, Reservation
from user.models import UserAddress

from trendshop_website.models import Category,Product


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['image','title', 'description','parent']



class ProductsForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'categories', 'price', 'image','stock']



class AddToCartForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1, max_value=20,
                                  widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CartItem
        fields = ['quantity']


class OrderAddressForm(forms.ModelForm):
    delivery_address = forms.ModelChoiceField(queryset=UserAddress.objects.all(),
                                              widget=forms.Select(attrs={'class': 'select2 form-control'}))

    class Meta:
        model = Order
        fields = ['delivery_address']


class ReservationForm(forms.ModelForm):
    message = forms.CharField(max_length=200, widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Reservation
        fields = ['name', 'email', 'date', 'time', 'people', 'message']


class ContactUsForm(forms.ModelForm):
    message = forms.CharField(max_length=200, widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = ContactUs
        fields = ['name', 'email', 'subject', 'message']


class NewsLetterSubscriptionForm(forms.ModelForm):
    email = forms.EmailField(max_length=50, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = NewsLetter
        fields = ['email']

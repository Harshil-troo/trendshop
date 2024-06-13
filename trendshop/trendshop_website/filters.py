import django_filters
from django import forms
from trendshop_website.models import Order


class OrderFilter(django_filters.FilterSet):
    status = django_filters.MultipleChoiceFilter(
        choices=Order.STATUS,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox'}))
    created = django_filters.DateRangeFilter(widget=forms.RadioSelect(attrs={'class': 'radio'}))

    class Meta:
        model = Order
        fields = ['status']

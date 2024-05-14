"""This file contains filterset for user model."""

import django_filters
from .models import User


class UserFilter(django_filters.FilterSet):
    """
    This is filter class for user model.
    """

    def __init__(self, *args, **kwargs):
        """
        This method will initialise custom class.
        """
        super(UserFilter, self).__init__(*args, **kwargs)
        for field in self.filters:
            self.filters[field].field.widget.attrs['class'] = 'form-control'

    class Meta:
        """
        Model Meta is basically the inner class of your model class.
        Model Meta is basically used to change the behavior of your model fields like changing
        order options,verbose_name, and a lot of other options.
        """
        model = User
        fields = ['is_superuser', 'is_staff', 'is_active']

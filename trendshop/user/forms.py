"""
This file contains signup, login, profile and user address model forms which are used in
project.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from user.models import User, UserAddress


class SignupForm(UserCreationForm):
    """
    This form will create user.
    """

    def __init__(self, *args, **kwargs):
        """
        This method will initialise custom class.
        """
        super(SignupForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['email'].required = True

    class Meta:
        """
        Model Meta is basically the inner class of your model class.
        Model Meta is basically used to change the behavior of your model fields like changing
        order options,verbose_name, and a lot of other options.
        """
        model = User
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']

    def clean(self):
        """
        This method will validate data from form.
        """
        cleaned_data = super(SignupForm, self).clean()
        email = self.cleaned_data.get('email')
        phone_number = self.cleaned_data.get('phone_number')
        validate_email(email)

        if User.objects.filter(email__iexact=email).exclude(id=self.instance.id).exists():
            raise ValidationError("Email already exists", code='invalid')
        if User.objects.filter(phone_number=phone_number).exclude(id=self.instance.id).exists():
            raise ValidationError("Phone number already exists", code='invalid')

        return cleaned_data


class LoginForm(AuthenticationForm):
    """
    This form will authenticate user.
    """

    def __init__(self, *args, **kwargs):
        """
        This method will initialise custom class.
        """
        super(LoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-lg'


class ProfileForm(forms.ModelForm):
    """
    This form will display user details.
    """

    def __init__(self, *args, **kwargs):
        """
        This method will initialise custom class.
        """
        super(ProfileForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['gender'].widget.attrs['class'] = 'select2 form-control'
        self.fields['email'].required = True

    class Meta:
        """
        Model Meta is basically the inner class of your model class.
        Model Meta is basically used to change the behavior of your model fields like changing
        order options,verbose_name, and a lot of other options.
        """
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'email', 'gender', 'birth_date', 'image', 'phone_number']
        forms.DateInput.input_type = "date"
        widgets = {'image': forms.FileInput}


class UserAddressForm(forms.ModelForm):
    """
    This is model form of user address model.
    """

    def __init__(self, *args, **kwargs):
        """
        This method will initialise custom class.
        """
        super(UserAddressForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['type'].widget.attrs['class'] = 'select2 form-control'

    class Meta:
        """
        Model Meta is basically the inner class of your model class.
        Model Meta is basically used to change the behavior of your model fields like changing
        order options,verbose_name, and a lot of other options.
        """
        model = UserAddress
        fields = ['address', 'pincode', 'city', 'state', 'type']


class UserForm(forms.ModelForm):
    repassword = forms.CharField(required=True, label='Re-Enter Password',widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['user_types','first_name','last_name','email','password','gst','username','gender','phone_number']
        labels = {
            'first_name':'First Name',
            'last_name':'Last Name',
            'email':'Email Id',
            'gst':'GST No.',
            'username':'User Name',
            'password':'Password',
            'phone_number':'Phone Number'
        }
        widgets = {
            'password':forms.PasswordInput,
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        repassword = cleaned_data.get("repassword")
        if password != repassword:
            raise forms.ValidationError("Please type the same password.")
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['gst'].required = False

class UserUpdateForm(UserForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != 'gst' and name != 'user_types':
                field.disabled = True







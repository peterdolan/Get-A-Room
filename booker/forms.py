from booker.models import AdminUser
from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class AdminUserForm(forms.ModelForm):
    class Meta:
        model = AdminUser
        fields = ('organization', 'picture')
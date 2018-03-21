from django.forms import ModelForm
from user.models import User


class UserRegisterForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'verify_code', 'nick', 'phone', 'email']


class UserLoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

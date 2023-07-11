from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django import forms

from django.contrib.auth.models import User
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Имя пользователя", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class SignupForm(UserCreationForm): 
    username = forms.CharField(label="Имя пользователя", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=200, help_text='Required',widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta: 
        model = User 
        fields =('username', 'email', 'password1', 'password2') 
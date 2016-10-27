from django import forms
from database.models import User
# from django.forms import *


class RegistrationForm(forms.Form):
    name = forms.CharField(label='Naam',
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Naam'}),
                           max_length=30)

    lastName = forms.CharField(label='Achternaam',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Achternaam'}),
                               max_length=30)

    email = forms.EmailField(label='Email',
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))

    password = forms.CharField(label='Wachtwoord',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email',
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(label='Wachtwoord',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Wachtwoord'}))


class UserForm(forms.ModelForm):
    # password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('name', 'lastName', 'email', 'password')


class UserProfileFrom(forms.Form):
    name = forms.CharField(label='Naam',
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Naam'}),
                           max_length=30)

    lastName = forms.CharField(label='Achternaam',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Achternaam'}),
                               max_length=30)

    email = forms.EmailField(label='Email',
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))

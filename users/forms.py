from django import forms
from django.contrib.auth.models import User


class RegistrationForm(forms.Form):
    name = forms.CharField(label='Naam',
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Naam'}),
                           max_length=30)

    lastName = forms.CharField(label='Achternaam',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Achternaam'}),
                               max_length=30)

    email = forms.EmailField(label='Email',
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))

    password1 = forms.CharField(label='Wachtwoord',
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

    password2 = forms.CharField(label='Wachtwoord (Again)',
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email',
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(label='Wachtwoord',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Wachtwoord'}))


class UserForm(forms.ModelForm):
    email = forms.EmailField(label='Email',
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))

    password = forms.CharField(label='Wachtwoord',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


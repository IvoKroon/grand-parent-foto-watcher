# from django import forms
from django.forms import ModelForm, TextInput, ChoiceField
from django import forms
from database.models import Slides


class SliderForm(ModelForm):
    # password = forms.CharField(widget=forms.PasswordInput())
    speed = ChoiceField(choices=[(x, x) for x in range(1, 6)],
                        widget=forms.Select(
                            attrs={'class': 'form-control'}))

    class Meta:
        model = Slides
        fields = ('title', 'desc', 'speed')
        widgets = {
            'title': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'desc': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Beschrijving'}),
        }


class CodeFrom(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Code'}),
                           max_length=6)

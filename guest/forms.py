from django import forms


class GuestForm(forms.Form):
    # # image = forms.ImageField()
    code = forms.CharField(label='Code',
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Slider code'}),
                            max_length=60)

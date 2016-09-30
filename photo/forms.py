from django import forms


class PhotoForm(forms.Form):
    # image = forms.ImageField()
    image = forms.ImageField(widget=forms.FileInput())
    title = forms.CharField(label='Title',
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
                            max_length=60)

    desc = forms.CharField(label='Beschrijving',
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Beschrijving'}),
                           max_length=200)

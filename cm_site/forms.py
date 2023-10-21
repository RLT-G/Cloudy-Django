from django import forms

class SearchForm(forms.Form):
    text_field = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'search__text', 
            'placeholder': 'What are you looking for?'
            }),
        required=False
    )

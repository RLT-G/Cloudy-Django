from django import forms
from .models import ErrorReport
from django.contrib.auth import get_user_model


class SearchForm(forms.Form):
    text_field = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'search__text', 
            'placeholder': 'What are you looking for?'
            }),
        required=False
    )


class ErrorReportForm(forms.ModelForm):
    class Meta:
        model = ErrorReport
        fields = ['email', 'subject', 'description', 'photo']
        widgets = {
            'photo': forms.FileInput(attrs={'id': 'input__file'})
        }


User = get_user_model()

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'artist_name']
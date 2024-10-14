from .models import *
from django import forms

class FormLogIn(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Usuario'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'})
    )
    next = forms.CharField(widget=forms.HiddenInput, initial="/")

class FormSignUp(forms.ModelForm):
    class Meta:
        model=User
        fields=['username', 'password']
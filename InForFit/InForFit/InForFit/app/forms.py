from .models import *
from django import forms

class FormLogIn(forms.Form):
    dni = forms.CharField(max_length=9)
    password = forms.CharField(widget=forms.PasswordInput)
    next = forms.CharField(widget=forms.HiddenInput, initial="/")

class FormSignUp(forms.ModelForm):
    class Meta:
        model=User
        fields=['username', 'password']
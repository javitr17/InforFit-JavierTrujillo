from .models import *
from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

class FormLogIn(forms.Form):
    dni = forms.CharField(
        max_length=9,
        widget=forms.TextInput(attrs={'placeholder': 'DNI'})  # Placeholder agregado
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})  # Placeholder agregado
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    next = forms.CharField(
        widget=forms.HiddenInput(),
        initial="/"
    )
class FormSignUp(forms.Form):
    dni = forms.CharField(max_length=9)
    password = forms.CharField(widget=forms.PasswordInput)
    next = forms.CharField(widget=forms.HiddenInput, initial="/")
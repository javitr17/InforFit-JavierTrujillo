from .models import *
from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from django.core.validators import MinLengthValidator
from django.contrib.auth.forms import PasswordChangeForm


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

class FormRegistro(forms.ModelForm):
    # Campos de Socio
    GENERO_SOCIO = [
        ('Hombre', 'Hombre'),
        ('Mujer', 'Mujer'),
        ('Otro', 'Otro'),
    ]
    nombre = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Nombre','autocomplete': 'given-name'}))
    apellidos = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Apellidos', 'autocomplete': 'family-name'}))
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Fecha Nacimiento'}))
    telefono = forms.CharField(
        max_length=16,
        validators=[MinLengthValidator(9)],
        widget=forms.TextInput(attrs={'placeholder': 'Teléfono', 'autocomplete': 'tel'})
    )
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email', 'autocomplete': 'email'}))
    genero=forms.ChoiceField(
        choices=GENERO_SOCIO,
        widget=forms.RadioSelect,
        initial='Otro',
    )
    # Campos de Datos Domicilio
    dni = forms.CharField(max_length=9, widget=forms.TextInput(attrs={'placeholder': 'DNI'}))
    calle = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Calle'}))
    ciudad = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Ciudad'}))
    codigo_postal = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'placeholder': 'Código postal'}))
    pais = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'País'}))

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña', 'autocomplete': 'new-password'}),
        min_length=8,
        required=True
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar Contraseña', 'autocomplete': 'new-password'}),
        required=True
    )

    class Meta:
        model = Socio
        fields = ['nombre', 'apellidos', 'fecha_nacimiento', 'telefono', 'email', 'genero']

    # Añadir campos de DatosDomicilio
    def save(self, commit=False):  # Usamos commit=False para evitar guardar en la base de datos
        socio = super().save(commit=False)  # Crea el objeto Socio pero no lo guarda en la base de datos
        socio.user = None  # Asegúrate de que no intente relacionar un usuario aún

        # Crea un objeto DatosDomicilio no guardado
        domicilio = DatosDomicilio(
            dni=self.cleaned_data['dni'],
            calle=self.cleaned_data['calle'],
            ciudad=self.cleaned_data['ciudad'],
            codigo_postal=self.cleaned_data['codigo_postal'],
            pais=self.cleaned_data['pais'],
        )

        # Devuelve los objetos como un diccionario
        return {
            'socio': socio,
            'domicilio': domicilio
        }


class FormDatosDomicilio(forms.ModelForm):
    class Meta:
        model = DatosDomicilio
        fields = ['dni', 'calle', 'ciudad', 'codigo_postal', 'pais']
        widgets = {
            'dni': forms.TextInput(attrs={'placeholder': 'DNI'}),
            'calle': forms.TextInput(attrs={'placeholder': 'Calle'}),
            'ciudad': forms.TextInput(attrs={'placeholder': 'Ciudad'}),
            'codigo_postal': forms.TextInput(attrs={'placeholder': 'Código postal'}),
            'pais': forms.TextInput(attrs={'placeholder': 'País'}),
        }

class FormCambioContraseña(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña actual'}),
        label="Contraseña actual"
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Nueva contraseña'}),
        label="Nueva contraseña"
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar nueva contraseña'}),
        label="Confirmar nueva contraseña"
    )

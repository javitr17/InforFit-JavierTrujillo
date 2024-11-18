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

class FormRegistro(forms.ModelForm):
    # Campos de Socio
    nombre = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Nombre'}))
    apellidos = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Apellidos'}))
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Fecha Nacimiento'}))
    telefono = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'placeholder': 'Teléfono'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    genero=forms.ChoiceField(
        choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')],
        widget=forms.RadioSelect,
        initial='O',
    )
    # Campos de Datos Domicilio
    dni = forms.CharField(max_length=9, widget=forms.TextInput(attrs={'placeholder': 'DNI'}))
    calle = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Calle'}))
    ciudad = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Ciudad'}))
    codigo_postal = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'placeholder': 'Código postal'}))
    pais = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'País'}))

    class Meta:
        model = Socio
        fields = ['nombre', 'apellidos', 'fecha_nacimiento', 'telefono', 'email', 'genero']

    # Añadir campos de DatosDomicilio
    def save(self, commit=True):
        # Guardar el socio
        socio = super().save(commit=False)
        if commit:
            socio.save()

        # Crear y guardar los datos del domicilio
        domicilio_data = self.cleaned_data
        DatosDomicilio.objects.create(
            user=socio,  # Asumiendo que el socio y domicilio están vinculados por el usuario
            dni=domicilio_data['dni'],
            calle=domicilio_data['calle'],
            ciudad=domicilio_data['ciudad'],
            codigo_postal=domicilio_data['codigo_postal'],
            pais=domicilio_data['pais']
        )

        return socio  # Retorna el objeto Socio guardado
from .models import *
from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from django.contrib.auth.forms import PasswordChangeForm
import re
from django.core.validators import RegexValidator, MinLengthValidator, EmailValidator
from django.core.exceptions import ValidationError
from datetime import date, timedelta




class FormLogIn(forms.Form):
    dni = forms.CharField(
        max_length=9,
        widget=forms.TextInput(attrs={'placeholder': 'DNI'})  # Placeholder agregado
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'})  # Placeholder agregado
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    next = forms.CharField(
        widget=forms.HiddenInput(),
        initial="/"
    )

    def clean_dni(self):
        dni = self.cleaned_data.get("dni")
        # Expresión regular para 8 números seguidos de 1 letra
        if not re.fullmatch(r"^\d{8}[a-zA-Z]$", dni):
            raise forms.ValidationError("El formato del DNI introducido no es válido")
        return dni

    def clean_password(self):
        """Validar que la contraseña cumpla con el formato."""
        password = self.cleaned_data.get("password")
        if len(password) < 8:
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError("La contraseña debe contener al menos un número.")
        return password
class FormSignUp(forms.Form):
    dni = forms.CharField(max_length=9)
    password = forms.CharField(widget=forms.PasswordInput)
    next = forms.CharField(widget=forms.HiddenInput, initial="/")


def validar_dni(dni):
    """
    Valida un DNI español.
    - Debe tener 8 números seguidos de una letra mayúscula.
    - Calcula la letra correcta y compara con la introducida.
    """
    letras_dni = "TRWAGMYFPDXBNJZSQVHLCKE"
    # Validar que el formato sea correcto (8 números y 1 letra)
    if not re.match(r'^\d{8}[A-Z]$', dni.upper()):
        raise ValidationError("El DNI debe tener 8 números seguidos de una letra mayúscula (ejemplo: 12345678Z).")

    # Separar la parte numérica y la letra
    numero = int(dni[:-1])  # Los 8 primeros caracteres como número
    letra = dni[-1].upper()  # Último carácter como letra en mayúscula

    # Calcular la letra correcta
    letra_correcta = letras_dni[numero % 23]

    # Comprobar si la letra introducida coincide con la correcta
    if letra != letra_correcta:
        raise ValidationError("El DNI introducido no existe")

class FormRegistro(forms.ModelForm):
    # Opciones de género
    GENERO_SOCIO = [
        ('Hombre', 'Hombre'),
        ('Mujer', 'Mujer'),
        ('Otro', 'Otro'),
    ]

    # Validadores
    telefono_validator = RegexValidator(
        regex=r'^\+?[0-9]{9,16}$',
        message="El teléfono debe contener entre 9 y 16 dígitos, y puede comenzar con +."
    )

    codigo_postal_validator = RegexValidator(
        regex=r'^\d{5}$',
        message="El código postal debe contener exactamente 5 números."
    )

    # Campos del formulario
    nombre = forms.CharField(max_length=100,
                             widget=forms.TextInput(attrs={'placeholder': 'Nombre', 'autocomplete': 'given-name'}))
    apellidos = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'placeholder': 'Apellidos', 'autocomplete': 'family-name'}))
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Fecha Nacimiento'}))
    telefono = forms.CharField(
        max_length=16,
        validators=[telefono_validator],
        widget=forms.TextInput(attrs={'placeholder': 'Teléfono', 'autocomplete': 'tel'}))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'autocomplete': 'email'}))
    genero = forms.ChoiceField(
        choices=GENERO_SOCIO,
        widget=forms.RadioSelect,
        initial='Otro',
    )
    dni = forms.CharField(
        max_length=9,
        validators=[validar_dni],  # Cambiado a validador personalizado
        widget=forms.TextInput(attrs={'placeholder': 'DNI'})
    )
    calle = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Calle'}))
    ciudad = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Ciudad'}))
    codigo_postal = forms.CharField(
        max_length=10,
        validators=[codigo_postal_validator],
        widget=forms.TextInput(attrs={'placeholder': 'Código postal'})
    )
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
        fields = ['nombre', 'apellidos', 'fecha_nacimiento', 'telefono', 'email', 'genero', 'dni', 'calle', 'ciudad', 'codigo_postal', 'pais']

    # Validación personalizada para contraseñas
        # Validación personalizada para contraseñas
    def clean_password_confirm(self):
            password = self.cleaned_data.get('password')
            password_confirm = self.cleaned_data.get('password_confirm')
            if password and password_confirm and password != password_confirm:
                raise ValidationError("Las contraseñas no coinciden.")
            return password_confirm

    def clean_password(self):
            """Validar que la contraseña cumpla con el formato."""
            password = self.cleaned_data.get("password")
            if len(password) < 8:
                raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres.")
            if not any(char.isdigit() for char in password):
                raise forms.ValidationError("La contraseña debe contener al menos un número.")
            return password

    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data.get("fecha_nacimiento")
        today = date.today()

        # Definir los límites de edad
        edad_minima = today.year - 100
        edad_maxima = today.year - 5

        # Comprobar que la fecha de nacimiento esté dentro del rango
        if fecha_nacimiento.year < edad_minima:
            raise ValidationError(f"La fecha de nacimiento no puede ser anterior a al año {edad_minima}")
        if fecha_nacimiento.year > edad_maxima:
            raise ValidationError(f"La fecha de nacimiento no puede ser posterior al año {edad_maxima}")

        return fecha_nacimiento
    # Validación general del formulario
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        telefono = cleaned_data.get('telefono')

        # Validación adicional: por ejemplo, el email o teléfono no pueden ser "prohibidos"
        if email and "prohibido" in email:
            self.add_error("El correo electrónico no es válido.")

        if telefono and not telefono.isdigit():
            self.add_error("El teléfono solo puede contener números.")

        return cleaned_data

    def save(self, commit=False):
        socio = super().save(commit=False)
        domicilio = DatosDomicilio(
            dni=self.cleaned_data['dni'],
            calle=self.cleaned_data['calle'],
            ciudad=self.cleaned_data['ciudad'],
            codigo_postal=self.cleaned_data['codigo_postal'],
            pais=self.cleaned_data['pais'],
        )
        return {'socio': socio, 'domicilio': domicilio}


class FormDatosDomicilio(forms.ModelForm):
    # Validadores
    codigo_postal_validator = RegexValidator(
        regex=r'^\d{5}$',
        message="El código postal debe contener exactamente 5 números."
    )

    # Campos con validadores y widgets
    dni = forms.CharField(
        max_length=9,
        validators=[validar_dni],
        widget=forms.TextInput(attrs={'placeholder': 'DNI'})
    )
    calle = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Calle'})
    )
    ciudad = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Ciudad'})
    )
    codigo_postal = forms.CharField(
        max_length=5,
        validators=[codigo_postal_validator],
        widget=forms.TextInput(attrs={'placeholder': 'Código postal'})
    )
    pais = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'País'})
    )

    class Meta:
        model = DatosDomicilio
        fields = ['dni', 'calle', 'ciudad', 'codigo_postal', 'pais']

    # Validación personalizada para evitar errores generales
    def clean(self):
        cleaned_data = super().clean()
        dni = cleaned_data.get("dni")
        ciudad = cleaned_data.get("ciudad")

        if ciudad and ciudad.lower() == "prohibido":
            raise ValidationError("El nombre de la ciudad no es válido.")

        return cleaned_data

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


class FormEntrenamiento(forms.Form):
    # Opciones para cada campo
    DIAS_OPCIONES = [
        ('1', '1 día'),
        ('2', '2 días'),
        ('3', '3 días'),
        ('4', '4 días'),
        ('5', '5 días'),
        ('6', '6 días'),
        ('7', '7 días'),
    ]

    TIEMPO_OPCIONES = [
        ('45min', '45 minutos'),
        ('1h', '1 hora'),
        ('1:30h', '1 hora 30 minutos'),
        ('2h', '2 horas'),
    ]

    NIVEL_OPCIONES = [
        ('principiante', 'Principiante'),
        ('intermedio', 'Intermedio'),
        ('alto', 'Alto'),
    ]

    OBJETIVO_OPCIONES = [
        ('ganar_musculo', 'Ganar músculo'),
        ('fuerza', 'Fuerza'),
        ('perder_peso', 'Perder peso'),
    ]

    # Campos del formulario
    dias_a_la_semana = forms.ChoiceField(
        choices=DIAS_OPCIONES,
        widget=forms.RadioSelect

    )

    tiempo_del_entreno = forms.ChoiceField(
        choices=TIEMPO_OPCIONES,
        widget=forms.RadioSelect

    )

    nivel_de_la_persona = forms.ChoiceField(
        choices=NIVEL_OPCIONES,
        widget=forms.RadioSelect

    )

    objetivo = forms.ChoiceField(
        choices=OBJETIVO_OPCIONES,
        widget=forms.RadioSelect

    )

class FormPeso(forms.ModelForm):
    class Meta:
        model = DatosFisicos
        fields = ['peso']  # Solo el campo peso

    def clean_peso(self):
        peso = self.cleaned_data.get('peso')
        if not peso or peso <= 0:
            raise forms.ValidationError('El peso debe ser mayor que cero.')
        return peso

class FormAltura(forms.ModelForm):
    class Meta:
        model = DatosFisicos
        fields = ['altura']  # Solo el campo altura


class FormDatosSocio(forms.ModelForm):
    # Opciones de género
    GENERO_SOCIO = [
        ('Hombre', 'Hombre'),
        ('Mujer', 'Mujer'),
        ('Otro', 'Otro'),
    ]

    # Validadores
    telefono_validator = RegexValidator(
        regex=r'^\+?[0-9]{9,16}$',
        message="El teléfono debe contener entre 9 y 16 dígitos, y puede comenzar con +."
    )

    # Campos del formulario
    nombre = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Nombre', 'autocomplete': 'given-name'})
    )
    apellidos = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Apellidos', 'autocomplete': 'family-name'})
    )
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Fecha de nacimiento'})
    )
    telefono = forms.CharField(
        max_length=16,
        validators=[telefono_validator],
        widget=forms.TextInput(attrs={'placeholder': 'Teléfono', 'autocomplete': 'tel'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'autocomplete': 'email'})
    )
    genero = forms.ChoiceField(
        choices=GENERO_SOCIO,
        widget=forms.RadioSelect,
        initial='Otro'
    )


    class Meta:
        model = Socio
        fields = ['nombre', 'apellidos', 'fecha_nacimiento', 'telefono', 'email', 'genero']

    # Validación personalizada de la fecha de nacimiento
    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data.get("fecha_nacimiento")
        today = date.today()
        edad_minima = 5
        edad_maxima = 100

        edad_usuario = today.year - fecha_nacimiento.year - (
                    (today.month, today.day) < (fecha_nacimiento.month, fecha_nacimiento.day))

        if edad_usuario < edad_minima:
            raise ValidationError(f"Debes tener al menos {edad_minima} años.")
        if edad_usuario > edad_maxima:
            raise ValidationError(f"La edad máxima permitida es {edad_maxima} años.")
        return fecha_nacimiento

    # Validación personalizada del teléfono (en caso de ser requerido)
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not telefono.isdigit():
            raise ValidationError("El teléfono debe contener solo números.")
        return telefono


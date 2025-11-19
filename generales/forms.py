from django import forms

from django.forms.models import inlineformset_factory

from generales.models import Suscribir, Comentario, Contacto

from django import forms

from .models import PendingUser

from django.contrib.auth.hashers import make_password

from django.contrib.auth.models import User


class SuscribirseForm(forms.ModelForm):
    
    class Meta:
        model = Suscribir
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not email:
            raise forms.ValidationError("Email Requerido")
        return email



class ComentarioForm(forms.ModelForm):

    class Meta:
        model = Comentario
        fields = ('comentario', 'nombre', 'email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['comentario'].widget.attrs.update({'placeholder':"Comentario *"})
        self.fields['nombre'].widget.attrs.update({'placeholder':"Nombre *"})
        self.fields['email'].widget.attrs.update({'placeholder':"E-Mail *"})

    def clean_comentario(self):
        comentario = self.cleaned_data["comentario"]
        if not comentario:
            raise forms.ValidationError("Comentario Requerido")
        return comentario
    
    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"]
        if not nombre:
            raise forms.ValidationError("Nombre Requerido")
        return nombre

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not email:
            raise forms.ValidationError("Email Requerido")
        return email
    
class ContactoForm(forms.ModelForm):
    nombre = forms.TextInput()

    class Meta:
        model=Contacto
        fields = ['nombre', 'email', 'textoMensage']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['textoMensage'].widget.attrs.update({'placeholder':"Mensage *"})
        self.fields['nombre'].widget.attrs.update({'placeholder':"Nombre *"})
        self.fields['email'].widget.attrs.update({'placeholder':"E-Mail *"})

    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"]
        if not nombre:
            raise forms.ValidationError("Nombre Requerido")
        return nombre

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not email:
            raise forms.ValidationError("Email Requerido")
        return email

    def clean_textoMensage(self):
        textoMensage = self.cleaned_data["textoMensage"]
        if not textoMensage:
            raise forms.ValidationError("Mensage Requerido")
        return textoMensage
    
class RegisterForm(forms.ModelForm):
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repetir contraseña", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado")
        return email

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password")
        p2 = cleaned.get("password2")

        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Las contraseñas no coinciden")

        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()

        return user

class CodeVerificationForm(forms.Form):
    email = forms.EmailField(widget=forms.HiddenInput)
    codigo = forms.CharField(max_length=6)

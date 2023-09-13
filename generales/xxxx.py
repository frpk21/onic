from django import forms

from django.forms.models import inlineformset_factory

from generales.models import Suscribir, Comentario, Contacto


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
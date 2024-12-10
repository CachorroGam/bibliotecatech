from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Libro
from .models import Prestamo, Libro
from users.models import Prestamo



class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, initial=False)




class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['titulo', 'autor', 'genero', 'fecha_publicacion', 'isbn', 'disponible', 'portada', 'descripcion']
        widgets = {
            'fecha_publicacion': forms.DateInput(attrs={'type': 'date'}),
        }





class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']





class ContactForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    email = forms.EmailField()
    asunto = forms.CharField(max_length=100)
    mensaje = forms.CharField(widget=forms.Textarea)





# forms.py

from django import forms
from .models import Prestamo

class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['libro', 'usuario', 'fecha_devolucion', 'estado', 'dias_prestamo', 'fecha_prestamo']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Obtener el usuario desde kwargs si está presente
        super().__init__(*args, **kwargs)

        if user:  # Si el usuario está presente
            self.fields['usuario'].initial = user  # Establece el usuario como valor inicial





class EditarPrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['libro', 'usuario', 'fecha_devolucion', 'estado', 'dias_prestamo', 'fecha_prestamo']  # Campos editables
        widgets = {
            'dias_prestamo': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }

        fecha_prestamo = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
        )

        def clean(self):
            cleaned_data = super().clean()
            fecha_prestamo = cleaned_data.get('fecha_prestamo')
            fecha_devolucion = cleaned_data.get('fecha_devolucion')

            if fecha_prestamo and fecha_devolucion:
                dias_prestamo = (fecha_devolucion - fecha_prestamo).days
                cleaned_data['dias_prestamo'] = dias_prestamo
            
            return cleaned_data
    

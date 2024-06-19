from django import forms
from django.contrib.auth.hashers import make_password
from empleados.models import Sede

class formularioRegistro(forms.Form):
    nombre = forms.CharField(label='nombre', max_length=50, error_messages={
            'required': 'Introduzca el nombre.',
        })
    apellido= forms.CharField(label='apellido', max_length=50, error_messages={
            'required': 'Introduzca el apellido.',
        })
    fecha_nacimiento = forms.DateField(label='fecha de Nacimiento', error_messages={
            'required': 'Introduzca la fecha de nacimiento.',
            'invalid': 'Fecha invalida, debe estar compuesta por dd/mm/aaaa.',
            }, input_formats=['%Y-%m-%d']
            )
    telefono= forms.CharField(label='telefono', max_length=13, min_length=10, error_messages={
            'required': 'Introduzca el telefono.',
            'min_length': 'El telefono debe tener minimo 10 digitos, debe ser compuesto por numero de area y numero de telefono abonado.'
         })
    mail= forms.EmailField(label='mail', max_length=50, error_messages={
            'required': 'Introduzca el Mail.',
            'invalid': 'Mail invalido, el mail debe respetar el formato mail@direccion.'
        })
    contraseña= forms.CharField(label='contraseña',max_length=50, min_length=6, 
            error_messages={
            'required': 'Introduzca una contraseña.',
            'min_length': 'La contraseña debe tener mínimo 6 caracteres.'})

    def clean_contraseña(self):
        password = self.cleaned_data.get('contraseña')
        return make_password(password)
    
class formularioRegistroEmpleado(forms.Form):
    mail= forms.EmailField(label='mail', max_length=50, error_messages={
            'required': 'Introduzca el Mail.',
            'invalid': 'Mail invalido, el mail debe respetar el formato mail@direccion.'
        })
    sede = forms.ModelChoiceField(queryset=Sede.objects.all(), empty_label='Seleccione la sede')
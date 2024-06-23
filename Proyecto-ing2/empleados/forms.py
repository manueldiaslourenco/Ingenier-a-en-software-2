from django import forms

class FormularioEditarEmpleado(forms.Form):
    nombre = forms.CharField(label='Nombre', max_length=50, required=False)
    apellido = forms.CharField(label='Apellido', max_length=50, required=False)
    fecha_nacimiento = forms.DateField(label='Fecha de Nacimiento', required=False)
    telefono = forms.CharField(label='Teléfono', max_length=20, min_length=10, error_messages={
            'min_length': 'El telefono debe tener minimo 10 digitos, debe ser compuesto por numero de area y numero de telefono abonado.'
         })

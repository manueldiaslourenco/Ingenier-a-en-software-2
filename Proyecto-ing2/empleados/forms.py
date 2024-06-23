from django import forms

class FormularioEditarEmpleado(forms.Form):
    nombre = forms.CharField(label='Nombre', max_length=50, required=False)
    apellido = forms.CharField(label='Apellido', max_length=50, required=False)
    fecha_nacimiento = forms.DateField(label='Fecha de Nacimiento', required=False)
    telefono = forms.CharField(label='Teléfono', max_length=20, required=False)

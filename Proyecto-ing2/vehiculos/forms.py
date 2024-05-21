from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .backend import validar_extensiones

class formularioCargarVehiculo(forms.Form):
    patente = forms.CharField(label='patente', max_length=50, error_messages={
            'required': 'Por favor, introduce una patente.',
        })
    
    marca = forms.CharField(label='marca', max_length=50, error_messages={
            'required': 'Por favor, introduce una marca.',
        })
    
    modelo = forms.CharField(label='modelo', max_length=50, error_messages={
            'required': 'Por favor, introduce un modelo.',
        })
    
    tipo = forms.CharField(label='tipo' , max_length=50, error_messages={
            'required': 'Por favor, selecciona un tipo.',
        })

    año_fabricacion = forms.IntegerField(label='Año de fabricación', error_messages={
        'required': 'Por favor, introduce el año de fabricación del vehículo.',
        'min_value': 'El año de fabricación no puede ser menor a 1900.',
        'max_value': 'El año de fabricación no puede ser mayor a 2024.',
    }, validators=[
        MinValueValidator(1900),
        MaxValueValidator(2024)
    ])

    kilometraje = forms.DecimalField(label='kilometraje', max_digits = 10, decimal_places = 0, error_messages={
            'required': 'Por favor, introduce el kilometraje del vehiculo.',
            'max_digits': 'El número ingresado es demasiado grande.',
            'max_decimal_places': 'El número ingresado es demasiado grande.',
            'max_whole_digits': 'El número ingresado es demasiado grande.',
        })

    imagen1 = forms.ImageField(label='imagen1', required=False, validators=[validar_extensiones])

    imagen2= forms.ImageField(label='imagen2', required=False, validators=[validar_extensiones])

    imagen3= forms.ImageField(label='imagen3', required=False, validators=[validar_extensiones])
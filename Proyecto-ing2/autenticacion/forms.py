from django import forms

class cuestionarioRegistro(forms.Form):
    nombre = forms.CharField(label='Nombre', max_length=50, error_messages={
            'required': 'Por favor, introduce tu nombre.',
        })
    apellido= forms.CharField(label='Apellido', max_length=50, error_messages={
            'required': 'Por favor, introduce tu apellido.',
        })
    dni = forms.CharField(label='Dni', max_length=8, error_messages={
            'required': 'Por favor, introduce tu Dni.',
            'max_length': 'El Dni debe tener como maximo 8 caracteres.'
        })
    #fecha_nacimiento = forms.DateField(label='Fecha de Nacimiento')
    mail= forms.CharField(label='Mail', max_length=50, error_messages={
            'required': 'Por favor, introduce tu Mail.',
        })
    #telefono= forms.CharField(label='Telefono', max_length=13, error_messages={
     #       'required': 'Por favor, introduce tu Dni.',
      #      'max_length': 'El Dni debe tener como maximo 8 caracteres.'
       # })
    contraseña= forms.CharField(label='Contraseña',max_length=50, min_length=6, 
            error_messages={
            'required': 'Por favor, introduce una contraseña.',
            'min_length': 'La contraseña debe tener mínimo 6 caracteres.'})
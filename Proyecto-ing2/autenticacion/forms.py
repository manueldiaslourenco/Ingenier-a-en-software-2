from django import forms

class cuestionarioRegistro(forms.Form):
    nombre = forms.CharField(label='Nombre', max_length=50, error_messages={
            'required': 'Por favor, introduce tu nombre.',
        })
    apellido= forms.CharField(label='Apellido', max_length=50, error_messages={
            'required': 'Por favor, introduce tu apellido.',
        })
    dni = forms.CharField(label='Dni', min_length=8, error_messages={
            'required': 'Por favor, introduce tu Dni.',
            'min_length': 'El DNI debe tener 8 digitos.'
        })
    fecha_nacimiento = forms.DateField(label='Fecha de Nacimiento', error_messages={
            'required': 'Por favor, introduce tu fecha de nacimiento.',
            'invalid': 'Fecha invalida, debe estar compuesta por dia/mes/año.',
            }, input_formats=['%d/%m/%Y']
            )
    telefono= forms.CharField(label='Telefono', max_length=13, min_length=10, error_messages={
            'required': 'Por favor, introduce tu telefono.',
            'min_length': 'El telefono debe tener minimo 10 digitos, debe ser compuesto por numero de area y numero de telefono abonado.'
         })
    mail= forms.CharField(label='Mail', max_length=50, error_messages={
            'required': 'Por favor, introduce tu Mail.',
        })
    contraseña= forms.CharField(label='Contraseña',max_length=50, min_length=6, 
            error_messages={
            'required': 'Por favor, introduce una contraseña.',
            'min_length': 'La contraseña debe tener mínimo 6 caracteres.'})
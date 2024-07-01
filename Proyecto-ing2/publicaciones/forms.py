from django import forms 

class formularioCrearPublicacion(forms.Form):
    
    embarcacion = forms.CharField(label='embarcacion', max_length=50, error_messages={
            'required': 'Por favor, selleciona una embarcación.',})

    monto = forms.DecimalField(label='monto',max_digits=15, decimal_places=2, initial=0, required=False, error_messages={
            'max_digits': 'El número  ingresado es demasiado grande.',
            'max_decimal_places': 'El número ingresado tiene demasiados decimales.',
            'max_whole_digits': 'El número ingresado tiene demasiados dígitos.',
        })
    
    descripcion = forms.CharField(label='descripcion', max_length=250, required=False, error_messages= {
        'max_legth': 'El límite de caracteres es 250'
    })

class formularioEditarPublicacion(forms.Form):
    
    descripcion = forms.CharField(label='descripcion', max_length=250, required=False, error_messages= {
        'max_legth': 'El límite de caracteres es 250'
    })
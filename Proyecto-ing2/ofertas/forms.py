from django import forms 

class formularioCrearOferta(forms.Form):
    
    articulo_cambio = forms.CharField(label='articulo_cambio', max_length=50, error_messages={
            'required': 'Por favor, selleciona una embarcación o un vehiculo.',})

    monto = forms.DecimalField(label='monto',max_digits=15, decimal_places=2, initial=0, required=False, error_messages={
            'max_digits': 'El número  ingresado es demasiado grande.',
            'max_decimal_places': 'El número ingresado tiene demasiados decimales.',
            'max_whole_digits': 'El número ingresado tiene demasiados dígitos.',
        })
    
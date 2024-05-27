from django import forms
from .backend import validar_extensiones

class formularioCargaEmbarcacion(forms.Form):
    matricula = forms.CharField(label='matricula', max_length=50, error_messages={
            'required': 'Por favor, introduce una matricula.',
        })
    modelo= forms.CharField(label='modelo', max_length=50, error_messages={
            'required': 'Por favor, introduce un modelo.',
        })
    
    tipo = forms.CharField(label='tipo' , max_length=50, error_messages={
            'required': 'Por favor, selecciona un tipo.',
        })

    eslora= forms.DecimalField(label='eslora',max_digits=10, decimal_places=2, error_messages={
            'required': 'Por favor, introduce la eslora de la embarcación.',
            'max_digits': 'El número ingresado es demasiado grande.',
            'max_decimal_places': 'El número ingresado tiene demasiados decimales.',
            'max_whole_digits': 'El número ingresado tiene demasiados dígitos.',
        })

    manga= forms.DecimalField(label='manga',max_digits=10, decimal_places=2, error_messages={
            'required': 'Por favor, introduce la manga de la embarcación.',
            'max_digits': 'El número ingresado es demasiado grande.',
            'max_decimal_places': 'El número ingresado tiene demasiados decimales.',
            'max_whole_digits': 'El número ingresado tiene demasiados dígitos.',
        })

    calado= forms.DecimalField(label='calado',max_digits=10, decimal_places=2, error_messages={
            'required': 'Por favor, introduce el calado de la embarcación.',
            'max_digits': 'El número  ingresado es demasiado grande.',
            'max_decimal_places': 'El número ingresado tiene demasiados decimales.',
            'max_whole_digits': 'El número ingresado tiene demasiados dígitos.',
        })

    motor= forms.BooleanField(label= 'motor', initial=False, required=False)

    deuda = forms.DecimalField(label='deuda',max_digits=10, decimal_places=2, initial=0, required=False, error_messages={
            'required': 'Por favor, introduce la eslora de la embarcación.',
            'max_digits': 'El número  ingresado es demasiado grande.',
            'max_decimal_places': 'El número ingresado tiene demasiados decimales.',
            'max_whole_digits': 'El número ingresado tiene demasiados dígitos.',
        })
    
    sede= forms.CharField(label= 'sede', max_length=50, error_messages={
            'required': 'Por favor, seleciona una sede.',
        })

    imagen1 = forms.ImageField(label='imagen1', required=False, validators=[validar_extensiones])

    imagen2= forms.ImageField(label='imagen2', required=False, validators=[validar_extensiones])

    imagen3= forms.ImageField(label='imagen3', required=False, validators=[validar_extensiones])

    def clean_matricula(self):
        matricula = self.cleaned_data.get('matricula', '').upper()
        return matricula


class formularioEditarEmbarcacion(forms.Form):
    eslora= forms.DecimalField(label='eslora',max_digits=10, decimal_places=2, required=False, error_messages={
            'required': 'Por favor, introduce la eslora de la embarcación.',
            'max_digits': 'El número ingresado es demasiado grande.',
            'max_decimal_places': 'El número ingresado tiene demasiados decimales.',
            'max_whole_digits': 'El número ingresado tiene demasiados dígitos.',
        })

    manga= forms.DecimalField(label='manga',max_digits=10, decimal_places=2, required=False, error_messages={
            'required': 'Por favor, introduce la manga de la embarcación.',
            'max_digits': 'El número ingresado es demasiado grande.',
            'max_decimal_places': 'El número ingresado tiene demasiados decimales.',
            'max_whole_digits': 'El número ingresado tiene demasiados dígitos.',
        })

    calado= forms.DecimalField(label='calado',max_digits=10, decimal_places=2, required=False, error_messages={
            'required': 'Por favor, introduce la calado de la embarcación.',
            'max_digits': 'El número  ingresado es demasiado grande.',
            'max_decimal_places': 'El número ingresado tiene demasiados decimales.',
            'max_whole_digits': 'El número ingresado tiene demasiados dígitos.',
        })

    motor= forms.BooleanField(label= 'motor', initial=False, required=False)

    deuda = forms.DecimalField(label='deuda',max_digits=10, decimal_places=2, initial=0, required=False, error_messages={
            'required': 'Por favor, introduce la deuda de la embarcación.',
            'max_digits': 'El número  ingresado es demasiado grande.',
            'max_decimal_places': 'El número ingresado tiene demasiados decimales.',
            'max_whole_digits': 'El número ingresado tiene demasiados dígitos.',
        })
    
    sede= forms.CharField(label= 'sede', max_length=50, required=False)

    imagen1 = forms.ImageField(label='imagen1', required=False, validators=[validar_extensiones])

    imagen2= forms.ImageField(label='imagen2', required=False, validators=[validar_extensiones])

    imagen3= forms.ImageField(label='imagen3', required=False, validators=[validar_extensiones])

    def clean_matricula(self):
        matricula = self.cleaned_data.get('matricula', '').upper()
        return matricula
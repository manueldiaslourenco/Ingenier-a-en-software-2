from django.utils import timezone


def eliminar_logicamente_usuario(objeto):
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    objeto.mail = '*' + objeto.mail  + timestamp
    objeto.save()
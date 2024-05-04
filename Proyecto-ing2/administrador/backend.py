from datetime import datetime, date, timedelta

def calcular_edad(fecha_nacimiento):
    fecha_actual = datetime.now()
    edad = fecha_actual.year - fecha_nacimiento.year - ((fecha_actual.month, fecha_actual.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    return edad

def es_mayor_de_18(fecha_nacimiento):
    hace_18_años = date.today() - timedelta(days=365.25*18)
    return fecha_nacimiento <= hace_18_años
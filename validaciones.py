# ================================================================
# validaciones.py — Funciones de validacion reutilizables
# Funciones:
#   validar_telefono() — verifica formato de telefono
#   validar_dni()      — verifica formato de DNI
# ================================================================

import re  # modulo para validar con expresiones regulares


# Valida que el telefono tenga solo digitos y entre 8 y 15 caracteres
# Devuelve True si es valido, False si no
def validar_telefono(telefono):
    patron = re.compile(r"^\d{8,15}$")  # solo digitos, entre 8 y 15 caracteres
    resultado = patron.match(telefono)  # intenta hacer coincidir el patron
    return resultado is not None        # True si coincide, False si no


# Valida que el DNI tenga entre 7 y 8 digitos numericos
# Devuelve True si es valido, False si no
def validar_dni(dni):
    patron = re.compile(r"^\d{7,8}$")  # solo digitos, entre 7 y 8 caracteres
    resultado = patron.match(dni)
    return resultado is not None
# ============================================================
# SISTEMA DE GESTIÓN DE SERVICIOS - PyME Aire Acondicionado/Electricidad
# ============================================================

# ------------------------------------------------------------
# ESTRUCTURAS DE DATOS GLOBALES
# ------------------------------------------------------------
clientes = {}   # clave: telefono (str) -> {"nombre": str, "ordenes": [id_orden, ...]}
tecnicos = {}   # clave: id_tecnico (int) -> {"nombre": str, "especialidad": str, "disponible": bool}
ordenes = {}    # clave: id_orden (int) -> {datos de la orden}
pagos = {}      # clave: id_orden (int) -> {"cobrado": float, "facturado": float}
presupuestos = {}  # clave: id_orden (int) -> {datos del presupuesto}
 
ultimo_id_orden = 0
ultimo_id_tecnico = 0


# ================================================================
# MODULO 1 — Ordenes de Servicio
# Funciones:
#   cargar_clientes()            — lee el archivo JSON y devuelve el diccionario
#   guardar_clientes()           — guarda el diccionario en el archivo JSON
#   buscar_o_crear_cliente()     — busca por telefono, si no existe ofrece crearlo
#   crear_orden()                — registra una orden nueva
#   cambiar_estado_orden()       — avanza el estado de una orden existente
#   mostrar_ordenes_pendientes() — lista las ordenes activas del dia
# ================================================================

import json                                        # para leer y escribir archivos JSON
from datetime import date                          # para registrar la fecha de creacion
from validaciones import validar_telefono, validar_dni  # funciones de validacion compartidas

ARCHIVO_CLIENTES = "clientes.json"  # nombre del archivo donde se guardan los clientes

# Estados posibles de una orden, en orden de avance
ESTADOS_VALIDOS = ["pendiente", "en_proceso", "completada", "cobrada"]


# ----------------------------------------------------------------
# Lee el archivo JSON y devuelve el diccionario de clientes
# Si el archivo no existe o esta corrupto, devuelve diccionario vacio
# ----------------------------------------------------------------
def cargar_clientes():
    try:
        archivo = open(ARCHIVO_CLIENTES, "r", encoding="UTF-8")  # abre en modo lectura
        contenido = archivo.read()                                # lee todo el texto
        archivo.close()                                           # cierra el archivo
        clientes = json.loads(contenido)                          # convierte JSON a diccionario
        return clientes
    except FileNotFoundError:
        # ocurre si el archivo todavia no existe
        print("Aviso: no se encontro el archivo de clientes. Se empieza con lista vacia.")
        return {}
    except json.JSONDecodeError:
        # ocurre si el archivo existe pero el contenido no es JSON valido
        print("Error: el archivo de clientes esta corrupto. Se empieza con lista vacia.")
        return {}


# ----------------------------------------------------------------
# Guarda el diccionario de clientes en el archivo JSON
# ----------------------------------------------------------------
def guardar_clientes(clientes):
    try:
        archivo = open(ARCHIVO_CLIENTES, "w", encoding="UTF-8")        # abre en modo escritura
        contenido = json.dumps(clientes, indent=4, ensure_ascii=False)  # convierte a JSON prolijo
        archivo.write(contenido)                                         # escribe el contenido
        archivo.close()                                                  # cierra el archivo
        print("Datos guardados correctamente.")
    except OSError:
        # ocurre si no se puede escribir (permisos, disco lleno, etc)
        print("Error: no se pudieron guardar los datos.")


# ----------------------------------------------------------------
# Busca un cliente por telefono
# Si no existe, pregunta si se quiere cargar como cliente nuevo
# Devuelve el telefono si el cliente queda disponible, o None si se cancela
# ----------------------------------------------------------------
def buscar_o_crear_cliente(clientes):
    telefono = input("Ingresa el telefono del cliente (solo numeros): ").strip()

    # Validamos el formato del telefono
    if not validar_telefono(telefono):
        print("Telefono invalido. Debe tener entre 8 y 15 digitos numericos.")
        return None

    # Si ya existe, lo devolvemos directamente
    if telefono in clientes:
        print("Cliente encontrado:", clientes[telefono]["nombre"])
        return telefono

    # Si no existe, ofrecemos cargarlo
    print("El cliente con telefono", telefono, "no existe en el sistema.")
    respuesta = input("Queres cargarlo ahora? (s/n): ").strip().lower()

    if respuesta != "s":
        print("Operacion cancelada.")
        return None

    # Pedimos los datos del cliente nuevo
    nombre = input("Nombre completo: ").strip()

    if nombre == "":
        print("El nombre no puede estar vacio.")
        return None

    # DNI es opcional, pero si lo ingresan lo validamos
    dni = input("DNI (opcional, Enter para omitir): ").strip()

    if dni != "" and not validar_dni(dni):
        print("DNI invalido. Debe tener entre 7 y 8 digitos numericos.")
        return None

    # Verificamos que el DNI no este ya usado por otro cliente
    # Usamos un conjunto para guardar los DNIs registrados y comparar rapido
    if dni != "":
        dnis_registrados = set()                             # conjunto vacio
        for tel in clientes:                                 # recorremos todos los clientes
            dni_existente = clientes[tel].get("dni", "")    # obtenemos el DNI si existe
            if dni_existente != "":
                dnis_registrados.add(dni_existente)          # lo agregamos al conjunto

        if dni in dnis_registrados:                          # si el DNI ya esta registrado
            print("Ese DNI ya esta registrado en otro cliente.")
            return None

    direccion = input("Direccion: ").strip()

    # Pedimos el tipo de cliente
    print("Tipo de cliente:")
    print("  1. Frecuente")
    print("  2. Nuevo")
    print("  3. Problematico")

    opcion_tipo = input("Elegis una opcion (1/2/3): ").strip()

    if opcion_tipo == "1":
        tipo = "frecuente"
    elif opcion_tipo == "2":
        tipo = "nuevo"
    elif opcion_tipo == "3":
        tipo = "problematico"
    else:
        print("Opcion invalida. Se asigna tipo 'nuevo' por defecto.")
        tipo = "nuevo"

    # Creamos el cliente y lo agregamos al diccionario
    clientes[telefono] = {
        "nombre": nombre,
        "dni": dni,           # puede ser string vacio si no lo ingresaron
        "direccion": direccion,
        "tipo": tipo,
        "ordenes": []
    }

    print("Cliente", nombre, "cargado correctamente.")
    return telefono


# ----------------------------------------------------------------
# Registra una orden nueva vinculada a un cliente
# ----------------------------------------------------------------
def crear_orden(clientes, ordenes, ultimo_id_orden):
    telefono = buscar_o_crear_cliente(clientes)

    if telefono is None:          # si se cancelo o hubo error
        return ultimo_id_orden    # devolvemos el contador sin cambios

    cliente = clientes[telefono]

    # Alertamos si el cliente es problematico
    if cliente["tipo"] == "problematico":
        print("AVISO: este cliente esta marcado como PROBLEMATICO.")
        confirmar = input("Queres continuar igual? (s/n): ").strip().lower()
        if confirmar != "s":
            print("Orden cancelada.")
            return ultimo_id_orden

    descripcion = input("Descripcion del problema: ").strip()

    if descripcion == "":
        print("La descripcion no puede estar vacia.")
        return ultimo_id_orden

    fecha_visita = input("Fecha de visita (YYYY-MM-DD) o Enter para dejar sin fecha: ").strip()

    # Generamos el ID de la orden nueva
    ultimo_id_orden = ultimo_id_orden + 1          # incrementamos el contador
    id_orden = "ORD-" + str(ultimo_id_orden)       # formato: ORD-1, ORD-2, etc

    fecha_hoy = str(date.today())                  # fecha actual como string

    # Creamos la orden
    ordenes[id_orden] = {
        "id": id_orden,
        "telefono_cliente": telefono,              # vinculamos por telefono
        "descripcion": descripcion,
        "estado": "pendiente",                     # toda orden arranca como pendiente
        "fecha_creacion": fecha_hoy,
        "fecha_visita": fecha_visita if fecha_visita != "" else None,
        "tecnico_id": None,                        # se asigna desde el modulo 2
        "repuestos": [],                           # se carga desde el modulo 5
        "monto_total": 0                           # se calcula desde el modulo 3
    }

    # Vinculamos la orden al cliente
    clientes[telefono]["ordenes"].append(id_orden)

    guardar_clientes(clientes)  # guardamos los cambios en el archivo

    print("Orden", id_orden, "creada correctamente para", cliente["nombre"])
    return ultimo_id_orden


# ----------------------------------------------------------------
# Avanza el estado de una orden al siguiente estado valido
# ----------------------------------------------------------------
def cambiar_estado_orden(ordenes, clientes):
    id_orden = input("Ingresa el ID de la orden (ej: ORD-1): ").strip()

    if id_orden not in ordenes:
        print("No se encontro una orden con ese ID.")
        return

    orden = ordenes[id_orden]
    estado_actual = orden["estado"]
    indice_actual = ESTADOS_VALIDOS.index(estado_actual)  # posicion del estado actual en la lista

    if indice_actual == len(ESTADOS_VALIDOS) - 1:         # si ya esta en el ultimo estado
        print("La orden ya esta en estado", estado_actual, "y no puede avanzar mas.")
        return

    estado_nuevo = ESTADOS_VALIDOS[indice_actual + 1]     # siguiente estado en la lista

    print("Estado actual:", estado_actual, "-> Nuevo estado:", estado_nuevo)
    confirmar = input("Confirmas el cambio? (s/n): ").strip().lower()

    if confirmar != "s":
        print("Cambio cancelado.")
        return

    ordenes[id_orden]["estado"] = estado_nuevo  # aplicamos el cambio

    if estado_nuevo == "cobrada":               # mensaje extra si paso a cobrada
        telefono = orden["telefono_cliente"]
        if telefono in clientes:
            print("Orden cobrada para el cliente:", clientes[telefono]["nombre"])

    guardar_clientes(clientes)
    print("Estado actualizado a:", estado_nuevo)


# ----------------------------------------------------------------
# Muestra todas las ordenes pendientes o en proceso
# ----------------------------------------------------------------
def mostrar_ordenes_pendientes(ordenes, clientes):
    activas = []

    for id_orden in ordenes:
        orden = ordenes[id_orden]
        if orden["estado"] == "pendiente" or orden["estado"] == "en_proceso":
            activas.append(orden)

    if len(activas) == 0:
        print("No hay ordenes pendientes ni en proceso.")
        return

    print("==================================================")
    print("ORDENES ACTIVAS HOY:", len(activas))
    print("==================================================")

    for orden in activas:
        telefono = orden["telefono_cliente"]

        if telefono in clientes:
            nombre = clientes[telefono]["nombre"]
        else:
            nombre = "Cliente desconocido"

        print("  ID:", orden["id"], "| Cliente:", nombre, "(", telefono, ")")
        print("  Estado:", orden["estado"], "| Visita:", orden["fecha_visita"] or "Sin fecha")
        print("  Descripcion:", orden["descripcion"])
        print()

# ============================================================
# MODULO 2 - GESTION DE TÉCNICOS
# ============================================================

def registrar_tecnico():  # Modulo 2 - Registrar técnico
    print("")
 

def mostrar_tecnicos():   #Modulo 2 - Mostrar técnicos
    print("")
 

def asignar_tecnico_a_orden():  #Modulo 2 - Asignar técnico a orden
    print("")
 
 
# ============================================================
# MODULO 3 - CONTROL DE PAGOS Y DEUDAS
# ============================================================
 
def registrar_pago(): #Modulo 3 - Registrar pago
    print("")
 
def ver_estado_pagos(): #Modulo 3 - Ver estado de pagos / deudas
    print("")
 
# ============================================================
# MODULO 4 - BUSQUEDA E HISTORIAL DE CLIENTES
# ============================================================
 
def buscar_cliente(): #Modulo 4 - Buscar cliente
    print("") 
 
 
def ver_historial_cliente(): #Modulo 4 - Ver historial de cliente
    print("")
 
# ============================================================
# MODULO 5 - PRESUPUESTOS Y COSTOS
# ============================================================
 
def generar_presupuesto(): #Modulo 5 - Generar presupuesto
    print("")
 
 
def ver_presupuestos(): #Modulo 5 - Ver presupuestos
    print("")
 

# ============================================================
# MENU PRINCIPAL
# ============================================================
 
def menu():
    opcion = ""
    ultimo_id_orden = 0   # contador de ordenes
    ordenes = {}          # diccionario de ordenes
    clientes = {}         # diccionario de clientes
    tecnicos = {}         # diccionario de tecnicos
    pagos = {}            # diccionario de pagos
    presupuestos = {}     # diccionario de presupuestos
    while opcion != "0":
        print("\n========== SISTEMA DE GESTIÓN - SERVICIOS TÉCNICOS ==========")
        print("=== Órdenes de Servicio ===")
        print("1. Crear orden de servicio")
        print("2. Cambiar estado de una orden")
        print("3. Ver órdenes pendientes\n") 
        print("--- Técnicos ---")
        print("4. Registrar técnico")
        print("5. Mostrar técnicos")
        print("6. Asignar técnico a una orden\n")
        print("--- Pagos ---")
        print("7. Registrar pago")
        print("8. Ver estado de pagos / deudas\n")
        print("--- Clientes ---")
        print("9. Buscar cliente")
        print("10. Ver historial de cliente\n")
        print("--- Presupuestos ---")
        print("11. Generar presupuesto")
        print("12. Ver presupuestos")
        print("0. Salir")
        print("==============================================================")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            ultimo_id_orden = crear_orden(clientes, ordenes, ultimo_id_orden)  
        elif opcion == "2":
            cambiar_estado_orden(ordenes, clientes)  
        elif opcion == "3":
            mostrar_ordenes_pendientes(ordenes, clientes)  # pasamos ambas estructuras necesarias
        elif opcion == "4":
            registrar_tecnico()
        elif opcion == "5":
            mostrar_tecnicos()
        elif opcion == "6":
            asignar_tecnico_a_orden()
        elif opcion == "7":
            registrar_pago()
        elif opcion == "8":
            ver_estado_pagos()
        elif opcion == "9":
            buscar_cliente()
        elif opcion == "10":
            ver_historial_cliente()
        elif opcion == "11":
            generar_presupuesto()
        elif opcion == "12":
            ver_presupuestos()
        elif opcion == "0":
            print("Saliendo del sistema...")
        else:
            print("Opción inválida. Intente nuevamente.")

menu()
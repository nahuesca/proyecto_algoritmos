# ======================================================================
# SISTEMA DE GESTION DE SERVICIOS - PyME Aire Acondicionado/Electricidad
# ======================================================================

# ESTRUCTURAS DE DATOS GLOBALES
# ------------------------------------------------------------
clientes = {} # clave: telefono (str) -> datos del cliente y lista de ordenes
tecnicos = {} # clave: id_tecnico (int) -> datos del tecnico y disponibilidad
ordenes = {}  # clave: id_orden (str) -> datos completos de la orden
pagos = {}  # clave: id_orden (str) -> montos cobrado y facturado
presupuestos = {}  # clave: id_orden (str) -> datos del presupuesto

ultimo_id_orden = 0    # contador global de ordenes creadas
ultimo_id_tecnico = 0  # contador global de tecnicos registrados


# MODULO 1 - Ordenes de Servicio
# Funciones:
#   cargar_clientes()            - lee el archivo JSON y devuelve el diccionario
#   guardar_clientes()           - guarda el diccionario en el archivo JSON
#   buscar_o_crear_cliente()     - busca por telefono, si no existe ofrece crearlo
#   crear_orden()                - registra una orden nueva
#   cambiar_estado_orden()       - avanza el estado de una orden existente
#   mostrar_ordenes_pendientes() - lista las ordenes activas del dia
# ================================================================

import json # para leer y escribir archivos JSON
from datetime import date  # para registrar la fecha de creacion
from validaciones import validar_telefono, validar_dni  # funciones de validacion compartidas

ARCHIVO_CLIENTES = "clientes.json"  # nombre del archivo donde se guardan los clientes
ARCHIVO_TECNICOS = "tecnicos.json"  # nombre del archivo donde se guardan los tecnicos

ESTADOS_VALIDOS = ["pendiente", "en_proceso", "completada", "cobrada"]  # estados posibles en orden de avance


# ================================================================
# Lee el archivo JSON y devuelve el diccionario de clientes
# Si el archivo no existe o esta corrupto, devuelve diccionario vacio
def cargar_clientes():
    try:
        archivo = open(ARCHIVO_CLIENTES, "r", encoding="UTF-8")  # abre en modo lectura
        contenido = archivo.read() # lee todo el texto
        archivo.close() # cierra el archivo
        clientes = json.loads(contenido) # convierte JSON a diccionario
        return clientes # devuelve el diccionario cargado
    except FileNotFoundError:
        print("Aviso: no se encontro el archivo de clientes. Se empieza con lista vacia.")  # archivo no existe aun
        return {} # devuelve diccionario vacio
    except json.JSONDecodeError:
        print("Error: el archivo de clientes esta corrupto. Se empieza con lista vacia.")   # JSON invalido
        return {} # devuelve diccionario vacio

# ================================================================
# Guarda el diccionario de clientes en el archivo JSON
# ================================================================
def guardar_clientes(clientes):
    try:
        archivo = open(ARCHIVO_CLIENTES, "w", encoding="UTF-8") # abre en modo escritura
        contenido = json.dumps(clientes, indent=4, ensure_ascii=False)   # convierte a JSON prolijo
        archivo.write(contenido) # escribe el contenido
        archivo.close() # cierra el archivo
        print("Datos guardados correctamente.") # confirma al usuario
    except OSError:
        print("Error: no se pudieron guardar los datos.") # error de permisos o disco lleno

# ================================================================
# Busca un cliente por telefono
# Si no existe, pregunta si se quiere cargar como cliente nuevo
# Devuelve el telefono si el cliente queda disponible, o None si se cancela
# ================================================================
def buscar_o_crear_cliente(clientes):
    telefono = input("Ingresa el telefono del cliente (solo numeros): ").strip()  # pide el telefono

    if not validar_telefono(telefono): # valida el formato
        print("Telefono invalido. Debe tener entre 8 y 15 digitos numericos.")
        return None # cancela si el formato es invalido

    if telefono in clientes: # si ya existe en el sistema
        print("Cliente encontrado:", clientes[telefono]["nombre"])
        return telefono # devuelve el telefono directamente

    print("El cliente con telefono", telefono, "no existe en el sistema.")
    respuesta = input("Queres cargarlo ahora? (s/n): ").strip().lower()  # pregunta si lo carga

    if respuesta != "s": # si no confirma
        print("Operacion cancelada.")
        return None # cancela la operacion

    nombre = input("Nombre completo: ").strip() # pide el nombre

    if nombre == "":# nombre no puede estar vacio
        print("El nombre no puede estar vacio.")
        return None  # cancela si esta vacio

    dni = input("DNI (opcional, Enter para omitir): ").strip() # pide el DNI (es opcional)

    if dni != "" and not validar_dni(dni): # valida solo si lo ingresaron
        print("DNI invalido. Debe tener entre 7 y 8 digitos numericos.")
        return None # cancela si el DNI es invalido

    if dni != "": # si ingresaron un DNI
        dnis_registrados = set() # conjunto para comparar rapido
        for tel in clientes:  # recorre todos los clientes
            dni_existente = clientes[tel].get("dni", "") # obtiene el DNI si existe
            if dni_existente != "":  # si el cliente tiene DNI
                dnis_registrados.add(dni_existente) # lo agrega al conjunto

        if dni in dnis_registrados: # si el DNI ya esta registrado
            print("Ese DNI ya esta registrado en otro cliente.")
            return None # cancela para evitar duplicado

    direccion = input("Direccion: ").strip() # pide la direccion
    print("Tipo de cliente:") # muestra las opciones disponibles
    print("  1. Frecuente")
    print("  2. Nuevo")
    print("  3. Problematico")
    opcion_tipo = input("Elegis una opcion (1/2/3): ").strip() # pide la opcion

    if opcion_tipo == "1":  # asigna el tipo segun la opcion
        tipo = "frecuente"
    elif opcion_tipo == "2":
        tipo = "nuevo"
    elif opcion_tipo == "3":
        tipo = "problematico"
    else:
        print("Opcion invalida. Se asigna tipo 'nuevo' por defecto.")
        tipo = "nuevo" # valor por defecto si la opcion no es valida

    clientes[telefono] = {  # crea la entrada del cliente
        "nombre": nombre,
        "dni": dni,  # puede ser string vacio si no lo ingresaron
        "direccion": direccion,
        "tipo": tipo,
        "ordenes": [] # empieza sin ordenes
    }

    print("Cliente", nombre, "cargado correctamente.")
    return telefono # devuelve el telefono del nuevo cliente


# ================================================================
# Registra una orden nueva vinculada a un cliente
# ================================================================
def crear_orden(clientes, ordenes, ultimo_id_orden):
    telefono = buscar_o_crear_cliente(clientes) # obtiene o crea el cliente

    if telefono is None: # si se cancelo o hubo error
        return ultimo_id_orden # devuelve el contador sin cambios

    cliente = clientes[telefono] # referencia al cliente encontrado

    if cliente["tipo"] == "problematico":                                # alerta si es cliente problematico
        print("AVISO: este cliente esta marcado como PROBLEMATICO.")
        confirmar = input("Queres continuar igual? (s/n): ").strip().lower()
        if confirmar != "s": # si no confirma, cancela
            print("Orden cancelada.")
            return ultimo_id_orden                                       # devuelve el contador sin cambios

    descripcion = input("Descripcion del problema: ").strip() # pide la descripcion del trabajo

    if descripcion == "": # descripcion es obligatoria
        print("La descripcion no puede estar vacia.")
        return ultimo_id_orden # cancela si esta vacia

    fecha_visita = input("Fecha de visita (YYYY-MM-DD) o Enter para dejar sin fecha: ").strip()  # pide la fecha

    ultimo_id_orden = ultimo_id_orden + 1 # incrementa el contador
    id_orden = "ORD-" + str(ultimo_id_orden) # genera el ID en formato ORD-1, ORD-2...

    fecha_hoy = str(date.today())# obtiene la fecha actual como string

    ordenes[id_orden] = { # crea la orden en el diccionario
        "id": id_orden, # identificador de la orden
        "telefono_cliente": telefono,# vincula al cliente por telefono
        "descripcion": descripcion,# detalle del problema
        "estado": "pendiente",# toda orden arranca como pendiente
        "fecha_creacion": fecha_hoy,# fecha de registro
        "fecha_visita": fecha_visita if fecha_visita != "" else None,   # None si no ingresaron fecha
        "tecnico_id": None,# se asigna desde el modulo 2
        "repuestos": [],# se carga desde el modulo 5
        "monto_total": 0# se calcula desde el modulo 3
    }

    clientes[telefono]["ordenes"].append(id_orden) # vincula la orden al cliente

    guardar_clientes(clientes) # guarda los cambios en el archivo

    print("Orden", id_orden, "creada correctamente para", cliente["nombre"])
    return ultimo_id_orden   # devuelve el contador actualizado


# ================================================================
# Avanza el estado de una orden al siguiente estado valido
# ================================================================
def cambiar_estado_orden(ordenes, clientes):
    id_orden = input("Ingresa el ID de la orden (ej: ORD-1): ").strip()  # pide el ID de la orden

    if id_orden not in ordenes:  # verifica que exista
        print("No se encontro una orden con ese ID.")
        return  # sale si no existe

    orden = ordenes[id_orden]   # referencia a la orden
    estado_actual = orden["estado"]  # estado en el que esta ahora
    indice_actual = ESTADOS_VALIDOS.index(estado_actual)  # posicion en la lista de estados

    if indice_actual == len(ESTADOS_VALIDOS) - 1:  # si ya esta en el ultimo estado
        print("La orden ya esta en estado", estado_actual, "y no puede avanzar mas.")
        return   # no hay mas estados posibles

    estado_nuevo = ESTADOS_VALIDOS[indice_actual + 1]  # toma el siguiente estado en la lista

    print("Estado actual:", estado_actual, "-> Nuevo estado:", estado_nuevo)
    confirmar = input("Confirmas el cambio? (s/n): ").strip().lower()   # pide confirmacion

    if confirmar != "s": # si no confirma
        print("Cambio cancelado.")
        return   # cancela el cambio

    ordenes[id_orden]["estado"] = estado_nuevo # aplica el nuevo estado

    if estado_nuevo == "cobrada": # mensaje extra al pasar a cobrada
        telefono = orden["telefono_cliente"] # obtiene el telefono del cliente
        if telefono in clientes:   # verifica que el cliente exista
            print("Orden cobrada para el cliente:", clientes[telefono]["nombre"])

    guardar_clientes(clientes) # guarda los cambios
    print("Estado actualizado a:", estado_nuevo)


# ================================================================
# Muestra todas las ordenes pendientes o en proceso
# ================================================================
def mostrar_ordenes_pendientes(ordenes, clientes):
    activas = [] # lista para acumular las ordenes activas

    for id_orden in ordenes:  # recorre todas las ordenes
        orden = ordenes[id_orden]  # referencia a la orden actual
        if orden["estado"] == "pendiente" or orden["estado"] == "en_proceso":  # filtra las activas
            activas.append(orden) # agrega a la lista

    if len(activas) == 0:  # si no hay ordenes activas
        print("No hay ordenes pendientes ni en proceso.")
        return  # sale sin mostrar nada

    print("==================================================")
    print("ORDENES ACTIVAS HOY:", len(activas)) # muestra el total de activas
    print("==================================================")

    for orden in activas: # recorre las ordenes activas
        telefono = orden["telefono_cliente"] # obtiene el telefono del cliente

        if telefono in clientes: # busca el nombre del cliente
            nombre = clientes[telefono]["nombre"]
        else:
            nombre = "Cliente desconocido" # fallback si no se encuentra

        print("  ID:", orden["id"], "| Cliente:", nombre, "(", telefono, ")")
        print("  Estado:", orden["estado"], "| Visita:", orden["fecha_visita"] or "Sin fecha")
        print("  Descripcion:", orden["descripcion"])
        print()  # linea en blanco entre ordenes


# ============================================================
# MODULO 2 - GESTION DE TECNICOS
# ============================================================

#AGREGAR REASIGNAR TECNICO
#VALIDAR TELEFONO TECNICO

# Lee el archivo JSON y devuelve el diccionario de tecnicos
def cargar_tecnicos():
    try:
        archivo = open(ARCHIVO_TECNICOS, "r", encoding="UTF-8")  # abre en lectura
        contenido = archivo.read() # lee el contenido
        archivo.close() # cierra el archivo
        return json.loads(contenido)  # convierte a diccionario y devuelve
    except FileNotFoundError:
        print("Aviso: no se encontro el archivo de tecnicos. Se empieza con lista vacia.")  # archivo no existe aun
        return {} # devuelve diccionario vacio
    except json.JSONDecodeError:
        print("Error: el archivo de tecnicos esta corrupto. Se empieza con lista vacia.")   # JSON invalido
        return {} # devuelve diccionario vacio


# Guarda el diccionario de tecnicos en el archivo JSON
def guardar_tecnicos(tecnicos):
    try:
        archivo = open(ARCHIVO_TECNICOS, "w", encoding="UTF-8")    # abre en escritura
        contenido = json.dumps(tecnicos, indent=4, ensure_ascii=False)   # convierte a JSON prolijo
        archivo.write(contenido)    # escribe el contenido
        archivo.close() # cierra el archivo
    except OSError:
        print("Error: no se pudieron guardar los datos de tecnicos.") # error de permisos o disco lleno


# Registra un tecnico nuevo y devuelve el contador actualizado
# Ya no tiene campo "disponible" porque se deriva de las ordenes
def registrar_tecnico(tecnicos, ultimo_id_tecnico):
    print("\n--- Registro de Nuevo Tecnico ---")

    nombre = ""
    while nombre.strip() == "": # no acepta nombre vacio
        nombre = input("Nombre del tecnico: ").strip()

    especialidad = ""
    while especialidad.strip() == "": # no acepta especialidad vacia
        especialidad = input("Especialidad: ").strip()

    while True: # repite hasta que el telefono sea valido o el usuario lo omita
        telefono = input("Telefono del tecnico (opcional, Enter para omitir): ").strip() # campo opcional
        if telefono == "" or validar_telefono(telefono): # vacio es valido, o bien pasa la validacion
            break # sale del bucle si es aceptable
        print("Telefono invalido. Debe tener entre 8 y 15 digitos numericos.") # avisa y vuelve a pedir

    ultimo_id_tecnico = ultimo_id_tecnico + 1 # incrementa el contador

    tecnicos[ultimo_id_tecnico] = {
        "nombre": nombre,
        "especialidad": especialidad,
        "telefono": telefono,
        "ordenes_asignadas": []  # empieza sin ordenes, sin campo disponible
    }

    guardar_tecnicos(tecnicos)
    print("Tecnico", nombre, "registrado con ID:", ultimo_id_tecnico)
    return ultimo_id_tecnico


# Determina si un tecnico esta disponible revisando sus ordenes activas
# Un tecnico esta ocupado si tiene al menos una orden en estado en_proceso
def esta_disponible(id_tecnico, tecnicos, ordenes):
    for id_o in tecnicos[id_tecnico]["ordenes_asignadas"]:  # recorre las ordenes del tecnico
        if id_o in ordenes and ordenes[id_o]["estado"] == "en_proceso":  # si hay una activa
            return False  # esta ocupado
    return True  # si no hay ninguna activa, esta libre


# Lista todos los tecnicos y calcula su estado en base a las ordenes
def mostrar_tecnicos(tecnicos, ordenes):
    print("\n--- Estado del Equipo de Tecnicos ---")
    if not tecnicos:
        print("No hay tecnicos registrados en el sistema.")
        return

    for id_t in tecnicos: # recorre el diccionario
        datos = tecnicos[id_t]
        if esta_disponible(id_t, tecnicos, ordenes): # calcula disponibilidad en el momento
            estado = "Disponible"
        else:
            estado = "Ocupado"
        print("ID:", id_t, "| Nombre:", datos["nombre"], "| Especialidad:", datos["especialidad"], "| Estado:", estado)


# Devuelve lista de IDs de tecnicos sin ordenes activas en este momento
def obtener_tecnicos_disponibles(tecnicos, ordenes):
    disponibles = []
    for id_t in tecnicos: # recorre todos los tecnicos
        if esta_disponible(id_t, tecnicos, ordenes): # usa la funcion auxiliar
            disponibles.append(id_t)

    if not disponibles:
        print("No hay tecnicos disponibles en este momento.")
    return disponibles


# Asigna un tecnico disponible a una orden existente
def asignar_tecnico_a_orden(tecnicos, ordenes):
    print("\n--- Asignar Tecnico a Orden ---")
    disponibles = obtener_tecnicos_disponibles(tecnicos, ordenes)  # pasa ordenes tambien
    if not disponibles:
        return

    try:
        id_tecnico = int(input("Ingrese el ID del tecnico: "))
    except ValueError:
        print("Error: el ID del tecnico debe ser un numero.")
        return

    id_orden = input("Ingrese el ID de la orden (ej: ORD-1): ").strip()

    if id_tecnico in tecnicos and id_orden in ordenes:
        tecnicos[id_tecnico]["ordenes_asignadas"].append(id_orden)  # registra en historial

        ordenes[id_orden]["tecnico_id"] = id_tecnico  # vincula el tecnico a la orden
        ordenes[id_orden]["estado"] = "en_proceso" # avanza el estado

        guardar_tecnicos(tecnicos)
        print("Tecnico", tecnicos[id_tecnico]["nombre"], "asignado a orden", id_orden)
    else:
        print("Error: Tecnico u orden no encontrados.")


# Marca la ultima orden del tecnico como completada
# La disponibilidad se recalcula sola al cambiar el estado de la orden
def finalizar_trabajo_tecnico(id_tecnico, tecnicos, ordenes):
    if id_tecnico not in tecnicos:
        print("Error: Tecnico no encontrado.")
        return

    if esta_disponible(id_tecnico, tecnicos, ordenes): # ya esta libre
        print("El tecnico ya no tiene ordenes activas.")
        return

    if tecnicos[id_tecnico]["ordenes_asignadas"]:
        id_ultima_orden = tecnicos[id_tecnico]["ordenes_asignadas"][-1]  # toma la ultima orden
        if id_ultima_orden in ordenes:
            ordenes[id_ultima_orden]["estado"] = "completada"  # cambia el estado, eso lo libera

    guardar_tecnicos(tecnicos)
    print("El tecnico", tecnicos[id_tecnico]["nombre"], "finalizo su orden y esta disponible.")

# ============================================================
# MODULO 3 - CONTROL DE PAGOS Y DEUDAS
# ============================================================

# Registra un pago asociado a una orden
def registrar_pago():
    print("")  # pendiente de implementacion


# Muestra el estado de pagos y deudas de los clientes
def ver_estado_pagos():
    print("")  # pendiente de implementacion


# ============================================================
# MODULO 4 - BUSQUEDA E HISTORIAL DE CLIENTES
# ============================================================

# Busca un cliente por nombre o telefono
def buscar_cliente():
    print("")  # pendiente de implementacion


# Muestra el historial completo de un cliente
def ver_historial_cliente():
    print("")  # pendiente de implementacion


# ============================================================
# MODULO 5 - PRESUPUESTOS Y COSTOS
# ============================================================

# Genera un presupuesto para una orden
def generar_presupuesto():
    print("")  # pendiente de implementacion


# Lista todos los presupuestos registrados
def ver_presupuestos():
    print("")  # pendiente de implementacion


# ============================================================
# MENU PRINCIPAL
# ============================================================

def menu():
    opcion = ""  # valor inicial para entrar al while
    ultimo_id_orden = 0  # contador de ordenes creadas en esta sesion
    ultimo_id_tecnico = 0 # contador de tecnicos registrados en esta sesion
    ordenes = {}  # diccionario de ordenes, vacio al arrancar
    clientes = cargar_clientes()  # carga clientes desde archivo al iniciar
    tecnicos = cargar_tecnicos() # carga tecnicos desde archivo al iniciar
    pagos = {} # diccionario de pagos, vacio al arrancar
    presupuestos = {} # diccionario de presupuestos, vacio al arrancar

    while opcion != "0": # repite hasta que el usuario elija salir
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

        opcion = input("Seleccione una opción: ") # lee la opcion del usuario

        if opcion == "1":  # crear orden de servicio
            ultimo_id_orden = crear_orden(clientes, ordenes, ultimo_id_orden)
        elif opcion == "2": # cambiar estado de una orden
            cambiar_estado_orden(ordenes, clientes)
        elif opcion == "3": # ver ordenes pendientes
            mostrar_ordenes_pendientes(ordenes, clientes)
        elif opcion == "4": # registrar un tecnico nuevo
            ultimo_id_tecnico = registrar_tecnico(tecnicos, ultimo_id_tecnico)
        elif opcion == "5":
            mostrar_tecnicos(tecnicos, ordenes)
        elif opcion == "6":
            asignar_tecnico_a_orden(tecnicos, ordenes)
        elif opcion == "7":   # registrar un pago
            registrar_pago()
        elif opcion == "8":  # ver pagos y deudas
            ver_estado_pagos()
        elif opcion == "9":  # buscar un cliente
            buscar_cliente()
        elif opcion == "10":   # ver historial de un cliente
            ver_historial_cliente()
        elif opcion == "11":  # generar un presupuesto
            generar_presupuesto()
        elif opcion == "12": # ver presupuestos existentes
            ver_presupuestos()
        elif opcion == "0":  # salir del sistema
            print("Saliendo del sistema...")
        else:
            print("Opción inválida. Intente nuevamente.") # opcion no reconocida

menu()  # punto de entrada del programa


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
import re # para busqueda flexible de texto con expresiones regulares
from datetime import date  # para registrar la fecha de creacion
from validaciones import validar_telefono, validar_dni  # funciones de validacion compartidas

ARCHIVO_CLIENTES = "clientes.json"  # nombre del archivo donde se guardan los clientes
ARCHIVO_TECNICOS = "tecnicos.json"  # nombre del archivo donde se guardan los tecnicos
ARCHIVO_PAGOS = "pagos.json"  # nombre del archivo donde se guardan los pagos

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
def crear_orden(clientes, ordenes, ultimo_id_orden, pagos):
    telefono = buscar_o_crear_cliente(clientes) # obtiene o crea el cliente

    if telefono is None: # si se cancelo o hubo error
        return ultimo_id_orden # devuelve el contador sin cambios

    alerta_deuda(telefono, pagos, clientes) # avisa si el cliente tiene deuda pendiente

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

def reasignar_tecnico_a_orden(tecnicos, ordenes):
    print("\n--- Reasignar Tecnico a Orden ---")

    id_orden = input("Ingrese el ID de la orden a reasignar (ej: ORD-1): ").strip()  # pide la orden

    if id_orden not in ordenes:  # verifica que la orden exista
        print("No se encontro una orden con ese ID.")
        return  # sale si no existe

    orden = ordenes[id_orden]  # referencia a la orden

    if orden["estado"] == "completada" or orden["estado"] == "cobrada":  # no reasignar si ya termino
        print("La orden ya esta", orden["estado"], "y no se puede reasignar.")
        return  # sale sin hacer cambios

    id_tecnico_actual = orden["tecnico_id"]  # tecnico que tenia la orden

    if id_tecnico_actual is None:  # si la orden no tenia tecnico asignado todavia
        print("Esta orden no tiene tecnico asignado. Use la opcion de asignar tecnico.")
        return  # redirige al usuario a la funcion correcta

    nombre_anterior = tecnicos[id_tecnico_actual]["nombre"]  # nombre del tecnico que se va a sacar
    print("Tecnico actual:", nombre_anterior)

    disponibles = obtener_tecnicos_disponibles(tecnicos, ordenes)  # lista de tecnicos libres

    if not disponibles:  # si no hay ninguno libre
        return  # sale, obtener_tecnicos_disponibles ya imprimio el aviso

    try:
        id_tecnico_nuevo = int(input("Ingrese el ID del nuevo tecnico: "))  # pide el ID del nuevo
    except ValueError:
        print("Error: el ID del tecnico debe ser un numero.")
        return  # sale si no es un numero

    if id_tecnico_nuevo not in tecnicos:  # verifica que el tecnico nuevo exista
        print("No se encontro un tecnico con ese ID.")
        return  # sale si no existe

    if id_tecnico_nuevo == id_tecnico_actual:  # no tiene sentido reasignar al mismo
        print("El tecnico nuevo es el mismo que el actual. No se realizo ningun cambio.")
        return  # sale sin cambios

    if id_tecnico_nuevo not in disponibles:  # verifica que el nuevo este disponible
        print("El tecnico seleccionado no esta disponible en este momento.")
        return  # sale si esta ocupado

    # saca la orden del historial del tecnico anterior
    if id_orden in tecnicos[id_tecnico_actual]["ordenes_asignadas"]:
        tecnicos[id_tecnico_actual]["ordenes_asignadas"].remove(id_orden)

    # agrega la orden al historial del tecnico nuevo
    tecnicos[id_tecnico_nuevo]["ordenes_asignadas"].append(id_orden)

    # actualiza el campo tecnico_id en la orden
    ordenes[id_orden]["tecnico_id"] = id_tecnico_nuevo

    guardar_tecnicos(tecnicos)  # guarda los cambios en el archivo

    nombre_nuevo = tecnicos[id_tecnico_nuevo]["nombre"]  # nombre del tecnico nuevo para el mensaje
    print("Orden", id_orden, "reasignada de", nombre_anterior, "a", nombre_nuevo)
    
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

# ================================================================
# MODULO 3 - CONTROL DE PAGOS Y DEUDAS
# Funciones:
#   cargar_pagos()                - lee el archivo JSON de pagos
#   guardar_pagos()               - guarda los pagos en el archivo JSON
#   registrar_pago()              - registra o agrega un pago a una orden
#   ver_deudores()                - lista clientes con saldo pendiente
#   ver_historial_pagos_cliente() - muestra pagos de un cliente
#   alerta_deuda()                - avisa si el cliente tiene deuda
# ================================================================

# Lee el archivo JSON y devuelve el diccionario de pagos
# Si no existe o esta corrupto, devuelve diccionario vacio
def cargar_pagos():
    try:
        archivo = open(ARCHIVO_PAGOS, "r", encoding="UTF-8")   # abrimos el archivo en modo lectura
        contenido = archivo.read()  # leemos todo el texto del archivo
        archivo.close() # cerramos el archivo
        pagos = json.loads(contenido)  # convertimos el texto JSON a diccionario
        return pagos # devolvemos el diccionario de pagos
    except FileNotFoundError:
        return {} # si no existe el archivo devolvemos vacio
    except json.JSONDecodeError:
        print("Error: el archivo de pagos esta corrupto.")  # avisamos que el archivo esta corrupto
        return {} # devolvemos vacio para poder seguir


# Guarda el diccionario de pagos en el archivo JSON
def guardar_pagos(pagos):
    try:
        archivo = open(ARCHIVO_PAGOS, "w", encoding="UTF-8")  # abrimos en modo escritura
        contenido = json.dumps(pagos, indent=4, ensure_ascii=False)  # convertimos a texto JSON prolijo
        archivo.write(contenido)  # escribimos el contenido en el archivo
        archivo.close()  # cerramos el archivo
    except OSError:
        print("Error: no se pudieron guardar los pagos.")  # avisamos si no se pudo escribir


# Registra un pago nuevo o agrega un pago parcial a una orden existente
# Si la orden no tiene pago registrado crea la deuda, si ya tiene agrega una transaccion
def registrar_pago(pagos, ordenes, clientes):
    id_orden = input("Ingresa el ID de la orden (ej: ORD-1): ").strip()     # pedimos el ID de la orden

    if id_orden not in ordenes:  # verificamos que la orden exista
        print("No se encontro una orden con ese ID.")  # avisamos si no existe
        return  # salimos de la funcion

    orden = ordenes[id_orden] # obtenemos los datos de la orden

    if orden["estado"] == "pendiente" or orden["estado"] == "en_proceso":   # si la orden no esta terminada
        print("La orden todavia no esta completada. No se puede registrar pago aun.")  # avisamos
        return  # salimos de la funcion

    if id_orden in pagos: # si ya tiene pago registrado
        pago = pagos[id_orden]  # obtenemos el pago existente

        if pago["saldo"] <= 0:  # si ya esta todo pagado
            print("Esta orden ya esta totalmente pagada.") # avisamos
            return  # salimos de la funcion

        print("Saldo pendiente: $", pago["saldo"]) # mostramos cuanto falta pagar

        monto_input = input("Cuanto paga ahora ($): ").strip() # pedimos el monto del pago

        try:
            monto = float(monto_input) # convertimos el texto a decimal
        except ValueError:
            print("Monto invalido. Debe ser un numero.")  # avisamos si no es numero
            return   # salimos de la funcion

        if monto <= 0: # si el monto no es positivo
            print("El monto debe ser mayor a cero.") # avisamos
            return  # salimos de la funcion

        if monto > pago["saldo"]: # si paga mas de lo que debe
            print("El monto supera el saldo pendiente: $", pago["saldo"])   # avisamos
            return # salimos de la funcion

        print("Metodo de pago:") # mostramos las opciones
        print("  1. Efectivo") # opcion efectivo
        print("  2. Transferencia") # opcion transferencia
        opcion = input("Elegis una opcion (1/2): ").strip() # pedimos la opcion

        if opcion == "1": # si eligio efectivo
            metodo = "efectivo"  # guardamos el metodo
        elif opcion == "2": # si eligio transferencia
            metodo = "transferencia"  # guardamos el metodo
        else:
            metodo = "efectivo" # si no es valido usamos efectivo
            print("Opcion invalida. Se registra como efectivo.") # avisamos

        fecha_hoy = str(date.today()) # obtenemos la fecha de hoy como texto

        transaccion = {  # creamos el diccionario de la transaccion
            "monto": monto, # cuanto pago
            "metodo": metodo, # como pago
            "fecha": fecha_hoy # cuando pago
        }

        pagos[id_orden]["transacciones"].append(transaccion) # agregamos la transaccion a la lista
        pagos[id_orden]["saldo"] = pago["saldo"] - monto # actualizamos el saldo restante

        if pagos[id_orden]["saldo"] == 0: # si el saldo llego a cero
            ordenes[id_orden]["estado"] = "cobrada" # cambiamos el estado de la orden
            print("Pago total. La orden pasa a estado COBRADA.") # informamos al usuario
        else:
            print("Pago parcial registrado. Saldo restante: $", pagos[id_orden]["saldo"])  # mostramos saldo restante

        guardar_pagos(pagos)   # guardamos los cambios en el archivo
        return  # salimos de la funcion

    # si llegamos aca la orden no tiene pago registrado todavia, creamos la deuda
    monto_input = input("Monto total del trabajo ($): ").strip()  # pedimos el monto total de la deuda

    try:
        monto_total = float(monto_input)  # convertimos el texto a decimal
    except ValueError:
        print("Monto invalido. Debe ser un numero.") # avisamos si no es numero
        return  # salimos de la funcion

    if monto_total <= 0: # si el monto no es positivo
        print("El monto debe ser mayor a cero.") # avisamos
        return # salimos de la funcion

    pago_inmediato = input("El cliente pago algo ahora? (s/n): ").strip().lower()  # preguntamos si pago algo ya

    transacciones = [] # lista vacia de transacciones
    saldo = monto_total  # el saldo arranca igual al total

    if pago_inmediato == "s":   # si pago algo ahora
        monto_ahora_input = input("Cuanto pago ahora ($): ").strip() # pedimos cuanto pago

        try:
            monto_ahora = float(monto_ahora_input)  # convertimos a decimal
        except ValueError:
            print("Monto invalido. Se registra la deuda sin pago inicial.")  # avisamos
            monto_ahora = 0 # dejamos el pago inicial en cero

        if monto_ahora > 0 and monto_ahora <= monto_total:# si el monto es valido
            print("Metodo de pago:") # mostramos las opciones
            print("  1. Efectivo") # opcion efectivo
            print("  2. Transferencia") # opcion transferencia
            opcion = input("Elegis una opcion (1/2): ").strip() # pedimos la opcion

            if opcion == "1": # si eligio efectivo
                metodo = "efectivo"  # guardamos el metodo
            elif opcion == "2": # si eligio transferencia
                metodo = "transferencia"  # guardamos el metodo
            else:
                metodo = "efectivo" # si no es valido usamos efectivo
                print("Opcion invalida. Se registra como efectivo.")  # avisamos

            fecha_hoy = str(date.today()) # obtenemos la fecha de hoy

            transaccion = {   # creamos el diccionario de la transaccion
                "monto": monto_ahora,  # cuanto pago
                "metodo": metodo,  # como pago
                "fecha": fecha_hoy  # cuando pago
            }
            transacciones.append(transaccion)  # agregamos la transaccion a la lista
            saldo = monto_total - monto_ahora # recalculamos el saldo restante

    pagos[id_orden] = {  # creamos el registro de pago nuevo
        "id_orden": id_orden, # vinculo con la orden
        "telefono_cliente": orden["telefono_cliente"],# telefono para identificar al cliente
        "monto_total": monto_total, # deuda original completa
        "saldo": saldo, # lo que falta pagar
        "transacciones": transacciones # lista de pagos recibidos hasta ahora
    }

    if saldo == 0: # si quedo todo pagado
        ordenes[id_orden]["estado"] = "cobrada" # cambiamos el estado de la orden
        print("Pago total registrado. La orden pasa a estado COBRADA.")      # informamos al usuario
    else:
        print("Deuda registrada. Saldo pendiente: $", saldo) # mostramos el saldo que queda

    guardar_pagos(pagos) # guardamos los cambios en el archivo


# Lista todos los clientes que tienen saldo pendiente mayor a cero
def ver_deudores(pagos, clientes):
    telefonos_vistos = set()  # conjunto para no repetir clientes
    hay_deudores = False  # bandera para saber si hay deudores

    print("==================================================")
    print("CLIENTES CON DEUDA PENDIENTE")
    print("==================================================")

    for id_orden in pagos: # recorremos todos los pagos registrados
        pago = pagos[id_orden]  # obtenemos el pago actual

        if pago["saldo"] <= 0: # si no tiene saldo pendiente
            continue  # pasamos al siguiente sin mostrar

        telefono = pago["telefono_cliente"] # obtenemos el telefono del cliente

        if telefono in clientes: # si el cliente existe en el sistema
            nombre = clientes[telefono]["nombre"] # obtenemos el nombre
            tipo = clientes[telefono]["tipo"] # obtenemos el tipo de cliente
        else:
            nombre = "Cliente desconocido" # nombre generico si no existe
            tipo = "-"  # tipo desconocido

        if tipo == "nuevo" or tipo == "problematico": # si es cliente de riesgo
            print("  ALERTA - Cliente", tipo.upper(), "con deuda:") # mostramos alerta especial

        print("  Orden:", id_orden, "| Cliente:", nombre, "(", telefono, ")")  # mostramos la orden y el cliente
        print("  Saldo pendiente: $", pago["saldo"]) # mostramos cuanto debe
        print() # linea en blanco entre registros

        telefonos_vistos.add(telefono)# agregamos el telefono al conjunto
        hay_deudores = True  # marcamos que hay al menos un deudor

    if not hay_deudores: # si no encontramos ninguno
        print("  No hay clientes con deuda pendiente.")# avisamos

    print("Total de clientes con deuda:", len(telefonos_vistos)) # mostramos el total sin repetidos


# Muestra el historial completo de pagos de un cliente buscado por telefono
def ver_historial_pagos_cliente(pagos, clientes):
    telefono = input("Ingresa el telefono del cliente: ").strip() # pedimos el telefono

    if telefono not in clientes:  # si no existe en el sistema
        print("No se encontro un cliente con ese telefono.") # avisamos
        return   # salimos de la funcion

    nombre = clientes[telefono]["nombre"] # obtenemos el nombre del cliente

    print("==================================================")
    print("HISTORIAL DE PAGOS —", nombre)
    print("==================================================")

    hay_pagos = False  # bandera para saber si hay pagos

    for id_orden in pagos: # recorremos todos los pagos
        pago = pagos[id_orden] # obtenemos el pago actual

        if pago["telefono_cliente"] != telefono:   # si no es de este cliente
            continue  # pasamos al siguiente

        hay_pagos = True  # encontramos al menos un pago

        print("  Orden:", id_orden) # mostramos el ID de la orden
        print("  Monto total: $", pago["monto_total"]) # mostramos la deuda original
        print("  Saldo restante: $", pago["saldo"])  # mostramos lo que falta pagar

        if len(pago["transacciones"]) == 0: # si no hay transacciones todavia
            print("  Sin pagos recibidos todavia.") # avisamos
        else:
            print("  Pagos recibidos:")  # titulo de la lista de pagos
            for transaccion in pago["transacciones"]:  # recorremos cada pago recibido
                print("    [", transaccion["fecha"], "] $", transaccion["monto"], "-", transaccion["metodo"])  # mostramos el detalle

        print()  # linea en blanco entre ordenes

    if not hay_pagos:   # si no encontramos ninguno
        print("  Este cliente no tiene pagos registrados.") # avisamos


# Verifica si un cliente tiene deuda y muestra una alerta
# La llama el modulo 1 antes de crear una orden nueva
def alerta_deuda(telefono, pagos, clientes):
    deuda_total = 0  # acumulador de la deuda total

    for id_orden in pagos: # recorremos todos los pagos
        pago = pagos[id_orden] # obtenemos el pago actual
        if pago["telefono_cliente"] == telefono: # si es de este cliente
            deuda_total = deuda_total + pago["saldo"]  # sumamos el saldo pendiente

    if deuda_total > 0:  # si tiene deuda
        tipo = clientes[telefono]["tipo"] # obtenemos el tipo de cliente
        print("AVISO: este cliente tiene deuda pendiente de $", deuda_total) # mostramos el aviso

        if tipo == "nuevo" or tipo == "problematico": # si es cliente de riesgo
            print("ATENCION: el cliente es", tipo.upper(), "y tiene deuda. Se recomienda no continuar.")  # alerta fuerte


# ================================================================
# MODULO 4 - BUSQUEDA E HISTORIAL DE CLIENTES
# Variables: clientes, ordenes, pagos, tecnicos
# Funciones:
#   buscar_cliente()        - busca por nombre o telefono y muestra info basica
#   ver_historial_cliente() - busca y muestra el historial completo de ordenes
# ================================================================

# Busca un cliente por texto libre en nombre o telefono usando expresiones regulares
# Muestra info basica: tipo, deuda y cantidad de ordenes registradas
def buscar_cliente(clientes, pagos):
    texto = input("Ingresa nombre o telefono para buscar: ").strip() # texto libre del usuario

    if texto == "": # si no escribio nada
        print("No ingresaste texto para buscar.") # avisamos
        return # salimos

    try:
        patron = re.compile(texto, re.IGNORECASE) # compilamos el patron ignorando mayusculas
    except re.error:
        print("Texto de busqueda invalido.") # avisamos si el texto tiene caracteres invalidos
        return # salimos

    resultados = [] # lista de telefonos que coinciden con la busqueda

    for telefono in clientes: # recorremos todos los clientes
        nombre = clientes[telefono]["nombre"] # nombre del cliente actual
        if re.search(patron, telefono) or re.search(patron, nombre): # buscamos en telefono y nombre
            resultados.append(telefono) # guardamos si hay coincidencia

    if len(resultados) == 0: # si no encontramos nada
        print("No se encontro ningun cliente con ese texto.") # avisamos
        return # salimos

    if len(resultados) == 1: # si encontramos uno solo
        telefono = resultados[0] # lo tomamos directamente
    else:
        print("Se encontraron", len(resultados), "clientes:") # informamos cuantos hay
        contador = 1 # indice para que el usuario elija
        for tel in resultados: # mostramos cada resultado
            nombre = clientes[tel]["nombre"] # nombre del cliente
            tipo = clientes[tel]["tipo"] # tipo del cliente
            print(" ", contador, ".", nombre, "(", tel, ") -", tipo) # mostramos la opcion
            contador = contador + 1 # avanzamos el contador

        opcion_input = input("Elegis un numero (o Enter para cancelar): ").strip() # pedimos eleccion

        if opcion_input == "": # si cancelo
            return # salimos sin mostrar nada

        try:
            opcion = int(opcion_input) # convertimos a entero
        except ValueError:
            print("Opcion invalida.") # avisamos si no es numero
            return # salimos

        if opcion < 1 or opcion > len(resultados): # si esta fuera de rango
            print("Numero fuera de rango.") # avisamos
            return # salimos

        telefono = resultados[opcion - 1] # tomamos el elegido (ajustamos indice base 0)

    cliente = clientes[telefono] # referencia al cliente encontrado

    deuda_total = 0 # acumulador de deuda pendiente
    for id_orden in pagos: # recorremos todos los pagos
        if pagos[id_orden]["telefono_cliente"] == telefono: # si es de este cliente
            deuda_total = deuda_total + pagos[id_orden]["saldo"] # sumamos el saldo pendiente

    print("==================================================")
    print("CLIENTE:", cliente["nombre"])
    print("Telefono:", telefono, "| Tipo:", cliente["tipo"].upper())
    if cliente["dni"] != "": # si tiene DNI cargado
        print("DNI:", cliente["dni"]) # lo mostramos
    print("Direccion:", cliente["direccion"]) # mostramos la direccion
    if deuda_total > 0: # si tiene deuda
        print("DEUDA PENDIENTE: $", deuda_total) # mostramos la deuda con alerta
    else:
        print("Sin deuda pendiente.") # confirmamos que esta al dia
    print("Ordenes registradas:", len(cliente["ordenes"])) # cantidad total de ordenes
    print("==================================================")


# Busca un cliente y muestra el historial completo de sus ordenes en orden cronologico
# Incluye estado, tecnico asignado y datos de pago de cada orden
def ver_historial_cliente(clientes, ordenes, pagos, tecnicos):
    texto = input("Ingresa nombre o telefono para buscar: ").strip() # texto libre del usuario

    if texto == "": # si no escribio nada
        print("No ingresaste texto para buscar.") # avisamos
        return # salimos

    try:
        patron = re.compile(texto, re.IGNORECASE) # compilamos el patron ignorando mayusculas
    except re.error:
        print("Texto de busqueda invalido.") # avisamos si el texto tiene caracteres invalidos
        return # salimos

    resultados = [] # lista de telefonos que coinciden con la busqueda

    for telefono in clientes: # recorremos todos los clientes
        nombre = clientes[telefono]["nombre"] # nombre del cliente actual
        if re.search(patron, telefono) or re.search(patron, nombre): # buscamos en telefono y nombre
            resultados.append(telefono) # guardamos si hay coincidencia

    if len(resultados) == 0: # si no encontramos nada
        print("No se encontro ningun cliente con ese texto.") # avisamos
        return # salimos

    if len(resultados) == 1: # si encontramos uno solo
        telefono = resultados[0] # lo tomamos directamente
    else:
        print("Se encontraron", len(resultados), "clientes:") # informamos cuantos hay
        contador = 1 # indice para que el usuario elija
        for tel in resultados: # mostramos cada resultado
            nombre = clientes[tel]["nombre"] # nombre del cliente
            tipo = clientes[tel]["tipo"] # tipo del cliente
            print(" ", contador, ".", nombre, "(", tel, ") -", tipo) # mostramos la opcion
            contador = contador + 1 # avanzamos el contador

        opcion_input = input("Elegis un numero (o Enter para cancelar): ").strip() # pedimos eleccion

        if opcion_input == "": # si cancelo
            return # salimos sin mostrar nada

        try:
            opcion = int(opcion_input) # convertimos a entero
        except ValueError:
            print("Opcion invalida.") # avisamos si no es numero
            return # salimos

        if opcion < 1 or opcion > len(resultados): # si esta fuera de rango
            print("Numero fuera de rango.") # avisamos
            return # salimos

        telefono = resultados[opcion - 1] # tomamos el elegido (ajustamos indice base 0)

    cliente = clientes[telefono] # referencia al cliente encontrado
    ids_ordenes = cliente["ordenes"] # lista de IDs de ordenes del cliente

    deuda_total = 0 # acumulador de deuda
    for id_orden in pagos: # recorremos todos los pagos
        if pagos[id_orden]["telefono_cliente"] == telefono: # si es de este cliente
            deuda_total = deuda_total + pagos[id_orden]["saldo"] # sumamos el saldo

    print("==================================================")
    print("HISTORIAL:", cliente["nombre"])
    print("Telefono:", telefono, "| Tipo:", cliente["tipo"].upper())
    if deuda_total > 0: # si tiene deuda
        print("DEUDA PENDIENTE: $", deuda_total) # mostramos con alerta
    else:
        print("Sin deuda pendiente.") # confirmamos al dia
    print("==================================================")

    if len(ids_ordenes) == 0: # si no tiene ordenes
        print("Este cliente no tiene ordenes registradas.") # avisamos
        return # salimos

    ids_validos = [] # lista de IDs que todavia existen en ordenes
    for id_ord in ids_ordenes: # recorremos los IDs del cliente
        if id_ord in ordenes: # si la orden todavia existe en el sistema
            ids_validos.append(id_ord) # la agregamos

    # construimos pares [fecha, id] para poder ordenar sin sorted() con clave
    pares = [] # lista de pares [fecha_creacion, id_orden]
    for id_ord in ids_validos: # recorremos los IDs validos
        fecha = ordenes[id_ord]["fecha_creacion"] # obtenemos la fecha de la orden
        pares.append([fecha, id_ord]) # agregamos el par

    # burbujeo descendente: la orden mas reciente queda primero
    n = len(pares) # cantidad de ordenes
    for i in range(n): # pasadas del burbujeo
        for j in range(0, n - i - 1): # comparamos pares adyacentes
            if pares[j][0] < pares[j + 1][0]: # si el izquierdo es mas viejo
                temp = pares[j] # guardamos temporalmente
                pares[j] = pares[j + 1] # movemos el mas nuevo a la izquierda
                pares[j + 1] = temp # movemos el mas viejo a la derecha

    print("Ordenes (mas reciente primero):")
    print()

    for par in pares: # recorremos los pares ya ordenados
        id_ord = par[1] # obtenemos el ID de la orden
        orden = ordenes[id_ord] # referencia a la orden

        print("  Orden:", id_ord, "| Estado:", orden["estado"].upper()) # ID y estado
        print("  Fecha:", orden["fecha_creacion"]) # fecha de creacion
        print("  Descripcion:", orden["descripcion"]) # descripcion del trabajo

        if orden["tecnico_id"] is not None: # si tiene tecnico asignado
            id_tec = orden["tecnico_id"] # ID del tecnico
            if id_tec in tecnicos: # si el tecnico existe en el sistema
                nombre_tec = tecnicos[id_tec]["nombre"] # nombre del tecnico
            else:
                nombre_tec = "Tecnico desconocido" # nombre generico si fue borrado
            print("  Tecnico:", nombre_tec) # mostramos el tecnico
        else:
            print("  Tecnico: sin asignar") # si no tiene tecnico asignado

        if id_ord in pagos: # si tiene pago registrado
            pago = pagos[id_ord] # referencia al pago
            print("  Monto total: $", pago["monto_total"], "| Saldo pendiente: $", pago["saldo"]) # datos de pago

        print() # linea en blanco entre ordenes


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
    pagos = cargar_pagos() # carga pagos desde archivo al iniciar
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
            ultimo_id_orden = crear_orden(clientes, ordenes, ultimo_id_orden, pagos)
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
            registrar_pago(pagos, ordenes, clientes)
        elif opcion == "8":  # ver clientes con deuda pendiente
            ver_deudores(pagos, clientes)
        elif opcion == "9":  # buscar un cliente
            buscar_cliente(clientes, pagos)
        elif opcion == "10":   # ver historial de un cliente
            ver_historial_cliente(clientes, ordenes, pagos, tecnicos)
        elif opcion == "11":  # generar un presupuesto
            generar_presupuesto()
        elif opcion == "12": # ver presupuestos existentes
            ver_presupuestos()
        elif opcion == "0":  # salir del sistema
            print("Saliendo del sistema...")
        else:
            print("Opción inválida. Intente nuevamente.") # opcion no reconocida

menu()  # punto de entrada del programa


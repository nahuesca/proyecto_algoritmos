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


# ============================================================
# MÓDULO 1 - ÓRDENES DE SERVICIO
# ============================================================

# Pide los datos de una nueva orden, registra al cliente si no existe,
# genera un id nuevo y guarda la orden con estado "pendiente".
def crear_orden(ordenes, clientes, ultimo_id_orden):
    print("\n--- Nueva orden de servicio ---")

    telefono = input("Telefono del cliente: ")  # identificador principal del cliente
    nombre = input("Nombre del cliente: ")  # nombre para mostrar en pantallas/historial
    direccion = input("Direccion: ")  # donde se realiza el trabajo
    tipo_trabajo = input("Tipo de trabajo (ej: instalacion, reparacion): ")  # descripcion corta del servicio
    descripcion = input("Descripcion del problema: ")  # detalle que aporta el cliente

    if telefono not in clientes:  # si el telefono no esta registrado
        clientes[telefono] = {"nombre": nombre, "ordenes": []}  # creamos al cliente nuevo

    nuevo_id = ultimo_id_orden + 1  # calculamos el proximo id

    ordenes[nuevo_id] = {  # creamos la orden con sus datos
        "telefono_cliente": telefono,  # vinculo con el cliente
        "direccion": direccion,  # direccion del trabajo
        "tipo_trabajo": tipo_trabajo,  # tipo de servicio
        "descripcion": descripcion,  # detalle del problema
        "estado": "pendiente",  # toda orden nueva arranca pendiente
        "tecnico_asignado": None,  # todavia no tiene tecnico
    }

    clientes[telefono]["ordenes"].append(nuevo_id)  # asociamos la orden al cliente

    print(f"Orden creada con exito. Numero de orden: {nuevo_id}")  # confirmacion al usuario

    return ordenes, clientes, nuevo_id  # devolvemos las estructuras y el nuevo id
 
# Busca una orden por id, valida que exista, y actualiza su estado al nuevo valor ingresado.
def cambiar_estado_orden(ordenes):
    print("\n--- Cambiar estado de orden ---")
    estados_validos = ["pendiente", "en_proceso", "completada", "cobrada"]  # estados posibles del sistema

    try:
        id_orden = int(input("Ingrese el numero de orden: "))  # intentamos convertir a entero
    except ValueError:  # si el usuario ingreso texto u otro valor invalido
        print("El numero de orden debe ser un valor numerico.")
        return ordenes  # devolvemos sin cambios

    if id_orden not in ordenes:  # verificamos que la orden exista
        print(f"No se encontro una orden con el numero {id_orden}.")
        return ordenes  # devolvemos sin cambios

    print(f"Orden encontrada. Estado actual: {ordenes[id_orden]['estado']}")  # mostramos el estado actual

    print("Estados disponibles: pendiente, en_proceso, completada, cobrada")
    nuevo_estado = input("Ingrese el nuevo estado: ")  # pedimos el nuevo estado

    if nuevo_estado not in estados_validos:  # verificamos que el estado sea valido
        print("Estado invalido. Debe ser: pendiente, en_proceso, completada o cobrada.")
        return ordenes  # devolvemos sin cambios

    ordenes[id_orden]["estado"] = nuevo_estado  # actualizamos el estado de la orden

    print(f"Estado actualizado correctamente a: {nuevo_estado}")  # confirmacion al usuario

    return ordenes  # devolvemos el diccionario actualizado
 
# Filtra y muestra todas las ordenes con estado pendiente o en proceso.
def mostrar_ordenes_pendientes(ordenes, clientes):
    print("\n--- Ordenes pendientes y en proceso ---")

    hay_ordenes = False  # bandera para saber si encontramos al menos una orden

    for id_orden, orden in ordenes.items():  # recorremos todas las ordenes
        if orden["estado"] in ["pendiente", "en_proceso"]:  # filtramos por estado
            hay_ordenes = True  # se encontro al menos una orden
            nombre_cliente = clientes[orden["telefono_cliente"]]["nombre"]  # obtenemos el nombre del cliente
            print(f"Orden #{id_orden} | Cliente: {nombre_cliente} | Estado: {orden['estado']} | Trabajo: {orden['tipo_trabajo']}")  # mostramos la orden

    if not hay_ordenes:  # si no encontramos ninguna
        print("No hay ordenes pendientes ni en proceso.")  # avisamos al usuario

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
            ordenes, clientes, ultimo_id_orden = crear_orden(ordenes, clientes, ultimo_id_orden)  # actualizamos las tres estructuras
        elif opcion == "2":
            ordenes = cambiar_estado_orden(ordenes)  # actualizamos ordenes con el estado nuevo
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

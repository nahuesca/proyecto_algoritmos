# PROYECTO ESTRUCTURA DE DATOS 1

# Etapa 2 - Análisis y Diseño
1) DESCRIPCIÓN DEL NEGOCIO
Instalación, reparación y mantenimiento de equipos de climatización y electricidad general. 4 personas: el dueño en oficina y 3 técnicos en campo.
Cómo trabaja hoy:
Pedidos anotados en cuaderno, datos de clientes en Excel básico
Coordinación con técnicos por WhatsApp
Pagos y deudas guardados en la cabeza o en notas sueltas
Sin sistema centralizado: información dispersa entre cuadernos, WhatsApp, Excel y memoria
Problemas principales:
No sabe en qué estado está cada trabajo en tiempo real
No sabe si un trabajo ya se cobró
Pierde tiempo buscando datos viejos de clientes
Información se pierde: hojas sueltas, chats, memoria
Tareas repetidas: anotar pedido, pasarlo por WhatsApp, facturar
Presupuestos y cálculos de mano de obra manuales
2) MÓDULOS IDENTIFICADOS
Módulo 1 – Registro y Gestión de Órdenes de Servicio
Centraliza cada trabajo: cliente, problema, técnico asignado, estado, presupuesto, repuestos y estado de cobro.
Funcionalidades:
Crear orden con: nombre, teléfono, dirección, descripción del problema y técnico asignado
Cambiar estado: Pendiente → En Proceso → Completada → Cobrada
Ver órdenes abiertas y buscar por cliente, teléfono o ID
Registrar repuestos utilizados y costos
Vincular orden con pago (cobrada / pendiente de cobro)
Historial de cambios de estado con fecha y hora
Justificación: El dueño definió como lo más urgente "saber en qué estado está cada laburo": si está pendiente, si el técnico ya fue, o si terminó y hay que cobrarlo. Hoy busca esa información revolviendo cuadernos o scrolleando kilométricos chats de WhatsApp.
Supuestos:
Cada orden tiene ID único autogenerado
DNI del cliente no es obligatorio (nunca fue mencionado)
Una orden puede tener múltiples repuestos
El dueño gestiona los estados manualmente; los técnicos no acceden al sistema
Módulo 2 – Gestión de Técnicos y Asignación de Trabajos
Registra los técnicos disponibles, muestra qué tiene asignado cada uno y permite reasignar ante urgencias.
Funcionalidades:
Registrar técnicos (nombre y teléfono)
Asignar o reasignar una orden a un técnico
Ver órdenes por técnico (pendientes y en proceso)
Ver estado de cada técnico: disponible u ocupado
Ver histórico de trabajos por técnico
Justificación: El dueño organiza el día "a los ponchazos" y cuando entra una urgencia necesita saber de inmediato quién está libre. Hoy lo averigua llamando o esperando que el técnico avise. A veces el técnico termina sin avisar y él no sabe si puede llamar al cliente a cobrarle.
Supuestos:
Los técnicos tienen horarios flexibles
La priorización la decide el dueño, no el sistema
Los técnicos NO acceden al sistema; reciben la info por WhatsApp o llamada
El estado disponible/ocupado lo actualiza el dueño manualmente
Módulo 3 – Control de Pagos y Deudas
Registra pagos, deudas y tipo de cliente. Vincula cada cobro con su orden correspondiente.
Funcionalidades:
Registrar pago por orden: efectivo, transferencia, a deber o en cuotas
Registrar pagos parciales descontando del total adeudado
Listar clientes con deuda y monto
Clasificar clientes: frecuente (descuento/cuotas), nuevo (pago inmediato), problemático (sin crédito)
Ver historial de pagos por cliente
Alertar cuando un cliente nuevo o problemático tiene deuda vieja
Permitir corregir estado de pago (error, cheque rebotado, etc.)
Justificación: "Si pierdo el dato de una deuda, es plata que regala el negocio." El dueño diferencia entre clientes buenos (les permite deber) y problemáticos (les exige pagar primero). Los pagos parciales son frecuentes y deben descontarse correctamente del total para no generar reclamos erróneos.
Supuestos:
Tres tipos de cliente: frecuente, nuevo y problemático (el dueño asigna el tipo manualmente)
"Cobrado" y "facturado" son estados distintos
Los pagos en cuotas se registran como transacciones separadas pero vinculadas a la misma deuda
El dueño decide caso a caso si atender a un cliente con deuda; el sistema no lo bloquea automáticamente
Módulo 4 – Búsqueda e Historial de Clientes
Acceso rápido al historial completo de un cliente: trabajos, pagos, deudas y tipo.
Funcionalidades:
Buscar por nombre, teléfono o apodo (ej.: "el de la esquina")
Ver todos los trabajos realizados en orden cronológico
Ver deuda pendiente, última intervención y tipo de cliente
Ver detalle de un trabajo viejo (qué se hizo, con quién, cuánto se cobró)
Filtrar solo órdenes pendientes o incompletas
Justificación: Los técnicos llaman desde la calle para preguntar dirección o forma de cobro porque no tienen acceso a la información. El dueño identifica clientes por nombre de pila, empresa o referencias informales, rara vez por apellido. Necesita acceder a todo en pocos pasos: "si tengo que hacer veinte clics, no lo voy a usar."
Supuestos:
La búsqueda por teléfono es prioritaria
Se admiten referencias informales como criterio de búsqueda
Historial en orden cronológico descendente
Módulo 5 – Cálculo de Presupuestos y Costos
Asiste en el armado de presupuestos y en el cálculo de lo que corresponde pagarle a cada técnico al cierre del mes.
Funcionalidades:
Lista de repuestos con precios base ajustables por trabajo
Clasificar trabajo como simple o complicado (define el valor de mano de obra)
Calcular presupuesto automáticamente (repuestos + mano de obra) con posibilidad de ajuste manual
Registrar presupuestos rechazados
Calcular lo que corresponde pagarle a cada técnico al cierre del mes
Justificación: El dueño calcula presupuestos "a ojo" y estima la mano de obra según si el trabajo es simple o complicado. Hoy los presupuestos rechazados se olvidan o quedan perdidos en notas. El cálculo de pago a técnicos también es manual y propenso a error.
Supuestos:
Solo dos categorías de mano de obra: simple y complicada
Los técnicos cobran por comisión o porcentaje, no por hora fija
En trabajos simples el presupuesto se hace antes de ir; en complicados se ajusta en el lugar
El cálculo de fin de mes es orientativo; el dueño lo verifica igualmente
4. Relaciones entre Módulos
Cada orden de servicio se conecta con el técnico asignado (M2), su estado de pago (M3) y el historial del cliente (M4). Un pago siempre queda vinculado a una orden específica, o a la deuda vieja si es un pago parcial. El dueño cierra el ciclo: marca la orden como completada cuando el técnico termina, y como cobrada cuando recibe el pago.
5. Flujo de un Trabajo Típico
Cliente llama → Dueño registra orden → Estado: PENDIENTE
Técnico llega al trabajo → Estado: EN PROCESO
Técnico termina y avisa → Estado: COMPLETADA
Se cobra → Dueño registra pago → Estado: COBRADA → Orden archivada
Si hay deuda anterior: el sistema informa al dueño, quien decide si hace el trabajo igual o exige pago previo. Si el cliente paga algo a cuenta, se registra como pago parcial vinculado a esa deuda.
6. Supuestos y Limitaciones
Supuestos generales:
Sin autenticación/login: lo usa solo el dueño desde una PC
Sin integración con AFIP ni sistemas impositivos
Sin notificaciones automáticas a técnicos (coordinación sigue por WhatsApp)
Sin acceso de clientes ni técnicos al sistema
Limitaciones conocidas:
Pagos se registran manualmente (sin integración bancaria)
Sin reportes de ganancias/pérdidas automáticos
Sin alertas automáticas de deuda: el dueño las ve cuando busca al cliente
El sistema no bloquea trabajar con clientes deudores; el dueño decide
7. MVP – Mínimo Viable
Obligatorio:
Registro y gestión de órdenes de servicio
Control de pagos y deudas
Búsqueda rápida por teléfono o nombre
Puede esperar: 4. Gestión de técnicos y asignación 5. Cálculo de presupuestos
Con los tres primeros, el dueño cubre lo esencial: saber qué trabajos hay, en qué estado están y si ya se cobraron.

# ETAPA 3 – DESARROLLO 
Análisis técnico de cada módulo 
Estructuras de datos globales
Antes de los módulos, defininimos qué "tablas" van a estar en memoria:
clientes — diccionario donde la clave es el teléfono (es lo que el dueño siempre tiene a mano). Cada cliente tiene: nombre, teléfono, dirección, tipo (frecuente / nuevo / problematico), y lista de IDs de órdenes asociadas.
tecnicos — diccionario con ID de técnico. Cada uno tiene: nombre, teléfono, y lista de IDs de órdenes asignadas.
ordenes — diccionario con ID único autoincremental. Cada orden tiene: ID, teléfono del cliente, ID del técnico, descripción del problema, estado (pendiente / en_proceso / completada / cobrada), fecha de creación, fecha de visita, lista de repuestos (nombre + costo), monto total, y referencia al pago.
pagos — diccionario con ID de pago. Cada pago tiene: ID de orden asociada, monto total de la deuda, lista de transacciones (monto + método + fecha), y saldo restante.
presupuestos — diccionario con ID de presupuesto. Cada uno tiene: ID de orden, lista de repuestos con precio, tipo de trabajo (simple / complicado), costo de mano de obra, total calculado, total ajustado (si el dueño lo modificó), y estado (aprobado / rechazado / pendiente).

Módulo 1 — Órdenes de Servicio
Variables clave: 
ordenes, clientes, contador ultimo_id_orden.
Qué hace: 
Es el centro de todo. Registra cada trabajo desde que entra el llamado hasta que se completa y se cobra.
Cómo funciona: 
La función crear_orden pide los datos del cliente y del trabajo, da de alta al cliente en clientes si no existe, genera un ID automático y guarda la orden en ordenes con estado pendiente. 
La función cambiar_estado_orden busca una orden por su ID y avanza su estado (pendiente → en_proceso → completada → cobrada). 
La función mostrar_ordenes_pendientes filtra ordenes y muestra solo las que están pendientes o en proceso, para ver de un vistazo qué falta hacer.

Módulo 2 — Gestión de Técnicos
Variables clave: 
tecnicos, ordenes.
Qué hace: 
Mantiene el registro de los técnicos y permite ver quién está disponible y asignarlo a un trabajo.
Cómo funciona: 
La función registrar_tecnico agrega un técnico nuevo a tecnicos con su nombre y especialidad. 
La función mostrar_tecnicos lista los técnicos junto con su disponibilidad. 
La función asignar_tecnico_a_orden vincula un técnico a una orden existente, actualizando el campo correspondiente dentro de ordenes.

Módulo 3 — Control de Pagos y Deudas
Variables clave: 
pagos, ordenes, clientes.
Qué hace: 
Registra todo el movimiento de plata: quién pagó, cuánto, y quién todavía debe.
Cómo funciona: 
La función registrar_pago agrega una transacción de pago (monto, método, fecha) vinculada a una orden, y recalcula el saldo pendiente. 
La función ver_estado_pagos filtra pagos y muestra la lista de clientes con saldo mayor a cero, junto con cuánto deben.

Módulo 4 — Búsqueda e Historial de Clientes
Variables clave: 
clientes, ordenes, pagos.
Qué hace: 
Permite encontrar cualquier información sobre un cliente en pocos pasos.
Cómo funciona: 
La función buscar_cliente acepta un texto libre y busca coincidencias en el teléfono o el nombre dentro de clientes. 
La función ver_historial_cliente arma una vista consolidada del cliente seleccionado, mostrando sus órdenes (con estado) y su deuda total pendiente.

Módulo 5 — Presupuestos y Costos
Variables clave: 
presupuestos, ordenes.
Qué hace: 
Calcula cuánto cobrarle al cliente según los repuestos y la mano de obra.
Cómo funciona: 
La función generar_presupuesto pide la lista de repuestos con sus precios, suma el costo de mano de obra según el tipo de trabajo, calcula el total y lo guarda en presupuestos vinculados a una orden. 
La función ver_presupuestos lista los presupuestos generados con su estado (aprobado, rechazado, pendiente).

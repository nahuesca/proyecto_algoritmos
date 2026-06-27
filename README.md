# SISTEMA DE GESTIÓN DE SERVICIOS TÉCNICOS
## PyME Aire Acondicionado y Electricidad

Sistema de gestión integral para una pequeña empresa de servicios técnicos. Permite organizar órdenes de servicio, gestionar técnicos, controlar pagos y generar presupuestos.

---

## Tabla de Contenidos

1. [Descripción del Negocio](#descripción-del-negocio)
2. [Cómo Ejecutar](#cómo-ejecutar)
3. [Módulos del Sistema](#módulos-del-sistema)
4. [Librerías Utilizadas](#librerías-utilizadas)
5. [Estructuras de Datos](#estructuras-de-datos)
6. [Flujo Típico](#flujo-típico-de-un-trabajo)
7. [Limitaciones Conocidas](#limitaciones-conocidas)
8. [Archivos del Proyecto](#archivos-del-proyecto)

---

## Descripción del Negocio

La PyME está conformada por:
- 1 dueño (en oficina): gestiona órdenes, pagos y coordinación
- 3 técnicos (en campo): ejecutan los trabajos

### Problema que Resuelve
- Antes: Pedidos en cuaderno, datos en Excel, coordinación por WhatsApp
- Ahora: Sistema centralizado con información organizada y en tiempo real

---

## Cómo Ejecutar

### Requisitos
- Python 3.7 o superior
- Sistema operativo: Windows, macOS o Linux

### Pasos para Ejecutar

1. Clonar o descargar el repositorio
```bash
git clone https://github.com/nahuesca/proyecto_algoritmos.git
cd proyecto_algoritmos
```

2. Ejecutar el programa
```bash
python main.py
```

3. Navegar por el menú
- El sistema muestra un menú principal con opciones numeradas
- Ingresa el número de la opción deseada
- Sigue las indicaciones en pantalla

### Ejemplo de Ejecución
```
========== SISTEMA DE GESTIÓN - SERVICIOS TÉCNICOS ==========
=== Órdenes de Servicio ===
1. Crear orden de servicio
2. Cambiar estado de una orden
3. Ver órdenes pendientes
...
0. Salir
==============================================================
Seleccione una opción: 1
```

---

## Módulos del Sistema

### Módulo 1: Órdenes de Servicio
**Funciones principales:** crear_orden, cambiar_estado_orden, mostrar_ordenes_pendientes

**Qué hace:**
- Crear nuevas órdenes de servicio vinculadas a un cliente
- Cambiar el estado de una orden (Pendiente → En Proceso → Completada → Cobrada)
- Listar órdenes pendientes y en proceso
- Validar datos del cliente (teléfono, DNI)
- Clasificar clientes (Frecuente, Nuevo, Problemático)
- Mostrar alertas para clientes problemáticos o con deuda

**Estados de una Orden:**
- pendiente: Orden creada, aguardando asignación
- en_proceso: Técnico asignado, trabajando
- completada: Trabajo terminado, aguardando pago
- cobrada: Orden pagada completamente

**Persistencia:** clientes.json, ordenes.json

---

### Módulo 2: Gestión de Técnicos
**Funciones principales:** registrar_tecnico, mostrar_tecnicos, asignar_tecnico_a_orden, reasignar_tecnico_a_orden, finalizar_trabajo_tecnico

**Qué hace:**
- Registrar técnicos con nombre, especialidad y teléfono (opcional)
- Visualizar estado en tiempo real de todos los técnicos
- Mostrar técnicos disponibles
- Asignar un técnico disponible a una orden
- Reasignar técnicos entre órdenes
- Finalizar trabajo de un técnico (libera disponibilidad)
- Calcular disponibilidad automáticamente basada en órdenes activas

**Cálculo de Disponibilidad:**
- Un técnico está ocupado si tiene al menos una orden en estado "en_proceso"
- Un técnico está disponible si no tiene órdenes activas

**Persistencia:** tecnicos.json

---

### Módulo 3: Control de Pagos y Deudas
**Funciones principales:** registrar_pago, ver_deudores, ver_historial_pagos_cliente, alerta_deuda

**Qué hace:**
- Registrar deudas al completar una orden
- Aceptar pagos parciales o totales
- Registrar método de pago (Efectivo, Transferencia)
- Listar clientes con saldo pendiente
- Ver historial completo de pagos de un cliente
- Mostrar alerta automática si el cliente tiene deuda pendiente
- Cambiar estado de orden a "cobrada" cuando el saldo llega a cero

**Ejemplo de Flujo de Pago:**
1. Orden completada → se crea deuda
2. Cliente paga $50 → se registra transacción parcial
3. Cliente paga $100 → se registra segunda transacción
4. Saldo = $0 → orden pasa a estado "cobrada"

**Persistencia:** pagos.json

---

### Módulo 4: Búsqueda e Historial de Clientes
**Funciones principales:** buscar_cliente, ver_historial_cliente

**Qué hace:**
- Buscar clientes por nombre o teléfono (búsqueda con expresiones regulares)
- Ver información básica del cliente (tipo, deuda, cantidad de órdenes)
- Ver historial completo de órdenes (ordenadas por fecha, más reciente primero)
- Mostrar detalles de cada orden: estado, técnico asignado, descripción, pagos
- Filtrar y seleccionar de múltiples resultados

**Búsqueda Flexible:**
- Soporta búsqueda parcial: "Juan" encuentra "Juan López"
- Busca en teléfono y nombre simultáneamente
- Ignora mayúsculas/minúsculas

---

### Módulo 5: Presupuestos y Costos
**Funciones principales:** generar_presupuesto, ver_presupuestos, calcular_comisiones

**Qué hace:**
- Generar presupuestos para órdenes
- Clasificar trabajos: Simple o Complicado (con costos fijos de mano de obra)
- Cargar repuestos con precios individuales
- Calcular total automáticamente: suma de repuestos + mano de obra
- Permitir ajuste manual del total
- Registrar aprobación/rechazo del presupuesto por cliente
- Calcular comisiones mensuales de técnicos basadas en órdenes cobradas

**Costos Configurables:**
- Mano de obra simple: $5.000
- Mano de obra complicado: $12.000

**Cálculo de Comisiones:**
1. Seleccionar mes (ej: 2025-06)
2. Para cada técnico:
   - Sumar montos de órdenes "cobradas" en ese mes
   - Ingresar porcentaje de comisión
   - Sistema calcula: total × porcentaje / 100

**Persistencia:** presupuestos.json

---

## Librerías Utilizadas

| Librería | Versión | Propósito |
|----------|---------|----------|
| json | Built-in | Lectura/escritura de archivos JSON |
| re | Built-in | Búsqueda flexible de texto con expresiones regulares |
| datetime | Built-in | Manejo de fechas de creación y pago |

Nota: El sistema solo usa librerías estándar de Python, no requiere instalaciones adicionales.

---

## Estructuras de Datos

### Clientes (clientes.json)
```json
{
  "1234567890": {
    "nombre": "Juan López",
    "dni": "12345678",
    "direccion": "Calle Principal 123",
    "tipo": "frecuente",
    "ordenes": ["ORD-1", "ORD-2"]
  }
}
```

### Técnicos (tecnicos.json)
```json
{
  "1": {
    "nombre": "Carlos García",
    "especialidad": "Electricista",
    "telefono": "1234567890",
    "ordenes_asignadas": ["ORD-1"]
  }
}
```

### Órdenes (ordenes.json)
```json
{
  "ORD-1": {
    "id": "ORD-1",
    "telefono_cliente": "1234567890",
    "descripcion": "Reparar aire acondicionado",
    "estado": "en_proceso",
    "fecha_creacion": "2025-06-27",
    "fecha_visita": "2025-06-28",
    "tecnico_id": 1,
    "repuestos": [],
    "monto_total": 0
  }
}
```

### Pagos (pagos.json)
```json
{
  "ORD-1": {
    "id_orden": "ORD-1",
    "telefono_cliente": "1234567890",
    "monto_total": 5000.0,
    "saldo": 2500.0,
    "transacciones": [
      {
        "monto": 2500.0,
        "metodo": "efectivo",
        "fecha": "2025-06-27"
      }
    ]
  }
}
```

### Presupuestos (presupuestos.json)
```json
{
  "ORD-1": {
    "id_orden": "ORD-1",
    "tipo_trabajo": "complicado",
    "mano_de_obra": 12000.0,
    "repuestos": [
      {"nombre": "Filtro", "precio": 500.0},
      {"nombre": "Cable", "precio": 200.0}
    ],
    "total_calculado": 12700.0,
    "total_final": 12700.0,
    "estado": "aprobado"
  }
}
```

---

## Flujo Típico de un Trabajo

```
1. Cliente llama o visita
   |
2. Dueño registra orden (Estado: PENDIENTE)
   - Sistema alerta si el cliente tiene deuda anterior
   |
3. Se asigna técnico disponible (Estado: EN PROCESO)
   - Sistema calcula disponibilidad en tiempo real
   |
4. Técnico finaliza trabajo (Estado: COMPLETADA)
   |
5. Se genera presupuesto (si no se hizo antes)
   - Repuestos + Mano de obra
   - Cliente aprueba o rechaza
   |
6. Se registra el pago
   - Puede ser pago total o parcial
   - Se registra método (efectivo/transferencia)
   |
7. Saldo = $0 → Orden pasa a COBRADA
   |
8. Se calcula comisión del técnico (si aplica)
```

---

## Limitaciones Conocidas

### 1. Validación de Teléfono
- Limitación: Solo valida que tenga entre 8 y 15 dígitos
- No valida formato específico de país
- Solución futura: Integrar librería phonenumbers para validación internacional

### 2. Persistencia en Archivos JSON
- Limitación: Sin encriptación de datos
- No hay respaldo automático
- Sin versionado de cambios
- Solución futura: Migrar a base de datos SQL (SQLite, PostgreSQL)

### 3. Concurrencia
- Limitación: El sistema no es multi-usuario
- Si dos usuarios editan simultáneamente, puede haber pérdida de datos
- Solución futura: Implementar servidor con framework como Flask/Django

### 4. Búsqueda de Clientes
- Limitación: Usa expresiones regulares básicas
- Búsqueda lenta con muchos registros (>10.000)
- Solución futura: Implementar índices o base de datos

### 5. Integridad de Datos
- Limitación: Sin validación cruzada entre archivos
- Si un archivo JSON se corrompe, se inicia vacío sin recuperación
- Solución futura: Agregar backup automático y validación

### 6. Interfaz de Usuario
- Limitación: Solo interfaz de línea de comandos (CLI)
- No hay interfaz gráfica
- Solución futura: Crear interfaz web con Flask/React

### 7. Generación de Reportes
- Limitación: No hay exportación a PDF, Excel
- Sin gráficos de análisis
- Solución futura: Agregar reportes con librería reportlab u openpyxl

### 8. Histórico Completo
- Limitación: No se registra quién hizo cada cambio
- Sin auditoría de operaciones
- Solución futura: Agregar log de operaciones con timestamps y usuario

### 9. Reasignación de Técnicos
- Limitación: Validación limitada en reasignación de órdenes
- Solución futura: Mejorar lógica con más validaciones

### 10. Cálculo de Comisiones
- Limitación: Se calcula manualmente, ingresando porcentaje para cada técnico
- No hay porcentajes configurables por defecto
- Solución futura: Agregar tabla de comisiones por técnico/tipo de trabajo

---

## Archivos del Proyecto

```
proyecto_algoritmos/
|
├── main.py                    Sistema principal - 1000+ líneas
├── validaciones.py            Funciones de validación
├── README.md                  Este archivo (documentación)
|
├── clientes.json              Base de datos de clientes (generado)
├── tecnicos.json              Base de datos de técnicos (generado)
├── ordenes.json               Base de datos de órdenes (generado)
├── pagos.json                 Base de datos de pagos (generado)
└── presupuestos.json          Base de datos de presupuestos (generado)
```

### Descripción de Archivos

| Archivo | Descripción |
|---------|-------------|
| main.py | Contiene toda la lógica del sistema: menú principal, gestión de órdenes, técnicos, pagos, presupuestos |
| validaciones.py | Funciones reutilizables para validar teléfono y DNI |
| clientes.json | Almacena clientes, sus datos y referencias a órdenes |
| tecnicos.json | Almacena técnicos y su historial de órdenes asignadas |
| ordenes.json | Almacena órdenes de servicio y su estado |
| pagos.json | Almacena deudas y transacciones de pago |
| presupuestos.json | Almacena presupuestos y su estado (aprobado/rechazado) |

---

## Características Principales

- Automatización de Disponibilidad: Los técnicos se marcan disponibles/ocupados automáticamente
- Alertas de Deuda: Aviso cuando un cliente crea una nueva orden con saldo pendiente
- Búsqueda Flexible: Encuentra clientes por nombre, teléfono o parcialmente
- Historial Completo: Ver todos los trabajos y pagos de un cliente
- Cálculo Automático: Presupuestos con suma de repuestos + mano de obra
- Pagos Parciales: Acepta pagos en cuotas, registro de método de pago
- Persistencia: Todos los datos se guardan en JSON

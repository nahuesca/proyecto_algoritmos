# PROYECTO ESTRUCTURA DE DATOS 1

## Descripción del Negocio

Sistema de gestión integral para una PyME de servicios técnicos (climatización y electricidad).

**Equipo:** 1 dueño (oficina) + 3 técnicos (campo)

### Problema Actual
- Pedidos en cuaderno, datos en Excel básico
- Coordinación por WhatsApp
- Información dispersa (cuadernos, WhatsApp, Excel, memoria)
- Sin visibilidad del estado de trabajos en tiempo real

---

## Módulos del Sistema

### 1. Órdenes de Servicio
- Crear órdenes con cliente, problema, técnico y presupuesto
- Cambiar estado: Pendiente → En Proceso → Completada → Cobrada
- Ver órdenes abiertas y buscar por cliente

### 2. Gestión de Técnicos
- Registrar técnicos y especialidades
- Asignar/reasignar órdenes
- Ver estado de disponibilidad

### 3. Control de Pagos y Deudas
- Registrar pagos (efectivo, transferencia, cuotas)
- Clasificar clientes: frecuente / nuevo / problemático
- Alertar deudas pendientes

### 4. Búsqueda e Historial de Clientes
- Buscar por nombre, teléfono o apodo
- Ver historial completo de trabajos y pagos
- Acceso rápido desde el campo

### 5. Presupuestos y Costos
- Calcular presupuestos automáticamente
- Clasificar trabajos: simple / complicado
- Calcular comisiones de técnicos

---

## Estructuras de Datos

```python
clientes      # {teléfono: {nombre, órdenes}}
tecnicos      # {id_tecnico: {nombre, especialidad, disponible}}
ordenes       # {id_orden: {datos del trabajo}}
pagos         # {id_orden: {cobrado, facturado}}
presupuestos  # {id_orden: {repuestos, mano de obra, total}}
```

---

## Flujo Típico de un Trabajo

```
Cliente llama
    ↓
Dueño registra orden (PENDIENTE)
    ↓
Técnico va al trabajo (EN PROCESO)
    ↓
Técnico termina (COMPLETADA)
    ↓
Se cobra (COBRADA) → Orden archivada
```

---

## MVP – Mínimo Viable

**Obligatorio:**
1. Registro y gestión de órdenes
2. Control de pagos y deudas
3. Búsqueda rápida (teléfono/nombre)

**Puede esperar:**
- Gestión de técnicos
- Cálculo de presupuestos

---

## Estructura del Proyecto

```
proyecto_algoritmos/
├── main.py           # Archivo principal con toda la lógica
├── README.md         # Este archivo
```

---

## Estado del Proyecto

**En Desarrollo**

- Módulo 1: Órdenes de Servicio (implementado)
- Módulo 2: Gestión de Técnicos (esqueleto)
- Módulo 3: Control de Pagos (esqueleto)
- Módulo 4: Búsqueda de Clientes (esqueleto)
- Módulo 5: Presupuestos (esqueleto)

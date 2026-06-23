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

### 1. Órdenes de Servicio ✓ Implementado
- Crear órdenes con cliente, problema, técnico y presupuesto
- Cambiar estado: Pendiente → En Proceso → Completada → Cobrada
- Ver órdenes abiertas y buscar por cliente
- **Características implementadas:**
  - Persistencia en archivo JSON (`clientes.json`)
  - Búsqueda y creación de clientes por teléfono
  - Validación de datos (teléfono, DNI)
  - Clasificación de clientes: frecuente / nuevo / problemático
  - Alertas para clientes problemáticos
  - Historial de órdenes por cliente

### 2. Gestión de Técnicos 🔧 En Desarrollo
- Registrar técnicos y especialidades
- Asignar/reasignar órdenes
- Ver estado de disponibilidad

### 3. Control de Pagos y Deudas 🔧 En Desarrollo
- Registrar pagos (efectivo, transferencia, cuotas)
- Clasificar clientes: frecuente / nuevo / problemático
- Alertar deudas pendientes

### 4. Búsqueda e Historial de Clientes 🔧 En Desarrollo
- Buscar por nombre, teléfono o apodo
- Ver historial completo de trabajos y pagos
- Acceso rápido desde el campo

### 5. Presupuestos y Costos 🔧 En Desarrollo
- Calcular presupuestos automáticamente
- Clasificar trabajos: simple / complicado
- Calcular comisiones de técnicos

---

## Estructuras de Datos

```python
clientes      # {teléfono: {nombre, dni, direccion, tipo, ordenes}}
tecnicos      # {id_tecnico: {nombre, especialidad, disponible}}
ordenes       # {id_orden: {id, telefono_cliente, descripcion, estado, fecha_creacion, fecha_visita, tecnico_id, repuestos, monto_total}}
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

## MVP – Mínimo Viable ✓ Completado

**Implementado:**
1. ✓ Registro y gestión de órdenes
2. ✓ Control básico de clientes y sus datos
3. ✓ Búsqueda rápida (teléfono/nombre)
4. ✓ Persistencia de datos (JSON)

**En Desarrollo:**
- Gestión de técnicos
- Cálculo de presupuestos
- Sistema de pagos y deudas

---

## Estructura del Proyecto

```
proyecto_algoritmos/
├── main.py                  # Sistema principal con menú interactivo
├── validaciones.py          # Funciones de validación (teléfono, DNI)
├── clientes.json            # Base de datos de clientes y órdenes
├── README.md                # Este archivo
```

---

## Instalación y Uso

### Requisitos
- Python 3.7+

### Ejecutar el sistema
```bash
python main.py
```

El sistema presenta un menú interactivo con las siguientes opciones:

**Órdenes de Servicio:**
1. Crear orden de servicio
2. Cambiar estado de una orden
3. Ver órdenes pendientes

**Técnicos:**
4. Registrar técnico
5. Mostrar técnicos
6. Asignar técnico a una orden

**Pagos:**
7. Registrar pago
8. Ver estado de pagos / deudas

**Clientes:**
9. Buscar cliente
10. Ver historial de cliente

**Presupuestos:**
11. Generar presupuesto
12. Ver presupuestos

---

## Estado del Proyecto

**En Desarrollo - Fase 1 Completada**

### Módulo 1: Órdenes de Servicio ✓
- [x] Crear órdenes
- [x] Cambiar estados
- [x] Listar órdenes activas
- [x] Persistencia en JSON
- [x] Validación de datos

### Módulo 2: Gestión de Técnicos 🔧
- [ ] Registrar técnicos
- [ ] Mostrar técnicos
- [ ] Asignar técnico a orden

### Módulo 3: Control de Pagos 🔧
- [ ] Registrar pagos
- [ ] Ver estado de pagos/deudas

### Módulo 4: Búsqueda de Clientes 🔧
- [ ] Buscar cliente
- [ ] Ver historial completo

### Módulo 5: Presupuestos 🔧
- [ ] Generar presupuestos
- [ ] Ver presupuestos

---

## Notas de Desarrollo

- El sistema almacena datos en `clientes.json` para persistencia entre sesiones
- Los clientes se identifican por número de teléfono (clave única)
- Las órdenes tienen ID único en formato `ORD-N`
- Se validan teléfono y DNI con funciones de validación
- Existe alerta automática para clientes clasificados como "problemáticos"

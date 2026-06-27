# PROYECTO ESTRUCTURA DE DATOS 1

## Descripcion del Negocio

Sistema de gestion integral para una PyME de servicios tecnicos (climatizacion y electricidad).

**Equipo:** 1 dueno (oficina) + 3 tecnicos (campo)

### Problema Actual
- Pedidos en cuaderno, datos en Excel basico
- Coordinacion por WhatsApp
- Informacion dispersa (cuadernos, WhatsApp, Excel, memoria)
- Sin visibilidad del estado de trabajos en tiempo real

---

## Modulos del Sistema

### 1. Ordenes de Servicio ✓ Implementado
- Crear ordenes con cliente, problema, tecnico y presupuesto
- Cambiar estado: Pendiente → En Proceso → Completada → Cobrada
- Ver ordenes abiertas y buscar por cliente
- Persistencia en archivo JSON (`clientes.json`)
- Validacion de datos (telefono, DNI)
- Clasificacion de clientes: frecuente / nuevo / problematico
- Alertas para clientes problematicos y con deuda pendiente

### 2. Gestion de Tecnicos ✓ Implementado
- Registrar tecnicos con nombre, especialidad y telefono (telefono opcional)
- Asignar tecnico disponible a una orden
- Reasignar tecnico entre ordenes
- Finalizar trabajo (marca la ultima orden del tecnico como completada)
- Disponibilidad calculada en tiempo real a partir de las ordenes asignadas
- Ver estado de disponibilidad en tiempo real

### 3. Control de Pagos y Deudas ✓ Implementado
- Registrar deuda al completar una orden
- Aceptar pagos parciales o totales (efectivo / transferencia)
- Ver clientes con saldo pendiente
- Historial de pagos por cliente
- Alerta automatica de deuda al crear una orden nueva
- Persistencia en archivo JSON (`pagos.json`)

### 4. Busqueda e Historial de Clientes ✓ Implementado
- Buscar por nombre, telefono o apodo (búsqueda por texto con regex)
- Ver historial completo de trabajos y pagos (ordenes ordenadas por fecha)
- Acceso rapido desde el campo

### 5. Presupuestos y Costos ✓ Implementado
- Calcular presupuestos automaticamente (suma de repuestos + mano de obra)
- Clasificar trabajos: simple / complicado (costos de mano de obra configurables)
- Ajuste manual del total y registro de aprobacion/rechazo por cliente
- Calcular comisiones de tecnicos por mes (basado en ordenes cobradas)
- Persistencia en archivo JSON (`presupuestos.json`)

---

## Estructuras de Datos

```python
clientes      # {telefono: {nombre, dni, direccion, tipo, ordenes}}
tecnicos      # {id_tecnico: {nombre, especialidad, telefono, ordenes_asignadas}}
ordenes       # {id_orden: {id, telefono_cliente, descripcion, estado, fecha_creacion, fecha_visita, tecnico_id, repuestos, monto_total}}
pagos         # {id_orden: {id_orden, telefono_cliente, monto_total, saldo, transacciones: [{monto, metodo, fecha}]}}
presupuestos  # {id_orden: {id_orden, tipo_trabajo, mano_de_obra, repuestos, total_calculado, total_final, estado}}
```

---

## Flujo Tipico de un Trabajo

```
Cliente llama
    ↓
Dueno registra orden (PENDIENTE)  → alerta si el cliente tiene deuda
    ↓
Se asigna tecnico disponible (EN PROCESO) → posibilidad de reasignar tecnico si es necesario
    ↓
Tecnico termina (COMPLETADA)
    ↓
Se registra deuda / pago (permitidos pagos parciales)
    ↓
Saldo en cero → orden pasa a COBRADA
    ↓
Si hubo presupuesto aprobado, se registra el estado del presupuesto (aprobado/rechazado)
```

---

## Estructura del Proyecto

```
proyecto_algoritmos/
├── main.py           # Sistema principal con menu interactivo
├── validaciones.py   # Funciones de validacion (telefono, DNI)
├── clientes.json     # Base de datos de clientes y ordenes
├── tecnicos.json     # Base de datos de tecnicos
├── pagos.json        # Base de datos de pagos y deudas
├── presupuestos.json # Base de datos de presupuestos y presupuestos registrados
└── README.md         # Este archivo
```

---

## Instalacion y Uso

### Requisitos
- Python 3.7+

### Ejecutar el sistema
```bash
python main.py
```

---

## Notas Técnicas y Nuevos Cambios
- El sistema ahora determina la disponibilidad de los técnicos en tiempo real revisando sus ordenes asignadas (no se almacena un campo "disponible").
- Se agregó la posibilidad de reasignar técnicos entre ordenes y de finalizar el trabajo de un técnico (marca la última orden del técnico como completada).
- Los presupuestos se calculan automáticamente a partir de los repuestos y un costo de mano de obra según el tipo de trabajo (constantes definidas: MANO_OBRA_SIMPLE, MANO_OBRA_COMPLICADO).
- Los presupuestos permiten ajuste manual y registro de aprobacion/rechazo por parte del cliente.
- Se añadió el módulo de comisiones: calcular comisiones mensuales por técnico sobre órdenes cobradas.
- Validaciones mejoradas: teléfono y DNI se validan al crear clientes y técnicos (telefono opcional para técnicos).
- Las funciones puras (ej. calcular_total_presupuesto) están diseñadas para facilitar tests automatizados (pytest).
- Archivos JSON: si faltan o están corruptos, el sistema inicializa estructuras vacías y continúa funcionando mostrando un aviso.

---

## Estado del Proyecto

### Modulo 1: Ordenes de Servicio ✓
- [x] Crear ordenes
- [x] Cambiar estados
- [x] Listar ordenes activas
- [x] Persistencia en JSON
- [x] Validacion de datos

### Modulo 2: Gestion de Tecnicos ✓
- [x] Registrar tecnicos
- [x] Mostrar tecnicos
- [x] Asignar tecnico a orden
- [x] Reasignar tecnico
- [x] Finalizar trabajo y liberar tecnico
- [x] Disponibilidad derivada de ordenes

### Modulo 3: Control de Pagos ✓
- [x] Registrar deuda al completar orden
- [x] Pagos parciales y totales
- [x] Ver clientes deudores
- [x] Historial de pagos por cliente
- [x] Alerta de deuda al crear orden
- [x] Persistencia en JSON

### Modulo 4: Busqueda de Clientes ✓
- [x] Buscar cliente (nombre/telefono)
- [x] Ver historial completo (ordenes, tecnicos, pagos)

### Modulo 5: Presupuestos ✓
- [x] Generar presupuestos (repuestos + mano de obra)
- [x] Ajuste manual y registro de aprobacion
- [x] Ver presupuestos
- [x] Calcular comisiones de tecnicos


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
- Registrar tecnicos con nombre, especialidad y telefono
- Asignar tecnico disponible a una orden
- Ver estado de disponibilidad en tiempo real
- Finalizar trabajo y liberar tecnico

### 3. Control de Pagos y Deudas ✓ Implementado
- Registrar deuda al completar una orden
- Aceptar pagos parciales o totales (efectivo / transferencia)
- Ver clientes con saldo pendiente
- Historial de pagos por cliente
- Alerta automatica de deuda al crear una orden nueva
- Persistencia en archivo JSON (`pagos.json`)

### 4. Busqueda e Historial de Clientes 🔧 En Desarrollo
- Buscar por nombre, telefono o apodo
- Ver historial completo de trabajos y pagos
- Acceso rapido desde el campo

### 5. Presupuestos y Costos 🔧 En Desarrollo
- Calcular presupuestos automaticamente
- Clasificar trabajos: simple / complicado
- Calcular comisiones de tecnicos

---

## Estructuras de Datos

```python
clientes      # {telefono: {nombre, dni, direccion, tipo, ordenes}}
tecnicos      # {id_tecnico: {nombre, especialidad, telefono, ordenes_asignadas}}
ordenes       # {id_orden: {id, telefono_cliente, descripcion, estado, fecha_creacion, fecha_visita, tecnico_id}}
pagos         # {id_orden: {id_orden, telefono_cliente, monto_total, saldo, transacciones}}
presupuestos  # {id_orden: {repuestos, mano_de_obra, total}}
```

---

## Flujo Tipico de un Trabajo

```
Cliente llama
    ↓
Dueno registra orden (PENDIENTE)  → alerta si el cliente tiene deuda
    ↓
Tecnico va al trabajo (EN PROCESO)
    ↓
Tecnico termina (COMPLETADA)
    ↓
Se registra deuda / pago
    ↓
Saldo en cero → orden pasa a COBRADA
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
- [x] Liberar tecnico al finalizar
- [x] Validacion de telefono

### Modulo 3: Control de Pagos ✓
- [x] Registrar deuda al completar orden
- [x] Pagos parciales y totales
- [x] Ver clientes deudores
- [x] Historial de pagos por cliente
- [x] Alerta de deuda al crear orden
- [x] Persistencia en JSON

### Modulo 4: Busqueda de Clientes 🔧
- [ ] Buscar cliente
- [ ] Ver historial completo

### Modulo 5: Presupuestos 🔧
- [ ] Generar presupuestos
- [ ] Ver presupuestos

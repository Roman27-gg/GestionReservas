# Software FJ: Sistema Integral de Gestión de Clientes, Servicios y Reservas

Aplicación en Python 3.10+ orientada a objetos para la empresa **Software FJ**,
que gestiona clientes, servicios y reservas (reservas de salas, alquiler de
equipos y asesorías especializadas).

## Estructura del Proyecto

```
software_fj/
├── AGENTS.md              # Especificaciones y reglas de desarrollo
├── README.md              # Este archivo
├── requirements.txt       # Dependencias (solo librería estándar)
├── main.py                # Simulación de 12 operaciones completas
├── src/
│   ├── __init__.py
│   ├── excepciones.py     # Jerarquía de excepciones personalizadas
│   ├── logger.py          # Configuración de logging
│   ├── entidad.py         # Clase abstracta base Entidad
│   ├── cliente.py         # Cliente con encapsulación y validación
│   ├── servicio.py        # Clase abstracta Servicio
│   ├── servicios_concretos.py  # ReservaSala, AlquilerEquipo, AsesoriaEspecializada
│   ├── reserva.py         # Reserva con estados y transiciones
│   └── gestor.py          # Orquestación centralizada (memoria)
├── tests/
│   ├── __init__.py
│   ├── test_excepciones.py
│   ├── test_cliente.py
│   ├── test_servicios.py
│   ├── test_reserva.py
│   ├── test_gestor.py
│   └── test_simulacion.py
└── logs/
    └── eventos.log        # Archivo de log generado en ejecución
```

## Requisitos

- Python 3.10 o superior
- Solo librería estándar de Python (`abc`, `logging`, `datetime`, `re`, `unittest`, etc.)
- No se utiliza ninguna base de datos (todo en memoria)

## Cómo ejecutar el programa

Desde la raíz del proyecto:

```bash
python3 main.py
```

La simulación ejecuta 12 operaciones (válidas e inválidas), muestra resultados
por consola y registra todo en `logs/eventos.log`. Al final imprime un resumen
de operaciones exitosas y errores controlados.

## Cómo correr las pruebas

Desde la raíz del proyecto:

```bash
python3 -m unittest discover -s tests -v
```

Se ejecutan 99 pruebas unitarias que cubren:
- Excepciones personalizadas (lanzamiento, jerarquía, encadenamiento `__cause__`)
- Cliente (datos válidos, inválidos por campo, encapsulación)
- Servicios (cálculo correcto, variantes impuesto/descuento, validación, polimorfismo)
- Reserva (transiciones de estado, confirmar/cancelar/procesar, errores)
- Gestor (CRUD, integridad, reservas)
- Simulación (ejecución completa, generación de log)

## Decisiones de implementación

| Decisión | Valor |
|----------|-------|
| Sobrecarga `calcular_costo` | Argumentos por defecto + `**kwargs` |
| ID de entidades | Entero autoincremental |
| Servicio no disponible | Atributo `disponible` en `Servicio` |
| Formato documento | Alfanumérico 6-12 caracteres |
| IVA | 0.19 (19%) |
| Descuento máximo | 0.30 (30%) |
| Enum estados | `EstadoReserva` en `reserva.py` |
| Type hints | En toda firma pública |
| Python target | >= 3.10 |

## Arquitectura

- **Entidad**: Clase abstracta base con `id` autoincremental y `describir()` abstracto
- **Cliente**: Hereda de `Entidad`, datos encapsulados con `@property` y setters validados
- **Servicio**: Clase abstracta con `calcular_costo()`, `describir()` y `validar_parametros()`
- **Servicios concretos**: `ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada`
- **Reserva**: Integra cliente, servicio, duración y estado (`PENDIENTE`, `CONFIRMADA`, `CANCELADA`, `PROCESADA`)
- **Gestor**: Listas internas en memoria, orquestación de operaciones
- **Excepciones**: Jerarquía propia desde `SoftwareFJError` con encadenamiento `raise ... from ...`
- **Logging**: Archivo `logs/eventos.log` con fecha, nivel y mensaje

# AGENTS.md — Software FJ: Sistema Integral de Gestión de Clientes, Servicios y Reservas

Este archivo define cómo debe trabajar cualquier agente de código en este proyecto. Léelo completo antes de escribir una sola línea.

## 1. Descripción del proyecto

Aplicación en **Python 3.10+**, orientada a objetos, para la empresa **Software FJ**, que gestiona **clientes, servicios y reservas**. Los servicios son: reservas de salas, alquiler de equipos y asesorías especializadas.

Objetivo: una aplicación **estable, modular y extensible** que aplique de forma rigurosa:

- Abstracción
- Herencia
- Polimorfismo
- Encapsulación
- Manejo avanzado de excepciones

La aplicación **nunca debe caerse** por un error de datos u operación: los errores se capturan, se registran en el log y el programa continúa.

## 2. Restricciones obligatorias

- **Prohibido usar bases de datos** (nada de sqlite3, SQLAlchemy, etc.). Toda la información vive en objetos y listas en memoria.
- Los **archivos solo se usan para el log** de eventos y errores.
- Usar únicamente la librería estándar de Python para la aplicación (`abc`, `logging`, `datetime`, `re`, `unittest`, `tkinter`, etc.). Dependencias externas solo para pruebas y solo si son imprescindibles (por ejemplo `pytest`), y deben quedar en `requirements.txt`.
- Código, nombres de clases y comentarios coherentes en un solo idioma (español, siguiendo el enunciado), con nombres de módulos en `snake_case` y clases en `PascalCase`.
- **Interfaz gráfica en inglés** usando `tkinter` (librería estándar). Todos los textos de la GUI deben estar en inglés.

## 3. Arquitectura mínima requerida

| Componente | Requisito |
|---|---|
| Clase abstracta base | Representa entidades generales del sistema (por ejemplo `Entidad`, con `id` y métodos abstractos como `describir()`). |
| `Cliente` | Hereda de la entidad base. Datos personales **encapsulados** (atributos privados, `@property`, setters con validación robusta: nombre, documento, correo, teléfono). |
| `Servicio` (abstracta) | Métodos abstractos para **calcular costo**, **describir** el servicio y **validar parámetros**. |
| Mínimo 3 servicios concretos | `ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada`. Cada uno **sobrescribe** los métodos abstractos (polimorfismo). |
| `Reserva` | Integra cliente, servicio, duración y estado (`PENDIENTE`, `CONFIRMADA`, `CANCELADA`, etc.). Implementa `confirmar()`, `cancelar()` y `procesar()` con manejo de excepciones. |
| Métodos sobrecargados | Variantes del cálculo de costo: con impuestos, con descuentos, con parámetros opcionales. En Python se logra con argumentos por defecto, `*args/**kwargs` o `functools.singledispatchmethod`; documenta la técnica elegida. |
| **Interfaz gráfica (GUI)** | Ventana en inglés con `tkinter` que permita: registrar clientes, crear servicios, crear reservas, confirmar/cancelar/procesar reservas, y listar entidades. Todos los textos de la interfaz en inglés. |
| Archivo de logs | Registra **todos** los errores y eventos relevantes (usar el módulo `logging`, con fecha, nivel y mensaje). |

### Excepciones (requisito central)

- Jerarquía de **excepciones personalizadas** que hereden de una excepción base del proyecto (por ejemplo `SoftwareFJError`): datos inválidos, parámetros faltantes, operación no permitida, reserva incorrecta, servicio no disponible, cálculo inconsistente.
- Usar y demostrar **todas** estas estructuras: `try/except`, `try/except/else`, `try/except/finally`.
- Usar **encadenamiento de excepciones** (`raise NuevaExcepcion(...) from error_original`).
- Cada error capturado debe quedar registrado en el log antes de continuar.
- Prohibido el `except:` desnudo y prohibido silenciar errores con `pass`.

## 4. Estructura de carpetas esperada (división por paquetes)

```
software_fj/
├── AGENTS.md
├── README.md
├── requirements.txt
├── main.py                  # Ejecuta la simulación de al menos 10 operaciones
├── src/
│   ├── __init__.py
│   ├── excepciones.py       # Excepciones personalizadas
│   ├── logger.py            # Configuración del log
│   ├── entidad.py           # Clase abstracta base
│   ├── cliente.py
│   ├── servicio.py          # Clase abstracta Servicio
│   ├── servicios_concretos.py
│   ├── reserva.py
│   ├── gestor.py            # Listas internas y orquestación (opcional pero recomendado)
│   └── gui/                 # Paquete de interfaz gráfica (en inglés)
│       ├── __init__.py
│       ├── ventana_principal.py   # Ventana principal (MainWindow)
│       ├── clientes_view.py       # Vista de gestión de clientes
│       ├── servicios_view.py      # Vista de gestión de servicios
│       ├── reservas_view.py       # Vista de gestión de reservas
│       └── widgets.py             # Widgets reutilizables
├── tests/
│   ├── __init__.py
│   ├── test_cliente.py
│   ├── test_servicios.py
│   ├── test_reserva.py
│   ├── test_excepciones.py
│   ├── test_gui.py            # Pruebas para la interfaz gráfica
│   └── test_simulacion.py
└── logs/
    └── eventos.log          # Generado en ejecución
```

El proyecto debe dividirse en paquetes (carpetas con `__init__.py`) que separen responsabilidades: lógica de dominio (`src/`), interfaz gráfica (`src/gui/`), y pruebas (`tests/`). Puedes ajustar nombres, pero conserva la separación por responsabilidades y documenta cualquier cambio en el README.

## 5. Pruebas unitarias (obligatorias)

- Usar `unittest` (o `pytest` si se agrega a `requirements.txt`).
- Comando oficial para correr todas las pruebas desde la raíz del proyecto:

  ```bash
  python -m unittest discover -s tests -v
  ```

- Cobertura mínima de pruebas por componente:
  - **Cliente**: datos válidos, datos inválidos (cada campo), encapsulación (no se puede asignar un valor inválido).
  - **Servicios**: cada servicio concreto calcula el costo correcto; las variantes sobrecargadas (con impuesto, con descuento, sin parámetros opcionales); validación de parámetros incorrectos; polimorfismo (tratar una lista de servicios como `Servicio`).
  - **Reserva**: confirmar, cancelar, procesar; transiciones de estado válidas e inválidas (por ejemplo, confirmar una reserva ya cancelada); duración inválida; servicio no disponible.
  - **Excepciones**: cada excepción personalizada se lanza en el caso correcto; el encadenamiento (`__cause__`) está presente donde corresponde.
  - **Logs**: los errores quedan escritos en el archivo de log.
  - **GUI**: la ventana principal se crea sin errores; los botones y campos existen y responden; los textos están en inglés.
  - **Simulación**: `main.py` o la función de simulación se ejecuta completa sin lanzar excepciones no controladas.
- Las pruebas deben ser **independientes y repetibles**: no depender del orden, y limpiar o aislar el archivo de log (por ejemplo con un directorio temporal).
- Probar casos felices **y** casos de error. Una suite que solo prueba el camino feliz no es suficiente.

## 6. Ciclo de trabajo obligatorio: iterar hasta que todo esté correcto

El agente **no debe dar una tarea por terminada tras el primer intento**. Debe seguir este ciclo cuantas veces haga falta:

1. **Planificar**: revisar qué parte de los requisitos (sección 3) se va a implementar o corregir.
2. **Escribir primero la prueba** (o al menos junto con el código) que demuestra el comportamiento esperado.
3. **Implementar** el código mínimo necesario.
4. **Ejecutar las pruebas**: `python -m unittest discover -s tests -v`.
5. **Ejecutar la aplicación**: `python main.py` y verificar que no se interrumpe y que el log se genera.
6. **Si algo falla**: leer el error completo, encontrar la causa raíz, corregir y **volver al paso 4**. No avanzar con pruebas en rojo.
7. **Revisar la lista de verificación** (sección 8) y detectar qué falta.
8. **Refactorizar** si hay duplicación o responsabilidades mezcladas, y volver a correr pruebas y aplicación.
9. Repetir hasta que **todas** las casillas de la sección 8 estén cumplidas.

Reglas del ciclo:

- Nunca declarar "listo" sin haber ejecutado realmente las pruebas y la aplicación, y sin mostrar su resultado.
- Nunca borrar, comentar ni debilitar una prueba para que pase. Si una prueba es incorrecta, corrígela explicando por qué.
- No ocultar errores con `try/except` amplios para lograr verde. Una prueba que pasa por silenciar un fallo real es una prueba fallida.
- Si tras varios intentos una causa no es evidente, agregar trazas o logs temporales, aislar el caso mínimo que reproduce el error y retirar lo temporal al terminar.
- Cada corrección de un bug debe incluir una prueba que lo habría detectado.

## 7. Simulación obligatoria (`main.py`)

Sin base de datos, el programa debe simular **al menos 10 operaciones completas** que incluyan:

- Registros de clientes **válidos e inválidos**.
- Creación **correcta e incorrecta** de servicios.
- Reservas **exitosas y fallidas** (confirmadas, canceladas, con datos inválidos, con servicio no disponible).
- Casos de errores graves, tras los cuales el programa **continúa** con la siguiente operación.

Cada operación debe imprimir un resultado claro por consola y dejar registro en el log. Al final, mostrar un resumen (operaciones exitosas, errores controlados).

## 8. Definición de terminado (lista de verificación)

El trabajo solo está terminado cuando **todo** lo siguiente es cierto:

- [ ] Existe una clase abstracta base de entidades.
- [ ] `Cliente` tiene encapsulación y validaciones robustas.
- [ ] `Servicio` es abstracta y hay al menos 3 servicios concretos que sobrescriben costo, descripción y validación.
- [ ] `Reserva` integra cliente, servicio, duración y estado, con `confirmar`, `cancelar` y `procesar`.
- [ ] Hay métodos sobrecargados (variantes de cálculo de costo) y están probados.
- [ ] Hay excepciones personalizadas con jerarquía propia.
- [ ] Se usan `try/except`, `try/except/else`, `try/except/finally` y encadenamiento con `raise ... from ...`.
- [ ] Todos los errores se registran en el archivo de logs.
- [ ] No se usa ninguna base de datos.
- [ ] Existe una interfaz gráfica en inglés con `tkinter` (paquete `src/gui/`).
- [ ] La simulación ejecuta 10 o más operaciones completas, válidas e inválidas, sin interrumpirse.
- [ ] `python -m unittest discover -s tests -v` pasa al 100 %.
- [ ] `python main.py` se ejecuta de principio a fin sin excepciones no controladas.
- [ ] El código está documentado (docstrings en clases y métodos públicos) y el `README.md` explica estructura, cómo ejecutar el programa y cómo correr las pruebas.
- [ ] El proyecto está dividido en paquetes (carpetas con `__init__.py`) que separan responsabilidades.

## 9. Estilo de código

- Seguir PEP 8; type hints en funciones públicas.
- Docstrings en todas las clases y métodos públicos.
- Funciones y métodos cortos, con una sola responsabilidad.
- Sin números ni textos mágicos repetidos: usar constantes o enums (por ejemplo `Enum` para el estado de la reserva).
- Nunca usar `print` para registrar errores internos: usar `logging`. `print` solo para la salida de la simulación al usuario.
- Mensajes de error claros, específicos y útiles para depurar.
- Todos los textos de la interfaz gráfica deben estar en inglés.

## 10. Cómo reportar al terminar cada iteración

Al final de cada bloque de trabajo, el agente debe informar:

1. Qué cambió y en qué archivos.
2. El resultado real de `python -m unittest discover -s tests -v` (cantidad de pruebas y si pasaron).
3. El resultado de `python main.py` y una verificación del contenido del log.
4. Qué ítems de la sección 8 siguen pendientes, y cuál es el siguiente paso.

Si algo no se pudo verificar, decirlo explícitamente en lugar de suponer que funciona.

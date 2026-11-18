"""Simulación principal del proyecto Software FJ.

Ejecuta al menos 10 operaciones completas que incluyen:
- Registros de clientes válidos e inválidos
- Creación correcta e incorrecta de servicios
- Reservas exitosas y fallidas
- Casos de errores graves tras los cuales el programa continúa

Cada operación imprime un resultado claro por consola y deja registro
en el log. Al final, muestra un resumen de operaciones exitosas y
errores controlados.
"""

from src.cliente import crear_cliente, Cliente
from src.servicios_concretos import (
    crear_servicio,
    ReservaSala,
    AlquilerEquipo,
    AsesoriaEspecializada,
)
from src.reserva import Reserva, EstadoReserva
from src.gestor import Gestor
from src.excepciones import (
    DatosInvalidosError,
    ParametrosFaltantesError,
    OperacionNoPermitidaError,
    ServicioNoDisponibleError,
    CalculoInconsistenteError,
    SoftwareFJError,
)
from src.logger import logger

# Contadores de operaciones
operaciones_exitosas = 0
errores_controlados = 0


def registrar_operacion_exitosa(mensaje: str) -> None:
    """Registra una operación exitosa e imprime por consola."""
    global operaciones_exitosas
    operaciones_exitosas += 1
    logger.info("OPERACIÓN EXITOSA: %s", mensaje)
    print(f"[OK] {mensaje}")


def registrar_error_controlado(mensaje: str, error: Exception) -> None:
    """Registra un error controlado e imprime por consola."""
    global errores_controlados
    errores_controlados += 1
    logger.error("ERROR CONTROLADO: %s - %s", mensaje, error)
    print(f"[ERROR] {mensaje}: {error}")


def operacion_1_registro_cliente_valido(gestor: Gestor) -> None:
    """Operación 1: Registrar cliente válido."""
    try:
        cliente = crear_cliente(
            nombre="Juan Pérez",
            documento="ABC12345",
            correo="juan@email.com",
            telefono="3001234567",
        )
        gestor.registrar_cliente(cliente)
        registrar_operacion_exitosa(
            f"Cliente registrado: {cliente.nombre} (id={cliente.id})"
        )
    except (DatosInvalidosError, ParametrosFaltantesError) as error:
        registrar_error_controlado("Registro de cliente válido", error)


def operacion_2_registro_cliente_documento_invalido(gestor: Gestor) -> None:
    """Operación 2: Registrar cliente con documento inválido."""
    try:
        cliente = crear_cliente(
            nombre="María García",
            documento="AB",  # Muy corto
            correo="maria@email.com",
            telefono="3019876543",
        )
        gestor.registrar_cliente(cliente)
        registrar_operacion_exitosa(
            f"Cliente registrado: {cliente.nombre} (id={cliente.id})"
        )
    except (DatosInvalidosError, ParametrosFaltantesError) as error:
        registrar_error_controlado("Registro cliente documento inválido", error)


def operacion_3_registro_cliente_correo_invalido(gestor: Gestor) -> None:
    """Operación 3: Registrar cliente con correo inválido."""
    try:
        cliente = crear_cliente(
            nombre="Carlos López",
            documento="XYZ98765",
            correo="correo-invalido",
            telefono="3029876543",
        )
        gestor.registrar_cliente(cliente)
        registrar_operacion_exitosa(
            f"Cliente registrado: {cliente.nombre} (id={cliente.id})"
        )
    except (DatosInvalidosError, ParametrosFaltantesError) as error:
        registrar_error_controlado("Registro cliente correo inválido", error)


def operacion_4_crear_reserva_sala_valida(gestor: Gestor) -> None:
    """Operación 4: Crear servicio ReservaSala válido."""
    try:
        servicio = crear_servicio(
            "ReservaSala", tipo_sala="estándar", capacidad=10, equipamiento=False
        )
        gestor.registrar_servicio(servicio)
        registrar_operacion_exitosa(
            f"Servicio creado: {servicio.nombre} (id={servicio.id})"
        )
    except (DatosInvalidosError, ParametrosFaltantesError) as error:
        registrar_error_controlado("Creación ReservaSala válida", error)


def operacion_5_crear_reserva_sala_invalida(gestor: Gestor) -> None:
    """Operación 5: Crear ReservaSala con capacidad inválida."""
    try:
        servicio = crear_servicio(
            "ReservaSala", tipo_sala="estándar", capacidad=0, equipamiento=False
        )
        gestor.registrar_servicio(servicio)
        registrar_operacion_exitosa(
            f"Servicio creado: {servicio.nombre} (id={servicio.id})"
        )
    except (DatosInvalidosError, ParametrosFaltantesError) as error:
        registrar_error_controlado("Creación ReservaSala inválida", error)


def operacion_6_crear_alquiler_equipo_valido(gestor: Gestor) -> None:
    """Operación 6: Crear servicio AlquilerEquipo válido."""
    try:
        servicio = crear_servicio(
            "AlquilerEquipo", tipo_equipo="básico", cantidad=2, incluye_tecnico=False
        )
        gestor.registrar_servicio(servicio)
        registrar_operacion_exitosa(
            f"Servicio creado: {servicio.nombre} (id={servicio.id})"
        )
    except (DatosInvalidosError, ParametrosFaltantesError) as error:
        registrar_error_controlado("Creación AlquilerEquipo válido", error)


def operacion_7_crear_asesoria_valida(gestor: Gestor) -> None:
    """Operación 7: Crear servicio AsesoriaEspecializada válido."""
    try:
        servicio = crear_servicio(
            "AsesoriaEspecializada",
            especialidad="Contabilidad",
            nivel_experto="SENIOR",
            modalidad="virtual",
        )
        gestor.registrar_servicio(servicio)
        registrar_operacion_exitosa(
            f"Servicio creado: {servicio.nombre} (id={servicio.id})"
        )
    except (DatosInvalidosError, ParametrosFaltantesError) as error:
        registrar_error_controlado("Creación Asesoria válida", error)


def operacion_8_reserva_exitosa_confirmar_procesar(gestor: Gestor) -> None:
    """Operación 8: Reserva exitosa → confirmar → procesar."""
    try:
        # Buscar cliente y servicio creados en operaciones anteriores
        clientes = gestor.listar_clientes()
        servicios = gestor.listar_servicios()
        if not clientes or not servicios:
            raise DatosInvalidosError("No hay clientes o servicios registrados")

        cliente = clientes[0]
        servicio = servicios[0]  # Debería ser la ReservaSala de op 4

        reserva = gestor.crear_reserva(
            cliente_id=cliente.id,
            servicio_id=servicio.id,
            duracion=3.0,
        )
        gestor.confirmar_reserva(reserva.id)
        costo = gestor.procesar_reserva(reserva.id)
        registrar_operacion_exitosa(
            f"Reserva procesada: id={reserva.id}, cliente={cliente.nombre}, "
            f"servicio={servicio.nombre}, costo={costo:.2f}"
        )
    except (
        DatosInvalidosError,
        OperacionNoPermitidaError,
        ServicioNoDisponibleError,
        CalculoInconsistenteError,
    ) as error:
        registrar_error_controlado("Reserva exitosa confirmar-procesar", error)


def operacion_9_reserva_cliente_inexistente(gestor: Gestor) -> None:
    """Operación 9: Reserva con cliente inexistente."""
    try:
        servicios = gestor.listar_servicios()
        if not servicios:
            raise DatosInvalidosError("No hay servicios registrados")

        servicio = servicios[0]
        gestor.crear_reserva(
            cliente_id=9999,  # ID inexistente
            servicio_id=servicio.id,
            duracion=1.0,
        )
        registrar_operacion_exitosa("Reserva con cliente inexistente (inesperado)")
    except DatosInvalidosError as error:
        registrar_error_controlado("Reserva cliente inexistente", error)


def operacion_10_reserva_servicio_no_disponible(gestor: Gestor) -> None:
    """Operación 10: Reserva con servicio no disponible."""
    try:
        clientes = gestor.listar_clientes()
        if not clientes:
            raise DatosInvalidosError("No hay clientes registrados")

        cliente = clientes[0]
        servicio_no_disp = ReservaSala(
            tipo_sala="VIP", capacidad=5, equipamiento=True, disponible=False
        )
        gestor.registrar_servicio(servicio_no_disp)
        gestor.crear_reserva(
            cliente_id=cliente.id,
            servicio_id=servicio_no_disp.id,
            duracion=1.0,
        )
        registrar_operacion_exitosa("Reserva servicio no disponible (inesperado)")
    except ServicioNoDisponibleError as error:
        registrar_error_controlado("Reserva servicio no disponible", error)


def operacion_11_cancelar_reserva_confirmada(gestor: Gestor) -> None:
    """Operación 11: Cancelar reserva confirmada."""
    try:
        clientes = gestor.listar_clientes()
        servicios = gestor.listar_servicios()
        if not clientes or not servicios:
            raise DatosInvalidosError("No hay clientes o servicios registrados")

        cliente = clientes[0]
        servicio = servicios[1] if len(servicios) > 1 else servicios[0]

        reserva = gestor.crear_reserva(
            cliente_id=cliente.id,
            servicio_id=servicio.id,
            duracion=1.0,
        )
        gestor.confirmar_reserva(reserva.id)
        gestor.cancelar_reserva(reserva.id)
        registrar_operacion_exitosa(
            f"Reserva cancelada: id={reserva.id}, estado={reserva.estado.value}"
        )
    except (
        DatosInvalidosError,
        OperacionNoPermitidaError,
        ServicioNoDisponibleError,
    ) as error:
        registrar_error_controlado("Cancelar reserva confirmada", error)


def operacion_12_confirmar_reserva_ya_cancelada(gestor: Gestor) -> None:
    """Operación 12: Confirmar reserva ya cancelada (debe fallar)."""
    try:
        clientes = gestor.listar_clientes()
        servicios = gestor.listar_servicios()
        if not clientes or not servicios:
            raise DatosInvalidosError("No hay clientes o servicios registrados")

        cliente = clientes[0]
        servicio = servicios[0]

        reserva = gestor.crear_reserva(
            cliente_id=cliente.id,
            servicio_id=servicio.id,
            duracion=1.0,
        )
        gestor.cancelar_reserva(reserva.id)
        # Intentar confirmar una reserva ya cancelada → debe fallar
        gestor.confirmar_reserva(reserva.id)
        registrar_operacion_exitosa(
            f"Confirmar reserva cancelada (inesperado, id={reserva.id})"
        )
    except OperacionNoPermitidaError as error:
        registrar_error_controlado("Confirmar reserva ya cancelada", error)


def simular() -> dict:
    """Ejecuta la simulación de al menos 10 operaciones.

    Returns:
        Diccionario con resumen: {'exitosas': int, 'errores': int}.
    """
    global operaciones_exitosas, errores_controlados
    operaciones_exitosas = 0
    errores_controlados = 0

    print("=" * 60)
    print("SIMULACIÓN - Software FJ: Sistema de Gestión")
    print("=" * 60)
    logger.info("=== Inicio de simulación ===")

    gestor = Gestor()

    # Ejecutar todas las operaciones
    operaciones = [
        operacion_1_registro_cliente_valido,
        operacion_2_registro_cliente_documento_invalido,
        operacion_3_registro_cliente_correo_invalido,
        operacion_4_crear_reserva_sala_valida,
        operacion_5_crear_reserva_sala_invalida,
        operacion_6_crear_alquiler_equipo_valido,
        operacion_7_crear_asesoria_valida,
        operacion_8_reserva_exitosa_confirmar_procesar,
        operacion_9_reserva_cliente_inexistente,
        operacion_10_reserva_servicio_no_disponible,
        operacion_11_cancelar_reserva_confirmada,
        operacion_12_confirmar_reserva_ya_cancelada,
    ]

    for operacion in operaciones:
        try:
            operacion(gestor)
        except Exception as error_original:
            # Captura de última instancia para garantizar continuidad
            logger.critical(
                "Error grave no controlado en operación: %s",
                error_original,
            )
            raise CalculoInconsistenteError(
                f"Error grave en simulación: {error_original}"
            ) from error_original

    # Mostrar resumen
    resumen = gestor.resumen_operaciones(
        exitosas=operaciones_exitosas,
        errores=errores_controlados,
    )
    print(resumen)
    logger.info(
        "=== Fin de simulación: %d exitosas, %d errores ===",
        operaciones_exitosas,
        errores_controlados,
    )

    return {"exitosas": operaciones_exitosas, "errores": errores_controlados}


if __name__ == "__main__":
    simular()

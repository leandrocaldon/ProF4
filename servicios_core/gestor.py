# ======================================================================
# INTEGRANTE 5 - Gestor, logs y simulación (rol sin asignar en el grupo)
# ESTADO: hecho por Jefferson como propuesta para que el grupo lo revise.
# Si copias este archivo al repo, borra este encabezado y deja solo el código.
# ======================================================================

"""
gestor.py
GestorSistema: guarda en listas internas los clientes, servicios y reservas
(sin base de datos) y hace todas las operaciones del sistema.
Cada operación usa try/except/else/finally y deja registro en el log.
"""

from excepciones import (
    ClienteInvalidoError,
    ReservaError,
    ReservaNoDisponibleError,
    ServicioInvalidoError,
    ServicioNoDisponibleError,
    SoftwareFJError,
)
from modelos.asesoria import Asesoria
from modelos.cliente import Cliente
from modelos.equipo import AlquilerEquipo
from modelos.reserva import Reserva
from modelos.sala import ReservaSala
from utilidades.logger import registrar_log


class GestorSistema:
    """Administra las listas de clientes, servicios y reservas."""

    TIPOS_SERVICIO = {  # tipo de servicio -> clase que lo crea
        "sala": ReservaSala,
        "equipo": AlquilerEquipo,
        "asesoria": Asesoria,
    }

    def __init__(self):
        self.__clientes = []             # clientes registrados
        self.__servicios = []            # servicios creados
        self.__reservas = []             # reservas hechas
        self.__no_disponibles = set()    # ids de servicios que no se pueden reservar

    # ---------- consultas (solo lectura) ----------
    @property
    def clientes(self):
        return tuple(self.__clientes)

    @property
    def servicios(self):
        return tuple(self.__servicios)

    @property
    def reservas(self):
        return tuple(self.__reservas)

    def buscar_cliente(self, documento):
        """Devuelve el cliente con ese documento, o None si no existe."""
        for cliente in self.__clientes:
            if cliente.documento == str(documento):
                return cliente
        return None

    def buscar_servicio(self, id_servicio):
        """Devuelve el servicio con ese id, o None si no existe."""
        for servicio in self.__servicios:
            if servicio.id == id_servicio:
                return servicio
        return None

    def buscar_reserva(self, id_reserva):
        """Devuelve la reserva con ese id. Si no existe lanza ReservaNoDisponibleError."""
        for reserva in self.__reservas:
            if reserva.id == id_reserva:
                return reserva
        raise ReservaNoDisponibleError(f"No existe la reserva {id_reserva}.")

    # ---------- clientes ----------
    def registrar_cliente(self, nombre, documento, email, telefono):
        """Crea el cliente (Cliente valida los datos) y lo agrega a la lista."""
        try:
            cliente = Cliente(nombre, documento, email, telefono)
        except ClienteInvalidoError as error:
            registrar_log("ERROR", f"Cliente no registrado ({documento}): {error}")
            raise
        else:
            self.__clientes.append(cliente)
            registrar_log("INFO", f"Cliente registrado: {cliente.describir()}")
            return cliente
        finally:
            registrar_log("INFO", "Operación de registro de cliente finalizada.")

    # ---------- servicios ----------
    def registrar_servicio(self, tipo, id_servicio, nombre, tarifa, extra):
        """
        Crea un servicio y lo agrega a la lista.
        extra es la capacidad (sala), las unidades (equipo) o el nivel (asesoría).
        """
        try:
            clase = self.TIPOS_SERVICIO.get(tipo)
            if clase is None:
                raise ServicioInvalidoError(f"Tipo de servicio desconocido: '{tipo}'.")
            if self.buscar_servicio(id_servicio) is not None:
                raise ServicioInvalidoError(f"Ya existe un servicio con id {id_servicio}.")
            if isinstance(tarifa, str):
                try:
                    tarifa = float(tarifa)  # tarifa que llega como texto
                except ValueError as error:
                    # encadena el error de conversión con uno del servicio
                    raise ServicioInvalidoError(f"La tarifa '{tarifa}' no es un número.") from error
            servicio = clase(id_servicio, nombre, tarifa, extra)
        except ServicioInvalidoError as error:
            causa = f" | causa: {type(error.__cause__).__name__}: {error.__cause__}" if error.__cause__ else ""
            registrar_log("ERROR", f"Servicio no creado ({id_servicio}): {error}{causa}")
            raise
        else:
            self.__servicios.append(servicio)
            registrar_log("INFO", f"Servicio creado: {servicio.describir()}")
            return servicio
        finally:
            registrar_log("INFO", "Operación de registro de servicio finalizada.")

    def cambiar_disponibilidad(self, id_servicio, disponible):
        """Marca un servicio como disponible o no disponible para reservar."""
        if self.buscar_servicio(id_servicio) is None:
            raise ServicioInvalidoError(f"No existe el servicio {id_servicio}.")
        if disponible:
            self.__no_disponibles.discard(id_servicio)
        else:
            self.__no_disponibles.add(id_servicio)
        registrar_log("INFO", f"Servicio {id_servicio} {'disponible' if disponible else 'NO disponible'}.")

    # ---------- reservas ----------
    def crear_reserva(self, documento, id_servicio, duracion):
        """Crea una reserva PENDIENTE para un cliente y un servicio que existan."""
        try:
            cliente = self.buscar_cliente(documento)
            if cliente is None:
                raise ReservaError(f"No hay un cliente con documento {documento}.")
            servicio = self.buscar_servicio(id_servicio)
            if servicio is None:
                raise ReservaError(f"No existe el servicio {id_servicio}.")
            if id_servicio in self.__no_disponibles:
                raise ServicioNoDisponibleError(f"El servicio {servicio.nombre} no está disponible.")
            reserva = Reserva(cliente, servicio, duracion)
        except SoftwareFJError as error:
            registrar_log("ERROR", f"Reserva no creada ({documento}, {id_servicio}, {duracion}): "
                                   f"{type(error).__name__}: {error}")
            raise
        else:
            self.__reservas.append(reserva)
            registrar_log("INFO", f"Reserva creada: {reserva.describir()}")
            return reserva
        finally:
            registrar_log("INFO", "Operación de creación de reserva finalizada.")

    def confirmar_reserva(self, id_reserva):
        return self.__cambiar_reserva(id_reserva, "confirmar", lambda r: r.confirmar())

    def cancelar_reserva(self, id_reserva):
        return self.__cambiar_reserva(id_reserva, "cancelar", lambda r: r.cancelar())

    def procesar_reserva(self, id_reserva, impuesto=None, descuento=None):
        return self.__cambiar_reserva(id_reserva, "procesar", lambda r: r.procesar(impuesto, descuento))

    def __cambiar_reserva(self, id_reserva, accion, operacion):
        """Busca la reserva y le aplica confirmar, cancelar o procesar."""
        try:
            reserva = self.buscar_reserva(id_reserva)
            operacion(reserva)
        except SoftwareFJError as error:
            registrar_log("ERROR", f"No se pudo {accion} la reserva {id_reserva[:8]}: "
                                   f"{type(error).__name__}: {error}")
            raise
        else:
            registrar_log("INFO", f"Reserva {accion}: {reserva.describir()}")
            return reserva
        finally:
            registrar_log("INFO", f"Operación '{accion}' finalizada.")

    # ---------- resumen ----------
    def resumen(self):
        return (f"Clientes: {len(self.__clientes)} | Servicios: {len(self.__servicios)} | "
                f"Reservas: {len(self.__reservas)}")

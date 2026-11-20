"""
test_gestor.py
Pruebas del GestorSistema: listas internas y manejo de errores.
"""

import logging
import unittest
from uuid import uuid4

from excepciones import (
    ClienteInvalidoError,
    EstadoReservaError,
    ReservaError,
    ReservaNoDisponibleError,
    ServicioInvalidoError,
    ServicioNoDisponibleError,
    SoftwareFJError,
)
from servicios_core.gestor import GestorSistema

logging.disable(logging.CRITICAL)  # los errores provocados a propósito no se imprimen en pantalla


class TestGestor(unittest.TestCase):
    """Pruebas del GestorSistema."""

    def setUp(self):
        """Prepara un gestor nuevo para cada prueba."""
        self.gestor = GestorSistema()
        self.cliente = self.gestor.registrar_cliente(
            "Prueba Gestor", str(uuid4().int % 1000000000).zfill(9), "gestor@gmail.com", "3001234567")
        self.gestor.registrar_servicio("sala", "S01", "Sala de prueba", 100000, 10)

    def test_listas_internas(self):
        """Verifica que el gestor guarda clientes, servicios y reservas."""
        self.assertEqual(len(self.gestor.clientes), 1)
        self.assertEqual(len(self.gestor.servicios), 1)
        self.assertEqual(len(self.gestor.reservas), 0)

    def test_flujo_reserva(self):
        """Verifica el flujo completo: crear reserva, confirmar y procesar."""
        reserva = self.gestor.crear_reserva(self.cliente.documento, "S01", 2)
        self.gestor.confirmar_reserva(reserva.id)
        self.gestor.procesar_reserva(reserva.id, impuesto=0.19)
        self.assertEqual(reserva.estado, "PROCESADA")
        self.assertEqual(reserva.costo, 238000)

    def test_cliente_invalido_no_se_guarda(self):
        """Verifica que un cliente inválido no se guarda."""
        with self.assertRaises(ClienteInvalidoError):
            self.gestor.registrar_cliente("Malo", "123", "sin-arroba", "300")
        self.assertEqual(len(self.gestor.clientes), 1)

    def test_tarifa_texto_encadena_error(self):
        """Verifica que una tarifa en texto produce un error encadenado."""
        with self.assertRaises(ServicioInvalidoError) as contexto:
            self.gestor.registrar_servicio("equipo", "E01", "PC", "mil", 2)
        self.assertIsInstance(contexto.exception.__cause__, ValueError)

    def test_tipo_desconocido(self):
        """Verifica que un tipo de servicio desconocido falla."""
        with self.assertRaises(ServicioInvalidoError):
            self.gestor.registrar_servicio("transporte", "T01", "Van", 50000, 1)

    def test_servicio_no_disponible(self):
        """Verifica que no se reserva un servicio no disponible."""
        self.gestor.cambiar_disponibilidad("S01", False)
        with self.assertRaises(ServicioNoDisponibleError):
            self.gestor.crear_reserva(self.cliente.documento, "S01", 1)

    def test_cliente_que_no_existe(self):
        """Verifica el error al buscar un cliente que no existe."""
        with self.assertRaises(ReservaError):
            self.gestor.crear_reserva("999999999", "S01", 1)

    def test_reserva_que_no_existe(self):
        """Verifica el error al buscar una reserva que no existe."""
        with self.assertRaises(ReservaNoDisponibleError):
            self.gestor.cancelar_reserva("no-existe")

    def test_cancelar_procesada(self):
        """Verifica que no se cancela una reserva ya procesada."""
        reserva = self.gestor.crear_reserva(self.cliente.documento, "S01", 1)
        self.gestor.confirmar_reserva(reserva.id)
        self.gestor.procesar_reserva(reserva.id)
        with self.assertRaises(EstadoReservaError):
            self.gestor.cancelar_reserva(reserva.id)

    def test_todas_heredan_de_la_base(self):
        """Verifica que todas las excepciones heredan de SoftwareFJError."""
        for excepcion in (ClienteInvalidoError, ServicioInvalidoError, ServicioNoDisponibleError,
                          ReservaError, ReservaNoDisponibleError, EstadoReservaError):
            self.assertTrue(issubclass(excepcion, SoftwareFJError))


if __name__ == "__main__":
    unittest.main()

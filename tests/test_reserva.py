"""
test_reserva.py
Pruebas de la clase Reserva y del CalculadorCostos.
Autor: Jefferson Stick Murillo Córdoba
Ejecutar desde la carpeta del proyecto: python -m unittest discover tests
"""

import unittest

from excepciones import CalculoError, EstadoReservaError, ReservaError
from modelos.reserva import EstadoReserva, Reserva
from modelos.sala import ReservaSala
from servicios_core.calculadora import CalculadorCostos


def crear_sala():
    """Sala del módulo Servicios: 100000 por hora."""
    return ReservaSala("S01", "Sala principal", 100000, 20)


class ClientePrueba:
    """Cliente falso, solo para crear reservas."""
    nombre = "Cliente de prueba"


class TestReserva(unittest.TestCase):
    """Pruebas de la clase Reserva."""

    def setUp(self):
        """Crea un cliente, un servicio y una reserva para cada prueba."""
        self.reserva = Reserva(ClientePrueba(), crear_sala(), 2)

    def test_empieza_pendiente(self):
        """Verifica que una reserva nueva empieza PENDIENTE."""
        self.assertEqual(self.reserva.estado, EstadoReserva.PENDIENTE)
        self.assertEqual(self.reserva.estado, "PENDIENTE")

    def test_flujo_completo(self):
        """Verifica el flujo completo: confirmar y procesar."""
        self.reserva.confirmar()
        self.assertEqual(self.reserva.estado, EstadoReserva.CONFIRMADA)
        self.assertEqual(self.reserva.procesar(), 200000)
        self.assertEqual(self.reserva.estado, EstadoReserva.PROCESADA)

    def test_cancelar_pendiente(self):
        """Verifica que se puede cancelar una reserva pendiente."""
        self.reserva.cancelar()
        self.assertEqual(self.reserva.estado, EstadoReserva.CANCELADA)

    def test_cancelar_confirmada(self):
        """Verifica que se puede cancelar una reserva confirmada."""
        self.reserva.confirmar()
        self.reserva.cancelar()
        self.assertEqual(self.reserva.estado, EstadoReserva.CANCELADA)

    def test_cancelar_procesada_falla(self):
        """Verifica que no se cancela una reserva procesada."""
        self.reserva.confirmar()
        self.reserva.procesar()
        with self.assertRaises(EstadoReservaError):
            self.reserva.cancelar()

    def test_confirmar_dos_veces_falla(self):
        """Verifica que no se confirma dos veces."""
        self.reserva.confirmar()
        with self.assertRaises(EstadoReservaError):
            self.reserva.confirmar()

    def test_procesar_pendiente_falla(self):
        """Verifica que no se procesa una reserva pendiente."""
        with self.assertRaises(EstadoReservaError):
            self.reserva.procesar()

    def test_procesar_cancelada_falla(self):
        """Verifica que no se procesa una reserva cancelada."""
        self.reserva.cancelar()
        with self.assertRaises(EstadoReservaError):
            self.reserva.procesar()

    def test_duracion_cero_falla(self):
        """Verifica que una duración cero falla."""
        with self.assertRaises(ReservaError):
            Reserva(ClientePrueba(), crear_sala(), 0)

    def test_duracion_negativa_falla(self):
        """Verifica que una duración negativa falla."""
        with self.assertRaises(ReservaError):
            Reserva(ClientePrueba(), crear_sala(), -3)

    def test_duracion_texto_falla(self):
        """Verifica que una duración en texto falla."""
        with self.assertRaises(ReservaError):
            Reserva(ClientePrueba(), crear_sala(), "dos")

    def test_sin_cliente_falla(self):
        """Verifica que una reserva sin cliente falla."""
        with self.assertRaises(ReservaError):
            Reserva(None, crear_sala(), 2)

    def test_procesar_con_descuento_malo_falla(self):
        """Verifica que un descuento fuera de rango falla al procesar."""
        self.reserva.confirmar()
        with self.assertRaises(CalculoError):
            self.reserva.procesar(descuento=1.5)
        self.assertEqual(self.reserva.estado, EstadoReserva.CONFIRMADA)


class TestCalculadorCostos(unittest.TestCase):
    """Pruebas del CalculadorCostos."""

    def setUp(self):
        """Crea un servicio de prueba para la calculadora."""
        self.servicio = crear_sala()

    def test_sin_nada_extra(self):
        """Verifica el costo sin impuesto ni descuento."""
        self.assertEqual(CalculadorCostos.costo(self.servicio, 1), 100000)

    def test_con_impuesto(self):
        """Verifica el costo con impuesto."""
        self.assertEqual(CalculadorCostos.costo(self.servicio, 1, impuesto=0.19), 119000)

    def test_con_descuento(self):
        """Verifica el costo con descuento."""
        self.assertEqual(CalculadorCostos.costo(self.servicio, 1, descuento=0.10), 90000)

    def test_con_ambos(self):
        """Verifica el costo con impuesto y descuento."""
        # 100000 - 10 % = 90000, + 19 % = 107100
        self.assertEqual(CalculadorCostos.costo(self.servicio, 1, impuesto=0.19, descuento=0.10), 107100)

    def test_impuesto_fuera_de_rango(self):
        """Verifica que un impuesto fuera de rango falla."""
        with self.assertRaises(CalculoError):
            CalculadorCostos.costo(self.servicio, 1, impuesto=1.5)

    def test_descuento_negativo(self):
        """Verifica que un descuento negativo falla."""
        with self.assertRaises(CalculoError):
            CalculadorCostos.costo(self.servicio, 1, descuento=-0.1)

    def test_duracion_invalida_encadena_error(self):
        """Verifica que una duración inválida produce un error encadenado."""
        with self.assertRaises(CalculoError) as contexto:
            CalculadorCostos.costo(self.servicio, -2)
        self.assertIsNotNone(contexto.exception.__cause__)

    def test_impuesto_texto(self):
        """Verifica que un impuesto en texto falla."""
        with self.assertRaises(CalculoError):
            CalculadorCostos.costo(self.servicio, 1, impuesto="19%")


if __name__ == "__main__":
    unittest.main()

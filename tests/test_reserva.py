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

    def setUp(self):
        self.reserva = Reserva(ClientePrueba(), crear_sala(), 2)

    def test_empieza_pendiente(self):
        self.assertEqual(self.reserva.estado, EstadoReserva.PENDIENTE)
        self.assertEqual(self.reserva.estado, "PENDIENTE")

    def test_flujo_completo(self):
        self.reserva.confirmar()
        self.assertEqual(self.reserva.estado, EstadoReserva.CONFIRMADA)
        self.assertEqual(self.reserva.procesar(), 200000)
        self.assertEqual(self.reserva.estado, EstadoReserva.PROCESADA)

    def test_cancelar_pendiente(self):
        self.reserva.cancelar()
        self.assertEqual(self.reserva.estado, EstadoReserva.CANCELADA)

    def test_cancelar_confirmada(self):
        self.reserva.confirmar()
        self.reserva.cancelar()
        self.assertEqual(self.reserva.estado, EstadoReserva.CANCELADA)

    def test_cancelar_procesada_falla(self):
        self.reserva.confirmar()
        self.reserva.procesar()
        with self.assertRaises(EstadoReservaError):
            self.reserva.cancelar()

    def test_confirmar_dos_veces_falla(self):
        self.reserva.confirmar()
        with self.assertRaises(EstadoReservaError):
            self.reserva.confirmar()

    def test_procesar_pendiente_falla(self):
        with self.assertRaises(EstadoReservaError):
            self.reserva.procesar()

    def test_procesar_cancelada_falla(self):
        self.reserva.cancelar()
        with self.assertRaises(EstadoReservaError):
            self.reserva.procesar()

    def test_duracion_cero_falla(self):
        with self.assertRaises(ReservaError):
            Reserva(ClientePrueba(), crear_sala(), 0)

    def test_duracion_negativa_falla(self):
        with self.assertRaises(ReservaError):
            Reserva(ClientePrueba(), crear_sala(), -3)

    def test_duracion_texto_falla(self):
        with self.assertRaises(ReservaError):
            Reserva(ClientePrueba(), crear_sala(), "dos")

    def test_sin_cliente_falla(self):
        with self.assertRaises(ReservaError):
            Reserva(None, crear_sala(), 2)

    def test_procesar_con_descuento_malo_falla(self):
        self.reserva.confirmar()
        with self.assertRaises(CalculoError):
            self.reserva.procesar(descuento=1.5)
        self.assertEqual(self.reserva.estado, EstadoReserva.CONFIRMADA)


class TestCalculadorCostos(unittest.TestCase):

    def setUp(self):
        self.servicio = crear_sala()

    def test_sin_nada_extra(self):
        self.assertEqual(CalculadorCostos.costo(self.servicio, 1), 100000)

    def test_con_impuesto(self):
        self.assertEqual(CalculadorCostos.costo(self.servicio, 1, impuesto=0.19), 119000)

    def test_con_descuento(self):
        self.assertEqual(CalculadorCostos.costo(self.servicio, 1, descuento=0.10), 90000)

    def test_con_ambos(self):
        # 100000 - 10 % = 90000, + 19 % = 107100
        self.assertEqual(CalculadorCostos.costo(self.servicio, 1, impuesto=0.19, descuento=0.10), 107100)

    def test_impuesto_fuera_de_rango(self):
        with self.assertRaises(CalculoError):
            CalculadorCostos.costo(self.servicio, 1, impuesto=1.5)

    def test_descuento_negativo(self):
        with self.assertRaises(CalculoError):
            CalculadorCostos.costo(self.servicio, 1, descuento=-0.1)

    def test_duracion_invalida_encadena_error(self):
        with self.assertRaises(CalculoError) as contexto:
            CalculadorCostos.costo(self.servicio, -2)
        self.assertIsNotNone(contexto.exception.__cause__)

    def test_impuesto_texto(self):
        with self.assertRaises(CalculoError):
            CalculadorCostos.costo(self.servicio, 1, impuesto="19%")


if __name__ == "__main__":
    unittest.main()

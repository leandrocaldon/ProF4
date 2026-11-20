"""Pruebas de los servicios: sala, alquiler de equipos y asesoría."""

import unittest

from modelos.sala import ReservaSala
from modelos.equipo import AlquilerEquipo
from modelos.asesoria import Asesoria
from excepciones import ServicioInvalidoError


class TestServicios(unittest.TestCase):
    """Pruebas de los servicios concretos."""

    def test_reserva_sala(self):
        """Verifica el costo de una reserva de sala."""
        sala = ReservaSala("S01", "Sala principal", 100, 20)

        self.assertEqual(sala.calcular_costo(2), 200)
        self.assertIn("Sala principal", sala.describir())

    def test_sala_capacidad_invalida(self):
        """Verifica que una capacidad inválida falla."""
        with self.assertRaises(ServicioInvalidoError):
            ReservaSala("S02", "Sala pequeña", 100, 0)

    def test_alquiler_equipo(self):
        """Verifica el costo de un alquiler de equipos."""
        equipo = AlquilerEquipo("E01", "Computador", 50, 3)

        self.assertEqual(equipo.calcular_costo(2), 300)
        self.assertIn("Computador", equipo.describir())

    def test_equipo_cantidad_invalida(self):
        """Verifica que una cantidad de equipos inválida falla."""
        with self.assertRaises(ServicioInvalidoError):
            AlquilerEquipo("E02", "Proyector", 50, 0)

    def test_asesoria(self):
        """Verifica el costo de una asesoría."""
        asesoria = Asesoria("A01", "Asesoría informática", 100, "basico")

        self.assertEqual(asesoria.calcular_costo(2), 200)
        self.assertIn("Asesoría informática", asesoria.describir())

    def test_asesoria_nivel_invalido(self):
        """Verifica que un nivel de asesoría inválido falla."""
        with self.assertRaises(ServicioInvalidoError):
            Asesoria("A02", "Asesoría", 100, "experto")


if __name__ == "__main__":
    unittest.main()

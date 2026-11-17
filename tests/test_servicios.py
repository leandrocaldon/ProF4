import unittest

from modelos.sala import ReservaSala
from modelos.equipo import AlquilerEquipo
from modelos.asesoria import Asesoria
from excepciones import ServicioInvalidoError


class TestServicios(unittest.TestCase):

    def test_reserva_sala(self):
        sala = ReservaSala("S01", "Sala principal", 100, 20)

        self.assertEqual(sala.calcular_costo(2), 200)
        self.assertIn("Sala principal", sala.describir())

    def test_sala_capacidad_invalida(self):
        with self.assertRaises(ServicioInvalidoError):
            ReservaSala("S02", "Sala pequeña", 100, 0)

    def test_alquiler_equipo(self):
        equipo = AlquilerEquipo("E01", "Computador", 50, 3)

        self.assertEqual(equipo.calcular_costo(2), 300)
        self.assertIn("Computador", equipo.describir())

    def test_equipo_cantidad_invalida(self):
        with self.assertRaises(ServicioInvalidoError):
            AlquilerEquipo("E02", "Proyector", 50, 0)

    def test_asesoria(self):
        asesoria = Asesoria("A01", "Asesoría informática", 100, "basico")

        self.assertEqual(asesoria.calcular_costo(2), 200)
        self.assertIn("Asesoría informática", asesoria.describir())

    def test_asesoria_nivel_invalido(self):
        with self.assertRaises(ServicioInvalidoError):
            Asesoria("A02", "Asesoría", 100, "experto")


if __name__ == "__main__":
    unittest.main()

# Responsabilidades: Integrante – Módulo Clientes e Integrante – Módulo Servicios

---

## Integrante – Módulo Clientes

*Objetivo:* implementar la base de entidades y la clase `Cliente` con validaciones y datos encapsulados.

*Archivos:* `modelos/entidad.py`, `modelos/cliente.py`, `tests/test_cliente.py`.

*Tareas:*
1. **`Entidad`** (clase abstracta): atributo `id` (generado de forma única) y método abstracto `describir()`.
2. **`Cliente(Entidad)`**:
   - Atributos privados `__nombre`, `__documento`, `__email`, `__telefono`, expuestos solo mediante *properties*.
   - Validaciones en el constructor y en los setters: nombre no vacío, documento con formato válido, email con formato correcto, teléfono numérico.
   - Si un dato no es válido, lanzar `ClienteInvalidoError` (definida en `excepciones.py` por el Integrante 5; coordinar el nombre con él).
   - Implementar `describir()`.
3. **Tests** (`tests/test_cliente.py`): al menos un caso válido y uno inválido por cada validación.
4. **Docstrings** en todas las clases y métodos públicos.

*Entregable:* `Cliente` funcional con tests pasando, listo para que el Integrante 5 lo registre en `GestorSistema`.

---

## Integrante – Módulo Servicios

*Objetivo:* implementar la clase abstracta `Servicio` y tres servicios derivados, cada uno con su propio cálculo de costo y validación.

*Archivos:* `modelos/servicio.py`, `modelos/sala.py`, `modelos/equipo.py`, `modelos/asesoria.py`, `tests/test_servicios.py`.

*Tareas:*
1. **`Servicio(Entidad)`** (abstracta): atributos `nombre` y `tarifa_base` (validada como número positivo). Métodos abstractos `calcular_costo(duracion)`, `validar_parametros()` y `describir()`.
2. **`ReservaSala(Servicio)`**: costo por hora, con atributo `capacidad`.
3. **`AlquilerEquipo(Servicio)`**: costo por día, con atributo `cantidad_unidades`.
4. **`Asesoria(Servicio)`**: costo por sesión, con atributo `nivel_especializacion` (por ejemplo, básico, intermedio, avanzado, con un multiplicador distinto para cada nivel).
5. Cada derivada sobrescribe `calcular_costo`, `validar_parametros` y `describir` (esto demuestra el polimorfismo).
6. Las validaciones lanzan `ServicioInvalidoError`. Al convertir texto a número, usar `raise ServicioInvalidoError(...) from e` para cumplir el encadenamiento de excepciones.
7. **Tests** (`tests/test_servicios.py`): un caso válido y uno inválido por servicio, y verificar que `calcular_costo` devuelve valores distintos según el tipo.

*Entregable:* tres servicios derivados probados, con costo, descripción y validación sobrescritos, listos para usar en `GestorSistema` y en `CalculadorCostos`.

---

## Puntos de coordinación

- Ambos dependen de `Entidad` y de `excepciones.py`. Conviene que el Integrante 5 suba `excepciones.py` pronto, o que el Integrante del módulo Clientes suba `entidad.py` primero, para evitar bloqueos.
- Ambos deben usar el mismo estilo de docstrings y nombres en español.
- Cada uno trabaja en su rama (`feature/clientes` y `feature/servicios`), y el Integrante 1 revisa los Pull Requests.

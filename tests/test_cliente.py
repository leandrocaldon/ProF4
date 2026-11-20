"""
Pruebas unitarias para la clase Cliente.
"""

import pytest
from uuid import uuid4

from modelos.cliente import Cliente
from excepciones import ClienteInvalidoError


def crear_cliente(documento=None):
    """Crea un cliente valido para realizar pruebas."""

    if documento is None:
        documento = str(uuid4().int % 1000000000).zfill(9)

    return Cliente(
        nombre="Sebastian",
        documento=documento,
        email="sebastian@gmail.com",
        telefono="3001234567"
    )


def test_cliente_valido():
    """Comprueba que se pueda crear un cliente correctamente."""

    cliente = crear_cliente()

    assert cliente.nombre == "Sebastian"
    assert cliente.documento is not None
    assert cliente.email == "sebastian@gmail.com"
    assert cliente.telefono == "3001234567"
    assert cliente.id is not None


def test_nombre_vacio():
    """Comprueba que no se permita un nombre vacio."""

    with pytest.raises(ClienteInvalidoError):
        crear_cliente().nombre = ""


def test_nombre_invalido_constructor():
    """Comprueba la validacion del nombre en el constructor."""

    with pytest.raises(ClienteInvalidoError):
        Cliente("", "123456789", "test@gmail.com", "3001234567")


def test_documento_formato_invalido():
    """Comprueba que el documento tenga un formato correcto."""

    with pytest.raises(ClienteInvalidoError):
        crear_cliente().documento = "ABC123"


def test_documento_duplicado():
    """Comprueba que no existan documentos duplicados."""

    documento = str(uuid4().int % 1000000000).zfill(9)

    crear_cliente(documento)

    with pytest.raises(ClienteInvalidoError):
        crear_cliente(documento)


def test_email_invalido():
    """Comprueba que se rechace un correo incorrecto."""

    with pytest.raises(ClienteInvalidoError):
        crear_cliente().email = "correo-invalido"


def test_email_invalido_constructor():
    """Comprueba la validacion del correo en el constructor."""

    with pytest.raises(ClienteInvalidoError):
        Cliente("Sebastian", "123456789", "correo-mal", "3001234567")


def test_telefono_invalido():
    """Comprueba que el telefono solo contenga numeros."""

    with pytest.raises(ClienteInvalidoError):
        crear_cliente().telefono = "ABC12345"


def test_telefono_invalido_constructor():
    """Comprueba la validacion del telefono en el constructor."""

    with pytest.raises(ClienteInvalidoError):
        Cliente("Sebastian", "123456789", "test@gmail.com", "ABC123")


def test_describir():
    """Comprueba el funcionamiento del metodo describir."""

    cliente = crear_cliente()

    resultado = cliente.describir()

    assert "Sebastian" in resultado
    assert cliente.documento in resultado


def test_documento_modificado():
    """Comprueba que se pueda actualizar un documento valido."""

    cliente = crear_cliente()

    nuevo_documento = str(uuid4().int % 1000000000).zfill(9)

    cliente.documento = nuevo_documento

    assert cliente.documento == nuevo_documento

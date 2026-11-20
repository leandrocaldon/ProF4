from abc import ABC, abstractmethod
from uuid import uuid4


class Entidad(ABC):

    def __init__(self, id=None):
        if id is None:
            self.__id = str(uuid4())
        else:
            self.__id = str(id)

    @property
    def id(self):
        return self.__id

    @abstractmethod
    def describir(self):
        pass

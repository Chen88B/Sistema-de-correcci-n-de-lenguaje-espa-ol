import abc
class ReglaBase(abc.ABC):
    def __init__(self, nombre,descripcion, prioridad):
        self._nombre = nombre
        self._descripcion = descripcion
        self._prioridad = prioridad

    """Metodo que va a devolver un lista de errores"""
    @abc.abstractmethod
    def aplicar(self,tokens_info):
        pass
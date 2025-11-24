class Error:
    def __init__(self, tipo, mensaje, token_inicia, token_final, prioridad,sugerencia,origen,idx_char_inicio=None, idx_char_final=None, correccion_automatica=None):
        self._tipo = tipo
        self._mensaje = mensaje
        self._token_inicia = token_inicia
        self._token_final = token_final
        self._prioridad = prioridad
        self._sugerencia = sugerencia
        self._origen = origen
        self._idx_char_inicio = idx_char_inicio
        self._idx_char_final = idx_char_final
        self._correccion_automatica= correccion_automatica

    """Metodo get de la clase"""
    @property
    def tipo(self):
        return self._tipo

    @property
    def mensaje(self):
        return self._mensaje

    @property
    def token_inicia(self):
        return self._token_inicia

    @property
    def token_final(self):
        return self._token_final

    @property
    def prioridad(self):
        return self._prioridad

    @property
    def sugerencia(self):
        return self._sugerencia

    @property
    def origen(self):
        return self._origen

    @property
    def idx_char_inicio(self):
        return self._idx_char_inicio

    @property
    def idx_char_final(self):
        return self._idx_char_final

    @property
    def correccion_automatica(self):
        return self._correccion_automatica

    def convertir_diccionario(self):
        return {
            "tipo": self._tipo,
            "mensaje": self._mensaje,
            "token_inicia": self._token_inicia,
            "token_final": self._token_final,
            "prioridad": self._prioridad,
            "sugerencia": self._sugerencia,
            "origen": self._origen,
            "cadena_inicio": self._idx_char_inicio,
            "cadena_final": self._idx_char_final,
            "correccion_automatica": self._correccion_automatica
        }

    def representar(self):
        return (f"Error(tipo={self._tipo}, mensaje={self._mensaje}, "
                f"rango=({self._token_inicia}, {self._token_final}, "
                f"prioridad={self._prioridad}"
                f"sugerencia={self.sugerencia}"
                f"origen={self.origen}"
                f"cadena_inicio={self._idx_char_inicio}, "
                f"cadena_final={self._idx_char_final}, "
                f"correccion_automatica={self._correccion_automatica})")

from reglas.regla_base import ReglaBase
from datos.error import Error
class PalabraProhibida(ReglaBase):
    def __init__(self,palabras_prohibidas=None):
        if palabras_prohibidas is None:
            palabras_prohibidas = {"puta", "mierda", "joder", "chingar"}

        self._palabras = set(palabras_prohibidas)
        super().__init__(nombre="Palabra prohibida",descripcion="Detecta palabras ofensivas o no permitidas en el texto.",prioridad=100)

    def aplicar(self, tokens_info):
        errores = []

        for token in tokens_info:
            # Revisamos tanto el texto exacto como el lema (raíz)
            if token.texto.lower() in self._palabras or token.base.lower() in self._palabras:
                # Generamos una censura del mismo largo que la palabra
                censura = "*" * len(token.texto)

                errores.append(
                    Error(
                        tipo="Palabra_prohibida",
                        mensaje=f"Lenguaje inapropiado detectado: '{token.texto}'.",
                        token_inicia=token.posicion,
                        token_final=token.posicion,
                        prioridad=self._prioridad,
                        sugerencia="Elimina o sustituye esta palabra.",
                        origen="Regla manual",
                        idx_char_inicio=token.idx_inicio,
                        idx_char_final=token.idx_final,
                        correccion_automatica=censura  # Ejemplo: "mierda" -> "******"
                    )
                )

        return errores
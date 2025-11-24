from reglas.regla_base import ReglaBase
from datos.error import Error
class RepeticionInnecesariaDePalabra(ReglaBase):
    def __init__(self):
        super().__init__(nombre="Repetición innecesaria de palabra",descripcion="Detecta si la misma palabra aparece repetida consecutivamente sin necesidad.",prioridad=40)

    def aplicar(self, tokens_info):
        errores = []

        for i in range(len(tokens_info) - 1):
            actual = tokens_info[i]
            siguiente = tokens_info[i + 1]

            # Ignoramos si son signos de puntuación (opcional, pero recomendado)
            if actual.categoria == "PUNCT":
                continue

            # Normalizamos para comparar
            if actual.texto.lower() == siguiente.texto.lower():
                errores.append(
                    Error(
                        tipo="Repetición_innecesaria",
                        mensaje=f"La palabra '{actual.texto}' aparece repetida sin necesidad.",
                        token_inicia=actual.posicion,
                        token_final=siguiente.posicion,
                        prioridad=self._prioridad,
                        sugerencia=f"Elimina una aparición.",
                        origen="Regla manual",
                        idx_char_inicio=actual.idx_inicio,
                        idx_char_final=siguiente.idx_final,
                        correccion_automatica=actual.texto
                    )
                )

        return errores
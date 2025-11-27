from reglas.regla_base import ReglaBase
from datos.error import Error
class RepeticionInnecesariaDePalabra(ReglaBase):
    def __init__(self):
        super().__init__(nombre="Repetición innecesaria de palabra",descripcion="Detecta si la misma palabra aparece repetida consecutivamente sin necesidad.",prioridad=95)

    def aplicar(self, tokens_info):
        errores = []

        for i in range(len(tokens_info) - 1):
            actual = tokens_info[i]
            siguiente = tokens_info[i + 1]

            # 1. Ignorar Puntuación (PUNCT) y Símbolos (SYM)
            # Esto evita detectar "..." o "***" o "???" como errores de repetición.
            if actual.categoria in ("PUNCT", "SYM"):
                continue

            # 2. Ignorar explícitamente asteriscos (por si SpaCy los marca como 'X' u 'Other')
            if "*" in actual.texto:
                continue

            # 3. Ignorar números (opcional, por si repiten "20 20")
            if actual.es_numero:
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
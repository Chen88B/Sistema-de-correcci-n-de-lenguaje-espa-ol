from reglas.regla_base import ReglaBase
from datos.error import Error
class RedundanciaDepreposicion(ReglaBase):
    def __init__(self):
        super().__init__(nombre="Redundancia de preposición",descripcion="Detecta la repetición o uso innecesario de dos preposiciones consecutivas.",prioridad=95)
        # Conjuntos de combinaciones redundantes
        self.combinaciones_invalidas = {
            ("a", "a"),
            ("de", "de"),
            ("en", "en"),
            ("para", "para"),
            ("a", "para"),
            ("para", "a"),
        }

    def aplicar(self, tokens_info):
        errores = []

        for i in range(len(tokens_info) - 1):
            t1 = tokens_info[i]
            t2 = tokens_info[i + 1]

            # Solo analizamos Preposiciones consecutivas
            if t1.categoria != "ADP" or t2.categoria != "ADP":
                continue

            pair = (t1.texto.lower(), t2.texto.lower())

            # Verificamos si está en nuestra lista prohibida O si son idénticas
            es_invalido = pair in self.combinaciones_invalidas or t1.texto.lower() == t2.texto.lower()

            if es_invalido:
                correccion = None
                sugerencia_txt = "Elimina una de las preposiciones."

                # Si son idénticas, la corrección segura es dejar solo una
                if t1.texto.lower() == t2.texto.lower():
                    correccion = t1.texto  # Reemplaza "de de" por "de"

                # Si es "para a" -> suele ser corrección a "para" (coloquialismo "voy para a casa")
                elif pair == ("para", "a"):
                    correccion = "para"

                errores.append(Error(
                    tipo="Redundancia_preposicion",
                    mensaje=f"Uso redundante o incorrecto: '{t1.texto} {t2.texto}'.",
                    token_inicia=t1.posicion,
                    token_final=t2.posicion,
                    prioridad=self._prioridad,
                    sugerencia=sugerencia_txt,
                    origen="Regla manual",
                    idx_char_inicio=t1.idx_inicio,
                    idx_char_final=t2.idx_final,
                    correccion_automatica=correccion
                ))

        return errores
from reglas.regla_base import ReglaBase
from datos.error import Error
class DobleNegacionIncorrecta(ReglaBase):
    def __init__(self):
        super().__init__(nombre="Doble negación incorrecta",descripcion="Detecta uso indebido de negaciones incompatibles (nunca no, jamás no, no no...).",prioridad=65)
        # Negadores incompatibles con “no”
        self.negadores_fuertes = {
            "nunca", "jamás", "nadie", "ninguno", "ninguna", "nada"
        }

    def aplicar(self, tokens_info):
        errores = []
        cantidad = len(tokens_info)

        for i, token in enumerate(tokens_info):
            palabra = token.base.lower()

            # Necesitamos mirar el siguiente token
            if i + 1 >= cantidad:
                break

            siguiente = tokens_info[i + 1]
            palabra_sig = siguiente.base.lower()

            # 1) Detectar 'no no'
            if palabra == "no" and palabra_sig == "no":
                errores.append(Error(
                    tipo="doble_negacion_no_no",
                    mensaje="Uso incorrecto de 'no no'.",
                    token_inicia=token.posicion,
                    token_final=siguiente.posicion,
                    prioridad=self._prioridad,
                    sugerencia="Elimina una de las negaciones.",
                    origen="Regla manual",
                    idx_char_inicio=token.idx_inicio,
                    idx_char_final=siguiente.idx_final,
                    correccion_automatica="no"  # Reemplaza "no no" por "no"
                ))

            # 2) Detectar negador fuerte + "no" (ej: "nunca no")
            elif palabra in self.negadores_fuertes and palabra_sig == "no":
                errores.append(Error(
                    tipo="doble_negacion_fuerte_no",
                    mensaje=f"La expresión '{token.texto} no' es redundante.",
                    token_inicia=token.posicion,
                    token_final=siguiente.posicion,
                    prioridad=self._prioridad,
                    sugerencia=f"Deja solo '{token.texto}'.",
                    origen="Regla manual",
                    idx_char_inicio=token.idx_inicio,
                    idx_char_final=siguiente.idx_final,
                    correccion_automatica=token.texto  # Reemplaza "nunca no" por "nunca"
                ))

        return errores
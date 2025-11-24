from reglas.regla_base import ReglaBase
from datos.error import Error
class MayusculaAInicio(ReglaBase):
    def __init__(self):
        super().__init__(nombre="Mayúscula al inicio",descripcion="Verifica que el texto comience con una letra en mayúscula.",prioridad=5)

    def aplicar(self, tokens_info):
        errores = []
        if not tokens_info:
            return errores

        primer_token = None
        # Buscamos el primer token que sea una palabra real
        for token in tokens_info:
            if token.categoria in ("PUNCT", "SPACE", "SYM"):
                continue
            if token.es_email or token.es_url or token.es_numero:
                continue
            primer_token = token
            break

        if primer_token is None:
            return errores

        # Verificar si empieza con minúscula
        if not primer_token.texto[0].isupper():
            # Corrección: Primera letra mayúscula + resto igual
            correccion = primer_token.texto[0].upper() + primer_token.texto[1:]

            errores.append(
                Error(
                    tipo="MayusculaInicio",
                    mensaje=f"La oración debe empezar con mayúscula: '{primer_token.texto}'",
                    token_inicia=primer_token.posicion,
                    token_final=primer_token.posicion,
                    prioridad=self._prioridad,
                    sugerencia=f"Cambiar a '{correccion}'",
                    origen="Regla manual",
                    # --- NUEVOS CAMPOS ---
                    idx_char_inicio=primer_token.idx_inicio,
                    idx_char_final=primer_token.idx_final,
                    correccion_automatica=correccion
                )
            )

        return errores
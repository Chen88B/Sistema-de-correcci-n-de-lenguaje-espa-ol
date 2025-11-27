from reglas.regla_base import ReglaBase
from datos.error import Error

class SinVerbolPrincipal(ReglaBase):
    def __init__(self):
        super().__init__(
            nombre="Oración sin verbo principal",
            descripcion="Detecta si la oración carece por completo de un verbo principal.",
            prioridad=10
        )

    def aplicar(self, tokens_info):
        errores = []

        if not tokens_info:
            return errores

        # Detectar verbos conjugados o auxiliares
        hay_verbo = any(t.categoria in ("VERB", "AUX") for t in tokens_info)

        if hay_verbo:
            return errores

        # Evitar falsos positivos en frases muy cortas (títulos, exclamaciones)
        # a menos que tengan un sustantivo claro
        contiene_sustantivo = any(t.categoria == "NOUN" for t in tokens_info)
        if len(tokens_info) <= 2 and not contiene_sustantivo:
            return errores

        # Marcamos toda la oración como problemática
        token_inicial = tokens_info[0]
        token_final = tokens_info[-1]

        errores.append(
            Error(
                tipo="Oracion_sin_verbo_principal",
                mensaje="La oración no contiene un verbo principal conjugado.",
                token_inicia=token_inicial.posicion,
                token_final=token_final.posicion,
                prioridad=self._prioridad,
                sugerencia="Agrega un verbo para completar la idea.",
                origen="Regla manual",
                idx_char_inicio=token_inicial.idx_inicio,
                idx_char_final=token_final.idx_final,
                correccion_automatica=None # Imposible corregir automáticamente
            )
        )

        return errores
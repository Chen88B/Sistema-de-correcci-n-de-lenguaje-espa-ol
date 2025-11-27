from reglas.regla_base import ReglaBase
from datos.error import Error


class TildeMonosilaba(ReglaBase):
    def __init__(self):
        super().__init__(
            nombre="Tilde en monosílabos",
            descripcion="Detecta usos incorrectos de la tilde diacrítica analizando el contexto.",
            prioridad=30
        )

    def aplicar(self, tokens_info):
        errores = []
        cantidad = len(tokens_info)

        for i, token in enumerate(tokens_info):
            texto_original = token.texto
            palabra_lower = token.texto.lower()
            categoria = token.categoria

            prev_token = tokens_info[i - 1] if i > 0 else None
            next_token = tokens_info[i + 1] if i < cantidad - 1 else None

            correccion_base = None  # Guardamos la palabra en minúscula (tú, el, mí...)
            mensaje = ""

            # --- 1. CASO: TU / TÚ ---
            if palabra_lower in ["tu", "tú"]:
                es_pronombre = False
                if next_token and next_token.categoria in ["VERB", "AUX"]:
                    es_pronombre = True
                elif categoria == "PRON":
                    es_pronombre = True

                # Decidimos qué debería ser (lógica pura, sin mirar mayúsculas aún)
                if es_pronombre:
                    correccion_base = "tú"
                    mensaje = "Va seguido de un verbo, funciona como sujeto."
                else:
                    if next_token and next_token.categoria in ["NOUN", "PROPN"]:
                        correccion_base = "tu"
                        mensaje = "Va seguido de un sustantivo, es posesivo."

            # --- 2. CASO: EL / ÉL ---
            elif palabra_lower in ["el", "él"]:
                es_pronombre = False
                if next_token and next_token.categoria in ["VERB", "AUX"]:
                    es_pronombre = True
                elif categoria == "PRON":
                    es_pronombre = True

                if es_pronombre:
                    correccion_base = "él"
                    mensaje = "Funciona como pronombre personal."
                else:
                    if next_token and next_token.categoria == "NOUN":
                        correccion_base = "el"
                        mensaje = "Funciona como artículo determinado."

            # --- 3. CASO: MI / MÍ ---
            elif palabra_lower in ["mi", "mí"]:
                lleva_tilde = False
                if prev_token and prev_token.categoria == "ADP":
                    lleva_tilde = True
                elif next_token and next_token.categoria == "PUNCT":
                    lleva_tilde = True

                if lleva_tilde:
                    correccion_base = "mí"
                    mensaje = "Después de preposición es pronombre."
                else:
                    if next_token and next_token.categoria == "NOUN":
                        correccion_base = "mi"
                        mensaje = "Acompaña a un sustantivo, es posesivo."

            # --- 4. CASO: TE / TÉ ---
            elif palabra_lower in ["te", "té"]:
                es_bebida = False
                if prev_token and prev_token.categoria in ["DET", "POS"]:
                    es_bebida = True
                elif categoria == "NOUN":
                    es_bebida = True

                if es_bebida:
                    correccion_base = "té"
                    mensaje = "Se refiere a la bebida."
                else:
                    correccion_base = "te"
                    mensaje = "Es pronombre átono."

            # --- 5. CASO: SI / SÍ ---
            elif palabra_lower in ["si", "sí"]:
                lleva_tilde = False
                if categoria in ["ADV", "PRON"]:
                    lleva_tilde = True
                elif next_token and next_token.texto == ",":
                    lleva_tilde = True

                if lleva_tilde:
                    correccion_base = "sí"
                    mensaje = "Es afirmación."
                else:
                    if categoria == "SCONJ":
                        correccion_base = "si"
                        mensaje = "Es condicional."

            if correccion_base:
                correccion_final = correccion_base

                # 1. Aplicar Mayúscula si el original la tenía
                if token.texto[0].isupper():
                    correccion_final = correccion_base.capitalize()

                # 2. VERIFICACIÓN FINAL CRUCIAL:
                # Si la palabra calculada es IDÉNTICA a la original, NO HACEMOS NADA.
                if correccion_final == token.texto:
                    continue  # Saltamos al siguiente token, no hay error.

                # Si llegamos aquí, es porque son diferentes (ej: "Tu" != "Tú")
                errores.append(Error(
                    tipo="Tilde_diacritica",
                    mensaje=f"Uso de tilde: {mensaje}",
                    token_inicia=token.posicion,
                    token_final=token.posicion,
                    prioridad=self._prioridad,
                    sugerencia=f"Cambiar a '{correccion_final}'.",
                    origen="Regla manual",
                    idx_char_inicio=token.idx_inicio,
                    idx_char_final=token.idx_final,
                    correccion_automatica=correccion_final
                ))

        return errores
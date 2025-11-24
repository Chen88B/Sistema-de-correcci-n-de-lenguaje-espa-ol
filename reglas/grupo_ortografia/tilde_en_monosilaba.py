from reglas.regla_base import ReglaBase
from datos.error import Error
class TildeMonosilaba(ReglaBase):
    def __init__(self):
        super().__init__(nombre="Tilde en monosílabos",descripcion="Detecta usos incorrectos de la tilde diacrítica en palabras monosílabas.",prioridad=25 )

    def aplicar(self, tokens_info):
        errores = []

        for token in tokens_info:
            texto_original = token.texto
            palabra_lower = token.texto.lower()
            categoria = token.categoria  # DET, PRON, ADV, VERB, etc.

            correccion = None
            mensaje = ""

            # Analizamos caso por caso usando la lógica gramatical

            # --- CASO: EL / ÉL ---
            if palabra_lower in ["el", "él"]:
                # "él" es PRONOMBRE (él corre), "el" es DETERMINANTE (el coche)
                if categoria == "PRON" and texto_original != "él":
                    correccion = "él"
                    mensaje = "Como pronombre personal, debe llevar tilde."
                elif categoria == "DET" and texto_original == "él":
                    correccion = "el"
                    mensaje = "Como artículo, no debe llevar tilde."

            # --- CASO: TU / TÚ ---
            elif palabra_lower in ["tu", "tú"]:
                # "tú" es PRONOMBRE (tú eres), "tu" es DETERMINANTE (tu casa)
                if categoria == "PRON" and texto_original != "tú":
                    correccion = "tú"
                    mensaje = "Como pronombre personal, debe llevar tilde."
                elif categoria == "DET" and texto_original == "tú":
                    correccion = "tu"
                    mensaje = "Como posesivo, no debe llevar tilde."

            # --- CASO: MI / MÍ ---
            elif palabra_lower in ["mi", "mí"]:
                # "mí" es PRONOMBRE (para mí), "mi" es DETERMINANTE (mi gato)
                if categoria == "PRON" and texto_original != "mí":
                    correccion = "mí"
                    mensaje = "Como pronombre personal, debe llevar tilde."
                elif categoria == "DET" and texto_original == "mí":
                    correccion = "mi"
                    mensaje = "Como posesivo, no debe llevar tilde."

            # --- CASO: SI / SÍ ---
            elif palabra_lower in ["si", "sí"]:
                # "sí" es ADVERBIO/PRON (dijo que sí), "si" es CONJUNCION (si llueve)
                # Nota: SCONJ es conjunción subordinante
                if categoria in ["ADV", "PRON"] and texto_original != "sí":
                    correccion = "sí"
                    mensaje = "Como afirmación o pronombre, debe llevar tilde."
                elif categoria == "SCONJ" and texto_original == "sí":
                    correccion = "si"
                    mensaje = "Como condicional, no debe llevar tilde."

            # --- CASO: SE / SÉ ---
            elif palabra_lower in ["se", "sé"]:
                # "sé" es VERBO (ser/saber), "se" es PRONOMBRE
                if categoria == "VERB" and texto_original != "sé":
                    correccion = "sé"
                    mensaje = "Del verbo saber o ser, debe llevar tilde."
                elif categoria == "PRON" and texto_original == "sé":
                    correccion = "se"
                    mensaje = "Como pronombre, no debe llevar tilde."

            # --- GENERAR ERROR SI HAY CORRECCIÓN ---
            if correccion:
                # Respetar mayúscula inicial si la tenía
                if token.texto[0].isupper():
                    correccion = correccion.capitalize()

                errores.append(Error(
                    tipo="Tilde_diacritica",
                    mensaje=f"Uso incorrecto de tilde en '{token.texto}'. {mensaje}",
                    token_inicia=token.posicion,
                    token_final=token.posicion,
                    prioridad=self._prioridad,
                    sugerencia=f"Cambiar a '{correccion}'.",
                    origen="Regla manual",
                    idx_char_inicio=token.idx_inicio,
                    idx_char_final=token.idx_final,
                    correccion_automatica=correccion
                ))

        return errores

from reglas.regla_base import ReglaBase
from datos.error import Error
class ConcordanciaProfundoSujetoVerbol(ReglaBase):
    def __init__(self):
        super().__init__(nombre="Concordancia Sujeto–Verbo",descripcion="Verifica que el sujeto y el verbo concuerden en número y persona.",prioridad=90)

    def aplicar(self, tokens_info):
        errores = []
        for sujeto in tokens_info:
            if sujeto.depedencia not in ("nsubj", "nsubj:pass"):
                continue

            try:
                verbo = tokens_info[sujeto.cabeza_indice]
            except IndexError:
                continue

            if verbo.categoria not in ("VERB", "AUX"):
                continue

            # --- EXTRACCIÓN Y NORMALIZACIÓN ---

            # 1. Número
            subj_num = sujeto.morfologicos.get("Number")
            verb_num = verbo.morfologicos.get("Number")

            # 2. Persona
            subj_per = sujeto.morfologicos.get("Person")
            verb_per = verbo.morfologicos.get("Person")

            # TRUCO: Si el sujeto es un Sustantivo o Nombre Propio y NO tiene persona,
            # asumimos que es 3ra persona.
            if not subj_per and sujeto.categoria in ("NOUN", "PROPN"):
                subj_per = "3"

            # Si tras la normalización sigue faltando info, saltamos
            if not subj_num or not verb_num or not subj_per or not verb_per:
                continue

            # --- COMPARACIÓN ---
            if subj_num != verb_num or subj_per != verb_per:
                # Excepción común: "La gente" (Singular) vs "dicen" (Plural) -> Error gramatical pero común
                # Excepción: "Usted" (2da semántica, 3ra gramatical). SpaCy suele manejarlo bien como 3ra.

                errores.append(Error(
                    tipo="Concordancia_sujeto_verbo",
                    mensaje=f"Sujeto '{sujeto.texto}' ({subj_per}ª {subj_num}) no concuerda con verbo '{verbo.texto}' ({verb_per}ª {verb_num}).",
                    token_inicia=sujeto.posicion,
                    token_final=verbo.posicion,
                    prioridad=self._prioridad,
                    sugerencia="Ajusta el número o la persona del verbo.",
                    origen="Regla manual",
                    idx_char_inicio=verbo.idx_inicio,
                    idx_char_final=verbo.idx_final,
                    correccion_automatica=None
                ))

        return errores


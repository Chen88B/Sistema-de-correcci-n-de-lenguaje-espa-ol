from reglas.regla_base import ReglaBase
from datos.error import Error

class ConcordanciaEntreSustantivoAdjectivo(ReglaBase):
    def __init__(self):
        super().__init__(
            nombre="Concordancia Sustantivo–Adjetivo",
            descripcion="Detecta discordancias de género o número entre un sustantivo y un adjetivo que lo modifica.",
            prioridad=75
        )

    def aplicar(self, tokens_info):
        errores = []

        for token in tokens_info:
            # Solo adjetivos que modifican directamente (amod)
            if token.categoria != "ADJ" or token.depedencia != "amod":
                continue

            try:
                sustantivo = tokens_info[token.cabeza_indice]
            except IndexError:
                continue

            if sustantivo.categoria not in ("NOUN", "PROPN"): # Incluimos nombres propios
                continue

            adj_gen = token.morfologicos.get("Gender")
            adj_num = token.morfologicos.get("Number")
            noun_gen = sustantivo.morfologicos.get("Gender")
            noun_num = sustantivo.morfologicos.get("Number")

            # Lógica segura: Si falta el rasgo en alguno, asumimos compatibilidad
            # (Ej: 'grande' no tiene género, sirve para masc y fem)
            error_gen = (adj_gen and noun_gen and adj_gen != noun_gen)
            error_num = (adj_num and noun_num and adj_num != noun_num)

            if error_gen or error_num:
                errores.append(Error(
                    tipo="Concordancia_adj_sust",
                    mensaje=f"El adjetivo '{token.texto}' no concuerda con '{sustantivo.texto}'.",
                    token_inicia=token.posicion,
                    token_final=sustantivo.posicion,
                    prioridad=self._prioridad,
                    sugerencia=f"Ajusta a '{noun_gen or ''} {noun_num or ''}'.",
                    origen="Regla manual",
                    idx_char_inicio=token.idx_inicio,
                    idx_char_final=token.idx_final,
                    correccion_automatica=None
                ))

        return errores
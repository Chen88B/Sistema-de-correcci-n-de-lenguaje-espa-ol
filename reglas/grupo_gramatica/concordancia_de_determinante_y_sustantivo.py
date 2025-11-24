from reglas.regla_base import ReglaBase
from datos.error import Error
class ConcordanciaDeDeterminanteYSustantivo(ReglaBase):
    def __init__(self):
        super().__init__(nombre="Concordancia determinante-sustantivo",descripcion="Detecta discordancias de género o número entre un determinante y el sustantivo que modifica.",prioridad=80)

    def aplicar(self, tokens_info):
        errores = []
        # Mapa simple para corrección automática de artículos definidos
        mapa_articulos = {
            ("Masc", "Sing"): "el", ("Masc", "Plur"): "los",
            ("Fem", "Sing"): "la", ("Fem", "Plur"): "las"
        }

        for token in tokens_info:
            if token.categoria != "DET": continue
            try:
                sustantivo = tokens_info[token.cabeza_indice]
            except IndexError:
                continue
            if sustantivo.categoria != "NOUN": continue

            det_gen = token.morfologicos.get("Gender")
            det_num = token.morfologicos.get("Number")
            noun_gen = sustantivo.morfologicos.get("Gender")
            noun_num = sustantivo.morfologicos.get("Number")

            match_genero = True
            if det_gen and noun_gen and det_gen != noun_gen:
                match_genero = False

            match_numero = True
            if det_num and noun_num and det_num != noun_num:
                match_numero = False

            if not match_genero or not match_numero:
                correccion = None
                # Si es un artículo definido (el/la...) intentamos sugerir el correcto
                if token.texto.lower() in ["el", "la", "los", "las"]:
                    clave = (noun_gen, noun_num)
                    if clave in mapa_articulos:
                        correccion = mapa_articulos[clave]
                        if token.texto[0].isupper(): correccion = correccion.capitalize()

                errores.append(Error(
                    tipo="Concordancia_det_sust",
                    mensaje=f"El determinante '{token.texto}' no concuerda con '{sustantivo.texto}'.",
                    token_inicia=token.posicion,
                    token_final=sustantivo.posicion,
                    prioridad=self._prioridad,
                    sugerencia="Ajusta género/número.",
                    origen="Regla manual",
                    idx_char_inicio=token.idx_inicio,
                    idx_char_final=token.idx_final,
                    correccion_automatica=correccion
                ))

        return errores

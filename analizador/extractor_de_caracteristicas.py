from datos.token_info import TokenInfo
from analizador.analizador_linguistico import AnalizadorLinguistico

class ExtractorDeCaracteristicas:
    def __init__(self, analizador: AnalizadorLinguistico):
        self._analizador = analizador

    """
    Metodo que convierte un texto en una lista de TokenInfo con información léxica y sintáctica.
    """
    def extraer_desde_texto(self, texto):
        doc = self._analizador.analizar(texto)
        tokens_info = []
        for i,token in enumerate(doc):
            # CALCULO DE INDICES (SpaCy nos da .idx, nosotros calculamos el final)
            start_char = token.idx
            end_char = token.idx + len(token.text)
            tokens_info.append(
                TokenInfo(
                    texto=token.text,
                    base=token.lemma_,
                    categoria=token.pos_,
                    depedencia=token.dep_,
                    cabeza=token.head.text,
                    cabeza_indice=token.head.i,
                    morfologicos=token.morph.to_dict(),
                    etiqueta = token.tag_,
                    posicion = token.i,
                    idx_inicio=start_char,
                    idx_final=end_char,
                    forma = token.shape_,
                    es_stop = token.is_stop,
                    es_numero = token.like_num,
                    es_email = token.like_email,
                    es_url = token.like_url
                )
            )

        return tokens_info

    """Desde aqui, todos son metodos get y set de los atributos"""
    @property
    def analizador(self):
        return self._analizador

    @analizador.setter
    def analizador(self, analizador):
        self._analizador = analizador


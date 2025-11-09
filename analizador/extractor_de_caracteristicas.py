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
        for token in doc:
            tokens_info.append(
                TokenInfo(
                    texto=token.text,
                    base=token.lemma_,
                    categoria=token.pos_,
                    depedencia=token.dep_,
                    cabeza=token.head.text,
                    morfologicos=token.morph.to_dict()
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


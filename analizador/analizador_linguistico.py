import spacy

class AnalizadorLinguistico:
    def __init__(self,modelo):
        self._modelo=modelo
        self._npl=spacy.load(modelo)

    """
    Metodos que devuelve un objeto que ya tiene todos los analisis de la palabras
    Parametros: texto:String
    Devuelve: doc:Doc
    """
    def analizar(self,texto):
        doc=self._npl(texto)
        return doc

    """Desde aqui, todos son metodos get y set de los atributos"""

    @property
    def modelo(self):
        return self._modelo

    @modelo.setter
    def modelo(self,modelo):
        self._modelo=modelo

    @property
    def npl(self):
        return self._npl

    @npl.setter
    def npl(self,npl):
        self._npl=npl
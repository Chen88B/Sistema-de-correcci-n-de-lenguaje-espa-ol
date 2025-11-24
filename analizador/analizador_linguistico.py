import spacy

class AnalizadorLinguistico:
    def __init__(self,modelo):
        self._modelo = modelo
        try:
            self._nlp = spacy.load(modelo)
        except OSError:
            print(f"Error: El modelo '{modelo}' no está instalado. Ejecuta: python -m spacy download {modelo}")
            raise

    """
    Metodos que devuelve un objeto que ya tiene todos los analisis de la palabras
    Parametros: texto:String
    Devuelve: doc:Doc
    """
    def analizar(self,texto):
        doc=self._nlp(texto)
        return doc

    """Desde aqui, todos son metodos get y set de los atributos"""

    @property
    def modelo(self):
        return self._modelo

    @modelo.setter
    def modelo(self,nuevo_modelo):
        if nuevo_modelo != self._modelo:
            print(f"Cambiando modelo a {nuevo_modelo}...")
            self._modelo = nuevo_modelo
            self._nlp = spacy.load(nuevo_modelo)

    @property
    def nlp(self):
        return self._nlp


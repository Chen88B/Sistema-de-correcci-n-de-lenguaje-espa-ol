import spacy.displacy
from analizador.analizador_linguistico import AnalizadorLinguistico

class VisualizadorDependencias:
    def __init__(self, analizador: AnalizadorLinguistico):
        self._analizador = analizador

    """
    Metodo que muestra visualmente las dependencias sintácticas usando spaCy.
    Parametros: texto:String
    Delvueve: Imprimir Informacion: void
    """
    def mostrar_dependencias(self, texto):
        doc = self._analizador.analizar(texto)
        spacy.displacy.serve(doc, style="dep")

    """Desde aqui, todos son metodos get y set de los atributos"""
    @property
    def analizador(self):
        return self._analizador

    @analizador.setter
    def analizador(self, analizador):
        self._analizador = analizador
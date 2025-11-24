import spacy.displacy
from pathlib import Path


class VisualizadorDependencias:
    def __init__(self, analizador):
        self._analizador = analizador

    def guardar_dependencias_html(self, texto: str, archivo_salida="dependencias.html"):
        """Genera un archivo HTML en lugar de bloquear el servidor."""
        doc = self._analizador.analizar(texto)
        html = spacy.displacy.render(doc, style="dep", page=True)

        output_path = Path(archivo_salida)
        output_path.write_text(html, encoding="utf-8")
        print(f"Visualización guardada en: {output_path.absolute()}")
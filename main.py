from analizador.analizador_linguistico import AnalizadorLinguistico
from analizador.extractor_de_caracteristicas import ExtractorDeCaracteristicas
from analizador.visualizador_de_depedencias import VisualizadorDependencias


#Configuración Inicial
MODELO_SPACY = "es_core_news_sm"
mi_analizador = AnalizadorLinguistico(MODELO_SPACY)

#Probar ExtractorDeCaracteristicas
print("--- Probando ExtractorDeCaracteristicas ---")
extractor = ExtractorDeCaracteristicas(mi_analizador)
texto_prueba = "Apple está buscando comprar una startup del Reino Unido."

lista_de_tokens = extractor.extraer_desde_texto(texto_prueba)

#Representa la informacion en Token
for token in lista_de_tokens:
    print(token.representar())

print("\n")

#Probar VisualizadorDependencias ---
print("--- Probando VisualizadorDependencias ---")
print("Iniciando servidor de displaCy en http://localhost:5000")
print("Presiona Ctrl+C en esta terminal para detener el servidor.")

visualizador = VisualizadorDependencias(mi_analizador)
visualizador.mostrar_dependencias(texto_prueba)

print("Servidor detenido.")
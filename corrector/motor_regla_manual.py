from analizador.extractor_de_caracteristicas import ExtractorDeCaracteristicas
class MotorReglaManual:
    def __init__(self,extractor:ExtractorDeCaracteristicas):
        self._extractor = extractor
        self._reglas=[]

    """Agrega UNA regla al motor"""
    def agregar_regla(self, regla):
        self._reglas.append(regla)

    """Agrega VARIAS reglas"""
    def agregar_reglas(self, reglas):
        self._reglas.extend(reglas)

    """
    1. Extrae tokens mediante el analizador
    2. Ejecuta todas las reglas manuales
    3. Ordena los errores 
    4. Devuelve la lista final
    """
    def analizar(self, texto):
        tokens = self._extractor.extraer_desde_texto(texto)

        errores_acumulados = []

        for regla in self._reglas:
            try:
                resultado = regla.aplicar(tokens)
            except Exception as e:
                print(f"[ERROR] La regla '{regla._nombre}' falló: {e}")
                continue

            if resultado:
                errores_acumulados.extend(resultado)

        errores_acumulados.sort(key=lambda x: x.idx_char_inicio)

        return errores_acumulados
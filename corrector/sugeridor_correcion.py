from datos.error import Error
class SugeridorCorrecion:
    def aplicar_sugerencia(self, texto, error: Error):
        # 1. Validar si hay corrección automática disponible
        if not error.correccion_automatica:
            return texto

        # 2. Obtener índices de caracteres (NO tokens)
        inicio = error.idx_char_inicio
        fin = error.idx_char_final

        # 3. Validaciones de seguridad para no romper el string
        if inicio < 0 or fin > len(texto) or inicio > fin:
            return texto

        # 4. Cirugía del texto
        texto_corregido = (
                texto[:inicio] +
                error.correccion_automatica +
                texto[fin:]
        )

        return texto_corregido

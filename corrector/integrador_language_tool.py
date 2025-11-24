from datos.error import Error


class IntegradorLanguageTool:
    def __init__(self, languagetool_client):
        self._lt = languagetool_client

    def analizar(self, texto):
        # LanguageTool devuelve una lista de objetos 'Match'
        matches = self._lt.check(texto)
        errores = []

        for match in matches:
            # 1. Obtener datos de forma segura (atributos del objeto)
            # Nota: language-tool-python usa atributos, no diccionario.
            offset = match.offset
            length = match.errorLength
            rule_id = match.ruleId
            mensaje = match.message
            replacements = match.replacements

            # 2. Calcular sugerencia y corrección automática
            sugerencia_texto = ""
            correccion_auto = None

            if replacements and len(replacements) > 0:
                # LT suele dar muchas opciones, tomamos la primera como la mejor
                mejor_opcion = replacements[0]
                sugerencia_texto = f"Cambiar por: '{mejor_opcion}'"
                correccion_auto = mejor_opcion

            # 3. Crear el objeto Error compatible con tu sistema
            errores.append(
                Error(
                    tipo=f"LT_{rule_id}",  # Prefijo LT para distinguir origen
                    mensaje=mensaje,
                    # Ponemos -1 o 0 para indicar que es externo.
                    token_inicia=-1,
                    token_final=-1,
                    prioridad=20,  # Prioridad baja (LT a veces falla en contexto)
                    sugerencia=sugerencia_texto,
                    origen="LanguageTool",
                    idx_char_inicio=offset,
                    idx_char_final=offset + length,
                    correccion_automatica=correccion_auto
                )
            )

        return errores
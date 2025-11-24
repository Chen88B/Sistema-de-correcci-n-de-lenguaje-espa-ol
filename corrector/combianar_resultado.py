class CombinadorDeResultados:
    def __init__(self):
        pass

    def combinar(self, errores_manual, errores_lt):
        todos_errores = errores_manual + errores_lt

        # 2. Ordenamos por PRIORIDAD descendente (Los más importantes primero)
        #    Si LanguageTool tiene prioridad 20, las reglas manuales (prioridad 40-100) ganarán.
        todos_errores.sort(key=lambda e: e.prioridad, reverse=True)

        # 3. Filtrado de Choques
        errores_limpios = []
        zonas_ocupadas = []  # Guardaremos tuplas (inicio, fin)

        for error in todos_errores:
            inicio = error.idx_char_inicio
            fin = error.idx_char_final

            es_valido = True

            # Comprobamos si este error choca con alguna zona ya aceptada (de mayor prioridad)
            for (ocupado_inicio, ocupado_fin) in zonas_ocupadas:
                # Lógica de solapamiento:
                # Si no (termina antes de empezar O empieza después de terminar) -> CHOCA
                if not (fin <= ocupado_inicio or inicio >= ocupado_fin):
                    es_valido = False
                    break  # Ya chocó, descartar

            if es_valido:
                errores_limpios.append(error)
                zonas_ocupadas.append((inicio, fin))
            else:
                print(f"Descartado por solapamiento: {error.mensaje}")

        return errores_limpios
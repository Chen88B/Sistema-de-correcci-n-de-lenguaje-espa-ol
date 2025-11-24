from reglas.regla_base import ReglaBase
from datos.error import Error
class ProblemaDePorque(ReglaBase):
    def __init__(self):
        super().__init__(nombre="Problema de porque",descripcion="Detecta usos incorrectos de las diferentes formas de 'porque'.",prioridad=60)

    def aplicar(self, tokens_info):
        errores = []
        cantidad = len(tokens_info)

        for i, token in enumerate(tokens_info):
            palabra = token.texto.lower()

            # --- CASO 1: 'porqué' (Sustantivo) ---
            if palabra == "porqué":
                # Error si NO tiene determinante antes (ej: "el porqué" es correcto)
                if i == 0 or tokens_info[i - 1].categoria != "DET":
                    errores.append(Error(
                        tipo="Mal_uso_porqué",
                        mensaje="'porqué' suele usarse como sustantivo y requiere artículo.",
                        token_inicia=token.posicion,
                        token_final=token.posicion,
                        prioridad=self._prioridad,
                        sugerencia="Si no es sustantivo, usa 'por qué'.",
                        origen="Regla Manual",
                        idx_char_inicio=token.idx_inicio,
                        idx_char_final=token.idx_final,
                        correccion_automatica="por qué"
                    ))

            # --- CASO 2: 'porque' en preguntas ---
            elif palabra == "porque":
                # Verificamos signos de interrogación cercanos
                # Nota: Esto verifica el token inmediatamente anterior/posterior
                inicio_pregunta = (i > 0 and tokens_info[i - 1].texto == "¿")
                fin_pregunta = (i + 1 < cantidad and tokens_info[i + 1].texto == "?")

                if inicio_pregunta or fin_pregunta:
                    errores.append(Error(
                        tipo="Porque_en_pregunta",
                        mensaje="En preguntas debe usarse 'por qué'.",
                        token_inicia=token.posicion,
                        token_final=token.posicion,
                        prioridad=self._prioridad,
                        sugerencia="por qué",
                        origen="Regla Manual",
                        idx_char_inicio=token.idx_inicio,
                        idx_char_final=token.idx_final,
                        correccion_automatica="por qué"
                    ))

            # --- CASO 3: 'por' + 'que' (separado) ---
            elif palabra == "por":
                if i + 1 < cantidad and tokens_info[i + 1].texto.lower() == "que":
                    siguiente = tokens_info[i + 1]
                    # Si 'que' actúa como conjunción (SCONJ), suelen ir juntos
                    if siguiente.categoria in ("SCONJ", "ADV"):
                        errores.append(Error(
                            tipo="Por_que_incorrecto",
                            mensaje="'por que' aquí parece ser una conjunción causal.",
                            token_inicia=token.posicion,
                            token_final=siguiente.posicion,
                            prioridad=self._prioridad,
                            sugerencia="porque",
                            origen="Regla Manual",
                            idx_char_inicio=token.idx_inicio,
                            idx_char_final=siguiente.idx_final,
                            correccion_automatica="porque"
                        ))
        return errores
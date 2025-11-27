import language_tool_python
import sys

# --- IMPORTS DE TUS MÓDULOS ---
from analizador.analizador_linguistico import AnalizadorLinguistico
from analizador.extractor_de_caracteristicas import ExtractorDeCaracteristicas

from corrector.motor_regla_manual import MotorReglaManual
from corrector.integrador_language_tool import IntegradorLanguageTool
from corrector.combianar_resultado import CombinadorDeResultados
from corrector.sugeridor_correcion import SugeridorCorrecion

# --- REGLAS MANUALES ---
from reglas.grupo_gramatica.concordancia_de_determinante_y_sustantivo import ConcordanciaDeDeterminanteYSustantivo
from reglas.grupo_gramatica.concordancia_profunda_sujeto_verbol import ConcordanciaProfundoSujetoVerbol
from reglas.grupo_gramatica.concordancia_entre_sustantivo_adjetivo import ConcordanciaEntreSustantivoAdjectivo
from reglas.grupo_sintaxis.doble_negaccion_incorrecta import DobleNegacionIncorrecta
from reglas.grupo_sintaxis.oracion_sin_verbo_principal import SinVerbolPrincipal
from reglas.grupo_sintaxis.redundancia_de_preposicion import RedundanciaDepreposicion
from reglas.grupo_estilo_redaccion.problema_de_porque import ProblemaDePorque
from reglas.grupo_estilo_redaccion.repeticion_innecesaria_de_palabra import RepeticionInnecesariaDePalabra
from reglas.grupo_semantica.palabra_prohibida import PalabraProhibida
from reglas.grupo_ortografia.tilde_en_monosilaba import TildeMonosilaba
from reglas.grupo_ortografia.uso_incorrecto_de_mayuscula_a_inicio_de_oracion import MayusculaAInicio


def ejecutar_correccion_interactiva(texto, errores, sugeridor):
    texto_actual = texto
    cambios = 0

    print("\n--- MODO INTERACTIVO (Revisando del final al inicio) ---")

    for i, error in enumerate(errores, 1):
        if not error.correccion_automatica:
            print(f"\n [{i}] Aviso: {error.mensaje}")
            continue

        # Mostrar contexto
        fragmento = texto_actual[error.idx_char_inicio:error.idx_char_final]
        print(f"\n[{i}/{len(errores)}] ({error.origen}) {error.tipo}")
        print(f"   Texto original:  '{fragmento}'")
        print(f"   Sugerencia:   '{error.correccion_automatica}'")

        opcion = input("   ¿Aplicar cambio? (s/n): ").strip().lower()

        if opcion == "s":
            texto_actual = sugeridor.aplicar_sugerencia(texto_actual, error)
            print("    -> Corregido.")
            cambios += 1
        else:
            print("    -> Omitido.")

    return texto_actual, cambios


def ejecutar_correccion_total(texto, errores, sugeridor):
    texto_actual = texto
    cambios = 0

    for error in errores:
        if error.correccion_automatica:
            texto_actual = sugeridor.aplicar_sugerencia(texto_actual, error)
            cambios += 1

    return texto_actual, cambios


def inicializar_sistema():
    print("\n-->  INICIALIZANDO MOTORES (Solo se hace una vez)...")

    # 1. SpaCy
    try:
        analizador = AnalizadorLinguistico("es_core_news_sm")
        extractor = ExtractorDeCaracteristicas(analizador)
    except Exception as e:
        print(f"Error crítico cargando SpaCy: {e}")
        sys.exit(1)

    # 2. Motor Manual
    motor = MotorReglaManual(extractor)
    motor.agregar_reglas([
        ConcordanciaDeDeterminanteYSustantivo(),
        ConcordanciaProfundoSujetoVerbol(),
        ConcordanciaEntreSustantivoAdjectivo(),
        DobleNegacionIncorrecta(),
        SinVerbolPrincipal(),
        RedundanciaDepreposicion(),
        ProblemaDePorque(),
        RepeticionInnecesariaDePalabra(),
        PalabraProhibida(),
        TildeMonosilaba(),
        MayusculaAInicio()
    ])

    # 3. LanguageTool
    print("--> Conectando a LanguageTool...")
    try:
        # Intenta usar API pública (Rápido)
        lt_client = language_tool_python.LanguageTool('es', remote_server='https://api.languagetool.org/v2/')
        languagetool = IntegradorLanguageTool(lt_client)
    except Exception:
        print(" Usando modo LOCAL (Puede ser lento la primera vez)...")
        lt_client = language_tool_python.LanguageTool('es')
        languagetool = IntegradorLanguageTool(lt_client)

    combinador = CombinadorDeResultados()
    sugeridor = SugeridorCorrecion()

    print("-->  SISTEMA LISTO.\n")
    return motor, languagetool, combinador, sugeridor


def main():
    print("==============================================")
    print("     CORRECTOR INTELIGENTE DE ESPAÑOL         ")
    print("==============================================")

    motor, languagetool, combinador, sugeridor = inicializar_sistema()

    while True:
        print("\n" + "-" * 50)
        texto_input = input("Ingrese texto (o escribe 'salir' para terminar):\n> ")

        if texto_input.lower() in ["salir", "exit", "chau"]:
            print("¡Hasta luego!")
            break

        if not texto_input.strip():
            continue

        # --- ANÁLISIS ---
        print("\n Analizando...")
        errores_manual = motor.analizar(texto_input)
        errores_lt = languagetool.analizar(texto_input)

        # --- COMBINACIÓN ---
        todos_errores = combinador.combinar(errores_manual, errores_lt)

        # ORDEN INVERSO OBLIGATORIO
        todos_errores.sort(key=lambda x: x.idx_char_inicio, reverse=True)

        cantidad = len(todos_errores)
        if cantidad == 0:
            print(" El texto parece correcto.")
            continue

        print(f" Se encontraron {cantidad} problemas.")

        # --- MENÚ DE ACCIÓN ---
        print("1. Corrección Total (Automática)")
        print("2. Revisión paso a paso")
        print("3. Ver reporte")

        opcion = input("Opción: ").strip()

        texto_final = texto_input
        cambios = 0

        if opcion == "1":
            texto_final, cambios = ejecutar_correccion_total(texto_input, todos_errores, sugeridor)
            print("\n CORRECCIÓN TOTAL APLICADA ")
        elif opcion == "2":
            texto_final, cambios = ejecutar_correccion_interactiva(texto_input, todos_errores, sugeridor)
        else:
            print("\n--- REPORTE DE ERRORES ---")
            todos_errores_lectura = sorted(todos_errores, key=lambda x: x.idx_char_inicio)
            for err in todos_errores_lectura:
                print(f"- [{err.tipo}] {err.mensaje}")


        print("\nRESULTADO:")
        print(f"'{texto_final}'")
        print(f"(Cambios realizados: {cambios}/{cantidad})")


if __name__ == "__main__":
    main()
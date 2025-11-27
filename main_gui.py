import customtkinter as ctk
import threading
from tkinter import messagebox
import sys

# --- IMPORTS DEL BACKEND ---
import language_tool_python
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

# --- CONFIGURACIÓN VISUAL ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class CorrectorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de ventana
        self.title("Corrector Inteligente de Español")
        self.geometry("1100x700")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Variables de Backend
        self.motor = None
        self.languagetool = None
        self.combinador = None
        self.sugeridor = None
        self.backend_listo = False
        self.errores_actuales = []

        # --- LAYOUT PRINCIPAL ---
        self.crear_panel_izquierdo()
        self.crear_area_trabajo()

        # Iniciar carga de modelos en segundo plano
        self.mostrar_cargando("Iniciando motores de IA...\nEsto puede tardar unos segundos la primera vez.")
        threading.Thread(target=self.cargar_backend, daemon=True).start()

    def crear_panel_izquierdo(self):
        """Panel lateral con botones de acción"""
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="CORRECTOR\nINTELIGENTE",
                                       font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.btn_analizar = ctk.CTkButton(self.sidebar_frame, text="🔍 Analizar Texto", command=self.analizar_texto)
        self.btn_analizar.grid(row=1, column=0, padx=20, pady=10)
        self.btn_analizar.configure(state="disabled")

        self.btn_corregir_todo = ctk.CTkButton(self.sidebar_frame, text="✨ Corregir Todo",
                                               fg_color="green", hover_color="darkgreen",
                                               command=self.corregir_todo)
        self.btn_corregir_todo.grid(row=2, column=0, padx=20, pady=10)
        self.btn_corregir_todo.configure(state="disabled")

        self.btn_limpiar = ctk.CTkButton(self.sidebar_frame, text="🗑️ Limpiar",
                                         fg_color="transparent", border_width=2,
                                         text_color=("gray10", "#DCE4EE"),
                                         command=self.limpiar_texto)
        self.btn_limpiar.grid(row=3, column=0, padx=20, pady=10)

        # Status Label
        self.status_label = ctk.CTkLabel(self.sidebar_frame, text="Iniciando...", anchor="w")
        self.status_label.grid(row=5, column=0, padx=20, pady=10)

    def crear_area_trabajo(self):
        """Área derecha: Editor de texto y lista de errores"""
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=3)  # Editor pesa más
        self.main_frame.grid_columnconfigure(1, weight=1)  # Panel de errores
        self.main_frame.grid_rowconfigure(0, weight=1)

        # --- Columna 1: Editor ---
        self.textbox = ctk.CTkTextbox(self.main_frame, font=("Arial", 16), undo=True)
        self.textbox.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self.textbox.insert("0.0", "Escribe aquí tu texto...")

        # --- Columna 2: Lista de Errores ---
        self.error_frame_container = ctk.CTkFrame(self.main_frame)
        self.error_frame_container.grid(row=0, column=1, sticky="nsew")

        # Título lista
        self.label_errores = ctk.CTkLabel(self.error_frame_container, text="Problemas Detectados (0)",
                                          font=ctk.CTkFont(size=14, weight="bold"))
        self.label_errores.pack(pady=10)

        # Scrollable area
        self.scroll_errores = ctk.CTkScrollableFrame(self.error_frame_container, label_text="Detalles")
        self.scroll_errores.pack(fill="both", expand=True, padx=5, pady=5)

    def mostrar_cargando(self, mensaje):
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", mensaje)
        self.textbox.configure(state="disabled")

    def cargar_backend(self):
        """Carga pesada en hilo secundario"""
        try:
            # 1. SpaCy
            analizador = AnalizadorLinguistico("es_core_news_sm")
            extractor = ExtractorDeCaracteristicas(analizador)

            # 2. Motor Manual
            self.motor = MotorReglaManual(extractor)
            self.motor.agregar_reglas([
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
            modo_lt = ""
            try:
                lt_client = language_tool_python.LanguageTool('es')
                self.languagetool = IntegradorLanguageTool(lt_client)
                modo_lt = "Local 💻"
            except Exception as e:
                print(f"Fallo local, intentando nube: {e}")
                try:
                    # Fallback a Nube
                    lt_client = language_tool_python.LanguageTool('es',
                                                                  remote_server='https://api.languagetool.org/v2/')
                    self.languagetool = IntegradorLanguageTool(lt_client)
                    modo_lt = "Nube ☁️"
                except:
                    # Fallback final (Dummy)
                    class DummyLT:
                        def analizar(self, txt): return []

                    self.languagetool = DummyLT()
                    modo_lt = "OFF ❌"

            self.combinador = CombinadorDeResultados()
            self.sugeridor = SugeridorCorrecion()
            self.backend_listo = True

            # Actualizar UI desde hilo principal
            self.after(0, lambda: self.finalizar_carga(modo_lt))

        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Error Fatal", str(e)))

    def finalizar_carga(self, modo_lt):
        self.textbox.configure(state="normal")
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", "las casa rojas comen mucho. tu sabes el porque es mierda.")

        self.btn_analizar.configure(state="normal")
        self.status_label.configure(text=f"Motores Listos | LT: {modo_lt}")

    def limpiar_texto(self):
        self.textbox.delete("0.0", "end")
        self.limpiar_errores_ui()

    def limpiar_errores_ui(self):
        for widget in self.scroll_errores.winfo_children():
            widget.destroy()
        self.label_errores.configure(text="Problemas Detectados (0)")
        self.btn_corregir_todo.configure(state="disabled")

    def analizar_texto(self):
        if not self.backend_listo: return

        texto = self.textbox.get("0.0", "end-1c")
        if not texto.strip(): return

        self.limpiar_errores_ui()
        self.status_label.configure(text="Analizando...")
        self.update()

        # Ejecución
        errores_manual = self.motor.analizar(texto)
        errores_lt = self.languagetool.analizar(texto)

        # Combinar
        self.errores_actuales = self.combinador.combinar(errores_manual, errores_lt)

        # Ordenamos por posición para mostrar en la lista
        self.errores_actuales.sort(key=lambda x: x.idx_char_inicio)

        self.label_errores.configure(text=f"Problemas Detectados ({len(self.errores_actuales)})")
        self.status_label.configure(text="Análisis completo.")

        if self.errores_actuales:
            self.btn_corregir_todo.configure(state="normal")
            self.llenar_lista_errores(texto)
        else:
            self.status_label.configure(text="✅ Texto perfecto.")

    def llenar_lista_errores(self, texto_original):
        for error in self.errores_actuales:
            self.crear_tarjeta_error(error, texto_original)

    def crear_tarjeta_error(self, error, texto_completo):
        """Crea una tarjeta visual para cada error"""
        card = ctk.CTkFrame(self.scroll_errores, fg_color=("gray85", "gray25"))
        card.pack(fill="x", pady=5, padx=2)

        # Header: Tipo de error
        header_color = "#FF8C00" if error.origen == "Regla manual" else "#3B8ED0"  # Naranja vs Azul
        lbl_tipo = ctk.CTkLabel(card, text=f"{error.tipo}", text_color=header_color,
                                font=ctk.CTkFont(size=11, weight="bold"), anchor="w")
        lbl_tipo.pack(fill="x", padx=5, pady=(5, 0))

        # Texto del error
        lbl_msg = ctk.CTkLabel(card, text=error.mensaje, wraplength=200, anchor="w", justify="left")
        lbl_msg.pack(fill="x", padx=5)

        # Contexto (Snippet)
        snippet = texto_completo[error.idx_char_inicio:error.idx_char_final]
        lbl_snippet = ctk.CTkLabel(card, text=f"Error: '{snippet}'", text_color="red", anchor="w")
        lbl_snippet.pack(fill="x", padx=5)

        # Sugerencia y Botón
        if error.correccion_automatica:
            btn_corregir = ctk.CTkButton(card, text=f"Cambiar a '{error.correccion_automatica}'",
                                         height=25,
                                         command=lambda e=error: self.corregir_uno(e))
            btn_corregir.pack(fill="x", padx=5, pady=5)
        else:
            lbl_sug = ctk.CTkLabel(card, text=f"💡 {error.sugerencia}", text_color="gray", anchor="w")
            lbl_sug.pack(fill="x", padx=5, pady=5)

    def corregir_uno(self, error):
        """Corrige UN solo error y re-analiza"""
        texto_actual = self.textbox.get("0.0", "end-1c")
        nuevo_texto = self.sugeridor.aplicar_sugerencia(texto_actual, error)

        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", nuevo_texto)

        # Re-analizar automáticamente
        self.analizar_texto()

    def corregir_todo(self):
        """Aplica todas las correcciones de golpe"""
        texto_actual = self.textbox.get("0.0", "end-1c")

        # Orden inverso para no romper índices
        errores_reversa = sorted(self.errores_actuales, key=lambda x: x.idx_char_inicio, reverse=True)

        cambios = 0
        for error in errores_reversa:
            if error.correccion_automatica:
                texto_actual = self.sugeridor.aplicar_sugerencia(texto_actual, error)
                cambios += 1

        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", texto_actual)
        self.status_label.configure(text=f"Se aplicaron {cambios} correcciones.")

        # Re-analizar para verificar
        self.analizar_texto()


if __name__ == "__main__":
    app = CorrectorApp()
    app.mainloop()
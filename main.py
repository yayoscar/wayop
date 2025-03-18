from scraper.login import iniciar_sesion
from scraper.navigator import navegar_a_quincena
from scraper.downloader import descargar_comprobantes_pw
from utils.logger import logger
from config.settings import config
from utils.file_manager import get_last_downloaded, is_already_downloaded
import customtkinter as ctk
import threading
import os

from playwright.sync_api import sync_playwright


def obtener_inicio():
    """Determina desde qué quincena y año iniciar el scraping."""
    last_downloaded = get_last_downloaded()

    if last_downloaded:  # Si hay historial, iniciar desde la última quincena registrada
        year, quincena = last_downloaded
        quincena = int(quincena) + 1  # Iniciar en la siguiente quincena
        if quincena > 24:  # Si la quincena pasa de 24, avanzar de año
            year += 1
            quincena = 1
        print(f"📌 Continuando desde la siguiente quincena: {year} - Q{quincena:02d}")
    else:  # Si no hay historial, usar el `config.ini`
        year = int(config.get("PERIODO", "inicio").split()[0])
        quincena = int(config.get("PERIODO", "inicio").split()[1])
        print(f"📌 No hay historial previo. Iniciando desde {year} - Q{quincena:02d}")
    quincena=str(quincena).zfill(2)  # Asegurar formato correcto (01, 02, ..., 24)
    return year, quincena


def main():
    year, quincena = obtener_inicio()
    with sync_playwright() as p:
        pagina = iniciar_sesion(p)
        
        if pagina:
            if is_already_downloaded(year, quincena):  # Evitar descargas repetidas
                print(f"✅ Saltando {year} - Q{quincena}, ya fue descargado.")
            else:        
                while True:        
                    exito = navegar_a_quincena(pagina,year,quincena)
            
                    if exito:
                        descargar_comprobantes_pw(pagina, year, quincena)
                    else:
                        print("❌ No hay comprobantes disponibles.")

                        input("Presiona Enter para cerrar el navegador...")  # Mantenerlo abierto para prueba
            
                        pagina.context.close()
                        break
                    quincena = str(int(quincena) + 1).zfill(2)  # Asegurar formato correcto (01, 02, ..., 24)

                # 📌 Si la quincena pasa de 24, cambiar de año y actualizar la carpeta de descargas sin cerrar sesión
                    if int(quincena) > 24:
                        print(f"📅 Cambio de año detectado: {year} ➝ {year + 1}")
                        year += 1
                        quincena = "01"  # Reiniciar quincena a 01


class ScraperApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Descargador Web")
        self.geometry("500x400")
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.label = ctk.CTkLabel(self, text="Introduce tus credenciales")
        self.label.pack(pady=10)
        
        self.entry_user = ctk.CTkEntry(self, placeholder_text="Usuario")
        self.entry_user.pack(pady=5)
        
        self.entry_pass = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*")
        self.entry_pass.pack(pady=5)
        
        self.button_start = ctk.CTkButton(self, text="Iniciar Descarga", command=self.start_scraping)
        self.button_start.pack(pady=10)
        
        self.text_log = ctk.CTkTextbox(self, height=150)
        self.text_log.pack(pady=10, padx=10, fill='both', expand=True)
        
    def start_scraping(self):
        user = self.entry_user.get()
        password = self.entry_pass.get()
        
        self.text_log.insert('end', "Iniciando descarga...\n")
        
        thread = threading.Thread(target=self.run_scraper, args=(user, password))
        thread.start()
        
    def run_scraper(self, user, password):
        try:
            #resultado = descargar_pagina(user, password)  # Llama a tu función de descarga real
            resultado = "SI"  # Aquí llamas a tu función principal de scraping
            self.text_log.insert('end', f"Descarga finalizada: {resultado}\n")
        except Exception as e:
            self.text_log.insert('end', f"Error: {e}\n")

if __name__ == "__main__":
    main()
    # app = ScraperApp()
    # app.mainloop()

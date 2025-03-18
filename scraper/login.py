
from playwright.sync_api import sync_playwright

import time
from config.settings import config
from config_pw import CONFIG_PW
from utils.logger import logger
import os

def iniciar_sesion(playwright):
    """Inicia sesión en la plataforma usando Playwright con reintentos en caso de error."""
    navegador = playwright.chromium.launch(headless=CONFIG_PW["PLAYWRIGHT"]["headless"])
    contexto = navegador.new_context(accept_downloads=True)  # Habilitar descargas

    pagina = contexto.new_page()

    print("🔹 Accediendo a la página de login...")
    pagina.goto("https://portalautoservicios-sems.sep.gob.mx/login.jsp")

    intentos_login = 3  # Número máximo de intentos de login
    intentos_dashboard = 3  # Número máximo de intentos de carga del dashboard

    for intento in range(1, intentos_login + 1):
        try:
            # Esperar máximo 3 segundos a que aparezca el campo username
            pagina.wait_for_selector("#username", timeout=3000)
            print(f"✅ Campos de login encontrados en intento {intento}.")
            break  # Salimos del loop si lo encontramos
        except:
            print(f"⚠️ Intento {intento}: Campos de login no encontrados, recargando la página...")
            pagina.reload()
            time.sleep(1)

    else:
        print("❌ No se pudo cargar el formulario de login después de varios intentos.")
        navegador.close()
        return None

    # Rellenar los campos de usuario y contraseña
    pagina.fill("#username", CONFIG_PW["LOGIN"]["usuario"])
    pagina.fill("#password", CONFIG_PW["LOGIN"]["password"])

    # Presionar el botón de login
    pagina.click("#btnLogin")

    # 🔄 Intentar hasta 3 veces si el dashboard no carga correctamente
    for intento in range(1, intentos_dashboard + 1):
        try:
            print(f"⏳ Esperando carga del dashboard... Intento {intento}/3")
            pagina.wait_for_load_state("networkidle")
            
            # Esperar a que aparezca el texto "Impresión comprobante de pago"
            pagina.wait_for_selector("text=Impresión comprobante de pago", timeout=10000)
            print("✅ Página cargada correctamente.")
            # 1️⃣ Esperar a que se cargue la sección "Impresión comprobante de pago"
            pagina.wait_for_selector("text=Impresión comprobante de pago", timeout=10000)
            print("✅ Sección 'Impresión comprobante de pago' encontrada.")

            # 2️⃣ Hacer clic en el menú "Impresión comprobante de pago"
            selector = "[id^=dijit__TreeNode_]"  # Selecciona elementos cuyo ID comienza con 'dijit__TreeNode_'
            pagina.wait_for_selector(selector, timeout=10000)
            
            # 2️⃣ Hacer clic en el primer elemento que cumpla la condición
            pagina.locator(selector).first.click()
            return pagina

        except:
            print(f"⚠️ Intento {intento}: No se encontró 'Impresión comprobante de pago', recargando...")
            pagina.reload()
            time.sleep(2)

    print("❌ No se pudo cargar la página correctamente después de varios intentos.")
    navegador.close()
    return None

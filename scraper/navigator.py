from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from utils.logger import logger
from playwright.sync_api import Page

def navegar_a_descarga(driver, year, quincena):
    """Navega hasta la sección de descarga e ingresa los datos."""
    wait = WebDriverWait(driver, 10)

    try:
        # 1️⃣ Ir a la sección "Impresión comprobante de pago"
        logger.info("Navegando a la sección de impresión de comprobantes...")
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Impresión comprobante de pago')]")))

        elemento = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id, 'dijit__TreeNode_')]"))
        )

        # Hacer clic en el elemento
        elemento.click()
        logger.info(f"Cargando formulario de descarga para {year} - Q{quincena}...")

        time.sleep(3)
        # 2️⃣ Ingresar el año y la quincena
        input_anio = wait.until(EC.element_to_be_clickable((By.NAME, "anio")))
        input_quincena = wait.until(EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id, 'quincenacomprobanteEmpl')]")))

        input_anio.clear()
        input_anio.send_keys(str(year))
        input_quincena.clear()
        input_quincena.send_keys(str(quincena).zfill(2))  # Asegura dos dígitos

        # 3️⃣ Presionar el botón de búsqueda
        btn_buscar = wait.until(EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id, 'btnBuscarcomprobanteEmpl')]")))

        btn_buscar.click()
        # ⏳ 4️⃣ Esperar a que se complete la carga de información
        esperar_carga_informacion(driver)

        # 5️⃣ Verificar si hay resultados o si no existe información
        no_info_msg = "No existe información para mostrar"
        problemas_msg="Problemas al recuperar información"


        if no_info_msg in driver.page_source:
            logger.warning(f"🚫 No hay comprobantes disponibles para {year} - Q{quincena}. Deteniendo la búsqueda.")
            return False
        
        if problemas_msg in driver.page_source:
            logger.warning(f"🚫 Problemas para obtener {year} - Q{quincena}. Deteniendo la búsqueda.")
            return False

        logger.info(f"✅ Comprobantes disponibles para {year} - Q{quincena}, procediendo con la descarga.")
        return True  # Hay resultados

    except Exception as e:
        logger.error(f"Error al navegar a la sección de comprobantes: {e}")
        return False

def esperar_carga_informacion(driver):
    """Espera hasta que desaparezca el mensaje 'Cargando Información'."""
    wait = WebDriverWait(driver, 15)  # Esperar hasta 15 segundos como máximo

    try:
        # Esperar a que aparezca "Cargando Información"
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Cargando Información')]")))
        logger.info("⏳ Cargando información... esperando a que termine.")

        # Esperar hasta que desaparezca "Cargando Información"
        wait.until_not(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Cargando Información')]")))
        logger.info("✅ Carga completada.")

    except Exception as ex:
        logger.warning(f"⚠️ No se detectó el mensaje 'Cargando Información', continuando de todas formas. Error: {ex}")


def navegar_a_quincena(pagina: Page,year, quincena):
    """Navega hasta la sección de impresión de comprobantes y selecciona la quincena deseada."""

    print(f"📅 Navegando a la quincena {year} - Q{quincena}...")

    try:
    

        # 3️⃣ Ingresar el año
        selector="[id^=aniocomprobanteEmpl]"
        pagina.wait_for_selector(selector, timeout=10000)

        input_anio = pagina.locator("[id^=aniocomprobanteEmpl]").first
        input_anio.fill(str(year))

        # 4️⃣ Ingresar la quincena
        input_quincena = pagina.locator("[id^=quincenacomprobanteEmpl]").first
        input_quincena.fill(quincena)

        # 5️⃣ Hacer clic en el botón de búsqueda
        btn_buscar = pagina.get_by_role("button", name="Buscar")
        btn_buscar.click()
        print(f"🔍 Buscando comprobantes para {year} - Q{quincena}...")

        esperar_carga_informacion_pw(pagina)

        no_info_msg = "No existe información para mostrar"
        if no_info_msg in pagina.inner_text("body"):
            print(f"🚫 No hay comprobantes disponibles para {year} - Q{quincena}.")
            return False

        print(f"✅ Comprobantes disponibles para {year} - Q{quincena}.")
        return True  # Hay resultados

    except Exception as e:
        print(f"❌ Error al navegar a la quincena {year} - Q{quincena}: {e}")
        return False
    
def esperar_carga_informacion_pw(pagina: Page, timeout=15):
    """Espera hasta que desaparezca el mensaje 'Cargando Información' en Playwright."""
    
    try:
        # 🔎 Esperar hasta que aparezca "Cargando Información" (máximo 15 segundos)
        if pagina.locator("text=Cargando Información").is_visible():
            logger.info("⏳ Cargando información... esperando a que termine.")

            # Esperar hasta que desaparezca "Cargando Información"
            pagina.locator("text=Cargando Información").wait_for(state="hidden", timeout=timeout * 1000)
            logger.info("✅ Carga completada.")

        else:
            logger.info("🔍 No se detectó el mensaje 'Cargando Información', continuando de todas formas.")

    except Exception as ex:
        logger.warning(f"⚠️ Error al esperar la carga de información, continuando... Error: {ex}")
import time
import os
from utils.logger import logger
from utils.file_manager import mark_as_downloaded

from playwright.sync_api import Page, expect


DOWNLOAD_DIR = os.path.abspath("downloads")  # Ruta absoluta

def descargar_comprobantes_pw(pagina: Page, year: str, quincena: str):
    """Descarga los comprobantes disponibles en la tabla y los guarda en la carpeta correspondiente."""
    
    # 📂 Configurar la carpeta correcta para esta quincena
    download_path = os.path.abspath(f"downloads/{year}")
    os.makedirs(download_path, exist_ok=True)

    filas = pagina.locator(".dojoxGridRow")  # Seleccionar filas de la tabla
    num_filas = filas.count()

    if num_filas == 0:
        print(f"⚠️ No hay comprobantes disponibles para {year} - Q{quincena}")
        return

    for idx in range(num_filas):
        try:
            print(f"📥 Descargando comprobante {idx+1} de {num_filas} para {year} - Q{quincena}...")

            # Hacer clic en la fila correspondiente
            filas.nth(idx).click()
            time.sleep(2)

            # Capturar el evento de descarga
            with pagina.expect_download() as download_info:
                pagina.get_by_role("button", name="Imprimir").click()  # Clic en el botón de descarga

            #dijitButtonDisabled
            download = download_info.value
            archivo_descargado = download.path()  # Obtener la ruta temporal

            # Generar el nuevo nombre y mover el archivo
            nuevo_nombre = os.path.join(download_path, f"{year}-Q{quincena}-{idx+1}.pdf")
            os.rename(archivo_descargado, nuevo_nombre)

            print(f"✅ Archivo descargado: {nuevo_nombre}")

        except Exception as e:
            logger.error(f"❌ Error al descargar comprobante {idx+1}: {e}")
    mark_as_downloaded(year, quincena)

def esperar_boton_habilitado(pagina: Page, timeout=10):
    """Espera hasta que el botón 'Imprimir' esté habilitado antes de continuar."""
    print("⏳ Esperando que el botón 'Imprimir' esté habilitado...")

    
    boton = pagina.locator("[id^=btnImprimircomprobanteEmpl]")

    for _ in range(timeout * 2):  # Reintentar por `timeout` segundos
        if not boton.get_attribute("class") or "dijitButtonDisabled" not in boton.get_attribute("class"):
            print("✅ Botón 'Imprimir' habilitado.")
            return True
        time.sleep(0.5)  # Esperar 0.5 segundos antes de volver a revisar

    print("⚠️ Botón 'Imprimir' sigue deshabilitado después del tiempo de espera.")
    return False
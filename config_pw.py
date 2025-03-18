import os

CONFIG_PW = {
    "LOGIN": {
        "usuario": "PEOO820203MB1",
        "password": "atlante3"
    },
    "PLAYWRIGHT": {
        "headless": False,  # Cambia a True si no quieres ver el navegador
        "downloads_dir": os.path.abspath("downloads")  # Carpeta donde se guardarán los archivos
    }
}

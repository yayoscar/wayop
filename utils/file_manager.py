import json
import os

HISTORY_FILE = "history/downloaded_history.json"

def load_download_history():
    """Carga el historial de descargas desde un archivo JSON."""
    if not os.path.exists(HISTORY_FILE):
        return {}

    with open(HISTORY_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def save_download_history(history):
    """Guarda el historial de descargas en un archivo JSON."""
    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4)

def get_last_downloaded():
    """Obtiene la última quincena registrada en el historial."""
    history = load_download_history()

    if not history:  # Si no hay historial, retornar None
        return None

    # Obtener el último año con datos
    last_year = max(map(int, history.keys()))

    # Obtener la última quincena registrada en ese año
    last_quincena = max(map(int, history[str(last_year)]))

    return last_year, str(last_quincena).zfill(2)  # Retorna (YYYY, QQ) en formato correcto

def is_already_downloaded(year, quincena):
    """Verifica si un comprobante ya ha sido descargado."""
    history = load_download_history()
    return str(year) in history and quincena in history[str(year)]

def mark_as_downloaded(year, quincena):
    """Marca un comprobante como descargado en el historial."""
    history = load_download_history()

    if str(year) not in history:
        history[str(year)] = []

    if quincena not in history[str(year)]:
        history[str(year)].append(quincena)
    
    save_download_history(history)

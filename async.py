import httpx
import ssl
import asyncio

# Crear un contexto SSL con TLS 1.2 mínimo
ssl_context = ssl.create_default_context()
ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2  # Forzar TLS 1.2 o superior

async def fetch_data():
    url = "https://portalautoservicios-sems.sep.gob.mx/mvc/seguridad/menu/1"

    headers = {
        "Accept": "application/javascript, application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://portalautoservicios-sems.sep.gob.mx/",
        "Cookie": "visid_incap_3123066=OcGr/cXSSUOT5vFEJIa7VN2phmcAAAAAQUIPAAAAAAA9WpU4BK5o/bmdv7/37DCM; visid_incap_3127458=HV5fq8qmQY22ygbyjnhu1p7fh2cAAAAAQUIPAAAAAADN4UAKp5uzUA08Ptxc4drb; __utmz=31077566.1741875680.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ga=GA1.3.875420844.1741955004; _ga_FK2HWT74VG=GS1.3.1741955004.1.0.1741955004.0.0.0; __utma=31077566.573017518.1741875680.1741955489.1742306599.3; __utmc=31077566; JSESSIONID=9c7f0d2630e3257051f591576239; undefined=4; __utmt=1; __utmb=31077566.22.9.1742310926047"
    }

    async with httpx.AsyncClient(verify=ssl_context, timeout=60.0) as client:
        response = await client.get(url, headers=headers)
        print(response.json())

asyncio.run(fetch_data())

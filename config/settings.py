import configparser

class Config:
    def __init__(self, config_file="config.ini"):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    def get(self, section, key):
        return self.config.get(section, key, fallback=None)

# Instancia de configuración
config = Config()

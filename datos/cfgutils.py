import configparser
import os

class CfgUtils:
    """
    Utilidad simple para manejar configuración basada en archivos .cfg usando configparser.
    Sirve para guardar y leer records (puntuaciones) y otros valores.
    """
    def __init__(self, archivo, seccion, clave):
        self.archivo = archivo
        self.seccion = seccion
        self.clave = clave
        self.config = configparser.ConfigParser()
        self._asegurar_archivo()

    def _asegurar_archivo(self):
        """Crea el archivo si no existe y pone valor por defecto 0."""
        if not os.path.isfile(self.archivo):
            self.config[self.seccion] = {self.clave: "0"}
            with open(self.archivo, "w") as f:
                self.config.write(f)
        self.config.read(self.archivo)

    def leer(self):
        """Lee el valor de la clave (como string)."""
        self.config.read(self.archivo)
        return self.config.get(self.seccion, self.clave, fallback="0")

    def escribir(self, valor):
        """Escribe el valor de la clave."""
        self.config.read(self.archivo)
        if not self.config.has_section(self.seccion):
            self.config.add_section(self.seccion)
        self.config.set(self.seccion, self.clave, str(valor))
        with open(self.archivo, "w") as f:
            self.config.write(f)

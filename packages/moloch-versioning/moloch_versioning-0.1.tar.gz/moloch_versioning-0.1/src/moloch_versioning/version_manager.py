
from name_generator import NameGenerator

class VersionManager:
    """
    VersionManager es responsable de generar el número de versión en formato semántico (major.minor.patch)
    basado en el tipo de cambio realizado. Integra el NameGenerator para formar el identificador completo.
    """

    def __init__(self):
        self.major = 0
        self.minor = 0
        self.patch = 0
        self.name_generator = NameGenerator()

    def update_version(self, change_type):
        """
        Actualiza el número de versión según el tipo de cambio.
        :param change_type: Tipo de cambio ("major", "minor", "patch").
        :return: Versión en formato "vX.Y.Z" y nombre temático.
        """
        if change_type == "major":
            self.major += 1
            self.minor = 0
            self.patch = 0
        elif change_type == "minor":
            self.minor += 1
            self.patch = 0
        elif change_type == "patch":
            self.patch += 1
        else:
            raise ValueError("Tipo de cambio inválido. Use 'major', 'minor' o 'patch'.")

        version = f"v{self.major}.{self.minor}.{self.patch}"
        name = self.name_generator.generate_name()
        return name, version

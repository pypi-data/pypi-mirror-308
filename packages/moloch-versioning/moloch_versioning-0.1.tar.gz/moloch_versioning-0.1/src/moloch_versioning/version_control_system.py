
from config import ConfigManager
from version_manager import VersionManager
from hashing import VersionHasher
from changelog_manager import ChangelogManager

class VersionControlSystem:
    """
    VersionControlSystem integra la funcionalidad de control de versiones y gestiona la creación de changelogs
    con la clasificación de visibilidad adecuada.
    """

    def __init__(self):
        self.config_manager = ConfigManager()
        self.version_manager = VersionManager()
        # Usar una ruta relativa para el archivo de changelog
        self.changelog_manager = ChangelogManager(changelog_path="changelog.txt")
        self.hasher = None

    def create_version_identifier(self, change_type):
        """
        Genera el identificador de versión completo y añade una entrada en el changelog.
        :param change_type: Tipo de cambio ("major", "minor", "patch").
        :return: Identificador de versión en el formato [nombre_temático]_v[versión]_[hash_SHA256].
        """
        # Generar nombre temático y número de versión
        name, version = self.version_manager.update_version(change_type)
        
        # Crear hash basado en el nombre y versión
        self.hasher = VersionHasher(name, version)
        hash_value = self.hasher.generate_sha256_hash()

        # Formar el identificador completo
        full_version_identifier = f"{name}_{version}_{hash_value}"

        # Agregar entrada al changelog
        self.changelog_manager.add_entry(name, version, hash_value, change_type)

        return full_version_identifier

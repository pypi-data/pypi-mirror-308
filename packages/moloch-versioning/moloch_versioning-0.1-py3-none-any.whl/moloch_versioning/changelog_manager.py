import os
from datetime import datetime
from config import ConfigManager

class ChangelogManager:
    """
    ChangelogManager gestiona la creación y almacenamiento de changelogs para registrar cada versión generada.
    Incluye la clasificación de visibilidad (público, confidencial, secreto) de cada cambio,
    así como campos adicionales opcionales: Descripción, Estado de la Versión, y Impacto.
    """

    def __init__(self, changelog_path="changelog.txt"):
        self.changelog_path = changelog_path
        self.config_manager = ConfigManager()
        
        # Crear el archivo si no existe
        if not os.path.exists(self.changelog_path):
            with open(self.changelog_path, "w") as file:
                file.write("Changelog Inicial\n\n")

    def add_entry(self, name, version, hash_value, change_type, description="", status="Stable", impact="Medium"):
        """
        Añade una entrada al changelog con timestamp, nombre, versión, hash, y clasificación de visibilidad, así como
        descripción opcional, estado y nivel de impacto.
        :param name: Nombre temático de la versión.
        :param version: Número de versión en formato "vX.Y.Z".
        :param hash_value: Hash SHA256 de la versión.
        :param change_type: Tipo de cambio ("major", "minor", "patch").
        :param description: Descripción breve del cambio (opcional).
        :param status: Estado de la versión, como "Stable", "Beta", "Experimental" (opcional).
        :param impact: Nivel de impacto del cambio, como "High", "Medium", "Low" (opcional).
        """
        # Determinar la clasificación de visibilidad del cambio
        visibility = self.config_manager.get_visibility_classification(change_type)
        
        # Obtener el timestamp actual
        current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Crear la entrada del changelog con todos los datos
        entry = f"Timestamp: {current_timestamp}\n" \
                f"Version: {name}_{version}_{hash_value}\n" \
                f"Type: {change_type}\n" \
                f"Visibility: {visibility}\n" \
                f"Description: {description}\n" \
                f"Status: {status}\n" \
                f"Impact: {impact}\n---\n"

        # Guardar la entrada en el archivo changelog
        with open(self.changelog_path, "a") as changelog_file:
            changelog_file.write(entry)

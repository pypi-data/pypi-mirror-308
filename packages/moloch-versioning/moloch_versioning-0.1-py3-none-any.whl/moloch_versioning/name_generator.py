import random

class NameGenerator:
    """
    NameGenerator selecciona un nombre temático para cada versión. Por defecto, utiliza una lista de nombres de demonios,
    pero puede configurarse para otros temas en el futuro.
    """

    def __init__(self, theme="demons"):
        """
        Inicializa el generador con una lista de nombres basada en el tema seleccionado.
        :param theme: Tema de nombres (por defecto: "demons").
        """
        self.theme = theme
        self.names = self._load_names()

    def _load_names(self):
        """
        Carga una lista de nombres predefinida para el tema "demons". Esta lista puede expandirse o
        cambiarse en el futuro para temas adicionales.
        """
        demon_names = [
            "moloch", "baal", "asmodeus", "belial", "lucifer", "beelzebub", 
            "mammon", "azazel", "aamon", "dagon", "baphomet", "abaddon"
        ]
        return demon_names

    def generate_name(self):
        """
        Selecciona un nombre aleatorio de la lista basada en el tema.
        :return: Nombre temático seleccionado.
        """
        return random.choice(self.names)


# Ejemplo de uso del NameGenerator para verificar su funcionamiento
name_generator = NameGenerator()
generated_name = name_generator.generate_name()

generated_name  # Muestra un nombre temático seleccionado aleatoriamente del tema "demons".

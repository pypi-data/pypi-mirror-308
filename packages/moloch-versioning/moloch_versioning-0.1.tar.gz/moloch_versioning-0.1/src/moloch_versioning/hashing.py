
import hashlib

class VersionHasher:
    """
    VersionHasher es responsable de generar un hash SHA256 para cada versión, utilizando como entrada
    el nombre temático combinado con el número de versión (ej: "moloch_v0.0.1").
    """

    def __init__(self, name, version):
        """
        Inicializa el hasher con el nombre temático y el número de versión.
        :param name: Nombre temático de la versión.
        :param version: Número de versión en formato "vX.Y.Z".
        """
        self.name = name
        self.version = version

    def generate_sha256_hash(self):
        """
        Genera un hash SHA256 a partir del nombre temático y el número de versión.
        :return: Hash SHA256 en formato hexadecimal.
        """
        sha256 = hashlib.sha256()
        input_string = f"{self.name}_{self.version}"
        sha256.update(input_string.encode('utf-8'))
        return sha256.hexdigest()

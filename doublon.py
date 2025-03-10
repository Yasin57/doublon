import os
import hashlib
import time
from datetime import datetime
from typing import List, Dict, Set, Tuple, Optional

class File:
    """
    Classe représentant un fichier avec ses propriétés importantes pour la comparaison
    """
    def __init__(self, path: str):
        self.path = path
        self.name = os.path.basename(path)
        self.size = os.path.getsize(path)
        self.modification_time = os.path.getmtime(path)
        self.modification_date = datetime.fromtimestamp(self.modification_time)
        self._md5 = None
        self._first_bytes = None
        def __eq__(self, other):
        if not isinstance(other, File):
            return False
        # Deux fichiers sont considérés identiques si leur taille et MD5 sont identiques
        return self.size == other.size and self.md5 == other.md5
    
    def __hash__(self):
        # Pour pouvoir utiliser les fichiers dans des sets ou comme clés de dictionnaires
        return hash((self.size, self.md5))
    
    def __str__(self):
        return f"File(name='{self.name}', size={self.size}, md5={self.md5}, modified={self.modification_date})"

    @property
    def first_bytes_hex(self) -> str:
        """Retourne les 5 premiers octets du fichier en format hexadécimal"""
        if self._first_bytes is None:
            with open(self.path, 'rb') as f:
                self._first_bytes = f.read(5)
        return ''.join(f'{b:02x}' for b in self._first_bytes)

    @property
    def md5(self) -> str:
        """Calcule et retourne la signature MD5 du fichier (calculée à la demande)"""
        if self._md5 is None:
            with open(self.path, 'rb') as f:
                hash_md5 = hashlib.md5()
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
                self._md5 = hash_md5.hexdigest()
        return self._md5
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
    
        def scan_directory(directory: str) -> List[File]:
    """
    Parcourt récursivement un répertoire et retourne la liste des objets File
    """
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            path = os.path.join(root, filename)
            try:
                files.append(File(path))
            except (PermissionError, FileNotFoundError) as e:
                print(f"Erreur lors de l'accès au fichier {path}: {e}")
    return files


def find_duplicates(files: List[File]) -> Dict[str, List[File]]:
    """
    Identifie les fichiers en doublons dans une liste de fichiers
    Retourne un dictionnaire avec le MD5 comme clé et la liste des fichiers correspondants comme valeur
    """
    # Première passe: Grouper par taille (filtre rapide)
    size_groups = {}
    for file in files:
        if file.size not in size_groups:
            size_groups[file.size] = []
        size_groups[file.size].append(file)
    
    # Deuxième passe: Pour les fichiers de même taille, vérifier les premiers octets
    potential_duplicates = []
    for size_group in size_groups.values():
        if len(size_group) > 1:
            # Grouper par premiers octets
            first_bytes_groups = {}
            for file in size_group:
                if file.first_bytes_hex not in first_bytes_groups:
                    first_bytes_groups[file.first_bytes_hex] = []
                first_bytes_groups[file.first_bytes_hex].append(file)
            
            # Ajouter les groupes qui ont encore des doublons potentiels
            for first_bytes_group in first_bytes_groups.values():
                if len(first_bytes_group) > 1:
                    potential_duplicates.extend(first_bytes_group)
    
    # Troisième passe: Pour les fichiers ayant mêmes taille et premiers octets, vérifier MD5
    md5_groups = {}
    for file in potential_duplicates:
        if file.md5 not in md5_groups:
            md5_groups[file.md5] = []
        md5_groups[file.md5].append(file)
    
    # Filtrer pour ne garder que les groupes ayant des doublons
    duplicates = {md5: group for md5, group in md5_groups.items() if len(group) > 1}
    
    return duplicates

def get_directory_size_by_type(directory: str) -> Dict[str, int]:
    """
    Calcule la taille totale des fichiers par type dans un répertoire et ses sous-répertoires
    """
    extension_categories = {
        'texte': ['.txt', '.doc', '.docx', '.odt', '.csv', '.xls', '.ppt', '.odp'],
        'images': ['.jpg', '.png', '.bmp', '.gif', '.svg'],
        'vidéo': ['.mp4', '.avi', '.mov', '.mpeg', '.wmv'],
        'audio': ['.mp3', '.mp2', '.wav', '.bwf'],
        'autre': []  # Tous les autres types
    }
    
    # Initialiser les compteurs
    size_by_category = {category: 0 for category in extension_categories.keys()}
    
    # Parcourir les fichiers
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            path = os.path.join(root, filename)
            try:
                size = os.path.getsize(path)
                _, ext = os.path.splitext(filename)
                ext = ext.lower()
                
                # Déterminer la catégorie
                category_found = False
                for category, extensions in extension_categories.items():
                    if category != 'autre' and ext in extensions:
                        size_by_category[category] += size
                        category_found = True
                        break
                
                if not category_found:
                    size_by_category['autre'] += size
                    
            except (PermissionError, FileNotFoundError) as e:
                print(f"Erreur lors de l'accès au fichier {path}: {e}")
    
    return size_by_category


def compare_directories(dir1: str, dir2: str) -> Tuple[List[File], List[File]]:
    """
    Compare deux répertoires et retourne:
    1. Les fichiers de dir2 qui sont en doublons avec dir1
    2. Les fichiers de dir2 qui sont uniques (non présents dans dir1)
    """
    # Analyser les deux répertoires
    files_dir1 = scan_directory(dir1)
    files_dir2 = scan_directory(dir2)
    
    # Créer un ensemble pour un accès rapide
    files_dir1_set = set(files_dir1)
    
    # Identifier les doublons et les fichiers uniques
    duplicates = []
    unique_files = []
    
    for file2 in files_dir2:
        if file2 in files_dir1_set:
            duplicates.append(file2)
        else:
            unique_files.append(file2)
    
    return duplicates, unique_files
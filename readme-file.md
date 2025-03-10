# Gestionnaire de Fichiers en Doublons

Ce projet propose un système de gestion de fichiers permettant d'identifier, comparer et gérer les fichiers en doublons entre différents répertoires.

## Fonctionnalités

Le programme offre 5 fonctionnalités principales :

### 1. Analyse d'un répertoire
Détecte les fichiers en doublons dans un répertoire et ses sous-répertoires en utilisant une approche en 3 étapes :
- Comparaison des tailles de fichiers
- Vérification des 5 premiers octets
- Calcul et comparaison des signatures MD5

### 2. Analyse de l'espace disque par type de fichiers
Calcule la somme (en octets) des fichiers par catégorie :
- Texte (txt, doc, docx, odt, csv, xls, ppt, odp)
- Images (jpg, png, bmp, gif, svg)
- Vidéo (mp4, avi, mov, mpeg, wmv)
- Audio (mp3, mp2, wav, bwf)
- Autres (tous les autres types)

### 3. Comparaison de deux répertoires
Compare les fichiers entre deux répertoires et identifie :
- Les fichiers en doublons dans le deuxième répertoire
- Les fichiers uniques du deuxième répertoire

### 4. Suppression des doublons
Identique à la fonctionnalité 3, mais avec suppression automatique des fichiers en doublons dans le deuxième répertoire.

### 5. Rapatriement des fichiers uniques
Copie les fichiers uniques du deuxième répertoire vers le premier. Si deux fichiers ont le même nom, conserve celui qui a été modifié le plus récemment.

## Utilisation

```bash
python main.py --axe [1-5] --dir1 [chemin_repertoire1] --dir2 [chemin_repertoire2]
```

Arguments :
- `--axe` : Le numéro de l'axe à exécuter (1-5)
- `--dir1` : Chemin vers le premier répertoire
- `--dir2` : Chemin vers le deuxième répertoire (requis pour les axes 3, 4 et 5)

### Exemples concrets avec tes répertoires :

```bash
# Analyse de test_dir1 pour trouver les doublons
python main.py --axe 1 --dir1 test_dir1

# Analyse de l'espace disque par type de fichiers dans test_dir1
python main.py --axe 2 --dir1 test_dir1

# Comparaison des fichiers entre test_dir1 et test_dir2
python main.py --axe 3 --dir1 test_dir1 --dir2 test_dir2

# Suppression des doublons dans test_dir2 en fonction de test_dir1
python main.py --axe 4 --dir1 test_dir1 --dir2 test_dir2

# Rapatriement des fichiers uniques de test_dir2 vers test_dir1
python main.py --axe 5 --dir1 test_dir1 --dir2 test_dir2
```

## Implémentation

Le programme utilise une classe `File` qui encapsule les propriétés importantes d'un fichier :
- Chemin complet
- Nom
- Taille en octets
- Date de modification
- 5 premiers octets (en hexadécimal)
- Signature MD5

Les signatures MD5 et les premiers octets sont calculés à la demande pour optimiser les performances, en particulier lors de la manipulation de grands répertoires.

## Optimisations

Pour améliorer les performances avec de grandes quantités de fichiers, le programme :
1. Utilise une approche en 3 étapes pour identifier les doublons (taille → premiers octets → MD5)
2. Calcule les propriétés coûteuses (MD5) uniquement lorsque nécessaire
3. Utilise des structures de données efficaces (ensembles, dictionnaires) pour les opérations de recherche

## Dépendances

Le programme utilise uniquement des modules de la bibliothèque standard Python :
- `os`
- `hashlib`
- `time`
- `shutil`
- `datetime`
- `argparse`


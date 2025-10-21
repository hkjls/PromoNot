#!/usr/bin/env bash
# exit on error
set -o errexit

# Render installera les dépendances via pyproject.toml
# Il n'est donc plus nécessaire de faire "pip install" ici.

# Commandes pour Django
python manage.py collectstatic --no-input
python manage.py migrate

# N'oubliez pas de rendre ce script exécutable :
# bash
# chmod +x build.sh```

# #### 3. Configuration sur l'interface de Render
# Lors de la création de votre **Web Service** sur Render, les changements sont minimes mais importants :

# *   **Détection automatique** : Render détectera la présence de votre fichier `pyproject.toml` et utilisera automatiquement Poetry pour installer les dépendances. Vous n'avez rien à configurer pour cette étape.
# *   **Build Command** (Commande de construction) : `bash ./build.sh`. C'est la même commande, mais le contenu du script est maintenant adapté à un environnement géré par Poetry.
# *   **Start Command** (Commande de démarrage) : `poetry run gunicorn votre_projet.wsgi`. Il est recommandé d'utiliser `poetry run` pour s'assurer que Gunicorn est exécuté dans l'environnement virtuel géré par Poetry. Remplacez `votre_projet` par le nom de votre projet Django.
# *   **Variables d'environnement** : Vous devrez toujours configurer les variables d'environnement (`DATABASE_URL`, `SECRET_KEY`, etc.) comme dans la procédure standard.

# ### Résumé des différences clés

# | Élément | Projet avec `pip` | Projet avec `Poetry` |
# | :--- | :--- | :--- |
# | **Gestion des dépendances** | `requirements.txt` | `pyproject.toml` et `poetry.lock` |
# | **Script `build.sh`** | `pip install -r requirements.txt`<br>`python manage.py ...` | Pas de `pip install`.<br>`python manage.py ...` |
# | **Commande de démarrage** | `gunicorn votre_projet.wsgi` | `poetry run gunicorn votre_projet.wsgi` |

# En suivant ces ajustements, votre déploiement avec Poetry sur Render se déroulera sans accroc. La plateforme est conçue pour reconnaître et s'adapter à cet outil moderne de gestion de dépendances.

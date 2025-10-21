#!/usr/bin/env bash
# exit on error
set -o errexit

#!/usr/bin/env bash
# exit on error
set -o errexit

# =================================================================
# =============== SECTION DE DÉBOGAGE : AFFICHER TOUT ===============
# =================================================================
echo "--- DÉBUT DU DÉBOGAGE ---"

echo "1. Qui suis-je et où suis-je ?"
whoami
pwd

echo "2. Quels sont les fichiers présents ici ?"
ls -la

echo "3. Est-ce que Poetry a bien été installé et quelle est sa version ?"
poetry --version

echo "4. Quelles dépendances sont listées dans pyproject.toml ?"
# Cette commande affiche les dépendances sans les installer
poetry show

echo "--- FIN DU DÉBOGAGE ---"
# =================================================================

echo "--- DÉBUT DU BUILD NORMAL ---"

poetry run python manage.py collectstatic --no-input
poetry run python manage.py migrate

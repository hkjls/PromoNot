import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

# Récupère le modèle utilisateur de votre projet Django
User = get_user_model()

class Command(BaseCommand):
    """
    Crée un superutilisateur s'il n'en existe pas déjà un.
    Utilise les variables d'environnement ADMIN_USER, ADMIN_EMAIL et ADMIN_PASSWORD.
    """
    help = 'Crée un superutilisateur non-interactivement s\'il n\'en existe pas.'

    def handle(self, *args, **options):
        # Récupère les identifiants depuis les variables d'environnement
        username = os.environ.get('ADMIN_USER')
        email = os.environ.get('ADMIN_EMAIL')
        password = os.environ.get('ADMIN_PASSWORD')

        # Vérifie si toutes les variables nécessaires sont définies
        if not all([username, email, password]):
            self.stdout.write(self.style.ERROR(
                'Les variables d\'environnement ADMIN_USER, ADMIN_EMAIL, et ADMIN_PASSWORD doivent être définies.'
            ))
            return

        # La logique "intelligente" : on ne crée l'utilisateur que s'il n'existe pas
        if not User.objects.filter(username=username).exists():
            self.stdout.write(self.style.SUCCESS(f"Création du superutilisateur '{username}'..."))
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(f"Superutilisateur '{username}' créé avec succès."))
        else:
            self.stdout.write(self.style.WARNING(f"Le superutilisateur '{username}' existe déjà. Aucune action n'est nécessaire."))  # noqa: E501

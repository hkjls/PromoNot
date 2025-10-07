Base de données : Pour le développement, la base de données par défaut de Django, SQLite (db.sqlite3), est absolument parfaite. C'est un simple fichier, c'est rapide et ça ne demande aucune configuration. En production, vous passerez très certainement à PostgreSQL.
Serveur Web (WSGI/ASGI) : Le serveur de développement de Django (manage.py runserver) est génial pour coder, mais il n'est pas fait pour supporter du vrai trafic. En production, vous utiliserez un serveur d'application comme Gunicorn ou Uvicorn.
Gestion des fichiers statiques (CSS, JS, Images) : Comme pour le serveur, le runserver de Django gère ça magiquement pour vous en développement. En production, il faudra une stratégie, par exemple en utilisant un outil comme Whitenoise ou en servant ces fichiers depuis un service externe (comme Amazon S3).

User Authorization failures
User authorization failures can happen. If a user chooses to Cancel the request, then a failure is triggered. Build your integration to handle these cases gracefully, as needed.

In some cases, Notion redirects the user to the redirect_uri that you set up when you created the public integration, along with an error query parameter. Notion uses the common error codes in the OAuth specification. Use the error code to create a helpful prompt for the user when they’re redirected here.

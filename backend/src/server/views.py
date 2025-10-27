import json
import os
import urllib.parse

from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

from .models import secretKeys
from .notionFallBack import listenNotionFallback


# Create your views here.
def homePage(request):
    response = listenNotionFallback(request)
    try:
        db_id = response.pop('id')
        defaults_data = response

        obj, created = secretKeys.objects.update_or_create(
            id=db_id,
            defaults=defaults_data
        )

        params = urllib.parse.urlencode({'userId': db_id})
        homePage = os.getenv("REACT_HOME_PAGE")

        if created:
            print('new user created')
        else:
            print(f'{obj.user} updated')
    except Exception as e:
        raise ValueError(e)

    return redirect(f'{homePage}?{params}')

@csrf_exempt
def webHook(request):
    # if request.method != 'POST':
    #     return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

    # try:
    #     data = json.loads(request.body)
    # except json.JSONDecodeError:
    #     return JsonResponse({'error': 'JSON malformé'}, status=400)

    # if 'challenge' in data:
    #     challenge_token = data.get('challenge')
    #     print(f"Vérification du webhook reçue. Challenge : {challenge_token}")
    #     return JsonResponse({'challenge': challenge_token})

    # signature_recue = request.headers.get('X-Notion-Signature')
    # secret_attendu = os.environ.get('NOTION_WEBHOOK_SECRET')

    # if not secret_attendu or signature_recue != secret_attendu:
    #     print("Erreur de signature : la signature reçue ne correspond pas.")
    #     return JsonResponse({'error': 'Signature invalide'}, status=403)

    # print("Webhook authentifié reçu de Notion :")
    # print(data)

    # return JsonResponse({'status': 'ok'}, status=200)
    if request.method == 'POST':
        print("--- NOUVELLE REQUÊTE WEBHOOK REÇUE ---")

        # 1. On affiche tous les en-têtes (headers) pour voir si la signature est là
        print("Headers de la requête :")
        for header, value in request.headers.items():
            print(f"  {header}: {value}")

        # 2. On affiche le corps brut de la requête (body) pour voir le JSON exact
        print("\nCorps brut de la requête (body) :")
        # On utilise .decode() pour transformer les bytes en une chaîne de caractères lisible
        body_content = request.body.decode('utf-8')
        print(body_content)

        print("--- FIN DE LA REQUÊTE ---")

        # 3. On répond toujours 200 OK pour que Notion ne se plaigne pas
        #    et qu'on puisse tranquillement analyser les logs.
        #    On essaie même de renvoyer le 'challenge' si on le trouve, au cas où.
        try:
            data = json.loads(body_content)
            if 'challenge' in data:
                return JsonResponse({'challenge': data['challenge']}, status=200)
        except:  # noqa: E722
            pass # On ignore les erreurs de JSON pour le moment

        return JsonResponse({'status': 'debug_ok'}, status=200)

    # Gérer les autres méthodes
    return JsonResponse({'error': 'Méthode non autorisée, POST attendu'}, status=405)

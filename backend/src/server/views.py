import json
import os
import urllib.parse

from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

from .models import WebhookIntegration, secretKeys
from .notionFallBack import listenNotionFallback


# Create your views here.
def homePage(request):
    response = listenNotionFallback(request)
    try:
        db_id = response['id']
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
    if request.method != 'POST':
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON malformé'}, status=400)

    if 'verification_token' in data:
        verification_token = data.get('verification_token')

        try:

            integration, created = WebhookIntegration.objects.get_or_create(
                app_name='Notion'
            )

            integration.verification_token = verification_token
            integration.save()

            return JsonResponse({'verification_token':verification_token})

        except Exception as e:
            return JsonResponse({'error': e}, status=500)

    signature_recue = request.headers.get('X-Notion-Signature')
    secret_attendu = os.environ.get('NOTION_WEBHOOK_SECRET')

    if not secret_attendu or signature_recue != secret_attendu:
        print("Erreur de signature : la signature reçue ne correspond pas.")
        return JsonResponse({'error': 'Signature invalide'}, status=403)

    return JsonResponse({'status': 'ok'}, status=200)

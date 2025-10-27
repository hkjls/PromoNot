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
    if request.method == 'POST':
        signature_notion = request.headers.get('X-Notion-Signature')
        secret_notion = os.environ.get('NOTION_WEBHOOK_SECRET')

        if signature_notion != secret_notion:
            return JsonResponse({'error':'Signature invalide'}, status=403)

        try:
            data = json.loads(request.body)

            print("webhook authenticated")
            print(data)

            return JsonResponse({'Status':'ok'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error':'JSON malforme'}, status=400)
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

from django.http import HttpRequest, HttpResponse, JsonResponse  # noqa: I001
from django.conf import settings # noqa: I001
from utils.encrypt import encrypt_token
import base64
import requests
import os

def listenNotionFallback(request: HttpRequest)-> object:
    authorization_code = request.GET.get('code')

    if not authorization_code:
        return HttpResponse("Erreur : Le code d'autorisation est manquant.", status=400)

    credentials_string = f"{settings.NOTION_CLIENT_ID}:{settings.NOTION_CLIENT_SECRET}"
    credentials_bytes = credentials_string.encode('utf-8')
    base64_bytes = base64.b64encode(credentials_bytes)
    base64_string = base64_bytes.decode('utf-8')

    token_url = os.getenv("TOKEN_URL")
    headers = {
        'Authorization': f'Basic {base64_string}',
        'Content-Type': 'application/json',
    }

    data = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': settings.NOTION_AUTH_URI, # L'URL de callback que vous avez con
    }

    response = requests.post(token_url, json=data, headers=headers)

    if response.status_code != 200:
        return JsonResponse({'error': 'Failed to authenticate with Notion'}, status=500)

    access_token = response.json().get('access_token')
    owner_info = response.json().get('owner')
    bot_id = response.json().get('bot_id')
    workspace_id = response.json().get('workspace_id')

    if not owner_info or 'user' not in owner_info:
        return JsonResponse({'error': 'Invalid data structure from Notion'}, status=500)

    user_info = owner_info.get('user')
    mail = user_info.get('person').get('email')

    if response.status_code != 200:
        return {
            'error':"Problem with the server"
        }

    return {
        'id':user_info.get('id'),
        'user':user_info.get('name'),
        'secretKey':encrypt_token(access_token),
        'notion_bot_id':bot_id,
        'notion_workspace_id':workspace_id,
        'email':mail
    }

import hashlib
import hmac
import json
import os
import urllib.parse

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
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

        params = urllib.parse.urlencode({
            'userId': db_id,
            'botId': response['notion_bot_id'],
            'workspaceId':response['notion_workspace_id']
        })
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
    request_body_bytes = request.body

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
    # secret_attendu = os.environ.get('NOTION_WEBHOOK_SECRET')

    if not signature_recue:
        return JsonResponse({'error': 'Signature manquant'}, status=403)

    try:
        notion_integration = WebhookIntegration.objects.get(app_name='Notion')
        secret_verification = notion_integration.verification_token
        if not secret_verification:
            raise WebhookIntegration.DoesNotExist
    except WebhookIntegration.DoesNotExist:
        return JsonResponse({'error':'Configuration manquante'}, status=500)

    digest = hmac.new(
        key=secret_verification,
        msg=request_body_bytes,
        digestmod=hashlib.sha256
    ).hexdigest()

    signature_sha=f"sha256={digest}"

    if not hmac.compare_digest(signature_recue, signature_sha):
        return JsonResponse({'error':'Signature Invalide'}, status=403)

    bot_id = None
    if 'accessible_by' in data:
        bot_obj = filter(lambda x:x['type']=='bot', data['accessible_by'])
        bot_id = bot_obj['id']

    if not bot_id:
        return JsonResponse({'status':'ok, no bot_id'}, status=200)

    try:
        secret_key_entry = secretKeys.objects.get(notion_bot_id=bot_id)
        user_notion_id = secret_key_entry.id
    except secretKeys.DoesNotExist:
        return JsonResponse({'status':'ok, user not found'}, status=200)

    channel_layer = get_channel_layer()
    group_name = f'notion_updates_{user_notion_id}'

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type':'notion_update_event',
            'data':data
        }
    )

    return JsonResponse({'status': 'ok'}, status=200)

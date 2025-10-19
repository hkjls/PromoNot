import urllib.parse

from django.shortcuts import redirect

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
        homePage = 'http://localhost:5173/home'

        if created:
            print('new user created')
        else:
            print(f'{obj.user} updated')
    except Exception as e:
        raise ValueError(e)

    return redirect(f'{homePage}?{params}')

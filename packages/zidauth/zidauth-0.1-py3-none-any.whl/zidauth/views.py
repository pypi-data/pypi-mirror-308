from django.conf import settings
from django.views.generic.base import RedirectView, View
from urllib.parse import urlencode
import os
import requests
from django.http import JsonResponse
from .consts import ZID_API_BASE_URL, ZID_OAUTH_BASE_URL
from .models import Token


class OAuthRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        queries = {
            'client_id': os.getenv('ZID_CLIENT_ID'),
            'redirect_uri': os.getenv('ZID_REDIRECT_URI'),
            'response_type': 'code',
        }
        oauth_url = f"{ZID_OAUTH_BASE_URL}/authorize?{urlencode(queries)}"

        return oauth_url


class CallbackView(View):
    def get(self, request):
        code = request.GET.get('code')

        if not code:
            return JsonResponse({'error': 'Missing authorization code'}, status=400)

        # Load credentials from environment variables
        client_id = os.getenv('ZID_CLIENT_ID')
        client_secret = os.getenv('ZID_CLIENT_SECRET')
        redirect_uri = os.getenv('ZID_REDIRECT_URI')

        payload = {
            'grant_type': 'authorization_code',
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
            'code': code
        }

        try:
            response = requests.post(f'{ZID_OAUTH_BASE_URL}/token', data=payload)
            response.raise_for_status()
            token_data = response.json()

            Token.objects.create(
                access_token=token_data.get('access_token', ''),
                refresh_token=token_data.get('refresh_token', ''),
                expires_in=token_data.get('expires_in', ''),
            )

            return JsonResponse(token_data)
        except requests.exceptions.HTTPError as err:
            return JsonResponse({'error': 'Failed to fetch token', 'details': str(err)}, status=response.status_code)
        except requests.exceptions.RequestException as err:
            return JsonResponse({'error': 'Request error', 'details': str(err)}, status=500)

from django.urls import path
from .views import OAuthRedirectView

urlpatterns = [
    path('oauth/redirect/', OAuthRedirectView.as_view(), name='oauth_redirect'),
    path('oauth/callback/', OAuthRedirectView.as_view(), name='oauth_redirect'),
]

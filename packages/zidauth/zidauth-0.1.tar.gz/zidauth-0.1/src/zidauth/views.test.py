from django.test import TestCase, RequestFactory
from src.zidauth.views import OAuthRedirectView


class TestOAuthRedirectView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = OAuthRedirectView()


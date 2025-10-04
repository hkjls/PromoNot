from django.test import TestCase

from ..authToNotion import AuthToNotion


class AuthenticationNotionTest(TestCase):

    def testConnection(self):

        auth = AuthToNotion()
        self.assertIsNotNone(auth)
        print(auth)
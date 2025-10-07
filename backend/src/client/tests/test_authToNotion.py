from django.test import TestCase

from ..requestNotion import Notion


class AuthenticationNotionTest(TestCase):

    def testConnection(self):

        auth = Notion()
        self.assertIsNotNone(auth.db_list)
        print(auth.db_list())

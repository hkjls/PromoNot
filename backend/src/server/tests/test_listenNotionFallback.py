from django.test import TestCase

from ..notionFallBack import listenNotionFallback


class ListenNotionFallbackTest(TestCase):

    def testReceivedData(self):
        data = listenNotionFallback()
        self.assertIsNotNone(data)

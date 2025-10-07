from notion_client import Client  # noqa: I001
import os

class Notion:
    def __init__(self):
        self.auth = Client(auth=os.getenv("NOTION_API_KEY"))

    def db_list(self):
        return self.auth.search(
            filter={"property": "object", "value": "database"}
        )

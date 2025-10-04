from notion_client import Client  # noqa: I001
import os

def AuthToNotion():
    notion = Client(auth=os.getenv("NOTION_API_KEY"))
    return notion.search(
        filter={"property": "object", "value": "page"}
    )

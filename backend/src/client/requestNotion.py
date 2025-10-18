import requests


class Notion:
    def __init__(self, notion_token:str):
        if not notion_token:
            raise ValueError("A Notion token must be provided.")

        self.headers = {
            "Authorization": "Bearer " + notion_token,
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",  # Utilise la dernière version stable de l'API
        }

        self.urls = {
            'search_endpoint': 'https://api.notion.com/v1/search',
        }

        self.payload = {
            "filter": {
                "value": "database",
                "property": "object"
            }
        }

    def db_list(self):
        response  = requests.post(
            self.urls['search_endpoint'],
            headers=self.headers,
            json=self.payload
        )

        print(response.json().get("has_more"))
        print(response.json().get("next_cursor"))

        if response.status_code == 200:
            return response.json()

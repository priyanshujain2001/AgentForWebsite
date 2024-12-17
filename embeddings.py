import requests
import os 
class GetEmbeddings:
    def __init__(self) -> None:
        
        pass

    def embed(self, text):
        url = 'https://api.jina.ai/v1/embeddings'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {os.environ.get("jina_api_key")}'
        }
        data = {
            "model": "jina-embeddings-v3",
            "task": "retrieval.query",
            "dimensions": 1024,
            "late_chunking": True,
            "embedding_type": "float",
            "input": [
                text
            ]
        }
        response = requests.post(url, headers=headers, json=data)
        return response.json()["data"][0]["embedding"]
    

    

    
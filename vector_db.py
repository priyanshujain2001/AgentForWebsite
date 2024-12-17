import logging
from typing import Dict, List, Tuple
import os
from embeddings import GetEmbeddings
import os
from pinecone import Pinecone, ServerlessSpec
import time





class VectorCli:
    # Existing __init__ and other methods...
    def __init__(self):
        self.__embeddings = GetEmbeddings()
        print(os.environ.get("pinecone_api_key"),"svbss")
        self.pc = Pinecone(api_key=os.environ.get("pinecone_api_key"))

        self.index = self.pc.Index("ragpipeline")
    def upsert_data_in_pinecone(self, data_dict):
        time.sleep(2)
        """Takes input a dict containing {"id": str(id), "values":[], "metadata":{"text": text of chunk}}"""
        self.index.upsert(vectors=[data_dict], namespace="set1")
    def update_index(self, texts, tags: Dict = {}):
        docs = []
        for text in texts:
            metadata ={"text": text}
            doc_id = str(hash(text))  # Generate a unique ID for each document
            metadata.update(tags)
            print(metadata)
            data_dict = {
                "id": doc_id,
                "values": self.__embeddings.embed(text),
                "metadata": metadata
            }
            print(data_dict["metadata"],"#######")
            self.upsert_data_in_pinecone(data_dict)
    

    def retriever(self, query):
        embed_query = self.__embeddings.embed(query)
        response = self.index.query(vector=embed_query, top_k=10, include_values=False, include_metadata=True, namespace="set1")
        text_retrieved = [{"text": match["metadata"]["text"], "tags": match["metadata"]} for match in response["matches"]]
        return text_retrieved

    
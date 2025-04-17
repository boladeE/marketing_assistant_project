import cohere
from typing import List
import numpy as np
from config import settings

class CohereEmbeddings:
    def __init__(self):
        self.settings = settings
        self.client = cohere.Client(self.settings.COHERE_API_KEY)
    
    def generate_embedding(self, text: str) -> np.ndarray:
        """Generate embeddings for a single text using Cohere."""
        response = self.client.embed(
            texts=[text],
            model="embed-english-v3.0",
            input_type="search_document"
        )
        return np.array(response.embeddings[0])
    
    def rerank_results(self, query: str, documents: List[str], top_n: int = 5) -> List[str]:
        """Rerank documents based on relevance to the query."""
        results = self.client.rerank(
            query=query,
            documents=documents,
            top_n=top_n,
            model="rerank-english-v2.0"
        )
        
        # Extract the reranked documents in order
        reranked_docs = []
        for result in results.results:
            # Get the document at the index returned by the rerank API
            doc_index = result.index
            if 0 <= doc_index < len(documents):
                reranked_docs.append(documents[doc_index])
        
        return reranked_docs 
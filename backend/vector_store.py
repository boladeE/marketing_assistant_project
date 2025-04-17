import faiss
import numpy as np
from typing import List, Dict
import json
import os
from config import settings

class VectorStore:
    def __init__(self):
        self.settings = settings
        self.index = None
        self.documents = []
        self._load_or_create_index()
    
    def _load_or_create_index(self):
        """Load existing index or create a new one."""
        # Create directory for index if it doesn't exist
        os.makedirs(os.path.dirname(self.settings.INDEX_PATH), exist_ok=True)
        
        if os.path.exists(self.settings.INDEX_PATH):
            self.index = faiss.read_index(self.settings.INDEX_PATH)
            # Load documents metadata
            metadata_path = self.settings.INDEX_PATH.replace(".faiss", "_metadata.json")
            if os.path.exists(metadata_path):
                with open(metadata_path, 'r') as f:
                    self.documents = json.load(f)
        else:
            self.index = faiss.IndexFlatL2(self.settings.VECTOR_DIMENSION)
    
    def add_documents(self, texts: List[str], embeddings: List[np.ndarray]):
        """Add new documents to the vector store."""
        if len(texts) != len(embeddings):
            raise ValueError("Number of texts and embeddings must match")
        
        # Add to FAISS index
        self.index.add(np.array(embeddings))
        
        # Update documents list
        for text in texts:
            self.documents.append({"text": text})
        
        # Save index and metadata
        self._save_index()
    
    def search(self, query_embedding: np.ndarray, k: int = 5) -> List[Dict]:
        """Search for similar documents."""
        distances, indices = self.index.search(
            query_embedding.reshape(1, -1).astype('float32'),
            k
        )
        
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx < len(self.documents):  # Ensure index is valid
                results.append({
                    "text": self.documents[idx]["text"],
                    "score": float(distance)
                })
        
        return results
    
    def _save_index(self):
        """Save the index and metadata to disk."""
        os.makedirs(os.path.dirname(self.settings.INDEX_PATH), exist_ok=True)
        faiss.write_index(self.index, self.settings.INDEX_PATH)
        
        # Save metadata
        metadata_path = self.settings.INDEX_PATH.replace(".faiss", "_metadata.json")
        with open(metadata_path, 'w') as f:
            json.dump(self.documents, f) 
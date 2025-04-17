import os
import json
from typing import List, Dict, Any
import numpy as np
from PyPDF2 import PdfReader
from embeddings import CohereEmbeddings
from vector_store import VectorStore
from config import settings

class BrandStyleManager:
    def __init__(self):
        self.settings = settings
        self.embeddings = CohereEmbeddings()
        self.vector_store = VectorStore()
        self.brand_voice = self._load_brand_voice()
        self.sample_campaigns = self._load_sample_campaigns()
    
    def _load_brand_voice(self) -> Dict[str, Any]:
        """Load brand voice guidelines from JSON."""
        file_path = "data/style_guidelines/brand_voice.json"
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _load_sample_campaigns(self) -> List[Dict[str, Any]]:
        """Load sample campaigns from JSON."""
        file_path = "data/past_campaigns/sample_campaigns.json"
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("campaigns", [])
        return []
    
    def _extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from a PDF file."""
        text = ""
        try:
            reader = PdfReader(pdf_path)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
        return text
    
    def _load_book_excerpts(self):
        """Load and index book excerpts from PDF files in the data directory."""
        book_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data")) 
        
        all_texts = []
        all_embeddings = []
        
        # Look for PDF files in the data directory
        for filename in os.listdir(book_dir):
            if filename.endswith(".pdf"):
                file_path = os.path.join(book_dir, filename)
                print(f"Processing PDF file: {file_path}")
                
                # Extract text from PDF
                content = self._extract_text_from_pdf(file_path)
                
                if not content:
                    print(f"No text extracted from {file_path}")
                    continue
                
                # Split content into chunks (simple splitting by paragraphs)
                chunks = [chunk.strip() for chunk in content.split('\n\n') if chunk.strip()]
                
                # Generate embeddings for each chunk
                for chunk in chunks:
                    if len(chunk) > 50:  # Only process chunks with sufficient content
                        embedding = self.embeddings.generate_embedding(chunk)
                        all_texts.append(chunk)
                        all_embeddings.append(embedding)
        
        # Add all content to the vector store
        if all_texts and all_embeddings:
            print(f"Adding {len(all_texts)} chunks to vector store")
            self.vector_store.add_documents(all_texts, all_embeddings)
        else:
            print("No content found to add to vector store")
    
    def get_relevant_context(self, prompt: str, k: int = 5) -> List[Dict]:
        """Get relevant context for a given prompt from book excerpts."""
        # Generate embedding for the prompt
        prompt_embedding = self.embeddings.generate_embedding(prompt)
        
        # Search for similar content in book excerpts
        results = self.vector_store.search(prompt_embedding, k=k)
        
        # Optionally rerank results
        if results:
            texts = [result["text"] for result in results]
            reranked = self.embeddings.rerank_results(prompt, texts, top_n=k)
            # Convert reranked results to the expected format
            return [{"text": text} for text in reranked]
        
        # If no results, return empty list
        return []
    
    def get_brand_voice(self) -> Dict[str, Any]:
        """Get brand voice guidelines."""
        return self.brand_voice
    
    def get_sample_campaigns(self) -> List[Dict[str, Any]]:
        """Get sample campaigns."""
        return self.sample_campaigns
    
    def update_book_excerpt(self, pdf_path: str):
        """Add new book excerpt from PDF to the vector store."""
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        # Extract text from PDF
        content = self._extract_text_from_pdf(pdf_path)
        
        if not content:
            raise ValueError(f"No text extracted from PDF: {pdf_path}")
        
        # Split content into chunks
        chunks = [chunk.strip() for chunk in content.split('\n\n') if chunk.strip()]
        
        # Generate embeddings for each chunk
        all_texts = []
        all_embeddings = []
        
        for chunk in chunks:
            if len(chunk) > 50:  # Only process chunks with sufficient content
                embedding = self.embeddings.generate_embedding(chunk)
                all_texts.append(chunk)
                all_embeddings.append(embedding)
        
        # Add to vector store
        if all_texts and all_embeddings:
            self.vector_store.add_documents(all_texts, all_embeddings)
            print(f"Added {len(all_texts)} chunks from {pdf_path} to vector store")
        else:
            print(f"No content extracted from {pdf_path}") 

# # Example usage
# if __name__ == "__main__":
#     brand_style_manager = BrandStyleManager()
    
#     # Example: Get relevant context for a marketing prompt
#     prompt = "Generate a marketing campaign for an Umbrella company"
#     context = brand_style_manager.get_relevant_context(prompt)
    
#     # Print the context in a readable format
#     print(f"Relevant context for prompt: '{prompt}'")
#     for i, item in enumerate(context):
#         print(f"\nReference {i+1}:")
#         print(item["text"])

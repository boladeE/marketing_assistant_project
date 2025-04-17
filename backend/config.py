from dataclasses import dataclass
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

@dataclass
class Settings:
    # API Keys
    COHERE_API_KEY: str
    DEEPSEEK_API_KEY: str
    
    # Vector Store Settings
    VECTOR_DIMENSION: int = 1024  # Cohere's embed-english-v3.0 model dimension
    INDEX_PATH: str = "data/vector_store/index.faiss"
    
    # Content Settings
    MAX_CONTEXT_LENGTH: int = 2000
    DEFAULT_MODEL: str = "deepseek-chat"
    
    # Brand Settings
    BRAND_TONE: str = "professional and empathetic"
    BRAND_VOICE: str = "Adriana James"
    
    @classmethod
    def from_env(cls):
        """Create a Settings instance from environment variables."""
        return cls(
            COHERE_API_KEY=os.getenv("COHERE_API_KEY", ""),
            DEEPSEEK_API_KEY=os.getenv("DEEPSEEK_API_KEY", ""),
            VECTOR_DIMENSION=int(os.getenv("VECTOR_DIMENSION", "1024")),
            INDEX_PATH=os.getenv("INDEX_PATH", "data/vector_store/index.faiss"),
            MAX_CONTEXT_LENGTH=int(os.getenv("MAX_CONTEXT_LENGTH", "2000")),
            DEFAULT_MODEL=os.getenv("DEFAULT_MODEL", "deepseek-chat"),
            BRAND_TONE=os.getenv("BRAND_TONE", "professional and empathetic"),
            BRAND_VOICE=os.getenv("BRAND_VOICE", "Adriana James")
        )

# Create a global settings instance
settings = Settings.from_env() 
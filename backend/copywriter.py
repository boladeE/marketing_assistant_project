from typing import List, Dict, Any
import requests
import json
from config import settings
from brand_style import BrandStyleManager

# Initialize brand style manager
brand_style_manager = BrandStyleManager()

class MarketingCopywriter:
    def __init__(self):
        self.settings = settings
        self.api_key = self.settings.DEEPSEEK_API_KEY
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
    
    def _build_prompt(self, prompt: str, context: List[Dict], content_type: str, tone: str, 
                     brand_voice: Dict[str, Any], sample_campaigns: List[Dict[str, Any]]) -> str:
        """Build a prompt for the LLM using context and parameters."""
        # Format context from book excerpts
        context_text = "\n".join([f"Reference {i+1}: {ctx['text']}" for i, ctx in enumerate(context)])
        
        # Format brand voice guidelines
        brand_voice_text = json.dumps(brand_voice, indent=2)
        
        # Format sample campaigns
        sample_campaigns_text = ""
        for i, campaign in enumerate(sample_campaigns):
            sample_campaigns_text += f"\nExample Campaign {i+1}:\n"
            sample_campaigns_text += f"Title: {campaign.get('title', '')}\n"
            sample_campaigns_text += f"Subject: {campaign.get('subject', '')}\n"
            sample_campaigns_text += f"Content:\n{campaign.get('content', '')}\n"
        
        return f"""You are a professional marketing copywriter for {self.settings.BRAND_VOICE}.
                    Your task is to create {content_type} content that matches the following request: {prompt}

                    BRAND VOICE GUIDELINES:
                    {brand_voice_text}

                    SAMPLE CAMPAIGNS:
                    {sample_campaigns_text}

                    RELEVANT BOOK EXCERPTS:
                    {context_text}

                    Guidelines:
                    1. Maintain a {tone} tone throughout
                    2. Follow {self.settings.BRAND_VOICE}'s brand voice guidelines
                    3. Be persuasive and engaging
                    4. Include a clear call-to-action
                    5. Keep the content concise and impactful
                    6. Ensure there is no special formatting in the output just plain text.
                    7. Make no reference to Adriana James.

                    Generate the marketing copy:
                    """

    def generate_copy(self, prompt: str, context: List[Dict], content_type: str, tone: str,
                     brand_voice: Dict[str, Any], sample_campaigns: List[Dict[str, Any]]) -> str:
        """Generate marketing copy using DeepSeek."""
        full_prompt = self._build_prompt(prompt, context, content_type, tone, brand_voice, sample_campaigns)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.settings.DEFAULT_MODEL,
            "messages": [
                {"role": "system", "content": "You are a professional marketing copywriter."},
                {"role": "user", "content": full_prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        response = requests.post(self.api_url, headers=headers, json=data)
        response.raise_for_status()
        
        return response.json()["choices"][0]["message"]["content"].strip()

def generate_marketing_copy(prompt: str) -> str:
    """Helper function to generate marketing copy."""
    copywriter = MarketingCopywriter()
    context = brand_style_manager.get_relevant_context(prompt)
    content_type = "email"
    tone = "professional and empathetic"
    brand_voice = brand_style_manager.get_brand_voice()
    sample_campaigns = brand_style_manager.get_sample_campaigns()
    return copywriter.generate_copy(prompt, context, content_type, tone, brand_voice, sample_campaigns) 
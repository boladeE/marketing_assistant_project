# Marketing Assistant AI

## Project Overview

Marketing Assistant AI is an AI-powered tool designed to streamline the process of ideation, copywriting, and marketing campaign creation. It generates marketing content in line with the brand tone and voice of Adriana James, producing drafts that can be validated and refined by a human marketer.

## Objectives

* Reduce the time required to generate marketing copy.
* Create content for emails, campaigns, social media, website copy, funnel pages, and more.
* Ensure the AI produces copywriting that aligns with the brand tone and voice of Adriana James.
* Allow ongoing updates to improve the AI’s performance and accuracy.

## Deliverables

* A custom-trained LLM fine-tuned for marketing and copywriting.
* Ability to generate copy in the same style and brand tone of Adriana James.

## Tech Stack

* **LLM** : Open-source or proprietary LLM fine-tuned for marketing.
* **Embeddings & Re-Ranking** : Cohere for embeddings and ranking results.
* **Backend** : FastAPI for API services.
* **Vector Database** : FAISS for content retrieval.
* **Storage** : Local storage for historical marketing data.

## File Structure

```
Marketing_Assistant_AI/
│-- backend/
│   │-- main.py  # FastAPI backend
│   │-- copywriter.py  # AI-powered copy generation module
│   │-- vector_store.py  # Manages vector database operations
│   │-- embeddings.py  # Generates embeddings using Cohere
│   │-- brand_style.py  # Ensures brand tone consistency
│   │-- config.py  # Configuration settings
│   │-- requirements.txt  # Dependencies
│
│-- data/
│   │-- past_campaigns/  # Stores past marketing campaigns
│   │-- user_queries/  # Stores past user queries for AI training
│   │-- style_guidelines/  # Reference materials for brand tone
│
│-- docs/
│   │-- README.md  # Documentation for new developers
│   │-- API_Documentation.md  # API details
│
│-- .env  # Environment variables
│-- .gitignore  # Git ignore file
│-- LICENSE  # License information
```

## Setup & Installation

### 1. Clone the Repository

```bash
git clone http://23.29.118.76:3000/Test/ds_task_marketing_assistant_ai
cd marketing-assistant-ai
```

### 2. Set Up the Backend

```bash
cd backend
pip install -r requirements.txt
python main.py
```

## AI Copywriting Process

1. **User Input** : The user submits a request (e.g., "Generate an email campaign for a product launch").
2. **Preprocessing** : The AI extracts key details and matches them with past marketing data.
3. **Generation** : The fine-tuned LLM creates a draft aligned with Adriana James' brand tone.
4. **Refinement** : The AI applies re-ranking to prioritize relevant content.
5. **Final Output** : The generated copy is displayed for user review and editing.

### Example API Usage

#### Generate Marketing Copy

```python
import requests

url = "http://localhost:8000/generate-copy"
data = {"prompt": "Write a social media post for our new product launch"}
response = requests.post(url, json=data)
print(response.json())
```

## Success Criteria

* AI generates copywriting that accurately reflects the brand tone.
* AI can be updated with new marketing materials.
* CRUD functionality to manage training data.
* AI adapts to new marketing trends and user queries.

# Marketing Assistant AI

## Project Overview

This project focuses on building a Marketing Assistant AI, an advanced tool designed to assist marketers in creating high-quality marketing content efficiently. The project leverages state-of-the-art AI technologies to generate content that aligns with specific brand tones and styles, ensuring consistency and professionalism.

## Objectives

* Develop an AI-powered system for generating marketing content.
* Enable the creation of diverse content types, including emails, social media posts, and website copy.
* Ensure the generated content adheres to predefined brand guidelines.
* Continuously improve the AI's performance through iterative updates.

## Deliverables

* A fine-tuned language model tailored for marketing and copywriting tasks.
* A backend system to manage content generation and retrieval.
* A structured dataset for training and refining the AI model.

## Tech Stack

* **Language Model** : Fine-tuned LLM for marketing content generation.
* **Embeddings & Ranking** : Cohere for embedding generation and result ranking.
* **Backend Framework** : FastAPI for API development.
* **Database** : FAISS for vector-based content retrieval.
* **Storage** : Local storage for historical data and training materials.

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

## Project Workflow

1. **Data Collection** : Gather historical marketing data and brand guidelines.
2. **Model Training** : Fine-tune the language model using the collected data.
3. **Backend Development** : Build APIs for content generation and retrieval.
4. **Testing & Validation** : Ensure the AI generates content that meets quality standards.
5. **Deployment** : Deploy the system for real-world usage.

## Example API Usage

#### Generate Marketing Copy

```python
import requests

url = "http://localhost:8000/generate-copy"
data = {"prompt": "Write a social media post for our new product launch"}
response = requests.post(url, json=data)
print(response.json())
```

## Success Criteria

* The system generates high-quality marketing content aligned with brand guidelines.
* The AI model can be updated with new data to improve performance.
* The backend supports efficient content retrieval and management.
